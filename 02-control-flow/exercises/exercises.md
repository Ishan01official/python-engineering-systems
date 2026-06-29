# Module 02 — Exercises

## E02.1 — FizzBuzz, two ways

Print 1..30. For multiples of 3 print `Fizz`; multiples of 5 print `Buzz`; multiples of both print `FizzBuzz`.

a) Write it with `if/elif`.
b) Rewrite using a list comprehension that builds the full list, then print one per line.

## E02.2 — Replace `range(len(...))`

Refactor:
```python
words = ["apple", "banana", "cherry"]
for i in range(len(words)):
    print(f"{i + 1}: {words[i].upper()}")
```
Use `enumerate`.

## E02.3 — Parallel processing

Given:
```python
months = ["Jan", "Feb", "Mar"]
sales = [120, 85, 150]
costs = [60, 30, 90]
```

Print profit per month using a single `for` with `zip`. Make sure the loop raises an error if the lists have different lengths.

## E02.4 — Find with loop-else

Write `def find_index(xs, target)` that returns the index of `target` in `xs`, or prints `"not found"` and returns `-1`. Use a `for` loop with an `else` clause; no flag variable.

## E02.5 — Polling with timeout

Simulate polling: write `def wait_for(predicate, timeout=10, interval=1)` that calls `predicate()` once per `interval` seconds, returning `True` as soon as it does or raising `TimeoutError` after `timeout`. Use `time.sleep`.

## E02.6 — Pattern match

Build a `match` statement that, given a record like `{"type": "user", "id": 1, "name": "Ishan"}` or `{"type": "order", "id": 99, "total": 100.0}`, prints a one-line summary. Add a case for unknown shapes.
