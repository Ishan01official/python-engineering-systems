# Module 04 — Exercises

## E04.1 — Keyword-only arguments

Write `def send_email(to, *, subject, body, cc=None, bcc=None) -> None:` that prints what would be sent. Show that `send_email("a@b.com", "Hi", "Hello there")` raises a `TypeError` because subject and body must be passed by name.

## E04.2 — Fix the default

This function aggregates orders by user but has a bug:
```python
def add_order(user_id, order, orders={}):
    orders.setdefault(user_id, []).append(order)
    return orders

add_order(1, "apple")     # {1: ["apple"]}
add_order(2, "banana")    # {1: ["apple"], 2: ["banana"]}  — WHAT?!
```
Identify the bug. Rewrite the function so each call starts fresh unless the caller passes their own dict.

## E04.3 — Closure-based counter

Write `make_bounded_counter(start=0, step=1, maximum=None)` that returns a function which, when called, returns the next value but raises `StopIteration` once it reaches `maximum`.

## E04.4 — Dispatch table

You have order events with `type` fields: `"created"`, `"paid"`, `"shipped"`, `"refunded"`. Build a dispatch table (`dict[str, Callable]`) where each handler takes the event dict and prints a one-line summary. Wrap it in `def handle(event): ...`. Bonus: support an `"unknown_event"` fallback.

## E04.5 — Refactor a long signature

This function has 7 parameters. Refactor it to take a small config object (NamedTuple or dataclass) so calls are readable.
```python
def train_model(data_path, output_path, batch_size, lr, epochs, optimizer, seed, verbose):
    ...
```

## E04.6 — Predict the output

```python
funcs = []
for i in range(3):
    def make_fn():
        return i
    funcs.append(make_fn)

print([f() for f in funcs])
```
What does this print? Why? How would you fix it so it prints `[0, 1, 2]`?

## E04.7 — `functools.cache`

Write a recursive `path_count(m, n)` that returns the number of ways to go from `(0,0)` to `(m-1, n-1)` on a grid, moving only right or down. Decorate with `@cache` so it runs fast. Compute `path_count(20, 20)`.
