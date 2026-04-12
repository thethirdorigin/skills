# perf-monitor-struct-sizes

> Monitor struct sizes for stack optimisation on hot types

## Why It Matters

Large structs passed by value on the stack cause cache misses and increase the risk of stack overflows, especially in recursive functions or deeply nested call chains. A 512-byte struct that fits in a single cache line as a reference becomes a multi-cache-line copy when passed by value.

Adding a new field to a frequently used struct can silently double its size. Compile-time size assertions catch this accidental bloat before it reaches production. For hot types that appear in collections or are passed through many stack frames, keeping the size small has measurable performance impact.

## Bad

```rust
pub struct Event {
    pub id: u64,
    pub timestamp: i64,
    pub source: String,         // 24 bytes (ptr + len + cap)
    pub payload: Vec<u8>,       // 24 bytes
    pub metadata: HashMap<String, String>,  // 48 bytes
    pub tags: Vec<String>,      // 24 bytes
    pub trace_id: [u8; 128],    // 128 bytes -- added by a well-meaning contributor
    pub correlation_id: String, // 24 bytes
}

// No size check. The struct silently grew to 280+ bytes.
// Passing it by value in a loop copies all 280 bytes each time.
fn process_events(events: Vec<Event>) {
    for event in events {
        handle(event); // 280-byte copy per iteration
    }
}
```

## Good

```rust
pub struct Event {
    pub id: u64,
    pub timestamp: i64,
    pub source: String,
    pub payload: Vec<u8>,
    pub metadata: HashMap<String, String>,
    pub tags: Vec<String>,
    pub trace_id: Box<[u8; 128]>,  // heap-allocated -- only 8 bytes on stack
    pub correlation_id: String,
}

// Compile-time size assertion -- fails if struct grows beyond budget
const _: () = assert!(
    std::mem::size_of::<Event>() <= 160,
    "Event struct exceeds 160-byte size budget"
);

// Pass by reference in hot paths
fn process_events(events: &[Event]) {
    for event in events {
        handle(event); // passes a pointer, not a copy
    }
}
```

## See Also

- [perf-profile-first](perf-profile-first.md) - Profile before optimising
- [anti-clone-hot-loop](anti-clone-hot-loop.md) - Avoid cloning in hot loops
