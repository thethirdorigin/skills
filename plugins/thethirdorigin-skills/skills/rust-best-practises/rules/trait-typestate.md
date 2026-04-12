# trait-typestate

> Encode state transitions in the type system using phantom types

## Why It Matters

Runtime state checks — if !self.connected { panic!("not connected") } — shift invariant enforcement from compile time to runtime. The code compiles successfully even when the caller uses the API incorrectly, and the bug only surfaces when that code path executes. In production, this means a crash.

The typestate pattern uses Rust's type system to make invalid state transitions a compile error. A Connection<Disconnected> simply does not have a send() method. The caller cannot misuse the API because the compiler rejects the code before it ever runs. This is zero-cost: phantom types are erased at compile time and add no runtime overhead.

## Bad

```rust
struct Connection {
    stream: Option<TcpStream>,
    connected: bool,
}

impl Connection {
    fn send(&self, data: &[u8]) -> io::Result<()> {
        if !self.connected {
            panic!("must be connected before sending");
        }
        self.stream.as_ref().unwrap().write_all(data)
    }

    fn disconnect(&mut self) {
        if !self.connected {
            panic!("already disconnected");
        }
        self.stream.take();
        self.connected = false;
    }
}
```

## Good

```rust
use std::marker::PhantomData;

struct Disconnected;
struct Connected;

struct Connection<S> {
    stream: Option<TcpStream>,
    _state: PhantomData<S>,
}

impl Connection<Disconnected> {
    fn connect(addr: &str) -> io::Result<Connection<Connected>> {
        let stream = TcpStream::connect(addr)?;
        Ok(Connection {
            stream: Some(stream),
            _state: PhantomData,
        })
    }
}

impl Connection<Connected> {
    fn send(&self, data: &[u8]) -> io::Result<()> {
        // stream is guaranteed to be Some in the Connected state
        self.stream.as_ref().unwrap().write_all(data)
    }

    fn disconnect(self) -> Connection<Disconnected> {
        // Consumes self, preventing further use as Connected
        Connection {
            stream: None,
            _state: PhantomData,
        }
    }
}

// Compile error: Connection<Disconnected> has no method `send`
// let conn = Connection::<Disconnected>::new();
// conn.send(b"hello"); // does not compile
```

## See Also

- [trait-static-dispatch](trait-static-dispatch.md) - Zero-cost type-level patterns
- [err-panic-bugs-only](err-panic-bugs-only.md) - Why runtime checks are inferior to compile-time guarantees
