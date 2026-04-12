# log-defer-formatting

> Defer string formatting via message templates -- do not pre-format

## Why It Matters

Pre-formatting log messages with `format!()` allocates a String on the heap regardless of whether the log level is enabled. In a hot loop with debug logging disabled, this means thousands of wasted allocations per second that the subscriber will never see.

Message templates in `tracing` defer all formatting work to the subscriber. If the log level is disabled, no formatting occurs and no memory is allocated. When the level is enabled, the subscriber formats the fields in whatever way its output format requires -- JSON, logfmt, or human-readable.

## Bad

```rust
use tracing::info;

fn process_batch(batch_id: u64, items: &[Item]) {
    // Pre-formats even if info level is disabled
    let msg = format!("Processing batch {} with {} items", batch_id, items.len());
    info!("{}", msg);

    for (i, item) in items.iter().enumerate() {
        // Allocates a String on every iteration, even at WARN level
        let detail = format!("Item {} in batch {}: {:?}", i, batch_id, item);
        tracing::debug!("{}", detail);
    }
}
```

## Good

```rust
use tracing::{info, debug};

fn process_batch(batch_id: u64, items: &[Item]) {
    // Formatting deferred -- zero cost if info level is disabled
    info!(
        batch_id = batch_id,
        item_count = items.len(),
        "Processing batch"
    );

    for (i, item) in items.iter().enumerate() {
        // No allocation unless debug level is active
        debug!(
            batch_id = batch_id,
            item_index = i,
            item_id = %item.id,
            "Processing item"
        );
    }
}
```

## See Also

- [log-structured-events](log-structured-events.md) - Use named properties
- [log-hierarchical-naming](log-hierarchical-naming.md) - Hierarchical target names for filtering
