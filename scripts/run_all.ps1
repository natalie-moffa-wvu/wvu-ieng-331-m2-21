# Run all SQL analyses via Python (DuckDB API). No duckdb.exe required.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/run_all.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root
& py -3 scripts/run_all.py @args