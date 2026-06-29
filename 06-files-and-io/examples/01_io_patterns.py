"""
File I/O patterns — text, JSON, CSV, paths, context managers.

Run:
    python 06-files-and-io/examples/01_io_patterns.py
"""
import csv
import json
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path


def text_file_streaming() -> None:
    print("--- Stream a file line by line ---")
    # Use a temp directory so we don't leave junk around.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "log.txt"
        path.write_text(
            "INFO  hello\nERROR  bad thing\nINFO  done\nERROR  another\n",
            encoding="utf-8",
        )
        errors = 0
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("ERROR"):
                    errors += 1
        print(f"  {errors} error lines")
    print()


def json_roundtrip() -> None:
    print("--- JSON round-trip ---")
    record = {
        "user": "ishan",
        "scores": [88, 73, 91],
        "active": True,
        "metadata": None,
    }
    text = json.dumps(record, indent=2)
    parsed = json.loads(text)
    print(text)
    assert parsed == record
    print()


def csv_with_dictwriter() -> None:
    print("--- CSV with DictReader/DictWriter ---")
    rows = [
        {"name": "Alice", "age": 30, "city": "Delhi"},
        {"name": "Bob",   "age": 25, "city": "Mumbai"},
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "users.csv"
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "age", "city"])
            writer.writeheader()
            writer.writerows(rows)

        # Now read it back
        with open(path, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                print(f"  {r}")
    print()


def pathlib_examples() -> None:
    print("--- pathlib usage ---")
    p = Path("data") / "raw" / "users.csv"
    print(f"  full path:   {p}")
    print(f"  parent:      {p.parent}")
    print(f"  name:        {p.name}")
    print(f"  stem:        {p.stem}")
    print(f"  suffix:      {p.suffix}")
    print(f"  new ext:     {p.with_suffix('.parquet')}")
    print()


@contextmanager
def timer(name: str):
    """A reusable timing context manager."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  {name}: {elapsed * 1000:.2f} ms")


def custom_context_manager_demo() -> None:
    print("--- Custom context manager ---")
    with timer("dummy work"):
        sum(i * i for i in range(100_000))
    print()


if __name__ == "__main__":
    text_file_streaming()
    json_roundtrip()
    csv_with_dictwriter()
    pathlib_examples()
    custom_context_manager_demo()
