# Common Mistakes and Fixes

| Mistake | Fix |
|---------|-----|
| Technical names instead of domain language | Rename to domain terms: `ClaimAdjudicator`, `PolicyUnderwriter`; flag `Manager`, `Helper`, `Processor`, `Utils` |
| One model to rule them all | Define bounded contexts; each gets its own model |
| Giant aggregates | Keep aggregates small; reference by ID; accept eventual consistency |
| Anemic domain model (all logic in services) | Move behavior into entities and value objects |
| No Anti-Corruption Layer at integration points | Wrap every external system behind a translation layer |

## Diagnostic: if No

| Question | If No | Action |
|----------|-------|--------|
| Can a domain expert read your class names? | Technical jargon instead of domain language | Rename to ubiquitous language |
| Are bounded context boundaries explicitly defined? | Models bleed across boundaries | Draw a context map; define translation strategies |
| Are aggregates small (one root + minimal cluster)? | Aggregates are large and slow | Break into smaller aggregates; reference by ID |
| Do domain objects contain behavior? | Anemic model | Move business rules into entities and value objects |
| Is there an Anti-Corruption Layer at every external integration? | Foreign models pollute your domain | Add a translation layer at each boundary |
