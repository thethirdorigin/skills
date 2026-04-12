# name-funcs-snake

> Use snake_case for functions, methods, variables, and modules

## Why It Matters

snake_case for functions, methods, variables, and modules is the universal Rust convention. The compiler warns on non-snake_case items by default (`#[warn(non_snake_case)]`), and every crate in the ecosystem follows this pattern. Deviating from it makes your code look foreign and triggers compiler warnings that clutter the build output.

Consistent casing also helps readers instantly identify whether an identifier refers to a type (PascalCase) or a value/function (snake_case).

## Bad

```rust
mod CreditFacility;

fn DeployCreditFacility(facilityId: Uuid) -> Result<()> {
    let totalAmount = calculate_total(facilityId)?;
    let isValid = totalAmount > Decimal::ZERO;
    Ok(())
}
```

## Good

```rust
mod credit_facility;

fn deploy_credit_facility(facility_id: Uuid) -> Result<()> {
    let total_amount = calculate_total(facility_id)?;
    let is_valid = total_amount > Decimal::ZERO;
    Ok(())
}
```

## References

- [C-CASE](https://rust-lang.github.io/api-guidelines/naming.html#c-case) - RFC 430 naming conventions

## See Also

- [name-types-pascal](name-types-pascal.md) - PascalCase for types and traits
- [name-consts-screaming](name-consts-screaming.md) - SCREAMING_SNAKE_CASE for constants
