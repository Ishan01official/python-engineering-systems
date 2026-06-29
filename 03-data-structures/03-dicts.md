# 03 — Dicts

A `dict` is a **hash map** — a collection of key→value pairs. This is the workhorse of Python. JSON is just a `dict` on the wire. Python's own object attributes are stored in dicts. If you use Python for more than a week, you'll use a dict.

## Creating dicts

```python
d = {}
d = dict()
d = {"name": "Ishan", "role": "data engineer"}
d = dict(name="Ishan", role="data engineer")
d = dict([("a", 1), ("b", 2)])
d = {k: v for k, v in [("a", 1), ("b", 2)]}    # dict comprehension
```

## Core operations

```python
d = {"a": 1, "b": 2}

# Read
d["a"]                  # 1 — KeyError if missing
d.get("a")              # 1
d.get("x")              # None — no error
d.get("x", 0)           # 0 — default if missing

# Write
d["c"] = 3
d.update({"d": 4, "e": 5})   # bulk update

# Delete
del d["a"]              # KeyError if missing
d.pop("b")              # returns the value and removes it
d.pop("missing", None)  # safe default form

# Test membership — by KEY, not value
"a" in d                # True

# Iteration
for k in d: ...              # over keys (default)
for k, v in d.items(): ...   # over both
for v in d.values(): ...     # over values

# Size
len(d)
```

## Why dicts are fast

Lookup, insertion, and deletion are all **O(1) average**. Hash maps are one of the great inventions of computer science. The cost is:

- Keys must be **hashable** (so immutable types or your own classes with a stable hash).
- Items are stored in insertion order (since Python 3.7) — but you can't index by position.

If you need both "lookup by name" and "lookup by position", you probably want a list of tuples or two parallel data structures, not a single dict.

## Default values, the Pythonic ways

### `dict.get` for read

```python
counts.get(word, 0)
```

### `dict.setdefault` for "get-or-create"

```python
groups = {}
for item in items:
    groups.setdefault(item.category, []).append(item)
```

Creates the empty list only if the key isn't there.

### `collections.defaultdict` for cleaner aggregation

```python
from collections import defaultdict

counts = defaultdict(int)
for word in words:
    counts[word] += 1     # missing keys become 0 automatically

groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

`defaultdict(int)` makes any missing key default to 0 on first access. `defaultdict(list)` defaults to `[]`. You can pass any zero-argument callable.

### `collections.Counter` for counting

```python
from collections import Counter

c = Counter("mississippi")
print(c)                    # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
print(c.most_common(2))     # [('i', 4), ('s', 4)]
```

A `Counter` is a dict subclass. Use it any time you'd write `counts[x] += 1` in a loop.

## Merging dicts

```python
a = {"x": 1, "y": 2}
b = {"y": 99, "z": 3}

merged = {**a, **b}        # {'x': 1, 'y': 99, 'z': 3}  — b wins for 'y'
merged = a | b             # same, Python 3.9+
a |= b                     # update a in place
```

## Iteration patterns

```python
# Build a new dict by transforming
{k: v * 2 for k, v in d.items()}

# Filter
{k: v for k, v in d.items() if v > 10}

# Invert (swap keys and values) — only works if values are hashable & unique
{v: k for k, v in d.items()}

# Sort by value, return a list of (key, value)
sorted(d.items(), key=lambda kv: kv[1], reverse=True)
```

## Pitfalls

- **`d[key]` raises `KeyError` on missing keys.** Use `.get()` when missing is normal, `d[key]` when missing is a bug.
- **Iterating and mutating.** Don't add/remove keys mid-loop. Iterate `list(d)` (a snapshot of keys) if you must.
- **Unhashable keys.** Lists can't be keys. Convert to a tuple if you need a composite key.
- **Default-arg trap, dict version.** Same warning as for lists:
  ```python
  def add(item, cache={}):   # DANGER — shared across calls
      ...
  ```

## Read deeper

- **PCC** 3e, Ch. 6
- **LP** 6e, Ch. 8
- **FP** 2e, Ch. 3 — *the* deep dive on dicts and sets (hash tables, performance)
