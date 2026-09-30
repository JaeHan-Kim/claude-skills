# Pool Config Catalog

## Sizing starting point (PostgreSQL-oriented heuristic, not a law)
```
pool_size = (core_count * 2) + effective_spindle_count
```
`core_count` = DB server cores; `effective_spindle_count` = 1 for SSD, 0 if data fits in RAM.
Example only: 4-core SSD -> 9 -> 10. Use the user's real specs; never assume this example.

## HikariCP properties (Spring Boot)
```properties
# application.properties (Spring Boot)
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.connection-timeout=30000       # ms: max wait for a pool connection
spring.datasource.hikari.idle-timeout=600000            # ms: idle connections live 10 min
spring.datasource.hikari.max-lifetime=1800000           # ms: max connection lifetime 30 min; keep shorter than firewall/DB timeout
spring.datasource.hikari.keepalive-time=60000           # ms: ping to survive firewall NAT
spring.datasource.hikari.leak-detection-threshold=<2x P99 query time, ms>   # ms: warn if connection held > that; user's P99 [확인 필요] (60000 is only an example)
```

## pgBouncer modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `transaction` | Returned after each transaction | Most web applications |
| `session` | Held for whole client session | Temp tables, advisory locks, prepared statements |
| `statement` | Returned after each statement | Avoid: breaks multi-statement transactions |

## Common Mistakes
- Pool size equals thread count: threads spend most time not waiting on the database
- `minimumIdle` far below `maximumPoolSize`: connections created under load, when latency is critical
- `maxLifetime` not shorter than firewall timeout: silent TCP drops cause cryptic errors on first query
- Leak detection disabled in production: one missing `close()` eventually exhausts the pool
- One pool for OLTP and reporting: separate OLTP (short queries) from reporting (long queries)
