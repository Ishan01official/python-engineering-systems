"""
01 — Your first Python program, annotated.

Run me:
    python 00-foundations/examples/01_hello.py
"""

# A string literal. Python created a `str` object in memory.
# `print` is a built-in function that writes to standard output.
print("Hello, Python.")

# Variables: names that point at objects.
year = 2026
language = "Python"

# f-strings interpolate values into a string template. Use them by default.
print(f"You are learning {language} in {year}.")

# A simple expression. Python evaluates the right side first (creates the
# integer object 4), then binds the name `result` to it.
result = 2 + 2
print(f"2 + 2 = {result}")
