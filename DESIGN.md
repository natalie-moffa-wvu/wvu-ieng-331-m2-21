# Design Rationale

This document explains how the pipeline is structured, how data flows through it, and why specific design decisions were made.

---

## Parameter Flow

The pipeline begins in the `main()` function located in `pipeline.py`.

### Step 1: Argument Parsing
Command-line arguments are parsed using the `parse_args()` function:
```python
args = parse_args()