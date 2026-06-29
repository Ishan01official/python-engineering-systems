# 01 — `Series` and `DataFrame`

Two core types:

- **`Series`** — a 1D labeled array. Like a NumPy array, but with an *index* (labels for each element). Mental model: a single column.
- **`DataFrame`** — a 2D labeled table. Each column is a `Series`. Mental model: a spreadsheet or SQL table in memory.

## Series

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s)
# a    10
# b    20
# c    30
# dtype: int64

s["a"]          # 10
s.values        # array([10, 20, 30])
s.index         # Index(['a', 'b', 'c'])
s + 1           # vectorized, like NumPy
s.sum(); s.mean(); s.max()
```

If you don't pass an index, you get the default `RangeIndex` (0, 1, 2, ...).

## DataFrame

```python
df = pd.DataFrame({
    "name":  ["Alice", "Bob", "Carol"],
    "age":   [30, 25, 28],
    "city":  ["Delhi", "Mumbai", "Delhi"],
})
print(df)
#     name  age    city
# 0  Alice   30   Delhi
# 1    Bob   25  Mumbai
# 2  Carol   28   Delhi
```

Each column is a Series. Access them by name:

```python
df["age"]                # Series
df[["name", "age"]]      # DataFrame with just those columns
df["age"].mean()         # 27.66...
```

`df.age` (attribute-style) also works, but breaks for column names with spaces, hyphens, or that match a method. Stick to `df["age"]`.

## Inspecting a DataFrame

```python
df.shape           # (3, 3)
df.dtypes          # dtype of each column
df.info()          # summary: types, non-null counts, memory
df.describe()      # numeric summary stats per column
df.head(5)         # first 5 rows
df.tail(5)         # last 5 rows
df.sample(3)       # 3 random rows
df.columns         # Index of column names
df.index           # the row index
```

`df.info()` and `df.head()` are the first two things you call on any new dataset.

## Reading and writing

```python
df = pd.read_csv("users.csv")                    # most common
df = pd.read_csv("users.csv", dtype={"id": int})  # force a column's type
df = pd.read_parquet("users.parquet")             # faster + smaller than CSV
df = pd.read_json("data.json")
df = pd.read_excel("sheet.xlsx")                  # needs `openpyxl`

df.to_csv("out.csv", index=False)
df.to_parquet("out.parquet")
df.to_json("out.json", orient="records")
```

`index=False` on `to_csv` is almost always what you want — otherwise you save the default 0/1/2 index as a column.

## Adding and modifying columns

```python
df["age_squared"] = df["age"] ** 2          # broadcast-style assignment
df["upper_name"] = df["name"].str.upper()   # vectorized string method
df["adult"] = df["age"] >= 18                # boolean column
```

Most operations are vectorized — applied to the whole column without an explicit Python loop.

## Missing data

`NaN` (`float`) represents missing. Three idioms:

```python
df.isna()              # boolean mask of where NaNs are
df.dropna()            # drop rows with any NaN (or use subset=)
df.fillna(0)           # replace NaNs
df["age"].fillna(df["age"].mean())   # replace with column mean
```

Missing data handling is most of "data cleaning" in practice. Module 17 covers it.

## Read deeper

- **PfDA** 3e, Ch. 5 — Series and DataFrame basics
