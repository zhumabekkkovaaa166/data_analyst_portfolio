-- ============================================================
-- Challenge 2 — Top Customers                          [Top-N pattern]
-- ------------------------------------------------------------
-- Business question: marketing wants to reward the most LOYAL customers
-- -> find the top 5 by spend.
-- Metric: total_spent = SUM(Price * Quantity) per customer.
-- Caveat: "loyal" != "high spender". A single large order is a whale, not
-- a loyal customer. A production metric would use RFM (recency, frequency,
-- monetary), not a raw SUM.
-- Skills: JOIN · GROUP BY · ORDER BY DESC · LIMIT
-- ============================================================
SELECT
    c.CustomerName               AS customer_name,
    SUM(p.Price * od.Quantity)   AS total_spent
FROM Customers c
JOIN Orders       o  ON o.CustomerID = c.CustomerID
JOIN OrderDetails od ON od.OrderID   = o.OrderID
JOIN Products     p  ON p.ProductID  = od.ProductID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY total_spent DESC
LIMIT 5;
