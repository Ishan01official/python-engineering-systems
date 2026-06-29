# 03 — Scope and closures

## LEGB, revisited

Recap from Module 00.04. Python looks up names in this order:

```
Local  →  Enclosing  →  Global  →  Built-in
```

First match wins. Lookups happen at *use time*, not at *definition time* — this matters for closures.

## Assignment creates a local

This is the rule that catches people:

```python
counter = 0
def increment():
    counter = counter + 1    # UnboundLocalError!
```

The assignment `counter = ...` on the left makes Python decide that `counter` is local in this function. So when it tries to evaluate the right side, `counter` exists locally but hasn't been assigned yet — hence the error.

To assign to an outer name, use `nonlocal` (for enclosing) or `global` (for module level):

```python
counter = 0
def increment():
    global counter
    counter = counter + 1
```

Or, better, **return the new value** instead of mutating shared state:

```python
def incremented(counter):
    return counter + 1

counter = incremented(counter)
```

Avoiding `global` makes code testable and predictable.

## `nonlocal` for nested functions

```python
def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step

c = make_counter()
print(c())   # 1
print(c())   # 2
print(c())   # 3
```

Without `nonlocal`, the `n += 1` line would create a fresh local `n` and fail.

## Closures

A **closure** is a function that "remembers" the variables from its enclosing scope, even after that scope has finished executing.

The `make_counter` example above is a closure. The inner `step` keeps a reference to `n` from `make_counter`'s frame. Even after `make_counter` returns, that frame stays alive as long as `step` is alive — because `step` is still using `n`.

Closures are how decorators work (Module 10). They're also how callbacks "capture" data.

### The classic late-binding gotcha

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])    # [2, 2, 2]  — surprised?
```

All three lambdas share the same `i` — and by the time you call them, `i` is 2.

The fix is to bind `i` as a default argument, which is evaluated *at function creation*:

```python
funcs = [lambda i=i: i for i in range(3)]
print([f() for f in funcs])    # [0, 1, 2]
```

Ugly, but a real-world pattern.

## When to use modules-as-namespaces instead of nesting

Deeply nested functions are hard to test (you can only get at the outer one). Prefer:

- **A class** if you have related state and behavior.
- **A module** if you have related functions that share constants.

Keep `nonlocal` and `global` rare.

## Read deeper

- **FP** 2e, Ch. 9 — closures and decorators, the canonical explanation.
- **LP** 6e, Ch. 17 — scope rules in depth.
