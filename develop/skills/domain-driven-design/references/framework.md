# Framework Catalog

Moved out of SKILL.md. Load the section that matches the step you are on.

## Framework (six parts)

### 1. Ubiquitous Language

A shared, rigorous language between developers and domain experts used consistently in conversation, documentation, and code.

| Context | Pattern | Example |
|---------|---------|---------|
| Class naming | Name classes after domain concepts | `LoanApplication`, not `RequestHandler` |
| Method naming | Use verbs the business uses | `policy.underwrite()`, not `policy.process()` |
| Event naming | Past-tense domain actions | `ClaimSubmitted`, not `DataSaved` |
| Module structure | Organize by domain concept | `shipping/`, `billing/`, not `controllers/`, `services/` |
| Code review | Reject technical-only names | Flag `Manager`, `Helper`, `Processor`, `Utils` as naming smells |

See: [references/ubiquitous-language.md](references/ubiquitous-language.md)

### 2. Bounded Contexts and Context Mapping

A bounded context is an explicit boundary within which a particular domain model is defined and applicable.

| Context | Pattern | Example |
|---------|---------|---------|
| Service integration | Anti-Corruption Layer | Translate external API responses into your domain objects at the boundary |
| Team collaboration | Shared Kernel | Two teams co-own a small `Money` value object library |
| Legacy migration | Conformist / ACL | Wrap legacy system behind an adapter that speaks your domain language |
| API design | Open Host Service + Published Language | Expose a well-documented REST API with a canonical schema |
| Module boundaries | Separate packages per context | `myapp.shipping` and `myapp.billing` with explicit translation |

See: [references/bounded-contexts.md](references/bounded-contexts.md)

### 3. Entities, Value Objects, and Aggregates

- **Entity**: identity persists across state changes ("same person even if name changes")
- **Value Object**: defined entirely by attributes; immutable ("$10 bill is interchangeable")
- **Aggregate Root**: single entry point enforcing consistency; reference other aggregates by ID only

| Context | Pattern | Example |
|---------|---------|---------|
| Identity tracking | Entity with ID | `Order` identified by `orderId`, survives state changes |
| Immutable attributes | Value Object | `Address(street, city, zip)` — replace, never mutate |
| Consistency boundary | Aggregate Root | `Order` is root; `OrderLine` items exist only through it |
| Cross-aggregate reference | Reference by ID | `Order` stores `customerId`, not a `Customer` object |

See: [references/building-blocks.md](references/building-blocks.md)

### 4. Domain Events

Domain events capture something that happened in the domain that domain experts care about — named in past tense.

| Context | Pattern | Example |
|---------|---------|---------|
| State transitions | Raise event on domain action | `order.place()` raises `OrderPlaced` event |
| Cross-context integration | Publish integration event | `OrderPlaced` triggers `ShippingLabelRequested` in shipping context |
| Audit trail | Store events as history | Event log: `OrderPlaced` → `PaymentReceived` → `OrderShipped` |
| Eventual consistency | Async event handlers | `InventoryReserved` handler updates stock asynchronously |

See: [references/domain-events.md](references/domain-events.md)

### 5. Repositories and Factories

- **Repository**: provides the illusion of an in-memory collection; hides persistence details
- **Factory**: encapsulates complex object creation; ensures aggregates are always created in valid state

| Context | Pattern | Example |
|---------|---------|---------|
| Data access abstraction | Repository interface | `OrderRepository.findByCustomer(customerId)` in domain layer |
| Complex creation | Factory method | `Order.createFromQuote(quote)` validates and assembles |
| Query encapsulation | Specification | `spec = OverdueBy(days=30); repo.findMatching(spec)` |
| Ports and adapters | Interface in domain, impl in infra | `interface OrderRepository` in domain; `PostgresOrderRepository` in infrastructure |

See: [references/repositories-factories.md](references/repositories-factories.md)

### 6. Strategic Design and Distillation

- **Core Domain**: competitive advantage; invest best developers and deepest modeling here
- **Supporting Subdomain**: necessary but not differentiating; build it, don't over-engineer
- **Generic Subdomain**: commodity; buy or use open-source

| Context | Pattern | Example |
|---------|---------|---------|
| Build vs. buy | Classify subdomain type | Build custom pricing engine (core); use Stripe for payments (generic) |
| Code organization | Separate core from generic | `domain/pricing/` (deep model) vs. `infrastructure/email/` (thin adapter) |

See: [references/strategic-design.md](references/strategic-design.md)


## Earlier scope table

| Use | Skip |
|-----|------|
| Aligning code structure with business concepts | Architecture layering (use clean-architecture) |
| Defining service boundaries from domain analysis | Service coupling validation (use service-boundary-validator) |
| Domain experts and developers speak different languages | Simple CRUD apps without complex business rules |
| Identifying core domain vs. generic subdomains | |
