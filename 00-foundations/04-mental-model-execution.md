# 04 — Mental model: names, objects, and the call stack

This is the single most important note in Module 00. Get this right and 50% of the "wait, why did Python do that?" surprises disappear.

## Everything is an object

In Python, **every value is an object**. An object is a chunk of memory with:

- An **identity** — a unique address (you can see it with `id(obj)`)
- A **type** — `int`, `str`, `list`, `dict`, your own classes, etc.
- A **value** — the actual data

```python
x = 42
print(id(x), type(x), x)
# e.g. 4307886456 <class 'int'> 42
```

## Names are references, not boxes

A common mistake from C or other languages: thinking `x = 5` means "the box called `x` contains the value 5". That's wrong in Python.

The truth: `x = 5` means "**make the name `x` point to the integer object 5**". The name `x` is a label. The object lives in memory; the name is how you refer to it.

```python
a = [1, 2, 3]
b = a            # b is another label pointing to the SAME list
b.append(4)
print(a)         # [1, 2, 3, 4]  — surprised? you shouldn't be
```

```
   names                objects (in memory)
   ─────                ──────────────────
   a ───────┐
            ├──────►   [1, 2, 3, 4]
   b ───────┘
```

There is one list object. Two names point at it. Modifying it through either name shows up everywhere.

If you want a *copy*, ask for one:

```python
b = a.copy()       # for lists
import copy
b = copy.deepcopy(a)   # for nested structures
```

See [`examples/03_names_and_objects.py`](./examples/03_names_and_objects.py) for a runnable walkthrough.

## Mutable vs immutable

Some object types let you change them in place (mutable): `list`, `dict`, `set`, your custom classes by default.

Others don't (immutable): `int`, `float`, `str`, `tuple`, `frozenset`, `bool`, `None`.

```python
s = "hello"
s.upper()           # returns "HELLO" — a NEW string
print(s)            # still "hello"
```

For an immutable type, the only way to "change" the value is to rebind the name to a new object. `x = x + 1` does not modify the integer `x` points to — it creates a new integer and points `x` at it.

This distinction shows up *everywhere* in Python. Module 01 has a whole note on it.

## Namespaces and scope

A **namespace** is a mapping from names to objects. Python has several layers:

```
┌─────────────────────────────────────────┐
│  Built-ins  (print, len, str, ...)      │   ← always available
├─────────────────────────────────────────┤
│  Global     (module-level names)        │   ← top of your .py file
├─────────────────────────────────────────┤
│  Enclosing  (outer function, if nested) │
├─────────────────────────────────────────┤
│  Local      (inside the current call)   │   ← function arguments, local vars
└─────────────────────────────────────────┘
```

When you reference a name, Python searches **L → E → G → B** (Local, Enclosing, Global, Built-in) — the "LEGB rule". First match wins.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)          # "local"
    inner()
    print(x)              # "enclosing"

outer()
print(x)                  # "global"
```

We'll spend much more time on this in Module 04 (Functions).

## The call stack

When a function is called, Python pushes a new **frame** onto the call stack. The frame holds that function's local variables, its current bytecode position, and a reference back to who called it.

When the function returns, its frame is popped. The local variables vanish — unless something outside is still holding a reference to them (closures, returned objects).

You see the stack in every traceback:

```
Traceback (most recent call last):
  File "main.py", line 8, in <module>
    outer()
  File "main.py", line 5, in outer
    inner()
  File "main.py", line 2, in inner
    1 / 0
ZeroDivisionError: division by zero
```

Read tracebacks **bottom-up**: the bottom line is the actual error; the lines above are the chain of calls that got you there.

## Garbage collection

Python tracks how many references point to each object (refcounting). When the count drops to zero — no name, no list, no anything points to it — Python frees the memory immediately. There's also a cycle collector for more complex cases (two objects pointing at each other).

You almost never need to think about this. You only need to know:

- Python won't leak memory just because you "forgot to delete a variable".
- An object lives as long as *something* references it.
- Long-running programs that keep growing memory usually have a logic bug — they're appending to some list they never clear — not a "Python garbage collection failure".

## Try it

Run [`examples/03_names_and_objects.py`](./examples/03_names_and_objects.py) and [`examples/04_scope.py`](./examples/04_scope.py). Predict the output **before** you run them. The exercises in this module test exactly this.

## Read deeper

- **LP** 6e, Ch. 6 (dynamic typing) — the canonical explanation of names vs objects.
- **FP** 2e, Ch. 6 (object references, mutability, recycling) — denser but very precise.
