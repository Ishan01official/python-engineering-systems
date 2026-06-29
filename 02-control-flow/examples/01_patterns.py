"""
Control flow patterns — conditionals and loops you'll actually use.

Run:
    python 02-control-flow/examples/01_patterns.py
"""


def grade(score: float) -> str:
    """Chained comparisons + early return."""
    if score < 0 or score > 100:
        return "invalid"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def find_first(predicate, items):
    """Find-first using return-from-loop."""
    for item in items:
        if predicate(item):
            return item
    return None


def loop_else_demo() -> None:
    """The under-used for-else."""
    haystack = [1, 3, 5, 7]
    needle = 4
    for x in haystack:
        if x == needle:
            print(f"found {needle}")
            break
    else:
        print(f"{needle} not in {haystack}")


def parallel_iteration() -> None:
    """zip and enumerate."""
    names = ["Alice", "Bob", "Carol"]
    scores = [88, 73, 91]
    for rank, (name, score) in enumerate(zip(names, scores), start=1):
        print(f"{rank}. {name:5s} {score}")


def comprehensions() -> None:
    """Comprehensions for transform-and-filter."""
    nums = list(range(-5, 6))
    positives_squared = [n * n for n in nums if n > 0]
    print(f"positives squared: {positives_squared}")

    parity = {n: ("even" if n % 2 == 0 else "odd") for n in range(5)}
    print(f"parity dict: {parity}")


def match_demo() -> None:
    """Pattern matching for shape-based dispatch (Python 3.10+)."""
    events = [
        {"type": "click", "x": 10, "y": 20},
        {"type": "scroll", "delta": -3},
        {"type": "keypress", "key": "Enter"},
        "not a dict",
    ]
    for ev in events:
        match ev:
            case {"type": "click", "x": x, "y": y}:
                print(f"click at ({x}, {y})")
            case {"type": "scroll", "delta": d}:
                print(f"scroll by {d}")
            case {"type": t}:
                print(f"unknown event type: {t}")
            case _:
                print(f"not an event: {ev!r}")


if __name__ == "__main__":
    print("grades:", [grade(s) for s in [95, 82, 73, 60, 30, -5]])
    print("find_first even:", find_first(lambda x: x % 2 == 0, [1, 3, 7, 8, 9]))
    print()
    loop_else_demo()
    print()
    parallel_iteration()
    print()
    comprehensions()
    print()
    match_demo()
