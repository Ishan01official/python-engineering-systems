"""
Function patterns: arguments, closures, first-class usage.

Run:
    python 04-functions/examples/01_functions.py
"""
from functools import cache, partial
from operator import attrgetter
from typing import NamedTuple


# ---- arguments showcase ---------------------------------------------------

def connect(host: str, *, port: int = 5432, timeout: int = 30) -> str:
    """Keyword-only port and timeout — callers must name them."""
    return f"connecting to {host}:{port} (timeout={timeout}s)"


def total(*numbers: float) -> float:
    """Variable positional args."""
    return sum(numbers)


def configure(**options) -> None:
    """Variable keyword args."""
    for k, v in options.items():
        print(f"  {k} = {v}")


# ---- closures -------------------------------------------------------------

def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step


def make_multiplier(factor: float):
    def multiply(x: float) -> float:
        return x * factor
    return multiply


# ---- first-class function dispatch ----------------------------------------

def handle_create(payload): return f"created {payload}"
def handle_read(payload): return f"read {payload}"
def handle_update(payload): return f"updated {payload}"
def handle_delete(payload): return f"deleted {payload}"
def handle_unknown(payload): return f"unknown action for {payload}"


HANDLERS = {
    "POST":   handle_create,
    "GET":    handle_read,
    "PUT":    handle_update,
    "DELETE": handle_delete,
}


def dispatch(method: str, payload):
    return HANDLERS.get(method, handle_unknown)(payload)


# ---- memoization with @cache ---------------------------------------------

@cache
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ---- sorting with key -----------------------------------------------------

class Product(NamedTuple):
    name: str
    price: float
    rating: float


def sort_examples() -> None:
    products = [
        Product("A", 10.0, 4.5),
        Product("B", 8.5,  4.8),
        Product("C", 12.0, 4.2),
    ]
    print("--- sort by price ascending ---")
    for p in sorted(products, key=attrgetter("price")):
        print(p)
    print("--- sort by rating desc, then name asc ---")
    for p in sorted(products, key=lambda p: (-p.rating, p.name)):
        print(p)


# ---- main -----------------------------------------------------------------

if __name__ == "__main__":
    print(connect("db.prod.example.com"))
    print(connect("db.prod.example.com", port=5433, timeout=60))
    print()

    print(f"total(1, 2, 3, 4) = {total(1, 2, 3, 4)}")
    print("configure(...):")
    configure(host="db", port=5432, retries=3)
    print()

    counter = make_counter()
    print("counter:", counter(), counter(), counter())

    double = make_multiplier(2)
    print(f"double(10) = {double(10)}")
    print()

    print("dispatch:", dispatch("GET", "item-42"))
    print("dispatch:", dispatch("PATCH", "item-42"))
    print()

    print(f"fib(50) = {fib(50)}  (cached, fast)")
    print()

    sort_examples()
    print()

    pow_with_2 = partial(pow, 2)        # 2 ** exp
    print(f"partial pow(2, 10) = {pow_with_2(10)}")
