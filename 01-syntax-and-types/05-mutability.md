# 05 — Mutability vs immutability

The single distinction that, once internalized, makes a *huge* number of Python behaviors stop being surprising.

## The list

| Mutable | Immutable |
|---|---|
| `list` | `int`, `float`, `complex` |
| `dict` | `str` |
| `set` | `tuple` |
| `bytearray` | `frozenset` |
| user classes (by default) | `bytes` |
|  | `None`, `True`, `False` |

## What "mutable" means

You can change the **contents** of a mutable object without creating a new object. The object's identity (its `id()`) stays the same.

```python
xs = [1, 2, 3]
print(id(xs))     # some number, say 12345
xs.append(4)
print(id(xs))     # same number 12345 — same object
print(xs)         # [1, 2, 3, 4]
```

## What "immutable" means

There's no way to change the object. Any operation that "modifies" the value really creates a **new** object.

```python
s = "hello"
print(id(s))      # say 67890
s = s.upper()
print(id(s))      # different — a new string object
print(s)          # "HELLO"
```

Note: the *name* `s` is rebound. The original string `"hello"` still exists in memory until nothing references it.

## Consequences in real code

### 1. Function arguments

```python
def add_one(lst):
    lst.append(1)        # mutates the caller's list

def add_one_safe(lst):
    return lst + [1]     # returns a NEW list, original untouched
```

If your function takes a mutable argument and modifies it, the caller sees the change. Sometimes that's what you want. Sometimes it's a horrible bug. Be explicit in docstrings.

### 2. Default arguments — the classic trap

```python
def add_item(item, items=[]):    # DANGER
    items.append(item)
    return items

add_item("a")    # ["a"]
add_item("b")    # ["a", "b"]  — wait, what?
```

The default `[]` is evaluated **once**, when the function is defined. Every call reuses the same list. The fix:

```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

This is one of the most-cited Python footguns. EP has an item on it.

### 3. Dict keys must be immutable

Dict keys (and set elements) must be **hashable**. Mutable built-in types like `list` and `dict` are not hashable; immutable ones like `str`, `int`, `tuple` (with hashable contents) are.

```python
d = {(1, 2): "ok"}    # tuple key — fine
d = {[1, 2]: "bad"}   # TypeError: unhashable type: 'list'
```

### 4. Tuple "immutability" is shallow

```python
t = ([1, 2], [3, 4])
t[0] = [9, 9]       # TypeError — can't rebind the tuple's slot
t[0].append(99)     # OK — the inner list IS mutable
print(t)            # ([1, 2, 99], [3, 4])
```

A tuple guarantees its slots don't change. It does NOT guarantee what those slots *point at* is itself immutable.

## When to choose which

- **Default to immutable.** Tuples instead of lists when the size is fixed. `frozenset` instead of `set` when membership is fixed.
- **Use mutable** when you actually need to build up or modify a collection over time.
- **In function signatures**, prefer arguments that you don't mutate. Return new values instead.

## Try it

Run [`examples/03_mutability.py`](./examples/03_mutability.py).

## Read deeper

- **FP** 2e, Ch. 6 — object references, mutability, recycling. The clearest treatment.
- **EP** 3e — item on never using mutable default arguments.
