"""
NumPy fundamentals — vectorization, masks, broadcasting.

Run:
    python 15-numpy/examples/01_numpy_basics.py
"""
import time

import numpy as np


# ---- 1. Array creation, shape, dtype --------------------------------------

def array_basics() -> None:
    print("--- Array basics ---")
    a = np.arange(12).reshape(3, 4)
    print(a)
    print(f"shape: {a.shape}, dtype: {a.dtype}, nbytes: {a.nbytes}")
    print()


# ---- 2. Loop vs vectorized — proves the speedup ---------------------------

def vectorization_speedup() -> None:
    print("--- Vectorization speedup ---")
    n = 1_000_000
    a = np.arange(n, dtype=np.float64)

    t0 = time.perf_counter()
    out = np.empty_like(a)
    for i in range(n):
        out[i] = a[i] ** 2 + 1
    loop_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    out = a ** 2 + 1
    vec_time = time.perf_counter() - t0

    print(f"  python loop:   {loop_time*1000:7.1f} ms")
    print(f"  vectorized:    {vec_time*1000:7.1f} ms")
    print(f"  speedup:       {loop_time/vec_time:.1f}x")
    print()


# ---- 3. Boolean masks ----------------------------------------------------

def boolean_masks() -> None:
    print("--- Boolean masks ---")
    ages = np.array([22, 17, 31, 45, 12, 68])
    adults = ages[ages >= 18]
    working = ages[(ages >= 18) & (ages < 65)]
    print(f"  adults:        {adults}")
    print(f"  working-age:   {working}")
    print()


# ---- 4. Reductions over axes ---------------------------------------------

def axes_demo() -> None:
    print("--- axis=0 (down cols) vs axis=1 (across rows) ---")
    sales = np.array([
        [100, 200, 150],   # product 0 by quarter
        [ 80, 110,  90],   # product 1 by quarter
        [200, 250, 220],   # product 2 by quarter
    ])
    print(f"  per-product total (axis=1): {sales.sum(axis=1)}")
    print(f"  per-quarter total (axis=0): {sales.sum(axis=0)}")
    print(f"  grand total:                {sales.sum()}")
    print()


# ---- 5. Broadcasting -----------------------------------------------------

def broadcasting_demo() -> None:
    print("--- Broadcasting: center each column ---")
    rng = np.random.default_rng(0)
    m = rng.random((4, 3))
    centered = m - m.mean(axis=0)
    print("  original means per col:", m.mean(axis=0).round(3))
    print("  centered means per col:", centered.mean(axis=0).round(3))
    print()

    print("--- Outer product via broadcasting ---")
    x = np.arange(1, 4)
    y = np.arange(1, 5)
    table = x[:, None] * y[None, :]
    print(table)
    print()


# ---- 6. np.where ---------------------------------------------------------

def where_demo() -> None:
    print("--- np.where for conditional pick ---")
    prices = np.array([10, 20, 5, 100, 50, 200])
    discounted = np.where(prices > 50, prices * 0.9, prices)
    print(f"  prices:     {prices}")
    print(f"  discounted: {discounted}")
    print()


if __name__ == "__main__":
    array_basics()
    vectorization_speedup()
    boolean_masks()
    axes_demo()
    broadcasting_demo()
    where_demo()
