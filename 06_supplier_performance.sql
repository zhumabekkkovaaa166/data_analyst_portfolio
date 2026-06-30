-- ============================================================
-- Challenge 6 — Supplier Performance                   [multi-table join]
-- ------------------------------------------------------------
-- Business question: purchasing wants the most valuable supplier partners
-- to sign long-term contracts with.
-- Metric: total_revenue = SUM(Price * Quantity) per supplier.
-- Caveat: this is *turnover through* a supplier, not their margin or
-- reliability. A contract decision should also weigh purchase cost, supply
-- reliability, and concentration risk (60% of turnover on one supplier is
-- a risk, not just a plus).
-- Skills: JOIN · GROUP BY · SUM · ORDER BY DESC
-- ============================================================
SELECT
    s.SupplierName               AS supplier_name,
    SUM(p.Price * od.Quantity)   AS total_revenue
FROM Suppliers s
JOIN Products     p  ON p.SupplierID = s.SupplierID
JOIN OrderDetails od ON od.ProductID = p.ProductID
GROUP BY s.SupplierID, s.SupplierName
ORDER BY total_revenue DESC;
