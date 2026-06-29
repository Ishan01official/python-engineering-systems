"""Concrete Extractor implementations."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from .protocols import Record


class JSONLinesExtractor:
    """Reads one JSON object per line from a file. Streams — works on big files."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def extract(self) -> Iterator[Record]:
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)


class InMemoryExtractor:
    """For tests: yields from a list."""

    def __init__(self, records: list[Record]):
        self.records = records

    def extract(self) -> Iterator[Record]:
        yield from self.records
