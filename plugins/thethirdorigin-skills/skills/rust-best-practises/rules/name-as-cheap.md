# name-as-cheap

> Use as_ prefix for cheap, reference-to-reference conversions

## Why It Matters

The `as_` prefix is a Rust convention that signals a zero-cost conversion -- typically returning a view or reference into existing data without any allocation or computation. Callers can use `as_` methods freely in hot loops, pass them to functions expecting slices, and chain them without worrying about performance.

Misusing `as_` for methods that allocate breaks this contract and misleads callers into thinking an operation is free when it is not.

## Bad

```rust
impl AccountId {
    // Misleading: to_ prefix implies allocation, but this is a cheap view
    fn to_bytes(&self) -> &[u8] {
        &self.0
    }

    // Misleading: to_ implies cost, but it's just a reference cast
    fn to_str(&self) -> &str {
        std::str::from_utf8(&self.0).unwrap()
    }
}
```

## Good

```rust
impl AccountId {
    // as_ signals zero-cost — returns a view into existing data
    fn as_bytes(&self) -> &[u8] {
        &self.0
    }

    fn as_str(&self) -> &str {
        std::str::from_utf8(&self.0).unwrap()
    }
}

impl Transaction {
    // as_ for cheap reference conversions
    fn as_slice(&self) -> &[u8] {
        &self.payload
    }
}
```

## References

- [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#c-conv) - Ad-hoc conversions follow `as_`, `to_`, `into_` conventions

## See Also

- [name-to-expensive](name-to-expensive.md) - to_ prefix for expensive conversions
- [name-into-ownership](name-into-ownership.md) - into_ prefix for ownership transfer
