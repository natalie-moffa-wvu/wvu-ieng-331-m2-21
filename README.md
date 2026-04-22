# 331-milestone2-ruby-natalie
# Milestone 2: Python Pipeline

Team: Ruby and Natalie 
---

## How to Run

Follow these steps to run the pipeline from a fresh clone:

```bash
git clone https://github.com/{username}/wvu-ieng-331-m2-3.git
cd wvu-ieng-331-m2-21

# install dependencies
uv sync

# manually place the database file
# (olist.duckdb is NOT included in the repo)
# put it here:
# data/olist.duckdb

# run full pipeline (no filters)
uv run wvu-ieng-331-m2-21

# run with filters
uv run wvu-ieng-331-m2-21 --start-date 2018-01-01 --end-date 2018-06-01 --seller-state SP



## Parameters
The pipeline accepts command-line arguments to dynamically filter the dataset:
Parameter	Type	Default	Description
--start-date	string (YYYY-MM-DD)	None	Filters orders starting from this date
--end-date	string (YYYY-MM-DD)	None	Filters orders up to this date
--seller-state	string	None	Filters sellers by state (e.g., SP, RJ)


## Outputs
The pipeline generates three output files in the output/ directory:
    1. summary.csv
    Format: CSV
    Contains aggregated revenue grouped by seller state
    Columns:
    seller_state
    total_revenue
    Purpose: Provides a high-level summary of performance across regions
    2. detail.parquet
    Format: Parquet
    Contains the full dataset returned from the query
    Includes:
    seller_id
    seller_state
    total_orders
    revenue
    Purpose: Used for detailed analysis or further processing
    3. chart.html
    Format: Self-contained HTML file
    Generated using Altair
    Displays a bar chart of revenue by seller state
    Purpose: Quick visualization without needing Python
## Validation Checks
Before running any analysis, the pipeline performs validation to ensure data quality:
    1. Table Existence
    Confirms all 9 expected tables exist in the database
    Missing tables trigger a WARNING log
    2. Row Count Threshold
    Ensures core tables (orders, order_items, customers) contain at least 1,000 rows
    Prevents analysis on incomplete datasets
    3. Date Range Validation
    Checks minimum and maximum order dates
    Identifies:
    Empty datasets
    Future-dated records
    4. Key Column Integrity
    Ensures key identifiers (order_id, customer_id, etc.) are not entirely NULL
    Validation Behavior
    Validation results are logged using loguru
    Issues are reported as WARNINGS
    The pipeline continues execution even if validation issues occur
    This allows flexibility for extended datasets used in grading
    List each validation check your pipeline runs before analysis and what happens if it fails.

## Analysis Summary
The analysis evaluates seller performance based on order volume and revenue.
Key findings include:
A small number of sellers generate a large portion of total revenue
Seller performance is geographically concentrated, with certain states dominating
Revenue distribution follows an ABC-style pattern:
A-class sellers contribute the majority of revenue
B and C classes contribute progressively less
These results are consistent with typical marketplace dynamics where a few top performers dominate overall output.

## Limitations & Caveats
    1. Schema Dependency
    The pipeline assumes the database follows the Olist schema
    Changes to table or column names may break queries
    2. Validation Does Not Halt Execution
    Validation issues are logged but do not stop the pipeline
    This may allow invalid data to propagate into outputs
    3. Performance Constraints
    Data is converted from DuckDB → Pandas → Polars
    This may become inefficient for very large datasets
    4. Limited Filtering Options
    Only date range and seller state are supported
    Additional filters (e.g., product category) are not implemented
    5. Static Visualization
    The output chart is not interactive beyond basic HTML rendering
    No dashboard or advanced visualization features are included
    Future Improvements
    Add additional filters (product category, customer region)
    Improve performance by eliminating Pandas conversion
    Add JSON output for API integration
    Expand validation to include referential integrity checks
    Build interactive dashboards for visualization