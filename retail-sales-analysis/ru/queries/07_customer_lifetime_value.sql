-- ============================================================
-- Финал — Customer Lifetime Value (упрощённый)         [сегментация CASE WHEN]
-- ------------------------------------------------------------
-- Бизнес-вопрос: посчитать CLV каждого клиента, разбить на сегменты
-- High / Medium / Low и построить маркетинговую стратегию.
-- Метрика: revenue по клиенту + категориальная метка `segment`.
-- Две подмены:
--   1) Это ИСТОРИЧЕСКИЙ доход, не прогнозный CLV. Настоящий CLV — прогноз
--      будущей ценности с учётом оттока.
--   2) Пороги 10000 / 5000 — круглые числа с потолка. Зрелее задавать
--      границы по КВАНТИЛЯМ (топ-20% = High через ntile(5)), устойчиво
--      к росту и инфляции.
-- Навыки: JOIN · GROUP BY · SUM · CASE WHEN · ORDER BY
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
