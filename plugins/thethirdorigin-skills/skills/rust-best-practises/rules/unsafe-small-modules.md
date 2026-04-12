# unsafe-small-modules

> Contain unsafe code in small, focused modules with safe public interfaces

## Why It Matters

Every `unsafe` block requires manual verification that its invariants hold. When unsafe code is scattered across a large module, the entire module becomes the audit surface -- any function might depend on or violate the safety invariants. This makes code review expensive and error-prone.

Isolating unsafe code into a small, dedicated module with a safe public API shrinks the audit boundary to just that module. The rest of the codebase interacts only with the safe wrapper and benefits from the compiler's normal guarantees. When a soundness bug is suspected, reviewers know exactly where to look. This pattern also makes it straightforward to add targeted tests, run Miri on the critical section, and document the precise invariants that the unsafe code relies on.

## Bad

```rust
// lib.rs -- 800-line module with unsafe scattered throughout.

pub struct RingBuffer {
    ptr: *mut u8,
    cap: usize,
    head: usize,
    tail: usize,
}

impl RingBuffer {
    pub fn push(&mut self, byte: u8) {
        // Business logic mixed with unsafe pointer arithmetic.
        if self.len() == self.cap {
            self.grow(); // also contains unsafe
        }
        unsafe {
            self.ptr.add(self.tail).write(byte);
        }
        self.tail = (self.tail + 1) % self.cap;
    }

    pub fn pop(&mut self) -> Option<u8> {
        if self.is_empty() {
            return None;
        }
        let byte = unsafe { self.ptr.add(self.head).read() };
        self.head = (self.head + 1) % self.cap;
        Some(byte)
    }

    fn grow(&mut self) {
        unsafe {
            let new_ptr = alloc::alloc(Layout::array::<u8>(self.cap * 2).unwrap());
            core::ptr::copy_nonoverlapping(self.ptr, new_ptr, self.cap);
            alloc::dealloc(self.ptr, Layout::array::<u8>(self.cap).unwrap());
            self.ptr = new_ptr;
            self.cap *= 2;
        }
    }

    // ... 600 more lines of mixed safe and unsafe code.
}
```

## Good

```rust
// raw.rs -- small module, only unsafe code lives here.
//
// INVARIANTS:
// - `ptr` is a valid, aligned allocation of `cap` bytes (cap > 0).
// - Caller must ensure index < cap before calling read/write.

use std::alloc::{self, Layout};

pub(crate) struct RawBuf {
    ptr: *mut u8,
    cap: usize,
}

impl RawBuf {
    pub fn with_capacity(cap: usize) -> Self {
        assert!(cap > 0, "capacity must be non-zero");
        let layout = Layout::array::<u8>(cap).expect("layout overflow");
        // SAFETY: layout has non-zero size (cap > 0).
        let ptr = unsafe { alloc::alloc(layout) };
        assert!(!ptr.is_null(), "allocation failed");
        Self { ptr, cap }
    }

    pub fn capacity(&self) -> usize {
        self.cap
    }

    /// Read a byte at `index`.
    ///
    /// # Safety
    ///
    /// `index` must be less than `self.cap` and the byte must
    /// have been previously written.
    pub unsafe fn read(&self, index: usize) -> u8 {
        debug_assert!(index < self.cap);
        unsafe { self.ptr.add(index).read() }
    }

    /// Write a byte at `index`.
    ///
    /// # Safety
    ///
    /// `index` must be less than `self.cap`.
    pub unsafe fn write(&mut self, index: usize, byte: u8) {
        debug_assert!(index < self.cap);
        unsafe { self.ptr.add(index).write(byte) }
    }

    pub fn grow(&mut self, new_cap: usize) {
        assert!(new_cap > self.cap);
        let new_layout = Layout::array::<u8>(new_cap).expect("layout overflow");
        // SAFETY: ptr is a valid allocation of `self.cap` bytes, and
        // new_cap > self.cap so the new layout is larger.
        let new_ptr = unsafe {
            alloc::realloc(self.ptr, Layout::array::<u8>(self.cap).unwrap(), new_cap)
        };
        assert!(!new_ptr.is_null(), "reallocation failed");
        self.ptr = new_ptr;
        self.cap = new_cap;
    }
}

impl Drop for RawBuf {
    fn drop(&mut self) {
        // SAFETY: ptr and cap are always valid per module invariants.
        unsafe {
            alloc::dealloc(self.ptr, Layout::array::<u8>(self.cap).unwrap());
        }
    }
}

// ring_buffer.rs -- safe public API, no unsafe blocks.

mod raw;
use raw::RawBuf;

pub struct RingBuffer {
    buf: RawBuf,
    head: usize,
    tail: usize,
    len: usize,
}

impl RingBuffer {
    pub fn new(cap: usize) -> Self {
        Self { buf: RawBuf::with_capacity(cap), head: 0, tail: 0, len: 0 }
    }

    pub fn push(&mut self, byte: u8) {
        if self.len == self.buf.capacity() {
            self.buf.grow(self.buf.capacity() * 2);
        }
        // SAFETY: tail < capacity because len < capacity after potential grow.
        unsafe { self.buf.write(self.tail, byte) };
        self.tail = (self.tail + 1) % self.buf.capacity();
        self.len += 1;
    }

    pub fn pop(&mut self) -> Option<u8> {
        if self.len == 0 {
            return None;
        }
        // SAFETY: head < capacity and this slot was previously written.
        let byte = unsafe { self.buf.read(self.head) };
        self.head = (self.head + 1) % self.buf.capacity();
        self.len -= 1;
        Some(byte)
    }
}
```

## References

- [Unsafe in small modules](https://rust-unofficial.github.io/patterns/patterns/structural/unsafe-mods.html)

## See Also

- [unsafe-reserve-ffi](unsafe-reserve-ffi.md) - Reserve unsafe for FFI and low-level operations
- [unsafe-soundness](unsafe-soundness.md) - All safe functions must be sound
- [unsafe-safety-docs](unsafe-safety-docs.md) - Document safety invariants on every unsafe block
