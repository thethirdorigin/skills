# api-service-clone

> Service types use Arc<Inner> internally to provide cheap Clone

## Why It Matters

Service types — database pools, HTTP clients, cache handles — are typically shared across multiple request handlers, background tasks, and middleware layers. Each consumer needs its own handle to the service. If cloning duplicates the internal state (connection pools, buffers, configuration), you pay allocation costs and risk logical inconsistency between copies.

Wrapping the service internals in `Arc<Inner>` makes `Clone` a single atomic reference count increment. All clones share the same underlying resources. This pattern is used extensively in the Rust ecosystem by types like `reqwest::Client`, `sqlx::PgPool`, and `tonic::Channel`.

## Bad

```rust
pub struct AppState {
    db_pool: Pool<Postgres>,
    cache: HashMap<String, CachedValue>,
    config: AppConfig,
    metrics: MetricsRegistry,
}

// Cloning duplicates the entire pool, cache, and metrics — expensive and wrong.
// The cloned pool is a separate pool, not a shared handle.
let state_for_handler = app_state.clone(); // Deep copy of everything
```

## Good

```rust
struct AppStateInner {
    db_pool: Pool<Postgres>,
    cache: DashMap<String, CachedValue>,
    config: AppConfig,
    metrics: MetricsRegistry,
}

#[derive(Clone)]
pub struct AppState {
    inner: Arc<AppStateInner>,
}

impl AppState {
    pub fn new(config: AppConfig, db_pool: Pool<Postgres>) -> Self {
        Self {
            inner: Arc::new(AppStateInner {
                db_pool,
                cache: DashMap::new(),
                config,
                metrics: MetricsRegistry::new(),
            }),
        }
    }

    pub fn db(&self) -> &Pool<Postgres> {
        &self.inner.db_pool
    }

    pub fn config(&self) -> &AppConfig {
        &self.inner.config
    }
}

// Clone is cheap — just an atomic increment:
let state_for_handler = app_state.clone();
tokio::spawn(async move {
    state_for_handler.db().fetch_one("...").await;
});
```

## References

- [M-SERVICES-CLONE](https://rust-lang.github.io/api-guidelines/flexibility.html)

## See Also

- [api-send-sync](api-send-sync.md) - Ensure types are Send + Sync
- [api-private-fields](api-private-fields.md) - Encapsulate internal structure
