# 04 — Error-handling best practices

Six rules of thumb. Internalize these.

## 1. Catch specific exceptions

```python
# BAD
try:
    parse(data)
except Exception:
    return None

# GOOD
try:
    parse(data)
except (ValueError, TypeError):
    return None
```

The narrower the catch, the more bugs survive intact for you to fix. A `KeyError` from a typo deep inside `parse` is a bug. A `ValueError` from bad user input is something to handle.

## 2. Catch where you can do something useful

Don't sprinkle `try/except` everywhere "just in case". Catch:

- Where you have a meaningful **recovery** (retry, default, fallback).
- At program **boundaries** (CLI entry point, HTTP handler) to turn an exception into a user-friendly error message.

Everything in between should let the exception propagate. That's how errors find their way to a caller who *can* handle them.

## 3. Don't catch and ignore

```python
# BAD
try:
    do_thing()
except Exception:
    pass

# Better if you really do want to ignore one specific thing:
from contextlib import suppress
with suppress(FileNotFoundError):
    Path("optional.cfg").unlink()
```

Silent swallowing of every error is the single biggest debt you can take on in a codebase. Three months later, when the system behaves weirdly, nobody knows why.

## 4. Use the right granularity

```python
# Too coarse: error wraps a lot, message is vague
try:
    config = load_config()
    db = connect(config["db_url"])
    data = fetch(db)
    save(data, config["out_path"])
except Exception as e:
    log("something went wrong", e)

# Better: each block has its own meaning
try:
    config = load_config()
except FileNotFoundError:
    fail("config file missing — create config.yaml")

try:
    db = connect(config["db_url"])
except OperationalError as e:
    fail(f"could not connect to db: {e}")

# ... etc.
```

## 5. Add context with `raise ... from ...`

When you re-raise a different exception, wrap with `from`:

```python
try:
    parsed = json.loads(text)
except json.JSONDecodeError as e:
    raise ConfigError(f"config at {path} is not valid JSON") from e
```

The traceback now shows *both* — you see what went wrong AND where in your code the bigger failure happened. Don't lose information.

## 6. EAFP, not LBYL

"Easier to Ask Forgiveness than Permission" — the Pythonic approach. Try the thing; handle the failure:

```python
# Pythonic
try:
    value = d["key"]
except KeyError:
    value = default

# Or with .get(), which encapsulates this pattern
value = d.get("key", default)
```

vs. "Look Before You Leap":

```python
# Less idiomatic in Python (and racy in concurrent code)
if "key" in d:
    value = d["key"]
else:
    value = default
```

EAFP is also faster than LBYL in the success case (one dict lookup vs two), and race-free in multi-threaded contexts.

## Practical: when to use which built-in

| Situation | Use |
|---|---|
| Bad value | `ValueError` |
| Bad type | `TypeError` |
| Missing key | `KeyError` |
| Out-of-range index | `IndexError` |
| Missing attribute | `AttributeError` |
| File doesn't exist | `FileNotFoundError` |
| Bad arithmetic (divide by zero) | `ArithmeticError` / `ZeroDivisionError` |
| The code path "shouldn't be reachable" | `AssertionError` (via `assert`) or `RuntimeError` |
| Not yet implemented | `NotImplementedError` |

Reach for these *before* defining your own.

## Read deeper

- **EP** 3e — items on exception handling, raising with context, and using stdlib exceptions.
- **PCC** 3e, Ch. 10 — practical patterns at a beginner level.
