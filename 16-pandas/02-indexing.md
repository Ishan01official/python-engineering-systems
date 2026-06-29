# 02 — Indexing: `.loc`, `.iloc`, masks

pandas has three main ways to select rows/columns. Get clear on them once and stop guessing.

## `.loc` — by label

`df.loc[row_labels, column_labels]`. Both are *labels*, not positions.

```python
df.loc[0, "age"]                     # value at row label 0, column "age"
df.loc[[0, 2], "name"]               # rows 0 and 2, column "name"
df.loc[0:2, ["name", "age"]]         # rows 0,1,2 (LABEL-based slice, INCLUSIVE)
df.loc[:, "age"]                     # all rows, column "age"  → Series
df.loc[df["age"] > 25, :]            # boolean mask on rows
```

Crucially: **label-based slices include the endpoint**. `df.loc[0:2]` gives you rows labeled 0, 1, AND 2. This is different from Python slicing.

## `.iloc` — by position (integer index)

`df.iloc[row_positions, col_positions]`.

```python
df.iloc[0, 1]              # first row, second column
df.iloc[:3, :2]            # first 3 rows, first 2 columns (EXCLUSIVE end like Python)
df.iloc[-1, :]             # last row
df.iloc[[0, 2, 5], :]      # rows at positions 0, 2, 5
```

`.iloc` uses Python-style slicing — exclusive of the end.

## Boolean masks

```python
df[df["age"] >= 18]                          # adults
df[(df["age"] >= 18) & (df["city"] == "Delhi")]   # combine with & |, parens required
df[~df["city"].isna()]                       # not NaN
df[df["city"].isin(["Delhi", "Mumbai"])]     # value in set
```

Combine masks with `&` (and), `|` (or), `~` (not). The Python keywords `and`/`or`/`not` don't work — they call `__bool__`, which raises on Series.

## Picking columns

```python
df["age"]                  # Series
df[["age", "name"]]        # DataFrame (note the LIST inside)
df.drop(columns=["city"])  # returns a new DataFrame without those columns
```

## Setting values

```python
df.loc[df["age"] < 18, "category"] = "minor"
df["age"] = df["age"].fillna(0)
df.loc[0, "name"] = "Alicia"
```

Avoid the chained `df["age"][df["age"] > 0] = 100` form — it can write to a copy, not the original, and pandas may even warn ("SettingWithCopyWarning"). Use `.loc` with both row and column selection in one shot.

## Index management

```python
df.set_index("name", inplace=False)    # use 'name' as the row index
df.reset_index(drop=True)               # back to a default RangeIndex
df.sort_index()
df.sort_values(by="age", ascending=False)
```

A meaningful index (e.g. a timestamp or user ID) makes `.loc` lookups much more useful.

## Read deeper

- **PfDA** 3e, Ch. 5 — selecting/filtering
