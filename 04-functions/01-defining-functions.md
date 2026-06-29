# 01 — Defining functions

## The shape

```python
def add(a: int, b: int) -> int:
    """Return the sum of a and b."""
    return a + b
```

Four pieces:

1. `def name(...)` — the definition.
2. **Parameters** with optional type hints.
3. **Return type** with `->` (also optional, also a hint).
4. A **docstring** as the first statement of the body.

Type hints are not enforced at runtime. They're for readers, IDEs, and type checkers like mypy. We'll cover them in detail in Module 11; just *use them* for now.

## Docstrings

The first string in the function body is its docstring. It's the standard Python way of documenting code:

```python
def split_chunks(items: list, size: int) -> list[list]:
    """Split ``items`` into chunks of ``size`` elements.

    The final chunk may be smaller than ``size``.
    Raises ValueError if size <= 0.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items), size)]
```

Tools like `help(fn)` and Sphinx use docstrings. So do IDE tooltips. So does your future self.

Three common docstring conventions (pick one project-wide):
- **Google style** — `Args:` / `Returns:` / `Raises:` sections.
- **NumPy style** — used by NumPy, pandas, SciPy.
- **reStructuredText** — Python's own style.

For solo projects, prose-style docstrings are fine.

## Return rules

- A function without an explicit `return` returns `None`.
- `return` with no value also returns `None`.
- A function can have multiple `return` statements — early returns are great for readability.

```python
def grade(score: float) -> str:
    if score < 0 or score > 100:
        raise ValueError("score must be 0..100")
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    return "F"
```

The "single return point" style from older languages doesn't suit Python well. Early returns flatten nesting.

## Returning multiple values

A function returns one object. To "return multiple values" you return a tuple:

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

lo, hi, mean = stats([1, 2, 3, 4, 5])
```

When you have more than 2–3 things to return, switch to a `NamedTuple` or `dataclass`:

```python
from typing import NamedTuple

class Stats(NamedTuple):
    min: float
    max: float
    mean: float

def stats(numbers) -> Stats:
    return Stats(min(numbers), max(numbers), sum(numbers) / len(numbers))

r = stats(xs)
print(r.mean)
```

You keep tuple-unpacking compatibility but gain readable attribute names.

## Function objects

A function is itself an object. You can pass it around, store it in a list, attach it to another name:

```python
def shout(s): return s.upper() + "!"

f = shout                      # f points at the same function
print(f("hello"))              # "HELLO!"

actions = [str.upper, str.lower, str.title]
for fn in actions:
    print(fn("Hello World"))
```

This is the basis for callbacks, decorators, and a lot of Python's expressive power.

## Pitfalls

- **Mutable default arguments.** Covered in Module 01.05 — always use `None` and create the mutable object inside.
- **Missing return.** A function that "should return something" but has no `return` returns `None`. Type hints catch this if you use them.
- **Too many arguments.** If a function takes 6+ positional arguments, it's almost certainly trying to do too much. Split it, or pass a config object.
