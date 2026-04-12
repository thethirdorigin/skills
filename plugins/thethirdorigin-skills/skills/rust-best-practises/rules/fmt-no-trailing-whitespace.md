# fmt-no-trailing-whitespace

> Remove trailing whitespace on all lines

## Why It Matters

Trailing whitespace is invisible but causes real problems. When a collaborator opens the file and their editor trims whitespace on save, every affected line appears as a change in the diff -- even though no meaningful code changed. This obscures real modifications during code review and pollutes git blame.

rustfmt removes trailing whitespace automatically. Configuring your editor to trim on save prevents it from creeping back in between format runs.

## Bad

```rust
fn calculate_interest(principal: Decimal, rate: Decimal) -> Decimal {   
    let annual = principal * rate;  
    let monthly = annual / Decimal::from(12);  
    monthly   
}
```

## Good

```rust
fn calculate_interest(principal: Decimal, rate: Decimal) -> Decimal {
    let annual = principal * rate;
    let monthly = annual / Decimal::from(12);
    monthly
}
```

## See Also

- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
