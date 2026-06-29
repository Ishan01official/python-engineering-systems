# 01 — The Python data model

Python's data model is the **set of protocols** that built-in features check for when you do things like `for x in obj`, `len(obj)`, `obj[key]`, `obj + other`, `with obj`. Every protocol is "does this object implement these dunder methods?".

This is the single most important insight in *Fluent Python*. Master it and you can write classes that feel native — they work everywhere Python expects an iterable, a number, a context manager, a callable.

## What it means in practice

```python
class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [(r, s) for s in self.suits for r in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]
```

Just two dunders. Now:

- `len(deck)` works → because `__len__`.
- `deck[0]` works → because `__getitem__`.
- `deck[:3]` works → because `__getitem__` accepts slices.
- `for card in deck:` works → Python falls back to `__getitem__` from 0 until `IndexError`.
- `card in deck` works → Python iterates and checks.
- `random.choice(deck)` works → it only needs indexing and len.
- `sorted(deck)` works → it only needs iteration and `<`.

No inheritance from `list`, no explicit Iterable interface — you just implemented the protocol and got everything for free.

## The full menu (a partial list)

| Protocol | Methods |
|---|---|
| Object representation | `__repr__`, `__str__`, `__format__`, `__bytes__` |
| Numeric | `__int__`, `__float__`, `__abs__`, `__bool__` |
| Conversion | `__index__`, `__hash__` |
| Comparison | `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__`, `__ne__` |
| Arithmetic | `__add__`, `__sub__`, `__mul__`, `__matmul__`, `__truediv__`, `__floordiv__`, `__mod__`, `__pow__`, `__neg__`, ... |
| Reverse + in-place | `__radd__`, `__iadd__`, ... |
| Container | `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__` |
| Iteration | `__iter__`, `__next__`, `__reversed__` |
| Callable | `__call__` |
| Context manager | `__enter__`, `__exit__` |
| Async | `__aiter__`, `__anext__`, `__aenter__`, `__aexit__` |
| Attribute access | `__getattr__`, `__getattribute__`, `__setattr__`, `__delattr__`, `__dir__` |
| Descriptors | `__get__`, `__set__`, `__delete__` |

## Design rule of thumb

When defining a class, ask: "what built-in operations do I want users of this to write?"

- "I want `len(my_thing)` to work" → implement `__len__`.
- "I want `my_thing[0]`" → `__getitem__`.
- "I want `for x in my_thing`" → `__iter__` (or `__getitem__`).
- "I want `my_thing + other`" → `__add__`.
- "I want `bool(my_thing)`" → `__bool__` (or `__len__`).
- "I want sortability" → `__lt__` is enough.

Don't implement what you don't need. But when you do, lean on the protocol — your class will be at home in the rest of the language.

## Read deeper

- **FP** 2e, Ch. 1 — "The Python Data Model" — if you read one chapter of one Python book, read this one. Then read it again next year.
