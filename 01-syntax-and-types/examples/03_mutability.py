"""
Mutable vs immutable behavior — the source of many surprises.

Run:
    python 01-syntax-and-types/examples/03_mutability.py
"""


def mutating_argument_pitfall() -> None:
    print("--- Mutating a function argument ---")

    def append_99(items):
        items.append(99)        # mutates the caller's list

    xs = [1, 2, 3]
    append_99(xs)
    print(f"xs after call: {xs}")
    print()


def default_argument_trap() -> None:
    print("--- The mutable default argument trap ---")

    def bad(item, items=[]):    # <-- danger
        items.append(item)
        return items

    print(f"bad('a'): {bad('a')}")
    print(f"bad('b'): {bad('b')}")
    print(f"bad('c'): {bad('c')}  <- yikes, list persisted")
    print()


def default_argument_fix() -> None:
    print("--- The safe pattern ---")

    def good(item, items=None):
        if items is None:
            items = []
            items.append(item)
        return items

    print(f"good('a'): {good('a')}")
    print(f"good('b'): {good('b')}")
    print()


def tuple_shallow_immutability() -> None:
    print("--- Tuple immutability is shallow ---")
    t = ([1, 2], [3, 4])
    try:
        t[0] = [9, 9]
    except TypeError as e:
        print(f"can't rebind slot: {e}")
    t[0].append(99)
    print(f"but inner list mutated: {t}")
    print()


def hashability() -> None:
    print("--- Only hashable values can be dict keys / set members ---")
    d = {(1, 2): "tuple key OK"}
    print(d)
    try:
        d2 = {[1, 2]: "list key bad"}
    except TypeError as e:
        print(f"list as key: {e}")
    print()


if __name__ == "__main__":
    mutating_argument_pitfall()
    default_argument_trap()
    default_argument_fix()
    tuple_shallow_immutability()
    hashability()
