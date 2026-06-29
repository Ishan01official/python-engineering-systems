# 02 — Arguments

Python's argument system is rich. Used well, it makes calls self-documenting. Used poorly, it makes them impossible to read.

## Positional vs keyword arguments

```python
def greet(name, greeting):
    return f"{greeting}, {name}!"

# Positional — order matters
greet("Ishan", "Hi")

# Keyword — order doesn't, but names must match
greet(name="Ishan", greeting="Hi")
greet(greeting="Hi", name="Ishan")    # same call
```

**Use keyword arguments at the call site for any non-obvious value.** Compare:

```python
spawn_user("Ishan", 25, True, False, 3)              # what do True, False, 3 mean?
spawn_user("Ishan", age=25, active=True, banned=False, retries=3)   # clear
```

## Default values

```python
def connect(host, port=5432, timeout=30):
    ...

connect("db.example.com")                # uses defaults
connect("db.example.com", port=5433)     # override one
connect("db.example.com", timeout=60)    # by keyword
```

Defaults are evaluated **once**, when the function is defined. Never use a mutable default (`[]`, `{}`, `set()`) — covered in Module 01.05 — use `None` and create the value inside.

## `*args` — variable positional arguments

```python
def total(*numbers):
    return sum(numbers)

total(1, 2, 3)         # 6
total(1, 2, 3, 4, 5)   # 15

# You can also unpack a sequence into positional args:
xs = [1, 2, 3]
total(*xs)             # equivalent to total(1, 2, 3)
```

`*numbers` collects "any extra positional arguments" into a tuple. The name (`numbers`) is your choice; `args` is just the convention.

## `**kwargs` — variable keyword arguments

```python
def configure(**options):
    for key, value in options.items():
        print(f"{key} = {value}")

configure(host="db", port=5432, timeout=30)

# Unpacking a dict into keyword args:
opts = {"host": "db", "port": 5432}
configure(**opts)
```

`**options` collects "any extra keyword arguments" into a dict. Useful for forwarding arguments to inner calls.

## Putting it all together

```python
def f(pos1, pos2, /, normal, *, kw_only, **extras):
    ...
```

That declaration uses two rare features:

- `/` — **positional-only** marker. Everything before `/` *cannot* be passed by keyword.
- `*` — **keyword-only** marker. Everything after `*` *must* be passed by keyword.

The everyday version of this is the keyword-only form, which forces callers to be explicit:

```python
def open_file(path, *, mode="r", encoding="utf-8"):
    ...

open_file("data.csv")                          # OK
open_file("data.csv", mode="w")                # OK
open_file("data.csv", "w")                     # TypeError — "w" can't be positional
```

This is the right tool to prevent `open_file("data.csv", True, False)`-style calls where the booleans are mysterious.

## Argument-passing model

Python is "**pass by object reference**" (sometimes called "pass by assignment"):

- The function receives the **same object** the caller has.
- If the object is mutable and the function mutates it, the caller sees the change.
- If the function rebinds the parameter (`x = new_value`), the caller sees nothing.

```python
def reset_inplace(xs):
    xs.clear()             # mutates — caller sees this

def reset_rebind(xs):
    xs = []                # only rebinds the local name — caller unaffected
```

Internalize this once and a lot of "wait, why didn't my function change anything?" confusion disappears.

## Pitfalls

- **Mutable defaults.** Once more, just in case: don't.
- **`**kwargs` everywhere is a code smell.** It hides what the function actually accepts. Use it only at the boundaries (decorators, generic forwarders).
- **Too many parameters.** Past ~5, switch to passing a config object (`dataclass` or `dict`).
- **Boolean-flag parameters.** `do_thing(force=True)` is fine; `do_thing(True)` is illegible. Make boolean params keyword-only.

## Read deeper

- **LP** 6e, Ch. 17 (function arguments)
- **EP** 3e — items on keyword-only arguments, default-argument mutability, and unpacking
