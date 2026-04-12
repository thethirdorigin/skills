# name-to-expensive

> Use to_ prefix for expensive conversions that may allocate

## Why It Matters

The `to_` prefix signals that a conversion creates new owned data, typically involving allocation or significant computation. This tells callers that the result should be cached if used repeatedly, and that calling the method in a tight loop has real cost.

The distinction between `as_` (free view) and `to_` (allocating conversion) is a critical part of Rust API design. Getting it right helps callers make informed performance decisions without reading the implementation.

## Bad

```rust
impl LedgerEntry {
    // Misleading: as_ implies cheap, but this allocates a String
    fn as_string(&self) -> String {
        format!("{}:{}", self.account_id, self.amount)
    }

    // Misleading: as_ implies a view, but this creates a new Vec
    fn as_bytes(&self) -> Vec<u8> {
        bincode::serialize(self).unwrap()
    }
}
```

## Good

```rust
impl LedgerEntry {
    // to_ signals allocation — caller knows to cache the result
    fn to_string(&self) -> String {
        format!("{}:{}", self.account_id, self.amount)
    }

    // to_ signals new data is created
    fn to_bytes(&self) -> Vec<u8> {
        bincode::serialize(self).unwrap()
    }

    // Compare: as_ for the cheap version returning a reference
    fn as_account_id(&self) -> &AccountId {
        &self.account_id
    }
}
```

## References

- [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#c-conv) - Ad-hoc conversions follow `as_`, `to_`, `into_` conventions

## See Also

- [name-as-cheap](name-as-cheap.md) - as_ prefix for cheap conversions
- [name-into-ownership](name-into-ownership.md) - into_ prefix for ownership transfer
