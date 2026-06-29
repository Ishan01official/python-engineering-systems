# 03 — `for` loops

In Python, `for` doesn't increment a counter. It walks an **iterable** — anything you can iterate over: lists, tuples, dicts, strings, files, ranges, generators, etc.

## Forget C-style indexing

```python
# Don't do this in Python:
for i in range(len(items)):
    print(items[i])

# Do this:
for item in items:
    print(item)
```

If you genuinely need the index *and* the value, use `enumerate`:

```python
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Start at 1 instead of 0:
for i, item in enumerate(items, start=1):
    print(f"{i}: {item}")
```

## Iterating two things in parallel: `zip`

```python
names = ["Alice", "Bob", "Carol"]
scores = [88, 73, 91]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

`zip` stops at the shortest input. Use `zip(..., strict=True)` (3.10+) to raise an error if lengths differ — a great safety net.

## Iterating a dict

```python
d = {"a": 1, "b": 2}

for key in d:               # keys only
    ...
for key, value in d.items():  # both
    ...
for value in d.values():
    ...
```

`d.items()` is what you want 90% of the time.

## `range` for "do something N times"

```python
for _ in range(5):
    print("hi")

for i in range(0, 10, 2):
    print(i)          # 0, 2, 4, 6, 8
```

`range` is lazy — it doesn't build a list. `range(1_000_000_000)` uses tiny memory.

## Comprehensions: when a `for` builds a collection

Instead of:
```python
doubled = []
for x in xs:
    doubled.append(x * 2)
```

Write:
```python
doubled = [x * 2 for x in xs]
```

You can filter:
```python
positives_squared = [x**2 for x in xs if x > 0]
```

And produce dicts and sets:
```python
{x: x**2 for x in xs}        # dict comprehension
{x % 5 for x in xs}          # set comprehension
```

**Use comprehensions for transformations and filters.** Don't use them for side effects (printing, writing to files) — that defeats their purpose.

If a comprehension has more than 2 `for`s or more than 1 `if`, it's probably too clever — use a regular loop instead.

## Pitfalls

- **Modifying the list you're iterating over.** Don't `for x in xs: xs.remove(x)`. Iterate over a copy or build a new list.
- **`for i in range(len(xs))` smell.** Almost always replaceable with `enumerate`, `zip`, or just `for x in xs`.
- **Forgetting that `zip` truncates.** Use `strict=True` or `itertools.zip_longest` deliberately.

## Read deeper

- **PCC** 3e, Ch. 4 (for, lists)
- **LP** 6e, Ch. 14 (iterations and comprehensions)
- **FP** 2e, Ch. 17 (iterators, generators) — for the underlying machinery
