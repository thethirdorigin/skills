# api-constructors

> Use static inherent methods for constructors: new(), with_capacity()

## Why It Matters

Rust has no built-in constructor syntax. The community convention is to use `new()` as the primary constructor and descriptive names like `with_capacity()`, `from_parts()`, or `empty()` for alternative constructors. Exposing public fields directly as the only way to create a type means any field addition or reorder breaks all callers.

Static inherent methods encapsulate construction logic, enforce invariants, and provide a stable API surface. They also enable returning `Result` for fallible construction without forcing callers to handle bare struct initialization.

## Bad

```rust
pub struct RateLimiter {
    pub max_requests: u32,
    pub window: Duration,
    pub burst: Option<u32>,
}

// Callers construct directly — any field change breaks them:
let limiter = RateLimiter {
    max_requests: 100,
    window: Duration::from_secs(60),
    burst: None,
};

// Adding a new field `strategy: Strategy` forces every call site to update.
```

## Good

```rust
pub struct RateLimiter {
    max_requests: u32,
    window: Duration,
    burst: Option<u32>,
}

impl RateLimiter {
    /// Create a rate limiter with the given request cap per window.
    pub fn new(max_requests: u32, window: Duration) -> Self {
        Self {
            max_requests,
            window,
            burst: None,
        }
    }

    /// Create a rate limiter that allows temporary bursts.
    pub fn with_burst(max_requests: u32, window: Duration, burst: u32) -> Self {
        Self {
            max_requests,
            window,
            burst: Some(burst),
        }
    }
}

// Callers use named constructors:
let limiter = RateLimiter::new(100, Duration::from_secs(60));
let bursty = RateLimiter::with_burst(100, Duration::from_secs(60), 20);

// Adding internal fields is a non-breaking change.
```

## References

- [C-CTOR](https://rust-lang.github.io/api-guidelines/predictability.html#constructors-are-static-inherent-methods-c-ctor)

## See Also

- [api-builder-pattern](api-builder-pattern.md) - Builder pattern for many optional parameters
- [api-private-fields](api-private-fields.md) - Keep fields private for stability
