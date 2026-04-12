# test-test-util-feature

> Gate test utilities behind a test-util feature flag

## Why It Matters

Shared test helpers -- mock builders, fixture factories, assertion utilities -- are needed by downstream crates when they write integration tests against your library. Putting these helpers behind a `test-util` feature flag makes them available to dependents via `[dev-dependencies] mycrate = { features = ["test-util"] }` while keeping them out of production builds.

Without a feature flag, test utilities either ship to production (wasting binary size and exposing internal details) or live in a separate `mycrate-test-utils` crate (adding maintenance overhead and version synchronisation burden).

## Bad

```rust
// src/lib.rs -- test helpers compiled into every production build
pub mod testing {
    use super::*;

    pub fn mock_config() -> Config {
        Config {
            database_url: "postgres://test:test@localhost/test".into(),
            max_connections: 5,
            timeout: Duration::from_secs(1),
        }
    }

    pub fn mock_user() -> User {
        User { id: 1, name: "Test User".into(), email: "test@example.com".into() }
    }
}
```

## Good

```rust
// Cargo.toml
// [features]
// test-util = []

// src/lib.rs
#[cfg(feature = "test-util")]
pub mod testing {
    use super::*;

    /// Create a `Config` with sensible test defaults.
    pub fn mock_config() -> Config {
        Config {
            database_url: "postgres://test:test@localhost/test".into(),
            max_connections: 5,
            timeout: Duration::from_secs(1),
        }
    }

    /// Create a `User` fixture with default values.
    pub fn mock_user() -> User {
        User { id: 1, name: "Test User".into(), email: "test@example.com".into() }
    }
}

// Downstream crate's Cargo.toml:
// [dev-dependencies]
// mycrate = { path = "../mycrate", features = ["test-util"] }

// Downstream crate's test:
// use mycrate::testing::mock_config;
```

## References

- [M-TEST-UTIL](https://rust-lang.github.io/api-guidelines/future-proofing.html)

## See Also

- [test-mockable-design](test-mockable-design.md) - Design for testability with traits
- [crate-features-additive](crate-features-additive.md) - Features must be additive
