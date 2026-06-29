# Module 17 — Exercises

## E17.1 — Missing data triage

For each column type below, choose a strategy. Justify in one line each.
1. `age` (integer, 5% missing).
2. `signup_date` (datetime, 0.1% missing).
3. `country` (string, 20% missing).
4. `last_login` (datetime, 60% missing).
5. `phone_number` (string, 80% missing).

## E17.2 — Coerce a string column to numeric

```python
df["price"] = ["$10.50", "$20.00", "missing", "$5.25", "—"]
```
Convert to a float column with NaN where parsing fails. Use `pd.to_numeric(..., errors="coerce")` and a `str.replace` for the `$`.

## E17.3 — Wide to long

You have monthly sales as wide:
```
product,jan,feb,mar,apr
A,100,120,90,110
B,80,110,95,105
```
Reshape to long form with columns `product`, `month`, `sales`. Bonus: convert `month` to a proper date (1st of each month).

## E17.4 — Spot the join bug

Two DataFrames each have an `id` column, but in one it's `int` and in the other it's `str`. The merge runs without error and returns 0 rows. Why? Show the fix.

## E17.5 — Many-to-one validate

You merge `orders` (one row per order) with `users` (one row per user) on `user_id`. The output has *more* rows than `orders`. What went wrong with the `users` table? Show how `validate="m:1"` would have caught it earlier.

## E17.6 — Clean-then-aggregate pipeline

Take a CSV with at least 1000 rows (any open dataset). Write a script that:
1. Loads it.
2. Reports nulls per column.
3. Cleans one column with a deliberate strategy.
4. Drops rows that fail basic validation.
5. Computes a per-group summary.
6. Saves the cleaned data as Parquet and the summary as CSV.
