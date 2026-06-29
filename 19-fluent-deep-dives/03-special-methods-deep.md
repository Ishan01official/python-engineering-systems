# 03 — Special methods in earnest

Module 08.03 covered the common dunders. This is the level beneath.

## Reflected operators (`__radd__`, `__rmul__`, etc.)

Normally `a + b` calls `a.__add__(b)`. If `a` doesn't know how to add a `b`, Python tries `b.__radd__(a)`.

```python
class Money:
    def __init__(self, cents): self.cents = cents
    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.cents + other.cents)
        return NotImplemented
    def __radd__(self, other):
        # Lets sum([m1, m2, m3]) start from 0 + m1
        if other == 0:
            return self
        return NotImplemented
```

Without `__radd__`, `sum([Money(100), Money(200)])` fails because it starts with `0 + Money(...)` — and `int.__add__` doesn't know what to do.

## In-place operators (`__iadd__`, `__imul__`, ...)

`a += b` first tries `a.__iadd__(b)`; if missing, falls back to `a = a + b`. For mutable types, `__iadd__` should mutate `self` and return `self`. For immutable types, don't implement it — the fallback path is correct.

```python
class Counter:
    def __init__(self, n=0): self.n = n
    def __iadd__(self, other):
        self.n += other
        return self        # MUST return self
```

## `__hash__` and `__eq__` together

Rule: objects that compare equal must hash equal. The reverse isn't required (collisions are fine).

If you define `__eq__`, Python sets `__hash__` to `None` (making the class unhashable) unless you also define `__hash__`. This is a safety net for mutable types — a mutable object whose hash changes is poison in a dict.

For immutable value types, implement both:

```python
class Point:
    def __init__(self, x, y):
        self.__dict__["x"] = x      # bypass any __setattr__ to make it frozen
        self.__dict__["y"] = y
    def __eq__(self, o):
        return isinstance(o, Point) and (self.x, self.y) == (o.x, o.y)
    def __hash__(self):
        return hash((self.x, self.y))
```

Or just use `@dataclass(frozen=True)`.

## Descriptors

A descriptor is an object that implements `__get__` (and optionally `__set__`, `__delete__`) and is used as a class attribute. They're what make `@property` work.

```python
class Validated:
    def __init__(self, minimum=0):
        self.minimum = minimum
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        return obj.__dict__[self.name]
    def __set__(self, obj, value):
        if value < self.minimum:
            raise ValueError(f"{self.name} must be >= {self.minimum}")
        obj.__dict__[self.name] = value


class Account:
    balance = Validated(minimum=0)

a = Account()
a.balance = 100     # OK
a.balance = -10     # ValueError
```

Descriptors power ORMs (Django, SQLAlchemy), validation libraries (Pydantic v1), and `@property` itself. Worth knowing they exist; you'll rarely need to write one outside a library.

## `__init_subclass__` and `__set_name__`

These let parent classes hook into subclass creation. Used heavily by libraries to register plugins, enforce conventions, or wire up metadata. Not for everyday application code.

## `__call__` makes an instance callable

```python
class Multiplier:
    def __init__(self, factor): self.factor = factor
    def __call__(self, x):       return x * self.factor

triple = Multiplier(3)
triple(10)        # 30
```

Useful when you want a stateful callable — a "function with memory". `functools.partial` does a lot of this for you; `__call__` is the manual form.

## Read deeper

- **FP** 2e, Ch. 11 (Pythonic objects), Ch. 12 (sequences), Ch. 16 (operator overloading), Ch. 23 (descriptors)
