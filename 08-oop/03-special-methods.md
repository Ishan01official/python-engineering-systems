# 03 — Special methods (dunders)

Python's **data model** is the protocol for how objects interact with built-in operations. Implementing dunder methods plugs your class into the language.

The most important dunders:

| Dunder | What it enables |
|---|---|
| `__init__` | construction |
| `__repr__` | unambiguous string (for developers, REPL, debugger) |
| `__str__` | human-readable string (for users, `print`) |
| `__eq__` | `==` |
| `__hash__` | use as dict key / set element |
| `__lt__`, `__le__`, `__gt__`, `__ge__` | `<`, `<=`, `>`, `>=` (and sortability) |
| `__len__` | `len(obj)` |
| `__bool__` | truthiness in `if`/`while` |
| `__iter__`, `__next__` | iteration |
| `__contains__` | `x in obj` |
| `__getitem__`, `__setitem__` | `obj[key]` |
| `__call__` | `obj(...)` — makes the instance callable |
| `__enter__`, `__exit__` | context manager (`with`) |
| `__add__`, `__mul__`, etc. | operator overloading |

## A concrete example

```python
class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: "Vector") -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self) -> bool:
        return bool(abs(self))
```

Now your class behaves like a built-in:

```python
v = Vector(3, 4)
print(v)                          # uses __repr__ in REPL, __str__ in print (here repr is fallback)
v + Vector(1, 1)                  # Vector(4, 5)
abs(v)                            # 5.0
bool(v)                           # True
{v: "origin offset"}              # works as a dict key because __hash__ is defined
```

## `__repr__` vs `__str__`

- `__repr__` — unambiguous, ideally something you could paste back into Python to recreate the object. For debugging.
- `__str__` — friendly to read. Used by `print()`.

If you only implement one, implement `__repr__`. Python falls back to it for `str()`.

```python
class Person:
    def __init__(self, name, age):
        self.name, self.age = name, age

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age})"
```

```python
>>> p = Person("Ishan", 25)
>>> p
Person(name='Ishan', age=25)
>>> print(p)
Person(name='Ishan', age=25)
```

## `__eq__` and `__hash__` go together

- If you define `__eq__`, define `__hash__` too — or Python will set `__hash__` to `None` and your class won't be hashable.
- Two objects that are `==` MUST have the same hash. (The reverse isn't required.)
- For mutable objects with content-based equality, the safest is to leave them unhashable.

## `__iter__` for "this object is iterable"

```python
class CountDown:
    def __init__(self, start: int):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

for x in CountDown(3):
    print(x)        # 3, 2, 1
```

`yield` turns the method into a generator — see Module 09.

## Read deeper

- **FP** 2e, Ch. 1 — "The Python Data Model" is the seminal explanation; if you read one chapter of one book, read this.
- **LP** 6e, Ch. 30 (operator overloading)
- **EP** 3e — items on `__repr__`, equality and hashing, custom containers.
