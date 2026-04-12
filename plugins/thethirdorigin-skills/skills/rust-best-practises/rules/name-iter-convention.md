# name-iter-convention

> Use iter()/iter_mut()/into_iter() for iterator methods

## Why It Matters

The `iter()`, `iter_mut()`, and `into_iter()` trio is the standard Rust convention for producing iterators with different borrowing semantics. Every collection in the standard library follows this pattern, and Rust developers expect it. Using non-standard names forces callers to check documentation instead of relying on muscle memory.

The naming also encodes the borrow semantics: `iter()` borrows, `iter_mut()` borrows mutably, and `into_iter()` consumes. This consistency eliminates guesswork.

## Bad

```rust
impl Ledger {
    // Non-standard names — callers must check docs for borrow semantics
    fn get_entries(&self) -> impl Iterator<Item = &LedgerEntry> {
        self.entries.iter()
    }

    fn entries_mut(&mut self) -> impl Iterator<Item = &mut LedgerEntry> {
        self.entries.iter_mut()
    }

    fn take_entries(self) -> impl Iterator<Item = LedgerEntry> {
        self.entries.into_iter()
    }
}
```

## Good

```rust
impl Ledger {
    fn iter(&self) -> impl Iterator<Item = &LedgerEntry> {
        self.entries.iter()
    }

    fn iter_mut(&mut self) -> impl Iterator<Item = &mut LedgerEntry> {
        self.entries.iter_mut()
    }
}

impl IntoIterator for Ledger {
    type Item = LedgerEntry;
    type IntoIter = std::vec::IntoIter<LedgerEntry>;

    fn into_iter(self) -> Self::IntoIter {
        self.entries.into_iter()
    }
}
```

## References

- [C-ITER](https://rust-lang.github.io/api-guidelines/naming.html#c-iter) - Collections provide iter, iter_mut, into_iter

## See Also

- [name-into-ownership](name-into-ownership.md) - into_ prefix for ownership transfer
