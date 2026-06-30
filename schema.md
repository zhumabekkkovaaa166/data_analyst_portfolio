# Database schema — Northwind

## Tables

```
Customers ──< Orders >── Employees
                 │   └─< Shippers
                 │
              OrderDetails >── Products ──< Categories
                                   └────────< Suppliers
```

| Table | Key columns |
|---|---|
| `Customers` | CustomerID, CustomerName, ContactName, City, Country |
| `Orders` | OrderID, CustomerID, EmployeeID, ShipperID, OrderDate |
| `OrderDetails` | OrderDetailID, OrderID, ProductID, Quantity |
| `Products` | ProductID, ProductName, CategoryID, SupplierID, Price, Unit |
| `Categories` | CategoryID, CategoryName, Description |
| `Employees` | EmployeeID, FirstName, LastName, BirthDate |
| `Shippers` | ShipperID, ShipperName, Phone |
| `Suppliers` | SupplierID, SupplierName, City, Country |

## Revenue formula

```
total_revenue = SUM(Products.Price * OrderDetails.Quantity)
```

In this Northwind variant the price lives on `Products`, and `OrderDetails` only stores
`Quantity` (there is no per-line UnitPrice). So revenue is always
`SUM(p.Price * od.Quantity)`.

## Dialect notes

| Function | MySQL (playground) | SQLite |
|---|---|---|
| Year/Month | `YEAR(d)`, `MONTH(d)` | `strftime('%Y', d)`, `strftime('%m', d)` |
| Concatenate | `CONCAT(a, ' ', b)` | `a \|\| ' ' \|\| b` |

The `.sql` files use the MySQL-style functions the W3Schools playground accepts. The
Python notebook uses SQLite and therefore the `strftime` / `||` equivalents. This
dialect awareness is intentional.

## How to load the data

Easiest: open the [W3Schools SQL playground](https://www.w3schools.com/sql/trysql.asp) —
Northwind is preloaded. Run any file from `queries/`. For a local copy, the Python script
in `notebooks/` builds a small self-contained demo database so the charts reproduce with
no external download.
