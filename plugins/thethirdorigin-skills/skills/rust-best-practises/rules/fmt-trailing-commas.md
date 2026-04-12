# fmt-trailing-commas

> Use trailing commas in all multi-line comma-separated lists

## Why It Matters

Trailing commas make diffs cleaner. Adding a new item to a list only touches one line instead of two (modifying the old last line to add a comma, plus the new line). Reordering items is also simpler because every line has the same shape -- no special-casing the last element.

rustfmt adds trailing commas to multi-line lists by default, so adopting this convention means your manual formatting stays consistent with automated output.

## Bad

```rust
let config = AppConfig {
    database_url: db_url,
    max_connections: 20,
    idle_timeout: Duration::from_secs(300),
    enable_tls: true  // no trailing comma — adding a field changes this line too
};

fn transfer_funds(
    from: AccountId,
    to: AccountId,
    amount: Decimal,
    memo: Option<String>  // no trailing comma
) -> Result<TransferReceipt> {
    // ...
}
```

## Good

```rust
let config = AppConfig {
    database_url: db_url,
    max_connections: 20,
    idle_timeout: Duration::from_secs(300),
    enable_tls: true, // trailing comma — adding a field is a one-line diff
};

fn transfer_funds(
    from: AccountId,
    to: AccountId,
    amount: Decimal,
    memo: Option<String>, // trailing comma
) -> Result<TransferReceipt> {
    // ...
}
```

## See Also

- [fmt-line-width](fmt-line-width.md) - Keep lines under 100 characters
- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
