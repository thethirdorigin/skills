# own-copy-value-types

> Pass Copy types (u64, bool, Uuid, small enums) by value

## Why It Matters

For small types that implement `Copy`, passing by reference adds unnecessary indirection. A `&u64` is an 8-byte pointer to an 8-byte value -- the CPU must dereference the pointer to read the data, which is strictly worse than passing the value directly in a register.

Copy types include all primitives (`u8`..`u128`, `i8`..`i128`, `f32`, `f64`, `bool`, `char`), small structs that derive `Copy`, and `Uuid` (16 bytes). Passing these by value is both simpler and faster.

## Bad

```rust
fn is_active(status: &bool) -> bool {
    *status
}

fn calculate_fee(amount: &u64, rate: &f64) -> f64 {
    *amount as f64 * rate
}

fn find_facility(id: &Uuid, facilities: &[CreditFacility]) -> Option<&CreditFacility> {
    facilities.iter().find(|f| f.id == *id)
}

fn apply_discount(price: &Decimal, discount_percent: &u32) -> Decimal {
    price * Decimal::from(100 - discount_percent) / Decimal::from(100)
}
```

## Good

```rust
fn is_active(status: bool) -> bool {
    status
}

fn calculate_fee(amount: u64, rate: f64) -> f64 {
    amount as f64 * rate
}

fn find_facility(id: Uuid, facilities: &[CreditFacility]) -> Option<&CreditFacility> {
    facilities.iter().find(|f| f.id == id)
}

fn apply_discount(price: &Decimal, discount_percent: u32) -> Decimal {
    price * Decimal::from(100 - discount_percent) / Decimal::from(100)
}
```

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Borrow over clone for non-Copy types
