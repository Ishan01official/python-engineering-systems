"""
Look at the bytecode Python actually executes.

Run me:
    python 00-foundations/examples/02_disassemble.py
"""

import dis


def add(a, b):
    return a + b


def conditional_double(x):
    if x > 0:
        return x * 2
    return 0


if __name__ == "__main__":
    print("=== Bytecode for add(a, b) ===")
    dis.dis(add)

    print("\n=== Bytecode for conditional_double(x) ===")
    dis.dis(conditional_double)

    print("\nNotice: even tiny functions become several stack-based ops.")
    print("This is what the Python VM walks through at runtime.")
