# Module 08 — Exercises

## E08.1 — Define a class

Build `class Stack` with `push`, `pop`, `peek`, `__len__`, `__bool__`, and `__repr__`. Make `bool(stack)` return False when empty. Make `len(stack)` return the size. Make `repr(stack)` show the items top-to-bottom.

## E08.2 — Inheritance: shape area

Make an abstract base class `Shape` with an abstract method `area()`. Subclass it for `Circle(radius)`, `Rectangle(w, h)`, `Square(side)`. Show that `Square` is best implemented as a subclass of `Rectangle`, not `Shape` directly. Avoid repeating `area()` logic.

## E08.3 — Dunder showdown

Make a `Money` class wrapping an integer number of cents. Implement:
- `__init__(cents)`, `__repr__`, `__str__` (formatted as `$X.YY`)
- `__eq__`, `__hash__`
- `__add__` and `__sub__` (only with other `Money`)
- `__lt__` so `sorted([m1, m2, m3])` works
- `__mul__(scalar)` and `__rmul__(scalar)` so `3 * money` works too

## E08.4 — Promote to dataclass

Refactor this class to `@dataclass`. Keep the same public API.
```python
class User:
    def __init__(self, id, name, email, tags=None):
        self.id = id
        self.name = name
        self.email = email
        self.tags = tags if tags is not None else []

    def __repr__(self):
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r}, tags={self.tags})"

    def __eq__(self, other):
        return isinstance(other, User) and (self.id, self.name, self.email, self.tags) == \
               (other.id, other.name, other.email, other.tags)
```

## E08.5 — Composition vs inheritance

You're modeling notifications. You can send via Email, SMS, or Push. They can also be Urgent or Scheduled. Sketch a design using composition (NOT a class hierarchy) where adding a new transport doesn't require touching `Notification`. Just outline the classes and signatures.

## E08.6 — `__post_init__` validation

```python
@dataclass
class DateRange:
    start: date
    end: date
```
Add validation that raises `ValueError` if `start > end`. Use `__post_init__`.

## E08.7 — Don't trip the class-attribute mutable trap

What's wrong with this class? Fix it.
```python
class Cart:
    items = []
    def add(self, item):
        self.items.append(item)
```
