-- ============================================================
-- Задание 6 — Производительность поставщиков           [мульти-join]
-- ------------------------------------------------------------
-- Бизнес-вопрос: закуп хочет найти самых ценных поставщиков-партнёров
-- для долгосрочных контрактов.
-- Метрика: total_revenue = SUM(Price * Quantity) по поставщику.
-- Подмена: это оборот ЧЕРЕЗ поставщика, не его маржа и не надёжность.
-- Решение о контракте должно учитывать ещё закупочную цену, надёжность
-- поставок и риск зависимости (60% оборота на одном — это риск,
-- а не только плюс).
-- Навыки: JOIN · GROUP BY · SUM · ORDER BY DESC
-- ============================================================
SELECT
    s.SupplierName               AS supplier_name,
    SUM(p.Price * od.Quantity)   AS total_revenue
FROM Suppliers s
JOIN Products     p  ON p.SupplierID = s.SupplierID
JOIN OrderDetails od ON od.ProductID = p.ProductID
GROUP BY s.SupplierID, s.SupplierName
ORDER BY total_revenue DESC;
