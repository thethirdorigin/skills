# api-object-safe

> Design traits to be object-safe when trait objects may be useful

## Why It Matters

A trait that is not object-safe cannot be used as `dyn Trait`. This prevents dynamic dispatch, heterogeneous collections, dependency injection containers, and plugin architectures. The most common causes of non-object-safety are generic methods, methods returning `Self`, and methods with `Sized` bounds.

When designing a trait that may be used as a trait object, avoid generic type parameters on methods. Use `&dyn Trait` parameters or associated types instead. If some methods must remain non-object-safe, provide them as default methods with a `where Self: Sized` bound so the trait itself remains object-safe.

## Bad

```rust
pub trait Serializer {
    // Generic method prevents `dyn Serializer`
    fn serialize<T: Serialize>(&self, value: &T) -> Vec<u8>;

    // Returning Self prevents `dyn Serializer`
    fn with_options(self, pretty: bool) -> Self;
}

// Cannot create heterogeneous collections:
// let serializers: Vec<Box<dyn Serializer>> = vec![...]; // ERROR
```

## Good

```rust
pub trait Serializer {
    /// Serialize an already-erased value.
    fn serialize(&self, value: &dyn erased_serde::Serialize) -> Vec<u8>;

    /// Configure options, returning a boxed trait object.
    fn with_options(&self, pretty: bool) -> Box<dyn Serializer>;
}

// Methods that cannot be object-safe are gated with Sized:
pub trait Codec: Serializer {
    /// Only available on concrete types, not through dyn Codec.
    fn specialized_encode<T: Encode>(&self, value: &T) -> Vec<u8>
    where
        Self: Sized;
}

// Heterogeneous collections work:
let serializers: Vec<Box<dyn Serializer>> = vec![
    Box::new(JsonSerializer),
    Box::new(MsgpackSerializer),
];

for s in &serializers {
    let bytes = s.serialize(&my_data);
}
```

## References

- [C-OBJECT](https://rust-lang.github.io/api-guidelines/flexibility.html#traits-are-object-safe-if-they-may-be-useful-as-a-trait-object-c-object)

## See Also

- [api-di-hierarchy](api-di-hierarchy.md) - When to use dyn Trait vs generics
- [api-sealed-trait](api-sealed-trait.md) - Seal traits to control implementations
