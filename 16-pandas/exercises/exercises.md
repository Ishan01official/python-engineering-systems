# Module 16 — Exercises

## E16.1 — Load, inspect, summarize

Find a CSV (download any open dataset, or use one from `seaborn.load_dataset("titanic")`). Load it. Print `.info()`, `.describe()`, and the count of nulls per column. Identify the 2 columns that need the most cleaning.

## E16.2 — Indexing fluency

For a DataFrame `df` with columns `name, age, city, salary`, write the expressions for:
1. Just the `salary` column as a Series.
2. The first 5 rows of `name` and `age`.
3. Rows where `age >= 25` AND `city == "Delhi"`.
4. Rows where city is in `["Delhi", "Mumbai", "Bangalore"]`.
5. Set salary to 0 for everyone under 18.

## E16.3 — Group-by drill

Using `seaborn.load_dataset("titanic")`:
1. Survival rate by sex.
2. Survival rate by pclass and sex (use `groupby` with two keys).
3. The same as a pivot table (`index=sex, columns=pclass`).
4. Median fare per pclass.

## E16.4 — Time series

Generate a year of synthetic hourly data with `pd.date_range`. Resample to daily averages. Plot the 7-day rolling mean using `.plot()` (matplotlib). Save as `rolling_mean.png`.

## E16.5 — Promote a long-form table to wide

Given long-form data `[(date, metric, value)]`, use `pivot_table` to get one column per metric, one row per date. Then go back to long form with `melt`.

## E16.6 — Join two tables

You have `users(id, name, country)` and `orders(user_id, amount)`. Merge them so each order row has the user's name and country attached. Then group by country and sum order amounts.
