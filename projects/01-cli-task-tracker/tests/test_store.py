"""Tests for the TaskStore.

Run from the project root:
    python -m pytest tests/ -v
"""
from datetime import date
from pathlib import Path

import pytest

from tasks_cli.errors import TaskNotFound
from tasks_cli.models import Task
from tasks_cli.store import TaskStore


@pytest.fixture
def store(tmp_path: Path) -> TaskStore:
    return TaskStore(tmp_path / "tasks.json")


def test_empty_store_load_returns_empty_list(store):
    assert store.load() == []


def test_add_assigns_incrementing_ids(store):
    t1 = store.add(Task(id=0, title="first"))
    t2 = store.add(Task(id=0, title="second"))
    assert t1.id == 1
    assert t2.id == 2


def test_add_persists_to_disk(store):
    store.add(Task(id=0, title="hello"))
    reloaded = TaskStore(store.path)
    assert reloaded.load()[0].title == "hello"


def test_update_changes_status(store):
    t = store.add(Task(id=0, title="thing"))
    store.update(t.id, status="done")
    assert store.get(t.id).status == "done"


def test_get_unknown_raises(store):
    with pytest.raises(TaskNotFound):
        store.get(999)


def test_delete_unknown_raises(store):
    with pytest.raises(TaskNotFound):
        store.delete(999)


def test_due_roundtrips_as_date(store):
    store.add(Task(id=0, title="due-thing", due=date(2026, 7, 1)))
    reloaded = TaskStore(store.path).load()
    assert reloaded[0].due == date(2026, 7, 1)
