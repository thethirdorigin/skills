# trait-static-dispatch

> Use static dispatch (impl Trait / generics) for hot paths — zero runtime cost

## Why It Matters

Static dispatch means the compiler generates a separate, specialised copy of the function for each concrete type that is used. This enables inlining: the compiler can see through the function boundary and optimise the caller and callee as a single unit. There is no vtable pointer, no indirect call, and no branch misprediction penalty.

In performance-sensitive code — tight loops, serialisation pipelines, numeric computation — the difference between a direct call and an indirect vtable lookup can be significant. Static dispatch is the default choice in Rust and should remain the default unless you need runtime polymorphism.

## Bad

```rust
fn process_batch(handler: &dyn EventHandler, events: &[Event]) {
    for event in events {
        // Indirect call through vtable on every iteration.
        // The compiler cannot inline handler.process().
        handler.process(event);
    }
}
```

## Good

```rust
fn process_batch(handler: &impl EventHandler, events: &[Event]) {
    for event in events {
        // Direct call. The compiler monomorphises this function
        // for each concrete EventHandler and inlines process().
        handler.process(event);
    }
}

// Equivalent with explicit generic syntax:
fn process_batch<H: EventHandler>(handler: &H, events: &[Event]) {
    for event in events {
        handler.process(event);
    }
}
```

## See Also

- [trait-dynamic-dispatch](trait-dynamic-dispatch.md) - When dynamic dispatch is the right choice
- [trait-object-design](trait-object-design.md) - Designing traits that work with both dispatch modes
