# trait-dynamic-dispatch

> Use dynamic dispatch (dyn Trait) for DI boundaries, plugins, and heterogeneous collections

## Why It Matters

Static dispatch requires the compiler to know every concrete type at compile time. This makes it impossible to store different implementations in the same collection, load plugins at runtime, or inject dependencies without making the entire call chain generic. When you need runtime polymorphism — a Vec of mixed handlers, a plugin registry, or a dependency injection container — dynamic dispatch via dyn Trait is the correct tool.

The overhead of dynamic dispatch is a single pointer indirection per call. For DI boundaries and plugin systems, this cost is negligible compared to the I/O, network calls, or business logic inside each implementation. Trade the micro-optimisation for architectural flexibility.

## Bad

```rust
// Generic plugin system: can only register ONE concrete type per instantiation
struct PluginRegistry<P: Plugin> {
    plugins: Vec<P>,
}

impl<P: Plugin> PluginRegistry<P> {
    fn register(&mut self, plugin: P) {
        self.plugins.push(plugin);
    }
}

// Cannot mix LogPlugin and MetricsPlugin in the same registry.
```

## Good

```rust
struct PluginRegistry {
    plugins: Vec<Box<dyn Plugin>>,
}

impl PluginRegistry {
    fn register(&mut self, plugin: Box<dyn Plugin>) {
        self.plugins.push(plugin);
    }

    fn notify_all(&self, event: &Event) {
        for plugin in &self.plugins {
            plugin.on_event(event);
        }
    }
}

// Usage: mixed concrete types in one collection
let mut registry = PluginRegistry::default();
registry.register(Box::new(LogPlugin::new()));
registry.register(Box::new(MetricsPlugin::new()));
registry.register(Box::new(AuditPlugin::new()));
```

## See Also

- [trait-static-dispatch](trait-static-dispatch.md) - When static dispatch is preferred
- [trait-object-design](trait-object-design.md) - Designing object-safe traits
