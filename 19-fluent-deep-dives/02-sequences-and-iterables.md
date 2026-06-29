# 02 — Sequences and iterables beyond `list`

Python's container model is layered. Understanding the layers lets you accept the most general type your function actually needs.

## The hierarchy (from `collections.abc`)

```
Container ── __contains__
Sized     ── __len__
Iterable  ── __iter__
   ↓
Iterator  ── __next__
Reversible── __reversed__
Collection (Container + Sized + Iterable)
Sequence (Collection + indexable + reversible) ── __getitem__
   ↓
MutableSequence ── __setitem__, __delitem__, insert
Set / MutableSet
Mapping / MutableMapping
```

If you annotate `def f(x: list)`, you've over-specified. If `f` only iterates, accept `Iterable`. If it needs `len()` too, accept `Collection`. The result: callers can pass any matching type — a generator, a tuple, a set, your custom class — without conversion.

## Memoryviews and bytes-like

For binary data, the `bytes`/`bytearray`/`memoryview` family lets you slice without copying. `memoryview` is critical when you're processing big blobs (image data, network buffers): it gives you a view over the underlying bytes with zero allocation.

```python
data = bytearray(b"hello world")
view = memoryview(data)
view[0:5] = b"HELLO"
print(data)         # bytearray(b'HELLO world')
```

You won't reach for this often, but when you do (e.g., file-format parsing, embedded work), it's invaluable.

## `array.array` for homogeneous numeric data

If you want a fixed-type, contiguous numeric array and don't want NumPy:

```python
from array import array
ints = array("i", [1, 2, 3, 4])     # signed ints
```

Much more memory-efficient than a list of ints, but lacks NumPy's math. Useful in low-dependency embedded contexts.

## `deque` for fast queues and stacks

```python
from collections import deque
q = deque(maxlen=1000)         # bounded — auto-evicts old
q.appendleft(x); q.append(y)   # both O(1)
q.popleft(); q.pop()           # both O(1)
```

A list's `pop(0)` and `insert(0, x)` are O(n). `deque` is O(1) at both ends. Use it for sliding windows, BFS queues, rolling histories.

## Implementing your own sequence cleanly

The simplest path: subclass `collections.abc.Sequence` and implement `__getitem__` and `__len__`. You get `__contains__`, `__iter__`, `__reversed__`, `index`, `count` for free.

```python
from collections.abc import Sequence

class Page(Sequence):
    def __init__(self, items):
        self._items = list(items)

    def __getitem__(self, i):
        return self._items[i]

    def __len__(self):
        return len(self._items)

# Now this all works:
p = Page([1, 2, 3])
p[0]; 2 in p; list(reversed(p)); p.index(2); p.count(1)
```

## Read deeper

- **FP** 2e, Ch. 2 (sequences), Ch. 13 (interfaces, protocols, ABCs)
