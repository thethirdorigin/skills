# async-no-block

> Never block in async context -- no std::thread::sleep, no blocking I/O

## Why It Matters

Async runtimes like Tokio use cooperative scheduling: tasks voluntarily yield control at `.await` points. If a task calls `std::thread::sleep` or any other blocking operation, it holds the runtime thread hostage. No other task scheduled on that thread can make progress until the blocking call returns.

In a Tokio runtime with the default thread pool, blocking a single thread reduces throughput by 1/N (where N is the number of worker threads). Blocking all threads causes a complete deadlock -- every task stalls indefinitely.

## Bad

```rust
async fn wait_for_confirmation(tx_id: TransactionId) -> Result<Confirmation> {
    loop {
        if let Some(conf) = check_confirmation(tx_id).await? {
            return Ok(conf);
        }
        // Blocks the entire runtime thread for 1 second
        std::thread::sleep(Duration::from_secs(1));
    }
}

async fn compute_report(data: &[LedgerEntry]) -> Report {
    // CPU-bound work that blocks the runtime thread
    let result = expensive_computation(data); // synchronous, takes seconds
    Report::from(result)
}
```

## Good

```rust
async fn wait_for_confirmation(tx_id: TransactionId) -> Result<Confirmation> {
    loop {
        if let Some(conf) = check_confirmation(tx_id).await? {
            return Ok(conf);
        }
        // Yields to the runtime — other tasks continue running
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}

async fn compute_report(data: Vec<LedgerEntry>) -> Report {
    // Offload CPU-bound work to a blocking thread pool
    tokio::task::spawn_blocking(move || {
        let result = expensive_computation(&data);
        Report::from(result)
    })
    .await
    .expect("blocking task panicked")
}
```

## See Also

- [async-all-io](async-all-io.md) - Make all I/O operations async
- [async-yield-points](async-yield-points.md) - Include yield points in CPU-bound async tasks
