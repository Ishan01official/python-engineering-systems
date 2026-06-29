# 02 — Context managers (the full picture)

Module 06.04 covered the basics. Here's the deeper material.

## The protocol

A context manager is any object with `__enter__` and `__exit__`. The `with` block:

```python
with cm as x:
    body
```

is equivalent to:

```python
x = cm.__enter__()
try:
    body
except Exception as exc:
    if not cm.__exit__(type(exc), exc, exc.__traceback__):
        raise
else:
    cm.__exit__(None, None, None)
```

`__exit__` returns `True` to *suppress* the exception. Almost always you want to let exceptions propagate, so return `None` (or `False`).

## Class-based

```python
import time

class Timer:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self                          # what gets bound by `as`

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        print(f"{self.name}: {elapsed:.3f}s")
        # returning None → don't suppress exceptions

with Timer("work") as t:
    do_stuff()
```

## Decorator-based (preferred for simple cases)

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.3f}s")
```

This is cleaner than the class version for stateless setup/teardown.

## `contextlib` essentials

```python
from contextlib import (
    contextmanager,        # decorator we just saw
    suppress,              # silently ignore specific exceptions
    closing,               # ensure .close() is called on anything
    ExitStack,             # manage a dynamic number of cms
    nullcontext,           # a no-op context manager — useful as a default
)

# suppress
with suppress(FileNotFoundError):
    Path("optional.txt").unlink()

# closing — for objects with .close() but no context-manager support
from urllib.request import urlopen
with closing(urlopen(url)) as response:
    data = response.read()

# nullcontext — when you sometimes want a context manager, sometimes not
def maybe_log(verbose: bool):
    cm = timer("op") if verbose else nullcontext()
    with cm:
        run()
```

## `ExitStack` — stacks of unknown size

When the number of context managers depends on runtime:

```python
from contextlib import ExitStack

def merge(*paths):
    with ExitStack() as stack:
        files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
        for line in chain(*files):
            yield line
```

`ExitStack` ensures *all* the files close in reverse order, even on exception, even if you can't write them as a fixed `with a, b, c:` block.

## Reusable vs single-use

A `@contextmanager`-decorated function returns a fresh context manager each call. The decorated function is the factory.

```python
@contextmanager
def opened(path):
    f = open(path)
    try:
        yield f
    finally:
        f.close()

# Each call makes a fresh cm:
with opened("a.txt") as f: ...
with opened("a.txt") as f: ...     # fine
```

A class-based context manager you've already entered cannot be re-entered. Make a new instance each time.

## Async context managers

For async code (Module 13), use `__aenter__` / `__aexit__` and `async with`:

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.text()
```

The `@asynccontextmanager` decorator from `contextlib` gives you the decorator-based form.

## Read deeper

- **FP** 2e, Ch. 18
- **LP** 6e, Ch. 36
- Python docs: `contextlib`
