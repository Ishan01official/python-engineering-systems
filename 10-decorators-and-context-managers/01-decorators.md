# 01 — Decorators

A decorator is a function that takes a function and returns a (usually wrapped) function.

```python
@my_decorator
def f(x):
    return x + 1
```

is exactly equivalent to:

```python
def f(x):
    return x + 1

f = my_decorator(f)
```

That's it. The `@` syntax is sugar for "pass the function below to this decorator and rebind the name".

## A simple decorator

```python
from functools import wraps

def log_calls(fn):
    @wraps(fn)                    # preserves fn's name, docstring, etc.
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}({args}, {kwargs})")
        result = fn(*args, **kwargs)
        print(f"  -> {result!r}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

add(2, 3)
# calling add((2, 3), {})
#   -> 5
```

The mechanics:

1. `log_calls(fn)` runs at definition time, with `fn` = the original `add`.
2. It returns `wrapper`. Now the name `add` points at `wrapper`.
3. When you call `add(2, 3)`, you're really calling `wrapper(2, 3)`, which calls the original `add` inside.

**Always use `@functools.wraps(fn)`** when writing a decorator. Without it, `wrapper.__name__` would be `'wrapper'`, breaking tracebacks, docs, and `help()`.

## Decorators with arguments

If you want `@retry(times=3)`, you need a decorator *factory* — a function that returns a decorator:

```python
from functools import wraps
import time

def retry(times: int = 3, delay: float = 1.0):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < times:
                        time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator


@retry(times=3, delay=0.5)
def flaky_call():
    ...
```

Three levels of nesting. Worth re-reading until it clicks.

## Built-in decorators you'll actually use

```python
from functools import cache, lru_cache, wraps, cached_property

@cache                         # memoize (no eviction)
def fib(n): ...

@lru_cache(maxsize=128)        # memoize with size limit
def expensive(x): ...

class Report:
    @property                  # access without parens — report.total
    def total(self): ...

    @cached_property           # property that's computed once and cached
    def average(self): ...

class Thing:
    @staticmethod
    def utility(): ...

    @classmethod
    def from_dict(cls, d): ...
```

`@dataclass` is also a decorator. So is `@pytest.fixture`, `@app.route` (Flask), `@app.get` (FastAPI). You see them everywhere.

## When to write your own

Good fits:

- **Logging, metrics, timing** — cross-cutting concerns you want to add without polluting every function.
- **Caching / memoization** — `@cache` already covers most cases.
- **Retries** — wrap a flaky call.
- **Authorization / permission checks** — `@requires_login`.
- **Registering handlers** — `@app.route("/users")` style.

Bad fits:

- **Anywhere a regular function call is just as clear.** Decorators add a layer of indirection. If `log_calls(my_fn)(1, 2)` is fine, you don't need `@log_calls`.

## A class as a decorator

Less common but useful when the decorator has state:

```python
class CountCalls:
    def __init__(self, fn):
        self.fn = fn
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.fn(*args, **kwargs)

@CountCalls
def hello():
    print("hi")

hello(); hello(); hello()
print(hello.count)    # 3
```

## Read deeper

- **FP** 2e, Ch. 9 — the definitive treatment.
- **EP** 3e — items on decorators, `functools.wraps`, and avoiding common pitfalls.
