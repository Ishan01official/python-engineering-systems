# 04 — Booleans, `None`, and truthiness

## `True`, `False`

Two values. Both are singletons (only one `True` object exists in your program; same for `False`). They are technically `int`s under the hood: `True == 1`, `False == 0`. You can do `sum([True, False, True])` and get `2` — useful trick.

## `None`

The unique "absence of value" singleton. Used for:

- Optional return values: `dict.get("missing_key")` returns `None`.
- Default function arguments that mean "not provided".
- Initial value before something has been set.

```python
result = some_function()
if result is None:        # ← always use `is None`, not `== None`
    print("nothing came back")
```

**Why `is None` and not `== None`?** Because `is` checks identity (same object) and there is only ever one `None`. Some user-defined classes can override `__eq__` and return weird things — `is None` is bullet-proof.

## Truthiness

Every Python object can be tested in a boolean context. The rules:

**Falsy** (treated as False):
- `False`, `None`
- `0`, `0.0`, `0j`
- Empty containers: `""`, `[]`, `()`, `{}`, `set()`
- `range(0)` and other empty iterables

**Truthy:** everything else, including non-zero numbers, non-empty strings/lists/etc, and any custom object that doesn't say otherwise.

```python
if my_list:                  # idiomatic — true if non-empty
    print("has items")

if name:                     # true if non-empty string
    print(f"got {name}")
```

This is more Pythonic than `if len(my_list) > 0:` or `if name != "":`.

## Pitfalls

- **`0` and `False` are interchangeable in many contexts.** `True + True == 2`. Avoid relying on this — it confuses readers.
- **`bool("False") == True`**. Because `"False"` is a non-empty string, which is truthy. If you're parsing config files, parse the strings explicitly.
- **Don't use truthiness when you actually need "is this None vs is this falsy".** A user score of `0` is falsy but isn't "missing". Use `if value is None:` when "missing" is what you actually mean.

```python
def greet(name=None):
    # WRONG: empty string would be treated as "no name"
    if not name:
        name = "stranger"

    # BETTER: explicitly check for None
    if name is None:
        name = "stranger"
    return f"Hi {name}"
```

## Boolean operators: `and`, `or`, `not`

```python
True and False    # False
True or False     # True
not True          # False
```

These short-circuit. `a and b` evaluates `a`; if `a` is falsy, returns `a` immediately and doesn't evaluate `b`. Useful pattern:

```python
name = input_name or "default"   # if input_name is falsy, use "default"
```

But beware: this uses truthiness, so an empty string would also fall through to `"default"`. Sometimes you want that; sometimes you don't.

## Chained comparisons

```python
0 < x < 100         # equivalent to  0 < x  AND  x < 100
a == b == c         # equivalent to  a == b  AND  b == c
```

Python is one of the few languages that gets this right. Use it.

## Read deeper

- **LP** 6e, Ch. 12 — conditional logic, truth tests.
