from loguru import logger
import duckdb


EXPECTED_TABLES = [
    "orders",
    "order_items",
    "customers",
    "products",
    "sellers",
    "payments",
    "reviews",
    "geolocation",
    "category_translation",
]


def run_validation(db_path: str) -> None:
    """
    Run validation checks on database.

    Args:
        db_path: Path to DuckDB file
    """
    try:
        con = duckdb.connect(db_path)

        tables = con.execute("SHOW TABLES").fetchall()
        table_names = {t[0] for t in tables}

        for table in EXPECTED_TABLES:
            if table not in table_names:
                logger.warning(f"Missing table: {table}")

        # Row count check
        count = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        if count < 1000:
            logger.warning("Orders table has fewer than 1000 rows")

        # Date check
        date_check = con.execute("""
            SELECT MIN(order_purchase_timestamp), MAX(order_purchase_timestamp)
            FROM orders
        """).fetchone()

        if date_check[1] is None:
            logger.warning("No valid dates in orders table")

        con.close()

    except Exception as e:
        logger.error(f"Validation failed: {e}")