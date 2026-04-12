# crate-tier1-oobe

> Libraries must work out of the box on all Tier 1 platforms

## Why It Matters

Rust supports Windows, macOS, and Linux as Tier 1 platforms, meaning users on these platforms expect crates to compile and work without special setup. A library that only works on Linux because it uses Unix-specific system calls alienates a large portion of the Rust ecosystem.

Platform-specific code should be isolated behind `cfg` attributes with fallbacks or compile-time errors that clearly explain the platform requirement. When possible, use cross-platform abstractions from the standard library or well-maintained crates instead of platform-specific APIs.

## Bad

```rust
use std::os::unix::fs::PermissionsExt;

pub fn make_executable(path: &Path) -> std::io::Result<()> {
    // Only compiles on Unix -- Windows users get a build error
    // with no explanation or alternative
    let mut perms = std::fs::metadata(path)?.permissions();
    perms.set_mode(0o755);
    std::fs::set_permissions(path, perms)
}

pub fn get_home_dir() -> PathBuf {
    // Assumes Unix environment variable
    PathBuf::from(std::env::var("HOME").expect("HOME not set"))
}
```

## Good

```rust
use std::path::{Path, PathBuf};

pub fn make_executable(path: &Path) -> std::io::Result<()> {
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;
        let mut perms = std::fs::metadata(path)?.permissions();
        perms.set_mode(0o755);
        std::fs::set_permissions(path, perms)?;
    }

    #[cfg(windows)]
    {
        // Windows determines executability by file extension,
        // so this is a no-op. Document this behavior.
    }

    #[cfg(not(any(unix, windows)))]
    {
        compile_error!("make_executable is not implemented for this platform");
    }

    Ok(())
}

pub fn get_home_dir() -> Option<PathBuf> {
    // Cross-platform: works on Windows, macOS, and Linux
    dirs::home_dir()
}
```

## References

- [M-OOBE](https://rust-lang.github.io/api-guidelines/checklist.html)

## See Also

- [crate-features-additive](crate-features-additive.md) - Features must be additive
- [lint-cargo-hack](lint-cargo-hack.md) - Test feature and target combinations
