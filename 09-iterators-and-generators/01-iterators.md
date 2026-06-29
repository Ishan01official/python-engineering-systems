# 01 — Iterators

When you write `for x in container:`, Python doesn't iterate the container — it calls `iter(container)` to get an **iterator**, then repeatedly calls `next(iterator)` until `StopIteration` is raised. That's the entire protocol.

## The protocol

An iterator implements two methods:

- `__iter__(self)` — returns `self`. (An iterator is its own iterator.)
- `__next__(self)` — returns the next value, or raises `StopIteration`.

An **iterable** implements just `__iter__`, which returns a *fresh* iterator each time. Lists, dicts, sets, strings, files — all iterables.

```python
xs = [10, 20, 30]
it = iter(xs)             # get an iterator
print(next(it))           # 10
print(next(it))           # 20
print(next(it))           # 30
print(next(it))           # StopIteration
```

That's literally what `for` does:

```python
# These two are equivalent
for x in xs:
    print(x)

it = iter(xs)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)
```

## Iterators are single-use

```python
it = iter([1, 2, 3])
list(it)        # [1, 2, 3]
list(it)        # []   — exhausted
```

A list is iterable many times. The iterator you get from it is one-shot.

This matters in subtle ways: if a function returns an iterator (not a list), the caller can only loop through it *once*.

```python
def squares(n):
    return (i * i for i in range(n))    # generator expression — iterator

s = squares(5)
print(sum(s))    # 30
print(sum(s))    # 0  — already exhausted!
```

If you need to iterate twice, convert to a list, or return an iterable (e.g., a function that returns a fresh iterator on each call).

## Writing your own iterator

The cleanest way is with a generator (next note). But here's the explicit form, for understanding:

```python
class CountUp:
    def __init__(self, start: int, stop: int):
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


for n in CountUp(3, 7):
    print(n)         # 3, 4, 5, 6
```

Every place that takes an iterable (`for`, `list()`, `sum()`, `min()`, `max()`, comprehensions, `in`) works with this class for free, because it implements the protocol.

## Why this matters

Streaming. The iterator protocol lets you process data **one item at a time**, never holding the whole sequence in memory. A 100-GB log file? A `for line in open(path)` walks it on a desktop with 8 GB of RAM, no problem. Each line is read and processed, then released.

That's the foundation everything in the data-engineering track is built on.

## Read deeper

- **LP** 6e, Ch. 14, 20
- **FP** 2e, Ch. 17 — the canonical reference on iterators
