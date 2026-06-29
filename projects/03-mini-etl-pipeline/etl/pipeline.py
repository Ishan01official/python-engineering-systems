"""The pipeline orchestrator — generic over any conforming stages."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from .protocols import Extractor, Loader, Record, Transformer


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RunResult:
    extracted: int
    transformed: int
    dropped: int
    loaded: int
    duration_ms: int


class Pipeline:
    """Wires an Extractor → list of Transformers → Loader.

    The transformers run in order. If any returns None, the record is dropped.
    """

    def __init__(self, extractor: Extractor, transformers: list[Transformer], loader: Loader):
        self.extractor = extractor
        self.transformers = transformers
        self.loader = loader

    def _apply_transformers(self, record: Record) -> Record | None:
        for t in self.transformers:
            record = t.transform(record)
            if record is None:
                return None
        return record

    def run(self) -> RunResult:
        start = time.perf_counter()

        extracted = 0
        transformed_iter = []
        dropped = 0
        for record in self.extractor.extract():
            extracted += 1
            out = self._apply_transformers(record)
            if out is None:
                dropped += 1
            else:
                transformed_iter.append(out)

        loaded = self.loader.load(transformed_iter)
        duration_ms = int((time.perf_counter() - start) * 1000)

        result = RunResult(
            extracted=extracted,
            transformed=len(transformed_iter),
            dropped=dropped,
            loaded=loaded,
            duration_ms=duration_ms,
        )
        logger.info("pipeline_done", extra=result.__dict__)
        return result
