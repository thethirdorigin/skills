# unsafe-safety-docs

> Document safety contracts with // SAFETY: comments on every unsafe block

## Why It Matters

An `unsafe` block without a safety comment is an unverifiable claim. Reviewers cannot confirm that the invariants hold because the author never stated what invariants they are relying on. Future maintainers modifying nearby code may unknowingly violate preconditions that were only in the original author's head.

`// SAFETY:` comments serve as the primary review mechanism for unsafe code. They explain which preconditions are required, why they hold at this specific call site, and what would go wrong if they were violated. This makes unsafe code reviewable, auditable, and maintainable.

## Bad

```rust
pub struct RingBuffer {
    data: *mut u8,
    capacity: usize,
    head: usize,
    tail: usize,
}

impl RingBuffer {
    pub fn push(&mut self, byte: u8) {
        unsafe {
            self.data.add(self.head).write(byte);
        }
        self.head = (self.head + 1) % self.capacity;
    }

    pub fn pop(&mut self) -> Option<u8> {
        if self.head == self.tail {
            return None;
        }
        let byte = unsafe { self.data.add(self.tail).read() };
        self.tail = (self.tail + 1) % self.capacity;
        Some(byte)
    }
}
```

## Good

```rust
pub struct RingBuffer {
    data: *mut u8,
    capacity: usize,
    head: usize,
    tail: usize,
}

impl RingBuffer {
    pub fn push(&mut self, byte: u8) {
        debug_assert!(
            self.len() < self.capacity,
            "push called on full buffer"
        );

        // SAFETY: self.head is always in range [0, capacity) because it is
        // computed as (head + 1) % capacity. The allocation in new() guarantees
        // that self.data points to at least self.capacity bytes of valid memory.
        unsafe {
            self.data.add(self.head).write(byte);
        }
        self.head = (self.head + 1) % self.capacity;
    }

    pub fn pop(&mut self) -> Option<u8> {
        if self.head == self.tail {
            return None;
        }

        // SAFETY: self.tail is in range [0, capacity) by the same modular
        // arithmetic invariant. The byte at this position was previously
        // written by push(), so it is initialised.
        let byte = unsafe { self.data.add(self.tail).read() };
        self.tail = (self.tail + 1) % self.capacity;
        Some(byte)
    }
}
```

## See Also

- [unsafe-soundness](unsafe-soundness.md) - All code must be sound
- [unsafe-reserve-ffi](unsafe-reserve-ffi.md) - Reserve unsafe for legitimate uses
- [unsafe-pass-miri](unsafe-pass-miri.md) - Validate unsafe code with Miri
