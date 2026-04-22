from pathlib import Path
from typing import Optional
import duckdb
import polars as pl


def load_sql(file_name: str) -> str:
    """Load SQL query from file."""
    sql_path = Path(__file__).parent.parent.parent / "sql" / file_name
    return sql_path.read_text()


def get_seller_scorecard(
    db_path: str,
    start_date: Optional[str],
    end_date: Optional[str],
    seller_state: Optional[str],
) -> pl.DataFrame:
    """
    Execute seller scorecard query.

    Args:
        db_path: Path to DuckDB file
        start_date: Filter start date
        end_date: Filter end date
        seller_state: Seller state filter

    Returns:
        Polars DataFrame with results
    """
    query = load_sql("seller_scorecard.sql")

    con = duckdb.connect(db_path)
    result = con.execute(query, [start_date, end_date, seller_state]).fetch_df()
    con.close()

    return pl.from_pandas(result)