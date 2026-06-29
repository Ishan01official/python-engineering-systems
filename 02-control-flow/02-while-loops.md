# 02 — `while` loops

Use `while` when you **don't know in advance** how many iterations you'll need — you're looping *until something happens*.

## Shape

```python
while condition:
    ...
```

The condition is checked **before** each iteration. If it's false the first time, the body never runs.

## Three common patterns

### 1. Repeat until input is valid

```python
while True:
    choice = input("Enter y or n: ").strip().lower()
    if choice in ("y", "n"):
        break
    print("Please enter y or n.")
```

`while True` + `break` is the standard way to loop forever-with-an-exit. Don't be afraid of it.

### 2. Process until a sentinel

```python
total = 0
while (n := read_next_number()) is not None:
    total += n
```

The walrus operator (`:=`) shines here — assigns *and* tests in one expression.

### 3. Polling

```python
import time

while not job.is_done():
    time.sleep(1)
```

Used everywhere in data pipelines and APIs. Add a max-retry counter so you don't poll forever:

```python
for _ in range(60):       # at most 60 seconds
    if job.is_done():
        break
    time.sleep(1)
else:
    raise TimeoutError("Job did not finish in 60s")
```

(That's actually a `for-else` — see [`04-break-continue-else.md`](./04-break-continue-else.md).)

## Pitfalls

- **Infinite loops.** If the condition can never become false, you'll hang. Always identify the exit condition before writing the loop.
- **`while True:` with no `break`** — same problem.
- **Off-by-one in counters.** If you find yourself writing `i = 0` then `while i < n: ... i += 1`, you almost always want a `for` loop instead.

## When to prefer `for`

If you're iterating over a known collection or a known number of times, use `for`. `while` is for "loop until a condition flips".
