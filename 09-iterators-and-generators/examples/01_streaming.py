"""
Generators, pipelines, and itertools in action.

Run:
    python 09-iterators-and-generators/examples/01_streaming.py
"""
from itertools import accumulate, groupby, islice, pairwise


# ---- generator pipeline (lazy, O(1) memory) -------------------------------

def numbers(stop: int):
    for i in range(stop):
        yield i


def evens(stream):
    for n in stream:
        if n % 2 == 0:
            yield n


def squared(stream):
    for n in stream:
        yield n * n


def pipeline_demo() -> None:
    print("--- Lazy pipeline ---")
    result = squared(evens(numbers(10)))   # nothing has run yet
    print(list(result))                    # [0, 4, 16, 36, 64]
    print()


# ---- generator function vs generator expression --------------------------

def gen_function_vs_expression() -> None:
    print("--- Function form ---")
    def squares(n):
        for i in range(n):
            yield i * i
    print(list(squares(5)))

    print("--- Expression form (same thing, terser) ---")
    sq = (i * i for i in range(5))
    print(list(sq))
    print()


# ---- single-use trap -----------------------------------------------------

def exhausted_iterator_trap() -> None:
    print("--- Iterators are single-use ---")
    g = (i * i for i in range(5))
    print(f"first sum:  {sum(g)}")
    print(f"second sum: {sum(g)}   (already exhausted)")
    print()


# ---- itertools idioms ----------------------------------------------------

def itertools_demo() -> None:
    print("--- pairwise (sliding window of 2) ---")
    temps = [70, 72, 75, 73, 80, 78]
    deltas = [b - a for a, b in pairwise(temps)]
    print(f"deltas: {deltas}")

    print("--- accumulate (running total) ---")
    print(list(accumulate([1, 2, 3, 4, 5])))

    print("--- groupby (adjacent only — sort first if needed) ---")
    transactions = [("alice", 100), ("alice", 50), ("bob", 25), ("alice", 75)]
    transactions.sort(key=lambda t: t[0])
    for user, group in groupby(transactions, key=lambda t: t[0]):
        total = sum(amt for _, amt in group)
        print(f"  {user}: {total}")

    print("--- islice (slicing an iterator) ---")
    big = (i for i in range(10_000_000))   # never materialized
    first_5 = list(islice(big, 5))
    print(first_5)
    print()


# ---- real-world: streaming a "log" file -----------------------------------

def lines_of_text(path: str):
    """Yield lines from a file, stripping trailing newlines."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def streaming_demo() -> None:
    print("--- Streaming a log file ---")
    import tempfile, pathlib
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "log.txt"
        p.write_text("INFO ok\nERROR bad\nINFO ok\nERROR worse\n")
        err_count = sum(1 for line in lines_of_text(str(p)) if line.startswith("ERROR"))
        print(f"  {err_count} errors")
    print()


if __name__ == "__main__":
    pipeline_demo()
    gen_function_vs_expression()
    exhausted_iterator_trap()
    itertools_demo()
    streaming_demo()
