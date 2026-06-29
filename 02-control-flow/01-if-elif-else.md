# 01 — `if`, `elif`, `else`, and `match`

## The basic shape

```python
if condition:
    ...
elif other_condition:
    ...
else:
    ...
```

Python uses **indentation** instead of braces. Standard is 4 spaces. Mixing tabs and spaces is a syntax error in Python 3 — let your editor handle it.

## Idiomatic patterns

### Use truthiness for non-empty checks

```python
# Pythonic
if items:
    process(items)

# Not Pythonic
if len(items) > 0:
    process(items)
```

### Compare to `None` with `is`

```python
if result is None:
    handle_missing()
```

### Chained comparisons

```python
if 0 <= age < 18:
    print("minor")
elif 18 <= age < 65:
    print("adult")
else:
    print("senior")
```

### Ternary expressions

```python
status = "pass" if score >= 60 else "fail"
```

Don't nest ternaries deeply — if you find yourself doing `a if x else b if y else c`, refactor into an `if/elif/else` chain.

## `match` — structural pattern matching (3.10+)

```python
def describe(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at ({x}, {y})"
        case {"type": "scroll", "delta": d}:
            return f"scroll by {d}"
        case {"type": t}:
            return f"unknown event type: {t}"
        case _:
            return "not an event"
```

`match` shines for branching on the *shape* of data — dictionaries, tuples, classes. It's not a replacement for simple `if/elif`. Use it when you'd otherwise write a long chain of `isinstance` or dict key checks.

## Pitfalls

- **Don't write `if x == True:`**. Just `if x:`. (And never `if x == None:`; use `is None`.)
- **The colon is mandatory.** `if x:` — forgetting it is the #1 syntax error from C-family programmers.
- **Indentation is structural.** A 1-space indent inside a 4-space block is a hard error.

## Read deeper

- **LP** 6e, Ch. 12 — conditionals.
- **EP** 3e — items on assignment expressions, pattern matching.
