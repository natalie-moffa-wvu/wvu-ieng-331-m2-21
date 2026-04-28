# Milestone 2 Grade

**Team 21**

| Criterion | Score | Max |
|-----------|------:|----:|
| Pipeline Functionality | 0 | 6 |
| Parameterization & Configuration | 3 | 6 |
| Code Quality | 5 | 6 |
| Project Structure & M1 Integration | 2 | 3 |
| Design Rationale (DESIGN.md) | 3 | 3 |
| **Total** | **13** | **24** |

*Grace allowance applied: this team was originally Team 3 before being renumbered. The wrong-package import in `pipeline.py` (`from wvu_ieng_331_m2_3 ...`) is treated as a historical naming artifact rather than a defect. Code Quality is bumped 4 → 5 to reflect this allowance. Pipeline Functionality remains 0 because two other unrelated blockers still prevent execution.*

## Pipeline Functionality (0/6)

The pipeline cannot run due to two fatal errors:

1. **Malformed `pyproject.toml`**: Missing `[project]` and `[project.scripts]` TOML section headers. The file contains bare key-value pairs at the top level, which causes `uv sync` to treat the project as an empty workspace — no package is installed and no script entry point is registered. `uv run wvu-ieng-331-m2-21` fails with `No such file or directory`.

2. **SyntaxError in `pipeline.py` line 13**: Stray text after the docstring — `"""Parse CLI arguments."""do the uv fil d` — causes a `SyntaxError` before any code can execute.

(A third issue — `pipeline.py` imports from `wvu_ieng_331_m2_3` instead of `wvu_ieng_331_m2_21` — is forgiven per the grace allowance noted above.)

Neither the standard database run nor the holdout run could be executed. Score: 0/6.

## Parameterization & Configuration (3/6)

The parameter design itself is solid: three CLI parameters (`--start-date`, `--end-date`, `--seller-state`) are defined in `parse_args()`, passed through `get_seller_scorecard()`, and bound directly to SQL positional parameters (`$1`, `$2`, `$3`) with NULL-guard logic (`$1 IS NULL OR ...`). The SQL parameterization in `seller_scorecard.sql` is correct and prevents SQL injection. However, there is no input validation (e.g., date format checking, state code validation), and the pipeline cannot actually execute due to fatal errors above, so the parameters have no demonstrable effect. Score: 3/6.

## Code Quality (5/6)

**Positive**: `queries.py` and `validation.py` use type hints, docstrings, loguru logging, pathlib, and specific exception types (`FileNotFoundError`, `ValueError`, `OSError`). Loguru is imported and used throughout. SQL is stored in external `.sql` files loaded via `pathlib`.

**Negative**:
- `pipeline.py` has a syntax error from stray text in the docstring.
- `src/wvu_ieng_331_m2_21/src/wvu_ieng_331_m2_21/__init__.py` has plain text before the `from .pipeline import main` line (no surrounding `"""` quotes), which is a syntax error.
- The nested `src/wvu_ieng_331_m2_21/src/wvu_ieng_331_m2_21/` directory path is malformed.
- Pandas conversion roundtrip (DuckDB → Pandas → Polars) is noted as a limitation but not addressed.

(The wrong import path in `pipeline.py` would normally be a Code Quality negative, but it is forgiven under the grace allowance noted at the top.)

Score: 5/6.

## Project Structure & M1 Integration (2/3)

**Positive**: `src/` layout attempted, `sql/` directory with multiple `.sql` files, `scripts/` directory, `pyproject.toml` present, `.gitignore` and `.python-version` files present, loguru dependency declared.

**Negative**: `pyproject.toml` is missing `[project]` and `[project.scripts]` section headers (malformed TOML). An erroneous nested directory `src/wvu_ieng_331_m2_21/src/wvu_ieng_331_m2_21/` exists alongside the correct `src/wvu_ieng_331_m2_21/` path. Score: 2/3.

## Design Rationale (3/3)

DESIGN.md is thorough and well-structured with five substantive sections: Parameter Flow, SQL Parameterization, Validation Logic, Error Handling, and Scaling & Adaptation. Each section references specific code constructs (actual function names, SQL snippets, exception types). The rationale for design choices is explained with concrete reasons (e.g., why parameterized queries vs. f-strings, why warnings don't halt execution for holdout compatibility, why SQL is stored in files). Score: 3/3.
