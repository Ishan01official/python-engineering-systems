# 04 — Metaclasses (and when to walk away from them)

A class is itself an object. Its type is `type`. A **metaclass** is the type of a class — the class whose instance is your class.

```python
class Foo: pass

type(Foo)              # <class 'type'>
type(Foo())            # <class 'Foo'>
```

By defining a metaclass, you customize how classes themselves are built.

## A toy example

```python
class UpperAttrs(type):
    def __new__(mcs, name, bases, attrs):
        upper_attrs = {
            (key.upper() if not key.startswith("__") else key): value
            for key, value in attrs.items()
        }
        return super().__new__(mcs, name, bases, upper_attrs)


class Thing(metaclass=UpperAttrs):
    foo = "bar"

print(Thing.FOO)       # 'bar'
# print(Thing.foo)     # AttributeError — was renamed at class creation time
```

The metaclass intercepted the class's creation and renamed its attributes.

## What metaclasses are used for in real code

- **Django models, SQLAlchemy declarative base** — used to register subclasses, enforce schema, generate methods at class-definition time.
- **ABCs** — `ABCMeta` is a metaclass.
- **Plugin systems** — auto-registering subclasses in a registry as soon as they're defined.

## What metaclasses are NOT used for in real code

- Application code.
- "Adding logging to all methods" — use a decorator, not a metaclass.
- "Validating fields" — use `__init_subclass__`, descriptors, or a dataclass-like decorator.

99% of the time you think you need a metaclass, you actually need:

- A **decorator** on the class.
- `__init_subclass__` (hooks into subclass creation without a metaclass).
- A **descriptor** (per-attribute customization).
- A **mixin** (shared methods).

## `__init_subclass__` — the modern alternative

Most "I need a metaclass" use cases are now solved with `__init_subclass__`:

```python
class PluginBase:
    registry = {}

    def __init_subclass__(cls, *, name, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.registry[name] = cls


class Foo(PluginBase, name="foo"):
    pass

class Bar(PluginBase, name="bar"):
    pass

print(PluginBase.registry)
# {'foo': <class 'Foo'>, 'bar': <class 'Bar'>}
```

No metaclass needed. The base class itself intercepts the creation of every subclass.

## The takeaway

Metaclasses exist, they power some impressive libraries, and they're an interesting corner of Python. They are almost never the right tool for your code. Knowing they exist is enough; knowing `__init_subclass__` exists is more useful.

If you find yourself reaching for one, sleep on it. There's usually a simpler way.

## Read deeper

- **FP** 2e, Ch. 24 — class metaprogramming
- Python docs: data model, `__init_subclass__`, descriptors
