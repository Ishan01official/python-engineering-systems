# 03 — `groupby` — split, apply, combine

The single most powerful pandas operation. If you've used SQL `GROUP BY`, you'll feel at home.

## The mental model

`groupby` does three things:

1. **Split** the rows into groups by one or more keys.
2. **Apply** a function to each group (aggregate, transform, or filter).
3. **Combine** the results back into a Series or DataFrame.

```python
sales = pd.DataFrame({
    "user":   ["A", "A", "B", "B", "C"],
    "product":["X", "Y", "X", "X", "Y"],
    "amount": [10, 20, 15, 25, 30],
})

sales.groupby("user")["amount"].sum()
# user
# A    30
# B    40
# C    30
```

That replaces a `defaultdict(int)` + loop you'd write in plain Python — and runs much faster.

## Aggregating

```python
g = sales.groupby("user")

g["amount"].sum()           # one stat per group
g["amount"].mean()
g["amount"].count()
g.size()                     # rows per group (includes NaNs unlike count())

# Multiple stats at once
g["amount"].agg(["sum", "mean", "count"])

# Different stats per column
g.agg({"amount": ["sum", "mean"], "product": "nunique"})
```

## Multiple grouping keys

```python
sales.groupby(["user", "product"])["amount"].sum()
# user  product
# A     X          10
#       Y          20
# B     X          40
# C     Y          30
```

The result has a hierarchical index — you can flatten it with `.reset_index()`.

## Pivot — wide form

Often you want columns instead of nested groups:

```python
sales.pivot_table(index="user", columns="product", values="amount", aggfunc="sum", fill_value=0)
# product   X   Y
# user
# A        10  20
# B        40   0
# C         0  30
```

`pivot_table` is `groupby` + `unstack` in one. Use it when you want a 2D crosstab.

## Transform — same shape out

`agg` collapses; `transform` keeps the original number of rows:

```python
# Add a "user's total" column to every row
sales["user_total"] = sales.groupby("user")["amount"].transform("sum")
```

Each row gets its group's value. Useful for "what fraction of my user's spend was this purchase?" types of questions.

## Filter — keep or drop whole groups

```python
# Keep only users whose total > 30
big = sales.groupby("user").filter(lambda g: g["amount"].sum() > 30)
```

## `apply` — escape hatch

When `agg` / `transform` aren't enough, `apply` runs an arbitrary function per group:

```python
# Top item per user by amount
def top_row(g):
    return g.loc[g["amount"].idxmax()]

sales.groupby("user").apply(top_row, include_groups=False)
```

`apply` is the slow option — it has Python-level overhead per group. Prefer `agg` / `transform` when possible.

## Pitfalls

- **`groupby` is lazy** — it returns a `DataFrameGroupBy` object. Nothing happens until you call an aggregation.
- **NaNs in the group key** are dropped by default. Pass `dropna=False` to keep them.
- **`apply` is slow** — don't use it when a vectorized operation works.

## Read deeper

- **PfDA** 3e, Ch. 10 — the canonical reference for groupby in pandas
