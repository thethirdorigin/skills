# unsafe-soundness

> All code must be sound -- safe functions must never allow undefined behaviour

## Why It Matters

Soundness is Rust's core guarantee: if you use only safe code, undefined behaviour is impossible. A soundness bug -- a safe function that can cause UB -- is the most serious category of bug in Rust because it violates the fundamental contract that safe Rust users rely on.

A safe public function that wraps an `unsafe` block without properly validating its preconditions creates a soundness hole. Any user can trigger undefined behaviour without writing `unsafe` themselves, which defeats the entire purpose of Rust's safety model.

## Bad

```rust
/// Returns the element at the given index without bounds checking.
pub fn get_fast(slice: &[u8], index: usize) -> u8 {
    // SOUNDNESS BUG: This is a safe function that can cause UB.
    // Any caller can pass an out-of-bounds index and trigger UB
    // without writing unsafe themselves.
    unsafe { *slice.as_ptr().add(index) }
}

/// Creates a string from raw bytes without UTF-8 validation.
pub fn fast_string(bytes: Vec<u8>) -> String {
    // SOUNDNESS BUG: Caller can pass invalid UTF-8.
    // Downstream code that relies on String being valid UTF-8 will
    // exhibit undefined behaviour.
    unsafe { String::from_utf8_unchecked(bytes) }
}
```

## Good

```rust
/// Returns the element at the given index without bounds checking.
///
/// # Safety
///
/// `index` must be less than `slice.len()`.
pub unsafe fn get_unchecked(slice: &[u8], index: usize) -> u8 {
    // Marked unsafe -- caller takes responsibility for the precondition.
    *slice.as_ptr().add(index)
}

/// Returns the element at the given index, or `None` if out of bounds.
pub fn get(slice: &[u8], index: usize) -> Option<u8> {
    // Safe wrapper validates the precondition before calling unsafe code.
    if index < slice.len() {
        // SAFETY: We just verified that index < slice.len().
        Some(unsafe { *slice.as_ptr().add(index) })
    } else {
        None
    }
}

/// Creates a string from raw bytes, validating UTF-8.
pub fn to_string(bytes: Vec<u8>) -> Result<String, FromUtf8Error> {
    // Safe: validates invariant before constructing the String.
    String::from_utf8(bytes)
}
```

## References

- [M-UNSOUND](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [unsafe-reserve-ffi](unsafe-reserve-ffi.md) - Reserve unsafe for legitimate uses
- [unsafe-safety-docs](unsafe-safety-docs.md) - Document safety contracts
- [unsafe-pass-miri](unsafe-pass-miri.md) - Validate unsafe code with Miri
