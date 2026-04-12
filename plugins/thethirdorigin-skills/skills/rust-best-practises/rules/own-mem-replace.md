# own-mem-replace

> Use mem::take or mem::replace to move values out of enum variants without cloning

## Why It Matters

When transforming an enum that owns data, the borrow checker prevents moving a field while the enum is borrowed. A common workaround is cloning the inner value, but this introduces unnecessary allocation and copying -- especially wasteful when the owned data is a `String`, `Vec`, or other heap type.

`std::mem::take` swaps in the type's `Default` value and returns the original, giving you owned data with zero allocation. `std::mem::replace` does the same but lets you specify the replacement value explicitly. Both operations are O(1) pointer swaps, regardless of how large the contained data is. This pattern is idiomatic Rust for "take ownership of a field while leaving the struct in a valid state."

## Bad

```rust
#[derive(Clone)]
enum ConnectionState {
    Handshaking { buffer: Vec<u8> },
    Connected { session_id: String },
    Disconnected,
}

impl ConnectionState {
    fn finalize(&mut self) -> Option<String> {
        match self {
            // Clone to satisfy the borrow checker -- allocates a new String
            ConnectionState::Connected { session_id } => {
                let id = session_id.clone();
                *self = ConnectionState::Disconnected;
                Some(id)
            }
            _ => None,
        }
    }

    fn drain_buffer(&mut self) -> Vec<u8> {
        match self {
            // Clone entire buffer -- O(n) copy just to move data out
            ConnectionState::Handshaking { buffer } => {
                let data = buffer.clone();
                buffer.clear();
                data
            }
            _ => Vec::new(),
        }
    }
}
```

## Good

```rust
use std::mem;

enum ConnectionState {
    Handshaking { buffer: Vec<u8> },
    Connected { session_id: String },
    Disconnected,
}

impl ConnectionState {
    fn finalize(&mut self) -> Option<String> {
        // Replace the entire enum, getting owned data back with zero allocation
        match mem::replace(self, ConnectionState::Disconnected) {
            ConnectionState::Connected { session_id } => Some(session_id),
            other => {
                // Not connected -- put the original state back
                *self = other;
                None
            }
        }
    }

    fn drain_buffer(&mut self) -> Vec<u8> {
        match self {
            // mem::take swaps in Vec::default() (empty vec) and returns the original
            ConnectionState::Handshaking { buffer } => mem::take(buffer),
            _ => Vec::new(),
        }
    }
}
```

## References

- [mem-replace idiom](https://rust-unofficial.github.io/patterns/idioms/mem-replace.html)

## See Also

- [own-borrow-prefer](own-borrow-prefer.md) - Borrow over clone where possible
- [own-detect-cloning](own-detect-cloning.md) - Detect unnecessary cloning through review and profiling
