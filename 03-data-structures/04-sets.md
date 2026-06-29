# 04 — Sets

A `set` is an **unordered** collection of **unique, hashable** elements. Like a dict, but only keys — no values.

Use a set when you need:

- Fast membership tests (`x in s` is O(1) on average)
- Deduplication
- Set algebra (union, intersection, difference)

## Creating sets

```python
s = {1, 2, 3}
s = set()                  # empty (NOT {} — that's an empty dict!)
s = set([1, 2, 2, 3])      # {1, 2, 3}  — deduped automatically
s = {x ** 2 for x in range(5)}    # set comprehension
```

`{}` is an empty dict, not an empty set. The empty set is `set()`. Sources of confusion #1.

## Operations

```python
s = {1, 2, 3}

# Mutation
s.add(4)
s.update([5, 6, 7])
s.remove(2)             # KeyError if missing
s.discard(99)           # silent if missing
popped = s.pop()        # arbitrary element

# Test
3 in s                  # True
len(s)                  # 4

# Iteration (no defined order)
for x in s: ...
```

## Set algebra

This is where sets shine. All four operations are O(len(s1) + len(s2)) on average:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b      # union         {1, 2, 3, 4, 5, 6}
a & b      # intersection  {3, 4}
a - b      # difference    {1, 2}        (in a, not in b)
a ^ b      # symmetric diff {1, 2, 5, 6} (in either, not both)

a <= b     # subset
a < b      # proper subset
a >= b     # superset
a.isdisjoint(b)   # no common elements?
```

These are also available as methods (`a.union(b)`, `a.intersection(b)`) which accept any iterable, not just a set.

## Classic use cases

### Deduplicate while preserving... nothing

```python
unique = list(set(items))      # order is lost
```

### Deduplicate while preserving order

```python
# Python 3.7+: dicts are ordered, sets are not
seen = set()
unique = [x for x in items if not (x in seen or seen.add(x))]

# Cleaner trick using dict
unique = list(dict.fromkeys(items))   # dict keys preserve insertion order
```

### Fast lookup

```python
allowed = {"GET", "POST", "PUT", "DELETE"}
if request.method in allowed:        # O(1)
    ...
```

If you wrote this as a list (`["GET", "POST", ...]`), each `in` would be a linear scan. Use a set whenever you have a fixed lookup table.

### Set difference for "what's missing"

```python
required = {"user_id", "email", "name"}
provided = set(payload.keys())
missing = required - provided
if missing:
    raise ValueError(f"missing fields: {missing}")
```

## `frozenset`

An immutable set. Hashable, so you can use one as a dict key or put it inside another set.

```python
fs = frozenset([1, 2, 3])
{fs: "value"}      # works as a dict key
```

## Pitfalls

- **`{}` is a dict, not a set.** Use `set()` for an empty set.
- **Elements must be hashable.** No lists or dicts as set elements. Use tuples (with hashable contents).
- **Order is undefined.** Don't rely on iteration order.
- **Sets allocate eagerly.** A set of 10 million strings uses a lot of memory. Consider a bloom filter if memory is tight and false positives are acceptable.

## Read deeper

- **LP** 6e, Ch. 5 (sets) and Ch. 8 (mappings)
- **FP** 2e, Ch. 3 — sets and the hash table internals
