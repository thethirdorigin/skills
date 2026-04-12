# own-arc-async

> Use Arc\<T\> for shared ownership across async tasks

## Why It Matters

Async tasks in Tokio (and other multi-threaded runtimes) may run on different OS threads. `Rc<T>` uses non-atomic reference counting, which is not thread-safe -- it does not implement `Send`, so the compiler rejects it when you try to move it into a spawned task.

`Arc<T>` provides atomic reference counting that is safe to share across threads. Cloning an `Arc` is cheap (an atomic increment), and it ensures the inner data lives as long as any task holds a reference.

## Bad

```rust
use std::rc::Rc;

async fn start_processing(config: AppConfig) {
    // Rc is !Send — this won't compile with tokio::spawn
    let shared_config = Rc::new(config);

    let config_clone = Rc::clone(&shared_config);
    tokio::spawn(async move {
        // ERROR: Rc<AppConfig> cannot be sent between threads safely
        process_payments(config_clone).await;
    });

    let config_clone = Rc::clone(&shared_config);
    tokio::spawn(async move {
        process_disbursements(config_clone).await;
    });
}
```

## Good

```rust
use std::sync::Arc;

async fn start_processing(config: AppConfig) {
    // Arc is Send + Sync — safe to share across tasks
    let shared_config = Arc::new(config);

    let config_clone = Arc::clone(&shared_config);
    tokio::spawn(async move {
        process_payments(&config_clone).await;
    });

    let config_clone = Arc::clone(&shared_config);
    tokio::spawn(async move {
        process_disbursements(&config_clone).await;
    });
}
```

## See Also

- [own-arc-dyn-trait](own-arc-dyn-trait.md) - Arc\<dyn Trait\> for dependency injection
- [async-send-sync](async-send-sync.md) - Send + Sync bounds for async trait objects
