"""
Load Brazilian E-Commerce (Olist) CSVs into a DuckDB file.

Option A — GitHub mirror (no Kaggle account):
  git clone --depth 1 https://github.com/spdrio/Brazilian-E-Commerce-Public-Dataset-by-Olist.git data/olist-mirror
  CSVs live under: data/olist-mirror/files/

Option B — Kaggle zip (if you use it):
  https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
  Unzip so olist_orders_dataset.csv and siblings sit in one folder.


Then run all analyses (Python; no duckdb CLI):
  py -3 scripts/run_all.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

# Kaggle filenames -> table names expected by the project SQL files
CSV_TABLES: list[tuple[str, str]] = [
    ("olist_orders_dataset.csv", "orders"),
    ("olist_order_items_dataset.csv", "order_items"),
    ("olist_customers_dataset.csv", "customers"),
    ("olist_products_dataset.csv", "products"),
    ("olist_order_reviews_dataset.csv", "order_reviews"),
]


def _looks_like_placeholder(path_str: str) -> bool:
    u = path_str.upper()
    return (
        "PASTE" in u
        or "PATH\\TO\\" in u
        or "PATH/TO/" in path_str.upper()
        or "YOUR_DATABASE" in u
        or "YOUR_REAL" in u
        or "FOLDER_HERE" in u
        or "CONTAINING\\CSVS" in u
    )


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(
            "Usage: py -3 scripts/load_olist.py <folder_with_csvs> <output.duckdb>"
        )

    csv_arg, db_arg = sys.argv[1], sys.argv[2]
    if _looks_like_placeholder(csv_arg) or _looks_like_placeholder(db_arg):
        sys.exit(
            "You used an example/placeholder path.\n"
            "1. Download & unzip Kaggle Olist CSVs.\n"
            "2. In File Explorer, open the folder that CONTAINS olist_orders_dataset.csv.\n"
            "3. Click the address bar, copy the full path, and use it as the FIRST argument.\n"
            "   Example (yours will differ): "
            '"C:\\\\Users\\\\johnm\\\\Downloads\\\\archive"'
        )

    folder = Path(csv_arg).resolve()
    db_path = Path(db_arg).resolve()

    if not folder.is_dir():
        sys.exit(f"Not a folder: {folder}")

    missing = [f for f, _ in CSV_TABLES if not (folder / f).is_file()]
    if missing:
        sys.exit(
            "Missing CSV(s) in folder:\n  "
            + "\n  ".join(missing)
            + f"\n\nExpected folder: {folder}"
        )

    con = duckdb.connect(str(db_path))
    for csv_name, table in CSV_TABLES:
        path = (folder / csv_name).resolve()
        con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(
            f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto(?);",
            [str(path)],
        )
        n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {n:,} rows")

    con.close()
    print(f"\nWrote {db_path}")


if __name__ == "__main__":
    main()