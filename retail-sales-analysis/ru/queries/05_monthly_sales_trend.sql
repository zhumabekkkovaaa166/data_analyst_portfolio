-- ============================================================
-- Задание 5 — Месячный тренд продаж                    [функции дат]
-- ------------------------------------------------------------
-- Бизнес-вопрос: директор хочет видеть, как менялись продажи за год,
-- чтобы поймать сезонность для планирования.
-- Метрика: revenue = SUM(Price * Quantity) по (году, месяцу).
-- Ключ: группировать по году И месяцу вместе. Только по месяцу — январи
-- разных лет схлопнутся, тренд год-к-году пропадёт. Хронологический
-- ORDER BY делает сезонную волну читаемой.
--
-- Про диалект: YEAR()/MONTH() — стиль MySQL. В SQLite используйте
--   strftime('%Y', o.OrderDate), strftime('%m', o.OrderDate).
-- Навыки: JOIN · YEAR() · MONTH() · GROUP BY
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
