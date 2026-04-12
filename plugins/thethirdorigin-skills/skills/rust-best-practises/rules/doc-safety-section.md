# doc-safety-section

> Document safety requirements with a Safety section for unsafe functions

## Why It Matters

An unsafe function transfers the burden of correctness from the compiler to the caller. The caller must uphold specific invariants — pointer validity, alignment, aliasing rules, lifetime guarantees — that the compiler cannot check. Without a Safety section, callers are guessing at what invariants they need to maintain, and a wrong guess leads to undefined behavior: memory corruption, data races, or security vulnerabilities.

The Safety section is a binding contract. It lists every precondition the caller must satisfy for the function to be sound. This is not optional documentation — it is the only place where these requirements are specified, and it enables code reviewers to verify that every call site upholds the contract.

## Bad

```rust
/// Reads a value from the given pointer.
pub unsafe fn read_ptr<T>(ptr: *const T) -> T {
    // Caller has no idea what safety requirements exist.
    ptr.read()
}
```

## Good

```rust
/// Reads a value of type `T` from the given pointer.
///
/// # Safety
///
/// The caller must ensure that:
/// - `ptr` is non-null and properly aligned for `T`.
/// - `ptr` points to a valid, initialized value of type `T`.
/// - The memory at `ptr` is not concurrently mutated by another thread
///   for the duration of this call.
/// - The pointed-to value will not be dropped by another owner. If `T`
///   implements `Drop`, the caller is responsible for ensuring the value
///   is not double-freed.
pub unsafe fn read_ptr<T>(ptr: *const T) -> T {
    ptr.read()
}
```

## See Also

- [doc-panics-section](doc-panics-section.md) - Documenting panic conditions
- [doc-errors-section](doc-errors-section.md) - Documenting error conditions
