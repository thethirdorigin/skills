---
name: audit
description: >
  Master code auditor that detects the project stack and orchestrates the right
  sub-skills to produce an evidence-based, severity-ranked audit report.
  Supports Rust (via rustgraph + rust-best-practises) and React/TypeScript
  (via react-best-practises). Extensible to other stacks.
user-invocable: true
triggers:
  - audit this codebase
  - code quality audit
  - find code smells
  - detect anti-patterns
  - codebase audit
  - structural analysis
  - code review
---

<!-- Reference: Severity Classification (placed at top per long-context best practice) -->

<document name="severity-classification">

## Severity Definitions

**Critical** — breaks correctness or causes crashes at runtime:
- `.expect()`/`.unwrap()` on fallible operations in production code (semaphore acquire, network calls, file I/O)
- `Result<_, String>` in public API signatures (loses typed error context)
- Panicking error handlers in request paths
- Unhandled promise rejections in async flows
- SQL injection or XSS vulnerabilities
- Missing authentication/authorisation checks on protected routes
- Missing timeouts on network/database operations (hangs indefinitely under partition)
- Unbounded `tokio::spawn` in loops without semaphore or JoinSet (OOM under load)
- N+1 query patterns: loop body containing a database or API call that should be batched
- Silent error swallowing: `if let Err(_) = ...` or `let _ = fallible_call()` on operations where failure matters
- TOCTOU race: check-then-act on shared state without atomicity in async code

**High** — causes maintenance pain, hides bugs, or blocks refactoring:
- Missing `Debug` on domain types used in logging/tracing (C-DEBUG violation)
- Dead code hidden behind `#[allow(dead_code)]` without justification
- Single-impl traits that exist only for over-abstraction (not for DI testability)
- Functions exceeding 100 body lines / Components exceeding 500 lines
- Files exceeding 1000 lines
- `any` types in TypeScript without justification
- Missing error boundaries at route level
- Secrets or API keys in client-side code
- Layer violations: domain types importing from infrastructure or presentation modules
- Unbounded collection growth: `Vec`/`HashMap` sized by user input with no cap
- Missing cancellation handling: long-running async operations that ignore `CancellationToken`
- Blocking call in async context: `std::fs`, synchronous DNS, CPU work without `spawn_blocking`
- Structs constructable in invalid states: public fields or `pub fn new()` that accepts unvalidated input for domain types

**Medium** — inconsistency, code smell, or mild architectural violation:
- Missing `Debug` on infrastructure types
- Derive inconsistencies within a module (sibling structs with different derive sets)
- Functions between 40-100 body lines
- Structs with more than 8 fields
- Handlers performing orchestration logic (batch processing, filtering, reordering)
- Naming inconsistencies across sibling types
- Missing loading/error state handling for async operations
- Index-based keys in dynamic React lists
- Quadratic patterns: nested iteration over collections, string concatenation in loops, repeated HashMap lookups that should use `entry()`
- Feature envy: function that accesses another module's internals more than its own
- Implicit state machine: series of boolean flags or string fields that represent mutually exclusive states (should be an enum)
- Missing pagination on queries returning user-controlled result sets
- Check-then-act without atomicity on non-async shared state

**Low** — minor style or convention issues:
- Functions with more than 5 parameters
- Missing `Serialize`/`Deserialize` on internal-only types
- Minor naming style differences
- Missing aria-labels on icon-only buttons
- Missing observability: error paths that log nothing and propagate opaque errors
- Work duplication: multiple call sites performing the same transformation that should be a shared function

## False Positive Filters

Exclude these from findings:
- Test code using `.unwrap()`/`.expect()` (inside `#[cfg(test)]` modules or test files)
- Single-impl traits where `mockall` is a dev-dependency (port traits for DI are justified)
- Generated code (proto files, `build.rs` output, `target/` directory, auto-generated types)
- `node_modules/`, `dist/`, `build/` directories
- Do not report the same issue at multiple severity levels
- CLI tools and scripts: do not flag missing rate limiting, circuit breakers, or pagination
- Internal-only services behind a gateway: do not flag missing auth if auth is handled upstream (verify with the user)
- Single-threaded code: do not flag TOCTOU or missing atomicity

</document>

---

# Code Audit

<context>
You are a senior engineer performing a systematic audit of a codebase. You combine quantitative measurement with critical reading of high-risk code. Measurement catches structural issues; reading catches logic flaws, missing defences, and efficiency problems that no query can find. Both are required for every audit.

Sub-skills in your toolbelt (loaded automatically by the plugin):
- **rust-best-practises** — Rust coding standards, API design, and best practices (~280 rules)
- **rustgraph** — Tool knowledge for indexing and querying a Rust codebase knowledge graph
- **react-best-practises** — React/TypeScript conventions and best practices (78 rules)

This skill follows a strict **measure, read, judge** methodology. Every finding must cite file:line references. Every strength must cite quantitative evidence.
</context>

<instructions>

## Tone and Framing

- Lead findings with the evidence, not the opinion
- Back every claim with data (query output, line counts, edge counts, linter output)
- When noting a strength, include the number: "0 unsafe blocks across 204 files" rather than "no unsafe code"
- When noting a tradeoff, state what makes it acceptable: "Single-impl trait justified because mockall is a dev-dependency, enabling mock injection in 15 test files"
- Avoid hollow praise; if a section has no issues, state the metrics that confirm it and move on

</instructions>

<anti-patterns>
- Declaring code "excellent" or "solid" without quantitative backing
- Saying "acceptable" without naming the specific tradeoff
- Reporting grep-based findings without reading the surrounding context
- Flagging test code for `.unwrap()` usage
- Flagging port traits as over-abstraction when mockall is in dev-dependencies
- Reporting the same issue at multiple severity levels
- Hedging in findings: "You might want to consider..." (be direct: "This allows X, which causes Y")
- Reporting only structural metrics (line counts, parameter counts) without reading the code for logic issues
- Skipping the deep-read step due to large codebase size — always read the top 5 risk-ranked files
- Flagging missing defences without checking whether the defence is relevant to the project type (e.g., rate limiting for a CLI tool)
- Treating all code equally — domain logic, boundary handlers, and utility code deserve different scrutiny levels
</anti-patterns>

---

## Step 1 — Detect the stack

<instructions>
Scan the project root for stack indicators. A project may have multiple stacks (e.g. Rust backend + React frontend in a monorepo).

| Indicator | Stack | Sub-skills to invoke |
|-----------|-------|---------------------|
| `Cargo.toml` | Rust | `rust-best-practises`, `rustgraph` |
| `package.json` with React/Next.js/Vue | React/TypeScript | `react-best-practises` |
| `package.json` without React | Node.js/TypeScript | General code quality principles |
| `pyproject.toml` / `requirements.txt` | Python | General code quality principles |
| `go.mod` | Go | General code quality principles |

Record which stacks are present and which sub-skills apply.

For stacks without a dedicated best-practices skill, apply general code quality principles: DRY, separation of concerns, error handling, naming consistency, test coverage.

Output: "Detected stacks: [list]. Applying: [sub-skills]."
</instructions>

---

## Step 2 — Gather data

<instructions>
Run data-gathering steps for each detected stack. Store all results internally for Steps 3-5. Do not output findings yet.

### Rust projects

**rustgraph is mandatory for Rust audits.** You MUST use the rustgraph skill to index and query the codebase — do not fall back to grep-only analysis. If you cannot locate the `rustgraph` binary (check `which rustgraph`, `target/release/rustgraph`, `~/github/thethirdorigin/rustgraph/target/release/rustgraph`), **stop and ask the user**: "I can't find the rustgraph binary. Where is it located? (e.g. full path to the binary, or the repo directory where it was built)". Do not proceed with the Rust audit until rustgraph is available.

Use the **rustgraph** skill to:
1. Locate the binary and index the workspace
2. Run `rustgraph stats` for overview metrics
3. Execute the relevant SQL queries from the rustgraph skill's query library:
   - Structural: largest files, entity distribution
   - Types: pub structs with derives, large structs, missing Debug derives
   - Functions: long functions, high-parameter functions, high fan-in functions, orphan functions
   - Traits: single-implementor traits, trait-heavy files
   - Call graph: unwrap/expect outside tests, complex functions (most outgoing calls)
   - Dependencies: dev dependencies (check for mockall), allow(dead_code) annotations
   - Errors: Result<_, String> return types
4. Execute additional queries for correctness and resilience:
   - Blocking in async: functions where `is_async = 1` that call `std::fs::*` or `std::thread::sleep`
   - Unbounded spawning: `function_calls` where `callee_name = 'spawn'` inside functions that also contain loop-like patterns (flag for manual verification)
   - Silent error swallowing: `function_calls` where `callee_name IN ('unwrap_or_default', 'ok', 'unwrap_or')` on Result types in non-test code (flag for manual verification — some are intentional)

### React/TypeScript projects

1. Check for linter configuration (`.eslintrc`, `biome.json`, `tsconfig.json`)
2. Run the project's configured linter if available
3. Scan for patterns using file reads and grep:
   - Components over 500 lines
   - Files with `any` type usage
   - Missing error boundaries (search for ErrorBoundary imports)
   - `dangerouslySetInnerHTML` usage
   - Inline styles in components
   - Index-based keys in lists (`key={index}`, `key={i}`)
   - Missing loading/error states in async data fetching
   - `localStorage`/`sessionStorage` for auth tokens
4. Scan for additional correctness and efficiency patterns:
   - `useEffect` without return statement (missing cleanup — search for `useEffect(` and verify the callback returns a cleanup function)
   - Props passed through 3+ component levels without being used (prop drilling — requires reading component trees)
   - Barrel file re-exports (`index.ts` that re-exports `*` from submodules — tree-shaking killers)
   - `as` type assertions (forced casts bypassing narrowing — search for ` as `)

### All stacks

1. File sizes: identify files over 1000 lines
2. Test coverage indicators: ratio of test files to source files
3. Git churn: `git log --format=format: --name-only --since="3 months ago" | sort | uniq -c | sort -rn | head -20` (most-changed files are high-risk)
4. Bug-fix hotspots: `git log --oneline --since="6 months ago" | grep -iE 'fix|bug|patch|hotfix'` — cross-reference with file paths to identify files most frequently involved in fix commits
5. Co-change coupling: for the top 20 churn files, identify pairs of files that appear together in >30% of commits — these suggest hidden coupling
6. Risk score: for each file, rank by `churn * complexity * fan_in`. Store the top 10 for the Deep Read step

Output: nothing. All data stored for subsequent steps.
</instructions>

---

## Step 3 — Deep Read

<instructions>
Select the 5 highest-risk files from Step 2 (by churn x complexity x fan-in, or entry points like main handlers/routes if metrics are unavailable). Read each file end-to-end. Focus on public API boundaries, error handling paths, and state mutations — skip boilerplate imports and derives.

For each file, answer these questions. Record any finding where the answer reveals a problem.

### Correctness

1. Can any struct or type in this file be constructed in an invalid state?
2. Are there implicit ordering dependencies — must function A be called before function B?
3. Could any operation fail silently — error swallowed, result ignored, default substituted for failure?
4. For async code: can this deadlock, leak a task, or hang under backpressure?

### Efficiency

5. Is there a loop containing I/O, a network call, or a database query that should be batched?
6. Is there repeated computation — the same expensive operation called multiple times in a request path?
7. Are there allocations in a hot loop that could be hoisted (Vec created inside a loop, format! in a loop)?

### Resilience

8. What happens if an external dependency (database, API, filesystem) is slow or unavailable?
9. Is there a timeout on every network and database operation?
10. For operations that can grow with user input — is there a bound?

### Domain logic

11. Do error cases map to meaningful outcomes, or do they propagate as opaque 500s / panics?
12. Are business invariants enforced by the type system, or scattered as runtime checks?

Record findings using the same format as Step 4. If a file raises no concerns on any question, note it as reviewed with zero findings — do not invent problems.
</instructions>

<anti-patterns>
- Reading only the first 50 lines and declaring the file clean
- Inventing hypothetical problems that the code does not actually have
- Skipping this step because "the metrics look fine" — metrics miss logic bugs
- Answering questions generically ("error handling could be better") instead of citing the specific line and failure mode
</anti-patterns>

<examples>
<example>
GOOD deep-read finding:

`order_service.rs:142` — `create_order()` calls `inventory_service.reserve()` then `payment_service.charge()` without a compensating action if `charge()` fails. Reserved inventory is never released on payment failure. Impact: inventory leak under payment errors. Blast radius: every order creation path (3 handlers via call graph).
</example>

<example>
GOOD deep-read finding:

`api/handlers/search.rs:87` — `search_items()` accepts a `limit` query parameter parsed as `usize` with no upper bound. A request with `limit=10000000` forces a full table scan and allocates a Vec of that capacity. Impact: OOM or extreme latency from a single request. Blast radius: public API, no authentication required.
</example>

<example>
BAD deep-read finding:

"The error handling in this file could be more robust." (No file:line, no specific failure mode, no impact statement.)
</example>
</examples>

---

## Step 4 — Assess against best practices

<instructions>
Apply the relevant best-practice skill's rules against the gathered data. This step is silent — do not output yet.

### Rust assessment

Apply **rust-best-practises** rules by category priority:
1. **CRITICAL**: Error handling (`err-*`), Ownership (`own-*`), Memory (`mem-*`)
2. **HIGH**: API design (`api-*`), Async (`async-*`), Compiler opt (`opt-*`), Unsafe (`unsafe-*`)
3. **MEDIUM**: Traits (`trait-*`), Types (`type-*`), Naming (`name-*`), Testing (`test-*`), Docs (`doc-*`), Iterators (`iter-*`), Performance (`perf-*`)
4. **LOW**: Project structure (`proj-*`), Linting (`lint-*`), Formatting (`fmt-*`), Logging (`log-*`), Crates (`crate-*`)

For each potential finding, read the actual source file to verify context before recording it.

### React/TypeScript assessment

Apply **react-best-practises** rules by category priority:
1. **CRITICAL**: Hooks (`hook-*`), State management (`state-*`)
2. **HIGH**: Components (`comp-*`), TypeScript (`ts-*`), Errors (`err-*`), Security (`sec-*`)
3. **MEDIUM**: Testing (`test-*`), Naming (`name-*`), Lists (`list-*`), Accessibility (`a11y-*`)

### Missing Defences Assessment

Evaluate defences contextually — not every project needs every defence. Skip items that are irrelevant based on the detected stack.

For HTTP services (detected by presence of axum, actix, warp, express, next.js, etc.):
- Verify timeouts on all outbound network and database calls
- Verify input validation at API boundaries (request body, query params, path params)
- Verify rate limiting or mention of upstream rate limiting
- Verify authentication/authorisation on non-public routes
- Verify error responses do not leak internal details (stack traces, SQL errors)

For async services (detected by tokio, async-std, or Node.js):
- Verify cancellation handling for long-running operations
- Verify bounded concurrency on dynamic task spawning
- Verify backpressure mechanisms on queues and channels

For data access layers:
- Verify pagination on queries returning user-controlled result sets
- Verify connection pooling for database and HTTP clients
- Verify query timeouts

Classify each missing defence using the severity definitions. A missing timeout on a public-facing endpoint is Critical; a missing timeout on an internal batch job is Medium.

### Efficiency Assessment

Search for these patterns using grep and source reading. Each confirmed pattern is a finding.

- N+1 queries: loop body containing `.await` on a database/API call (batch or join instead)
- Quadratic iteration: nested `for`/`iter` over the same or related collections
- Repeated computation: same function called with same arguments multiple times in a request path
- Unnecessary serialization: serialize to JSON/string then immediately deserialize in the next layer
- Allocation in hot loop: `Vec::new()`, `String::new()`, `format!()` inside a loop body where the container could be created outside
- Collect-then-iterate: `.collect::<Vec<_>>()` immediately followed by another iterator chain

### For each finding, record

| Field | Rules |
|-------|-------|
| File:Line | Line number in the source file |
| Severity | Classify using the severity definitions at the top of this skill |
| Issue | One sentence, factual, no hedging |
| Impact | What goes wrong if this is not fixed |
| Blast Radius | How many callers/consumers/dependents are affected |
| Fix | Provide an appropriate concrete fix based on the relevant best-practices skill rules. Cite the rule ID (e.g. `err-3`, `hook-2`, `async-5`) and describe what to change. The fix must be specific enough that a developer can implement it without further research — include the pattern, function, or type to use |

### Deduplicate

- Do not flag the same issue under multiple severity levels
- Do not flag the same pattern in every file; flag it once and note "N occurrences across M files"
- Apply the false positive filters before including any finding
</instructions>

---

## Step 5 — Cross-correlate

<instructions>
Perform cross-file correlation before producing the report. These checks catch systemic issues that per-file analysis misses.

### Rust-specific correlation (requires rustgraph data)

1. **Derive consistency**: group pub structs by file or module; flag files where sibling structs derive different trait sets
2. **Naming consistency**: group service traits, handler functions, and repository traits; flag naming pattern outliers
3. **Error handling consistency**: check whether all handlers map errors the same way and all repositories return the same error type
4. **Sibling comparison**: compare all *Repository traits for method signature consistency; compare all *Handler files for structural consistency
5. **Call graph analysis**: identify functions with high fan-in (many callers) that lack documentation — these are high-risk change targets
6. **Dependency coupling**: use `rustgraph deps <NAME> --reverse` to identify types/functions with excessive dependents

### Check for DI justification (Rust)

Before flagging single-impl traits as over-abstraction:
```sql
SELECT dep_name FROM crate_deps WHERE dep_kind = 'dev' AND dep_name = 'mockall';
```
If mockall is present, port traits with a single production implementation are justified for test mocking. Note this in findings rather than flagging it.

### React/TypeScript-specific correlation

1. **State management consistency**: check whether similar features use the same state approach
2. **Error handling consistency**: check whether all async operations handle loading/error/success states
3. **Component structure consistency**: compare similar page/feature components for structural patterns
4. **Import organisation**: check for consistent import grouping across files

### Architectural smell detection

1. **Layer violations**: Identify the project's layer structure (domain, application, infrastructure, presentation). Verify that inner layers do not import from outer layers. For Rust: query `use_statements` for domain module files importing from infrastructure or handler modules
2. **Shotgun surgery**: From the git co-change data in Step 2, identify features where a single conceptual change required modifying 8+ files. These suggest missing abstractions
3. **God types**: Identify types with both high field count AND high method count AND high fan-in. A struct with 12 fields, 20 methods, and 30 dependents is accumulating responsibilities
4. **Hidden temporal coupling**: From the co-change data, identify file pairs that appear together in >40% of commits. These are either legitimately coupled (same module) or hiding a dependency that should be made explicit

### All stacks

1. **Test coverage gaps**: identify core business logic files with no corresponding test file
2. **Documentation gaps**: identify public APIs (exported functions, public types) without documentation
3. **Naming pattern outliers**: flag files or functions that break the naming convention used by their siblings
</instructions>

---

## Step 6 — Produce the audit report

<instructions>
Consume all data from Steps 2-5 and produce the final report.

### Output format

Use this exact structure:

```
## Audit Report: <project name>

**Stack**: <detected stacks>
**Scope**: <N files | N lines | additional metrics per stack>

---

### Critical

| # | Issue | File:Line | Impact | Blast Radius | Fix |
|---|-------|-----------|--------|--------------|-----|

### High

| # | Issue | File:Line | Impact | Blast Radius | Fix |
|---|-------|-----------|--------|--------------|-----|

### Medium

| # | Issue | File:Line | Impact | Blast Radius | Fix |
|---|-------|-----------|--------|--------------|-----|

### Low

| # | Issue | File:Line | Impact | Blast Radius | Fix |
|---|-------|-----------|--------|--------------|-----|

---

### Missing Defences

| # | Defence | Scope | Impact if Absent | Recommendation |
|---|---------|-------|-----------------|----------------|

### Critical Path Findings

| # | Path Traced | Finding | File:Line | Impact |
|---|-------------|---------|-----------|--------|

---

### Top 5 Refactoring Targets

1. **File** (N lines) -- reason, estimated scope, N callers affected

### Architecture Observations

- Observation with quantitative evidence

### Quantitative Strengths

- Strength with numbers (e.g., "0 unsafe blocks across N files")
```

Omit severity sections that have zero findings. Omit Missing Defences if no defences are missing. Omit Critical Path Findings if the deep read produced no findings. Classify each finding using the severity definitions at the top of this skill.
</instructions>

<examples>
<example>
GOOD finding (evidence-backed, specific, actionable, with fix):

| 3 | `.expect()` on semaphore acquire in async request path | `multicall.rs:85` | Panics during graceful shutdown when Arc is dropped | 12 callers via call graph | Per `err-1`: replace `.expect()` with `.acquire().await.map_err(\|e\| AppError::Semaphore(e))?` and handle the closed-semaphore case in the caller |
</example>

<example>
GOOD strength (quantitative):

- 0 `unsafe` blocks across 204 files; full memory safety maintained through type system
- All 39 port traits bounded with `Send + Sync`; no async safety gaps
- 1012 function calls tracked, average fan-out of 13 calls per function
</example>

<example>
GOOD missing-defence finding:

| 2 | Request timeout | All 14 handler functions in `api/` | No timeout on outbound HTTP calls to payment service; a slow upstream causes thread pool exhaustion | Add `tokio::time::timeout` wrapping each outbound call, or configure a global client timeout |
</example>

<example>
GOOD efficiency finding:

| 5 | N+1 query in order listing | `order_repo.rs:67` | Loop calls `get_customer()` per order instead of batch `get_customers(ids)` — 15 orders = 16 DB round-trips; batch into 2 | 8 callers via call graph | Per `perf-4`: collect IDs with `.map(\|o\| o.customer_id).collect()`, then call `get_customers_by_ids(ids)` in a single query returning a `HashMap<Id, Customer>` |
</example>

<example>
BAD finding (vague, no evidence, no fix):

| 1 | Error handling could be improved | various files | unclear | unknown | — |
</example>

<example>
BAD strength (hollow praise):

- The codebase has excellent architecture and clean separation of concerns
</example>
</examples>

---

## Step 7 — Offer drill-down

<instructions>
After presenting the report, offer interactive exploration options based on the detected stack.

### Rust projects (via rustgraph)

```
Entity exploration:
- "Show all context for function <name>"    -> rustgraph function <name>
- "Show all context for struct <type>"      -> rustgraph struct <type>
- "Show trait implementors for <trait>"     -> rustgraph trait <trait>

Relationship traversal:
- "What depends on <name>?"                -> rustgraph deps <name> --reverse
- "What does <name> depend on?"            -> rustgraph deps <name>
- "Show the call graph around <function>"  -> rustgraph graph <name> --format dot

Search and discovery:
- "Search for <term>"                      -> rustgraph search <term>
- "Show everything in <file>"             -> rustgraph file <path>

Or run raw SQL against the graph.
```

### React/TypeScript projects

```
- "Show me all components over N lines"
- "Find all uses of <pattern>"
- "Show the import graph for <component>"
- "List all error boundaries"
```

### All stacks

```
- "Drill into finding #N"     -> Read the file, show context, explain the issue
- "Show test coverage for <module>"
- "What are the most-changed files?"
```

For drill-down requests, read relevant source files and provide full context with your analysis.
</instructions>

---

## References

- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) — C-* rules for naming, interoperability, documentation, type safety
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/) — M-* rules for error handling, async, documentation, testing, safety
- [Rust Unofficial Patterns](https://rust-unofficial.github.io/patterns/) — Idioms, design patterns, and anti-patterns
- [React Rules](https://react.dev/reference/rules) — Official React rules
- [rustgraph](https://github.com/thethirdorigin/rustgraph) — Knowledge graph builder for Rust codebases
