# 01 — Pythonic thinking

A handful of idioms that distinguish "Python written by a Python programmer" from "Python written by a Java programmer".

## Use f-strings for formatting

```python
# Idiomatic
print(f"User {user.name} (age {user.age})")

# Old, but still seen
print("User %s (age %d)" % (user.name, user.age))
print("User {} (age {})".format(user.name, user.age))
```

## Unpack instead of indexing

```python
# bad
first = pair[0]
second = pair[1]

# good
first, second = pair
```

For multiple return values, the unpacking call site reads better than `result = stats(...)` followed by `result[0]`, `result[1]`.

## Prefer enumerate over `range(len(...))`

```python
# bad
for i in range(len(items)):
    print(i, items[i])

# good
for i, item in enumerate(items):
    print(i, item)
```

## Use `zip` for parallel iteration

```python
for name, score in zip(names, scores, strict=True):
    ...
```

`strict=True` raises if the lengths differ — usually what you want.

## Comprehensions for transforms; loops for side effects

```python
# good — transform
doubled = [x * 2 for x in xs]

# bad — comprehension just for side effects
[print(x) for x in xs]      # don't

# good
for x in xs:
    print(x)
```

## Use the EAFP idiom

"Easier to Ask Forgiveness than Permission" — try the thing, handle failure.

```python
# Pythonic
try:
    value = d[key]
except KeyError:
    value = default

# Better here: a built-in does this
value = d.get(key, default)
```

vs the "Look Before You Leap" style of pre-checking everything.

## Iterate by content, not index

```python
# bad
i = 0
while i < len(xs):
    print(xs[i])
    i += 1

# good
for x in xs:
    print(x)
```

## Use the walrus operator for shared values

When you need a value both for a condition and for the body:

```python
if (n := len(data)) > 10:
    print(f"too long ({n})")

while (chunk := f.read(8192)):
    process(chunk)
```

Pre-walrus, you'd compute the value twice or write a slightly awkward loop. Don't overuse — `if (a := f(b := g())) :` is illegible.

## Avoid mutable default arguments

```python
# bad
def add(item, items=[]): ...

# good
def add(item, items=None):
    if items is None:
        items = []
    ...
```

(EP has at least three items about this single issue, because it bites hard.)

## Read deeper

- **EP** 3e — Items in "Pythonic Thinking" chapter, especially the first 15.
