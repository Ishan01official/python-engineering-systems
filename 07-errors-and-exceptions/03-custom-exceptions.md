# 03 — Custom exceptions

Define your own when:

1. Your library/module has a class of error specific to it that callers might want to handle differently.
2. A built-in exception is *too general* — `ValueError` could mean anything.

Don't define one for every bad input. Reuse `ValueError`, `TypeError`, `KeyError`, etc. when they fit.

## How

```python
class AppError(Exception):
    """Base class for this app's errors."""

class ConfigError(AppError):
    """A config file is missing or invalid."""

class DatabaseError(AppError):
    """Something went wrong talking to the database."""

class DatabaseTimeoutError(DatabaseError):
    """Database operation timed out."""
```

Now callers can choose:

```python
try:
    run()
except DatabaseTimeoutError:
    retry()
except DatabaseError:
    fall_back()
except AppError:
    crash_with_helpful_message()
```

Catching the **base** of your hierarchy (`AppError`) lets callers handle "anything from our library" without enumerating every subtype.

## Attaching data

You can add fields:

```python
class HTTPError(Exception):
    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status

try:
    fetch()
except HTTPError as e:
    if e.status == 404:
        return None
    raise
```

## Don't over-engineer

If you find yourself defining 20 custom exception classes for a small project, you're over-engineering. A reasonable rule:

- 1–2 base classes per library/component.
- A handful of specific subclasses for the cases callers actually care about.
- Everything else uses built-ins (`ValueError`, `KeyError`, etc.).

## Read deeper

- **LP** 6e, Ch. 35 (exception objects)
- **EP** 3e — items on exception hierarchies
