# async-yield-points

> Include yield points in long-running CPU-bound async tasks

## Why It Matters

Async runtimes are cooperative -- they rely on tasks yielding at `.await` points to schedule other work. A tight CPU-bound loop inside an async function never yields, which means every other task on the same runtime thread is starved until the loop completes. This causes latency spikes proportional to the batch size and can make the application appear unresponsive.

Inserting periodic yield points (via `tokio::task::yield_now().await`) gives the runtime a chance to poll other tasks, keeping latency bounded and predictable.

## Bad

```rust
async fn reconcile_ledger(entries: &[LedgerEntry]) -> ReconciliationReport {
    let mut mismatches = Vec::new();

    // Tight loop — processes 1 million entries without yielding
    // All other tasks on this thread are starved for the entire duration
    for entry in entries {
        if let Some(mismatch) = check_entry(entry) {
            mismatches.push(mismatch);
        }
    }

    ReconciliationReport::new(mismatches)
}
```

## Good

```rust
async fn reconcile_ledger(entries: &[LedgerEntry]) -> ReconciliationReport {
    let mut mismatches = Vec::new();

    for (i, entry) in entries.iter().enumerate() {
        if let Some(mismatch) = check_entry(entry) {
            mismatches.push(mismatch);
        }

        // Yield every 1000 items — other tasks get a chance to run
        if i % 1000 == 0 {
            tokio::task::yield_now().await;
        }
    }

    ReconciliationReport::new(mismatches)
}

// Alternative: offload to a blocking thread for truly heavy computation
async fn reconcile_ledger_heavy(entries: Vec<LedgerEntry>) -> ReconciliationReport {
    tokio::task::spawn_blocking(move || {
        let mismatches: Vec<_> = entries
            .iter()
            .filter_map(check_entry)
            .collect();
        ReconciliationReport::new(mismatches)
    })
    .await
    .expect("reconciliation task panicked")
}
```

## References

- [M-YIELD-POINTS](https://tokio.rs/tokio/tutorial) - Cooperative scheduling in async Rust

## See Also

- [async-no-block](async-no-block.md) - Never block in async context
