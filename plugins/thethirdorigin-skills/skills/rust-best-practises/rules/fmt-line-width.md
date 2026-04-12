# fmt-line-width

> Keep lines under 100 characters

## Why It Matters

The standard Rust style caps lines at 100 characters. Long lines are difficult to review in side-by-side diffs, GitHub PR views, and split-pane editors. They also force horizontal scrolling, which breaks reading flow and hides logic at the end of the line.

Breaking lines at logical points -- after commas, before method chains, or at operator boundaries -- preserves readability and makes the structure of complex expressions visible.

## Bad

```rust
fn create_credit_facility(db: &DatabaseConnection, facility_id: CreditFacilityId, customer_id: CustomerId, terms: &CreditTerms, collateral: CollateralRequirement) -> Result<CreditFacility, CreditFacilityError> {
    let facility = CreditFacility::new(facility_id, customer_id, terms.annual_rate(), terms.duration_months(), collateral.minimum_ratio(), collateral.asset_type());
    Ok(facility)
}
```

## Good

```rust
fn create_credit_facility(
    db: &DatabaseConnection,
    facility_id: CreditFacilityId,
    customer_id: CustomerId,
    terms: &CreditTerms,
    collateral: CollateralRequirement,
) -> Result<CreditFacility, CreditFacilityError> {
    let facility = CreditFacility::new(
        facility_id,
        customer_id,
        terms.annual_rate(),
        terms.duration_months(),
        collateral.minimum_ratio(),
        collateral.asset_type(),
    );
    Ok(facility)
}
```

## See Also

- [fmt-trailing-commas](fmt-trailing-commas.md) - Trailing commas in multi-line lists
- [fmt-cargo-fmt](fmt-cargo-fmt.md) - Automate formatting with cargo fmt
