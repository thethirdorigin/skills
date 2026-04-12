# trait-object-design

> Design trait methods to work naturally with trait objects

## Why It Matters

A trait with generic methods — fn process<T: Serialize>(&self, data: T) — cannot be used as dyn Trait because the compiler cannot generate a vtable for an unbounded set of monomorphised methods. This is called "object safety" and it is one of the most common stumbling blocks in Rust trait design.

If you anticipate that your trait will be used behind dyn (for DI, plugin systems, or heterogeneous collections), design its methods to be object-safe from the start. Use trait objects or type erasure (e.g., erased_serde, Box<dyn Any>) for parameters that would otherwise require generics. Retrofitting object safety later often requires breaking API changes.

## Bad

```rust
trait Processor {
    // Generic method makes the entire trait non-object-safe.
    // Cannot use Box<dyn Processor>.
    fn process<T: Serialize + Send>(&self, input: T) -> Vec<u8>;

    // Returning Self also breaks object safety.
    fn clone_processor(&self) -> Self;
}

// This does not compile:
// let processors: Vec<Box<dyn Processor>> = vec![...];
```

## Good

```rust
trait Processor {
    // Accept a trait object instead of a generic parameter.
    fn process(&self, input: &dyn erased_serde::Serialize) -> Vec<u8>;

    // Return a boxed trait object instead of Self.
    fn clone_processor(&self) -> Box<dyn Processor>;
}

// Now this works:
let processors: Vec<Box<dyn Processor>> = vec![
    Box::new(JsonProcessor),
    Box::new(CborProcessor),
];

for processor in &processors {
    let output = processor.process(&my_data);
}
```

## See Also

- [trait-dynamic-dispatch](trait-dynamic-dispatch.md) - When to use dyn Trait
- [trait-avoid-sized](trait-avoid-sized.md) - Avoiding unnecessary Sized constraints
