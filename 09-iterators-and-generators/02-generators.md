# 02 — Generators

A **generator function** is the easy way to create an iterator. Use `yield` anywhere in a function body, and Python turns it into a generator.

## The basic shape

```python
def count_up(start: int, stop: int):
    n = start
    while n < stop:
        yield n
        n += 1

for x in count_up(3, 7):
    print(x)      # 3, 4, 5, 6
```

What's happening:

1. Calling `count_up(3, 7)` does *not* run the body. It returns a **generator object**.
2. Each `next()` call resumes the body, runs until the next `yield`, returns that value, and pauses.
3. When the function returns (falls off the end or hits a `return`), `StopIteration` is raised.

You don't have to track state in a class — Python freezes the function's stack frame between yields.

## Why generators are huge for data work

```python
# This reads the whole file into memory
lines = open("huge.log").readlines()

# This streams — one line at a time
def lines_of(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

for line in lines_of("huge.log"):
    process(line)
```

Memory stays constant regardless of file size. Same idea applies to API pagination, queue processing, any "potentially huge stream" problem.

## Pipelines

Generators compose. You can stack them into a processing pipeline:

```python
def numbers(stop):
    for i in range(stop):
        yield i

def evens(stream):
    for n in stream:
        if n % 2 == 0:
            yield n

def squared(stream):
    for n in stream:
        yield n * n

# Pipeline — no intermediate lists, lazy from end to end
for n in squared(evens(numbers(10))):
    print(n)
# 0, 4, 16, 36, 64
```

Each stage processes one item at a time. The whole pipeline uses O(1) memory.

## Generator expressions

Same syntax as list comprehensions but with `()` instead of `[]`:

```python
squares = (n * n for n in range(1_000_000))
total = sum(squares)               # O(1) memory
```

A list comprehension `[n * n for n in range(1_000_000)]` would allocate a million-int list. The generator expression keeps one value live at a time.

**Rule of thumb:** when you only need to iterate once (e.g., feed into `sum`, `max`, `any`, `all`, `for`), prefer a generator expression over a list comprehension.

```python
# wasteful — materializes a list just to sum
sum([x * x for x in xs])

# better — generator goes straight into sum
sum(x * x for x in xs)
```

(When passing a single generator expression as a function's only argument, you can drop the outer parens.)

## `yield from`

Delegates iteration to another iterable:

```python
def chain(*iterables):
    for it in iterables:
        yield from it       # yields each value from `it`

list(chain([1, 2], [3, 4], [5]))     # [1, 2, 3, 4, 5]
```

Without `yield from`, you'd write `for x in it: yield x`. `yield from` is shorter and faster.

## Sending values into a generator

You can also push data into a generator with `gen.send(value)`, and `yield` becomes an expression that evaluates to the sent value. This was the basis of "classic coroutines" before `async`/`await`. You almost never need this; mention it so you recognize it in old code.

## Pitfalls

- **A generator is exhausted after one full iteration.** Don't try to loop over the same one twice.
- **Side effects don't run until you iterate.** A generator that should validate its inputs needs the validation *outside* the generator function, or callers won't see errors until they start consuming.
- **`return value` inside a generator** does NOT make `value` the result of the loop — it just raises `StopIteration(value)`. The returned value is only seen by code that catches that exception (mostly `yield from`).

## Read deeper

- **FP** 2e, Ch. 17 — generators in depth, including coroutines.
- **EP** 3e — items on generators, `yield from`, and iterator memory efficiency.
