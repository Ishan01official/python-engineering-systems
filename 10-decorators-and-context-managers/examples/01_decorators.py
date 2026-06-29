"""
Decorators and context managers in action.

Run:
    python 10-decorators-and-context-managers/examples/01_decorators.py
"""
import time
from contextlib import contextmanager
from functools import wraps


# ---- 1. Simple logging decorator -----------------------------------------

def log_calls(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"  -> {fn.__name__}({args}, {kwargs})")
        result = fn(*args, **kwargs)
        print(f"  <- {result!r}")
        return result
    return wrapper


@log_calls
def add(a, b):
    return a + b


# ---- 2. Decorator with arguments (retry) ---------------------------------

def retry(times: int = 3, delay: float = 0.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"  attempt {attempt} failed: {e}")
                    if attempt < times:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


_call_count = {"n": 0}

@retry(times=3, delay=0.01)
def flaky():
    _call_count["n"] += 1
    if _call_count["n"] < 3:
        raise RuntimeError("transient")
    return "success"


# ---- 3. Timing decorator + context manager (same idea, two forms) -------

def timed(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"  {fn.__name__} took {(time.perf_counter() - start) * 1000:.2f} ms")
    return wrapper


@contextmanager
def timing(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"  {name} took {(time.perf_counter() - start) * 1000:.2f} ms")


@timed
def crunch():
    return sum(i * i for i in range(100_000))


# ---- run -----------------------------------------------------------------

if __name__ == "__main__":
    print("--- log_calls ---")
    add(2, 3)
    print()

    print("--- retry (will fail twice, succeed on third) ---")
    result = flaky()
    print(f"final: {result}")
    print()

    print("--- timing via decorator ---")
    crunch()
    print()

    print("--- timing via context manager ---")
    with timing("inline block"):
        sum(i * i for i in range(100_000))
