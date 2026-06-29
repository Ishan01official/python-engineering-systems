"""
Practical patterns with each container.

Run:
    python 03-data-structures/examples/01_containers.py
"""
from collections import Counter, defaultdict, deque
from typing import NamedTuple


# ---- list patterns ----------------------------------------------------------

def list_slicing() -> None:
    print("--- list slicing ---")
    xs = list(range(10))
    print(f"every 2nd:   {xs[::2]}")
    print(f"reversed:    {xs[::-1]}")
    print(f"last 3:      {xs[-3:]}")
    print()


def deque_for_both_ends() -> None:
    print("--- deque is O(1) at both ends ---")
    q = deque(["a", "b", "c"])
    q.appendleft("Z")
    q.append("D")
    print(q)
    q.popleft()
    print(q)
    print()


# ---- tuple patterns --------------------------------------------------------

class Person(NamedTuple):
    name: str
    age: int
    email: str


def namedtuple_demo() -> None:
    print("--- NamedTuple for records ---")
    p = Person("Ishan", 25, "ishan@example.com")
    print(f"{p.name} ({p.age}): {p.email}")
    # Still behaves like a tuple
    name, age, email = p
    print(f"unpacked: {name}, {age}, {email}")
    print()


# ---- dict patterns ---------------------------------------------------------

def counter_demo() -> None:
    print("--- Counter for frequencies ---")
    words = "the quick brown fox jumps over the lazy dog the".split()
    counts = Counter(words)
    print(counts)
    print(f"most common 2: {counts.most_common(2)}")
    print()


def defaultdict_group_by() -> None:
    print("--- defaultdict for grouping ---")
    transactions = [
        ("alice", 100), ("bob", 50), ("alice", 75), ("bob", 25), ("carol", 200),
    ]
    totals = defaultdict(int)
    for user, amount in transactions:
        totals[user] += amount
    print(dict(totals))
    print()


def merge_dicts() -> None:
    print("--- merging dicts ---")
    defaults = {"timeout": 30, "retries": 3, "host": "localhost"}
    overrides = {"timeout": 60, "host": "prod.example.com"}
    final = defaults | overrides       # Python 3.9+
    print(final)
    print()


# ---- set patterns ---------------------------------------------------------

def set_difference_for_validation() -> None:
    print("--- set difference for missing-field check ---")
    required = {"user_id", "email", "name"}
    payload = {"user_id": 1, "email": "x@y.com"}
    missing = required - set(payload)
    print(f"missing: {missing}")
    print()


def dedup_preserve_order() -> None:
    print("--- dedup preserving order ---")
    items = ["a", "b", "a", "c", "b", "d"]
    unique = list(dict.fromkeys(items))
    print(unique)
    print()


if __name__ == "__main__":
    list_slicing()
    deque_for_both_ends()
    namedtuple_demo()
    counter_demo()
    defaultdict_group_by()
    merge_dicts()
    set_difference_for_validation()
    dedup_preserve_order()
