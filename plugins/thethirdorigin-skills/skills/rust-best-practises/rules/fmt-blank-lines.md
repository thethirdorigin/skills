# fmt-blank-lines

> Separate items with 0-1 blank lines -- no multiple consecutive blank lines

## Why It Matters

Multiple consecutive blank lines waste vertical space and create an uneven visual rhythm. Readers unconsciously interpret large gaps as section breaks, which can mislead them about the relationship between items. A single blank line between functions and logical blocks provides clear separation without excess whitespace.

Consistent spacing also makes it easier to navigate with keyboard shortcuts that jump between paragraphs or functions.

## Bad

```rust
fn validate_collateral(collateral: &Collateral) -> Result<()> {
    ensure!(collateral.value > Decimal::ZERO, "Collateral value must be positive");
    Ok(())
}



// Three blank lines above — excessive gap


fn calculate_ltv(loan_amount: Decimal, collateral_value: Decimal) -> Decimal {
    loan_amount / collateral_value
}




fn is_overcollateralized(ltv: Decimal, threshold: Decimal) -> bool {
    ltv < threshold
}
```

## Good

```rust
fn validate_collateral(collateral: &Collateral) -> Result<()> {
    ensure!(collateral.value > Decimal::ZERO, "Collateral value must be positive");
    Ok(())
}

fn calculate_ltv(loan_amount: Decimal, collateral_value: Decimal) -> Decimal {
    loan_amount / collateral_value
}

fn is_overcollateralized(ltv: Decimal, threshold: Decimal) -> bool {
    ltv < threshold
}
```

## See Also

- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
