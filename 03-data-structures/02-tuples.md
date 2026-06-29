# 02 — Tuples

A `tuple` is an **immutable**, ordered sequence. Once created, you can't add, remove, or reassign its slots.

Tuples are not "immutable lists". They have a different *purpose*:

- **Lists** = a homogeneous collection that grows and shrinks: "all the user IDs".
- **Tuples** = a fixed-size record: "(latitude, longitude)", "(year, month, day)".

If you've used C structs or Go structs, tuples fill the same role for quick-and-dirty groupings.

## Creating tuples

```python
t = (1, 2, 3)
t = 1, 2, 3          # parens optional in most contexts
t = ()                # empty
t = (42,)             # one-element tuple — note the trailing comma
t = tuple([1, 2, 3])  # from any iterable
```

The trailing-comma rule for one-element tuples bites everyone once. `(42)` is just the integer 42 with parens around it.

## Operations

```python
t = (10, 20, 30)
t[0]            # 10
t[1:]           # (20, 30)
len(t)          # 3
20 in t         # True

# Tuples support + and * like sequences
t + (40,)       # (10, 20, 30, 40)   — returns a new tuple
t * 2           # (10, 20, 30, 10, 20, 30)

# Methods (only two)
t.count(20)     # 1
t.index(30)     # 2

# No append, no pop, no sort — they're immutable.
```

## Tuple unpacking — Python's secret weapon

```python
point = (3, 4)
x, y = point          # x=3, y=4

a, b = b, a           # swap, no temp variable

first, *rest = [1, 2, 3, 4]
# first=1, rest=[2,3,4]

first, *middle, last = [1, 2, 3, 4, 5]
# first=1, middle=[2,3,4], last=5
```

This works for any iterable, not just tuples. You'll see it everywhere.

## Use cases

### Multiple return values

```python
def divmod_explicit(a, b):
    return a // b, a % b           # returns a tuple

quotient, remainder = divmod_explicit(17, 5)
```

### Dict iteration

```python
for key, value in d.items():
    ...
```

`.items()` yields tuples, and the loop unpacks them.

### Records that don't deserve a class

```python
people = [("Alice", 30), ("Bob", 25)]
for name, age in people:
    ...
```

If you find yourself doing `person[0]` and `person[1]` and forgetting which is which — **promote it to a NamedTuple or a dataclass**:

```python
from typing import NamedTuple
class Person(NamedTuple):
    name: str
    age: int

people = [Person("Alice", 30), Person("Bob", 25)]
for p in people:
    print(p.name, p.age)        # readable
```

`NamedTuple` is a tuple under the hood, so you keep immutability + indexing, and gain attribute access. We'll cover dataclasses in Module 08.

## When is "immutable" actually shallow?

A tuple guarantees its **slots** don't change. If a slot points at a mutable object, the object can still be modified.

```python
t = ([1, 2], [3, 4])
t[0].append(99)        # OK — mutating the inner list
print(t)               # ([1, 2, 99], [3, 4])
```

For full immutability all the way down, use immutable types in your tuple (tuples of tuples, tuples of ints, etc.).

## Hashability

A tuple is hashable **only if all its contents are hashable**. This is why tuples can be dict keys but `(1, [2])` cannot:

```python
{(1, 2): "ok"}             # fine
{(1, [2]): "bad"}          # TypeError
```

## Read deeper

- **PCC** 3e, Ch. 4 (tuples)
- **LP** 6e, Ch. 9 (lists and tuples)
