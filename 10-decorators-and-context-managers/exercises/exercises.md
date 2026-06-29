# Module 10 — Exercises

## E10.1 — `@timed`

Write a `@timed` decorator that prints how long the wrapped function takes. Apply it to a function that sums squares up to N. Make sure `help(your_function)` still shows the *original* docstring, not the wrapper's.

## E10.2 — Retry with backoff

Write `@retry(times=3, backoff=2.0, on=(ConnectionError, TimeoutError))`. First retry after 1s, then 2s, then 4s. Re-raise only if all attempts fail.

## E10.3 — Authorization decorator

Write `@requires_role(role)` that checks a global "current_user" dict's `role` field before running the function; raises `PermissionError` if not authorized. Decorate two functions with different roles. Show that calling the wrong one raises.

## E10.4 — `@cache` correctness

Memoize a recursive `def count_paths(m, n)` that counts paths from (0,0) to (m,n) moving only right or down. With `@cache`, `count_paths(20, 20)` should be near-instant. Why does `@cache` work here but would be wrong on a function that depends on the time, files, or random state?

## E10.5 — Custom context manager

Write `@contextmanager`-based `cd(new_dir)` that changes the working directory on enter and restores it on exit (even if the block raises). Test by `os.getcwd()` before and after.

## E10.6 — `ExitStack` with unknown count

Write a function `merge_files(*paths)` that opens N files (unknown at write time), yields all their lines (in order, file by file), and ensures all files close even if one fails to open.
