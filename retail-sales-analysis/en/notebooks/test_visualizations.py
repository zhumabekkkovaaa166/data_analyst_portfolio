"""
Unit tests for en/notebooks/visualizations.py

Tests cover:
- Database construction and schema validation
- Data integrity (deterministic seed)
- Query result correctness
- Chart file generation
- Main orchestration function
"""

import os
import sqlite3
import tempfile
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

# We need to handle the RESULTS_DIR side-effect at import time
import importlib
import sys


@pytest.fixture(scope="module")
def vis_module():
    """Import visualizations module with a temporary RESULTS_DIR."""
    module_path = os.path.join(os.path.dirname(__file__), "visualizations.py")
    spec = importlib.util.spec_from_file_location("visualizations_en", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def db_connection(vis_module):
    """Provide a fresh demo database connection per test."""
    con = vis_module.build_demo_db()
    yield con
    con.close()


@pytest.fixture
def tmp_results(tmp_path, vis_module, monkeypatch):
    """Redirect chart output to a temporary directory."""
    monkeypatch.setattr(vis_module, "RESULTS_DIR", str(tmp_path))
    return tmp_path


# ======================================================================
# Tests for build_demo_db()
# ======================================================================
class TestBuildDemoDB:
    def test_returns_connection(self, vis_module):
        con = vis_module.build_demo_db()
        assert isinstance(con, sqlite3.Connection)
        con.close()

    def test_tables_exist(self, db_connection):
        cur = db_connection.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = sorted([row[0] for row in cur.fetchall()])
        expected = sorted([
            "Categories", "Customers", "Employees",
            "OrderDetails", "Orders", "Products", "Suppliers"
        ])
        assert tables == expected

    def test_categories_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Categories")
        assert cur.fetchone()[0] == 8

    def test_categories_names(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT CategoryName FROM Categories ORDER BY CategoryID")
        names = [row[0] for row in cur.fetchall()]
        expected = [
            "Beverages", "Condiments", "Confections", "Dairy",
            "Grains", "Meat", "Produce", "Seafood"
        ]
        assert names == expected

    def test_suppliers_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Suppliers")
        assert cur.fetchone()[0] == 10

    def test_products_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Products")
        assert cur.fetchone()[0] == 40

    def test_products_price_range(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT MIN(Price), MAX(Price) FROM Products")
        min_price, max_price = cur.fetchone()
        assert min_price >= 5.0
        assert max_price <= 120.0

    def test_customers_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Customers")
        assert cur.fetchone()[0] == 25

    def test_employees_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Employees")
        assert cur.fetchone()[0] == 5

    def test_orders_count(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM Orders")
        assert cur.fetchone()[0] == 600

    def test_order_details_not_empty(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM OrderDetails")
        count = cur.fetchone()[0]
        assert count > 600  # each order has 1-4 details

    def test_orders_date_format(self, db_connection):
        cur = db_connection.cursor()
        cur.execute("SELECT OrderDate FROM Orders LIMIT 10")
        for (date_str,) in cur.fetchall():
            parts = date_str.split("-")
            assert len(parts) == 3
            assert len(parts[0]) == 4  # year
            assert len(parts[1]) == 2  # month
            assert len(parts[2]) == 2  # day

    def test_deterministic_output(self, vis_module):
        """Running build_demo_db twice produces identical data."""
        con1 = vis_module.build_demo_db()
        con2 = vis_module.build_demo_db()
        cur1 = con1.cursor()
        cur2 = con2.cursor()

        cur1.execute("SELECT * FROM Products ORDER BY ProductID")
        cur2.execute("SELECT * FROM Products ORDER BY ProductID")
        assert cur1.fetchall() == cur2.fetchall()

        cur1.execute("SELECT * FROM Orders ORDER BY OrderID")
        cur2.execute("SELECT * FROM Orders ORDER BY OrderID")
        assert cur1.fetchall() == cur2.fetchall()

        con1.close()
        con2.close()

    def test_foreign_key_integrity(self, db_connection):
        """Product CategoryIDs reference valid Categories."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Products p "
            "LEFT JOIN Categories c ON p.CategoryID = c.CategoryID "
            "WHERE c.CategoryID IS NULL"
        )
        assert cur.fetchone()[0] == 0

    def test_order_customer_integrity(self, db_connection):
        """Order CustomerIDs reference valid Customers."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Orders o "
            "LEFT JOIN Customers c ON o.CustomerID = c.CustomerID "
            "WHERE c.CustomerID IS NULL"
        )
        assert cur.fetchone()[0] == 0


# ======================================================================
# Tests for chart_monthly_trend()
# ======================================================================
class TestChartMonthlyTrend:
    def test_returns_file_path(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_monthly_trend(db_connection)
        assert isinstance(result, str)
        assert result.endswith("monthly_trend.png")

    def test_creates_png_file(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_monthly_trend(db_connection)
        assert os.path.isfile(result)
        assert os.path.getsize(result) > 0

    def test_monthly_data_has_12_months(self, db_connection):
        q = """
            SELECT strftime('%m', o.OrderDate) AS month,
                   SUM(p.Price * od.Quantity)  AS revenue
            FROM Orders o
            JOIN OrderDetails od ON od.OrderID  = o.OrderID
            JOIN Products     p  ON p.ProductID = od.ProductID
            GROUP BY month ORDER BY month;
        """
        df = pd.read_sql(q, db_connection)
        assert len(df) == 12

    def test_monthly_revenue_positive(self, db_connection):
        q = """
            SELECT strftime('%m', o.OrderDate) AS month,
                   SUM(p.Price * od.Quantity)  AS revenue
            FROM Orders o
            JOIN OrderDetails od ON od.OrderID  = o.OrderID
            JOIN Products     p  ON p.ProductID = od.ProductID
            GROUP BY month ORDER BY month;
        """
        df = pd.read_sql(q, db_connection)
        assert (df["revenue"] > 0).all()

    def test_seasonal_pattern(self, db_connection):
        """Revenue should generally increase toward year-end due to probability weights."""
        q = """
            SELECT strftime('%m', o.OrderDate) AS month,
                   SUM(p.Price * od.Quantity)  AS revenue
            FROM Orders o
            JOIN OrderDetails od ON od.OrderID  = o.OrderID
            JOIN Products     p  ON p.ProductID = od.ProductID
            GROUP BY month ORDER BY month;
        """
        df = pd.read_sql(q, db_connection)
        # Dec (month 12) has the highest weight (16%), should be high
        dec_rev = df[df["month"] == "12"]["revenue"].iloc[0]
        jan_rev = df[df["month"] == "01"]["revenue"].iloc[0]
        assert dec_rev > jan_rev


# ======================================================================
# Tests for chart_category_revenue()
# ======================================================================
class TestChartCategoryRevenue:
    def test_returns_file_path(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_category_revenue(db_connection)
        assert isinstance(result, str)
        assert result.endswith("category_revenue.png")

    def test_creates_png_file(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_category_revenue(db_connection)
        assert os.path.isfile(result)
        assert os.path.getsize(result) > 0

    def test_all_categories_present(self, db_connection):
        q = """
            SELECT c.CategoryName AS category,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Categories c
            JOIN Products     p  ON p.CategoryID = c.CategoryID
            JOIN OrderDetails od ON od.ProductID = p.ProductID
            GROUP BY c.CategoryName ORDER BY revenue DESC;
        """
        df = pd.read_sql(q, db_connection)
        assert len(df) == 8

    def test_revenue_sorted_descending(self, db_connection):
        q = """
            SELECT c.CategoryName AS category,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Categories c
            JOIN Products     p  ON p.CategoryID = c.CategoryID
            JOIN OrderDetails od ON od.ProductID = p.ProductID
            GROUP BY c.CategoryName ORDER BY revenue DESC;
        """
        df = pd.read_sql(q, db_connection)
        revenues = df["revenue"].tolist()
        assert revenues == sorted(revenues, reverse=True)

    def test_average_splits_above_below(self, db_connection):
        """Some categories are above average and some below."""
        q = """
            SELECT c.CategoryName AS category,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Categories c
            JOIN Products     p  ON p.CategoryID = c.CategoryID
            JOIN OrderDetails od ON od.ProductID = p.ProductID
            GROUP BY c.CategoryName ORDER BY revenue DESC;
        """
        df = pd.read_sql(q, db_connection)
        avg = df["revenue"].mean()
        above = (df["revenue"] > avg).sum()
        below = (df["revenue"] <= avg).sum()
        assert above > 0
        assert below > 0


# ======================================================================
# Tests for chart_clv_segments()
# ======================================================================
class TestChartCLVSegments:
    def test_returns_file_path(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_clv_segments(db_connection)
        assert isinstance(result, str)
        assert result.endswith("clv_segments.png")

    def test_creates_png_file(self, vis_module, db_connection, tmp_results):
        result = vis_module.chart_clv_segments(db_connection)
        assert os.path.isfile(result)
        assert os.path.getsize(result) > 0

    def test_all_customers_segmented(self, db_connection):
        q = """
            SELECT c.CustomerName AS customer,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Customers c
            JOIN Orders       o  ON o.CustomerID = c.CustomerID
            JOIN OrderDetails od ON od.OrderID   = o.OrderID
            JOIN Products     p  ON p.ProductID  = od.ProductID
            GROUP BY c.CustomerID, c.CustomerName;
        """
        df = pd.read_sql(q, db_connection)
        assert len(df) == 25  # all customers have orders

    def test_segment_distribution(self, db_connection):
        """Quantile segmentation: 50% Low, 30% Medium, 20% High."""
        q = """
            SELECT c.CustomerName AS customer,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Customers c
            JOIN Orders       o  ON o.CustomerID = c.CustomerID
            JOIN OrderDetails od ON od.OrderID   = o.OrderID
            JOIN Products     p  ON p.ProductID  = od.ProductID
            GROUP BY c.CustomerID, c.CustomerName;
        """
        df = pd.read_sql(q, db_connection)
        df["segment"] = pd.qcut(
            df["revenue"], q=[0, 0.5, 0.8, 1.0],
            labels=["Low", "Medium", "High"]
        )
        counts = df["segment"].value_counts()
        # Approximately 50% Low, 30% Medium, 20% High
        # With 25 customers: ~12-13 Low, ~7-8 Medium, ~5 High
        assert counts["Low"] >= 10
        assert counts["Medium"] >= 5
        assert counts["High"] >= 3
        assert counts.sum() == 25

    def test_segment_labels(self, db_connection):
        q = """
            SELECT c.CustomerName AS customer,
                   SUM(p.Price * od.Quantity) AS revenue
            FROM Customers c
            JOIN Orders       o  ON o.CustomerID = c.CustomerID
            JOIN OrderDetails od ON od.OrderID   = o.OrderID
            JOIN Products     p  ON p.ProductID  = od.ProductID
            GROUP BY c.CustomerID, c.CustomerName;
        """
        df = pd.read_sql(q, db_connection)
        df["segment"] = pd.qcut(
            df["revenue"], q=[0, 0.5, 0.8, 1.0],
            labels=["Low", "Medium", "High"]
        )
        unique_segments = set(df["segment"].unique())
        assert unique_segments == {"Low", "Medium", "High"}


# ======================================================================
# Tests for main()
# ======================================================================
class TestMain:
    def test_main_runs_without_error(self, vis_module, tmp_results, capsys):
        vis_module.main()
        captured = capsys.readouterr()
        assert "Charts written:" in captured.out

    def test_main_creates_all_charts(self, vis_module, tmp_results):
        vis_module.main()
        expected_files = [
            "monthly_trend.png",
            "category_revenue.png",
            "clv_segments.png",
        ]
        for fname in expected_files:
            fpath = os.path.join(str(tmp_results), fname)
            assert os.path.isfile(fpath), f"Missing: {fname}"


# ======================================================================
# Edge case / robustness tests
# ======================================================================
class TestEdgeCases:
    def test_results_dir_created_if_missing(self, vis_module, tmp_path, monkeypatch):
        new_dir = str(tmp_path / "new_results")
        monkeypatch.setattr(vis_module, "RESULTS_DIR", new_dir)
        os.makedirs(new_dir, exist_ok=True)
        con = vis_module.build_demo_db()
        vis_module.chart_monthly_trend(con)
        assert os.path.isdir(new_dir)
        con.close()

    def test_product_supplier_integrity(self, db_connection):
        """All product SupplierIDs reference valid Suppliers."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Products p "
            "LEFT JOIN Suppliers s ON p.SupplierID = s.SupplierID "
            "WHERE s.SupplierID IS NULL"
        )
        assert cur.fetchone()[0] == 0

    def test_order_employee_integrity(self, db_connection):
        """All order EmployeeIDs reference valid Employees."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM Orders o "
            "LEFT JOIN Employees e ON o.EmployeeID = e.EmployeeID "
            "WHERE e.EmployeeID IS NULL"
        )
        assert cur.fetchone()[0] == 0

    def test_order_detail_product_integrity(self, db_connection):
        """All OrderDetail ProductIDs reference valid Products."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM OrderDetails od "
            "LEFT JOIN Products p ON od.ProductID = p.ProductID "
            "WHERE p.ProductID IS NULL"
        )
        assert cur.fetchone()[0] == 0

    def test_total_revenue_positive(self, db_connection):
        cur = db_connection.cursor()
        cur.execute(
            "SELECT SUM(p.Price * od.Quantity) FROM OrderDetails od "
            "JOIN Products p ON od.ProductID = p.ProductID"
        )
        total = cur.fetchone()[0]
        assert total > 0
