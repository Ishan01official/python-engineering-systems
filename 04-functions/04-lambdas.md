# 04 — Lambdas

A `lambda` is an anonymous, single-expression function. It exists so you can write a tiny function inline without naming it.

```python
square = lambda x: x ** 2
square(5)            # 25
```

That `lambda x: x ** 2` is exactly equivalent to:

```python
def square(x):
    return x ** 2
```

## When lambdas are appropriate

**As keys and predicates passed to other functions:**

```python
sorted(people, key=lambda p: p.age)
max(items, key=lambda it: it.score)
filter(lambda x: x > 0, numbers)
```

Inline, throwaway, single-expression. That's the sweet spot.

## When lambdas are NOT appropriate

**Never assign a lambda to a name.** If it's worth naming, write `def`:

```python
# Bad — flake8/ruff will warn about this
square = lambda x: x ** 2

# Good — same behavior, better debugger output, can have a docstring
def square(x):
    return x ** 2
```

The named-`def` version shows `square` in tracebacks; the lambda version shows `<lambda>`.

**Don't write multi-line logic in a lambda.** It can't span multiple statements, and trying to squeeze logic into nested conditionals makes it unreadable:

```python
# Awful
process = lambda x: (x ** 2 if x > 0 else -x ** 2) + (1 if x else 0)

# Fine
def process(x):
    base = x ** 2 if x > 0 else -x ** 2
    bump = 1 if x else 0
    return base + bump
```

## `key=` parameter idioms

Sorting and selection functions take `key=`, which is the most common lambda use:

```python
items.sort(key=lambda it: it.price)                    # by price
items.sort(key=lambda it: (-it.score, it.name))        # score desc, name asc
max(words, key=len)                                    # longest word
sorted(d.items(), key=lambda kv: kv[1], reverse=True)  # dict sorted by value desc
```

`operator.itemgetter` and `operator.attrgetter` are even faster (and more readable) alternatives when you're just plucking a field:

```python
from operator import itemgetter, attrgetter

sorted(d.items(), key=itemgetter(1), reverse=True)
items.sort(key=attrgetter("price"))
```

## Lambdas in `map` and `filter`

```python
doubled = list(map(lambda x: x * 2, xs))
positives = list(filter(lambda x: x > 0, xs))
```

**A list comprehension is usually more Pythonic:**

```python
doubled = [x * 2 for x in xs]
positives = [x for x in xs if x > 0]
```

`map`/`filter` shine when you already have a named function:

```python
list(map(str.upper, words))             # cleaner than [w.upper() for w in words]? debatable
```

For one-off transformations, prefer comprehensions. For applying a named function, `map`/`filter` are fine.

## Read deeper

- **LP** 6e, Ch. 19 (advanced function topics — lambdas, comprehensions, generators)
- **FP** 2e, Ch. 7 — functions as objects
