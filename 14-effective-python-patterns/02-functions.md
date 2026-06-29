# 02 — Functions

## Force keyword-only arguments for clarity

```python
# bad — what do True/False mean at the call site?
def open_file(path, True, False, 1024): ...

# good — readable calls
def open_file(path, *, write=False, append=False, buffer_size=1024): ...
open_file("data.csv", write=True, buffer_size=4096)
```

The `*` in the signature makes everything after it keyword-only.

## Return multiple values via NamedTuple/dataclass once you exceed 2–3

```python
# bad — what does result[2] mean?
def stats(xs):
    return min(xs), max(xs), sum(xs)/len(xs), len(xs), variance(xs)

# good
@dataclass(frozen=True)
class Stats:
    min: float
    max: float
    mean: float
    n: int
    variance: float

def stats(xs) -> Stats: ...
```

## Don't suppress exceptions to "make it work"

```python
# bad
try:
    risky()
except Exception:
    pass

# better: explicit about what you're ignoring and why
from contextlib import suppress
with suppress(FileNotFoundError):
    Path("optional.cfg").unlink()
```

## Use `*args` and `**kwargs` only when you really need them

They obscure the signature. Spell out the parameters when you can.

## Prefer generators for sequence-producing functions

```python
# bad — builds the whole list eagerly
def even_squares(n):
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i * i)
    return result

# good — streamable, O(1) memory
def even_squares(n):
    for i in range(n):
        if i % 2 == 0:
            yield i * i
```

Callers can still do `list(even_squares(100))` if they really need a list.

## Use `*args` to forward arguments verbatim

When wrapping a function:

```python
def with_retries(fn, *args, **kwargs):
    for _ in range(3):
        try:
            return fn(*args, **kwargs)
        except Exception:
            continue
    raise
```

This passes everything through transparently.

## Read deeper

- **EP** 3e — chapter on functions, items on default arguments, keyword-only, generators, exceptions
