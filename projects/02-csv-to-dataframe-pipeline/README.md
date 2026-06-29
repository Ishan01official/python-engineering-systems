# Project 2 — CSV to DataFrame pipeline

Take a messy CSV, validate and clean it, summarize per group, and write Parquet output. Consolidates modules 06 (I/O), 09 (generators), 12 (testing), 15 (NumPy), 16 (pandas), 17 (cleaning).

## Spec

Input: `data/raw_sales.csv` with columns:
```
date, region, product, units, unit_price
```

The CSV is messy: stray whitespace, mixed-case region names, missing values, occasional non-numeric `units`/`unit_price`.

Output:
- `data/clean_sales.parquet` — the cleaned per-row table.
- `data/summary_by_region.csv` — region totals.

## Cleaning rules

1. Strip whitespace and lowercase `region`.
2. Coerce `units` and `unit_price` to numeric; rows that fail become NaN.
3. Drop rows where any of `date, region, product` is missing.
4. Fill missing `units` with 0 and missing `unit_price` with the product's median.
5. Add a derived column `revenue = units * unit_price`.

## Files

```
02-csv-to-dataframe-pipeline/
├── README.md
├── pipeline.py        # the run function, importable + runnable
├── tests/
│   └── test_pipeline.py
└── data/              # input/output dir (created at runtime)
```

## Stretch goals

- Read input as a stream of chunks (`pd.read_csv(..., chunksize=10_000)`) so it works on multi-GB files.
- Add a CLI wrapper (`python pipeline.py --input X --output Y`).
- Emit a JSON `manifest` of the run: row counts in/out, NaN counts, timing.
- Repartition the output by date (one Parquet file per day).
