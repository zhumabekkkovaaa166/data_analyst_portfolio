-- ============================================================
-- Задание 3 — Самые продаваемые товары                 [агрегация в штуках]
-- ------------------------------------------------------------
-- Бизнес-вопрос: закуп хочет топ-10 самых востребованных товаров,
-- чтобы пополнить их склад в первую очередь.
-- Метрика: total_quantity_sold = SUM(Quantity) по товару.
-- Ключ: ШТУКИ, не выручка. SQL почти как в задании 2, но решение про склад
-- измеряется в единицах. Revenue вывел бы один дорогой малопродаваемый
-- товар и сбил бы пополнение.
-- Навыки: JOIN · GROUP BY · ORDER BY DESC · LIMIT
-- ============================================================
SELECT
    p.ProductName       AS product_name,
    SUM(od.Quantity)    AS total_quantity_sold
FROM Products p
JOIN OrderDetails od ON od.ProductID = p.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY total_quantity_sold DESC
LIMIT 10;
