# 03 — Generics

A generic function or class can work with multiple types while keeping them connected. Example: a stack of `int`s should give back `int`s, not `Any`.

## The modern syntax (3.12+)

```python
def first[T](items: list[T]) -> T:
    return items[0]
```

The `[T]` declares a type variable scoped to this function. The hint says "this function takes a list of *some* T and returns a T of the same kind".

`first([1, 2, 3])` → `T = int`, return type is `int`.
`first(["a", "b"])` → `T = str`, return type is `str`.

## The older syntax (3.5+) — still common

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]
```

Same behavior, more verbose. New code can use the 3.12+ form; older code uses `TypeVar`.

## Generic classes

```python
# 3.12+
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

s: Stack[int] = Stack()
s.push(1)
s.push("nope")        # mypy: argument has incompatible type "str"; expected "int"
```

## Bounded type variables

Restrict T to a particular hierarchy:

```python
class Numeric(Protocol):
    def __add__(self, other): ...

def total[T: Numeric](items: list[T]) -> T:
    result = items[0]
    for x in items[1:]:
        result = result + x
    return result
```

Now T is "anything that supports `+`". The function accepts ints, floats, your custom money type — but not strings (well, strings do support `+`, so they would qualify; the example is illustrative).

## Constraints (a set of allowed types)

```python
from typing import TypeVar
T = TypeVar("T", int, float)        # T must be int OR float, not "either int or float"

def avg(xs: list[T]) -> T: ...
```

## Variance — the brief version

This part is technical and you'll rarely write it yourself, but you'll *encounter* it:

- `list[Dog]` is NOT a subtype of `list[Animal]`. (Otherwise you could put a `Cat` in a list typed as `list[Dog]`.)
- `Sequence[Dog]` IS a subtype of `Sequence[Animal]`. (Because Sequence is read-only.)

Tooling handles this automatically. The takeaway: prefer the most general type in function signatures (`Iterable`, `Sequence`, `Mapping`) so callers have flexibility.

## When generics earn their cost

- **Containers and data structures.** A generic `Cache[K, V]` is much more useful than a non-generic one.
- **Higher-order functions** that pass values through. `def first[T](items: list[T]) -> T` preserves the caller's type.
- **Library code** with reusable abstractions.

For application code calling specific types, generics are usually overkill. Plain hints work.

## Read deeper

- **EP** 3e — items on type variables
- **FP** 2e, Ch. 15 — typing with generics and Protocols together
- mypy generics docs
