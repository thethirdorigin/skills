# own-borrow-prefer

> Borrow (&T, &mut T) over clone where possible

## Why It Matters

Cloning allocates memory and copies data. Borrowing is free -- it passes a pointer that the compiler verifies at zero runtime cost. In hot paths, unnecessary clones can dominate profiling output, turning O(1) operations into O(n) where n is the size of the cloned data.

Beyond performance, preferring borrows makes ownership flow explicit. When you see a `.clone()`, it should mean "I intentionally need a second owner" -- not "I added this to make the borrow checker stop complaining."

## Bad

```rust
fn process_transaction(tx: &Transaction) -> Result<Receipt> {
    // Unnecessary clone — we only need to read the account ID
    let account_id = tx.account_id.clone();
    let balance = fetch_balance(&account_id)?;

    // Unnecessary clone — format! can borrow
    let description = tx.description.clone();
    log::info!("Processing: {}", description);

    // Unnecessary clone — validate only needs a reference
    let cloned_tx = tx.clone();
    validate(&cloned_tx)?;

    Ok(Receipt::new(tx.id))
}
```

## Good

```rust
fn process_transaction(tx: &Transaction) -> Result<Receipt> {
    // Borrow the account ID directly — no allocation
    let balance = fetch_balance(&tx.account_id)?;

    // Borrow the description — format!/log macros accept references
    log::info!("Processing: {}", tx.description);

    // Pass the reference through — validate borrows too
    validate(tx)?;

    Ok(Receipt::new(tx.id))
}

// Accept &str instead of String to avoid forcing callers to clone
fn validate(tx: &Transaction) -> Result<()> {
    ensure!(tx.amount > Decimal::ZERO, "Amount must be positive");
    Ok(())
}
```

## See Also

- [own-detect-cloning](own-detect-cloning.md) - Detect unnecessary cloning through review and profiling
- [own-move-intentional](own-move-intentional.md) - Prefer moves over clones when ownership transfer is intentional
