# api-impl-asref

> Accept impl AsRef<str> or impl AsRef<Path> for flexible string/path inputs

## Why It Matters

Functions that take `&str` force callers holding a `String` to add `.as_str()`, and callers holding a `PathBuf` cannot call the function at all. Functions that take `&String` are even worse — they prevent passing string literals directly.

Accepting `impl AsRef<str>` or `impl AsRef<Path>` provides zero-cost conversion from all common string and path types. Callers pass whatever they have — `&str`, `String`, `&String`, `PathBuf`, `&Path`, `OsString` — without explicit conversions.

## Bad

```rust
pub fn find_user(name: &str) -> Option<User> {
    db.query_one("SELECT * FROM users WHERE name = ?", &[name])
}

pub fn open_config(path: &str) -> io::Result<Config> {
    let content = fs::read_to_string(path)?;
    toml::from_str(&content).map_err(Into::into)
}

// Callers must convert:
let name: String = get_name();
find_user(&name);          // OK but requires & on owned String
find_user(name.as_str());  // Also works but verbose

let path: PathBuf = dirs::config_dir().unwrap().join("app.toml");
open_config(path.to_str().unwrap()); // Panics on non-UTF-8 paths!
```

## Good

```rust
pub fn find_user(name: impl AsRef<str>) -> Option<User> {
    let name = name.as_ref();
    db.query_one("SELECT * FROM users WHERE name = ?", &[name])
}

pub fn open_config(path: impl AsRef<Path>) -> io::Result<Config> {
    let content = fs::read_to_string(path)?;
    toml::from_str(&content).map_err(Into::into)
}

// Callers pass whatever they have:
find_user("alice");              // &str
find_user(name);                 // String
find_user(&name);                // &String

open_config("config.toml");     // &str
open_config(path);               // PathBuf
open_config(&path);              // &PathBuf
```

## References

- [M-IMPL-ASREF](https://rust-lang.github.io/api-guidelines/flexibility.html)

## See Also

- [api-generic-params](api-generic-params.md) - Generalise parameters with trait bounds
- [api-pathbuf-paths](api-pathbuf-paths.md) - Use Path/PathBuf for filesystem paths
