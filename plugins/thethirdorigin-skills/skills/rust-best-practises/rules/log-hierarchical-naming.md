# log-hierarchical-naming

> Use hierarchical dot-notation naming for log targets and span names

## Why It Matters

Flat, unnamed log events cannot be filtered granularly. When debugging an order processing issue, you want to see only order-related logs at debug level without drowning in debug output from authentication, caching, and database modules. Hierarchical naming enables this with `RUST_LOG=app::orders=debug`.

Consistent naming conventions also make it easy to configure log levels per module in production: verbose logging for the subsystem under investigation, minimal logging for everything else.

## Bad

```rust
use tracing::info;

fn process_order(order_id: u64) {
    // No target -- cannot be filtered independently
    info!("doing stuff");
    info!("order processed");
}

fn authenticate_user(user_id: &str) {
    // Also no target -- RUST_LOG=debug enables everything
    info!("checking auth");
}

// RUST_LOG=debug floods the console with both order and auth logs.
// No way to see only order processing at debug level.
```

## Good

```rust
use tracing::info;

fn process_order(order_id: u64) {
    info!(
        target: "app.orders.processing",
        order_id = order_id,
        "Processing order"
    );

    info!(
        target: "app.orders.processing",
        order_id = order_id,
        "Order completed"
    );
}

fn authenticate_user(user_id: &str) {
    info!(
        target: "app.auth",
        user_id = %user_id,
        "Authenticating user"
    );
}

// Fine-grained filtering:
// RUST_LOG=app::orders=debug,app::auth=warn
// Shows order debug logs while suppressing auth noise.
```

## See Also

- [log-structured-events](log-structured-events.md) - Structured events with named properties
- [log-otel-conventions](log-otel-conventions.md) - OpenTelemetry naming conventions
