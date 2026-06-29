"""
Before/after — turn beginner Python into idiomatic Python.

Run:
    python 14-effective-python-patterns/examples/01_before_after.py
"""
from dataclasses import dataclass


# ---- B1: range(len()) → enumerate ---------------------------------------

def b1_before(items):
    result = []
    for i in range(len(items)):
        result.append(f"{i}: {items[i]}")
    return result


def b1_after(items):
    return [f"{i}: {x}" for i, x in enumerate(items)]


# ---- B2: index access → tuple unpacking ---------------------------------

def b2_before(pairs):
    out = []
    for p in pairs:
        out.append(p[0] + p[1])
    return out


def b2_after(pairs):
    return [a + b for a, b in pairs]


# ---- B3: keyword-only arguments ------------------------------------------

def b3_before(path, write=False, append=False, buffer_size=1024):
    """Callers can do b3_before('x', True, False, 4096) — what do True/False mean?"""
    return path, write, append, buffer_size


def b3_after(path, *, write=False, append=False, buffer_size=1024):
    """Forces b3_after('x', write=True, buffer_size=4096) at call site."""
    return path, write, append, buffer_size


# ---- B4: many returns → NamedTuple/dataclass ----------------------------

def b4_before(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers), len(numbers)


@dataclass(frozen=True)
class Stats:
    min: float
    max: float
    mean: float
    n: int


def b4_after(numbers) -> Stats:
    return Stats(
        min=min(numbers),
        max=max(numbers),
        mean=sum(numbers) / len(numbers),
        n=len(numbers),
    )


# ---- B5: mutable default → None sentinel --------------------------------

def b5_before(item, bucket=[]):     # SHARED BUG across calls
    bucket.append(item)
    return bucket


def b5_after(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


# ---- B6: hidden iteration cost → generator -------------------------------

def b6_before(n):
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i * i)
    return result                  # builds whole list in memory


def b6_after(n):
    for i in range(n):              # lazy — caller decides whether to materialize
        if i % 2 == 0:
            yield i * i


# ---- run -----------------------------------------------------------------

if __name__ == "__main__":
    print("B1:", b1_after(["a", "b", "c"]))
    print("B2:", b2_after([(1, 2), (3, 4)]))
    print("B3:", b3_after("data.csv", write=True))
    print("B4:", b4_after([3, 1, 4, 1, 5, 9, 2, 6]))

    # Demonstrate the b5 bug:
    print("B5 bug:", b5_before("x"), b5_before("y"), b5_before("z"), " <- shared!")
    print("B5 fix:", b5_after("x"), b5_after("y"), b5_after("z"))

    # b6 — peek without materializing the whole sequence
    from itertools import islice
    print("B6 first 5 of huge:", list(islice(b6_after(1_000_000_000), 5)))
