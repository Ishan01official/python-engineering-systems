# 01 — Variables and binding

## What `x = 5` means

Three things happen, in order:

1. Python evaluates the right-hand side. `5` is a literal; it produces an `int` object (or reuses an existing cached one — Python caches small ints).
2. Python looks up (or creates) the name `x` in the current namespace.
3. Python binds the name `x` to the object.

The name is a label. The object lives separately. (Module 00 said this; I'm saying it again because it matters.)

## Valid names

```
my_var        ✓
_private      ✓
camelCase     ✓ (works, but Python convention is snake_case)
2things       ✗ (can't start with a digit)
my-var        ✗ (hyphen is the minus operator)
class         ✗ (reserved keyword)
```

The full list of reserved words: `False, None, True, and, as, assert, async, await, break, class, continue, def, del, elif, else, except, finally, for, from, global, if, import, in, is, lambda, nonlocal, not, or, pass, raise, return, try, while, with, yield`.

## Multiple assignment

```python
a, b, c = 1, 2, 3       # tuple unpacking
x = y = z = 0            # all three names bound to the same object 0
first, *rest = [1, 2, 3, 4]   # first=1, rest=[2,3,4]
```

The starred form is great for splitting a sequence into "head and tail" without slicing.

## Augmented assignment

```python
x += 1     # x = x + 1, but for some types more efficient
xs += [1]  # for lists, equivalent to xs.extend([1]) — mutates in place
xs = xs + [1]  # creates a new list, rebinds xs
```

These two look the same but aren't — for mutable types, `+=` typically mutates the existing object. We'll revisit this in the mutability note.

## Walrus operator `:=`

Python 3.8+. Assigns *inside* an expression:

```python
if (n := len(data)) > 10:
    print(f"too big ({n} items)")
```

Useful when you'd otherwise compute the same thing twice. Don't overuse it.

## `del` removes a binding

```python
x = 5
del x
print(x)   # NameError
```

`del` doesn't destroy the object — it removes the *name*. If no other name points at the object, Python's garbage collector will eventually free it.

## Pitfalls

- **Don't use single-letter names** except for trivial counters/indices. Future-you reading the code in 6 months will thank you.
- **Don't shadow builtins.** Names like `list`, `dict`, `id`, `type`, `str`, `sum` are built-ins. Naming a variable `list = [1,2,3]` works *but* it makes `list` unusable for the rest of the scope. Same for `len`, `max`, `min`, `sum`, `id`, etc.
- **One assignment, one purpose.** A variable that means "user count" early and "average score" later is a reading hazard.

## Read deeper

- **LP** 6e, Ch. 6 — names, references, dynamic typing.
- **EP** 3e — items about unpacking, assignment expressions, and naming.
