# unsafe-reserve-ffi

> Reserve unsafe for FFI boundaries, novel abstractions, and measured performance gains

## Why It Matters

Every `unsafe` block is a promise: "I, the author, guarantee that the invariants the compiler cannot verify are upheld here." This is a serious commitment that shifts the burden of correctness from the compiler to the human. Using `unsafe` to bypass the borrow checker because it feels too restrictive is not a valid justification -- it means the design needs rethinking, not that safety should be abandoned.

Legitimate uses of `unsafe` include FFI calls to C libraries, implementing low-level data structures that cannot be expressed in safe Rust, and performance-critical code where profiling proves the safe version is a bottleneck.

## Bad

```rust
fn get_first_two(items: &[u32]) -> (&u32, &u32) {
    // Using unsafe to "work around" the borrow checker
    // when a simple bounds check would suffice
    unsafe {
        let ptr = items.as_ptr();
        (&*ptr, &*ptr.add(1))
    }
}

fn swap_values(a: &mut u32, b: &mut u32) {
    // Using unsafe because "it's faster" -- no profiling evidence
    unsafe {
        let tmp = std::ptr::read(a);
        std::ptr::write(a, std::ptr::read(b));
        std::ptr::write(b, tmp);
    }
}
```

## Good

```rust
// Safe alternative -- the compiler verifies correctness
fn get_first_two(items: &[u32]) -> Option<(&u32, &u32)> {
    Some((&items.get(0)?, &items.get(1)?))
}

// std::mem::swap does this safely and the compiler optimises it
fn swap_values(a: &mut u32, b: &mut u32) {
    std::mem::swap(a, b);
}

// Legitimate unsafe: FFI boundary
extern "C" {
    fn c_library_init(config: *const c_char) -> c_int;
    fn c_library_process(data: *const u8, len: usize) -> c_int;
}

pub fn init(config: &str) -> Result<(), Error> {
    let c_config = CString::new(config)?;
    // SAFETY: c_config is a valid null-terminated C string,
    // and c_library_init only reads from the pointer during this call.
    let result = unsafe { c_library_init(c_config.as_ptr()) };
    if result != 0 {
        return Err(Error::InitFailed(result));
    }
    Ok(())
}
```

## References

- [M-UNSAFE](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [unsafe-implies-ub](unsafe-implies-ub.md) - Unsafe implies UB risk, not general danger
- [unsafe-safety-docs](unsafe-safety-docs.md) - Document safety contracts
- [unsafe-soundness](unsafe-soundness.md) - All code must be sound
