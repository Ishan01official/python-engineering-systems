"""JSON-backed persistence for tasks."""
from __future__ import annotations

import json
from pathlib import Path

from .errors import TaskNotFound
from .models import Task


class TaskStore:
    """A flat list of tasks stored as JSON.

    The file is rewritten on every save (atomic via tempfile + replace).
    Fine for hundreds of tasks; if you grow to millions, switch to SQLite.
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> list[Task]:
        if not self.path.exists():
            return []
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(d) for d in raw]

    def save(self, tasks: list[Task]) -> None:
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(
            json.dumps([t.to_dict() for t in tasks], indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.path)        # atomic on POSIX

    def add(self, task: Task) -> Task:
        tasks = self.load()
        if task.id == 0:
            task.id = max((t.id for t in tasks), default=0) + 1
        tasks.append(task)
        self.save(tasks)
        return task

    def get(self, task_id: int) -> Task:
        for t in self.load():
            if t.id == task_id:
                return t
        raise TaskNotFound(task_id)

    def update(self, task_id: int, **fields) -> Task:
        tasks = self.load()
        for i, t in enumerate(tasks):
            if t.id == task_id:
                for k, v in fields.items():
                    setattr(t, k, v)
                tasks[i] = t
                self.save(tasks)
                return t
        raise TaskNotFound(task_id)

    def delete(self, task_id: int) -> None:
        tasks = self.load()
        new = [t for t in tasks if t.id != task_id]
        if len(new) == len(tasks):
            raise TaskNotFound(task_id)
        self.save(new)
