-- ============================================================
-- Задание 1 — Выручка по категориям                    [HAVING + подзапрос]
-- ------------------------------------------------------------
-- Бизнес-вопрос: какая категория самая прибыльная, если учитывать только
-- категории с выручкой выше средней по категориям?
-- Метрика: total_revenue = SUM(Price * Quantity) по категории.
-- Примечание: фильтр «выше среднего» НЕ выбирает лидера (максимум всегда
-- выше среднего). Он очерчивает множество *значимых* категорий, чтобы
-- слабые не мешали решению.
-- Навыки: JOIN · GROUP BY · HAVING · Подзапрос
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
