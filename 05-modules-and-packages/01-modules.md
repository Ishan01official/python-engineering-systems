# 01 — Modules

A **module** is just a `.py` file. When you write `import math`, Python finds `math.py` (or its compiled equivalent), executes it once, and gives you back a *module object* whose attributes are the names defined in that file.

## Creating a module

Make `mathx.py`:

```python
# mathx.py

PI = 3.14159265

def area_of_circle(r):
    return PI * r * r

def _internal_helper():
    """Underscore prefix is a convention for 'don't import this directly'."""
    return 42
```

Now from elsewhere:

```python
import mathx

print(mathx.PI)
print(mathx.area_of_circle(2))
```

That's it. There's no boilerplate, no "package declaration", no `module` keyword. Files are modules.

## The `if __name__ == "__main__":` idiom

When you run `python mathx.py`, Python sets the special variable `__name__` to `"__main__"`. When you `import mathx`, `__name__` is `"mathx"`.

This idiom lets a file be both **importable as a module** and **runnable as a script**:

```python
# mathx.py
def area_of_circle(r):
    return 3.14159 * r * r

if __name__ == "__main__":
    # This block runs only when executed directly, NOT on import.
    print(area_of_circle(5))
```

Every example file in this repo uses this pattern. Use it for your own.

## What "import" actually does

1. Find the module on the search path (`sys.path`).
2. Execute its top-level code, **once per process**. If you `import` the same module twice, the second import just rebinds the name.
3. Bind the result to the current namespace.

Side effects in module-level code (printing, opening files, hitting the network) happen on first import. **Keep import-time work to a minimum** — define functions and classes; don't *do* things.

## `import` forms

```python
import json                       # import the module; use as json.dumps(...)
import json as j                  # alias
from json import dumps, loads     # bind specific names
from json import dumps as to_json # alias on import
from json import *                # WILDCARD — almost always a bad idea
```

`from x import *` makes your namespace silently fill with whatever `x` exposes. Future you reading the file has no idea where `parse_record` came from. Avoid except in `__init__.py` re-exports.

## The standard library is huge

A non-exhaustive tour of "you probably need these eventually":

| Module | For |
|---|---|
| `os`, `os.path`, `pathlib` | Filesystem |
| `sys` | Python runtime |
| `json` | JSON read/write |
| `csv` | CSV read/write |
| `datetime` | Dates and times |
| `re` | Regular expressions |
| `collections` | `Counter`, `defaultdict`, `deque`, `OrderedDict` |
| `itertools` | Iteration primitives |
| `functools` | `partial`, `cache`, `reduce` |
| `typing` | Type hints |
| `dataclasses` | Auto-generated `__init__`, `__repr__`, `__eq__` |
| `logging` | Structured logging |
| `argparse` | CLI argument parsing |
| `subprocess` | Run external processes |
| `urllib.request` | HTTP (low-level; for serious work use `requests` or `httpx`) |
| `sqlite3` | SQLite client built in |
| `concurrent.futures` | Easy thread/process pools |
| `asyncio` | Async I/O |

This is your *first* search when looking for a library. Half the time the answer is already in the stdlib.

## Read deeper

- **LP** 6e, Part V — modules and packages, the definitive treatment.
