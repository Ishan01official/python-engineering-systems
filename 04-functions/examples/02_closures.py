"""
Closures and the late-binding gotcha.

Run:
    python 04-functions/examples/02_closures.py
"""


def late_binding_trap() -> None:
    print("--- Classic late-binding bug ---")
    funcs = [lambda: i for i in range(3)]
    results = [f() for f in funcs]
    print(f"results: {results}  (expected [0, 1, 2] — got something else)")
    print()


def late_binding_fix() -> None:
    print("--- The fix: bind i as a default ---")
    funcs = [lambda i=i: i for i in range(3)]
    results = [f() for f in funcs]
    print(f"results: {results}")
    print()


def closure_captures_reference() -> None:
    print("--- A closure captures the variable, not its value ---")
    x = 10
    def get_x():
        return x
    print(f"before: get_x() = {get_x()}")
    x = 999
    print(f"after:  get_x() = {get_x()}  (sees the new value!)")
    print()


def assignment_makes_it_local() -> None:
    print("--- Assignment in nested fn makes it local — UnboundLocalError ---")
    count = 0
    def step():
        # If we did `count = count + 1` here, Python would say count is local
        # and raise UnboundLocalError. We must declare nonlocal.
        nonlocal count
        count = count + 1
    step()
    step()
    step()
    print(f"count after 3 calls: {count}")
    print()


if __name__ == "__main__":
    late_binding_trap()
    late_binding_fix()
    closure_captures_reference()
    assignment_makes_it_local()
