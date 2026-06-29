# 04 — `dataclass`

When all your class does is "hold a few fields", writing `__init__`, `__repr__`, and `__eq__` by hand is busywork. `@dataclass` writes them for you.

## The basics

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str = ""           # field with a default
```

This gives you, for free:

- `__init__(self, name, age, email="")`
- `__repr__` → `Person(name='Ishan', age=25, email='')`
- `__eq__` → compares by field values

```python
p = Person("Ishan", 25)
print(p)              # Person(name='Ishan', age=25, email='')
p == Person("Ishan", 25)   # True
```

The annotations are mandatory — that's how `dataclass` knows what the fields are.

## Useful options

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

`frozen=True` makes instances immutable. Trying to do `p.x = 5` raises `FrozenInstanceError`. Also makes instances **hashable** (Python adds `__hash__` because immutable values are safe to hash).

```python
@dataclass(slots=True)
class Compact:
    a: int
    b: int
```

`slots=True` (Python 3.10+) tells Python to use `__slots__` — fixed attribute names, no per-instance `__dict__`. Saves memory and is faster for attribute access. Good for classes you'll instantiate millions of times.

```python
@dataclass(order=True)
class Score:
    value: int
    name: str
```

`order=True` adds `__lt__`, `__le__`, `__gt__`, `__ge__` based on field order. Now `Score` instances are sortable.

## Default factories — the mutable safety net

```python
from dataclasses import dataclass, field

@dataclass
class Cart:
    items: list[str] = field(default_factory=list)   # ← fresh list per instance
```

If you wrote `items: list[str] = []`, that's the mutable-default trap again — `dataclass` actually catches it and raises an error. Use `field(default_factory=list)` instead.

## Post-init validation

```python
@dataclass
class Range:
    start: int
    end: int

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"start > end: {self.start} > {self.end}")
```

`__post_init__` runs after the auto-generated `__init__`. Use it for cross-field validation.

## `dataclass` vs `NamedTuple` vs `dict`

| Need | Use |
|---|---|
| Immutable record with field access, no methods | `NamedTuple` |
| Mutable record with field access | `@dataclass` |
| Immutable record with field access + methods | `@dataclass(frozen=True)` |
| Quick ad-hoc record | `dict` |
| Performance-critical, many instances | `@dataclass(slots=True)` |
| Validation, parsing, schema, rich types | `pydantic.BaseModel` (third-party) |

For data engineering work specifically, `pydantic` is worth a look — it adds runtime validation on top of the dataclass idea. But the stdlib `dataclass` handles a huge fraction of cases.

## Read deeper

- Python docs: https://docs.python.org/3/library/dataclasses.html
- **FP** 2e, Ch. 5 — data class builders, including comparisons with `attrs`, `pydantic`, etc.
- **EP** 3e — items on dataclasses and immutability
