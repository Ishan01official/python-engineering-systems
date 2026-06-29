"""Concrete Loader implementations."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .protocols import Record


class JSONLinesLoader:
    """Writes one JSON object per line. Atomic via tempfile + replace."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self, records: Iterable[Record]) -> int:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        count = 0
        with open(tmp, "w", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, default=str))
                f.write("\n")
                count += 1
        tmp.replace(self.path)
        return count


class InMemoryLoader:
    """For tests: appends to a list. The list is the loader's `loaded` attribute."""

    def __init__(self):
        self.loaded: list[Record] = []

    def load(self, records: Iterable[Record]) -> int:
        self.loaded.extend(records)
        return len(self.loaded)
