"""Task model and serialization helpers."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


@dataclass
class Task:
    id: int
    title: str
    status: str = "open"          # "open" | "done"
    tag: str | None = None
    due: date | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        if self.due is not None:
            d["due"] = self.due.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Task":
        due = d.get("due")
        return cls(
            id=d["id"],
            title=d["title"],
            status=d.get("status", "open"),
            tag=d.get("tag"),
            due=date.fromisoformat(due) if due else None,
        )

    def is_open(self) -> bool:
        return self.status == "open"
