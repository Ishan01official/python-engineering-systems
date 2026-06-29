# Module 11 — Exercises

## E11.1 — Add hints to an existing function

Annotate the parameters and return of:
```python
def histogram(items, key=lambda x: x):
    counts = {}
    for item in items:
        k = key(item)
        counts[k] = counts.get(k, 0) + 1
    return counts
```
Make sure mypy is happy. (Hint: you'll need a `Callable` and a generic `T`.)

## E11.2 — Optional vs not

These two signatures look similar but mean different things. Explain in your own words:
```python
def a(x: int | None = None) -> str: ...
def b(x: int = 0) -> str: ...
```
Which would you pick for: "called with no argument means use a default" vs "called with no argument means do nothing"?

## E11.3 — Protocol

Define a `Protocol` called `Drawable` with a method `draw(self) -> str`. Write `render(items: list[Drawable]) -> str` that joins draws with newlines. Show that a class with a `draw` method works without inheriting from `Drawable`.

## E11.4 — TypedDict for JSON

You receive payloads like:
```python
{"user": {"id": 1, "name": "Alice"}, "events": [{"type": "login", "ts": "..."}, ...]}
```
Write `Payload`, `User`, `Event` as TypedDicts. Use a `Literal` for `event.type` (only allow `"login"`, `"logout"`, `"signup"`).

## E11.5 — Generic stack

Implement `class Stack[T]` with `push`, `pop`, `peek`, `__len__`, `__bool__`. Make sure a `Stack[int]` rejects `push("hi")` according to mypy.

## E11.6 — Install and run mypy

In your venv: `pip install mypy`. Run `mypy 11-typing-and-protocols/` and fix any complaints. Commit a screenshot or text snippet of clean output.
