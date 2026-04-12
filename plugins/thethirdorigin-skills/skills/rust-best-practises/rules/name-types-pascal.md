# name-types-pascal

> Use PascalCase for types, traits, and enum variants

## Why It Matters

PascalCase for types is a core Rust convention enforced by the compiler itself -- `#[warn(non_camel_case_types)]` is on by default. Consistent casing lets readers distinguish types from values at a glance without checking the definition. It also ensures interoperability with the standard library and third-party crates, which universally follow this convention.

## Bad

```rust
struct credit_facility {
    id: Uuid,
    status: facility_status,
}

enum facility_status {
    active,
    frozen,
    closed,
}

trait disbursement_handler {
    fn disburse(&self, amount: Decimal) -> Result<()>;
}
```

## Good

```rust
struct CreditFacility {
    id: Uuid,
    status: FacilityStatus,
}

enum FacilityStatus {
    Active,
    Frozen,
    Closed,
}

trait DisbursementHandler {
    fn disburse(&self, amount: Decimal) -> Result<()>;
}
```

## References

- [C-CASE](https://rust-lang.github.io/api-guidelines/naming.html#c-case) - RFC 430 naming conventions

## See Also

- [name-funcs-snake](name-funcs-snake.md) - snake_case for functions and variables
- [name-consts-screaming](name-consts-screaming.md) - SCREAMING_SNAKE_CASE for constants
