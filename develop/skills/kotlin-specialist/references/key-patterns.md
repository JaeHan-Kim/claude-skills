# Kotlin Key Patterns and Constraints (moved from SKILL.md)

## Key Patterns

### Sealed Class State Modeling

```kotlin
sealed class UiState<out T> {
    data object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String, val cause: Throwable? = null) : UiState<Nothing>()
}
```

### Coroutines & Flow (Structured Concurrency)

```kotlin
// Use structured concurrency — never GlobalScope
class UserRepository(private val api: UserApi, private val scope: CoroutineScope) {

    fun userUpdates(id: String): Flow<UiState<User>> = flow {
        emit(UiState.Loading)
        try {
            emit(UiState.Success(api.fetchUser(id)))
        } catch (e: IOException) {
            emit(UiState.Error("Network error", e))
        }
    }.flowOn(Dispatchers.IO)
}
```

### Null Safety

```kotlin
// Prefer safe calls and elvis operator
val displayName = user?.profile?.name ?: "Anonymous"

// !! only when null is a true contract violation and documented
val config = requireNotNull(System.getenv("APP_CONFIG")) { "APP_CONFIG must be set" }
```

## Constraints

**MUST DO:**
- Use null safety (`?`, `?.`, `?:`) — use `!!` only with documented justification
- Prefer `sealed class` for state modeling
- Use `suspend` functions for async operations
- Use `Flow` for reactive streams
- Verify coroutine cancellation on teardown
- Run `detekt` and `ktlint` before committing

**MUST NOT DO:**
- Use `runBlocking` in production code
- Use `!!` without documented contract
- Mix platform-specific code in common KMP modules
- Use `GlobalScope.launch` (use structured concurrency)
- Create memory leaks with coroutine scopes

