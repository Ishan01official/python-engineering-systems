# 01 — Lists

A `list` is an ordered, mutable sequence. It's the Python equivalent of a dynamic array. Use it when:

- You need to keep items in order.
- The collection will grow or shrink.
- You access elements by position, not by name.

## Creating lists

```python
xs = [1, 2, 3]
xs = list()              # empty
xs = list("abc")         # ['a', 'b', 'c'] — from any iterable
xs = [x * 2 for x in range(5)]   # comprehension
```

## Core operations

```python
xs = [10, 20, 30, 40]

# Indexing and slicing
xs[0]            # 10
xs[-1]           # 40
xs[1:3]          # [20, 30]
xs[::-1]         # [40, 30, 20, 10]

# Mutation
xs.append(50)              # [10, 20, 30, 40, 50]
xs.insert(0, 5)            # [5, 10, 20, 30, 40, 50]
xs.extend([60, 70])        # [..., 50, 60, 70]
xs.remove(20)              # removes first occurrence of 20 (ValueError if missing)
popped = xs.pop()          # remove and return last
popped = xs.pop(0)         # remove and return first
xs.clear()                 # empty it

# Search
30 in xs                   # True/False
xs.index(30)               # position of first 30 (ValueError if missing)
xs.count(30)               # how many 30s

# Sort
xs.sort()                  # in place
xs.sort(reverse=True)
xs.sort(key=lambda s: s.lower())  # custom key
ys = sorted(xs)            # returns a NEW sorted list
```

`sort()` mutates; `sorted()` returns new. Same distinction with `reverse()` vs `reversed()`.

## Performance, in one table

| Operation | Time | Why |
|---|---|---|
| `xs[i]` | O(1) | array indexing |
| `xs.append(x)` | O(1) amortized | resize occasionally |
| `xs.pop()` | O(1) | from the end |
| `xs.pop(0)` | O(n) | must shift everything left |
| `xs.insert(0, x)` | O(n) | same reason |
| `x in xs` | O(n) | linear scan |
| `xs.sort()` | O(n log n) | Timsort |

**If you're doing lots of front-insertions or front-pops, use `collections.deque` instead.** It's O(1) at both ends.

## Comprehensions revisited

```python
# Basic
squares = [x ** 2 for x in range(10)]

# With filter
evens = [x for x in range(20) if x % 2 == 0]

# Two-level
pairs = [(i, j) for i in range(3) for j in range(3) if i != j]
```

Rule of thumb: if a comprehension takes more than one line of mental parsing, write it as a regular loop.

## Pitfalls

- **`xs * 3` shallow-copies references.** `[[]] * 3` gives you three names for the *same* list:
  ```python
  bad = [[]] * 3
  bad[0].append(1)
  print(bad)    # [[1], [1], [1]]   — surprise

  good = [[] for _ in range(3)]
  good[0].append(1)
  print(good)   # [[1], [], []]    — expected
  ```
- **Mutating while iterating.** Don't do `for x in xs: xs.remove(x)`. Build a new list with a comprehension, or iterate `xs[:]` (a copy).
- **Slice assignment can mutate.** `xs[:] = [10, 20]` replaces the contents of the existing list in-place. `xs = [10, 20]` rebinds the name to a new list. The difference matters when other names point at the same list.

## Read deeper

- **PCC** 3e, Ch. 3–4
- **LP** 6e, Ch. 8
- **FP** 2e, Ch. 2 — sequences in great depth
