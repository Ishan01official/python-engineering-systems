"""
Demonstrate the LEGB scope rule: Local, Enclosing, Global, Built-in.

Run:
    python 00-foundations/examples/04_scope.py
"""

x = "G — global"


def outer() -> None:
    x = "E — enclosing"

    def inner() -> None:
        x = "L — local"
        print(f"inner sees x = {x!r}")

    inner()
    print(f"outer sees x = {x!r}")


def shows_builtin_resolution() -> None:
    # `len` is a built-in. We didn't define it locally; Python finds it in B.
    print(f"len('python') = {len('python')}")


def shadows_a_builtin() -> None:
    # DON'T do this in real code. Demonstrating that local names shadow builtins.
    len = "I'm not the builtin anymore"
    print(f"Inside shadows_a_builtin: len = {len!r}")


if __name__ == "__main__":
    outer()
    print(f"module sees x = {x!r}")
    print()
    shows_builtin_resolution()
    shadows_a_builtin()
    # After shadows_a_builtin returns, the builtin is fine again — `len` was local.
    print(f"After: len('still works') = {len('still works')}")
