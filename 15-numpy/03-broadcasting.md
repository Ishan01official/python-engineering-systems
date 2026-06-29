# 03 — Broadcasting

The rule that lets you do arithmetic between arrays of different shapes — without explicitly looping or replicating data.

## The simplest case

```python
a = np.array([1, 2, 3, 4])
a * 10            # array([10, 20, 30, 40])
a + 1             # array([2, 3, 4, 5])
```

NumPy treats the scalar `10` as if it were repeated to match `a`'s shape. No actual replication happens — that's what makes it cheap.

## Two compatible arrays

```python
m = np.array([[1, 2, 3],
              [4, 5, 6]])         # shape (2, 3)
col_means = np.array([2.5, 3.5, 4.5])  # shape (3,)

m - col_means
# array([[-1.5, -1.5, -1.5],
#        [ 1.5,  1.5,  1.5]])
```

The 1D `col_means` of shape `(3,)` is broadcast across the rows of `m`. Every row gets the same subtraction.

## The rules

When operating on arrays of different shapes, NumPy compares shapes **right to left**:

1. If the dimensions don't match, **prepend** the shorter shape with 1s.
2. Dimensions are *compatible* if they're equal, or one of them is 1.
3. The output shape is the elementwise max.

Examples:

```
(3,)      vs (3,)        → (3,)         match
(2, 3)    vs (3,)        → (2, 3)       prepend → (1, 3); broadcast row
(2, 3)    vs (2, 1)      → (2, 3)       broadcast col
(8, 1, 6) vs (   7, 1)   → (8, 7, 6)    broadcast both
(2, 3)    vs (2,)        → ERROR        (2,) → (1, 2) ≠ (2, 3)
```

If you ever get `ValueError: operands could not be broadcast together`, read the shapes printed in the error and walk through this rule.

## Adding axes explicitly

Often the fix for a broadcasting failure is reshaping. `None` (or `np.newaxis`) inserts a length-1 dimension:

```python
a = np.array([1, 2, 3])         # shape (3,)
a[:, None]                       # shape (3, 1)  — a column
a[None, :]                       # shape (1, 3)  — a row
```

Outer product via broadcasting:

```python
x = np.arange(1, 4)
y = np.arange(1, 5)
x[:, None] * y[None, :]
# array([[ 1,  2,  3,  4],
#        [ 2,  4,  6,  8],
#        [ 3,  6,  9, 12]])
```

That's a 3×4 multiplication table, computed in one expression with zero loops.

## Center every column of a matrix

```python
m = np.random.default_rng(0).random((5, 3))
centered = m - m.mean(axis=0)         # subtract per-column mean
```

`m.mean(axis=0)` has shape `(3,)`. `m` has shape `(5, 3)`. Broadcasting handles the alignment.

## Pitfalls

- **Silent broadcasting where you didn't want it.** If you accidentally get an `(N, 1)` instead of `(N,)`, an operation can blow up in size. Print shapes when in doubt: `print(a.shape, b.shape)`.
- **Type promotion** — broadcasting an `int8` against a `float64` produces `float64`. Watch the dtype if memory matters.
- **Memory illusion.** Broadcasting *doesn't* materialize the replicated array. But if you save the broadcast result (`np.broadcast_to(a, (1000, 1000))`), it's a view; modifying it does weird things. Use `np.broadcast_to(...).copy()` if you need a real array.

## Read deeper

- **PfDA** 3e, Ch. 4 — broadcasting section
- NumPy docs: https://numpy.org/doc/stable/user/basics.broadcasting.html
