# api-di-hierarchy

> Prefer concrete types > generics > dyn Trait for dependency injection

## Why It Matters

Rust offers three levels of abstraction for dependency injection, each with different trade-offs. Concrete types are the fastest — the compiler inlines everything. Generics monomorphise at compile time, producing specialized code for each type. `dyn Trait` uses vtable-based dynamic dispatch, adding indirection and preventing inlining.

Default to concrete types for internal wiring. Use generics when a library needs to work with caller-provided types. Reserve `dyn Trait` for cases that genuinely require runtime polymorphism — plugin systems, heterogeneous collections, or reducing compile times in large projects.

## Bad

```rust
// Defaulting to dyn Trait everywhere, even for internal dependencies
pub struct OrderService {
    db: Arc<dyn Database>,
    cache: Arc<dyn Cache>,
    logger: Arc<dyn Logger>,
    mailer: Arc<dyn Mailer>,
}

impl OrderService {
    pub fn new(
        db: Arc<dyn Database>,
        cache: Arc<dyn Cache>,
        logger: Arc<dyn Logger>,
        mailer: Arc<dyn Mailer>,
    ) -> Self {
        Self { db, cache, logger, mailer }
    }
}

// Every method call goes through a vtable. No inlining. No devirtualisation.
// Compile times are faster, but runtime is slower and the code is harder to
// navigate (jump-to-definition lands on trait, not implementation).
```

## Good

```rust
// Level 1: Concrete types for internal, known dependencies
pub struct OrderService {
    db: PgPool,
    cache: RedisCache,
    mailer: SmtpMailer,
}

// Level 2: Generics for library code that callers parameterise
pub struct Repository<S: Storage> {
    storage: S,
}

impl<S: Storage> Repository<S> {
    pub fn new(storage: S) -> Self {
        Self { storage }
    }

    pub fn find(&self, id: &str) -> Option<Record> {
        self.storage.get(id)
    }
}

// Level 3: dyn Trait only when runtime polymorphism is required
pub struct PluginHost {
    plugins: Vec<Box<dyn Plugin>>,
}

impl PluginHost {
    pub fn run_all(&self, event: &Event) {
        for plugin in &self.plugins {
            plugin.handle(event);
        }
    }
}
```

## References

- [M-DI-HIERARCHY](https://rust-lang.github.io/api-guidelines/flexibility.html)

## See Also

- [api-object-safe](api-object-safe.md) - Design traits for object safety
- [api-generic-params](api-generic-params.md) - Minimise parameter assumptions
