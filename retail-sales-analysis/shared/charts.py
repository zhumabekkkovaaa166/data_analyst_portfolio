"""Reusable chart functions for the retail-sales-analysis project."""

import os

import pandas as pd
import matplotlib.pyplot as plt

from shared.locale_config import LOCALES

# SQL queries shared across all locales (SQLite dialect)
_Q_MONTHLY_TREND = """
    SELECT strftime('%m', o.OrderDate) AS month,
           SUM(p.Price * od.Quantity)  AS revenue
    FROM Orders o
    JOIN OrderDetails od ON od.OrderID  = o.OrderID
    JOIN Products     p  ON p.ProductID = od.ProductID
    GROUP BY month
    ORDER BY month;
"""

_Q_CATEGORY_REVENUE = """
    SELECT c.CategoryName            AS category,
           SUM(p.Price * od.Quantity) AS revenue
    FROM Categories c
    JOIN Products     p  ON p.CategoryID = c.CategoryID
    JOIN OrderDetails od ON od.ProductID = p.ProductID
    GROUP BY c.CategoryName
    ORDER BY revenue DESC;
"""

_Q_CLV = """
    SELECT c.CustomerName            AS customer,
           SUM(p.Price * od.Quantity) AS revenue
    FROM Customers c
    JOIN Orders       o  ON o.CustomerID = c.CustomerID
    JOIN OrderDetails od ON od.OrderID   = o.OrderID
    JOIN Products     p  ON p.ProductID  = od.ProductID
    GROUP BY c.CustomerID, c.CustomerName;
"""


def _save(fig, path, dpi=130):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=dpi)
    plt.close(fig)


def chart_monthly_trend(con, results_dir, locale="en"):
    """Line chart of monthly revenue with fill."""
    labels = LOCALES[locale]["chart_monthly_trend"]
    df = pd.read_sql(_Q_MONTHLY_TREND, con)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["month"], df["revenue"], marker="o", linewidth=2, color="#2563eb")
    ax.fill_between(df["month"], df["revenue"], alpha=0.12, color="#2563eb")
    ax.set_title(labels["title"])
    ax.set_xlabel(labels["xlabel"])
    ax.set_ylabel(labels["ylabel"])
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    out = os.path.join(results_dir, "monthly_trend.png")
    _save(fig, out)
    return out


def chart_category_revenue(con, results_dir, locale="en"):
    """Bar chart of category revenue with above-average highlighting."""
    labels = LOCALES[locale]["chart_category_revenue"]
    df = pd.read_sql(_Q_CATEGORY_REVENUE, con)
    avg = df["revenue"].mean()

    colors = ["#2563eb" if v > avg else "#cbd5e1" for v in df["revenue"]]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(df["category"], df["revenue"], color=colors)
    ax.axhline(
        avg, color="#ef4444", linestyle="--", linewidth=1.5,
        label=labels["avg_label"].format(avg=avg),
    )
    ax.set_title(labels["title"])
    ax.set_ylabel(labels["ylabel"])
    ax.legend()
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    out = os.path.join(results_dir, "category_revenue.png")
    _save(fig, out)
    return out


def chart_clv_segments(con, results_dir, locale="en"):
    """Bar chart of customer segments by quantile."""
    labels = LOCALES[locale]["chart_clv_segments"]
    df = pd.read_sql(_Q_CLV, con)

    df["segment"] = pd.qcut(
        df["revenue"], q=[0, 0.5, 0.8, 1.0],
        labels=["Low", "Medium", "High"],
    )
    counts = df["segment"].value_counts().reindex(["High", "Medium", "Low"])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(counts.index, counts.values,
           color=["#2563eb", "#60a5fa", "#cbd5e1"])
    ax.set_title(labels["title"])
    ax.set_ylabel(labels["ylabel"])
    for i, v in enumerate(counts.values):
        ax.text(i, v + 0.1, str(int(v)), ha="center")
    fig.tight_layout()

    out = os.path.join(results_dir, "clv_segments.png")
    _save(fig, out)
    return out
