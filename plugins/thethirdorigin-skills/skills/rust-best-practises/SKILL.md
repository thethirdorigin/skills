---
name: rust-best-practises
description: Rust coding standards, API design, and best practices. Use when writing, reviewing, or refactoring Rust code. Covers architecture discovery, naming, error handling, ownership, async patterns, traits, testing, documentation, linting, performance, and crate design. References Rust API Guidelines (C-*) and Microsoft Rust Guidelines (M-*).
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

## 1. Architecture Discovery

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

## 2. Code Formatting

<instructions>
- 4-space indentation, never tabs — all indentation must be multiples of 4
- Maximum line width: 100 characters
- Use trailing commas in all multi-line comma-separated lists (smaller diffs, easier reordering)
- Single-line format for small items: `Foo { f1, f2 }`
- No trailing whitespace on any line
- Single space after comment sigils: `// comment` or `/* comment */`
- Separate items with 0-1 blank lines
- Run `cargo fmt` before every commit
- Use `rustfmt` configuration from the workspace if present
</instructions>

## 3. Naming Conventions

<instructions>
### Standard Casing (C-CASE)
- Types, traits, enum variants: `PascalCase` (CreditFacility, MarginAccountId)
- Functions, methods, local variables: `snake_case` (deploy_credit_facility, total_amount)
- Constants, statics: `SCREAMING_SNAKE_CASE` (MAX_RETRIES, DEFAULT_TIMEOUT)
- Modules, crates: `snake_case` matching domain concepts
- Lifetimes: short lowercase, usually `'a`, `'de`, `'src`

### Conversion Methods (C-CONV)
- `as_` — cheap reference-to-reference conversion (no allocation, no copy)
- `to_` — expensive conversion that may allocate (e.g., `to_string()`)
- `into_` — consumes self, transforms ownership (e.g., `into_inner()`)

### Iterator Methods (C-ITER)
- `iter()` returns `&T`, `iter_mut()` returns `&mut T`, `into_iter()` consumes and returns `T`
- Iterator type names match the methods: `Iter`, `IterMut`, `IntoIter`

### Getter Methods (C-GETTER)
- Simple field access: name the method after the field without a `get_` prefix
- Example: `fn name(&self) -> &str` not `fn get_name(&self) -> &str`

### No Weasel Words (M-CONCISE-NAMES)
- Remove meaningless terms: Service, Manager, Factory, Handler, Helper, Processor, Provider
- Use specific names reflecting actual functionality
- Prefer `Builder` over `Factory` when constructing values
</instructions>

<anti-patterns>
- `get_` prefix on simple getters: use `fn name()` not `fn get_name()`
- Magic numbers without constants: use `const MAX_RETRIES: u32 = 3;` not inline `3`
- Generic abbreviations: use `item_count` not `cnt`, `total_amount` not `amt`
- Single-letter variables outside of closures and short iterator chains
</anti-patterns>

## 4. API Design

<instructions>
### Interoperability — Eagerly Implement Common Traits (C-COMMON-TRAITS, M-PUBLIC-DEBUG, M-PUBLIC-DISPLAY)
- All public types: derive or implement `Debug` (C-DEBUG, M-PUBLIC-DEBUG)
- Where meaningful: `Clone`, `Default`, `PartialEq`, `Eq`, `Hash`
- For data structures: implement `Serialize` and `Deserialize` (C-SERDE)
- All public types should be `Send` where possible (M-TYPES-SEND, C-SEND-SYNC)
- Types expected to be read by users: implement `Display` (M-PUBLIC-DISPLAY)
- Use standard conversion traits: `From`, `AsRef`, `AsMut` (C-CONV-TRAITS)
- Collections: implement `FromIterator` and `Extend` (C-COLLECT)
- Debug output must never be empty (C-DEBUG-NONEMPTY)
- Custom Debug for sensitive types must not leak secrets

### Type Safety (C-NEWTYPE, C-CUSTOM-TYPE, M-STRONG-TYPES)
- Use newtypes to distinguish semantically different values of the same underlying type
  - Example: `struct UserId(Uuid)` and `struct AccountId(Uuid)` — not raw `Uuid` everywhere
- Arguments convey meaning through types, not `bool` or `Option`:
  - Instead of `fn process(data: &[u8], compressed: bool)`, use an enum: `enum Encoding { Raw, Compressed }`
- Use `PathBuf` for OS paths instead of `String` (M-STRONG-TYPES)
- Use bitflags for flag sets, not enums (C-BITFLAG)

### Builders for Complex Construction (C-BUILDER, M-INIT-BUILDER)
- Use builders when a type has 4+ optional parameters
- Pattern: `Foo::builder()` returns `FooBuilder` with chainable methods and `.build()` finaliser
- Required parameters passed to builder creation, optional set via methods
- For types with 2-3 optional parameters, inherent methods suffice

### Predictability
- Functions with a clear receiver are methods (C-METHOD)
- Functions do not take out-parameters — return values instead (C-NO-OUT)
- Constructors are static, inherent methods (C-CTOR): `fn new()`, `fn with_capacity()`
- Operator overloads are unsurprising (C-OVERLOAD)
- Only smart pointers implement Deref/DerefMut (C-DEREF)
- Prefer regular functions over associated functions for unrelated computation (M-REGULAR-FN)

### Flexibility
- Functions minimise assumptions about parameters using generics (C-GENERIC)
- Accept `impl AsRef<str>`, `impl AsRef<Path>`, `impl AsRef<[u8]>` where feasible (M-IMPL-ASREF)
- Accept `impl Read`/`impl Write` for I/O functions — enables composability (M-IMPL-IO)
- Accept `impl RangeBounds<T>` instead of hand-rolled start/end parameters (M-IMPL-RANGEBOUNDS)
- Traits are object-safe if they may be useful as a trait object (C-OBJECT)
- Expose intermediate results to avoid forcing callers to redo work (C-INTERMEDIATE)

### Type Hierarchy for Dependency Injection (M-DI-HIERARCHY)
- Prefer concrete types over generic parameters
- Prefer generic parameters over `dyn Trait` objects
- Use enums for mock/test implementations
- Accept narrow, single-concern traits for generic bounds
- Implement traits for concrete types on top of inherent functions

### Library UX
- Essential functionality is inherent — users must not need trait imports (M-ESSENTIAL-FN-INHERENT)
- Service-like types implement shared-ownership Clone via `Arc<Inner>` (M-SERVICES-CLONE)
- Avoid `Rc`, `Arc`, `Box`, `RefCell` in public APIs — hide behind clean interfaces (M-AVOID-WRAPPERS)
- Abstractions do not visibly nest: avoid requiring `Foo<Bar<Baz>>` from callers (M-SIMPLE-ABSTRACTIONS)
- Do not leak external crate types in public APIs (M-DONT-LEAK-TYPES)

### Future-Proofing
- Struct fields are private — use accessor methods (C-STRUCT-PRIVATE)
- Sealed traits protect against downstream implementations (C-SEALED)
- Data structures do not duplicate derived trait bounds (C-STRUCT-BOUNDS)
</instructions>

## 5. Error Handling

<instructions>
### Core Principle
- Use `Result<T, E>` for all recoverable errors — never panic in library code
- Use `?` operator for error propagation — do not match-and-rewrap
- Panics mean "stop the program" (M-PANIC-IS-STOP) — only for:
  - Programming bugs and contract violations (M-PANIC-ON-BUG)
  - Const contexts
  - User-requested abort
  - Poison (e.g., poisoned mutex)

### Library Error Types (M-ERRORS-CANONICAL-STRUCTS)
- Create situation-specific error structs with:
  - `Backtrace` capture
  - Cause chain via `source()`
  - `ErrorKind` enum for categorisation (internal, not directly exposed)
  - `is_xxx()` helper methods for error classification
- Implement `Display` with summary + backtrace + cause information
- Implement `std::error::Error` trait
- Error types must be meaningful and well-behaved (C-GOOD-ERR)

### Application Error Types (M-APP-ERROR)
- Applications may use `anyhow`, `eyre`, or similar ergonomic error crates
- Libraries MUST use concrete error types, not anyhow

### Error Handling Patterns
- Match existing error conversion patterns in the codebase (check for `From` impls)
- Error variants carry context strings, not raw inner errors
- Create private `bail!()` helper macros for frequently constructed errors
- Test error paths explicitly — not just happy paths
</instructions>

<anti-patterns>
- `.unwrap()` or `.expect()` in non-test code
- `panic!()` for recoverable errors
- Stringly-typed errors (use typed enums/structs)
- Catching all errors with a single generic variant
- Silently swallowing errors with `let _ = ...`
- Using `anyhow` in library crates (use `thiserror` or canonical structs)
</anti-patterns>

## 6. Ownership and Borrowing

<instructions>
- Borrow (`&T`, `&mut T`) over clone where possible — reduces memory overhead
- Pass by value for `Copy` types (u64, bool, Uuid, small enums)
- Use `Arc<T>` for shared ownership across async tasks — never `Rc` in async code
- `Arc<dyn Trait + Send + Sync>` for trait objects in dependency injection containers
- Prefer moves over clones when ownership transfer is intentional
- Detect unnecessary cloning through code review and profiling
</instructions>

<anti-patterns>
- `.clone()` to satisfy the borrow checker without understanding why
- `Rc<T>` in async code (not Send)
- Excessive `Box<dyn Trait>` when concrete types or generics suffice
- Cloning large data structures in hot loops
</anti-patterns>

## 7. Async Patterns

<instructions>
- All I/O operations are async — identify the runtime (tokio, async-std) from dependencies
- Use `async_trait` (or native async traits if edition 2024+) for trait definitions
- Never block in async context: no `std::thread::sleep`, use `tokio::time::sleep`
- All trait objects in async containers need `Send + Sync` bounds
- Long-running CPU-bound tasks: include yield points (M-YIELD-POINTS)
  - `yield_now().await` at regular intervals (target 10-100us between yields)
  - Use `has_budget_remaining()` for unpredictable operation durations
- Generated futures must be `Send` — validate with compile-time assertions (M-TYPES-SEND)
</instructions>

## 8. Iterators and Functional Chains

<instructions>
- Prefer iterator chains (`.iter().map().filter().collect()`) over explicit for loops
- Use `.into_iter()` when consuming the collection
- Leverage zero-cost abstractions — the compiler optimises away intermediate allocations
- Chain operations for expressive, efficient data processing
- Use `Option`/`Result` combinators: `.map()`, `.and_then()`, `.unwrap_or()`, `.unwrap_or_default()`
</instructions>

<anti-patterns>
- Manual loops that could be expressed as iterator chains
- Creating intermediate `Vec`s when a single iterator chain suffices
- Allocating collections before confirming necessity
</anti-patterns>

## 9. Generics and Traits

<instructions>
### Static vs Dynamic Dispatch
- **Static dispatch** (`impl Trait` or `<T: Trait>`): zero runtime overhead, enables inlining, monomorphises per type — use for hot paths
- **Dynamic dispatch** (`dyn Trait`): runtime cost, smaller binary — use for DI boundaries, plugin systems, heterogeneous collections

### Type State Pattern
- Encode state transitions in the type system using phantom types
- Example: `Connection<Disconnected>` -> `Connection<Connected>` -> `Connection<Authenticated>`
- Prevents invalid state transitions at compile time
- Trade-off: complexity increases with more states — use judiciously

### Trait Design
- Design trait methods to work naturally with trait objects
- Avoid methods requiring `Self: Sized` unless necessary
- Keep traits focused — single responsibility per trait
- Use supertraits to compose requirements: `trait Service: Send + Sync + Clone`
</instructions>

## 10. Documentation

<instructions>
### Canonical Sections (M-CANONICAL-DOCS)
Every public item should have:
- **Summary sentence**: under 15 words, single line (M-FIRST-DOC-SENTENCE)
- **Extended documentation**: detailed explanation when needed
- **Examples**: runnable code demonstrating usage
- **Errors**: what error types are returned and when
- **Panics**: conditions that cause panic (if any)
- **Safety**: requirements for unsafe functions

### Module Documentation (M-MODULE-DOCS)
- All public library modules require `//!` module documentation
- Cover: module contents, usage context, examples, side effects

### Doc Comments
- Use `///` for items, `//!` for crate/module level
- Use `?` in examples, not `unwrap()` (C-QUESTION-MARK)
- Include hyperlinks to related items (C-LINK)
- Mark re-exports with `#[doc(inline)]` (M-DOC-INLINE)
- Document magic values with rationale and side effects (M-DOCUMENTED-MAGIC)

### Code Comments
- Prefer line comments (`//`) over block comments
- Explain *why*, not *what* — the code shows what
- Complete sentences: start with capital letter, end with period
- Do not maintain "living comments" that must update alongside code
</instructions>

<anti-patterns>
- Undocumented public APIs
- Doc comments that restate the function signature
- `unwrap()` in documentation examples
- Missing `# Examples` sections for complex public functions
- Stale TODO comments — convert to tracked issues
</anti-patterns>

## 11. Testing

<instructions>
### Test Organisation
- Unit tests: `#[cfg(test)] mod tests` in the same file
- Integration tests: `tests/` directory at the crate root
- Doc tests: examples in `///` comments that compile and run

### Test Quality
- Test error paths, not just happy paths (C-GOOD-ERR)
- Use descriptive test names explaining what is verified
- Use specific assertion macros (`assert_eq!`, `assert!`) with meaningful messages
- Consider `cargo insta` for snapshot testing complex output

### Testable Design (M-DESIGN-FOR-AI, M-MOCKABLE-SYSCALLS)
- Design APIs to be testable — allow customers to validate usage in unit tests
- Make I/O and system calls mockable: accept traits, not concrete I/O types
- Use enum dispatching between native and mocked implementations
- Test utilities feature-gated behind `test-util` feature (M-TEST-UTIL)
- Mockable port traits: use `#[cfg_attr(test, automock)]` if mockall is available
</instructions>

## 12. Static Verification and Linting

<instructions>
### Clippy (M-STATIC-VERIFICATION)
- Run `cargo clippy --all-targets --all-features` during development and CI
- Fix the root cause of warnings — do not silence with `#[allow(...)]`
- Use `#[expect]` instead of `#[allow]` for justified overrides — it warns if the override becomes unnecessary (M-LINT-OVERRIDE-EXPECT)
- Include a reason attribute: `#[expect(clippy::too_many_arguments, reason = "builder pattern pending")]`

### Compiler Lints
Enable at workspace level:
- `ambiguous_negative_literals`
- `missing_debug_implementations`
- `redundant_imports`
- `unused_lifetimes`
- `unsafe_op_in_unsafe_fn`

### Additional Tools
- `cargo fmt --check` — formatting validation
- `cargo-audit` — security vulnerability scanning
- `cargo-hack` — feature combination testing
- `cargo-udeps` — unused dependency detection
- `miri` — unsafe code validation
</instructions>

## 13. Structured Logging (M-LOG-STRUCTURED)

<instructions>
- Use structured events with named properties and message templates
- Defer string formatting via templates: `tracing::info!(user_id = %id, "User logged in")`
- Use hierarchical dot-notation naming: `component.operation.state`
- Follow OpenTelemetry semantic conventions where applicable
- Redact sensitive data using dedicated mechanisms
- Match the logging framework already in use (tracing, log, etc.)
</instructions>

## 14. Dependencies and Crate Design

<instructions>
### Workspace Dependencies
- Use `{ workspace = true }` for shared dependencies — do not duplicate versions
- Check existing workspace dependencies before adding new ones
- Features must be additive: adding a feature must not disable public items (M-FEATURES-ADDITIVE)

### Crate Design
- Prefer smaller, focused crates over monolithic ones (M-SMALLER-CRATES)
  - Independent submodules should become separate crates
  - Dramatically improves compile times and prevents cyclic dependencies
- Avoid module-level statics where consistent view affects correctness (M-AVOID-STATICS)
- Re-export items individually, not via glob re-exports (M-NO-GLOB-REEXPORTS)
- Libraries must work out of the box on all Tier 1 platforms (M-OOBE)
</instructions>

## 15. Performance

<instructions>
- Profile before optimising — never guess (use `cargo flamegraph`, `criterion`, `divan`)
- Identify performance-relevant crates early; create benchmarks around hot paths (M-HOTPATH)
- Optimise for throughput: partition work chunks, let threads handle slices independently (M-THROUGHPUT)
- Monitor struct sizes for stack optimisation
- Zero-cost abstractions: trust the compiler to optimise iterator chains and generics
- Use connection pooling for database and HTTP clients
- Avoid hot spinning, individual item processing in loops, and work stealing unless measured
</instructions>

## 16. Unsafe Code

<instructions>
- Reserve unsafe for: FFI boundaries, novel abstractions, measured performance gains (M-UNSAFE)
- `unsafe` implies undefined behaviour risk — do not use for "danger" unrelated to UB (M-UNSAFE-IMPLIES-UB)
- All code must be sound: safe functions may rely on module-level guarantees, but must never allow UB from safe callers (M-UNSOUND)
- Document safety contracts with `// SAFETY:` comments
- Harden against adversarial code and misbehaving traits
- Pass Miri including adversarial test cases
- Expose unsafe functions rather than unsound safe abstractions
</instructions>

## 17. Comprehensive Anti-Patterns

<anti-patterns>
### Memory and Performance
- Cloning when borrowing suffices
- Unnecessary allocations or copies in hot paths
- Large structs on the stack unnecessarily
- Blocking calls in async context

### Code Quality
- Silencing clippy without addressing root cause
- Living comments that duplicate code logic
- Monolithic functions combining multiple responsibilities
- Over-engineering with unnecessary abstractions
- Magic numbers without named constants

### Error Handling
- Panicking on recoverable errors
- `.unwrap()` in production code
- Not testing error paths
- Poor error propagation (match-and-rewrap instead of ?)

### Architecture
- Domain layer importing infrastructure types
- Leaking external crate types in public APIs
- Circular dependencies between modules
- God objects with too many responsibilities

### Type System
- Primitive obsession: raw strings/ints where newtypes belong
- Boolean parameters where enums would be clearer
- Not leveraging exhaustive matching for enums
</anti-patterns>

## References

- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) — Official Rust API design checklist covering naming, interoperability, documentation, predictability, flexibility, type safety, and future-proofing (C-* rules)
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) — Comprehensive 60+ rule set covering error handling, documentation, testing, safety, performance, library design, and AI-readiness (M-* rules)
- [Microsoft Rust Guidelines (Agent-Optimised)](https://microsoft.github.io/rust-guidelines/agents/all.txt) — Full guideline text in agent-consumable format
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) — Official formatting and style conventions
- [Apollo GraphQL Rust Best Practices](https://github.com/apollographql/rust-best-practices) — Production Rust patterns from Apollo Engineering
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce) — Clean code principles applied to Rust: naming, ownership, error handling, iterators, documentation
