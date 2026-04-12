# unsafe-implies-ub

> Treat unsafe as implying undefined behaviour risk, not general "danger"

## Why It Matters

The `unsafe` keyword has a precise meaning in Rust: it marks operations that can cause undefined behaviour if their preconditions are violated. These operations include dereferencing raw pointers, calling `extern` functions, accessing mutable statics, implementing unsafe traits, and accessing union fields. Everything else is safe by definition, no matter how "dangerous" it might seem logically.

Using `unsafe` as a label for "this code is scary" or "this function is slow" dilutes its meaning. Reviewers and tools (like Miri) focus on `unsafe` blocks to verify memory safety. If `unsafe` is used for non-UB-related purposes, it wastes review effort and creates a false sense that the "dangerous" code has been audited for memory safety.

## Bad

```rust
// Using unsafe as a "danger" label -- no actual UB risk
unsafe fn delete_all_records(db: &Database) -> Result<(), Error> {
    db.execute("DELETE FROM users").await?;
    Ok(())
}

// Using unsafe for emphasis -- the operation is safe, just expensive
unsafe fn very_expensive_computation(data: &[f64]) -> f64 {
    data.iter().map(|x| x.powi(100)).sum()
}

// Caller has to use unsafe for no memory-safety reason
unsafe {
    delete_all_records(&db).await?;
}
```

## Good

```rust
// Dangerous operations that are still safe (no UB) don't need unsafe.
// Use type systems or naming to communicate danger:
fn delete_all_records(db: &Database) -> Result<(), Error> {
    db.execute("DELETE FROM users").await
}

// For operations that truly can cause UB, unsafe is correct:
pub unsafe fn from_raw_parts(ptr: *mut u8, len: usize, cap: usize) -> Vec<u8> {
    // SAFETY: Caller must guarantee:
    // - ptr was allocated by the global allocator with layout for cap bytes
    // - len <= cap
    // - ptr is not used after this call (ownership transferred)
    Vec::from_raw_parts(ptr, len, cap)
}

// Use the type system to prevent misuse of dangerous-but-safe operations:
pub struct DangerousOperation {
    _private: (), // Cannot be constructed outside this module
}

impl DangerousOperation {
    pub(crate) fn new() -> Self {
        Self { _private: () }
    }
}

pub fn delete_all_records(db: &Database, _proof: DangerousOperation) -> Result<(), Error> {
    db.execute("DELETE FROM users").await
}
```

## References

- [M-UNSAFE-IMPLIES-UB](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [unsafe-reserve-ffi](unsafe-reserve-ffi.md) - Reserve unsafe for legitimate uses
- [unsafe-soundness](unsafe-soundness.md) - All code must be sound
- [unsafe-safety-docs](unsafe-safety-docs.md) - Document safety contracts
