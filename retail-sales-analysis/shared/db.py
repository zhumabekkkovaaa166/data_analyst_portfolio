"""Build a deterministic Northwind-shaped SQLite demo database."""

import sqlite3

import numpy as np

from shared.locale_config import LOCALES

_SCHEMA = """
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

_MONTH_WEIGHTS = np.array([6, 6, 7, 7, 8, 8, 7, 7, 8, 9, 11, 16]) / 100


def build_demo_db(locale="en"):
    """Return an in-memory SQLite connection with demo data.

    Parameters
    ----------
    locale : str
        ``"en"`` or ``"ru"`` — controls category, product, customer and
        employee names inserted into the database.
    """
    loc = LOCALES[locale]
    rng = np.random.default_rng(42)
    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.executescript(_SCHEMA)

    categories = loc["categories"]
    cur.executemany(
        "INSERT INTO Categories VALUES (?,?)",
        [(i + 1, n) for i, n in enumerate(categories)],
    )

    suppliers = [loc["supplier_fmt"].format(chr(65 + i)) for i in range(10)]
    cur.executemany(
        "INSERT INTO Suppliers VALUES (?,?)",
        [(i + 1, n) for i, n in enumerate(suppliers)],
    )

    products = []
    for pid in range(1, 41):
        products.append((
            pid,
            loc["product_fmt"].format(pid),
            int(rng.integers(1, len(categories) + 1)),
            int(rng.integers(1, len(suppliers) + 1)),
            round(float(rng.uniform(5, 120)), 2),
        ))
    cur.executemany("INSERT INTO Products VALUES (?,?,?,?,?)", products)

    cur.executemany(
        "INSERT INTO Customers VALUES (?,?)",
        [(i + 1, loc["customer_fmt"].format(i + 1)) for i in range(25)],
    )

    cur.executemany("INSERT INTO Employees VALUES (?,?,?)", loc["employees"])

    orders, details, od_id = [], [], 1
    for oid in range(1, 601):
        month = int(rng.choice(range(1, 13), p=_MONTH_WEIGHTS))
        orders.append((
            oid,
            int(rng.integers(1, 26)),
            int(rng.integers(1, 6)),
            f"2023-{month:02d}-{int(rng.integers(1, 28)):02d}",
        ))
        for _ in range(int(rng.integers(1, 5))):
            details.append((
                od_id, oid,
                int(rng.integers(1, 41)),
                int(rng.integers(1, 30)),
            ))
            od_id += 1
    cur.executemany("INSERT INTO Orders VALUES (?,?,?,?)", orders)
    cur.executemany("INSERT INTO OrderDetails VALUES (?,?,?,?)", details)

    con.commit()
    return con
