# Module 00 — Exercises

Do these in a file `solutions.py` in this folder. **Predict the output before running.** If you predicted wrong, that's gold — go back to the note that covers it.

## E00.1 — Predict the output

```python
a = [1, 2, 3]
b = a
b = b + [4]      # NOTE: this is NOT b.append(4)
print(a)
print(b)
```

What does each line print? **Why?** (Hint: `+` on lists returns a new list; it doesn't mutate either side.)

## E00.2 — Predict the output

```python
x = "hello"
y = x
x = x.upper()
print(x, y)
```

Why doesn't `y` become `"HELLO"`?

## E00.3 — Bytecode inspection

Write a function `multiply_then_add(a, b, c)` that returns `a * b + c`. Use `dis.dis` to print its bytecode. How many ops are there? Which op does the multiplication?

## E00.4 — Stack reading

Trigger a `ZeroDivisionError` from a function `inner()` called by `outer()` called from the module top-level. Read the traceback. Confirm in your own words: *which line is the actual error, and which lines are the call chain?*

## E00.5 — Identity vs equality

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)         # ?
print(a is b)         # ?
print(id(a) == id(b)) # ?
```

What's the difference between `==` and `is`?

## E00.6 — Sanity-check your setup

Run [`examples/02_check_setup.py`](../examples/02_check_setup.py). Fix anything reported as missing. Commit a note `setup-notes.md` capturing your Python version and OS.

---

When you're done, commit:

```bash
git add 00-foundations/exercises/
git commit -m "NOTES(00): exercises solutions"
```
