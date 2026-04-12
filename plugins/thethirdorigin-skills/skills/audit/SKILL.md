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

**High** — causes maintenance pain, hides bugs, or blocks refactoring:
- Missing `Debug` on domain types used in logging/tracing (C-DEBUG violation)
- Dead code hidden behind `#[allow(dead_code)]` without justification
- Single-impl traits that exist only for over-abstraction (not for DI testability)
- Functions exceeding 100 body lines / Components exceeding 500 lines
- Files exceeding 1000 lines
- `any` types in TypeScript without justification
- Missing error boundaries at route level
- Secrets or API keys in client-side code

**Medium** — inconsistency, code smell, or mild architectural violation:
- Missing `Debug` on infrastructure types
- Derive inconsistencies within a module (sibling structs with different derive sets)
- Functions between 40-100 body lines
- Structs with more than 8 fields
- Handlers performing orchestration logic (batch processing, filtering, reordering)
- Naming inconsistencies across sibling types
- Missing loading/error state handling for async operations
- Index-based keys in dynamic React lists

**Low** — minor style or convention issues:
- Functions with more than 5 parameters
- Missing `Serialize`/`Deserialize` on internal-only types
- Minor naming style differences
- Missing aria-labels on icon-only buttons

## False Positive Filters

Exclude these from findings:
- Test code using `.unwrap()`/`.expect()` (inside `#[cfg(test)]` modules or test files)
- Single-impl traits where `mockall` is a dev-dependency (port traits for DI are justified)
- Generated code (proto files, `build.rs` output, `target/` directory, auto-generated types)
- `node_modules/`, `dist/`, `build/` directories
- Do not report the same issue at multiple severity levels

</document>

---

# Code Audit

<context>
You are a senior engineer performing a systematic, evidence-based audit of a codebase. You detect the project's tech stack, invoke the appropriate sub-skills, gather quantitative data, and apply judgment to produce findings.

Sub-skills in your toolbelt (loaded automatically by the plugin):
- **rust-best-practises** — Rust coding standards, API design, and best practices (~280 rules)
- **rustgraph** — Tool knowledge for indexing and querying a Rust codebase knowledge graph
- **react-best-practises** — React/TypeScript conventions and best practices (78 rules)

This skill follows a strict **measure first, judge second** methodology. Every finding must cite file:line references. Every strength must cite quantitative evidence.
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
Run data-gathering steps for each detected stack. Store all results internally for Steps 3-4. Do not output findings yet.

### Rust projects

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

### All stacks

1. File sizes: identify files over 1000 lines
2. Test coverage indicators: ratio of test files to source files
3. Git churn: `git log --format=format: --name-only --since="3 months ago" | sort | uniq -c | sort -rn | head -20` (most-changed files are high-risk)

Output: nothing. All data stored for subsequent steps.
</instructions>

---

## Step 3 — Assess against best practices

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

### For each finding, record

| Field | Rules |
|-------|-------|
| File:Line | Line number in the source file |
| Severity | Classify using the severity definitions at the top of this skill |
| Issue | One sentence, factual, no hedging |
| Impact | What goes wrong if this is not fixed |
| Blast Radius | How many callers/consumers/dependents are affected |
| Suggested Fix | One sentence, concrete action |

### Deduplicate

- Do not flag the same issue under multiple severity levels
- Do not flag the same pattern in every file; flag it once and note "N occurrences across M files"
- Apply the false positive filters before including any finding
</instructions>

---

## Step 4 — Cross-correlate

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

### All stacks

1. **Test coverage gaps**: identify core business logic files with no corresponding test file
2. **Documentation gaps**: identify public APIs (exported functions, public types) without documentation
3. **Naming pattern outliers**: flag files or functions that break the naming convention used by their siblings
</instructions>

---

## Step 5 — Produce the audit report

<instructions>
Consume all data from Steps 2-4 and produce the final report.

### Output format

Use this exact structure:

```
## Audit Report: <project name>

**Stack**: <detected stacks>
**Scope**: <N files | N lines | additional metrics per stack>

---

### Critical

| # | Issue | File:Line | Impact | Blast Radius |
|---|-------|-----------|--------|--------------|

### High

| # | Issue | File:Line | Impact | Blast Radius |
|---|-------|-----------|--------|--------------|

### Medium

| # | Issue | File:Line | Impact | Blast Radius |
|---|-------|-----------|--------|--------------|

### Low

| # | Issue | File:Line | Impact | Blast Radius |
|---|-------|-----------|--------|--------------|

---

### Top 5 Refactoring Targets

1. **File** (N lines) -- reason, estimated scope, N callers affected

### Architecture Observations

- Observation with quantitative evidence

### Quantitative Strengths

- Strength with numbers (e.g., "0 unsafe blocks across N files")
```

Omit severity sections that have zero findings. Classify each finding using the severity definitions at the top of this skill.
</instructions>

<examples>
<example>
GOOD finding (evidence-backed, specific, actionable):

| 3 | `.expect()` on semaphore acquire in async request path | `multicall.rs:85` | Panics during graceful shutdown when Arc is dropped | 12 callers via call graph |
</example>

<example>
GOOD strength (quantitative):

- 0 `unsafe` blocks across 204 files; full memory safety maintained through type system
- All 39 port traits bounded with `Send + Sync`; no async safety gaps
- 1012 function calls tracked, average fan-out of 13 calls per function
</example>

<example>
BAD finding (vague, no evidence):

| 1 | Error handling could be improved | various files | unclear | unknown |
</example>

<example>
BAD strength (hollow praise):

- The codebase has excellent architecture and clean separation of concerns
</example>
</examples>

---

## Step 6 — Offer drill-down

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
