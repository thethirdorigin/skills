# lint-cargo-audit

> Run cargo-audit for security vulnerability scanning

## Why It Matters

Known vulnerabilities in outdated dependencies are among the easiest attack vectors. A single transitive dependency with a published CVE can compromise your entire application. The RustSec advisory database tracks these vulnerabilities, and `cargo audit` checks your dependency tree against it.

Running `cargo audit` in CI or as a scheduled job catches vulnerable versions before they reach production. When a new advisory is published, the next CI run flags the affected crate, giving you time to update before the vulnerability is exploited.

## Bad

```rust
// Cargo.toml -- dependencies never audited for known vulnerabilities
// [dependencies]
// hyper = "0.14.18"     # has a known DoS vulnerability
// regex = "1.5.4"       # has a known ReDoS vulnerability
// chrono = "0.4.19"     # depends on a vulnerable version of time

// No CI step checks for advisories.
// Vulnerabilities discovered only after a security incident.
```

## Good

```rust
// CI pipeline includes:
// cargo install cargo-audit
// cargo audit

// Output:
// Crate:     hyper
// Version:   0.14.18
// Warning:   RUSTSEC-2023-0034
// Solution:  Upgrade to >= 0.14.27
//
// 1 vulnerability found!

// For automated dependency updates:
// cargo audit fix  (applies compatible version bumps)

// For continuous monitoring, add as a scheduled CI job:
// name: Security Audit
// schedule:
//   cron: "0 8 * * 1"  # Every Monday at 8 AM
// steps:
//   - cargo audit --deny warnings
```

## See Also

- [lint-clippy-all](lint-clippy-all.md) - Static analysis in CI
- [crate-workspace-deps](crate-workspace-deps.md) - Centralise dependency versions
