-- ============================================================
-- Challenge 3 — Best Selling Products                  [aggregation in units]
-- ------------------------------------------------------------
-- Business question: purchasing wants the top 10 most in-demand products
-- to prioritize for restocking.
-- Metric: total_quantity_sold = SUM(Quantity) per product.
-- Key call: UNITS, not revenue. Same SQL shape as Challenge 2, but a
-- warehouse decision is measured in items, not money. Using revenue here
-- would surface one expensive low-volume product and misguide the restock.
-- Skills: JOIN · GROUP BY · ORDER BY DESC · LIMIT
-- ============================================================
SELECT
    p.ProductName       AS product_name,
    SUM(od.Quantity)    AS total_quantity_sold
FROM Products p
JOIN OrderDetails od ON od.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY total_quantity_sold DESC
LIMIT 10;
