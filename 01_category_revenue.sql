-- ============================================================
-- Challenge 1 — Category Revenue                       [HAVING + Subquery]
-- ------------------------------------------------------------
-- Business question: which product category is the most profitable,
-- counting only categories whose revenue is above the average category
-- revenue?
-- Metric: total_revenue = SUM(Price * Quantity) per category.
-- Note: the "above average" filter does NOT pick the leader (a maximum is
-- by definition above the mean). It scopes the set of *significant*
-- categories so weak ones don't clutter the decision.
-- Skills: JOIN · GROUP BY · HAVING · Subquery
-- ============================================================
SELECT
    c.CategoryName               AS category,
    SUM(p.Price * od.Quantity)   AS total_revenue
FROM Categories c
JOIN Products     p  ON p.CategoryID = c.CategoryID
JOIN OrderDetails od ON od.ProductID = p.ProductID
GROUP BY c.CategoryName
HAVING SUM(p.Price * od.Quantity) > (
    SELECT AVG(cat_rev)
    FROM (
        SELECT SUM(p2.Price * od2.Quantity) AS cat_rev
        FROM Products     p2
        JOIN OrderDetails od2 ON od2.ProductID = p2.ProductID
        GROUP BY p2.CategoryID
    ) AS sub
)
ORDER BY total_revenue DESC;
