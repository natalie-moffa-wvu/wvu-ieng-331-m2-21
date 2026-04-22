"""
Run all project SQL files against olist.duckdb using the DuckDB Python API (no duckdb CLI).

Usage (from repo root):
  py -3 scripts/run_all.py
  py -3 scripts/run_all.py path/to/custom.duckdb
"""
from __future__ import annotations

import sys
from pathlib import Path

import duckdb

SQL_FILES = [
    "data_quality.sql",
    "cohort_retention.sql",
    "delivery_analysis.sql",
    "product_abc.sql",
    "seller_scorecard.sql",
]


def _split_statements(sql: str) -> list[str]:
    """Split on ';' and drop comment-only / empty chunks (Olist SQL has no ';' inside strings)."""
    out: list[str] = []
    for raw in sql.split(";"):
        chunk = raw.strip()
        if not chunk:
            continue
        lines: list[str] = []
        for line in chunk.splitlines():
            if line.strip().startswith("--"):
                continue
            lines.append(line)
        stmt = "\n".join(lines).strip()
        if stmt:
            out.append(stmt)
    return out


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    db = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "olist.duckdb"
    if not db.is_file():
        raise SystemExit(
            f"Missing database: {db}\n"
            "Load CSVs first:\n"
            f'  py -3 scripts/load_olist.py "<csv_folder>" "{db}"'
        )

    con = duckdb.connect(str(db))
    for name in SQL_FILES:
        path = root / name
        if not path.is_file():
            raise SystemExit(f"Missing file: {path}")
        print(f"\n=== {name} ===")
        sql_text = path.read_text(encoding="utf-8")
        for stmt in _split_statements(sql_text):
            rel = con.execute(stmt + ";")
            df = rel.fetchdf()
            if df is not None and not df.empty:
                print(df.to_string(index=False))
            else:
                print("(0 rows)")
    con.close()


if __name__ == "__main__":
    main()
