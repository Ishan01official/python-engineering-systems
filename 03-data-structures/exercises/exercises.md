# Module 03 — Exercises

## E03.1 — Word frequency

Given a string of text, return the 3 most frequent words (lowercased, ignoring punctuation). Use `Counter`. Bonus: ignore common stopwords (`the, a, an, of, to, and, in`).

## E03.2 — Group by

Given:
```python
people = [
    {"name": "Alice", "city": "Delhi"},
    {"name": "Bob",   "city": "Mumbai"},
    {"name": "Carol", "city": "Delhi"},
    {"name": "Dan",   "city": "Bangalore"},
]
```
Produce a dict `{city: [names...]}` using `defaultdict(list)`.

## E03.3 — Set algebra

Given two lists of user IDs (one for users who clicked an email, one for users who clicked a follow-up SMS), find:
1. Users who clicked **both**.
2. Users who clicked **only the email**.
3. Users who clicked **either** (no duplicates).

## E03.4 — Spot the bug

What's wrong with this code?
```python
grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```
Predict the output, then fix it.

## E03.5 — Promote to NamedTuple

This loop is hard to read because of the `[0]`/`[1]` indexing. Promote `point` to a `NamedTuple`:
```python
points = [(3, 4), (1, 5), (2, 9)]
for p in points:
    print(p[0] + p[1])
```

## E03.6 — Choose the right container

For each, name the best container and one alternative:
1. Tracking the unique URLs you've already crawled.
2. The pixels of an image (millions of integers).
3. The current routing table: hostname → IP address.
4. A history of the last 100 chat messages.
5. The fixed list of allowed HTTP methods.
