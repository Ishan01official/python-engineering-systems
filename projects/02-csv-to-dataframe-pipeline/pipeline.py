"""
CSV → cleaned DataFrame → Parquet + summary CSV.

Designed to be both importable (for tests) and runnable as a script.

Run:
    python pipeline.py             # uses data/raw_sales.csv by default
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class PipelineResult:
    rows_in: int
    rows_out: int
    dropped: int
    clean_path: Path
    summary_path: Path


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the cleaning rules from the README."""
    df = df.copy()

    # 1. Normalize strings — and treat empty strings as missing
    for col in ("region", "product"):
        df[col] = df[col].astype("string").str.strip()
        df.loc[df[col] == "", col] = pd.NA
    df["region"] = df["region"].str.lower()

    # 2. Coerce numerics — anything unparseable becomes NaN
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # 3. Drop rows missing critical fields
    required = df[["date", "region", "product"]].notna().all(axis=1)
    df = df.loc[required].copy()

    # 4. Fill remaining
    df["units"] = df["units"].fillna(0)
    df["unit_price"] = (
        df.groupby("product")["unit_price"]
        .transform(lambda s: s.fillna(s.median()))
    )
    # If a whole product had no prices, fall back to the global median
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median())

    # 5. Derived column
    df["revenue"] = df["units"] * df["unit_price"]

    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region", as_index=False)
        .agg(total_units=("units", "sum"),
             total_revenue=("revenue", "sum"),
             rows=("revenue", "count"))
        .sort_values("total_revenue", ascending=False)
    )


def run(input_csv: Path, output_dir: Path) -> PipelineResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(input_csv)
    rows_in = len(raw)

    clean_df = clean(raw)
    rows_out = len(clean_df)

    clean_path = output_dir / "clean_sales.parquet"
    summary_path = output_dir / "summary_by_region.csv"

    clean_df.to_parquet(clean_path, index=False)
    summarize(clean_df).to_csv(summary_path, index=False)

    return PipelineResult(
        rows_in=rows_in,
        rows_out=rows_out,
        dropped=rows_in - rows_out,
        clean_path=clean_path,
        summary_path=summary_path,
    )


def _make_sample(path: Path) -> None:
    """Generate a small messy sample so the script is runnable out of the box."""
    rows = [
        ("2026-06-01", " North ", "widget", "10", "5.0"),
        ("2026-06-01", "north",   "gizmo",  "3",  "12.0"),
        ("2026-06-02", "South",   "widget", "7",  ""),         # missing price
        ("2026-06-02", "SOUTH",   "gizmo",  "x",  "12.5"),      # bad units
        ("2026-06-03", "",        "widget", "5",  "5.0"),       # missing region
        ("2026-06-03", "east",    "widget", "9",  "4.8"),
        ("2026-06-04", "East",    "gizmo",  "2",  "13"),
        ("2026-06-04", "north",   "widget", "",   "5.0"),       # missing units
    ]
    df = pd.DataFrame(rows, columns=["date", "region", "product", "units", "unit_price"])
    df.to_csv(path, index=False)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    data = here / "data"
    raw = data / "raw_sales.csv"
    if not raw.exists():
        data.mkdir(exist_ok=True)
        _make_sample(raw)
        print(f"created sample input at {raw}")

    result = run(raw, data)
    print(f"rows_in={result.rows_in}, rows_out={result.rows_out}, dropped={result.dropped}")
    print(f"clean:   {result.clean_path}")
    print(f"summary: {result.summary_path}")
    print()
    print(pd.read_csv(result.summary_path))
