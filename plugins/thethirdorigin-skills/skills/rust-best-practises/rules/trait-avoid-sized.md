# trait-avoid-sized

> Avoid requiring Self: Sized on trait methods unless necessary

## Why It Matters

Adding where Self: Sized to a trait method excludes it from the vtable, making it unavailable through dyn Trait. This silently breaks downstream code that uses dynamic dispatch. The compiler will not warn when you add the bound — it simply omits the method from the trait object, and callers discover the problem when their code stops compiling.

Most trait methods work perfectly without a Sized bound. Only add it when the method signature genuinely requires it — for example, when returning Self by value, taking self by value in a way that requires knowing the size, or using Self as a generic parameter. For all other methods, leave the bound off and keep the trait object-safe by default.

## Bad

```rust
trait Formatter {
    // Unnecessarily requires Sized — prevents dyn Formatter usage
    fn format(&self, value: &dyn Debug) -> String
    where
        Self: Sized;

    fn name(&self) -> &str
    where
        Self: Sized;
}

// This does not compile because both methods require Sized:
// let formatter: Box<dyn Formatter> = Box::new(JsonFormatter);
// formatter.format(&my_value); // ERROR: method not available
```

## Good

```rust
trait Formatter {
    // Object-safe: no Sized bound needed
    fn format(&self, value: &dyn Debug) -> String;
    fn name(&self) -> &str;

    // Sized bound only where truly necessary (returns Self)
    fn with_indent(self, spaces: usize) -> Self
    where
        Self: Sized;
}

// Works with trait objects — format() and name() are available:
let formatter: Box<dyn Formatter> = Box::new(JsonFormatter::new());
let output = formatter.format(&my_value);

// with_indent() is only available on concrete types, which is correct
// because it returns Self.
let pretty = JsonFormatter::new().with_indent(4);
```

## See Also

- [trait-object-design](trait-object-design.md) - Designing traits for dynamic dispatch
- [trait-dynamic-dispatch](trait-dynamic-dispatch.md) - When to use dyn Trait
