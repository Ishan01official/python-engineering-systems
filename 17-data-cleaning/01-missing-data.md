# 01 — Missing data

In pandas, missing values are `NaN` (numeric columns) or `pd.NA`/`None` (object columns). Real datasets have them. Handling them is half of cleaning.

## Spotting

```python
df.isna()                    # boolean DataFrame: True where missing
df.isna().sum()              # count of NaNs per column — call this first on any new dataset
df.isna().mean()             # fraction missing per column

df["age"].notna()            # the inverse
```

## Removing

```python
df.dropna()                  # drop rows with ANY NaN — usually too aggressive
df.dropna(how="all")          # drop rows where EVERY column is NaN
df.dropna(subset=["email"])   # drop rows where email is NaN
df.dropna(axis=1)             # drop COLUMNS containing NaN
df.dropna(thresh=3)           # drop rows with fewer than 3 non-null values
```

Be deliberate. `df.dropna()` on a wide table can throw away 80% of your rows because *every* row has at least one NaN somewhere.

## Filling

```python
df["age"].fillna(0)                        # constant
df["age"].fillna(df["age"].mean())          # column mean
df["age"].fillna(df["age"].median())        # often better — robust to outliers
df["city"].fillna("unknown")                # categorical default

df.ffill()                                  # forward-fill: use previous row's value
df.bfill()                                  # backward-fill: use next row's value
```

Forward-fill is common in time series (a stock price that didn't change). For one-off categorical missingness, "unknown" as an explicit category is usually better than guessing.

## Per-column strategies

Rarely does one strategy fit all columns:

```python
df = df.assign(
    age   = df["age"].fillna(df["age"].median()),
    city  = df["city"].fillna("unknown"),
    score = df["score"].fillna(0),
)
```

## Replace with rules

```python
df.replace({"N/A": np.nan, "missing": np.nan, "-": np.nan})
```

Datasets often encode missing as a string sentinel rather than a true NaN. `replace` cleans these up before downstream operations.

## Categorical missingness as signal

Sometimes "missing" is itself information. A customer with no `last_login` might be a never-active user. Don't blindly impute — adding a boolean `is_missing_X` column can preserve that signal.

## Pitfalls

- **Implicit dtype changes.** Filling an integer column with `np.nan` promotes it to float. If you want true integer NaNs, use the `Int64` extension dtype: `df["age"] = df["age"].astype("Int64")`.
- **Dropping silently.** Always print `before / after` row counts. Losing 30% of your data should be a deliberate choice.
- **Using `==` with NaN.** `NaN == NaN` is `False`. Use `.isna()`.

## Read deeper

- **PfDA** 3e, Ch. 7 — handling missing data
