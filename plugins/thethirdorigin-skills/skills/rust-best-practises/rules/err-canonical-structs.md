# err-canonical-structs

> Design library error types as situation-specific structs with backtrace and source chain

## Why It Matters

A bare enum with wrapped inner errors loses critical debugging information. When a user reports "I/O error: permission denied," you need to know which file, which operation, and where in the call stack the failure originated. Without backtraces, developers resort to adding println! statements and recompiling to hunt down errors.

Rich error types with backtrace capture, a source chain via std::error::Error::source(), an ErrorKind enum for programmatic matching, and convenience is_xxx() helpers give callers everything they need: display for humans, classification for code, and trace for debugging.

## Bad

```rust
#[derive(Debug)]
pub enum Error {
    Io(io::Error),
    Parse(String),
    Config(String),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Error::Io(e) => write!(f, "{e}"),
            Error::Parse(msg) => write!(f, "{msg}"),
            Error::Config(msg) => write!(f, "{msg}"),
        }
    }
}

// No backtrace, no context about what operation failed,
// no way for callers to distinguish sub-variants of Io.
```

## Good

```rust
use std::backtrace::Backtrace;

#[derive(Debug)]
pub struct Error {
    kind: ErrorKind,
    backtrace: Backtrace,
}

#[derive(Debug)]
pub enum ErrorKind {
    ReadConfig {
        path: PathBuf,
        source: io::Error,
    },
    ParseConfig {
        path: PathBuf,
        line: usize,
        message: String,
    },
    MissingField {
        field: &'static str,
    },
}

impl Error {
    pub fn kind(&self) -> &ErrorKind {
        &self.kind
    }

    pub fn is_not_found(&self) -> bool {
        matches!(
            &self.kind,
            ErrorKind::ReadConfig { source, .. }
                if source.kind() == io::ErrorKind::NotFound
        )
    }

    pub fn backtrace(&self) -> &Backtrace {
        &self.backtrace
    }
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.kind {
            ErrorKind::ReadConfig { path, source } => {
                write!(f, "failed to read config at {}: {source}", path.display())
            }
            ErrorKind::ParseConfig { path, line, message } => {
                write!(f, "parse error in {} at line {line}: {message}", path.display())
            }
            ErrorKind::MissingField { field } => {
                write!(f, "missing required field '{field}'")
            }
        }
    }
}
```

## References

- [M-ERRORS-CANONICAL-STRUCTS](https://rust-lang.github.io/api-guidelines/documentation.html) — Library error types should be canonical structs with backtrace and source

## See Also

- [err-context-chain](err-context-chain.md) - Adding context to error variants
- [err-anyhow-app](err-anyhow-app.md) - When to use anyhow instead of custom types
