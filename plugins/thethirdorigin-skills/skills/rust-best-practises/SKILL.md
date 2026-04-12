---
name: rust-best-practises
description: >
  Rust coding standards, API design, and best practices with 121 rules across 16 categories.
  Use when writing, reviewing, or refactoring Rust code. Covers error handling, ownership,
  API design, async patterns, naming, testing, documentation, linting, performance, and
  common anti-patterns. References Rust API Guidelines (C-*) and Microsoft Rust Guidelines (M-*).
triggers:
  - writing Rust code
  - working on backend
  - Rust review
  - creating a new Rust module
  - backend service development
  - implementing a domain entity
  - adding an API endpoint
  - Rust refactoring
  - Rust error handling
  - Rust testing
---

# Rust Best Practices

<context>
You are a senior Rust engineer focused on writing safe, performant, idiomatic Rust code. Before implementing, always discover the project's architecture, workspace structure, and existing patterns. Match them — do not impose your own preferences.

This skill references two authoritative guideline systems:
- **C-*** rules from the Rust API Guidelines (rust-lang.github.io/api-guidelines)
- **M-*** rules from the Microsoft Rust Guidelines (microsoft.github.io/rust-guidelines)

**Companion skill**: **rust-skills** (179 concrete rules with bad→good code examples across memory optimisation, compiler tuning, async patterns, testing, and anti-patterns). Installed alongside this skill in the thethirdorigin marketplace.
</context>

## When to Apply

Reference these guidelines when:
- Writing new Rust functions, structs, or modules
- Designing public APIs for libraries or services
- Implementing error handling or async code
- Reviewing code for ownership, naming, or safety issues
- Refactoring existing Rust code
- Setting up linting, testing, or logging

## Architecture Discovery

<instructions>
Before writing any Rust code, perform these discovery steps:

- Read the root `Cargo.toml` to identify workspace members and shared dependencies
- Identify the architecture pattern in use (hexagonal, layered, flat, microservices)
- Map the layer boundaries: which modules are domain, application, infrastructure, presentation?
- Identify the dependency injection pattern: constructor injection, trait objects, concrete types?
- Find existing error types and their conversion patterns (From impls)
- Check for existing port/trait definitions that your code should implement or use
- Identify the async runtime (tokio, async-std) and its patterns in the codebase
- Check `[workspace.lints]` and `[workspace.dependencies]` sections for project-wide conventions
</instructions>

---

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Error Handling | CRITICAL | `err-` | 8 |
| 2 | Ownership and Borrowing | CRITICAL | `own-` | 6 |
| 3 | API Design | HIGH | `api-` | 20 |
| 4 | Async Patterns | HIGH | `async-` | 6 |
| 5 | Unsafe Code | HIGH | `unsafe-` | 5 |
| 6 | Generics and Traits | MEDIUM | `trait-` | 7 |
| 7 | Naming Conventions | MEDIUM | `name-` | 10 |
| 8 | Testing | MEDIUM | `test-` | 7 |
| 9 | Documentation | MEDIUM | `doc-` | 10 |
| 10 | Iterators and Functional Chains | MEDIUM | `iter-` | 5 |
| 11 | Performance | MEDIUM | `perf-` | 6 |
| 12 | Static Verification and Linting | LOW | `lint-` | 7 |
| 13 | Code Formatting | LOW | `fmt-` | 8 |
| 14 | Structured Logging | LOW | `log-` | 5 |
| 15 | Dependencies and Crate Design | LOW | `crate-` | 6 |
| 16 | Anti-patterns | REFERENCE | `anti-` | 5 |

---

## Quick Reference

### 1. Error Handling (CRITICAL)

- [`err-result-recoverable`](rules/err-result-recoverable.md) - Use `Result<T, E>` for all recoverable errors
- [`err-question-mark`](rules/err-question-mark.md) - Use `?` for propagation, not match-and-rewrap
- [`err-panic-bugs-only`](rules/err-panic-bugs-only.md) - Reserve panic for programming bugs only
- [`err-canonical-structs`](rules/err-canonical-structs.md) - Library errors: situation-specific structs with backtrace
- [`err-anyhow-app`](rules/err-anyhow-app.md) - Applications use `anyhow`; libraries use concrete types
- [`err-context-chain`](rules/err-context-chain.md) - Error variants carry context, not raw inner errors
- [`err-match-existing`](rules/err-match-existing.md) - Match existing error conversion patterns in the codebase
- [`err-test-error-paths`](rules/err-test-error-paths.md) - Test error paths explicitly

### 2. Ownership and Borrowing (CRITICAL)

- [`own-borrow-prefer`](rules/own-borrow-prefer.md) - Borrow (`&T`, `&mut T`) over clone where possible
- [`own-copy-value-types`](rules/own-copy-value-types.md) - Pass `Copy` types by value
- [`own-arc-async`](rules/own-arc-async.md) - Use `Arc<T>` for shared ownership across async tasks
- [`own-arc-dyn-trait`](rules/own-arc-dyn-trait.md) - Use `Arc<dyn Trait + Send + Sync>` for DI trait objects
- [`own-move-intentional`](rules/own-move-intentional.md) - Prefer moves over clones for ownership transfer
- [`own-detect-cloning`](rules/own-detect-cloning.md) - Detect unnecessary cloning through review and profiling

### 3. API Design (HIGH)

- [`api-common-traits`](rules/api-common-traits.md) - Eagerly implement `Debug`, `Clone`, `PartialEq`, `Eq`, `Hash`
- [`api-debug-display`](rules/api-debug-display.md) - All public types implement `Debug`; user-facing types implement `Display`
- [`api-send-sync`](rules/api-send-sync.md) - Public types should be `Send` where possible
- [`api-conversion-traits`](rules/api-conversion-traits.md) - Implement `From`, `AsRef`, `AsMut` for conversions
- [`api-newtype-safety`](rules/api-newtype-safety.md) - Use newtypes for type-safe distinctions
- [`api-enum-over-bool`](rules/api-enum-over-bool.md) - Use enums instead of `bool` parameters
- [`api-pathbuf-paths`](rules/api-pathbuf-paths.md) - Use `PathBuf`/`Path` for filesystem paths
- [`api-builder-pattern`](rules/api-builder-pattern.md) - Builder pattern for 4+ optional parameters
- [`api-method-receiver`](rules/api-method-receiver.md) - Functions with a clear receiver are methods
- [`api-no-out-params`](rules/api-no-out-params.md) - Return values instead of out-parameters
- [`api-constructors`](rules/api-constructors.md) - Static inherent methods: `new()`, `with_capacity()`
- [`api-generic-params`](rules/api-generic-params.md) - Minimise assumptions with generics
- [`api-impl-asref`](rules/api-impl-asref.md) - Accept `impl AsRef<T>` for flexible inputs
- [`api-impl-io`](rules/api-impl-io.md) - Accept `impl Read`/`impl Write` for I/O functions
- [`api-object-safe`](rules/api-object-safe.md) - Design traits to be object-safe when useful
- [`api-di-hierarchy`](rules/api-di-hierarchy.md) - Concrete > generics > `dyn Trait` for DI
- [`api-essential-inherent`](rules/api-essential-inherent.md) - Essential functionality is inherent
- [`api-service-clone`](rules/api-service-clone.md) - Service types use `Arc<Inner>` for cheap `Clone`
- [`api-private-fields`](rules/api-private-fields.md) - Struct fields private with accessor methods
- [`api-sealed-trait`](rules/api-sealed-trait.md) - Seal traits to prevent external implementations

### 4. Async Patterns (HIGH)

- [`async-all-io`](rules/async-all-io.md) - All I/O operations are async
- [`async-trait-usage`](rules/async-trait-usage.md) - Use `async_trait` or native async traits
- [`async-no-block`](rules/async-no-block.md) - Never block in async context
- [`async-send-sync`](rules/async-send-sync.md) - Trait objects in async need `Send + Sync` bounds
- [`async-yield-points`](rules/async-yield-points.md) - Long CPU tasks include yield points
- [`async-futures-send`](rules/async-futures-send.md) - Validate generated futures are `Send`

### 5. Unsafe Code (HIGH)

- [`unsafe-reserve-ffi`](rules/unsafe-reserve-ffi.md) - Reserve unsafe for FFI, novel abstractions, measured perf
- [`unsafe-implies-ub`](rules/unsafe-implies-ub.md) - Unsafe implies UB risk, not general "danger"
- [`unsafe-soundness`](rules/unsafe-soundness.md) - Safe functions must never allow undefined behaviour
- [`unsafe-safety-docs`](rules/unsafe-safety-docs.md) - Document safety contracts with `// SAFETY:` comments
- [`unsafe-pass-miri`](rules/unsafe-pass-miri.md) - Validate unsafe code with Miri

### 6. Generics and Traits (MEDIUM)

- [`trait-static-dispatch`](rules/trait-static-dispatch.md) - Static dispatch for hot paths — zero runtime cost
- [`trait-dynamic-dispatch`](rules/trait-dynamic-dispatch.md) - Dynamic dispatch for DI, plugins, heterogeneous collections
- [`trait-typestate`](rules/trait-typestate.md) - Encode state transitions in the type system
- [`trait-object-design`](rules/trait-object-design.md) - Design trait methods to work with trait objects
- [`trait-single-responsibility`](rules/trait-single-responsibility.md) - Keep traits focused, single responsibility
- [`trait-supertraits`](rules/trait-supertraits.md) - Use supertraits to compose requirements
- [`trait-avoid-sized`](rules/trait-avoid-sized.md) - Avoid `Self: Sized` unless necessary

### 7. Naming Conventions (MEDIUM)

- [`name-types-pascal`](rules/name-types-pascal.md) - `PascalCase` for types, traits, enums
- [`name-funcs-snake`](rules/name-funcs-snake.md) - `snake_case` for functions, methods, modules
- [`name-consts-screaming`](rules/name-consts-screaming.md) - `SCREAMING_SNAKE_CASE` for constants
- [`name-lifetime-short`](rules/name-lifetime-short.md) - Short lowercase lifetimes: `'a`, `'de`, `'src`
- [`name-as-cheap`](rules/name-as-cheap.md) - `as_` prefix for cheap reference conversions
- [`name-to-expensive`](rules/name-to-expensive.md) - `to_` prefix for expensive conversions
- [`name-into-ownership`](rules/name-into-ownership.md) - `into_` prefix for ownership transfer
- [`name-iter-convention`](rules/name-iter-convention.md) - `iter()`/`iter_mut()`/`into_iter()` convention
- [`name-no-get-prefix`](rules/name-no-get-prefix.md) - No `get_` prefix for simple getters
- [`name-no-weasel`](rules/name-no-weasel.md) - Remove meaningless terms: Service, Manager, Handler

### 8. Testing (MEDIUM)

- [`test-cfg-module`](rules/test-cfg-module.md) - Unit tests in `#[cfg(test)] mod tests`
- [`test-integration-dir`](rules/test-integration-dir.md) - Integration tests in `tests/` directory
- [`test-descriptive-names`](rules/test-descriptive-names.md) - Descriptive test names explaining what is verified
- [`test-error-paths`](rules/test-error-paths.md) - Test error paths, not just happy paths
- [`test-mockable-design`](rules/test-mockable-design.md) - Design for testability with traits
- [`test-test-util-feature`](rules/test-test-util-feature.md) - Gate test utilities behind `test-util` feature
- [`test-doc-examples`](rules/test-doc-examples.md) - Keep doc examples as executable tests

### 9. Documentation (MEDIUM)

- [`doc-summary-sentence`](rules/doc-summary-sentence.md) - Summary sentence under 15 words
- [`doc-examples-runnable`](rules/doc-examples-runnable.md) - Include runnable `# Examples` section
- [`doc-errors-section`](rules/doc-errors-section.md) - Document errors with `# Errors` section
- [`doc-panics-section`](rules/doc-panics-section.md) - Document panics with `# Panics` section
- [`doc-safety-section`](rules/doc-safety-section.md) - Document safety with `# Safety` section
- [`doc-module-docs`](rules/doc-module-docs.md) - Module documentation with `//!`
- [`doc-question-mark`](rules/doc-question-mark.md) - Use `?` in examples, not `.unwrap()`
- [`doc-intra-links`](rules/doc-intra-links.md) - Use intra-doc links for cross-references
- [`doc-explain-why`](rules/doc-explain-why.md) - Comments explain why, not what
- [`doc-no-living-comments`](rules/doc-no-living-comments.md) - Do not maintain comments that duplicate code

### 10. Iterators and Functional Chains (MEDIUM)

- [`iter-chains`](rules/iter-chains.md) - Prefer iterator chains over explicit for loops
- [`iter-into-consume`](rules/iter-into-consume.md) - Use `into_iter()` when consuming the collection
- [`iter-zero-cost`](rules/iter-zero-cost.md) - Trust zero-cost abstractions for iterators
- [`iter-option-combinators`](rules/iter-option-combinators.md) - Use `Option`/`Result` combinators
- [`iter-no-intermediate-vec`](rules/iter-no-intermediate-vec.md) - Avoid collecting intermediate iterators

### 11. Performance (MEDIUM)

- [`perf-profile-first`](rules/perf-profile-first.md) - Profile before optimising
- [`perf-benchmark-hotpaths`](rules/perf-benchmark-hotpaths.md) - Create benchmarks around hot paths
- [`perf-partition-throughput`](rules/perf-partition-throughput.md) - Partition work for throughput
- [`perf-monitor-struct-sizes`](rules/perf-monitor-struct-sizes.md) - Monitor struct sizes for stack optimisation
- [`perf-zero-cost-trust`](rules/perf-zero-cost-trust.md) - Trust compiler for iterator/generic optimisation
- [`perf-connection-pool`](rules/perf-connection-pool.md) - Use connection pooling for database and HTTP

### 12. Static Verification and Linting (LOW)

- [`lint-clippy-all`](rules/lint-clippy-all.md) - Run `cargo clippy --all-targets --all-features`
- [`lint-fix-root-cause`](rules/lint-fix-root-cause.md) - Fix root cause, do not silence with `#[allow]`
- [`lint-expect-over-allow`](rules/lint-expect-over-allow.md) - Use `#[expect]` with reason over `#[allow]`
- [`lint-enable-warnings`](rules/lint-enable-warnings.md) - Enable key compiler lints at workspace level
- [`lint-cargo-fmt`](rules/lint-cargo-fmt.md) - Run `cargo fmt --check` in CI
- [`lint-cargo-audit`](rules/lint-cargo-audit.md) - Run `cargo-audit` for vulnerability scanning
- [`lint-cargo-hack`](rules/lint-cargo-hack.md) - Test feature combinations with `cargo-hack`

### 13. Code Formatting (LOW)

- [`fmt-four-spaces`](rules/fmt-four-spaces.md) - 4-space indentation, never tabs
- [`fmt-line-width`](rules/fmt-line-width.md) - Maximum 100 character line width
- [`fmt-trailing-commas`](rules/fmt-trailing-commas.md) - Trailing commas in multi-line lists
- [`fmt-single-line-small`](rules/fmt-single-line-small.md) - Single-line format for small items
- [`fmt-no-trailing-whitespace`](rules/fmt-no-trailing-whitespace.md) - No trailing whitespace
- [`fmt-comment-space`](rules/fmt-comment-space.md) - Single space after comment sigils
- [`fmt-blank-lines`](rules/fmt-blank-lines.md) - Separate items with 0-1 blank lines
- [`fmt-cargo-fmt`](rules/fmt-cargo-fmt.md) - Run `cargo fmt` before every commit

### 14. Structured Logging (LOW)

- [`log-structured-events`](rules/log-structured-events.md) - Structured events with named properties
- [`log-defer-formatting`](rules/log-defer-formatting.md) - Defer string formatting via templates
- [`log-hierarchical-naming`](rules/log-hierarchical-naming.md) - Hierarchical dot-notation naming
- [`log-otel-conventions`](rules/log-otel-conventions.md) - Follow OpenTelemetry semantic conventions
- [`log-redact-sensitive`](rules/log-redact-sensitive.md) - Redact sensitive data in logs

### 15. Dependencies and Crate Design (LOW)

- [`crate-workspace-deps`](rules/crate-workspace-deps.md) - Use `{ workspace = true }` for shared dependencies
- [`crate-features-additive`](rules/crate-features-additive.md) - Features must be additive
- [`crate-smaller-focused`](rules/crate-smaller-focused.md) - Prefer smaller, focused crates
- [`crate-avoid-statics`](rules/crate-avoid-statics.md) - Avoid module-level statics
- [`crate-no-glob-reexport`](rules/crate-no-glob-reexport.md) - Re-export items individually, not via glob
- [`crate-tier1-oobe`](rules/crate-tier1-oobe.md) - Libraries work on all Tier 1 platforms

### 16. Anti-patterns (REFERENCE)

- [`anti-clone-hot-loop`](rules/anti-clone-hot-loop.md) - Avoid cloning large structures in hot loops
- [`anti-silence-clippy`](rules/anti-silence-clippy.md) - Fix clippy warnings, do not blanket-suppress
- [`anti-monolith-function`](rules/anti-monolith-function.md) - Split monolithic multi-responsibility functions
- [`anti-primitive-obsession`](rules/anti-primitive-obsession.md) - Use newtypes where raw strings/ints are used
- [`anti-bool-params`](rules/anti-bool-params.md) - Replace boolean parameters with enums

---

## How to Use

Reference these guidelines by task type:

| Task | Primary Categories |
|------|-------------------|
| New function | `err-`, `own-`, `name-` |
| New struct/API | `api-`, `name-`, `doc-` |
| Async code | `async-`, `own-` |
| Error handling | `err-`, `api-` |
| Trait design | `trait-`, `api-` |
| Testing | `test-`, `err-` |
| Performance tuning | `perf-`, `own-`, `iter-` |
| Code review | `anti-`, `lint-`, `fmt-` |
| Logging | `log-` |
| Unsafe code | `unsafe-` |
| Crate design | `crate-`, `api-` |

### Rule Application

1. **Check relevant category** based on task type
2. **Apply rules** with matching prefix
3. **Prioritise** CRITICAL > HIGH > MEDIUM > LOW > REFERENCE
4. **Read rule files** in `rules/` for detailed examples

---

## References

- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) — Official Rust API design checklist (C-* rules)
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) — 60+ rules covering error handling, documentation, testing, safety, performance (M-* rules)
- [Microsoft Rust Guidelines (Agent-Optimised)](https://microsoft.github.io/rust-guidelines/agents/all.txt) — Full guideline text in agent-consumable format
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) — Official formatting and style conventions
- [Apollo GraphQL Rust Best Practices](https://github.com/apollographql/rust-best-practices) — Production Rust patterns from Apollo Engineering
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce) — Clean code principles applied to Rust
