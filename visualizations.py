"""
Retail Sales Analysis — Python + SQL + pandas visualizations.

Self-contained: builds a small demo Northwind-shaped SQLite database, runs the
analytical queries (SQLite dialect), and exports charts to ../results/.

Run:  python notebooks/visualizations.py
The demo data is deterministic (fixed seed) so charts reproduce exactly.
Swap `build_demo_db()` for a real Northwind connection to use real data.
"""

import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# 1) Build a small, deterministic demo database (Northwind-shaped)
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

    categories = ["Beverages", "Condiments", "Confections", "Dairy",
                  "Grains", "Meat", "Produce", "Seafood"]
    cur.executemany("INSERT INTO Categories VALUES (?,?)",
                    [(i + 1, n) for i, n in enumerate(categories)])

    suppliers = [f"Supplier {chr(65+i)}" for i in range(10)]
    cur.executemany("INSERT INTO Suppliers VALUES (?,?)",
                    [(i + 1, n) for i, n in enumerate(suppliers)])

    products = []
    for pid in range(1, 41):
        cat = int(rng.integers(1, len(categories) + 1))
        sup = int(rng.integers(1, len(suppliers) + 1))
        price = round(float(rng.uniform(5, 120)), 2)
        products.append((pid, f"Product {pid:02d}", cat, sup, price))
    cur.executemany("INSERT INTO Products VALUES (?,?,?,?,?)", products)

    customers = [(i + 1, f"Customer {i+1:02d}") for i in range(25)]
    cur.executemany("INSERT INTO Customers VALUES (?,?)", customers)

    employees = [(1, "Anna", "Petrova"), (2, "Bolat", "Kim"),
                 (3, "Chen", "Wei"), (4, "Dana", "Sultan"), (5, "Erik", "Nurlan")]
    cur.executemany("INSERT INTO Employees VALUES (?,?,?)", employees)

    # Orders across 2023 with a mild seasonal pattern (peaks in Nov–Dec)
    orders, details = [], []
    od_id = 1
    for oid in range(1, 601):
        cust = int(rng.integers(1, 26))
        emp = int(rng.integers(1, 6))
        month = int(rng.choice(range(1, 13),
                               p=np.array([6, 6, 7, 7, 8, 8, 7, 7, 8, 9, 11, 16]) / 100))
        day = int(rng.integers(1, 28))
        orders.append((oid, cust, emp, f"2023-{month:02d}-{day:02d}"))
        for _ in range(int(rng.integers(1, 5))):
            details.append((od_id, oid, int(rng.integers(1, 41)),
                            int(rng.integers(1, 30))))
            od_id += 1
    cur.executemany("INSERT INTO Orders VALUES (?,?,?,?)", orders)
    cur.executemany("INSERT INTO OrderDetails VALUES (?,?,?,?)", details)

    con.commit()
    return con


# ----------------------------------------------------------------------
# 2) Queries (SQLite dialect) + charts
# ----------------------------------------------------------------------
def chart_monthly_trend(con):
    q = """
        SELECT strftime('%m', o.OrderDate) AS month,
               SUM(p.Price * od.Quantity)  AS revenue
        FROM Orders o
        JOIN OrderDetails od ON od.OrderID  = o.OrderID
        JOIN Products     p  ON p.ProductID = od.ProductID
        GROUP BY month
        ORDER BY month;
    """
    df = pd.read_sql(q, con)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(df["month"], df["revenue"], marker="o", linewidth=2, color="#2563eb")
    ax.fill_between(df["month"], df["revenue"], alpha=0.12, color="#2563eb")
    ax.set_title("Monthly Revenue Trend (2023) — seasonality peaks toward year-end")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
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
        GROUP BY c.CategoryName
        ORDER BY revenue DESC;
    """
    df = pd.read_sql(q, con)
    avg = df["revenue"].mean()
    colors = ["#2563eb" if v > avg else "#cbd5e1" for v in df["revenue"]]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(df["category"], df["revenue"], color=colors)
    ax.axhline(avg, color="#ef4444", linestyle="--", linewidth=1.5,
               label=f"average = {avg:,.0f}")
    ax.set_title("Category Revenue — blue = above average (the 'significant' set)")
    ax.set_ylabel("Revenue")
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

    # Quantile-based segmentation (the mature alternative to round-number cutoffs)
    df["segment"] = pd.qcut(df["revenue"], q=[0, 0.5, 0.8, 1.0],
                            labels=["Low", "Medium", "High"])
    counts = df["segment"].value_counts().reindex(["High", "Medium", "Low"])

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(counts.index, counts.values,
           color=["#2563eb", "#60a5fa", "#cbd5e1"])
    ax.set_title("Customer Segments by quantile (top 20% = High, not a round number)")
    ax.set_ylabel("Number of customers")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 0.1, str(int(v)), ha="center")
    fig.tight_layout()
    out = os.path.join(RESULTS_DIR, "clv_segments.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    con = build_demo_db()
    outputs = [
        chart_monthly_trend(con),
        chart_category_revenue(con),
        chart_clv_segments(con),
    ]
    con.close()
    print("Charts written:")
    for o in outputs:
        print("  -", os.path.relpath(o))


if __name__ == "__main__":
    main()
