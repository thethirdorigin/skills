# api-send-sync

> Public types should be Send where possible

## Why It Matters

In modern Rust applications, async runtimes like Tokio require futures and the values they capture to be Send. A public type that is not Send cannot be held across .await points, passed to tokio::spawn, or shared between threads. This severely limits composability and forces callers into single-threaded architectures.

The most common causes of non-Send types are Rc (use Arc instead) and Cell/RefCell (use Mutex or RwLock instead). Making types Send by default costs little and prevents painful refactoring when callers need concurrency.

## Bad

```rust
use std::cell::RefCell;
use std::rc::Rc;

pub struct ConnectionPool {
    connections: Rc<RefCell<Vec<Connection>>>,
}

// This type is neither Send nor Sync.
// Callers cannot use it with tokio::spawn:
//   tokio::spawn(async move {
//       pool.get().await;  // ERROR: `Rc<RefCell<...>>` cannot be sent between threads
//   });
```

## Good

```rust
use std::sync::{Arc, Mutex};

pub struct ConnectionPool {
    connections: Arc<Mutex<Vec<Connection>>>,
}

// Now Send + Sync. Works freely across async tasks:
//   let pool = pool.clone();
//   tokio::spawn(async move {
//       pool.get().await;  // OK
//   });
```

## References

- [C-SEND-SYNC](https://rust-lang.github.io/api-guidelines/interoperability.html#types-are-send-and-sync-where-possible-c-send-sync)
- [M-TYPES-SEND](https://rust-lang.github.io/api-guidelines/interoperability.html)

## See Also

- [api-service-clone](api-service-clone.md) - Cheap Clone for service types via Arc
