"""
Retail Sales Analysis — Python + SQL + pandas visualizations.

Self-contained: builds a small demo Northwind-shaped SQLite database, runs the
analytical queries (SQLite dialect), and exports charts to ../results/.

Run:  python notebooks/visualizations.py
The demo data is deterministic (fixed seed) so charts reproduce exactly.
Swap `build_demo_db()` for a real Northwind connection to use real data.
"""

import os
import sys

# Allow imports from the project root (one level above en/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from shared.db import build_demo_db
from shared.charts import chart_monthly_trend, chart_category_revenue, chart_clv_segments

LOCALE = "en"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def main():
    con = build_demo_db(locale=LOCALE)
    outputs = [
        chart_monthly_trend(con, RESULTS_DIR, locale=LOCALE),
        chart_category_revenue(con, RESULTS_DIR, locale=LOCALE),
        chart_clv_segments(con, RESULTS_DIR, locale=LOCALE),
    ]
    con.close()
    print("Charts written:")
    for o in outputs:
        print("  -", os.path.relpath(o))


if __name__ == "__main__":
    main()
