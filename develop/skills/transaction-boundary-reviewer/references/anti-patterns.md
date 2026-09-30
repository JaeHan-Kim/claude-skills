# Transaction Anti-Patterns and Reference Tables

## ACID
| Property | Means | Violated By |
|----------|-------|-------------|
| Atomicity | All commit or all roll back | Partial writes on failure |
| Consistency | Constraints hold before/after | Bypassed validation; wrong ordering |
| Isolation | Concurrent transactions do not interfere | Missing locks; wrong level |
| Durability | Committed data survives crashes | Missing fsync; premature ack |

## Isolation levels (defaults and anomaly behavior differ by engine; verify against the user's DB)
| Level | Prevents | Allows |
|-------|----------|--------|
| READ UNCOMMITTED | Nothing | Dirty, non-repeatable, phantoms |
| READ COMMITTED | Dirty reads | Non-repeatable, phantoms |
| REPEATABLE READ | Dirty + non-repeatable | Phantoms (engine-dependent) |
| SERIALIZABLE | All anomalies | (retries needed) |

## 1. Overly wide transaction
```java
// Bad — HTTP call inside transaction holds locks
@Transactional
public void processOrder(Order order) {
    orderRepository.save(order);
    paymentGateway.charge(order);  // external HTTP — locks held during this!
}
// Good — database work is atomic; side effects happen after commit
@Transactional
public Order saveOrder(Order order) { return orderRepository.save(order); }
public void processOrder(Order order) {
    Order saved = saveOrder(order);   // transaction commits here (call through another bean; self-invocation bypasses the proxy)
    paymentGateway.charge(saved);       // no locks held
}
```

## 2. Missing rollback on checked exceptions
```java
// Bad — IOException does NOT trigger rollback in Spring by default
@Transactional
public void importData(File file) throws IOException { ... }
// Good — explicit rollback declaration
@Transactional(rollbackFor = IOException.class)
public void importData(File file) throws IOException { ... }
```

## 3. Lost update
```java
// Bad — two threads read balance=100, both deduct 80, both save 20
@Transactional
public void deduct(Long accountId, BigDecimal amount) {
    Account account = accountRepo.findById(accountId).orElseThrow();
    account.setBalance(account.getBalance().subtract(amount));
    accountRepo.save(account);
}
// Good — pessimistic lock (SELECT FOR UPDATE; behavior is engine-dependent) or optimistic @Version
Account account = accountRepo.findByIdWithLock(accountId).orElseThrow();
```

## 4. Cross-service patterns
| Pattern | When |
|---------|------|
| Outbox | Publish events reliably after local commit |
| Saga (choreography) | Long-running, 2-3 services |
| Saga (orchestration) | Multi-step flows needing visibility; 4+ services |
| Two-Phase Commit | Avoid unless strong consistency is required and you control both systems |

## Checklist used to find items (each hit is quoted, not ticked)
- External I/O inside a DB transaction
- N+1 inside a transaction
- `rollbackFor` missing where checked exceptions should roll back
- Read-modify-write without lock or version
- Cross-service write without Outbox/Saga
- Isolation level not tied to a named anomaly
- Transaction boundaries not aligned with domain aggregate boundaries
