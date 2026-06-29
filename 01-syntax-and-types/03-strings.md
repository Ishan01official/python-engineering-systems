# 03 — Strings

A `str` is an **immutable** sequence of Unicode characters. Three things to internalize:

1. Immutable means no method "modifies a string". Every string method returns a *new* string.
2. Strings are sequences, so all sequence operations work: indexing, slicing, iteration, `in`, `len()`.
3. Python strings are Unicode by default. ASCII is a subset; you don't have to think about encoding until you read from or write to bytes.

## Creating strings

```python
s = "hello"
s = 'hello'             # single and double quotes are equivalent
s = """multi
        line"""         # triple-quoted strings preserve newlines
s = r"C:\Users\foo"     # raw string — backslashes are literal
s = b"bytes"            # not a str! a `bytes` object — covered later
```

## f-strings (use these by default)

```python
name = "Ishan"
score = 87.5

# Old style — avoid
print("Hi %s, your score is %.2f" % (name, score))
print("Hi {}, your score is {:.2f}".format(name, score))

# f-string — preferred
print(f"Hi {name}, your score is {score:.2f}")
```

Format spec after the colon: `{value:width.precisionFormat}`. A few useful ones:

```python
f"{42:5d}"        # "   42"     width 5, integer
f"{3.14159:.2f}"  # "3.14"      2 decimal places
f"{1000000:,}"    # "1,000,000" thousands separator
f"{0.5:.1%}"      # "50.0%"     percent
f"{255:08b}"      # "11111111"  binary, zero-padded to 8
f"{42:>10}"       # "        42" right-align in width 10
f"{name!r}"       # "'Ishan'"   use repr() instead of str()
```

## Useful methods

These all return **new** strings (or other values), not modifying the original:

```python
"  hello  ".strip()         # "hello"
"hello".upper()             # "HELLO"
"Hello".lower()             # "hello"
"hello".replace("l", "L")   # "heLLo"
"a,b,c".split(",")          # ["a", "b", "c"]
",".join(["a", "b", "c"])   # "a,b,c"
"hello".startswith("he")    # True
"hello".endswith("lo")      # True
"hello".find("l")           # 2     — -1 if not found
"hello".index("l")          # 2     — raises ValueError if not found
"hello world".count("l")    # 3
"42".isdigit()              # True
"abc".isalpha()             # True
```

`str.join` is the right way to assemble a string from many parts. **Do not** loop with `s = s + part` — that's quadratic time because each concat creates a new string.

```python
# BAD
result = ""
for x in many_strings:
    result = result + x       # O(n^2)

# GOOD
result = "".join(many_strings)  # O(n)
```

## Slicing

Slicing returns a new string `[start:stop:step]`:

```python
s = "abcdefgh"
s[0]        # "a"
s[-1]       # "h"
s[2:5]      # "cde"
s[:3]       # "abc"
s[::2]      # "acef" — every 2nd char
s[::-1]     # "hgfedcba" — reversed
```

Negative indices count from the end. `start` is inclusive; `stop` is exclusive — that's why `s[2:5]` gives you 3 characters, not 4.

## Strings vs bytes (the brief version)

```python
"héllo".encode("utf-8")     # b'h\xc3\xa9llo'   — turns str into bytes
b'h\xc3\xa9llo'.decode("utf-8")   # "héllo"     — turns bytes into str
```

- `str` is for **text**.
- `bytes` is for **raw data** (files on disk, network packets, image data).
- Reading a text file gives you `str`. Reading a binary file (`open(path, "rb")`) gives you `bytes`.
- Most encoding pain comes from mixing the two, or assuming the wrong encoding. UTF-8 is the right default for ~everything modern.

## Pitfalls

- **String concatenation in loops** — use `join`.
- **`==` works on strings.** No surprises. (Unlike Java's `equals` vs `==`.)
- **`is` does not do what you think.** Two strings can be equal but not identical: `s1 is s2` checks *same object*, not *same value*. CPython sometimes interns short strings, which makes `is` *seem* to work — don't rely on it.
- **Multi-line strings keep indentation.** Use `textwrap.dedent()` if you want them clean.

## Try it

Run [`examples/02_strings.py`](./examples/02_strings.py).

## Read deeper

- **LP** 6e, Ch. 7 — strings in detail.
- **FP** 2e, Ch. 4 — Unicode text vs bytes (essential read if you do any text data work).
