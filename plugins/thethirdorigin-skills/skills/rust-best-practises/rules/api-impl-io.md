# api-impl-io

> Accept impl Read/Write for I/O functions to enable composability

## Why It Matters

Functions that accept `&mut File` or `&mut TcpStream` are locked to a single I/O backend. They cannot be tested with in-memory buffers, cannot be composed with compression or encryption layers, and cannot write to logging frameworks.

Accepting `impl Read` or `impl Write` decouples your logic from the I/O source. In tests, pass a `Cursor<Vec<u8>>`. In production, pass a `BufWriter<File>`. Wrap with `GzEncoder` for compression. The function remains unchanged across all these scenarios.

## Bad

```rust
use std::fs::File;

pub fn load_manifest(file: &mut File) -> Result<Manifest, Error> {
    let mut content = String::new();
    file.read_to_string(&mut content)?;
    serde_json::from_str(&content).map_err(Into::into)
}

pub fn write_snapshot(file: &mut File, snapshot: &Snapshot) -> Result<(), Error> {
    let json = serde_json::to_vec_pretty(snapshot)?;
    file.write_all(&json)?;
    Ok(())
}

// Tests require real files:
#[test]
fn test_load_manifest() {
    let mut file = File::open("testdata/manifest.json").unwrap(); // brittle
    let manifest = load_manifest(&mut file).unwrap();
    assert_eq!(manifest.version, "1.0");
}
```

## Good

```rust
use std::io::{Read, Write};

pub fn load_manifest(reader: &mut impl Read) -> Result<Manifest, Error> {
    let mut content = String::new();
    reader.read_to_string(&mut content)?;
    serde_json::from_str(&content).map_err(Into::into)
}

pub fn write_snapshot(writer: &mut impl Write, snapshot: &Snapshot) -> Result<(), Error> {
    let json = serde_json::to_vec_pretty(snapshot)?;
    writer.write_all(&json)?;
    Ok(())
}

// Tests use in-memory buffers — no filesystem needed:
#[test]
fn test_load_manifest() {
    let json = br#"{"version": "1.0", "name": "test"}"#;
    let mut cursor = std::io::Cursor::new(json.as_slice());
    let manifest = load_manifest(&mut cursor).unwrap();
    assert_eq!(manifest.version, "1.0");
}

#[test]
fn test_write_snapshot() {
    let mut buffer = Vec::new();
    write_snapshot(&mut buffer, &snapshot).unwrap();
    assert!(String::from_utf8(buffer).unwrap().contains("\"version\""));
}
```

## References

- [M-IMPL-IO](https://rust-lang.github.io/api-guidelines/flexibility.html)

## See Also

- [api-generic-params](api-generic-params.md) - Minimise parameter assumptions with generics
