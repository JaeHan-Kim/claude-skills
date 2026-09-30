# SQL Quick-Reference Examples

## CTE Pattern
```sql
WITH ranked_orders AS (
    SELECT customer_id, order_id, total_amount,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM orders
    WHERE status = 'completed'
)
SELECT customer_id, order_id, total_amount
FROM ranked_orders
WHERE rn = 1;  -- latest completed order per customer
```

## Window Function Pattern
```sql
SELECT department_id, employee_id, salary,
       SUM(salary) OVER (PARTITION BY department_id ORDER BY hire_date) AS running_payroll,
       RANK()      OVER (PARTITION BY department_id ORDER BY salary DESC) AS salary_rank
FROM employees;
```

## Before / After
```sql
-- BEFORE: correlated subquery, one execution per row
SELECT order_id,
       (SELECT SUM(quantity) FROM order_items oi WHERE oi.order_id = o.id) AS item_count
FROM orders o;

-- AFTER: single aggregation join
SELECT o.order_id, COALESCE(agg.item_count, 0) AS item_count
FROM orders o
LEFT JOIN (SELECT order_id, SUM(quantity) AS item_count FROM order_items GROUP BY order_id) agg
       ON agg.order_id = o.id;
```

Speed of the AFTER form is a hypothesis until the user's EXPLAIN ANALYZE before/after says so.

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Query Patterns | `query-patterns.md` | JOINs, CTEs, subqueries, recursive queries |
| Window Functions | `window-functions.md` | ROW_NUMBER, RANK, LAG/LEAD, analytics |
| Optimization | `optimization.md` | EXPLAIN plans, indexes, statistics |
| Database Design | `database-design.md` | Normalization, keys, constraints |
| Dialect Differences | `dialect-differences.md` | PostgreSQL vs MySQL vs SQL Server |
