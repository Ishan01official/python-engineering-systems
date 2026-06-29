"""
String operations, f-strings, slicing.

Run:
    python 01-syntax-and-types/examples/02_strings.py
"""


def f_string_formatting() -> None:
    print("--- f-string format specs ---")
    pi = 3.14159265
    big = 1_500_000
    print(f"{pi:.3f}")        # 3.142
    print(f"{big:,}")          # 1,500,000
    print(f"{0.873:.1%}")      # 87.3%
    print(f"{42:>10}|")        # right-align, width 10
    print(f"{42:^10}|")        # center-align
    print(f"{42:<10}|")        # left-align
    print(f"{255:08b}")        # binary, zero-padded width 8
    print(f"{'hi'!r}")         # repr() rather than str()
    print()


def slicing() -> None:
    print("--- Slicing ---")
    s = "abcdefgh"
    print(f"s[0]    = {s[0]!r}")
    print(f"s[-1]   = {s[-1]!r}")
    print(f"s[2:5]  = {s[2:5]!r}")
    print(f"s[::2]  = {s[::2]!r}")    # every 2nd char
    print(f"s[::-1] = {s[::-1]!r}")   # reversed
    print()


def join_vs_concat() -> None:
    print("--- Use join, not += ---")
    parts = ["data", "engineering", "with", "python"]
    sentence = " ".join(parts)
    print(sentence)
    print()


def common_methods() -> None:
    print("--- Common methods ---")
    s = "   Hello, World!   "
    print(f"strip:      {s.strip()!r}")
    print(f"lower:      {s.lower().strip()!r}")
    print(f"replace:    {s.replace('World', 'Python').strip()!r}")
    csv = "a,b,c,d"
    print(f"split:      {csv.split(',')}")
    print(f"contains?   {'World' in s}")
    print()


def unicode_basics() -> None:
    print("--- Unicode and bytes ---")
    text = "héllo"
    encoded = text.encode("utf-8")
    print(f"text:    {text!r}")
    print(f"bytes:   {encoded!r}")
    print(f"decoded: {encoded.decode('utf-8')!r}")
    print()


if __name__ == "__main__":
    f_string_formatting()
    slicing()
    join_vs_concat()
    common_methods()
    unicode_basics()
