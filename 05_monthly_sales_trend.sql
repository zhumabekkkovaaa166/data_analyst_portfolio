-- ============================================================
-- Challenge 5 — Monthly Sales Trend                    [date functions]
-- ------------------------------------------------------------
-- Business question: the director wants to see how sales changed over the
-- year to spot seasonality for planning.
-- Metric: revenue = SUM(Price * Quantity) per (year, month).
-- Key call: group by year AND month together. Grouping by month only would
-- collapse Jan-2022 and Jan-2023 into one row and hide the year-over-year
-- trend. Chronological ORDER BY makes the seasonal wave readable.
--
-- Dialect note: YEAR()/MONTH() are MySQL-style. In SQLite use
--   strftime('%Y', o.OrderDate), strftime('%m', o.OrderDate).
-- Skills: JOIN · YEAR() · MONTH() · GROUP BY
-- ============================================================
SELECT
    YEAR(o.OrderDate)            AS year,
    MONTH(o.OrderDate)           AS month,
    SUM(p.Price * od.Quantity)   AS revenue
FROM Orders o
JOIN OrderDetails od ON od.OrderID  = o.OrderID
JOIN Products     p  ON p.ProductID = od.ProductID
GROUP BY YEAR(o.OrderDate), MONTH(o.OrderDate)
ORDER BY year, month;
