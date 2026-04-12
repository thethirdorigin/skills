# test-integration-dir

> Place integration tests in the tests/ directory at the crate root

## Why It Matters

Integration tests in the `tests/` directory compile as separate crates that depend on your library through its public API. This is exactly how downstream consumers use your crate, making integration tests the best way to verify that your public API is ergonomic, complete, and correctly exposed.

Mixing integration tests into `src/` blurs the line between unit and integration testing. Unit tests verify internal logic; integration tests verify the public contract. Keeping them separate ensures both roles are fulfilled.

## Bad

```rust
// src/lib.rs
pub fn create_order(items: &[Item]) -> Result<Order, OrderError> {
    // ...
}

// src/integration_tests.rs  <-- wrong location, compiles as part of the library
#[cfg(test)]
mod integration {
    use super::*;

    #[test]
    fn full_order_workflow() {
        let order = create_order(&[Item::new("widget", 2)]).unwrap();
        assert_eq!(order.status(), Status::Pending);
    }
}
```

## Good

```rust
// tests/order_workflow.rs  <-- separate crate, tests only the public API
use my_crate::{create_order, Item, Status};

#[test]
fn full_order_workflow_creates_pending_order() {
    let order = create_order(&[Item::new("widget", 2)]).unwrap();
    assert_eq!(order.status(), Status::Pending);
}

#[test]
fn empty_order_returns_error() {
    let result = create_order(&[]);
    assert!(result.is_err());
}
```

## See Also

- [test-cfg-module](test-cfg-module.md) - Unit tests belong in the same file
- [test-descriptive-names](test-descriptive-names.md) - Naming conventions for tests
