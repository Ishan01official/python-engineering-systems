# 01 — Type hints

Type hints are annotations. They don't affect runtime behavior — Python doesn't enforce them. Their value comes from tools: editors that autocomplete based on them, type checkers (mypy, pyright) that catch mismatches, and humans who read your code.

## Basics

```python
def greet(name: str, times: int = 1) -> str:
    return ("Hello, " + name + "!") * times

age: int = 25
names: list[str] = ["Alice", "Bob"]
```

The syntax: `name: TYPE = default`. For functions, parameter annotations follow each param; return type follows `->`.

## Modern (3.9+) collection syntax

```python
# Old style (Python 3.8 and earlier, needs `from typing import ...`)
from typing import List, Dict, Tuple, Set, Optional

def f(xs: List[int], by: Dict[str, int]) -> Optional[Tuple[int, str]]: ...

# Modern (Python 3.9+) — just use the built-ins
def f(xs: list[int], by: dict[str, int]) -> tuple[int, str] | None: ...
```

The new style is shorter, doesn't require imports, and is the idiom for any new code. Targeting Python 3.11+ as this curriculum does, **use the modern syntax**.

## Common types

```python
x: int = 1
x: float = 1.5
x: str = "hi"
x: bool = True
x: bytes = b"raw"
x: None = None              # rare — usually appears as `int | None`

xs: list[int] = [1, 2, 3]
ys: dict[str, float] = {"a": 1.0}
zs: tuple[int, str, bool] = (1, "x", True)        # fixed length, typed positions
ws: tuple[int, ...] = (1, 2, 3, 4)                # variable length, all int
us: set[str] = {"a", "b"}

# Optional values
x: int | None = None                              # 3.10+
from typing import Optional
x: Optional[int] = None                           # older syntax, same meaning

# Either-or
result: int | str

# Callable — `Callable[[arg types], return type]`
from typing import Callable
on_event: Callable[[str, int], None]

# Any escape hatch
from typing import Any
x: Any                       # disables checking — use sparingly
```

## Type aliases

```python
type UserId = int
type Headers = dict[str, str]
type JsonValue = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]

def get_user(id: UserId) -> dict: ...
```

`type` statements are Python 3.12+. Before that, `UserId = int` works as an assignment-style alias.

## `Literal` and `Final`

```python
from typing import Literal, Final

MAX_RETRIES: Final = 3                  # treated as a constant

def open_file(mode: Literal["r", "w", "a"]) -> None: ...
```

`Literal` says "only these exact values are valid". `Final` says "this should not be reassigned".

## `TypedDict` — typed dictionaries

```python
from typing import TypedDict

class User(TypedDict):
    id: int
    name: str
    email: str

def save(user: User) -> None: ...

save({"id": 1, "name": "Ishan", "email": "i@x.com"})        # OK
save({"id": 1, "name": "Ishan"})                            # missing 'email' — mypy error
```

Great for JSON-like data. For domain models you control, prefer `@dataclass` (you get methods, equality, `__repr__`, etc.).

## Running the type checker

```bash
pip install mypy
mypy your_file.py
```

mypy reads the hints and reports inconsistencies *before you run the code*. The catch: it only checks what's annotated. Untyped code is invisible to it. Add hints incrementally; even partial coverage catches a lot.

Strict mode (`mypy --strict`) demands hints everywhere and is worth turning on for new projects.

## When to add hints

- **Function signatures** — always. They're the contract.
- **Module-level constants** — usually inferred fine; annotate only when ambiguous.
- **Local variables** — only when type inference is wrong or unclear.
- **Class attributes** — yes. Especially for fields that don't have a clear default.

## Pitfalls

- **Hints are not runtime checked.** `greet(123)` won't raise; mypy will catch it before you ship.
- **`Optional[T]` vs `T | None`** — they mean the same thing. Pick one style; the modern `T | None` is shorter.
- **Forward references.** If you need to reference a class before it's defined (e.g. methods returning `Self`), use a string: `def copy(self) -> "MyClass":`. Python 3.11+ has `from typing import Self` which is cleaner.

## Read deeper

- **EP** 3e — the items on typing are excellent
- **FP** 2e, Ch. 8
- mypy docs and the official Python typing docs
