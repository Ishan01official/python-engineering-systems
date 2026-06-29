"""Concrete Transformer implementations.

Each transformer is a small, testable, pure-ish unit.
"""
from __future__ import annotations

import time
from typing import Callable

from .protocols import Record


class RequiredFields:
    """Drops any record missing required fields."""

    def __init__(self, *fields: str):
        self.fields = fields

    def transform(self, record: Record) -> Record | None:
        for f in self.fields:
            if f not in record or record[f] is None or record[f] == "":
                return None
        return record


class CoerceTypes:
    """Coerces specified fields with the given callable. Drops the record on failure."""

    def __init__(self, **coercers: Callable):
        self.coercers = coercers

    def transform(self, record: Record) -> Record | None:
        out = dict(record)
        for field, fn in self.coercers.items():
            if field not in out:
                continue
            try:
                out[field] = fn(out[field])
            except (TypeError, ValueError):
                return None
        return out


class AddTimestamp:
    """Adds an `enriched_at` epoch-seconds field."""

    def __init__(self, field: str = "enriched_at", clock: Callable[[], float] = time.time):
        self.field = field
        self.clock = clock      # injectable so tests can pin the time

    def transform(self, record: Record) -> Record | None:
        out = dict(record)
        out[self.field] = int(self.clock())
        return out
