"""
Numeric type gotchas and useful patterns.

Run:
    python 01-syntax-and-types/examples/01_numbers.py
"""
import math
from decimal import Decimal


def float_gotchas() -> None:
    print("--- Float gotchas ---")
    print(f"0.1 + 0.2 = {0.1 + 0.2}")
    print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}   (False!)")
    print(f"Use math.isclose: {math.isclose(0.1 + 0.2, 0.3)}")
    print()


def use_decimal_for_money() -> None:
    print("--- Decimal for money ---")
    price = Decimal("19.99")
    tax_rate = Decimal("0.07")
    total = price * (1 + tax_rate)
    print(f"price={price}, tax={tax_rate}, total={total}")
    print()


def big_int_no_overflow() -> None:
    print("--- Integers have no fixed size ---")
    x = 2**1000
    print(f"2^1000 has {len(str(x))} decimal digits")
    print()


def banker_s_rounding_surprise() -> None:
    print("--- round() uses banker's rounding ---")
    for v in [0.5, 1.5, 2.5, 3.5, 4.5]:
        print(f"round({v}) = {round(v)}")  # rounds half to even
    print()


def divisions() -> None:
    print("--- Three kinds of division ---")
    print(f"7 / 2  = {7 / 2}    (true division)")
    print(f"7 // 2 = {7 // 2}   (floor division)")
    print(f"7 % 2  = {7 % 2}    (modulo)")
    print(f"-7 // 2 = {-7 // 2}  (floor goes toward -inf)")
    print(f"divmod(17, 5) = {divmod(17, 5)}")
    print()


if __name__ == "__main__":
    float_gotchas()
    use_decimal_for_money()
    big_int_no_overflow()
    banker_s_rounding_surprise()
    divisions()
