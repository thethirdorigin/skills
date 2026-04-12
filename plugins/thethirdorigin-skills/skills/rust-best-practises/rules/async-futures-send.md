# async-futures-send

> Validate that generated futures are Send with compile-time assertions

## Why It Matters

A future is `Send` only if every type it holds across an `.await` point is `Send`. Holding a non-Send type like `Rc`, `Cell`, or a `MutexGuard` from `std::sync` across an `.await` makes the entire future non-Send. The resulting error message appears at the `tokio::spawn` call site, often far from where the non-Send type is held, making it difficult to diagnose.

Compile-time assertions catch this at the definition site instead. When you assert that a future is `Send` right where it is created, the error points directly to the problematic type, saving significant debugging time.

## Bad

```rust
use std::rc::Rc;

async fn process_entries(entries: Vec<LedgerEntry>) -> Result<()> {
    // Rc held across an .await — makes this future !Send
    let cache = Rc::new(HashMap::new());

    for entry in &entries {
        let result = validate(entry).await?; // .await while Rc is alive
        // cache.insert(entry.id, result);
    }

    Ok(())
}

// Error appears here — far from the Rc definition
// "future cannot be sent between threads safely"
tokio::spawn(process_entries(entries));
```

## Good

```rust
use std::sync::Arc;

async fn process_entries(entries: Vec<LedgerEntry>) -> Result<()> {
    // Arc instead of Rc — future is Send
    let cache = Arc::new(std::sync::Mutex::new(HashMap::new()));

    for entry in &entries {
        let result = validate(entry).await?;
        cache.lock().unwrap().insert(entry.id, result);
    }

    Ok(())
}

// Compile-time assertion — catches !Send at the definition site
fn _assert_process_entries_is_send() {
    fn assert_send<T: Send>(_: &T) {}
    let entries = Vec::new();
    let fut = process_entries(entries);
    assert_send(&fut);
}

// Alternative: use static_assertions crate for type-level checks
#[cfg(test)]
mod tests {
    use super::*;
    use static_assertions::assert_impl_all;

    // Verify key service futures are Send
    assert_impl_all!(
        std::pin::Pin<Box<dyn std::future::Future<Output = Result<()>> + Send>>: Send
    );
}
```

## References

- [M-TYPES-SEND](https://rust-lang.github.io/api-guidelines/) - Ensure types used in async contexts are Send

## See Also

- [async-send-sync](async-send-sync.md) - Send + Sync bounds for async trait objects
- [own-arc-async](own-arc-async.md) - Use Arc for shared ownership across async tasks
