# 04 — Context managers and `with`

## What `with` actually does

```python
with open("f.txt") as f:
    data = f.read()
```

is roughly equivalent to:

```python
f = open("f.txt")
try:
    data = f.read()
finally:
    f.close()
```

The `with` block guarantees the cleanup runs **even if an exception is raised inside**. That guarantee is the entire point.

Any object that implements the **context manager protocol** (`__enter__` and `__exit__`) can be used in `with`.

## Built-in context managers worth knowing

```python
# Files — the canonical example
with open(path) as f: ...

# Locks
import threading
lock = threading.Lock()
with lock:                       # acquires, releases on exit
    critical_section()

# Suppress an exception silently
from contextlib import suppress
with suppress(FileNotFoundError):
    Path("might_not_exist").unlink()

# Temporary directory (auto-deleted on exit)
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    work_in(tmpdir)              # tmpdir is wiped after the block

# Database connection (most clients)
import sqlite3
with sqlite3.connect(db_path) as conn:
    conn.execute("...")
```

## Multiple managers in one `with`

```python
with open("in.csv") as src, open("out.csv", "w") as dst:
    for line in src:
        dst.write(line.upper())
```

Both files close at the end of the block, in reverse order. Easier to read than nested `with` blocks.

## Writing your own

The easiest way is `@contextlib.contextmanager`:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    start = time.perf_counter()
    try:
        yield                       # control returns to the `with` block here
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.3f}s")

# Use it
with timer("load data"):
    big_load()
```

The contract: code before `yield` is the setup; code after is the teardown; whatever's in the `with` block runs at the `yield` point. The `try`/`finally` ensures teardown runs even on exceptions.

The other way is implementing the protocol explicitly with `__enter__` and `__exit__` on a class. The decorator-based form covers 90% of cases.

## When to use a context manager

Anywhere you have a "must be paired" setup/teardown:

- Opening / closing a resource (file, socket, connection)
- Acquiring / releasing a lock
- Starting / stopping a timer
- Setting / restoring config (e.g. temporarily setting a log level)
- Entering / exiting a transaction

The pattern is: "do X; later, undo X — and make sure undo always runs."

## Read deeper

- **LP** 6e, Ch. 36 — context managers in detail.
- **FP** 2e, Ch. 18 — `with`, `match`, and `else` blocks.
- **EP** 3e — items on `contextlib` and reusable setup/teardown.
