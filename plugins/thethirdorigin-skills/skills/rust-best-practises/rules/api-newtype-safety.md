# api-newtype-safety

> Use newtypes to distinguish semantically different values of the same underlying type

## Why It Matters

When multiple parameters share the same primitive type, the compiler cannot catch argument swaps. A function taking two `Uuid` parameters for source and destination accounts will happily accept them in the wrong order. This class of bug is silent, passes all type checks, and surfaces only at runtime — often in production.

Newtypes wrap a primitive in a named struct, giving the compiler enough information to reject swaps at compile time. They have zero runtime cost (the wrapper is erased) and serve as documentation at every call site.

## Bad

```rust
fn transfer(from: Uuid, to: Uuid, amount: u64) {
    // ...
}

// Caller can silently swap arguments:
let sender = Uuid::new_v4();
let receiver = Uuid::new_v4();
transfer(receiver, sender, 1000); // Compiles fine. Money flows backwards.
```

## Good

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct AccountId(Uuid);

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub struct Satoshis(u64);

fn transfer(from: AccountId, to: AccountId, amount: Satoshis) {
    // ...
}

// Caller must construct the right types:
let sender = AccountId(Uuid::new_v4());
let receiver = AccountId(Uuid::new_v4());
transfer(sender, receiver, Satoshis(1000));

// Swapping sender/receiver is still possible but the types make
// the intent explicit at every call site. Mixing AccountId with,
// say, a TransactionId is now a compile error.
```

## References

- [C-NEWTYPE](https://rust-lang.github.io/api-guidelines/type-safety.html#newtypes-provide-static-distinctions-c-newtype)
- [M-STRONG-TYPES](https://rust-lang.github.io/api-guidelines/type-safety.html)

## See Also

- [api-enum-over-bool](api-enum-over-bool.md) - Enums for call-site readability
- [api-common-traits](api-common-traits.md) - Derive standard traits on newtypes
