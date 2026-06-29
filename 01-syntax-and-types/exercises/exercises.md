# Module 01 — Exercises

## E01.1 — Format a price report

Given:
```python
items = [("Apple", 1.5, 3), ("Bread", 3.25, 1), ("Milk", 2.4, 2)]   # (name, unit_price, qty)
```

Print, using f-strings:
```
Apple   x 3 @ $1.50  =  $4.50
Bread   x 1 @ $3.25  =  $3.25
Milk    x 2 @ $2.40  =  $4.80
-------------------------
TOTAL:           $12.55
```

Constraints: right-align prices in width 6. Use `Decimal` for totals.

## E01.2 — Spot the mutation bug

The function below is supposed to return a *new* list with each element doubled, leaving the input alone. It doesn't. Fix it without changing the signature.

```python
def double_all(xs):
    for i in range(len(xs)):
        xs[i] = xs[i] * 2
    return xs
```

## E01.3 — Truthiness vs `is None`

You're parsing user input and want to fill in a default *only* when the user didn't provide anything. They might legitimately type `0`, `""`, or `False`. Write a function `apply_default(value, default)` that returns `default` only if `value is None`, otherwise returns `value`. Write three test cases that would break a naive `if not value:` implementation.

## E01.4 — Float comparison

Without using `math.isclose`, write `def isclose(a, b, tol=1e-9): ...` that returns True iff `a` and `b` are within tolerance. Test with `0.1 + 0.2` and `0.3`.

## E01.5 — String slicing puzzle

```python
s = "Python Engineering"
```

Using slicing only (no method calls), produce:
1. `"nohtyP"`
2. `"Pto nier"`  (every other char from `s`)
3. `"gnireenignE"`  (reverse of `"Engineering"`)

## E01.6 — Spot the trap

What does this print? Why?
```python
def collect(item, bag=[]):
    bag.append(item)
    return bag

print(collect("x"))
print(collect("y"))
print(collect("z", bag=[]))
print(collect("w"))
```
