# 02 — Numeric types

## Three core numeric types

| Type | Example | Notes |
|---|---|---|
| `int` | `42`, `-17`, `0`, `10**100` | Arbitrary precision — no overflow |
| `float` | `3.14`, `1.0`, `1e-9` | IEEE 754 double-precision |
| `complex` | `2+3j` | Rarely used outside scientific code |

There's also `bool`, which is technically a subclass of `int` (`True == 1`, `False == 0`).

## The "no overflow" superpower of `int`

In C, an `int` is typically 32 or 64 bits — overflow causes wrap-around or undefined behavior. In Python:

```python
>>> 2 ** 100
1267650600228229401496703205376
>>> _ * 10
12676506002282294014967032053760
```

Python's `int` grows as large as your RAM allows. This is fantastic for correctness, mildly costly for performance. (NumPy fixes this by giving you fixed-size integers when you need raw speed.)

## Float gotchas — read this and remember it

```python
>>> 0.1 + 0.2
0.30000000000000004
```

This is **not a Python bug**. It's how floating-point works in every language. Floats are stored in binary; 0.1 has no exact binary representation, just like 1/3 has no exact decimal representation.

Consequences:

- **Never compare floats with `==`.** Use a tolerance: `abs(a - b) < 1e-9`, or `math.isclose(a, b)`.
- **Never use floats for money.** Use `decimal.Decimal` or work in integer cents.

```python
from decimal import Decimal
price = Decimal("19.99")    # exact
tax = Decimal("0.07")
total = price * (1 + tax)
print(total)   # 21.3893
```

## Arithmetic operators

```python
7 / 2     # 3.5      — true division, always returns float
7 // 2    # 3        — floor division
7 % 2     # 1        — modulo
2 ** 10   # 1024     — exponent
divmod(7, 2)  # (3, 1)  — floor div + mod in one call
```

Floor division rounds **toward negative infinity**, which surprises some people:

```python
-7 // 2   # -4, not -3
```

## Bitwise operators (rarely needed, but nice to know)

```python
a & b     # AND
a | b     # OR
a ^ b     # XOR
~a        # NOT
a << 2    # left shift (multiply by 4)
a >> 1    # right shift (divide by 2)
```

You'll meet these in pandas/NumPy with boolean masks, and in low-level work.

## Reading numeric literals

```python
1_000_000        # underscore for readability, same as 1000000
0b1010           # binary  (= 10)
0o755            # octal   (= 493)
0xff             # hex     (= 255)
1e6              # scientific notation (= 1_000_000.0, a float)
```

## Conversions

```python
int("42")           # 42
int("42", 16)       # 66  (parse as hex)
float("3.14")       # 3.14
str(42)             # "42"
int(3.9)            # 3   (truncates toward zero — not rounded!)
round(3.5)          # 4   (banker's rounding — round half to EVEN; 2.5 → 2!)
round(3.567, 2)     # 3.57
```

`round` using banker's rounding is another "this isn't a bug" detail — it reduces statistical bias when rounding many numbers.

## Try it

Run [`examples/01_numbers.py`](./examples/01_numbers.py).

## Read deeper

- **LP** 6e, Ch. 5 — numeric types in depth.
- **PfDA** 3e, App. A — numeric precision for data work.
