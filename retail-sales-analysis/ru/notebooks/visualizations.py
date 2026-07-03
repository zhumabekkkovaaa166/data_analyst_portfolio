"""
Анализ розничных продаж — визуализация на Python + SQL + pandas.

Самодостаточный скрипт: собирает небольшую демо-базу в форме Northwind (SQLite),
запускает аналитические запросы (диалект SQLite) и экспортирует графики в ../results/.

Запуск:  python notebooks/visualizations.py
Демо-данные детерминированы (фиксированный seed), графики воспроизводятся точно.
Замените build_demo_db() на подключение к реальному Northwind для работы с реальными данными.
"""

import os
import sys

# Allow imports from the project root (one level above ru/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from shared.db import build_demo_db
from shared.charts import chart_monthly_trend, chart_category_revenue, chart_clv_segments

LOCALE = "ru"
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def main():
    con = build_demo_db(locale=LOCALE)
    outputs = [
        chart_monthly_trend(con, RESULTS_DIR, locale=LOCALE),
        chart_category_revenue(con, RESULTS_DIR, locale=LOCALE),
        chart_clv_segments(con, RESULTS_DIR, locale=LOCALE),
    ]
    con.close()
    print("Графики сохранены:")
    for o in outputs:
        print("  -", os.path.relpath(o))


if __name__ == "__main__":
    main()
