"""Protocols defining the three pipeline stages.

Using Protocols (Module 11) lets us swap implementations freely — any object
with the right shape qualifies.
"""
from __future__ import annotations

from typing import Iterable, Iterator, Protocol, runtime_checkable


Record = dict[str, object]


@runtime_checkable
class Extractor(Protocol):
    """Pulls records from a source. Returns an iterator so it can stream."""
    def extract(self) -> Iterator[Record]: ...


@runtime_checkable
class Transformer(Protocol):
    """Takes a record, returns a transformed one — or None to drop it."""
    def transform(self, record: Record) -> Record | None: ...


@runtime_checkable
class Loader(Protocol):
    """Writes records to a destination. Returns the count written."""
    def load(self, records: Iterable[Record]) -> int: ...
