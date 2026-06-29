# Module 05 — Exercises

## E05.1 — Build a tiny package

Create `mylib/` with this structure:
```
mylib/
├── __init__.py
├── text.py     # contains slugify(s), titlecase(s)
├── numbers.py  # contains is_prime(n), nth_prime(n)
└── time.py     # contains seconds_to_hms(sec)
```
Make sure `from mylib.text import slugify` works. Bonus: in `__init__.py`, re-export the most-used functions so `from mylib import slugify` also works.

## E05.2 — Both library and script

Take your `numbers.py` from E05.1 and add a `__main__` block: when run as `python mylib/numbers.py 100`, it prints all primes up to 100. When imported, that doesn't execute.

## E05.3 — venv hygiene

In a fresh directory:
1. Create a venv.
2. Activate it.
3. Install `requests`.
4. Run `pip freeze > requirements.txt`.
5. Deactivate. Delete the venv. Recreate it from `requirements.txt`. Verify the same packages are installed.

## E05.4 — Find a stdlib solution

For each, find a stdlib module that solves it. (No third-party packages.)
1. Parse `"2026-06-29T14:30:00"` into a date/time object.
2. URL-encode a string.
3. Compute SHA-256 of a string.
4. Iterate over all pairs `(i, j)` with `i < j` from a list.
5. Run a shell command and capture its output.

## E05.5 — Spot the import smell

```python
# In data_loader.py
from utils import *
```
Why is this a maintenance problem? Suggest a better alternative.
