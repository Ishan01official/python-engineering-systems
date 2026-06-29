# 01 — Classes and objects

A class is a **blueprint**; an instance is an **object** made from that blueprint.

```python
class Circle:
    def __init__(self, radius: float):
        self.radius = radius           # instance attribute

    def area(self) -> float:
        return 3.14159 * self.radius ** 2


c = Circle(5)                          # create an instance
print(c.radius)                        # 5
print(c.area())                        # 78.53...
```

## `__init__` and `self`

- `__init__` is the *initializer* (not the constructor — `__new__` is, but you almost never touch it). It runs after the instance is created, to set up its state.
- `self` is the convention for the first argument of any method. It's the instance the method is being called on. When you write `c.area()`, Python translates that into `Circle.area(c)`.

`self` isn't a keyword. You could name it anything. Don't.

## Instance vs class attributes

```python
class Dog:
    species = "Canis familiaris"      # CLASS attribute — shared by all dogs

    def __init__(self, name: str):
        self.name = name              # INSTANCE attribute — per dog
```

```python
fido = Dog("Fido")
rex = Dog("Rex")

print(fido.name)        # Fido
print(rex.name)         # Rex
print(fido.species)     # Canis familiaris
print(Dog.species)      # Canis familiaris (also accessible on the class)
```

**Don't put mutable values as class attributes** unless you mean to share them across all instances — same trap as mutable default arguments:

```python
class Bad:
    tags = []          # SHARED across all instances

class Good:
    def __init__(self):
        self.tags = []
```

## Methods

Three flavors:

```python
class Greeter:
    greeting = "Hi"

    def instance_method(self, name):
        return f"{self.greeting}, {name}"

    @classmethod
    def from_dict(cls, d):
        # `cls` is the class itself. Often used for "alternative constructors."
        return cls()      # could be Greeter or a subclass

    @staticmethod
    def shout(text):
        # No self, no cls. Just a function namespaced under the class.
        return text.upper() + "!"
```

- **Instance method** — needs an instance.
- **Class method** — needs the class, not an instance. Common for factory methods.
- **Static method** — needs neither. Sometimes a sign you don't need a class at all; sometimes it's the right namespace.

## Public, "private", and dunders

```python
class Cache:
    def __init__(self):
        self.size = 0           # public
        self._items = []         # convention: "internal, don't touch from outside"
        self.__hash = None       # name-mangled: stored as _Cache__hash
```

Python has no enforced privacy. Two conventions:

- `_name` — "internal use". You're trusted to not poke at it.
- `__name` (double underscore prefix, no suffix) — name mangling. Python rewrites `self.__hash` to `self._Cache__hash` to avoid accidental clashes in subclasses. Use sparingly.
- `__name__` (double underscore both sides) — **dunder** ("double underscore"). These are reserved for Python; don't invent your own.

Stick to `_underscore` for "private". The double-underscore mangling is rarely worth the friction.

## `isinstance` and `type`

```python
isinstance(c, Circle)       # True
isinstance(c, object)       # True — everything inherits from object
type(c) is Circle           # True
type(c) is object           # False — type is exact, ignores inheritance
```

Use `isinstance` for "is this a Circle or a subclass of Circle?". Use `type(x) is T` only when you really mean "exactly T".

## Read deeper

- **PCC** 3e, Ch. 9
- **LP** 6e, Ch. 27 (class coding basics)
- **FP** 2e, Ch. 11
