# err-match-existing

> Match existing error conversion patterns in the codebase

## Why It Matters

Most Rust projects establish a convention for error handling early on: thiserror with #[from], manual From impls, anyhow in binaries, or a project-specific error macro. When a new contributor introduces a different pattern — say, manual match-and-rewrap in a codebase that uses #[from] everywhere — it creates inconsistency that confuses future readers.

Before writing a new error type, scan the existing code. Look for From impls, thiserror derives, error module conventions, and how context is attached. Follow the established pattern. If the existing pattern is genuinely inadequate, propose the change as a deliberate refactor rather than silently diverging.

## Bad

```rust
// Existing codebase uses thiserror with #[from]:
// #[derive(Debug, thiserror::Error)]
// pub enum DbError {
//     #[error("query failed")]
//     Query(#[from] sqlx::Error),
// }

// New code ignores the pattern and hand-rolls conversion:
#[derive(Debug)]
pub enum CacheError {
    Redis(redis::RedisError),
}

impl From<redis::RedisError> for CacheError {
    fn from(err: redis::RedisError) -> Self {
        CacheError::Redis(err)
    }
}

impl std::fmt::Display for CacheError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            CacheError::Redis(e) => write!(f, "redis error: {e}"),
        }
    }
}

impl std::error::Error for CacheError {}
```

## Good

```rust
// Follow the same thiserror + #[from] pattern used throughout the project:
#[derive(Debug, thiserror::Error)]
pub enum CacheError {
    #[error("redis operation failed")]
    Redis(#[from] redis::RedisError),

    #[error("serialization failed for key {key}")]
    Serialize {
        key: String,
        #[source]
        source: serde_json::Error,
    },
}
```

## See Also

- [err-canonical-structs](err-canonical-structs.md) - Designing error types from scratch
- [err-anyhow-app](err-anyhow-app.md) - Choosing between typed and erased errors
