# crate-avoid-statics

> Avoid module-level statics where consistent view matters for correctness

## Why It Matters

Module-level statics with lazy initialisation (via `OnceLock`, `LazyLock`, or the `lazy_static` crate) create hidden global state with non-deterministic initialisation order. Different code paths may observe different states depending on which path triggers the initialisation first. In tests, statics persist across test cases, causing mysterious order-dependent failures.

Passing configuration and shared resources through constructors or function parameters makes dependencies explicit, enables testing with different configurations, and eliminates initialisation-order bugs.

## Bad

```rust
use std::sync::LazyLock;

static CONFIG: LazyLock<Config> = LazyLock::new(|| {
    // Which config file gets loaded depends on which code path
    // triggers this initialisation first. Tests cannot override it.
    Config::from_file("config.toml").expect("config must exist")
});

static DB_POOL: LazyLock<PgPool> = LazyLock::new(|| {
    // If CONFIG hasn't been initialised yet, this triggers it.
    // Initialisation order depends on call sequence.
    PgPool::connect(&CONFIG.database_url).expect("db must connect")
});

pub fn get_user(id: u64) -> Result<User, Error> {
    // Implicitly depends on global state -- untestable with different configs
    let conn = DB_POOL.get()?;
    conn.query_one("SELECT * FROM users WHERE id = $1", &[&id])
}
```

## Good

```rust
pub struct AppState {
    pub config: Config,
    pub db_pool: PgPool,
}

impl AppState {
    pub async fn new(config: Config) -> Result<Self, Error> {
        let db_pool = PgPool::connect(&config.database_url).await?;
        Ok(Self { config, db_pool })
    }
}

pub fn get_user(pool: &PgPool, id: u64) -> Result<User, Error> {
    // Explicit dependency -- testable with any pool
    let conn = pool.get()?;
    conn.query_one("SELECT * FROM users WHERE id = $1", &[&id])
}

// In tests:
#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn get_user_returns_expected_user() {
        let pool = setup_test_db().await;
        let user = get_user(&pool, 1).unwrap();
        assert_eq!(user.name, "Alice");
    }
}
```

## References

- [M-AVOID-STATICS](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [test-mockable-design](test-mockable-design.md) - Design for testability with traits
- [anti-primitive-obsession](anti-primitive-obsession.md) - Use domain types over primitives
