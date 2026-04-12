# api-compose-structs

> Decompose large structs into smaller composed structs to enable partial borrowing

## Why It Matters

Rust's borrow checker operates at the struct level when fields are accessed through methods. A monolithic struct with many fields forces full `&mut self` borrows, blocking concurrent access to independent groups of fields. Even if you only need to mutate one field, calling `&mut self` on a method locks the entire struct, preventing any other borrow for its lifetime.

Splitting a large struct into composed sub-structs lets each group be borrowed independently. When `App` contains `state: AppState` and `io: AppIo`, you can pass `&mut self.state` to one function and `&self.io` to another simultaneously -- something impossible with a flat struct accessed through methods. This pattern also improves code organization by grouping related fields, making the struct hierarchy a map of your domain.

## Bad

```rust
struct OrderService {
    config: ServiceConfig,
    cache: OrderCache,
    db: DatabasePool,
    logger: Logger,
    metrics: MetricsRecorder,
    rate_limiter: RateLimiter,
}

impl OrderService {
    fn process_order(&mut self, order: &Order) -> Result<Receipt> {
        // Borrowing self.rate_limiter mutably locks the entire OrderService
        self.rate_limiter.check(order.customer_id)?;

        // Cannot borrow self.db here -- self is already mutably borrowed above
        // if rate_limiter.check took &mut self as part of OrderService
        let balance = self.db.query_balance(order.customer_id)?;

        // Every field access goes through the monolithic struct
        self.metrics.record("order.processed", 1);
        self.cache.invalidate(order.id);
        self.logger.info(&format!("Processed order {}", order.id));

        Ok(Receipt::new(order.id))
    }

    // Every method that touches any field must take &mut self,
    // even if it only needs one or two fields. This prevents
    // callers from holding any other reference to the struct.
    fn refresh_cache(&mut self) -> Result<()> {
        let orders = self.db.query_recent_orders()?;
        self.cache.warm(orders);
        self.metrics.record("cache.refreshed", 1);
        Ok(())
    }
}
```

## Good

```rust
/// Groups fields that represent application state and business logic.
struct OrderState {
    cache: OrderCache,
    rate_limiter: RateLimiter,
}

/// Groups fields that handle I/O and external communication.
struct OrderIo {
    db: DatabasePool,
    logger: Logger,
    metrics: MetricsRecorder,
}

struct OrderService {
    config: ServiceConfig,
    state: OrderState,
    io: OrderIo,
}

impl OrderService {
    fn process_order(&mut self, order: &Order) -> Result<Receipt> {
        // Borrow state and io independently -- no conflict
        self.state.rate_limiter.check(order.customer_id)?;
        let balance = self.io.db.query_balance(order.customer_id)?;

        self.io.metrics.record("order.processed", 1);
        self.state.cache.invalidate(order.id);
        self.io.logger.info(&format!("Processed order {}", order.id));

        Ok(Receipt::new(order.id))
    }

    fn refresh_cache(&mut self) -> Result<()> {
        // Can pass sub-structs to helper functions independently
        let orders = self.io.db.query_recent_orders()?;
        self.state.cache.warm(orders);
        self.io.metrics.record("cache.refreshed", 1);
        Ok(())
    }
}

// Helper functions can borrow only the sub-struct they need
fn log_and_record(io: &mut OrderIo, message: &str, metric: &str) {
    io.logger.info(message);
    io.metrics.record(metric, 1);
}
```

## References

- [Compose structs for partial borrowing](https://rust-unofficial.github.io/patterns/patterns/structural/compose-structs.html)

## See Also

- [anti-monolith-function](anti-monolith-function.md) - Split monolithic functions into focused helpers
