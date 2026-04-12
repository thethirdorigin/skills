# own-detect-cloning

> Detect unnecessary cloning through code review and profiling

## Why It Matters

Gratuitous `.clone()` calls are the most common Rust performance mistake. Developers often add clones to satisfy the borrow checker without understanding why the borrow fails. Each clone may allocate and copy arbitrarily large data -- a `clone()` on a `Vec<Transaction>` with 10,000 entries copies all of them.

Every `.clone()` in a codebase should be intentional and justifiable. During code review, treat each clone as a question: "Why does this need a second owner?" If the answer is "to make it compile," the real fix is usually restructuring the ownership flow.

## Bad

```rust
fn process_batch(ledger: &Ledger) -> Result<Vec<Receipt>> {
    // Clone entire ledger entries to satisfy borrow checker
    let entries = ledger.entries().clone();
    let mut receipts = Vec::new();

    for entry in &entries {
        // Clone each entry to pass to validate — but validate only reads it
        let cloned_entry = entry.clone();
        validate(cloned_entry)?;

        // Clone the account ID — but we only need a reference
        let account = fetch_account(entry.account_id.clone())?;
        receipts.push(Receipt::from(&account));
    }

    Ok(receipts)
}

fn validate(entry: LedgerEntry) -> Result<()> {
    // Takes ownership but only reads — should take a reference
    ensure!(entry.amount > Decimal::ZERO, "Invalid amount");
    Ok(())
}
```

## Good

```rust
fn process_batch(ledger: &Ledger) -> Result<Vec<Receipt>> {
    let mut receipts = Vec::new();

    // Iterate by reference — no clone needed
    for entry in ledger.iter() {
        // Pass by reference — validate only reads
        validate(entry)?;

        // Pass Copy type by value, or borrow if not Copy
        let account = fetch_account(entry.account_id)?;
        receipts.push(Receipt::from(&account));
    }

    Ok(receipts)
}

fn validate(entry: &LedgerEntry) -> Result<()> {
    // Borrows — no ownership needed for validation
    ensure!(entry.amount > Decimal::ZERO, "Invalid amount");
    Ok(())
}

// When clone IS needed, document why
fn fork_facility(facility: &CreditFacility) -> CreditFacility {
    // Clone intentional: we need an independent copy to modify
    let mut forked = facility.clone();
    forked.id = FacilityId::new();
    forked.status = FacilityStatus::Draft;
    forked
}
```

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Borrow over clone where possible
- [own-move-intentional](own-move-intentional.md) - Prefer moves over clones for ownership transfer
