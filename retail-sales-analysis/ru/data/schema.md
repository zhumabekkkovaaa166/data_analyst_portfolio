# Схема базы данных — Northwind

## Таблицы

```
Customers ──< Orders >── Employees
                 │   └─< Shippers
                 │
              OrderDetails >── Products ──< Categories
                                   └────────< Suppliers
```

| Таблица | Ключевые поля |
|---|---|
| `Customers` | CustomerID, CustomerName, ContactName, City, Country |
| `Orders` | OrderID, CustomerID, EmployeeID, ShipperID, OrderDate |
| `OrderDetails` | OrderDetailID, OrderID, ProductID, Quantity |
| `Products` | ProductID, ProductName, CategoryID, SupplierID, Price, Unit |
| `Categories` | CategoryID, CategoryName, Description |
| `Employees` | EmployeeID, FirstName, LastName, BirthDate |
| `Shippers` | ShipperID, ShipperName, Phone |
| `Suppliers` | SupplierID, SupplierName, City, Country |

## Формула выручки

```
total_revenue = SUM(Products.Price * OrderDetails.Quantity)
```

В этом варианте Northwind цена хранится в `Products`, а `OrderDetails` содержит только
`Quantity` (без построчной цены). Поэтому выручка всегда `SUM(p.Price * od.Quantity)`.

## Нюансы диалектов

| Функция | MySQL (плейграунд) | SQLite |
|---|---|---|
| Год/Месяц | `YEAR(d)`, `MONTH(d)` | `strftime('%Y', d)`, `strftime('%m', d)` |
| Конкатенация | `CONCAT(a, ' ', b)` | `a \|\| ' ' \|\| b` |

В `.sql`-файлах используются функции в стиле MySQL, которые принимает плейграунд
W3Schools. Ноутбук на Python работает с SQLite и потому использует эквиваленты
`strftime` / `||`. Различие диалектов — намеренное.

## Как загрузить данные

Проще всего: открыть [плейграунд W3Schools](https://www.w3schools.com/sql/trysql.asp) —
Northwind уже загружен. Запускайте любой файл из `queries/`. Для локальной копии скрипт
в `notebooks/` собирает небольшую самодостаточную демо-базу, чтобы графики
воспроизводились без внешней загрузки.
