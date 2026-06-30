-- ============================================================
-- Final — Customer Lifetime Value (simplified)         [CASE WHEN segmentation]
-- ------------------------------------------------------------
-- Business question: compute each customer's CLV, split into High / Medium
-- / Low segments, and build a marketing strategy.
-- Metric: revenue per customer + a categorical `segment` label.
-- Two caveats:
--   1) This is HISTORICAL revenue, not predictive CLV. True CLV forecasts
--      future value with a churn probability.
--   2) Thresholds 10000 / 5000 are arbitrary round numbers. A mature
--      version sets boundaries by QUANTILES (top 20% = High via ntile(5)),
--      robust to growth and inflation.
-- Skills: JOIN · GROUP BY · SUM · CASE WHEN · ORDER BY
-- ============================================================
SELECT
    c.CustomerName               AS customer,
    SUM(p.Price * od.Quantity)   AS revenue,
    CASE
        WHEN SUM(p.Price * od.Quantity) > 10000 THEN 'High'
        WHEN SUM(p.Price * od.Quantity) >  5000 THEN 'Medium'
        ELSE 'Low'
    END                          AS segment
FROM Customers c
JOIN Orders       o  ON o.CustomerID = c.CustomerID
JOIN OrderDetails od ON od.OrderID   = o.OrderID
JOIN Products     p  ON p.ProductID  = od.ProductID
GROUP BY c.CustomerID, c.CustomerName
ORDER BY revenue DESC;
