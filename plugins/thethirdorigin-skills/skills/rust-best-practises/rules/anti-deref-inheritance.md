# anti-deref-inheritance

> Never misuse Deref or DerefMut to simulate struct inheritance

## Why It Matters

Implementing `Deref` so that a wrapper struct auto-dereferences to an inner "parent" struct creates the illusion of inheritance -- method calls silently resolve to the inner type. This is surprising to readers, confuses IDE tooling, and breaks Rust's composition-over-inheritance model. The `Deref` and `DerefMut` traits are designed exclusively for smart-pointer types (`Box`, `Rc`, `Arc`, `MutexGuard`) where the wrapper genuinely represents transparent access to the inner value.

When `Deref` is abused for field delegation, the compiler will happily call parent methods on a child value, but the resulting API is brittle. Adding a method to the inner type can silently shadow a method on the outer type, and trait implementations do not propagate through `Deref` coercions. Explicit delegation or shared traits give you the same convenience with clear, predictable behaviour.

## Bad

```rust
struct Connection {
    socket: TcpStream,
}

impl Connection {
    fn send(&self, data: &[u8]) -> io::Result<usize> {
        // ...
        Ok(data.len())
    }
}

struct PooledConnection {
    inner: Connection,
    pool: Arc<Pool>,
}

impl Deref for PooledConnection {
    type Target = Connection;
    fn deref(&self) -> &Connection {
        &self.inner
    }
}

// Looks like inheritance -- pooled.send(data) silently calls
// Connection::send via implicit deref. Readers have no idea
// where send() is defined.
fn use_pooled(pooled: &PooledConnection) {
    pooled.send(b"hello").unwrap();
}
```

## Good

```rust
struct Connection {
    socket: TcpStream,
}

impl Connection {
    fn send(&self, data: &[u8]) -> io::Result<usize> {
        // ...
        Ok(data.len())
    }
}

struct PooledConnection {
    inner: Connection,
    pool: Arc<Pool>,
}

// Explicit delegation -- clear where the method lives.
impl PooledConnection {
    fn send(&self, data: &[u8]) -> io::Result<usize> {
        self.inner.send(data)
    }

    fn return_to_pool(self) {
        self.pool.return_connection(self.inner);
    }
}

// Or define a shared trait both types implement:
trait Transport {
    fn send(&self, data: &[u8]) -> io::Result<usize>;
}

impl Transport for Connection {
    fn send(&self, data: &[u8]) -> io::Result<usize> {
        // direct send
        Ok(data.len())
    }
}

impl Transport for PooledConnection {
    fn send(&self, data: &[u8]) -> io::Result<usize> {
        self.inner.send(data)
    }
}
```

## References

- [Deref polymorphism anti-pattern](https://rust-unofficial.github.io/patterns/anti_patterns/deref.html)

## See Also

- [api-common-traits](api-common-traits.md) - Implement standard traits for public types
