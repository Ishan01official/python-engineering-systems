# 05 — Functions as first-class objects

"First-class" means functions can be:

1. Stored in variables
2. Passed as arguments
3. Returned from other functions
4. Stored in data structures

This is what makes decorators, callbacks, and functional patterns possible in Python.

## Storing a function in a variable

```python
def shout(s): return s.upper() + "!"

transform = shout
print(transform("hello"))    # "HELLO!"
```

`shout` and `transform` are now two names for the same function object.

## Passing a function as an argument

This is what `sorted(items, key=...)` does. You give it a function to call on each element:

```python
words = ["banana", "apple", "cherry"]
sorted(words, key=str.lower)         # str.lower is itself a function
sorted(words, key=lambda w: len(w))
```

## Returning a function

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor       # closes over `factor`
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(10))    # 20
print(triple(10))    # 30
```

`make_multiplier` is a **factory**. Each call produces a customized function. We'll lean on this pattern hard when we get to decorators (Module 10).

## Storing functions in a dict — dispatch

A clean alternative to long `if/elif` chains:

```python
def handle_create(req): ...
def handle_read(req): ...
def handle_update(req): ...
def handle_delete(req): ...

handlers = {
    "POST":   handle_create,
    "GET":    handle_read,
    "PUT":    handle_update,
    "DELETE": handle_delete,
}

def dispatch(req):
    handler = handlers.get(req.method, handle_unknown)
    return handler(req)
```

You can also use `match` (Python 3.10+) for shape-based dispatch. Dict dispatch is great when the key is a simple lookup.

## `functools` — the function toolbox

A few essentials:

### `functools.partial`

Pre-fill some arguments to create a new callable:

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
print(square(5))    # 25
print(cube(5))      # 125
```

Useful when an API wants a callback that takes specific arguments but you have a more general function.

### `functools.reduce`

Apply a binary function across an iterable to reduce it to one value:

```python
from functools import reduce
from operator import add, mul

reduce(add, [1, 2, 3, 4, 5])    # 15
reduce(mul, [1, 2, 3, 4, 5])    # 120
```

For sums and products, prefer the dedicated `sum()` / `math.prod()` — `reduce` is for less common reductions.

### `functools.cache` / `functools.lru_cache`

Memoize a function — cache results of past calls:

```python
from functools import cache

@cache
def fib(n):
    if n < 2: return n
    return fib(n - 1) + fib(n - 2)

print(fib(50))    # near-instant, even though recursion is exponential without cache
```

(That `@cache` is a *decorator* — Module 10 covers them in depth.)

## Pure functions are easiest

A **pure function** depends only on its arguments and returns a value with no side effects. It doesn't read globals, doesn't mutate inputs, doesn't print, doesn't write files.

Pure functions are:

- Trivially testable (same inputs → same output, always)
- Trivially parallelizable
- Trivially composable

Aim to make most of your functions pure. Keep the I/O and mutation at the edges of your program. This is the single best habit for writing maintainable Python.

## Read deeper

- **FP** 2e, Ch. 7 — functions as first-class objects, the foundational chapter.
- **EP** 3e — items on `functools`, dispatch, and avoiding hidden side effects.
