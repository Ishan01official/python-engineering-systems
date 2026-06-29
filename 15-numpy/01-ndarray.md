# 01 — The `ndarray`

NumPy's core object is the `ndarray` — an N-dimensional array of **homogeneous** numeric values stored in a contiguous block of memory.

## What makes it different from a Python list

| Python list | NumPy array |
|---|---|
| Heterogeneous (mixed types OK) | Homogeneous (one dtype) |
| Each element is a separate Python object | Stored as a flat C array |
| Slow elementwise math (loop in Python) | Fast elementwise math (loop in C, SIMD) |
| `[1,2,3]+[4,5,6]` is concat | `arr1+arr2` is elementwise add |

A 1-million-int list in Python uses ~28 MB. A 1-million-int NumPy array uses ~8 MB and arithmetic on it is 50-100x faster.

## Creating arrays

```python
import numpy as np

# From data
a = np.array([1, 2, 3])
b = np.array([[1, 2], [3, 4]])

# Constructors
zeros = np.zeros(10)               # array of 10 zeros (float64)
ones  = np.ones((3, 4))            # 3x4 of ones
empty = np.empty(5)                # uninitialized — fast, contents are garbage
ar    = np.arange(0, 10, 0.5)      # like range, but supports floats
lin   = np.linspace(0, 1, 5)       # 5 values evenly spaced from 0..1
rng   = np.random.default_rng(42)
rand  = rng.random((3, 3))         # uniform [0,1)
norm  = rng.standard_normal((3, 3))
```

## Shape, dtype, dimensions

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

a.shape      # (2, 3)
a.ndim       # 2
a.size       # 6
a.dtype      # dtype('int64')   on most 64-bit systems
a.nbytes     # 48   (6 int64 elements * 8 bytes)
```

The **dtype** is fixed at creation: `int8`, `int32`, `int64`, `float32`, `float64`, `bool`, `complex128`, etc. Force one:

```python
a = np.array([1, 2, 3], dtype=np.float32)
a.astype(np.int32)         # returns a new array with that dtype
```

`float32` uses half the memory of `float64`; for big arrays that's worth knowing.

## Indexing and slicing

```python
a = np.array([10, 20, 30, 40, 50])
a[0]            # 10
a[-1]           # 50
a[1:4]          # array([20, 30, 40])
a[::2]          # array([10, 30, 50])
a[::-1]         # reversed
```

2D:

```python
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
m[0]            # array([1, 2, 3])   — first row
m[0, 1]         # 2                  — row 0, col 1
m[:, 0]         # array([1, 4, 7])   — first column
m[1:, 1:]       # array([[5, 6], [8, 9]])
```

## Slices are *views*, not copies

This is a critical detail:

```python
a = np.array([1, 2, 3, 4, 5])
b = a[1:4]
b[0] = 999
print(a)        # array([1, 999, 3, 4, 5])  — the original changed!
```

Mutating `b` changes `a` because they share the same underlying buffer. Use `.copy()` if you need independence.

## Reshape and view

```python
a = np.arange(12)
a.reshape((3, 4))             # 3 rows, 4 cols — no copy when possible
a.reshape((3, -1))            # -1 means "compute this dimension"
a.flatten()                   # 1D copy
a.ravel()                     # 1D view if possible
```

## Type promotion (broadcasting of dtypes)

Mixing dtypes promotes to the wider one:

```python
np.array([1, 2]) + 0.5     # → array([1.5, 2.5])  — int + float → float
```

You can lose precision implicitly. Be deliberate about dtypes for big arrays.

## Read deeper

- **PfDA** 3e, Ch. 4 — NumPy basics, full chapter.
- NumPy docs: array creation, indexing, dtypes.
