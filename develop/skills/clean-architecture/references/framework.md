# Clean Architecture Framework (moved from SKILL.md)

## The Clean Architecture Framework

### 1. Dependency Rule and Concentric Circles

Source code dependencies always point inward. Nothing in an inner circle can know anything about an outer circle.

| Context | Pattern | Example |
|---------|---------|---------|
| Layer direction | Inner circles define interfaces; outer circles implement them | `UserRepository` interface in Use Cases; `PostgresUserRepository` in Adapters |
| Data crossing | DTOs or simple structs cross boundaries, not ORM entities | Use Case returns `UserResponse` DTO, not an ActiveRecord model |
| Framework isolation | Wrap framework calls behind interfaces | `EmailSender` interface hides whether you use SendGrid or SES |
| Database independence | Repository pattern abstracts persistence | Business logic calls `repo.save(user)`, never raw SQL |

See: [dependency-rule.md](dependency-rule.md)

### 2. Entities and Use Cases

- **Entities** encapsulate enterprise-wide business rules; no framework dependencies
- **Use Cases** contain application-specific rules; orchestrate Entities; accept Request Models and return Response Models

| Context | Pattern | Example |
|---------|---------|---------|
| Entity design | Encapsulate rules with no framework dependencies | `Order.calculateTotal()` knows nothing about HTTP |
| Use Case boundary | Define Input Port and Output Port interfaces | `CreateOrderInput` interface; `CreateOrderOutput` interface |
| Request/Response | Simple data structures cross the boundary | `CreateOrderRequest { items, customerId }` — no ORM models |
| Single responsibility | One Use Case per application operation | `PlaceOrder`, `CancelOrder`, `RefundOrder` as separate classes |

See: [entities-use-cases.md](entities-use-cases.md)

### 3. Interface Adapters and Frameworks

Interface Adapters convert data between Use Cases and external agencies. Frameworks belong in the outermost circle.

| Context | Pattern | Example |
|---------|---------|---------|
| Controller | Translates delivery mechanism to Use Case input | `OrderController.create(req)` builds `CreateOrderRequest` |
| Presenter | Translates Use Case output to view model | `OrderPresenter.present(response)` formats data for JSON |
| Gateway | Implements repository interface using a specific DB | `SqlOrderRepository implements OrderRepository` |
| Plugin architecture | Main component wires dependencies at startup | `main()` instantiates concrete classes and injects them |

See: [adapters-frameworks.md](adapters-frameworks.md)

### 4. Component Principles

- **REP**: classes in a component should be releasable together
- **CCP**: classes that change for the same reason belong in the same component
- **ADP**: no cycles in the component dependency graph
- **SDP**: depend in the direction of stability

See: [component-principles.md](component-principles.md)

### 5. SOLID Principles

| Principle | Core Rule | Common Violation |
|-----------|-----------|-----------------|
| SRP | One reason to change | `Employee` handles pay, reporting, and persistence |
| OCP | Extend by adding new code, not modifying existing | Adding `if` branches for new types |
| LSP | Subtypes usable through base type | `Square extends Rectangle` breaks `setWidth()` contract |
| ISP | Don't force clients to depend on unused methods | Fat interface forces importing unneeded methods |
| DIP | High-level modules depend on abstractions | `OrderService` imports `StripeClient` directly |

See: [solid-principles.md](solid-principles.md)

### 6. Boundaries and Boundary Anatomy

- **Full boundary**: reciprocal interfaces on both sides (Input Port + Output Port)
- **Partial boundary**: strategy or facade pattern
- **Humble Object**: split behavior at a boundary — testable logic separate from hard-to-test infrastructure

See: [boundaries.md](boundaries.md)

## Quick Diagnostic

| Question | If No | Action |
|----------|-------|--------|
| Can you test business rules without a database or web server? | Business rules coupled to infrastructure | Extract entities and use cases behind interfaces |
| Do source code dependencies point inward on every import? | Dependency Rule violated | Introduce interfaces; invert the offending dependency |
| Can you swap the database without changing business logic? | Persistence leaking inward | Implement Repository pattern |
| Are Use Cases independent of the delivery mechanism? | Use Cases know about HTTP | Remove delivery-specific types; use plain DTOs |
| Is the framework confined to the outermost circle? | Framework is your architecture | Wrap framework calls behind interfaces |

