"""Command-line interface."""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from .errors import TaskError
from .models import Task
from .store import TaskStore


DEFAULT_STORE = Path.home() / ".tasks.json"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="tasks", description="A tiny task tracker.")
    p.add_argument("--store", type=Path, default=DEFAULT_STORE)
    sub = p.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", help="Add a task")
    add.add_argument("title")
    add.add_argument("--tag")
    add.add_argument("--due", type=date.fromisoformat)

    lst = sub.add_parser("list", help="List tasks")
    lst.add_argument("--tag")
    lst.add_argument("--status", choices=["open", "done"])

    done = sub.add_parser("done", help="Mark a task done")
    done.add_argument("id", type=int)

    delete = sub.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int)

    sub.add_parser("stats", help="Show counts")

    return p.parse_args(argv)


def render_task(t: Task) -> str:
    marker = "[x]" if t.status == "done" else "[ ]"
    due = f" due {t.due.isoformat()}" if t.due else ""
    tag = f" #{t.tag}" if t.tag else ""
    return f"{marker} {t.id:3d}  {t.title}{tag}{due}"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    store = TaskStore(args.store)

    try:
        if args.cmd == "add":
            t = store.add(Task(id=0, title=args.title, tag=args.tag, due=args.due))
            print(render_task(t))

        elif args.cmd == "list":
            tasks = store.load()
            if args.tag:
                tasks = [t for t in tasks if t.tag == args.tag]
            if args.status:
                tasks = [t for t in tasks if t.status == args.status]
            for t in tasks:
                print(render_task(t))

        elif args.cmd == "done":
            t = store.update(args.id, status="done")
            print(render_task(t))

        elif args.cmd == "delete":
            store.delete(args.id)
            print(f"deleted {args.id}")

        elif args.cmd == "stats":
            tasks = store.load()
            open_n = sum(1 for t in tasks if t.is_open())
            done_n = len(tasks) - open_n
            print(f"open: {open_n}   done: {done_n}   total: {len(tasks)}")

    except TaskError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
