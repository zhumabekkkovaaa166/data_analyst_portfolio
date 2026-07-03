"""Shared utilities for the retail-sales-analysis project."""

from shared.db import build_demo_db
from shared.charts import chart_monthly_trend, chart_category_revenue, chart_clv_segments
from shared.locale_config import LOCALES

__all__ = [
    "build_demo_db",
    "chart_monthly_trend",
    "chart_category_revenue",
    "chart_clv_segments",
    "LOCALES",
]
