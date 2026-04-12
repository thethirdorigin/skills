# unsafe-pass-miri

> Validate unsafe code with Miri, including adversarial test cases

## Why It Matters

Undefined behaviour in unsafe code can appear to work correctly in normal testing. Memory that was freed may still contain the expected value. An unaligned read may succeed on x86 but crash on ARM. A data race may never trigger under low contention. These bugs are time bombs that detonate under different optimisation levels, different platforms, or different load patterns.

Miri is an interpreter for Rust's Mid-level Intermediate Representation that detects undefined behaviour at runtime: use-after-free, uninitialised memory reads, out-of-bounds access, data races, and alignment violations. Running your test suite under Miri -- especially with adversarial inputs -- catches bugs that no amount of regular testing can find.

## Bad

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ring_buffer_basic() {
        // Only tests the happy path with small inputs.
        // Does not exercise boundary conditions where UB lurks.
        let mut buf = RingBuffer::new(4);
        buf.push(1);
        buf.push(2);
        assert_eq!(buf.pop(), Some(1));
        assert_eq!(buf.pop(), Some(2));
    }

    // Never run with Miri.
    // Never tested with adversarial inputs (capacity 0, capacity 1, wraparound).
}
```

## Good

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ring_buffer_basic_operations() {
        let mut buf = RingBuffer::new(4);
        buf.push(1);
        buf.push(2);
        assert_eq!(buf.pop(), Some(1));
        assert_eq!(buf.pop(), Some(2));
        assert_eq!(buf.pop(), None);
    }

    #[test]
    fn ring_buffer_wraps_around_capacity_boundary() {
        let mut buf = RingBuffer::new(3);
        buf.push(1);
        buf.push(2);
        buf.push(3);
        assert_eq!(buf.pop(), Some(1));
        buf.push(4); // wraps around
        assert_eq!(buf.pop(), Some(2));
        assert_eq!(buf.pop(), Some(3));
        assert_eq!(buf.pop(), Some(4));
    }

    #[test]
    fn ring_buffer_single_capacity() {
        let mut buf = RingBuffer::new(1);
        buf.push(42);
        assert_eq!(buf.pop(), Some(42));
        buf.push(99);
        assert_eq!(buf.pop(), Some(99));
    }

    #[test]
    fn ring_buffer_fill_and_drain_repeatedly() {
        let mut buf = RingBuffer::new(2);
        for i in 0..100u8 {
            buf.push(i);
            buf.push(i + 1);
            assert_eq!(buf.pop(), Some(i));
            assert_eq!(buf.pop(), Some(i + 1));
        }
    }
}

// Run with: cargo +nightly miri test
// Miri detects:
// - Use of uninitialised memory
// - Out-of-bounds pointer arithmetic
// - Use-after-free
// - Data races (with -Zmiri-check-number-validity)
```

## See Also

- [unsafe-safety-docs](unsafe-safety-docs.md) - Document safety contracts
- [unsafe-soundness](unsafe-soundness.md) - All code must be sound
- [test-error-paths](test-error-paths.md) - Test error paths explicitly
