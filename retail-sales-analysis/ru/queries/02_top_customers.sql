-- ============================================================
-- Задание 2 — Топ клиентов                             [паттерн Top-N]
-- ------------------------------------------------------------
-- Бизнес-вопрос: маркетинг хочет поощрить самых ЛОЯЛЬНЫХ клиентов
-- -> найти топ-5 по тратам.
-- Метрика: total_spent = SUM(Price * Quantity) по клиенту.
-- Подмена: «лояльный» != «много потратил». Один крупный заказ — это «кит»,
-- а не лояльный клиент. В проде — RFM (recency, frequency, monetary),
-- а не голый SUM.
-- Навыки: JOIN · GROUP BY · ORDER BY DESC · LIMIT
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
