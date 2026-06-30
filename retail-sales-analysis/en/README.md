# Retail Sales Analysis — SQL Analytics

🇬🇧 English · [🇷🇺 Русский](../ru/README.md)

Business analytics on the classic **Northwind** retail dataset (customers, orders,
products, suppliers, employees). The focus is not SQL syntax — it's **analytical
judgment**: turning a business question into the *right* metric, and being explicit
about where a stated goal and a computed metric diverge.

> **Core principle:** a metric is not derived from the data — it's derived from the
> **decision** it will support. The same SQL can produce different metrics depending
> on the decision being made.

---

## What this demonstrates

`JOIN` · `GROUP BY` · `HAVING` · `Subqueries` · `Window Functions` ·
`Date Functions` · `CASE WHEN` · **Business reasoning**

## Challenges

| # | Business question | Metric | Skill |
|---|---|---|---|
| [1](./queries/01_category_revenue.sql) | Most profitable category, above-average only | `SUM(Price×Qty)` / category | `HAVING` + subquery |
| [2](./queries/02_top_customers.sql) | Top 5 customers for a loyalty campaign | `total_spent` | Top-N |
| [3](./queries/03_best_selling_products.sql) | Top 10 products to restock | `SUM(Quantity)` | aggregation in units |
| [4](./queries/04_employee_performance.sql) | Order throughput for bonuses | `COUNT(OrderID)` | `COUNT` + `CONCAT` |
| [5](./queries/05_monthly_sales_trend.sql) | Monthly trend / seasonality | `revenue` by (year, month) | date functions |
| [6](./queries/06_supplier_performance.sql) | Most valuable suppliers | `total_revenue` / supplier | multi-table join |
| [★](./queries/07_customer_lifetime_value.sql) | Customer segmentation (simplified CLV) | `revenue` + segment | `CASE WHEN` |

Each query carries a bilingual header stating the business question, the chosen
metric, and any caveat where the metric simplifies the brief.

---

## The interesting part: where the metric meets (or misses) intent

Several challenges hide a gap between the *word* in the brief and the *metric* actually
computed. Surfacing that gap is the analyst's real value. Full write-up in
[`analysis/business_reasoning.md`](./analysis/business_reasoning.md):

- **"Loyal" (Ch. 2)** — brief says *loyal*, metric computes *spend*. A whale ≠ a loyal
  customer; production would use **RFM**.
- **Restock vs. revenue (Ch. 3)** — near-identical SQL to Ch. 2, but measured in
  **units**: a warehouse decision isn't in dollars.
- **Goodhart's Law (Ch. 4)** — `COUNT(orders)` as a bonus target invites gaming.
- **"CLV" (Final)** — *historical* revenue, not *predictive*; thresholds should be
  **quantiles**, not round numbers.

---

## Repository structure

```
.
├── queries/      annotated .sql, one per challenge (bilingual headers)
├── analysis/     business reasoning (EN + RU)
├── notebooks/    Python + pandas visualizations (self-contained, runnable)
├── results/      exported charts — view without running anything
└── data/         schema notes & how to load Northwind
```

---

## How I'd productionize this

The queries run against a flat SQL playground, but the same logic maps to a modern
lakehouse stack:

- Wrap each challenge as a **dbt model** on **Trino**, materialized over **Iceberg**.
- Replace one-off aggregates with **incremental models** keyed on `OrderDate`.
- Add **dbt tests** (not-null, accepted-values on segments, FK relationship tests).
- Schedule with **Airflow**; the monthly-trend query becomes a daily-refreshed mart.
- Promote the "loyalty" definition from `SUM` to a proper **RFM** feature table.

---

## How to run

```bash
# 1) Reproduce the charts locally (self-contained demo data, no setup):
pip install -r requirements.txt
python notebooks/visualizations.py        # writes PNGs into results/

# 2) Or run the raw SQL against real Northwind:
#    load Northwind into any SQL engine and run any file in queries/
```

See [`data/schema.md`](./data/schema.md) for the schema and dialect notes.

---

## About

Built by **[Your Name]** — Analytics Engineer.
Stack: Trino · dbt · Apache Iceberg · S3 · Airflow.
[LinkedIn](#) · [Portfolio](#)
