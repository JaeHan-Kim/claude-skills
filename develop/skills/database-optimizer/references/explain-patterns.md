# EXPLAIN Output — Key Patterns

Illustrative only. Never state a row as a diagnosis without the user's own numbers.

| Pattern | Symptom | Typical Remedy |
|---------|---------|----------------|
| `Seq Scan` on large table | No filter selectivity | B-tree index on filter column |
| `Nested Loop` with large outer set | Row growth | Hash Join; index inner join key |
| `cost=... rows=1` but actual rows=50000 | Stale statistics | `ANALYZE <table>` |
| `Buffers: hit=10 read=90000` | Low cache hit rate | Larger `shared_buffers`; covering index |
| `Sort Method: external merge` | Sort spilling to disk | Raise `work_mem` for the session |

```sql
-- Always use BUFFERS to see cache hit vs. disk read ratio
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT o.id, c.name
FROM   orders o
JOIN   customers c ON c.id = o.customer_id
WHERE  o.status = 'pending'
  AND  o.created_at > now() - interval '7 days';
```
(EXPLAIN ANALYZE executes the statement; for INSERT/UPDATE/DELETE run inside a rolled-back transaction on a copy.)

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Query Optimization | `query-optimization.md` | Slow queries, plan analysis |
| Index Design | `index-design-patterns.md` | B-tree, covering, partial, expression |
| PostgreSQL Memory & WAL | `postgresql-memory-wal.md` | shared_buffers, work_mem, WAL |
| PostgreSQL VACUUM & Locking | `postgresql-vacuum-locking.md` | VACUUM, lock management |
| MySQL Memory & I/O | `mysql-memory-io.md` | InnoDB memory, I/O |
| PostgreSQL Monitoring | `monitoring-postgresql.md` | pg_stat_statements, locks |
| MySQL Monitoring | `monitoring-mysql.md` | Performance schema, InnoDB status |
