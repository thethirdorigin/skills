# api-common-traits

> Eagerly implement Debug, Clone, PartialEq, Eq, and Hash for public types

## Why It Matters

Public types that lack common trait implementations frustrate downstream users. Without Debug, types cannot be printed in logs or error messages. Without Clone, users cannot duplicate values without unsafe workarounds. Without PartialEq and Eq, types cannot be compared in tests or assertions. Without Hash, types cannot serve as keys in HashMaps or members of HashSets.

Deriving these traits costs nothing at the call site and dramatically increases how composable your types are. When in doubt, derive. You can always remove a derivation in a major version bump, but adding one is a non-breaking change.

## Bad

```rust
pub struct UserId(Uuid);

pub struct Config {
    pub name: String,
    pub timeout: Duration,
}

// Users cannot:
// - debug-print: println!("{:?}", user_id);
// - compare in tests: assert_eq!(id_a, id_b);
// - use as HashMap key: let map: HashMap<UserId, Account> = ...;
// - clone: let copy = config.clone();
```

## Good

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct UserId(Uuid);

#[derive(Debug, Clone, PartialEq)]
pub struct Config {
    name: String,
    timeout: Duration,
}

// Now users can freely debug-print, compare, hash, and clone these types.
```

## References

- [C-COMMON-TRAITS](https://rust-lang.github.io/api-guidelines/interoperability.html#types-eagerly-implement-common-traits-c-common-traits)

## See Also

- [api-debug-display](api-debug-display.md) - Debug and Display implementation guidance
- [api-send-sync](api-send-sync.md) - Thread-safety trait considerations
