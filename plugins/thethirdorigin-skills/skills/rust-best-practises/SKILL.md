---
name: rust-best-practises
description: >
  Comprehensive Rust coding standards, API design, and best practices with ~280 rules
  across 20 categories. Use when writing, reviewing, or refactoring Rust code. Covers
  error handling, ownership, memory optimisation, API design, async patterns, compiler
  optimisation, type safety, naming, testing, documentation, performance, unsafe code,
  generics, iterators, project structure, linting, formatting, logging, crate design,
  and common anti-patterns.
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
  - Rust performance
  - memory optimisation
  - Rust async
---

# Rust Best Practices

<context>
You are a senior Rust engineer focused on writing safe, performant, idiomatic Rust code. Before implementing, always discover the project's architecture, workspace structure, and existing patterns. Match them — do not impose your own preferences.

This is the single comprehensive Rust skill. It merges coding standards (API guidelines, naming, safety) with concrete optimisation rules (memory, compiler, performance) and anti-patterns into one unified reference.
</context>

## When to Apply

Reference these guidelines when:
- Writing new Rust functions, structs, or modules
- Designing public APIs for libraries or services
- Implementing error handling or async code
- Reviewing code for ownership, naming, or safety issues
- Refactoring existing Rust code
- Optimising memory usage or reducing allocations
- Tuning performance for hot paths
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
| 1 | Error Handling | CRITICAL | `err-` | 17 |
| 2 | Ownership and Borrowing | CRITICAL | `own-` | 21 |
| 3 | Memory Optimisation | CRITICAL | `mem-` | 15 |
| 4 | API Design | HIGH | `api-` | 31 |
| 5 | Async Patterns | HIGH | `async-` | 21 |
| 6 | Compiler Optimisation | HIGH | `opt-` | 12 |
| 7 | Unsafe Code | HIGH | `unsafe-` | 6 |
| 8 | Generics and Traits | MEDIUM | `trait-` | 8 |
| 9 | Type Safety | MEDIUM | `type-` | 10 |
| 10 | Naming Conventions | MEDIUM | `name-` | 19 |
| 11 | Testing | MEDIUM | `test-` | 18 |
| 12 | Documentation | MEDIUM | `doc-` | 16 |
| 13 | Iterators and Functional Chains | MEDIUM | `iter-` | 6 |
| 14 | Performance Patterns | MEDIUM | `perf-` | 17 |
| 15 | Project Structure | LOW | `proj-` | 11 |
| 16 | Static Verification and Linting | LOW | `lint-` | 18 |
| 17 | Code Formatting | LOW | `fmt-` | 8 |
| 18 | Structured Logging | LOW | `log-` | 5 |
| 19 | Dependencies and Crate Design | LOW | `crate-` | 6 |
| 20 | Anti-patterns | REFERENCE | `anti-` | 22 |

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
- [`err-thiserror-lib`](rules/err-thiserror-lib.md) - Use `thiserror` for library error types
- [`err-result-over-panic`](rules/err-result-over-panic.md) - Return `Result`, don't panic on expected errors
- [`err-no-unwrap-prod`](rules/err-no-unwrap-prod.md) - Never use `.unwrap()` in production code
- [`err-expect-bugs-only`](rules/err-expect-bugs-only.md) - Use `.expect()` only for programming errors
- [`err-from-impl`](rules/err-from-impl.md) - Use `#[from]` for automatic error conversion
- [`err-source-chain`](rules/err-source-chain.md) - Use `#[source]` to chain underlying errors
- [`err-lowercase-msg`](rules/err-lowercase-msg.md) - Error messages: lowercase, no trailing punctuation
- [`err-doc-errors`](rules/err-doc-errors.md) - Document errors with `# Errors` section
- [`err-custom-type`](rules/err-custom-type.md) - Create custom error types, not `Box<dyn Error>`

### 2. Ownership and Borrowing (CRITICAL)

- [`own-borrow-prefer`](rules/own-borrow-prefer.md) - Borrow (`&T`, `&mut T`) over clone where possible
- [`own-copy-value-types`](rules/own-copy-value-types.md) - Pass `Copy` types by value
- [`own-arc-async`](rules/own-arc-async.md) - Use `Arc<T>` for shared ownership across async tasks
- [`own-arc-dyn-trait`](rules/own-arc-dyn-trait.md) - Use `Arc<dyn Trait + Send + Sync>` for DI trait objects
- [`own-move-intentional`](rules/own-move-intentional.md) - Prefer moves over clones for ownership transfer
- [`own-detect-cloning`](rules/own-detect-cloning.md) - Detect unnecessary cloning through review and profiling
- [`own-mem-replace`](rules/own-mem-replace.md) - Use `mem::take`/`mem::replace` to move values out of enums
- [`own-temporary-mut`](rules/own-temporary-mut.md) - Rebind as immutable after the preparation phase
- [`own-return-on-error`](rules/own-return-on-error.md) - Return consumed arguments inside the error type
- [`own-borrow-over-clone`](rules/own-borrow-over-clone.md) - Prefer `&T` borrowing over `.clone()`
- [`own-slice-over-vec`](rules/own-slice-over-vec.md) - Accept `&[T]` not `&Vec<T>`, `&str` not `&String`
- [`own-cow-conditional`](rules/own-cow-conditional.md) - Use `Cow<'a, T>` for conditional ownership
- [`own-arc-shared`](rules/own-arc-shared.md) - Use `Arc<T>` for thread-safe shared ownership
- [`own-rc-single-thread`](rules/own-rc-single-thread.md) - Use `Rc<T>` for single-threaded sharing
- [`own-refcell-interior`](rules/own-refcell-interior.md) - Use `RefCell<T>` for interior mutability (single-thread)
- [`own-mutex-interior`](rules/own-mutex-interior.md) - Use `Mutex<T>` for interior mutability (multi-thread)
- [`own-rwlock-readers`](rules/own-rwlock-readers.md) - Use `RwLock<T>` when reads dominate writes
- [`own-copy-small`](rules/own-copy-small.md) - Derive `Copy` for small, trivial types
- [`own-clone-explicit`](rules/own-clone-explicit.md) - Make `Clone` explicit, avoid implicit copies
- [`own-move-large`](rules/own-move-large.md) - Move large data instead of cloning
- [`own-lifetime-elision`](rules/own-lifetime-elision.md) - Rely on lifetime elision when possible

### 3. Memory Optimisation (CRITICAL)

- [`mem-with-capacity`](rules/mem-with-capacity.md) - Use `with_capacity()` when size is known
- [`mem-smallvec`](rules/mem-smallvec.md) - Use `SmallVec` for usually-small collections
- [`mem-arrayvec`](rules/mem-arrayvec.md) - Use `ArrayVec` for bounded-size collections
- [`mem-box-large-variant`](rules/mem-box-large-variant.md) - Box large enum variants to reduce type size
- [`mem-boxed-slice`](rules/mem-boxed-slice.md) - Use `Box<[T]>` instead of `Vec<T>` when fixed
- [`mem-thinvec`](rules/mem-thinvec.md) - Use `ThinVec` for often-empty vectors
- [`mem-clone-from`](rules/mem-clone-from.md) - Use `clone_from()` to reuse allocations
- [`mem-reuse-collections`](rules/mem-reuse-collections.md) - Reuse collections with `clear()` in loops
- [`mem-avoid-format`](rules/mem-avoid-format.md) - Avoid `format!()` when string literals work
- [`mem-write-over-format`](rules/mem-write-over-format.md) - Use `write!()` instead of `format!()`
- [`mem-arena-allocator`](rules/mem-arena-allocator.md) - Use arena allocators for batch allocations
- [`mem-zero-copy`](rules/mem-zero-copy.md) - Use zero-copy patterns with slices and `Bytes`
- [`mem-compact-string`](rules/mem-compact-string.md) - Use `CompactString` for small string optimisation
- [`mem-smaller-integers`](rules/mem-smaller-integers.md) - Use smallest integer type that fits
- [`mem-assert-type-size`](rules/mem-assert-type-size.md) - Assert hot type sizes to prevent regressions

### 4. API Design (HIGH)

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
- [`api-non-exhaustive`](rules/api-non-exhaustive.md) - Use `#[non_exhaustive]` for future-proof enums/structs
- [`api-compose-structs`](rules/api-compose-structs.md) - Decompose large structs for partial borrowing
- [`api-raii-guards`](rules/api-raii-guards.md) - Use RAII guards for automatic resource cleanup
- [`api-builder-must-use`](rules/api-builder-must-use.md) - Add `#[must_use]` to builder types
- [`api-typestate`](rules/api-typestate.md) - Use typestate for compile-time state machines
- [`api-extension-trait`](rules/api-extension-trait.md) - Use extension traits to add methods to foreign types
- [`api-parse-dont-validate`](rules/api-parse-dont-validate.md) - Parse into validated types at boundaries
- [`api-impl-into`](rules/api-impl-into.md) - Accept `impl Into<T>` for flexible string inputs
- [`api-must-use`](rules/api-must-use.md) - Add `#[must_use]` to `Result` returning functions
- [`api-from-not-into`](rules/api-from-not-into.md) - Implement `From`, not `Into` (auto-derived)
- [`api-default-impl`](rules/api-default-impl.md) - Implement `Default` for sensible defaults
- [`api-serde-optional`](rules/api-serde-optional.md) - Gate `Serialize`/`Deserialize` behind feature flag

### 5. Async Patterns (HIGH)

- [`async-all-io`](rules/async-all-io.md) - All I/O operations are async
- [`async-trait-usage`](rules/async-trait-usage.md) - Use `async_trait` or native async traits
- [`async-no-block`](rules/async-no-block.md) - Never block in async context
- [`async-send-sync`](rules/async-send-sync.md) - Trait objects in async need `Send + Sync` bounds
- [`async-yield-points`](rules/async-yield-points.md) - Long CPU tasks include yield points
- [`async-futures-send`](rules/async-futures-send.md) - Validate generated futures are `Send`
- [`async-tokio-runtime`](rules/async-tokio-runtime.md) - Use Tokio for production async runtime
- [`async-no-lock-await`](rules/async-no-lock-await.md) - Never hold `Mutex`/`RwLock` across `.await`
- [`async-spawn-blocking`](rules/async-spawn-blocking.md) - Use `spawn_blocking` for CPU-intensive work
- [`async-tokio-fs`](rules/async-tokio-fs.md) - Use `tokio::fs` not `std::fs` in async code
- [`async-cancellation-token`](rules/async-cancellation-token.md) - Use `CancellationToken` for graceful shutdown
- [`async-join-parallel`](rules/async-join-parallel.md) - Use `tokio::join!` for parallel operations
- [`async-try-join`](rules/async-try-join.md) - Use `tokio::try_join!` for fallible parallel ops
- [`async-select-racing`](rules/async-select-racing.md) - Use `tokio::select!` for racing/timeouts
- [`async-bounded-channel`](rules/async-bounded-channel.md) - Use bounded channels for backpressure
- [`async-mpsc-queue`](rules/async-mpsc-queue.md) - Use `mpsc` for work queues
- [`async-broadcast-pubsub`](rules/async-broadcast-pubsub.md) - Use `broadcast` for pub/sub patterns
- [`async-watch-latest`](rules/async-watch-latest.md) - Use `watch` for latest-value sharing
- [`async-oneshot-response`](rules/async-oneshot-response.md) - Use `oneshot` for request/response
- [`async-joinset-structured`](rules/async-joinset-structured.md) - Use `JoinSet` for dynamic task groups
- [`async-clone-before-await`](rules/async-clone-before-await.md) - Clone data before await, release locks

### 6. Compiler Optimisation (HIGH)

- [`opt-inline-small`](rules/opt-inline-small.md) - Use `#[inline]` for small hot functions
- [`opt-inline-always-rare`](rules/opt-inline-always-rare.md) - Use `#[inline(always)]` sparingly
- [`opt-inline-never-cold`](rules/opt-inline-never-cold.md) - Use `#[inline(never)]` for cold paths
- [`opt-cold-unlikely`](rules/opt-cold-unlikely.md) - Use `#[cold]` for error/unlikely paths
- [`opt-likely-hint`](rules/opt-likely-hint.md) - Use `likely()`/`unlikely()` for branch hints
- [`opt-lto-release`](rules/opt-lto-release.md) - Enable LTO in release builds
- [`opt-codegen-units`](rules/opt-codegen-units.md) - Use `codegen-units = 1` for max optimisation
- [`opt-pgo-profile`](rules/opt-pgo-profile.md) - Use PGO for production builds
- [`opt-target-cpu`](rules/opt-target-cpu.md) - Set `target-cpu=native` for local builds
- [`opt-bounds-check`](rules/opt-bounds-check.md) - Use iterators to avoid bounds checks
- [`opt-simd-portable`](rules/opt-simd-portable.md) - Use portable SIMD for data-parallel ops
- [`opt-cache-friendly`](rules/opt-cache-friendly.md) - Design cache-friendly data layouts (SoA)

### 7. Unsafe Code (HIGH)

- [`unsafe-reserve-ffi`](rules/unsafe-reserve-ffi.md) - Reserve unsafe for FFI, novel abstractions, measured perf
- [`unsafe-implies-ub`](rules/unsafe-implies-ub.md) - Unsafe implies UB risk, not general "danger"
- [`unsafe-soundness`](rules/unsafe-soundness.md) - Safe functions must never allow undefined behaviour
- [`unsafe-safety-docs`](rules/unsafe-safety-docs.md) - Document safety contracts with `// SAFETY:` comments
- [`unsafe-pass-miri`](rules/unsafe-pass-miri.md) - Validate unsafe code with Miri
- [`unsafe-small-modules`](rules/unsafe-small-modules.md) - Contain unsafe in small, focused modules

### 8. Generics and Traits (MEDIUM)

- [`trait-static-dispatch`](rules/trait-static-dispatch.md) - Static dispatch for hot paths — zero runtime cost
- [`trait-dynamic-dispatch`](rules/trait-dynamic-dispatch.md) - Dynamic dispatch for DI, plugins, heterogeneous collections
- [`trait-typestate`](rules/trait-typestate.md) - Encode state transitions in the type system
- [`trait-object-design`](rules/trait-object-design.md) - Design trait methods to work with trait objects
- [`trait-single-responsibility`](rules/trait-single-responsibility.md) - Keep traits focused, single responsibility
- [`trait-supertraits`](rules/trait-supertraits.md) - Use supertraits to compose requirements
- [`trait-avoid-sized`](rules/trait-avoid-sized.md) - Avoid `Self: Sized` unless necessary
- [`trait-strategy`](rules/trait-strategy.md) - Strategy pattern via traits or closures

### 9. Type Safety (MEDIUM)

- [`type-newtype-ids`](rules/type-newtype-ids.md) - Wrap IDs in newtypes: `UserId(u64)`
- [`type-newtype-validated`](rules/type-newtype-validated.md) - Newtypes for validated data: `Email`, `Url`
- [`type-enum-states`](rules/type-enum-states.md) - Use enums for mutually exclusive states
- [`type-option-nullable`](rules/type-option-nullable.md) - Use `Option<T>` for nullable values
- [`type-result-fallible`](rules/type-result-fallible.md) - Use `Result<T, E>` for fallible operations
- [`type-phantom-marker`](rules/type-phantom-marker.md) - Use `PhantomData<T>` for type-level markers
- [`type-never-diverge`](rules/type-never-diverge.md) - Use `!` type for functions that never return
- [`type-generic-bounds`](rules/type-generic-bounds.md) - Add trait bounds only where needed
- [`type-no-stringly`](rules/type-no-stringly.md) - Avoid stringly-typed APIs, use enums/newtypes
- [`type-repr-transparent`](rules/type-repr-transparent.md) - Use `#[repr(transparent)]` for FFI newtypes

### 10. Naming Conventions (MEDIUM)

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
- [`name-types-camel`](rules/name-types-camel.md) - Use `UpperCamelCase` for types, traits, enums
- [`name-variants-camel`](rules/name-variants-camel.md) - Use `UpperCamelCase` for enum variants
- [`name-type-param-single`](rules/name-type-param-single.md) - Use single uppercase for type params: `T`, `E`, `K`, `V`
- [`name-as-free`](rules/name-as-free.md) - `as_` prefix: free reference conversion
- [`name-is-has-bool`](rules/name-is-has-bool.md) - Use `is_`, `has_`, `can_` for boolean methods
- [`name-iter-method`](rules/name-iter-method.md) - Name iterator methods consistently
- [`name-iter-type-match`](rules/name-iter-type-match.md) - Iterator type names match method
- [`name-acronym-word`](rules/name-acronym-word.md) - Treat acronyms as words: `Uuid` not `UUID`
- [`name-crate-no-rs`](rules/name-crate-no-rs.md) - Crate names: no `-rs` suffix

### 11. Testing (MEDIUM)

- [`test-cfg-module`](rules/test-cfg-module.md) - Unit tests in `#[cfg(test)] mod tests`
- [`test-integration-dir`](rules/test-integration-dir.md) - Integration tests in `tests/` directory
- [`test-descriptive-names`](rules/test-descriptive-names.md) - Descriptive test names explaining what is verified
- [`test-error-paths`](rules/test-error-paths.md) - Test error paths, not just happy paths
- [`test-mockable-design`](rules/test-mockable-design.md) - Design for testability with traits
- [`test-test-util-feature`](rules/test-test-util-feature.md) - Gate test utilities behind `test-util` feature
- [`test-doc-examples`](rules/test-doc-examples.md) - Keep doc examples as executable tests
- [`test-cfg-test-module`](rules/test-cfg-test-module.md) - Use `#[cfg(test)] mod tests { }`
- [`test-use-super`](rules/test-use-super.md) - Use `use super::*;` in test modules
- [`test-arrange-act-assert`](rules/test-arrange-act-assert.md) - Structure tests as arrange/act/assert
- [`test-proptest-properties`](rules/test-proptest-properties.md) - Use `proptest` for property-based testing
- [`test-mockall-mocking`](rules/test-mockall-mocking.md) - Use `mockall` for trait mocking
- [`test-mock-traits`](rules/test-mock-traits.md) - Use traits for dependencies to enable mocking
- [`test-fixture-raii`](rules/test-fixture-raii.md) - Use RAII pattern (Drop) for test cleanup
- [`test-tokio-async`](rules/test-tokio-async.md) - Use `#[tokio::test]` for async tests
- [`test-should-panic`](rules/test-should-panic.md) - Use `#[should_panic]` for panic tests
- [`test-criterion-bench`](rules/test-criterion-bench.md) - Use `criterion` for benchmarking
- [`test-doctest-examples`](rules/test-doctest-examples.md) - Keep doc examples as executable tests

### 12. Documentation (MEDIUM)

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
- [`doc-all-public`](rules/doc-all-public.md) - Document all public items with `///`
- [`doc-module-inner`](rules/doc-module-inner.md) - Use `//!` for module-level documentation
- [`doc-examples-section`](rules/doc-examples-section.md) - Include `# Examples` with runnable code
- [`doc-hidden-setup`](rules/doc-hidden-setup.md) - Use `# ` prefix to hide example setup code
- [`doc-link-types`](rules/doc-link-types.md) - Link related types and functions in docs
- [`doc-cargo-metadata`](rules/doc-cargo-metadata.md) - Fill `Cargo.toml` metadata

### 13. Iterators and Functional Chains (MEDIUM)

- [`iter-chains`](rules/iter-chains.md) - Prefer iterator chains over explicit for loops
- [`iter-into-consume`](rules/iter-into-consume.md) - Use `into_iter()` when consuming the collection
- [`iter-zero-cost`](rules/iter-zero-cost.md) - Trust zero-cost abstractions for iterators
- [`iter-option-combinators`](rules/iter-option-combinators.md) - Use `Option`/`Result` combinators
- [`iter-no-intermediate-vec`](rules/iter-no-intermediate-vec.md) - Avoid collecting intermediate iterators
- [`iter-option-as-iter`](rules/iter-option-as-iter.md) - Treat `Option` as a zero-or-one element iterator

### 14. Performance Patterns (MEDIUM)

- [`perf-profile-first`](rules/perf-profile-first.md) - Profile before optimising
- [`perf-benchmark-hotpaths`](rules/perf-benchmark-hotpaths.md) - Create benchmarks around hot paths
- [`perf-partition-throughput`](rules/perf-partition-throughput.md) - Partition work for throughput
- [`perf-monitor-struct-sizes`](rules/perf-monitor-struct-sizes.md) - Monitor struct sizes for stack optimisation
- [`perf-zero-cost-trust`](rules/perf-zero-cost-trust.md) - Trust compiler for iterator/generic optimisation
- [`perf-connection-pool`](rules/perf-connection-pool.md) - Use connection pooling for database and HTTP
- [`perf-iter-over-index`](rules/perf-iter-over-index.md) - Prefer iterators over manual indexing
- [`perf-iter-lazy`](rules/perf-iter-lazy.md) - Keep iterators lazy, collect() only when needed
- [`perf-collect-once`](rules/perf-collect-once.md) - Don't `collect()` intermediate iterators
- [`perf-entry-api`](rules/perf-entry-api.md) - Use `entry()` API for map insert-or-update
- [`perf-drain-reuse`](rules/perf-drain-reuse.md) - Use `drain()` to reuse allocations
- [`perf-extend-batch`](rules/perf-extend-batch.md) - Use `extend()` for batch insertions
- [`perf-chain-avoid`](rules/perf-chain-avoid.md) - Avoid `chain()` in hot loops
- [`perf-collect-into`](rules/perf-collect-into.md) - Use `collect_into()` for reusing containers
- [`perf-black-box-bench`](rules/perf-black-box-bench.md) - Use `black_box()` in benchmarks
- [`perf-release-profile`](rules/perf-release-profile.md) - Optimise release profile settings
- [`perf-profile-first`](rules/perf-profile-first.md) - Profile before optimizing

### 15. Project Structure (LOW)

- [`proj-lib-main-split`](rules/proj-lib-main-split.md) - Keep `main.rs` minimal, logic in `lib.rs`
- [`proj-mod-by-feature`](rules/proj-mod-by-feature.md) - Organise modules by feature, not type
- [`proj-flat-small`](rules/proj-flat-small.md) - Keep small projects flat
- [`proj-mod-rs-dir`](rules/proj-mod-rs-dir.md) - Use `mod.rs` for multi-file modules
- [`proj-pub-crate-internal`](rules/proj-pub-crate-internal.md) - Use `pub(crate)` for internal APIs
- [`proj-pub-super-parent`](rules/proj-pub-super-parent.md) - Use `pub(super)` for parent-only visibility
- [`proj-pub-use-reexport`](rules/proj-pub-use-reexport.md) - Use `pub use` for clean public API
- [`proj-prelude-module`](rules/proj-prelude-module.md) - Create `prelude` module for common imports
- [`proj-bin-dir`](rules/proj-bin-dir.md) - Put multiple binaries in `src/bin/`
- [`proj-workspace-large`](rules/proj-workspace-large.md) - Use workspaces for large projects
- [`proj-workspace-deps`](rules/proj-workspace-deps.md) - Use workspace dependency inheritance

### 16. Static Verification and Linting (LOW)

- [`lint-clippy-all`](rules/lint-clippy-all.md) - Run `cargo clippy --all-targets --all-features`
- [`lint-fix-root-cause`](rules/lint-fix-root-cause.md) - Fix root cause, do not silence with `#[allow]`
- [`lint-expect-over-allow`](rules/lint-expect-over-allow.md) - Use `#[expect]` with reason over `#[allow]`
- [`lint-enable-warnings`](rules/lint-enable-warnings.md) - Enable key compiler lints at workspace level
- [`lint-cargo-fmt`](rules/lint-cargo-fmt.md) - Run `cargo fmt --check` in CI
- [`lint-cargo-audit`](rules/lint-cargo-audit.md) - Run `cargo-audit` for vulnerability scanning
- [`lint-cargo-hack`](rules/lint-cargo-hack.md) - Test feature combinations with `cargo-hack`
- [`lint-deny-correctness`](rules/lint-deny-correctness.md) - `#![deny(clippy::correctness)]`
- [`lint-warn-suspicious`](rules/lint-warn-suspicious.md) - `#![warn(clippy::suspicious)]`
- [`lint-warn-style`](rules/lint-warn-style.md) - `#![warn(clippy::style)]`
- [`lint-warn-complexity`](rules/lint-warn-complexity.md) - `#![warn(clippy::complexity)]`
- [`lint-warn-perf`](rules/lint-warn-perf.md) - `#![warn(clippy::perf)]`
- [`lint-pedantic-selective`](rules/lint-pedantic-selective.md) - Enable `clippy::pedantic` selectively
- [`lint-missing-docs`](rules/lint-missing-docs.md) - `#![warn(missing_docs)]`
- [`lint-unsafe-doc`](rules/lint-unsafe-doc.md) - `#![warn(clippy::undocumented_unsafe_blocks)]`
- [`lint-cargo-metadata`](rules/lint-cargo-metadata.md) - `#![warn(clippy::cargo)]` for published crates
- [`lint-rustfmt-check`](rules/lint-rustfmt-check.md) - Run `cargo fmt --check` in CI
- [`lint-workspace-lints`](rules/lint-workspace-lints.md) - Configure lints at workspace level

### 17. Code Formatting (LOW)

- [`fmt-four-spaces`](rules/fmt-four-spaces.md) - 4-space indentation, never tabs
- [`fmt-line-width`](rules/fmt-line-width.md) - Maximum 100 character line width
- [`fmt-trailing-commas`](rules/fmt-trailing-commas.md) - Trailing commas in multi-line lists
- [`fmt-single-line-small`](rules/fmt-single-line-small.md) - Single-line format for small items
- [`fmt-no-trailing-whitespace`](rules/fmt-no-trailing-whitespace.md) - No trailing whitespace
- [`fmt-comment-space`](rules/fmt-comment-space.md) - Single space after comment sigils
- [`fmt-blank-lines`](rules/fmt-blank-lines.md) - Separate items with 0-1 blank lines
- [`fmt-cargo-fmt`](rules/fmt-cargo-fmt.md) - Run `cargo fmt` before every commit

### 18. Structured Logging (LOW)

- [`log-structured-events`](rules/log-structured-events.md) - Structured events with named properties
- [`log-defer-formatting`](rules/log-defer-formatting.md) - Defer string formatting via templates
- [`log-hierarchical-naming`](rules/log-hierarchical-naming.md) - Hierarchical dot-notation naming
- [`log-otel-conventions`](rules/log-otel-conventions.md) - Follow OpenTelemetry semantic conventions
- [`log-redact-sensitive`](rules/log-redact-sensitive.md) - Redact sensitive data in logs

### 19. Dependencies and Crate Design (LOW)

- [`crate-workspace-deps`](rules/crate-workspace-deps.md) - Use `{ workspace = true }` for shared dependencies
- [`crate-features-additive`](rules/crate-features-additive.md) - Features must be additive
- [`crate-smaller-focused`](rules/crate-smaller-focused.md) - Prefer smaller, focused crates
- [`crate-avoid-statics`](rules/crate-avoid-statics.md) - Avoid module-level statics
- [`crate-no-glob-reexport`](rules/crate-no-glob-reexport.md) - Re-export items individually, not via glob
- [`crate-tier1-oobe`](rules/crate-tier1-oobe.md) - Libraries work on all Tier 1 platforms

### 20. Anti-patterns (REFERENCE)

- [`anti-clone-hot-loop`](rules/anti-clone-hot-loop.md) - Avoid cloning large structures in hot loops
- [`anti-silence-clippy`](rules/anti-silence-clippy.md) - Fix clippy warnings, do not blanket-suppress
- [`anti-monolith-function`](rules/anti-monolith-function.md) - Split monolithic multi-responsibility functions
- [`anti-primitive-obsession`](rules/anti-primitive-obsession.md) - Use newtypes where raw strings/ints are used
- [`anti-bool-params`](rules/anti-bool-params.md) - Replace boolean parameters with enums
- [`anti-deny-warnings`](rules/anti-deny-warnings.md) - Use specific lint names, not blanket `#[deny(warnings)]`
- [`anti-deref-inheritance`](rules/anti-deref-inheritance.md) - Never misuse `Deref` to simulate struct inheritance
- [`anti-unwrap-abuse`](rules/anti-unwrap-abuse.md) - Don't use `.unwrap()` in production code
- [`anti-expect-lazy`](rules/anti-expect-lazy.md) - Don't use `.expect()` for recoverable errors
- [`anti-clone-excessive`](rules/anti-clone-excessive.md) - Don't clone when borrowing works
- [`anti-lock-across-await`](rules/anti-lock-across-await.md) - Don't hold locks across `.await`
- [`anti-string-for-str`](rules/anti-string-for-str.md) - Don't accept `&String` when `&str` works
- [`anti-vec-for-slice`](rules/anti-vec-for-slice.md) - Don't accept `&Vec<T>` when `&[T]` works
- [`anti-index-over-iter`](rules/anti-index-over-iter.md) - Don't use indexing when iterators work
- [`anti-panic-expected`](rules/anti-panic-expected.md) - Don't panic on expected/recoverable errors
- [`anti-empty-catch`](rules/anti-empty-catch.md) - Don't use empty `if let Err(_) = ...` blocks
- [`anti-over-abstraction`](rules/anti-over-abstraction.md) - Don't over-abstract with excessive generics
- [`anti-premature-optimize`](rules/anti-premature-optimize.md) - Don't optimise before profiling
- [`anti-type-erasure`](rules/anti-type-erasure.md) - Don't use `Box<dyn Trait>` when `impl Trait` works
- [`anti-format-hot-path`](rules/anti-format-hot-path.md) - Don't use `format!()` in hot paths
- [`anti-collect-intermediate`](rules/anti-collect-intermediate.md) - Don't `collect()` intermediate iterators
- [`anti-stringly-typed`](rules/anti-stringly-typed.md) - Don't use strings for structured data

---

## Recommended Cargo.toml Settings

```toml
[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
panic = "abort"
strip = true

[profile.bench]
inherits = "release"
debug = true
strip = false

[profile.dev]
opt-level = 0
debug = true

[profile.dev.package."*"]
opt-level = 3  # Optimize dependencies in dev
```

---

## How to Use

Reference these guidelines by task type:

| Task | Primary Categories |
|------|-------------------|
| New function | `err-`, `own-`, `name-` |
| New struct/API | `api-`, `type-`, `name-`, `doc-` |
| Async code | `async-`, `own-` |
| Error handling | `err-`, `api-` |
| Trait design | `trait-`, `api-` |
| Memory optimisation | `mem-`, `own-`, `perf-` |
| Performance tuning | `opt-`, `mem-`, `perf-` |
| Testing | `test-`, `err-` |
| Code review | `anti-`, `lint-`, `fmt-` |
| Logging | `log-` |
| Unsafe code | `unsafe-` |
| Crate design | `crate-`, `api-`, `proj-` |

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
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) — Idioms, design patterns, and anti-patterns for idiomatic Rust
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce) — Clean code principles applied to Rust
- [Rust Performance Book](https://nnethercote.github.io/perf-book/) — Practical performance optimisation guide
