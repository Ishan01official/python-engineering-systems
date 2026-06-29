# Module 09 — Exercises

## E09.1 — Hand-write an iterator class

Write `class FibIterator` that yields the first `n` Fibonacci numbers. Implement `__iter__` and `__next__` explicitly (no `yield`). Then rewrite it as a one-line generator function. Compare.

## E09.2 — Lazy CSV stream

Write `read_records(path)` that yields one dict per row from a CSV file. Then write `large_orders(records, min_total)` that filters them. Compose them so a multi-GB file works on a laptop.

## E09.3 — Replace nested loops with `itertools.product`

```python
for x in [1, 2, 3]:
    for y in ['a', 'b']:
        for z in [True, False]:
            print(x, y, z)
```
Rewrite with one `for` loop using `itertools.product`.

## E09.4 — Sliding window without `pairwise`

Write `def windows(seq, n)` that yields all length-`n` contiguous windows of `seq`. `windows([1,2,3,4,5], 3)` → `(1,2,3), (2,3,4), (3,4,5)`. Use only `itertools.islice` and `itertools.tee`. (Hint: look up `tee`.)

## E09.5 — One-line group-and-sum

You have `transactions = [("alice", 100), ("bob", 50), ("alice", 75), ("carol", 200), ("bob", 25)]`. Produce a dict `{user: total}` two ways: (a) using `defaultdict`, (b) using `sorted` + `itertools.groupby`. Which is more readable here?

## E09.6 — Spot the bug

```python
def primes_up_to(n):
    for x in range(2, n):
        for d in range(2, x):
            if x % d == 0:
                break
        else:
            yield x

primes = primes_up_to(30)
print(sum(primes))
print(list(primes))
```
What does the second print show? Why? How would you fix this code so the caller could iterate twice?
