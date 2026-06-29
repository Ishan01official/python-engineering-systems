# Module 07 — Exercises

## E07.1 — Find three antipatterns

What's wrong with each? Rewrite:

```python
# A
try:
    do_thing()
except:
    pass

# B
try:
    data = fetch()
    if not data:
        return
    parse(data)
    save(data)
except Exception as e:
    print(f"failed: {e}")

# C
if "key" in d:
    v = d["key"]
else:
    v = 0
```

## E07.2 — Custom exception hierarchy

You're writing a small payment library. Design a 3-class exception hierarchy:
- A base for any payment error
- One for "card declined"
- One for "network failure"

Show a `process()` function that raises one of them and a caller that retries on network failure but gives up on declined cards.

## E07.3 — Wrap and preserve context

A config file might be missing OR present-but-invalid JSON. Write `load_config(path)` that:
- Raises `ConfigError("config file missing")` from `FileNotFoundError`
- Raises `ConfigError("config not valid JSON")` from `json.JSONDecodeError`
Both with `raise ... from ...` so the original cause is preserved.

## E07.4 — Recoverable vs unrecoverable

For each, decide: should you catch it, let it propagate, or never catch at all?
1. `FileNotFoundError` when reading a user's "optional" config.
2. `ZeroDivisionError` from a math function whose inputs you control.
3. `KeyError` from a `dict[user_id]` lookup, where missing users are normal.
4. `KeyError` from `os.environ["DATABASE_URL"]` at startup.

## E07.5 — Retry with backoff

Write `def retry(fn, max_attempts=3, on=Exception):` that calls `fn()`, retries up to `max_attempts` times if it raises `on`, with an increasing sleep (0.1s, 0.2s, 0.4s). Re-raise the last exception if all attempts fail.
