# 02 — Vectorization

The single most important NumPy idea. **Don't write Python loops over array elements. Express the operation on the array as a whole.**

## A loop vs a vectorized op

```python
import numpy as np
a = np.arange(1_000_000, dtype=np.float64)

# Slow: ~150 ms
result = np.empty_like(a)
for i in range(len(a)):
    result[i] = a[i] ** 2 + 1

# Fast: ~3 ms (50× faster)
result = a ** 2 + 1
```

The expression `a ** 2 + 1` reads exactly like math, runs as a tight C loop, and uses SIMD where available. The Python loop pays interpreter overhead on every iteration.

## Universal functions (ufuncs)

Most NumPy functions are *ufuncs* — they apply elementwise:

```python
np.sqrt(a)
np.log(a + 1)
np.sin(a)
np.exp(a)
np.abs(a)
np.maximum(a, b)        # elementwise max of two arrays
np.where(a > 0, a, 0)   # like a ternary: where condition, take a, else 0
```

Operators (`+`, `-`, `*`, `/`, `**`, `==`, `<`, etc.) are also ufuncs in disguise.

## Reductions

```python
a.sum()
a.mean()
a.std()
a.min(); a.max()
a.argmax()           # index of the max
a.cumsum()           # running total

# Along an axis
m = np.array([[1, 2, 3], [4, 5, 6]])
m.sum(axis=0)        # array([5, 7, 9])    — sum each column
m.sum(axis=1)        # array([6, 15])      — sum each row
m.mean(axis=0)       # column means
```

`axis=0` "collapses rows" (operates down columns). `axis=1` "collapses columns" (operates across rows). The mnemonic that works for many people: the axis you specify is the one that disappears in the output shape.

## Boolean masks — filtering without `if`

```python
ages = np.array([22, 17, 31, 45, 12, 68])
adults = ages >= 18          # array([True, False, True, True, False, True])
ages[adults]                 # array([22, 31, 45, 68])

# Combine with bitwise ops (& | ~), parens are required
working_age = ages[(ages >= 18) & (ages < 65)]
```

Boolean indexing returns a *copy*, not a view.

## `np.where` — conditional pick

```python
prices = np.array([10, 20, 5, 100, 50])
discounted = np.where(prices > 50, prices * 0.9, prices)
# array([10. , 20. ,  5. , 90. , 50. ])
```

Like a vectorized `x if cond else y`.

## Fancy indexing — by integer arrays

```python
a = np.array([10, 20, 30, 40, 50])
a[[0, 2, 4]]            # array([10, 30, 50])
a[[True, False, True, False, True]]   # same idea via boolean
```

Useful when you want specific positions in a non-slice pattern.

## When you have to use a Python loop

Sometimes you really can't vectorize (e.g., the iterations depend on each other). In that case:

1. Look for a NumPy/SciPy function that already does what you want.
2. If not, consider `numba.jit` or Cython for raw speed.
3. Or accept the cost — millions of items in a Python loop is slow but not always wrong.

## Read deeper

- **PfDA** 3e, Ch. 4 — vectorization examples and idioms.
