"""
Demonstrate that Python names are references, not boxes.

Predict each print BEFORE you run me.

Run:
    python 00-foundations/examples/03_names_and_objects.py
"""


def demo_immutable_rebinding() -> None:
    print("--- Immutable rebinding ---")
    a = 10
    b = a            # b now refers to the same int object 10
    a = 20           # rebind a to a NEW int object 20
    print(f"a = {a}, b = {b}")  # a=20, b=10  — b is unaffected
    print(f"id(a) == id(b)? {id(a) == id(b)}")
    print()


def demo_mutable_aliasing() -> None:
    print("--- Mutable aliasing ---")
    a = [1, 2, 3]
    b = a            # b is ANOTHER NAME for the same list
    b.append(4)
    print(f"a = {a}")  # [1, 2, 3, 4]  — a sees the change too
    print(f"b = {b}")
    print(f"id(a) == id(b)? {id(a) == id(b)}  (same object)")
    print()


def demo_copying() -> None:
    print("--- Asking for a copy ---")
    a = [1, 2, 3]
    b = a.copy()
    b.append(4)
    print(f"a = {a}")  # [1, 2, 3]  unchanged
    print(f"b = {b}")  # [1, 2, 3, 4]
    print()


def demo_nested_copy_trap() -> None:
    print("--- Shallow copy trap ---")
    nested = [[1, 2], [3, 4]]
    shallow = nested.copy()
    shallow[0].append(99)       # mutate the inner list
    print(f"nested  = {nested}")   # the inner list changed in both
    print(f"shallow = {shallow}")
    print("Use copy.deepcopy() when nested structure must be fully independent.")
    print()


def demo_function_arguments() -> None:
    print("--- Function arguments ---")

    def add_one(seq: list) -> None:
        seq.append("appended-inside-fn")

    items = ["a", "b"]
    add_one(items)
    print(f"items = {items}  (the function mutated our list)")
    print()


if __name__ == "__main__":
    demo_immutable_rebinding()
    demo_mutable_aliasing()
    demo_copying()
    demo_nested_copy_trap()
    demo_function_arguments()
