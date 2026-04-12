# doc-module-docs

> Add //! module documentation to all public library modules

## Why It Matters

Module-level documentation is the entry point for users navigating your library in rustdoc. When a user clicks on a module name in the sidebar, they see the //! documentation first. Without it, they land on a bare list of types and functions with no explanation of the module's purpose, scope, or relationship to other modules.

Good module docs answer three questions: what does this module contain, when should I use it, and how does it relate to other parts of the library. A few sentences at the top of each public module file dramatically improve discoverability and reduce the time users spend hunting for the right type.

## Bad

```rust
// src/auth/mod.rs

use crate::db::UserRepo;
use crate::crypto::Hasher;

pub struct SessionManager { /* ... */ }
pub struct AuthToken { /* ... */ }
pub fn verify_credentials(/* ... */) { /* ... */ }

// Users see a bare list of items with no explanation of what
// "auth" means in this library or how to get started.
```

## Good

```rust
// src/auth/mod.rs

//! User authentication and session management.
//!
//! This module provides credential verification, session token generation,
//! and session lifecycle management. It is the primary entry point for
//! authenticating users against the [`UserRepo`](crate::db::UserRepo).
//!
//! # Getting Started
//!
//! ```
//! use mylib::auth::SessionManager;
//!
//! let manager = SessionManager::new(user_repo, hasher);
//! let token = manager.authenticate("alice", "s3cret")?;
//! # Ok::<(), mylib::auth::AuthError>(())
//! ```

use crate::db::UserRepo;
use crate::crypto::Hasher;

pub struct SessionManager { /* ... */ }
pub struct AuthToken { /* ... */ }
pub fn verify_credentials(/* ... */) { /* ... */ }
```

## References

- [M-MODULE-DOCS](https://rust-lang.github.io/api-guidelines/documentation.html) — Every public module should have module-level documentation

## See Also

- [doc-summary-sentence](doc-summary-sentence.md) - Writing concise summary lines
- [doc-examples-runnable](doc-examples-runnable.md) - Including tested examples in docs
