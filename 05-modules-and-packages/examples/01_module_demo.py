"""
Demonstrates a tiny self-contained module: usable both as a library
(via import) and as a script (via `python 01_module_demo.py`).

Try:
    python 05-modules-and-packages/examples/01_module_demo.py
    python -c "from importlib import import_module; m = import_module('05-modules-and-packages.examples.01_module_demo'); print(m.area_of_circle(5))"
"""

PI = 3.14159265358979


def area_of_circle(r: float) -> float:
    """Return the area of a circle with radius r."""
    return PI * r * r


def circumference(r: float) -> float:
    """Return the circumference of a circle with radius r."""
    return 2 * PI * r


def _private_helper() -> str:
    """Leading underscore = 'don't rely on me from outside this module'."""
    return "internal"


if __name__ == "__main__":
    # This block only runs when the file is executed directly.
    print(f"PI = {PI}")
    print(f"area of r=5:          {area_of_circle(5):.2f}")
    print(f"circumference of r=5: {circumference(5):.2f}")
