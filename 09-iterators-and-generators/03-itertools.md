# 03 — `itertools` — the iteration toolkit

Stdlib module with battle-tested, memory-efficient building blocks. If you find yourself writing nested loops to do something "iteratory", check here first.

## Most useful ones

### `chain` — concatenate iterables

```python
from itertools import chain
list(chain([1, 2], [3, 4], [5]))          # [1, 2, 3, 4, 5]
list(chain.from_iterable([[1, 2], [3, 4]]))  # same — for an iterable of iterables
```

### `islice` — slice an iterator

You can't do `gen[:10]` on a generator (no `__getitem__`). Use `islice`:

```python
from itertools import islice
first_ten = list(islice(gen, 10))
middle    = list(islice(gen, 100, 200))      # start, stop
```

### `groupby` — consecutive-element grouping

```python
from itertools import groupby

data = [("Mon", 1), ("Mon", 2), ("Tue", 3), ("Wed", 4), ("Wed", 5)]
for day, group in groupby(data, key=lambda x: x[0]):
    print(day, list(group))
# Mon [('Mon', 1), ('Mon', 2)]
# Tue [('Tue', 3)]
# Wed [('Wed', 4), ('Wed', 5)]
```

**Critical:** `groupby` only groups **adjacent** items. If you want SQL's `GROUP BY` behavior (group all items with the same key, regardless of position), sort first:

```python
data.sort(key=lambda x: x[0])
for day, group in groupby(data, key=lambda x: x[0]):
    ...
```

Or use `collections.defaultdict(list)`.

### `accumulate` — running total

```python
from itertools import accumulate
list(accumulate([1, 2, 3, 4]))             # [1, 3, 6, 10]
list(accumulate([1, 2, 3, 4], max))        # [1, 2, 3, 4]   — running max
```

### `combinations`, `permutations`, `product`

```python
from itertools import combinations, permutations, product

list(combinations("ABC", 2))               # AB, AC, BC
list(permutations("ABC", 2))               # AB, AC, BA, BC, CA, CB
list(product([1, 2], ['x', 'y']))          # (1,'x'),(1,'y'),(2,'x'),(2,'y')
```

`product` is great for "all combinations of these N axes" — cleaner than nested loops.

### `count`, `cycle`, `repeat`

```python
from itertools import count, cycle, repeat

# Infinite — pair with islice or break
next_id = count(start=1000)
print(next(next_id), next(next_id))        # 1000, 1001

for i, color in zip(range(5), cycle(["red", "green", "blue"])):
    print(i, color)
# 0 red, 1 green, 2 blue, 3 red, 4 green

list(repeat("x", 3))                       # ["x", "x", "x"]
```

### `takewhile`, `dropwhile`

```python
from itertools import takewhile, dropwhile

list(takewhile(lambda x: x < 5, [1, 2, 6, 1]))   # [1, 2]
list(dropwhile(lambda x: x < 5, [1, 2, 6, 1]))   # [6, 1]
```

### `pairwise` (3.10+) — sliding window of 2

```python
from itertools import pairwise
list(pairwise([1, 2, 3, 4]))               # [(1,2), (2,3), (3,4)]
```

Saves you the off-by-one mess of writing this by hand.

### `batched` (3.12+) — fixed-size chunks

```python
from itertools import batched
list(batched("ABCDEFG", 3))                # [('A','B','C'), ('D','E','F'), ('G',)]
```

Before 3.12 you'd write your own:

```python
def batched(iterable, n):
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch
```

## When NOT to use itertools

If a comprehension is just as readable, prefer the comprehension. `itertools` shines for:

- Infinite or huge streams (where you can't materialize a list)
- Combinatorial generation (`combinations`, `permutations`, `product`)
- Sliding windows and chunking (`pairwise`, `batched`)
- Composing pipelines without nesting loops

## Read deeper

- Python docs: https://docs.python.org/3/library/itertools.html — has a "recipes" section with idioms you can copy.
- **EP** 3e — items on `itertools` and stdlib utilities.
