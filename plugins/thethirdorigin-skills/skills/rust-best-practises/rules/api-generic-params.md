# api-generic-params

> Minimise assumptions about parameters using generics

## Why It Matters

Functions that accept concrete types force callers into specific implementations. A logging function that takes `&mut File` cannot write to a network socket, an in-memory buffer, or stderr. By accepting a trait bound like `impl Write`, the same function works with any I/O destination.

Generic parameters make functions composable, testable, and reusable. In tests, you pass a `Vec<u8>` instead of creating temporary files. In production, you pass a `BufWriter<File>` for performance. The function does not need to change.

## Bad

```rust
use std::fs::File;
use std::collections::HashMap;

pub fn write_report(file: &mut File, data: &HashMap<String, u64>) -> io::Result<()> {
    for (key, value) in data {
        writeln!(file, "{key}: {value}")?;
    }
    Ok(())
}

// Cannot use with:
// - Vec<u8> for testing
// - BufWriter for performance
// - TcpStream for network output
// - BTreeMap or custom data sources
```

## Good

```rust
use std::io::Write;

pub fn write_report(
    writer: &mut impl Write,
    data: &impl IntoIterator<Item = (&str, u64)>,
) -> io::Result<()> {
    for (key, value) in data {
        writeln!(writer, "{key}: {value}")?;
    }
    Ok(())
}

// Works with any writer and any iterable data source:
//   write_report(&mut file, &hash_map);
//   write_report(&mut buffer, &btree_map);
//   write_report(&mut io::stdout(), &vec_of_tuples);
```

## References

- [C-GENERIC](https://rust-lang.github.io/api-guidelines/flexibility.html#functions-minimize-assumptions-about-parameters-by-using-generics-c-generic)

## See Also

- [api-impl-asref](api-impl-asref.md) - AsRef for flexible string/path inputs
- [api-impl-io](api-impl-io.md) - Read/Write for I/O composability
