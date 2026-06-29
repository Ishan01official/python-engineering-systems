"""
pandas in action: load, inspect, groupby, time series.

Run:
    python 16-pandas/examples/01_pandas_tour.py
"""
import io

import numpy as np
import pandas as pd


CSV = """ts,user,product,amount
2026-06-01 09:15,A,X,10
2026-06-01 10:00,A,Y,20
2026-06-02 11:00,B,X,15
2026-06-02 14:30,B,X,25
2026-06-03 09:45,C,Y,30
2026-06-03 12:00,A,X,12
2026-06-04 08:00,B,Y,18
"""


def load_and_inspect() -> pd.DataFrame:
    print("--- load + inspect ---")
    df = pd.read_csv(io.StringIO(CSV), parse_dates=["ts"])
    print(df.head(3))
    print()
    print("dtypes:", dict(df.dtypes))
    print("shape:", df.shape)
    print()
    return df


def filter_and_select(df: pd.DataFrame) -> None:
    print("--- filter + select ---")
    print("rows with amount > 15:")
    print(df.loc[df["amount"] > 15, ["ts", "user", "amount"]])
    print()


def groupby_aggregations(df: pd.DataFrame) -> None:
    print("--- groupby ---")
    print("per-user totals:")
    print(df.groupby("user")["amount"].sum())
    print()
    print("multi-stat per user:")
    print(df.groupby("user")["amount"].agg(["sum", "mean", "count"]))
    print()
    print("user × product pivot:")
    print(df.pivot_table(index="user", columns="product",
                         values="amount", aggfunc="sum", fill_value=0))
    print()


def time_resample(df: pd.DataFrame) -> None:
    print("--- time-indexed resample ---")
    ts_df = df.set_index("ts").sort_index()
    daily = ts_df["amount"].resample("D").sum()
    print("daily totals:")
    print(daily)
    print()
    print("3-row rolling mean:")
    print(ts_df["amount"].rolling(3).mean().tail(5))
    print()


def transform_adds_group_column(df: pd.DataFrame) -> None:
    print("--- groupby.transform: per-row group stat ---")
    df = df.copy()
    df["user_total"] = df.groupby("user")["amount"].transform("sum")
    df["share_of_user"] = df["amount"] / df["user_total"]
    print(df[["user", "amount", "user_total", "share_of_user"]])
    print()


if __name__ == "__main__":
    df = load_and_inspect()
    filter_and_select(df)
    groupby_aggregations(df)
    time_resample(df)
    transform_adds_group_column(df)
