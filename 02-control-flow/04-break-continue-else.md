# 04 — `break`, `continue`, and loop-`else`

## `break`

Stops the loop immediately:

```python
for x in xs:
    if x < 0:
        break
    print(x)
```

## `continue`

Skips to the next iteration:

```python
for x in xs:
    if x < 0:
        continue           # skip negatives
    print(x)
```

## The unusual one: `else` on a loop

Python lets you attach `else` to a `for` or `while`. The `else` block runs **only if the loop completed without a `break`**.

```python
for item in haystack:
    if item == needle:
        print("found!")
        break
else:
    print("not found")
```

Read it as "for ... but if we never broke out, do this". Useful for search patterns.

It's an oddity that most Python beginners never learn — but you'll see it in real code, and it's the cleanest way to express "did we find it?" without an extra flag variable.

## Pitfalls

- **`continue` in deeply nested loops** can make logic hard to follow. If you have more than one level of nesting, refactor into a helper function and use `return`.
- **`break` only exits the innermost loop.** If you need to bail out of multiple levels, use a function and `return`, or raise + catch a sentinel exception.

## Patterns

### Find-first

```python
def find(haystack, needle):
    for i, item in enumerate(haystack):
        if item == needle:
            return i
    return -1
```

A `return` from inside a loop is often clearer than a `break` + flag.

### Skip then process

```python
for line in file:
    line = line.strip()
    if not line or line.startswith("#"):
        continue                   # skip blanks and comments
    process(line)
```

This is the standard "skip the noise, work on the signal" pattern. You'll write it constantly.
