# 05 — When to use what

A quick decision guide. Read this once, refer to it when you're choosing a container.

## Decision flow

```
Do I have key→value pairs?
├─ Yes → dict
│        └─ Counting frequencies? → Counter
│        └─ Aggregating into lists? → defaultdict(list)
│
└─ No → it's a collection of single items
    │
    ├─ Order matters?
    │   ├─ Yes
    │   │   ├─ Will it change size? → list
    │   │   ├─ Fixed-size record? → tuple (or NamedTuple/dataclass)
    │   │   └─ Frequent inserts/pops at both ends? → collections.deque
    │   │
    │   └─ No
    │       ├─ Need uniqueness or set algebra? → set
    │       └─ Need uniqueness AND immutability? → frozenset
```

(See [`diagrams/data-structure-decision.mmd`](./diagrams/data-structure-decision.mmd) for the rendered version.)

## Quick reference table

| Need | Use | Why |
|---|---|---|
| Sequence of items, growing | `list` | O(1) append, slice-friendly |
| Fixed-size group of related values | `tuple` | Immutable record |
| Lookup by name/key | `dict` | O(1) average |
| Unique items only | `set` | O(1) membership, dedup |
| Counting | `Counter` | counts.most_common(), arithmetic |
| Grouping into lists | `defaultdict(list)` | clean append-or-create |
| FIFO/LIFO queue | `collections.deque` | O(1) both ends |
| Priority queue | `heapq` (on a list) | O(log n) push/pop |
| Stack | `list` (.append/.pop) | O(1) at the end |

## A common refactor

When this:

```python
totals = {}
for tx in transactions:
    if tx.user_id not in totals:
        totals[tx.user_id] = 0
    totals[tx.user_id] += tx.amount
```

Becomes this:

```python
from collections import defaultdict
totals = defaultdict(float)
for tx in transactions:
    totals[tx.user_id] += tx.amount
```

Or this:

```python
from collections import Counter
counts = Counter(item.category for item in items)
top_5 = counts.most_common(5)
```

The standard library has solved most of these patterns. **Reach for `collections` before you write the long version.**

## Working with very large data

For data-engineering scale work (millions+ of rows), the built-in containers stop being the right answer:

- For numeric data → **NumPy arrays** (Module 15)
- For tabular data → **pandas DataFrames** (Module 16)
- For streams → **generators** (Module 09) — process one item at a time, never hold the whole thing

Built-ins are perfect up to maybe a million items. Past that, the dedicated tools are 10–1000× faster and use a fraction of the memory.

## Read deeper

- **EP** 3e — items on choosing the right container and using `collections`
- **FP** 2e, Ch. 2–3 — sequences, dicts, sets in depth
