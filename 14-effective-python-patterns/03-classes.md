# 03 — Classes

## Compose, don't always inherit

Inheritance often locks you in. Composition stays flexible. Default to composition; reach for inheritance only when you have a true is-a relationship and you'd otherwise repeat a lot of code.

## Use `@dataclass` for any record-like class

If your class is mostly fields with `__init__`, `__repr__`, `__eq__`, write `@dataclass`. You stop hand-rolling boilerplate, you stop forgetting to update `__repr__` after adding a field, and the class reads like its purpose.

## Implement `__repr__` for everything

A useful `__repr__` makes REPL debugging, log messages, and traceback values 10× more useful. The default `<Foo object at 0x7f...>` tells you nothing.

```python
def __repr__(self) -> str:
    return f"Account(owner={self.owner!r}, balance={self.balance})"
```

`@dataclass` writes this for you.

## Prefer `@property` for "looks like an attribute, behaves like one"

```python
class Rect:
    def __init__(self, w, h):
        self.w, self.h = w, h

    @property
    def area(self) -> float:
        return self.w * self.h
```

Callers write `r.area`, not `r.get_area()`. If you later need to validate or cache, you change the implementation, not the API.

## Hide implementation with a leading underscore

```python
class Cache:
    def __init__(self):
        self._items = {}      # internal; outsiders shouldn't poke at this
        self.size = 0          # public

    def add(self, key, value): ...
```

Python doesn't enforce, but readers respect. Avoid double underscores (`__name`) unless you have a specific name-mangling reason — they cause more confusion than they solve.

## Use ABCs or Protocols to declare interfaces

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def get(self, key: str) -> bytes: ...
    @abstractmethod
    def put(self, key: str, value: bytes) -> None: ...
```

Subclasses MUST implement abstract methods. Tools (mypy, IDEs) understand the contract. See Module 11 for Protocols, the structural alternative.

## Use `Self` for return types of "fluent" methods (3.11+)

```python
from typing import Self

class Builder:
    def with_name(self, name: str) -> Self:
        self.name = name
        return self
```

Now subclasses of `Builder` get the correctly-typed return without you re-annotating.

## Read deeper

- **EP** 3e — chapter on classes and interfaces
