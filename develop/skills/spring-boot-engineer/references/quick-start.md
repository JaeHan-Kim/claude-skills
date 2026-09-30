# Spring Boot Quick Start and Constraints (moved from SKILL.md)

## Quick Start — Minimal Working Structure

### Entity
```java
@Entity
@Table(name = "products")
public class Product {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @NotBlank private String name;
    @DecimalMin("0.0") private BigDecimal price;
}
```

### Repository
```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    List<Product> findByNameContainingIgnoreCase(String name);
}
```

### Service (constructor injection)
```java
@Service
public class ProductService {
    private final ProductRepository repo;
    public ProductService(ProductRepository repo) { this.repo = repo; }

    @Transactional(readOnly = true)
    public List<Product> search(String name) {
        return repo.findByNameContainingIgnoreCase(name);
    }
}
```

### REST Controller
```java
@RestController
@RequestMapping("/api/v1/products")
@Validated
public class ProductController {
    private final ProductService service;
    public ProductController(ProductService service) { this.service = service; }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Product create(@Valid @RequestBody ProductRequest request) {
        return service.create(request);
    }
}
```

### DTO (record)
```java
public record ProductRequest(
    @NotBlank String name,
    @DecimalMin("0.0") BigDecimal price
) {}
```

## Constraints

**MUST DO:**

| Rule | Correct Pattern |
|------|----------------|
| Constructor injection | `public MyService(Dep dep) { this.dep = dep; }` |
| Validate API input | `@Valid @RequestBody` on every mutating endpoint |
| Type-safe config | `@ConfigurationProperties(prefix = "app")` |
| Transaction scope | `@Transactional` on multi-step writes; `readOnly = true` on reads |
| Externalize secrets | Environment variables or Spring Cloud Config — never in `application.properties` |

**MUST NOT DO:**
- Field injection (`@Autowired` on fields)
- Skip input validation on API endpoints
- Mix blocking and reactive code (no `.block()` inside WebFlux chains)
- Use deprecated Spring Boot 2.x patterns (e.g., `WebSecurityConfigurerAdapter`)

