"""
Анализ розничных продаж — визуализация на Python + SQL + pandas.

Самодостаточный скрипт: собирает небольшую демо-базу в форме Northwind (SQLite),
запускает аналитические запросы (диалект SQLite) и экспортирует графики в ../results/.

Запуск:  python notebooks/visualizations.py
Демо-данные детерминированы (фиксированный seed), графики воспроизводятся точно.
Замените build_demo_db() на подключение к реальному Northwind для работы с реальными данными.
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


# ----------------------------------------------------------------------
# 1) Собираем детерминированную демо-базу (в форме Northwind)
# ----------------------------------------------------------------------
def build_demo_db():
    rng = np.random.default_rng(42)
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript(
        """
        CREATE TABLE Categories  (CategoryID INTEGER, CategoryName TEXT);
        CREATE TABLE Suppliers   (SupplierID INTEGER, SupplierName TEXT);
        CREATE TABLE Products    (ProductID INTEGER, ProductName TEXT,
                                  CategoryID INTEGER, SupplierID INTEGER, Price REAL);
        CREATE TABLE Customers   (CustomerID INTEGER, CustomerName TEXT);
        CREATE TABLE Employees   (EmployeeID INTEGER, FirstName TEXT, LastName TEXT);
        CREATE TABLE Orders      (OrderID INTEGER, CustomerID INTEGER,
                                  EmployeeID INTEGER, OrderDate TEXT);
        CREATE TABLE OrderDetails(OrderDetailID INTEGER, OrderID INTEGER,
                                  ProductID INTEGER, Quantity INTEGER);
        """
    )
    categories = ["Напитки", "Приправы", "Кондитерские", "Молочные",
                  "Крупы", "Мясо", "Овощи", "Морепродукты"]
    cur.executemany("INSERT INTO Categories VALUES (?,?)",
                    [(i + 1, n) for i, n in enumerate(categories)])
    suppliers = [f"Поставщик {chr(65+i)}" for i in range(10)]
    cur.executemany("INSERT INTO Suppliers VALUES (?,?)",
                    [(i + 1, n) for i, n in enumerate(suppliers)])
    products = []
    for pid in range(1, 41):
        products.append((pid, f"Товар {pid:02d}",
                         int(rng.integers(1, len(categories) + 1)),
                         int(rng.integers(1, len(suppliers) + 1)),
                         round(float(rng.uniform(5, 120)), 2)))
    cur.executemany("INSERT INTO Products VALUES (?,?,?,?,?)", products)
    cur.executemany("INSERT INTO Customers VALUES (?,?)",
                    [(i + 1, f"Клиент {i+1:02d}") for i in range(25)])
    cur.executemany("INSERT INTO Employees VALUES (?,?,?)",
                    [(1, "Анна", "Петрова"), (2, "Болат", "Ким"),
                     (3, "Чэнь", "Вэй"), (4, "Дана", "Султан"), (5, "Эрик", "Нурлан")])
    orders, details, od_id = [], [], 1
    for oid in range(1, 601):
        month = int(rng.choice(range(1, 13),
                    p=np.array([6, 6, 7, 7, 8, 8, 7, 7, 8, 9, 11, 16]) / 100))
        orders.append((oid, int(rng.integers(1, 26)), int(rng.integers(1, 6)),
                       f"2023-{month:02d}-{int(rng.integers(1, 28)):02d}"))
        for _ in range(int(rng.integers(1, 5))):
            details.append((od_id, oid, int(rng.integers(1, 41)),
                            int(rng.integers(1, 30))))
            od_id += 1
    cur.executemany("INSERT INTO Orders VALUES (?,?,?,?)", orders)
    cur.executemany("INSERT INTO OrderDetails VALUES (?,?,?,?)", details)
    con.commit()
    return con


# ----------------------------------------------------------------------
# 2) Запросы (диалект SQLite) + графики
# ----------------------------------------------------------------------
def chart_monthly_trend(con):
    q = """
        SELECT strftime('%m', o.OrderDate) AS month,
               SUM(p.Price * od.Quantity)  AS revenue
        FROM Orders o
        JOIN OrderDetails od ON od.OrderID  = o.OrderID
        JOIN Products     p  ON p.ProductID = od.ProductID
        GROUP BY month ORDER BY month;
    """
    df = pd.read_sql(q, con)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["month"], df["revenue"], marker="o", linewidth=2, color="#2563eb")
    ax.fill_between(df["month"], df["revenue"], alpha=0.12, color="#2563eb")
    ax.set_title("Месячный тренд выручки (2023) — пик сезонности к концу года")
    ax.set_xlabel("Месяц")
    ax.set_ylabel("Выручка")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = os.path.join(RESULTS_DIR, "monthly_trend.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def chart_category_revenue(con):
    q = """
        SELECT c.CategoryName            AS category,
               SUM(p.Price * od.Quantity) AS revenue
        FROM Categories c
        JOIN Products     p  ON p.CategoryID = c.CategoryID
        JOIN OrderDetails od ON od.ProductID = p.ProductID
        GROUP BY c.CategoryName ORDER BY revenue DESC;
    """
    df = pd.read_sql(q, con)
    avg = df["revenue"].mean()
    colors = ["#2563eb" if v > avg else "#cbd5e1" for v in df["revenue"]]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(df["category"], df["revenue"], color=colors)
    ax.axhline(avg, color="#ef4444", linestyle="--", linewidth=1.5,
               label=f"среднее = {avg:,.0f}")
    ax.set_title("Выручка по категориям — синие выше среднего («значимое множество»)")
    ax.set_ylabel("Выручка")
    ax.legend()
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    out = os.path.join(RESULTS_DIR, "category_revenue.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def chart_clv_segments(con):
    q = """
        SELECT c.CustomerName            AS customer,
               SUM(p.Price * od.Quantity) AS revenue
        FROM Customers c
        JOIN Orders       o  ON o.CustomerID = c.CustomerID
        JOIN OrderDetails od ON od.OrderID   = o.OrderID
        JOIN Products     p  ON p.ProductID  = od.ProductID
        GROUP BY c.CustomerID, c.CustomerName;
    """
    df = pd.read_sql(q, con)
    df["segment"] = pd.qcut(df["revenue"], q=[0, 0.5, 0.8, 1.0],
                            labels=["Low", "Medium", "High"])
    counts = df["segment"].value_counts().reindex(["High", "Medium", "Low"])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(counts.index, counts.values, color=["#2563eb", "#60a5fa", "#cbd5e1"])
    ax.set_title("Сегменты клиентов по квантилям (топ-20% = High, не круглое число)")
    ax.set_ylabel("Число клиентов")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 0.1, str(int(v)), ha="center")
    fig.tight_layout()
    out = os.path.join(RESULTS_DIR, "clv_segments.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    con = build_demo_db()
    outputs = [chart_monthly_trend(con), chart_category_revenue(con),
               chart_clv_segments(con)]
    con.close()
    print("Графики сохранены:")
    for o in outputs:
        print("  -", os.path.relpath(o))


if __name__ == "__main__":
    main()
