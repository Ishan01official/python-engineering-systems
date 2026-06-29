# 03 — Joins: `merge`, `concat`, `join`

Combining DataFrames. The pandas equivalent of SQL joins.

## `concat` — stack tables

```python
# Vertically (more rows)
pd.concat([df_jan, df_feb, df_mar], ignore_index=True)

# Horizontally (more columns, same index)
pd.concat([df_a, df_b], axis=1)
```

Use when the schemas are the same (vertical) or the rows align (horizontal). For "look up a value from another table", use `merge`.

## `merge` — SQL-style join

```python
merged = orders.merge(
    users,
    left_on="user_id",
    right_on="id",
    how="left",          # or "inner", "right", "outer"
)
```

The four `how` values mirror SQL:

- **inner** — only keys present in both tables (default).
- **left** — all rows from left; nulls for missing right matches.
- **right** — all rows from right.
- **outer** — all keys from either side.

If the join columns have the same name, use `on=`:

```python
df1.merge(df2, on="user_id", how="left")
```

## Validating joins

A merge that should be 1-to-1 but is secretly 1-to-many will silently inflate your row count. Always check:

```python
before = len(orders)
joined = orders.merge(users, on="user_id", how="left", validate="m:1")
print(f"{before} → {len(joined)}")
```

`validate=` checks the relationship type. Values: `1:1`, `1:m`, `m:1`, `m:m`. Raise if violated.

`indicator=True` adds a `_merge` column showing the source of each row — useful for debugging join misses:

```python
joined = orders.merge(users, on="user_id", how="left", indicator=True)
print(joined["_merge"].value_counts())
```

## Merging on the index

If one or both tables have the join key as their index:

```python
df1.merge(df2, left_index=True, right_index=True, how="left")
# or the convenience form
df1.join(df2, how="left")
```

`df.join` is `merge` with index defaults. Less flexible, more readable when you have a meaningful index.

## Multi-column keys

```python
sales.merge(quotas, on=["region", "quarter"])
```

The columns must exist in both, with matching dtypes. Mismatched dtypes (string `"1"` vs int `1`) silently produce empty joins — convert first.

## Pitfalls

- **Cardinality blow-up.** `merge` of two tables with duplicate keys produces the Cartesian product per key. Always `validate=`.
- **NaN in join keys.** NaN doesn't equal NaN, so rows with NaN keys never match. Decide explicitly: drop, fill, or treat as a category.
- **Performance.** A merge of two huge tables can be slow. Set the join column as the index first when joining on it repeatedly.

## Read deeper

- **PfDA** 3e, Ch. 8 — joins in pandas
