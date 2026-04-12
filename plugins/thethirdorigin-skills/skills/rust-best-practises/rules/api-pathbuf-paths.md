# api-pathbuf-paths

> Use PathBuf and Path for filesystem paths instead of String

## Why It Matters

Not all filesystem paths are valid UTF-8. On Unix systems, filenames can contain arbitrary bytes. On Windows, paths use UTF-16 with unpaired surrogates that cannot be represented as Rust strings. Using `String` or `&str` for paths silently rejects valid filesystem entries and creates platform-specific bugs.

`Path` and `PathBuf` handle OS-native path encoding correctly. Accepting `impl AsRef<Path>` makes your API work with `&str`, `String`, `PathBuf`, `&Path`, and `OsString` — all without requiring callers to convert manually.

## Bad

```rust
use std::fs;

pub fn read_config(path: &str) -> Result<Config, io::Error> {
    let content = fs::read_to_string(path)?;
    parse_config(&content)
}

pub fn list_files(dir: &str) -> Result<Vec<String>, io::Error> {
    let mut files = Vec::new();
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        // This panics on non-UTF-8 filenames:
        files.push(entry.file_name().into_string().unwrap());
    }
    Ok(files)
}
```

## Good

```rust
use std::fs;
use std::path::{Path, PathBuf};

pub fn read_config(path: impl AsRef<Path>) -> Result<Config, io::Error> {
    let content = fs::read_to_string(path)?;
    parse_config(&content)
}

pub fn list_files(dir: impl AsRef<Path>) -> Result<Vec<PathBuf>, io::Error> {
    let mut files = Vec::new();
    for entry in fs::read_dir(dir)? {
        files.push(entry?.path());
    }
    Ok(files)
}

// Callers can pass any path-like type:
//   read_config("config.toml");
//   read_config(PathBuf::from("/etc/app/config.toml"));
//   read_config(&path_variable);
```

## References

- [M-STRONG-TYPES](https://rust-lang.github.io/api-guidelines/type-safety.html)

## See Also

- [api-impl-asref](api-impl-asref.md) - Accept impl AsRef for flexible inputs
- [api-newtype-safety](api-newtype-safety.md) - Newtypes for semantic safety
