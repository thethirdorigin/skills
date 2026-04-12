# own-move-intentional

> Prefer moves over clones when ownership transfer is intentional

## Why It Matters

Moving a value in Rust is a zero-cost operation -- it copies the stack representation (pointer, length, capacity) without touching heap data. Cloning, on the other hand, duplicates the entire value including any heap allocations. When you are done with a value and want to transfer it to another owner, moving is both correct and free.

A common anti-pattern is cloning a value, passing the clone, and never using the original again. The compiler will not warn you about this -- it is a performance bug that only shows up in profiling.

## Bad

```rust
fn build_and_submit(entries: Vec<LedgerEntry>) -> Result<()> {
    // Clone entries, then never use the original again — wasteful
    let report = generate_report(entries.clone());
    submit(report)?;

    // entries is never used after this point, but we paid for a full clone
    Ok(())
}

async fn spawn_worker(config: AppConfig) {
    // Cloning config only to move the clone — original is dropped immediately
    let config_clone = config.clone();
    tokio::spawn(async move {
        run_worker(config_clone).await;
    });
    // config is dropped here unused
}
```

## Good

```rust
fn build_and_submit(entries: Vec<LedgerEntry>) -> Result<()> {
    // Move entries directly — zero cost, no allocation
    let report = generate_report(entries);
    submit(report)?;

    Ok(())
}

async fn spawn_worker(config: AppConfig) {
    // Move config directly into the task — no clone needed
    tokio::spawn(async move {
        run_worker(config).await;
    });
}
```

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Borrow over clone when you don't need ownership
- [own-detect-cloning](own-detect-cloning.md) - Detect unnecessary cloning patterns
