# Event Storming Catalog

Moved out of SKILL.md. Sticky legend, mistakes, facilitation checklist, level flow.

## Sticky Legend

| Color | Type | Naming Convention |
|-------|------|-------------------|
| Orange | Domain Event | Past tense: "Order Placed", "Payment Failed" |
| Blue | Command | Imperative: "Place Order", "Cancel Shipment" |
| Yellow | Actor / User | Role: "Customer", "Warehouse Clerk" |
| Lilac | Policy / Business Rule | "Whenever X, then Y" |
| Pink | Read Model / View | What the actor sees to decide |
| White | External System | Third-party name: "Stripe", "FedEx API" |
| White (wide) | Aggregate | Noun owning state and enforcing invariants |
| Red | Hotspot | Question or conflict — mark and move on |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Events named as nouns ("Order") | Enforce past-tense verbs: "Order Placed" |
| Only developers in the room | Require domain experts — they are the primary source |
| Skipping hotspots | Mark every disagreement; resolve after the session |
| Jumping to aggregates before events | Complete Level 1 and 2 before Level 3 |
| One person controlling the wall | Distribute stickies physically; anyone can place any sticky |

## Facilitation Checklist

- [ ] Diverse participants: domain experts equal or outnumber developers
- [ ] Timer set per phase
- [ ] Red hotspot stickies available to everyone
- [ ] Photography or digital export taken at end of each phase
- [ ] Follow-up scheduled for hotspot resolution


## Level 2 reading flow

Reading flow (left to right):
```
[Read Model] → [Actor] → [Command] → [Policy] → [Domain Event]
```

## Earlier output template

## Output Template

After the workshop, document each bounded context:

```
Bounded Context: [Name]
Ubiquitous Language: [key terms and their definitions]
Commands: [list of commands handled]
Domain Events: [list of events emitted]
Integration Events (published): [events other contexts listen to]
Aggregates: [name, invariants, state transitions]
External Dependencies: [other contexts or systems consumed]
Hotspots Remaining: [open questions]
```

## Earlier scope

## When to Use / When Not to Use

**Use when:**
- Starting a new product and need to discover bounded contexts
- Auditing or untangling a legacy system
- Aligning engineers with domain experts before writing code
- Asking "where should our service boundaries be?"

**Do not use when:**
- You need implementation code — run Event Storming first, then use `microservices-architect` or `spring-boot-engineer`
- The domain is already well-modeled and stable
