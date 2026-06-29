# 02 — `try` / `except` / `else` / `finally`

## The basic form

```python
try:
    risky()
except ValueError:
    handle_value_error()
```

If `risky()` raises `ValueError`, control jumps to the handler. If it raises something else, that propagates up — `except ValueError` doesn't catch it.

## Catching multiple types

```python
try:
    risky()
except (ValueError, KeyError) as e:
    handle(e)
```

A tuple of types catches any of them. Bind to a name with `as e` to inspect the exception.

## Multiple handlers — first match wins

```python
try:
    risky()
except KeyError:
    handle_missing_key()
except ValueError as e:
    handle_bad_value(e)
except Exception as e:
    handle_anything_else(e)
```

Order matters: a more general handler (e.g. `Exception`) catches everything below it. Put **specific** handlers before **general** ones.

## `else` — code that runs only if no exception

```python
try:
    data = parse(payload)
except ValueError:
    print("could not parse")
else:
    # runs ONLY if the try block succeeded
    save(data)
```

The `else` clause is for the "now-safe" follow-up. Without it, you'd put `save(data)` inside the `try` — meaning a bug in `save` would also be caught by `except ValueError`, which you don't want.

## `finally` — code that always runs

```python
conn = connect()
try:
    do_stuff(conn)
finally:
    conn.close()
```

`finally` runs whether or not an exception was raised, whether or not it was caught, whether or not the `try` block contains a `return`. Use it for cleanup.

Often a context manager is the cleaner way to express this. `with conn:` (when the type supports it) is the same idea with less ceremony.

## What NOT to do

### Bare except

```python
try:
    risky()
except:                  # BAD: catches EVERYTHING, including KeyboardInterrupt
    pass
```

Bare `except:` is `except BaseException:` — it catches Ctrl+C and `SystemExit`. Don't.

### Catch-all `except Exception` with no action

```python
try:
    risky()
except Exception:
    pass                # BAD: silently swallow every error
```

This is the worst pattern in Python — silently swallowing every error makes bugs invisible. If you genuinely want to ignore one specific exception:

```python
from contextlib import suppress
with suppress(FileNotFoundError):
    Path("might_not_exist").unlink()
```

`suppress` is explicit about exactly what you're ignoring.

### Catching to log and re-raise

If all you do is log and re-raise, you usually don't need to catch at all — Python's default behavior prints the traceback. Catch only when you have a specific recovery to do.

## Read deeper

- **LP** 6e, Ch. 34 (exception coding details)
- **EP** 3e — items on exceptions and error handling
