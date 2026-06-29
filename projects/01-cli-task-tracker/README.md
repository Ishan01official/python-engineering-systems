# Project 1 — CLI task tracker

A command-line task manager. Persists tasks to a local JSON file. Built to consolidate modules 00–08.

## Goals

- Comfort with `argparse` (or its modern alternative, `click` / `typer`).
- File I/O with pathlib and JSON.
- A small class hierarchy and proper exception handling.
- A test suite that runs in under a second.

## Spec

```
tasks add "Write the report" --due 2026-07-01 --tag work
tasks list
tasks list --tag work --status open
tasks done 3
tasks delete 5
tasks stats
```

Storage: a single `~/.tasks.json` (overridable via `--store PATH`).

## Files

```
01-cli-task-tracker/
├── README.md
├── tasks_cli/
│   ├── __init__.py
│   ├── cli.py          # argparse setup + dispatch
│   ├── store.py        # load/save the JSON file
│   ├── models.py       # the Task dataclass
│   └── errors.py
├── tests/
│   ├── test_store.py
│   └── test_cli.py
└── pyproject.toml
```

## Stretch goals

- Add an `export` command that writes a CSV (uses Module 06).
- Add `--format json|table` to `list`.
- Add a `due_soon` command that filters by date arithmetic.
- Replace the JSON store with SQLite (`sqlite3` is stdlib).

## Starter scaffold

See the files below. They're a starting point, not a solution.
