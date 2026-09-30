# Test Master — quick-start example and rules

A minimal Jest unit test illustrating the key patterns this skill enforces:

```js
// Good: meaningful description, specific assertion, isolated dependency
describe('calculateDiscount', () => {
  it('applies 10% discount for premium users', () => {
    const result = calculateDiscount({ price: 100, userTier: 'premium' });
    expect(result).toBe(90); // specific outcome, not just truthy
  });

  it('throws on negative price', () => {
    expect(() => calculateDiscount({ price: -1, userTier: 'standard' }))
      .toThrow('Price must be non-negative');
  });
});
```

Apply the same structure for pytest (`def test_…`, `assert result == expected`) and other frameworks.

## MUST DO

- Test happy paths AND error/edge cases (empty input, null, boundary values)
- Mock external dependencies — never call real APIs or databases in unit tests
- Use meaningful `it('…')` descriptions that read as plain-English specifications
- Assert specific outcomes (`expect(result).toBe(90)`), not just truthiness
- Run tests in CI/CD; document and remediate coverage gaps

## MUST NOT

- Skip error-path testing (do not test only the success branch of a try/catch)
- Use production data in tests — use fixtures or factories instead
- Create order-dependent tests — each test must be independently runnable
- Ignore flaky tests — quarantine and fix them; do not re-run until green
- Test implementation details (internal method calls) — test observable behaviour

## Report sections (Output Template detail)

1. Test scope and approach
2. Test cases with expected outcomes
3. Coverage analysis
4. Findings with severity (Critical/High/Medium/Low)
5. Specific fix recommendations
