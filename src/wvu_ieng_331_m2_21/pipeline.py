import argparse
from pathlib import Path
from loguru import logger
import polars as pl
import altair as alt

from wvu_ieng_331_m2_3.queries import get_seller_scorecard
from wvu_ieng_331_m2_3.validation import run_validation



def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument("--start-date", type=str, default=None)
    parser.add_argument("--end-date", type=str, default=None)
    parser.add_argument("--seller-state", type=str, default=None)

    return parser.parse_args()


def save_outputs(df: pl.DataFrame, output_dir: Path) -> None:
    """
    Save pipeline outputs.

    Args:
        df: DataFrame to save
        output_dir: Output directory
    """
    try:
        output_dir.mkdir(parents=True, exist_ok=True)

        # summary
        summary = df.group_by("seller_state").agg(
            pl.sum("revenue").alias("total_revenue")
        )
        summary.write_csv(output_dir / "summary.csv")

        # detail
        df.write_parquet(output_dir / "detail.parquet")

        # chart
        chart = (
            alt.Chart(df.to_pandas())
            .mark_bar()
            .encode(x="seller_state", y="revenue")
        )
        chart.save(output_dir / "chart.html")

    except OSError as e:
        logger.error(f"File write failed: {e}")


def main() -> None:
    """Main pipeline entry point."""
    args = parse_args()

    db_path = "data/olist.duckdb"
    output_dir = Path("output")

    try:
        logger.info("Running validation...")
        run_validation(db_path)

        logger.info("Running queries...")
        df = get_seller_scorecard(
            db_path,
            args.start_date,
            args.end_date,
            args.seller_state,
        )

        logger.info("Saving outputs...")
        save_outputs(df, output_dir)

        logger.info("Pipeline completed successfully")

    except FileNotFoundError:
        logger.error("Database file not found")

    except ValueError as e:
        logger.error(f"Invalid input: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")