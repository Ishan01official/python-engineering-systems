# 02 — Protocols (structural typing)

A `Protocol` describes a *shape*, not a class hierarchy. "Any object with these methods qualifies." This is duck typing made checkable.

## Why

Before Protocols, if you wanted "anything that can be iterated", you might:

- Annotate with `Iterable` from `typing` (works because the stdlib already defines `Iterable` as a Protocol-like ABC).
- Or accept anything and hope it works.

With Protocols, you define your own structural contracts:

```python
from typing import Protocol

class Closeable(Protocol):
    def close(self) -> None: ...

def safely_close(thing: Closeable) -> None:
    thing.close()
```

Any object with a `close()` method satisfies `Closeable` — without inheriting from it. Files, sockets, database connections, your own classes, all pass.

## A more useful example

You're writing a function that wants to accept anything supporting `read()`. Files do, but so do `io.StringIO`, `io.BytesIO`, network streams, custom test doubles.

```python
from typing import Protocol

class Readable(Protocol):
    def read(self, size: int = -1) -> bytes: ...

def head(src: Readable, n: int) -> bytes:
    return src.read(n)
```

With `Readable`, your function signature is honest: "give me something with `.read(size)`". You don't need a common base class. The caller doesn't need to know your Protocol type exists.

## `runtime_checkable`

By default Protocols only work for static checking. Adding `@runtime_checkable` makes them work with `isinstance`:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

isinstance(my_file, Closeable)     # True if my_file has a .close method
```

`runtime_checkable` only verifies method *existence*, not signatures — so it's a weaker check. Don't lean on it.

## Stdlib Protocols you'll meet

In `typing` and `collections.abc`:

| Protocol | Means "supports..." |
|---|---|
| `Iterable[T]` | `for x in obj` |
| `Iterator[T]` | `next(obj)` |
| `Sequence[T]` | indexing, len, contains |
| `Mapping[K, V]` | dict-like read access |
| `MutableMapping[K, V]` | dict-like read + write |
| `Sized` | `len(obj)` |
| `Container[T]` | `x in obj` |
| `Hashable` | usable as dict key |
| `Callable[[args], return]` | `obj(...)` |
| `SupportsInt`, `SupportsFloat`, `SupportsIndex`, ... | conversion protocols |

In function annotations, use the most-general Protocol that fits. "Takes a list" is often too narrow — "takes an iterable" is more useful to callers.

## Protocols vs ABCs

ABCs require inheritance: a class must explicitly say "I'm a `MutableMapping`". Protocols don't: any matching shape qualifies.

In modern Python, **prefer Protocols** for new abstractions. Use ABCs when:

- You want to share implementation, not just shape.
- You want runtime enforcement that subclasses implement all abstract methods.

## Read deeper

- **EP** 3e — items on Protocols and structural typing
- **FP** 2e, Ch. 13 — interfaces, Protocols, and ABCs side-by-side
- PEP 544 — the design document for Protocols
