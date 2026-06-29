"""
Exception patterns: catching, raising, custom types, wrapping.

Run:
    python 07-errors-and-exceptions/examples/01_exceptions.py
"""


# ---- custom exception hierarchy --------------------------------------------

class AppError(Exception):
    """Base class for this app's errors."""


class ConfigError(AppError):
    """Something is wrong with the configuration."""


class DatabaseError(AppError):
    """Something is wrong talking to the database."""


class HTTPError(AppError):
    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status


# ---- patterns -------------------------------------------------------------

def grade(score: float) -> str:
    if not 0 <= score <= 100:
        raise ValueError(f"score must be in [0,100], got {score}")
    if score >= 90: return "A"
    if score >= 70: return "B"
    return "C"


def specific_catches() -> None:
    print("--- Catching specific exceptions ---")
    d = {"name": "Ishan"}
    try:
        d["missing"]
    except KeyError as e:
        print(f"  caught KeyError: {e}")
    print()


def else_and_finally() -> None:
    print("--- try / else / finally ---")
    try:
        x = grade(85)
    except ValueError as e:
        print(f"  bad input: {e}")
    else:
        print(f"  parsed grade: {x}")
    finally:
        print("  (finally always runs)")
    print()


def raise_from() -> None:
    print("--- raise ... from ... ---")
    try:
        try:
            int("not a number")
        except ValueError as e:
            raise ConfigError("could not parse config field 'count'") from e
    except ConfigError as e:
        print(f"  outer caught: {type(e).__name__}: {e}")
        # `e.__cause__` is the original ValueError
        print(f"  caused by: {type(e.__cause__).__name__}: {e.__cause__}")
    print()


def http_error_with_data() -> None:
    print("--- Custom exception with data ---")
    def fetch(url: str):
        raise HTTPError("not found", status=404)

    try:
        fetch("http://example.com/missing")
    except HTTPError as e:
        if e.status == 404:
            print(f"  recovering from 404")
        else:
            raise
    print()


def eafp_vs_lbyl() -> None:
    print("--- EAFP (try/except) is preferred over LBYL (if-check-then-act) ---")
    d = {"a": 1, "b": 2}

    # EAFP
    try:
        v = d["a"]
    except KeyError:
        v = 0
    print(f"  EAFP: {v}")

    # The most idiomatic in this exact case is .get()
    v = d.get("missing", 0)
    print(f"  dict.get: {v}")
    print()


if __name__ == "__main__":
    specific_catches()
    else_and_finally()
    raise_from()
    http_error_with_data()
    eafp_vs_lbyl()
