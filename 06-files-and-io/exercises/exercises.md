# Module 06 — Exercises

## E06.1 — Stream a big "log"

Generate a fake log file with 100,000 lines (`for i in range(100_000): write...`). Then write a script that counts how many lines start with `"ERROR"` **without ever holding the whole file in memory**. Use a generator expression and `sum`.

## E06.2 — JSON round-trip with custom type

A dict contains a `datetime` object:
```python
record = {"event": "login", "at": datetime.now()}
```
Write `to_json(record)` and `from_json(text)` so the data survives a round trip. Pick a convention (ISO 8601) and stick with it.

## E06.3 — CSV → cleaned JSON

Given a CSV like:
```
name,age,city
Alice,30,Delhi
Bob, 25, Mumbai
Carol,, Bangalore
```
Write a script that:
1. Reads with `DictReader`.
2. Trims whitespace from every field.
3. Converts `age` to `int` (or `None` for missing).
4. Writes the result as `data.json` with `indent=2`.

## E06.4 — pathlib only

Refactor this `os.path`-based code to use `pathlib`:
```python
import os
base = "/tmp/data"
out = os.path.join(base, "processed", "users.csv")
os.makedirs(os.path.dirname(out), exist_ok=True)
ext = os.path.splitext(out)[1]
```

## E06.5 — Write your own context manager

Write `@contextmanager`-based `tempfile_named(suffix=".txt")` that yields a `Path` to a newly created temp file and deletes the file on exit (success OR exception). Test that the file is gone after the `with` block, even if an exception is raised inside it.

## E06.6 — Encoding bug

A file is failing to read with `UnicodeDecodeError`. The user "just wants to make it work". Why is `errors="ignore"` a bad solution? What's the right diagnostic and fix?
