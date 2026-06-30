-- ============================================================
-- Challenge 4 — Employee Performance                   [COUNT + CONCAT]
-- ------------------------------------------------------------
-- Business question: HR wants to evaluate order throughput per employee
-- for quarterly bonuses.
-- Metric: total_orders = COUNT(OrderID) per employee.
-- Caveat (Goodhart's Law): once COUNT(orders) drives a bonus it stops
-- being a fair measure — people split orders, chase easy ones, trade
-- quality for volume. A fairer target: revenue/margin per employee plus a
-- quality signal, harder to game alone.
-- Skills: JOIN · GROUP BY · COUNT · CONCAT
-- ============================================================
SELECT
    CONCAT(e.FirstName, ' ', e.LastName) AS employee,
    COUNT(o.OrderID)                     AS total_orders
FROM Employees e
JOIN Orders o ON o.EmployeeID = e.EmployeeID
GROUP BY e.EmployeeID, e.FirstName, e.LastName
ORDER BY total_orders DESC;
