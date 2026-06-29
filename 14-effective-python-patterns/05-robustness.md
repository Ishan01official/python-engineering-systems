# 05 — Robustness, performance, hardening

## Use type hints and a type checker

`mypy` or `pyright` catch entire classes of bugs (mismatched arguments, None where a value was expected, refactor mistakes). Add hints incrementally; even partial coverage helps. Don't argue with the type checker — fix the code or be explicit about the gap.

## Validate inputs at the boundary

Untrusted data (user input, API requests, files from disk) gets validated *once*, at the edge of your program. After that, internal functions can assume the data is well-formed.

This is where `pydantic`, `attrs`, and `dataclass` with `__post_init__` shine. Parse, don't just check.

## Log structured data, not strings

```python
# fragile
log(f"User {user.id} bought item {item.id} for {price}")

# better — fields, machine-grepable
logger.info("purchase", extra={"user_id": user.id, "item_id": item.id, "price": price})
```

When something breaks at 3am, you want to grep on `user_id` not parse free text.

## Use `logging`, not `print`, for anything that lives past a script

The `logging` module supports levels (DEBUG, INFO, WARNING, ERROR), handlers (file, stderr, syslog, network), and formatting. `print` doesn't, and you'll regret it the first time you want to silence INFO without removing every `print`.

## Profile before optimizing

`cProfile`, `time.perf_counter`, `timeit`. Measure before you change. The bottleneck is rarely where you guess.

```python
import cProfile
cProfile.run("main()", sort="cumulative")
```

## Reach for NumPy/pandas before threading

For numerical work, vectorizing with NumPy/pandas is usually 10–1000× faster than parallelizing pure-Python loops. Try the algorithmic fix first.

## Don't catch what you can't handle

```python
# bad — swallowed bugs
try:
    process(item)
except Exception:
    pass

# good — only specific things you actually recover from
try:
    process(item)
except (ValidationError, TimeoutError) as e:
    log.warning("skipping", item=item.id, reason=str(e))
```

## Tests are not optional past prototype stage

If the code matters for more than a day, it has tests. See Module 12.

## Read deeper

- **EP** 3e — robustness, performance, and testing chapters
