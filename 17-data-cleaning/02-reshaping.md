# 02 — Reshaping: long vs wide

Most data analysis tools (and most pandas operations) prefer **long form** — one row per observation, one column per variable. Data often arrives in **wide form** — many columns of related measurements. Knowing how to switch is essential.

## Wide vs long

Wide (often how a spreadsheet looks):

```
user     jan   feb   mar
Alice    100   120   90
Bob       80   110   95
```

Long (the same data, one row per observation):

```
user    month  amount
Alice   jan    100
Alice   feb    120
Alice   mar    90
Bob     jan    80
Bob     feb    110
Bob     mar    95
```

Long form is what `groupby`, `pivot_table`, plotting libraries, and ML tools all expect. **Default to long; pivot to wide only at the display step.**

## Wide → long: `melt`

```python
long = wide.melt(
    id_vars=["user"],                   # keep these columns as-is
    value_vars=["jan", "feb", "mar"],   # columns to unpivot
    var_name="month",                   # name for the new "variable" column
    value_name="amount",                # name for the new "value" column
)
```

If you omit `value_vars`, all non-id columns are melted.

## Long → wide: `pivot_table`

```python
wide = long.pivot_table(
    index="user",
    columns="month",
    values="amount",
    aggfunc="sum",          # how to combine if there are duplicates
    fill_value=0,
)
```

`pivot_table` (with `aggfunc`) handles duplicate `(user, month)` pairs by aggregating. `pivot` (without it) raises if duplicates exist — useful as a sanity check.

## `stack` / `unstack` — index-level pivoting

These work on the row/column index itself, useful after a multi-key groupby:

```python
g = df.groupby(["user", "month"])["amount"].sum()    # Series with MultiIndex
wide = g.unstack("month")                              # one column per month
back_to_long = wide.stack()                           # back to MultiIndex Series
```

## Choosing the right operation

| You have | You want | Use |
|---|---|---|
| Wide table | Long table | `melt` |
| Long table | Wide table (no duplicates) | `pivot` |
| Long table | Wide table (with aggregation) | `pivot_table` |
| MultiIndex Series | Wide DataFrame | `unstack` |
| Wide DataFrame | MultiIndex Series | `stack` |

## Splitting and combining columns

```python
# Split a single 'name' column into 'first' and 'last'
df[["first", "last"]] = df["name"].str.split(" ", n=1, expand=True)

# Combine columns into a label
df["full"] = df["first"] + " " + df["last"]
```

## Read deeper

- **PfDA** 3e, Ch. 8 — data wrangling
