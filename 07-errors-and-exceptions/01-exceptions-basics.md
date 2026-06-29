# 01 — What exceptions are

When something goes wrong, Python **raises an exception**. The exception travels up the call stack until something catches it. If nothing catches it, Python prints the traceback and the program exits.

## The hierarchy

All exceptions inherit from `BaseException`. The ones *you* care about all inherit from `Exception` (a subclass of `BaseException`). A simplified view:

```
BaseException
├── SystemExit              # raised by sys.exit()
├── KeyboardInterrupt       # raised by Ctrl+C
└── Exception               # everything you should normally catch
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── ValueError
    ├── TypeError
    ├── AttributeError
    ├── NameError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    └── ... (many more)
```

You'll meet `KeyError`, `IndexError`, `ValueError`, `TypeError`, and `FileNotFoundError` constantly.

**Don't catch `BaseException`.** It would catch `KeyboardInterrupt` and `SystemExit` — i.e., make your program impossible to terminate.

## Raising

```python
raise ValueError("score must be 0..100")

# Re-raise inside a handler — preserves the original traceback
try:
    parse(data)
except ValueError:
    log("bad input")
    raise

# Wrap and re-raise with context
try:
    parse(data)
except ValueError as e:
    raise RuntimeError("could not parse payload") from e
```

The `from e` form is great — the traceback shows both the original and the wrapped exception, so you don't lose context.

## Reading tracebacks

Read **bottom-up**:

```
Traceback (most recent call last):
  File "main.py", line 8, in <module>      ← outermost caller
    run()
  File "main.py", line 5, in run
    parse(data)
  File "main.py", line 2, in parse
    return int(data["age"])               ← where the error actually happened
KeyError: 'age'                            ← what went wrong
```

The bottom is the error itself. Walk up to see how you got there.

When wrapping with `raise X from Y`, you'll see:

```
... lower exception ...
The above exception was the direct cause of the following exception:
... higher exception ...
```

Both tracebacks are preserved.

## Read deeper

- **LP** 6e, Ch. 33 (exception basics)
- Python docs: built-in exceptions list at https://docs.python.org/3/library/exceptions.html
