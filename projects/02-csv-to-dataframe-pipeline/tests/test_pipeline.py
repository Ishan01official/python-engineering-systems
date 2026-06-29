"""Tests for the CSV → DataFrame pipeline."""
from pathlib import Path

import pandas as pd
import pytest

from pipeline import clean, summarize, run, _make_sample


@pytest.fixture
def raw_df() -> pd.DataFrame:
    return pd.DataFrame({
        "date":       ["2026-06-01", "2026-06-01", "2026-06-02", "not a date"],
        "region":     [" North ", "north", "", "South"],
        "product":    ["widget", "gizmo", "widget", "widget"],
        "units":      ["10", "3", "5", "7"],
        "unit_price": ["5.0", "12.0", "", "5.0"],
    })


def test_clean_strips_and_lowercases_region(raw_df):
    out = clean(raw_df)
    assert set(out["region"].unique()) <= {"north", "south"}


def test_clean_drops_rows_missing_required(raw_df):
    out = clean(raw_df)
    # row 2 had empty region; row 3 had unparseable date — both must be dropped
    assert len(out) == 2


def test_revenue_is_units_times_price(raw_df):
    out = clean(raw_df)
    assert ((out["units"] * out["unit_price"]) == out["revenue"]).all()


def test_summary_columns_are_present(raw_df):
    out = clean(raw_df)
    s = summarize(out)
    assert list(s.columns) == ["region", "total_units", "total_revenue", "rows"]


def test_run_creates_outputs(tmp_path: Path):
    raw_csv = tmp_path / "raw.csv"
    _make_sample(raw_csv)
    result = run(raw_csv, tmp_path / "out")
    assert result.clean_path.exists()
    assert result.summary_path.exists()
    assert result.rows_in > result.rows_out         # some rows were dropped
