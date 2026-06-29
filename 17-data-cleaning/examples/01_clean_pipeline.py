"""
End-to-end data cleaning: load messy data, validate, fix, reshape, join.

Run:
    python 17-data-cleaning/examples/01_clean_pipeline.py
"""
import io

import numpy as np
import pandas as pd


MESSY = """id,name,age,email,signup
1,Alice,30,alice@x.com,2026-01-15
2, Bob ,25,bob@x.com,2026-02-01
3,Carol,,carol@x.com,2026-02-15
4,Dan,N/A,,2026-03-01
5,Eve,200,eve@x.com,2026-03-15
6,,28,frank@x.com,
"""

ORDERS = """user_id,amount
1,100
1,50
2,200
3,75
99,999
"""


def clean_users(text: str) -> pd.DataFrame:
    print("--- load + inspect ---")
    df = pd.read_csv(io.StringIO(text), parse_dates=["signup"])
    print(df)
    print()
    print("nulls per column:")
    print(df.isna().sum())
    print()

    print("--- clean ---")

    # 1. Strip whitespace in object columns
    for col in df.select_dtypes("object").columns:
        df[col] = df[col].str.strip()

    # 2. Coerce "N/A" string to real NaN, then make age numeric
    df["age"] = pd.to_numeric(df["age"].replace({"N/A": np.nan}), errors="coerce")

    # 3. Drop impossible ages (> 120)
    bad_age = df["age"] > 120
    print(f"  dropping {bad_age.sum()} rows with impossible age")
    df = df.loc[~bad_age]

    # 4. Require name and email
    required = df["name"].notna() & df["email"].notna()
    print(f"  dropping {(~required).sum()} rows missing name or email")
    df = df.loc[required]

    # 5. Fill remaining age with median
    median_age = df["age"].median()
    df["age"] = df["age"].fillna(median_age).round().astype("Int64")

    print(f"  final shape: {df.shape}")
    print(df)
    print()
    return df


def join_with_orders(users: pd.DataFrame, orders_text: str) -> pd.DataFrame:
    print("--- join with orders ---")
    orders = pd.read_csv(io.StringIO(orders_text))

    joined = orders.merge(
        users,
        left_on="user_id",
        right_on="id",
        how="left",
        validate="m:1",       # many orders to one user
        indicator=True,
    )
    print("merge indicator counts:")
    print(joined["_merge"].value_counts())
    print()

    print("orders with no matching user:")
    print(joined.loc[joined["_merge"] == "left_only", ["user_id", "amount"]])
    print()

    # Keep only valid joins
    valid = joined.loc[joined["_merge"] == "both"].drop(columns=["_merge", "id"])
    return valid


def aggregate_per_user(joined: pd.DataFrame) -> pd.DataFrame:
    print("--- aggregate per user ---")
    summary = (
        joined.groupby(["user_id", "name"])
        .agg(total=("amount", "sum"), orders=("amount", "count"))
        .reset_index()
        .sort_values("total", ascending=False)
    )
    print(summary)
    print()
    return summary


if __name__ == "__main__":
    users = clean_users(MESSY)
    joined = join_with_orders(users, ORDERS)
    aggregate_per_user(joined)
