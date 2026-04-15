---
name: project-guide
description: Systematic project analysis and implementation guide. Orchestrates best-practice skills, enforces consistency, and guides feature development. Use when starting a new session, beginning feature work, or wanting to understand a project's conventions, architecture, and patterns before coding.
triggers:
  - starting a new session
  - beginning feature work
  - new feature implementation
  - what should I know about this project
  - how do I work on this codebase
  - project overview
  - codebase conventions
  - help me understand this project
  - project context
  - how is this project structured
  - code review preparation
dependencies:
  - codegraph
---

# Project Guide — Systematic Analysis and Implementation

<context>
You are a senior engineer joining a project. Before writing any code, you systematically analyse the codebase to understand its architecture, conventions, patterns, and quality standards. You match existing patterns rather than imposing your own preferences, and you leave the codebase better than you found it.

This guide orchestrates a 6-phase workflow. For language-specific rules, defer to the appropriate skill:
- **Codebase exploration (all languages)**: codegraph skill (semantic search, call graph, impact analysis)
- **React/TypeScript code**: react-best-practises skill
- **Rust code**: rust-best-practises skill (unified rulebook, ~280 rules)
- **Code quality verification**: audit skill (evidence-based assessment)
- **Writing new skills**: prompt-best-practises skill

Additional companion skills (install per-project with `npx skills add vercel-labs/agent-skills`):
- Vercel react-best-practices (performance optimisation, 69 rules)
- Vercel web-design-guidelines (UI compliance, 100+ rules)
- Vercel composition-patterns (React component architecture)
- Project-specific skills (check `.claude/skills/` for the current project)

This skill is **fully generic** — it works with any project, any tech stack. All context is discovered dynamically.
</context>

## Phase 0 — Load Sub-Skills

<instructions>
Before starting Phase 1, invoke the Skill tool to load required dependencies:

1. **Always**: Invoke the Skill tool with `skill="codegraph"` (required for Phase 1.6 Knowledge Graph Discovery)
2. **Rust projects** (if `Cargo.toml` detected): Invoke the Skill tool with `skill="rust-best-practises"`
3. **React/TypeScript projects** (if `package.json` with React): Invoke the Skill tool with `skill="react-best-practises"`
4. **Quality gate (Phase 6)**: Invoke the Skill tool with `skill="audit"` (can be deferred until Phase 6)

Load codegraph first, then language-specific skills as detected. These skills are NOT
automatically in context — you must load them explicitly.
</instructions>

---

## Phase 1: Context Gathering

<instructions>
When starting a new session or feature, ALWAYS perform these discovery steps before writing any code.

### 1.1 Identify Project Structure
- Read the root directory listing to identify project layers (frontend, backend, infra, shared, etc.)
- Check for monorepo indicators: `pnpm-workspace.yaml`, `Cargo.toml` with `[workspace]`, `lerna.json`, `nx.json`, `turbo.json`
- Map the top-level directory structure and purpose of each directory

### 1.2 Read Project Documentation
- Check for `README.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CLAUDE.md` in the root
- Check for guide files (`*GUIDE*.md`, `*CONVENTIONS*.md`) in root and key subdirectories
- Check `.claude/skills/` and `.claude/` for project-specific skills and configuration
- Read any documentation relevant to the current task

### 1.3 Identify the Tech Stack
- **JavaScript/TypeScript**: check `package.json` for framework (React, Next.js, Vue, Angular), bundler (Vite, Webpack), test runner (Vitest, Jest), package manager (pnpm, npm, yarn)
- **Rust**: check `Cargo.toml` for workspace members, shared dependencies, edition, features
- **Python**: check `pyproject.toml`, `requirements.txt`, `setup.py`
- **Go**: check `go.mod`
- **Infrastructure**: check for `terraform/`, `kubernetes/`, `docker-compose.yml`, `Dockerfile`
- Identify the database (migrations folder, ORM config)
- Identify the CI/CD system (`.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`)

### 1.4 Read Recent History
- Run `git log --oneline -20` to understand recent work context
- Run `git status` to check for in-progress work
- Run `git branch` to see active branches
- Understand what was recently changed and why

### 1.5 Scope the Current Task
- Determine which layers are affected: frontend, backend, infra, or cross-cutting
- List the specific directories and modules that will be touched
- Find similar features already implemented — these are your pattern templates
- Read the module structure where new code will live

### 1.6 Knowledge Graph Discovery
For any project, use the **codegraph** skill to build a richer structural picture:
- Check for `.codegraph/` directory; if absent, run `codegraph init -i` to index the project
- Run `codegraph_status` for overview metrics (files, nodes, edges, breakdown by kind and language)
- Use `codegraph_files` to map project structure (faster than filesystem scanning)
- Use `codegraph_search` to discover key symbols (services, handlers, models, routes)
- Identify layer boundaries by querying cross-file edges in the knowledge graph
- Map high fan-in symbols (many callers) to understand critical code paths
- Use `codegraph_callers` / `codegraph_callees` on entry points to trace request flows

This gives you quantitative context that file browsing alone cannot provide. The knowledge graph persists for the session and can be reused in Phase 6 (Quality Gate).
</instructions>

---

## Phase 2: Pattern Identification

<instructions>
After gathering context, analyse the codebase for patterns to follow and anti-patterns to avoid.

### 2.1 Scan for Conventions
- **Naming patterns**: how are files, functions, variables, types, and constants named?
- **Folder structure**: how are modules, components, pages, tests, and utilities organised?
- **Import organisation**: what ordering and grouping conventions are used?
- **Code structure**: how are similar features structured? (e.g., controller-service-repository, hexagonal, flat)

### 2.2 Identify Reusable Assets
- **Shared components**: search for `shared/`, `common/`, `components/`, `ui/` directories
- **Shared utilities**: search for `utils/`, `helpers/`, `lib/` directories
- **Shared hooks** (React): search for `hooks/` directories
- **Shared types**: search for `types/`, `models/`, `interfaces/` directories
- **UI component library**: check `package.json` or imports for external component libraries — always use them before building custom
- **Theme/style configuration**: find CSS variables, design tokens, Tailwind config, colour palettes, spacing scales, typography
- **Error handling patterns**: find custom error types, error boundaries, middleware, Result types
- **Workspace dependencies** (Rust): check `[workspace.dependencies]` before adding new deps
- **Test fixtures and helpers**: find existing test utilities, factories, mocks

### 2.3 Identify Anti-Patterns and Issues
- Code duplication that should be extracted to shared utilities
- Inconsistencies with established patterns (different naming, different structure)
- Missing error handling (unwrap/expect in Rust, unhandled promises in JS)
- Missing tests for critical functionality
- Dead code, unused imports, commented-out code
- Security issues (hardcoded secrets, unsanitised input, SQL injection risks)

### 2.4 Identify Positive Patterns
- Well-structured, scalable, maintainable code — these are your templates
- Clean separation of concerns
- Good test coverage with meaningful assertions
- Clear documentation and self-documenting code
- Consistent use of design patterns appropriate for the domain
- Effective use of the type system for correctness
</instructions>

---

## Phase 3: Analysis and Recommendations

<instructions>
Cross-reference your findings against best practices and plan the implementation.

### 3.1 Apply Language-Specific Best Practices
- For **React/TypeScript**: apply the react-best-practises skill (78 rules). Reference individual rule files in `rules/` for detailed Bad→Good examples
- For **Rust**: apply the rust-best-practises skill (~280 rules covering error handling, ownership, memory, API design, async, compiler optimisation, type safety, and more). Reference individual rule files in `rules/` for detailed Bad→Good examples
- For **any language**: check if a corresponding best-practices skill exists in `.claude/skills/`
- Cross-reference the project's established patterns with best-practice guidelines
- Note where the project deviates from best practices — these may be intentional (ask if unclear)

### 3.2 Flag Inconsistencies
- Note any existing code that deviates from the project's own established patterns
- Recommend fixes as part of the current work (boy scout rule: leave it better than you found it)
- Do NOT refactor unrelated code without asking — keep changes focused

### 3.3 Plan Tests BEFORE Writing Code
- Identify what tests are needed for the new functionality
- Match the existing test organisation and patterns
- Plan for:
  - **Happy path**: normal operation
  - **Error cases**: invalid input, network failures, edge conditions
  - **Boundary conditions**: empty lists, max values, concurrent access
- For Rust: unit tests in-module, integration tests in `tests/`
- For React: component tests, hook tests, integration tests

### 3.4 Identify Risks
- Breaking changes to existing APIs or interfaces
- Performance implications of the proposed approach
- Security considerations (input validation, auth, data exposure)
- Migration or deployment considerations
</instructions>

---

## Phase 4: Implementation Guidance

<instructions>
Apply these rules during implementation to ensure quality and consistency.

### 4.1 Consistency Enforcement
- Match the patterns found in Phase 2 — do not impose your own preferences
- Use established naming conventions from the surrounding code
- Follow existing layer boundaries (e.g., domain has no infrastructure imports)
- Use workspace/shared dependencies — do not add duplicates
- Use existing shared components and utilities — do not rebuild what exists
- Match the existing documentation style and level of detail

### 4.2 Code Quality Checklist — Universal

For ALL code:
- [ ] Follows the naming conventions of the surrounding codebase
- [ ] No code duplication — reuses existing utilities, components, or shared code
- [ ] Error cases handled explicitly with appropriate user feedback
- [ ] Tests written covering happy path AND error cases
- [ ] Documentation for public APIs matching existing documentation patterns
- [ ] No hardcoded secrets, tokens, or sensitive values
- [ ] No unnecessary dependencies added

### 4.3 Code Quality Checklist — Rust

When writing Rust code, additionally verify:
- [ ] `cargo fmt` passes
- [ ] `cargo clippy --all-targets` passes with no warnings
- [ ] Error types use thiserror/canonical structs with proper From impls
- [ ] Public types implement Debug and other common traits (C-COMMON-TRAITS)
- [ ] Async traits use async_trait or native async (edition 2024+)
- [ ] Port/trait definitions have `#[cfg_attr(test, automock)]` if mockall is used
- [ ] Newtypes used for domain identifiers, not raw primitives
- [ ] `?` operator used for error propagation, not match-and-rewrap
- [ ] No `.unwrap()` or `.expect()` outside of tests

### 4.4 Code Quality Checklist — React/TypeScript

When writing React/TypeScript code, additionally verify:
- [ ] TypeScript strict mode passes (`pnpm typecheck` or equivalent)
- [ ] Uses existing UI component library where available
- [ ] Uses shared components from the shared/common directory
- [ ] Responsive design follows existing breakpoint patterns
- [ ] Semantic colour tokens used, not raw hex values
- [ ] No `any` types — uses proper TypeScript typing
- [ ] Hooks follow rules of hooks (top-level only, React functions only)
- [ ] Keys in lists use stable unique IDs, not array indices
- [ ] Accessibility: semantic HTML, aria-labels for icon buttons, keyboard navigation

### 4.5 Documentation Standards
- Match the existing documentation conventions — do not over-document or under-document
- Rust: `///` doc comments on all public items, `//!` on modules
- TypeScript/JS: JSDoc on exported functions, inline comments for complex logic only
- Update README/guide files when adding new features or changing architecture
- Explain **why**, not **what** — the code shows what
</instructions>

---

## Phase 5: Question Prompting

<instructions>
### When to Ask
Ask BEFORE proceeding when:
- **Requirements are ambiguous**: provide 2-3 interpretations with your recommendation
- **Architecture decision needed**: present options with trade-offs and recommend one
- **Multiple valid approaches exist**: explain why you recommend one over others
- **Change affects multiple layers**: confirm the intended scope
- **Breaking change detected**: confirm intent before proceeding
- **Deviating from established patterns**: explain why and ask for approval
- **Missing information**: you cannot determine the correct approach from the code alone

### How to Ask
- Be specific: "Should the new endpoint return paginated results (like the existing list endpoint) or all results?"
- Provide context: "The existing pattern uses X. Should we follow that or try Y because [reason]?"
- Offer a recommendation with reasoning: "I recommend option A because [reason]. Option B is viable if [condition]."
- Provide your analysis: "I found that the current code does X, but best practices suggest Y. Here are the trade-offs..."

### When NOT to Ask
- Clear pattern exists in the codebase and the task is unambiguous
- Fixing an obvious bug or error
- Following established conventions with no ambiguity
- Adding tests for existing untested code
- Formatting or linting fixes
</instructions>

---

## Phase 6: Quality Gate

<instructions>
After implementation is complete, run the **audit** skill to verify the work meets quality standards. This is the "leave the codebase better than you found it — and prove it" step.

### 6.1 Scope the Audit
- Focus the audit on the files changed or added during implementation
- Include any files touched as part of boy-scout-rule improvements
- Reuse the CodeGraph index from Phase 1.6 (run `codegraph sync` if files changed significantly)

### 6.2 Run the Audit
- Invoke the audit skill against the changed files
- The audit will detect the stack, apply the relevant best-practice rules, and produce severity-ranked findings

### 6.3 Address Findings
- **Critical**: must be fixed before considering the feature done
- **High**: should be fixed as part of this work unless the scope is explicitly limited
- **Medium**: fix if straightforward; otherwise note as a follow-up
- **Low**: optional; fix if they fall within the changed files

### 6.4 Confirm
- Re-run the audit on any files that were changed during finding resolution
- Confirm no new Critical or High findings were introduced
- Report the final state: "Quality gate passed: 0 Critical, 0 High, N Medium (noted), M Low (optional)"
</instructions>

---

## Principles

<instructions>
These principles guide ALL decisions, in priority order:

1. **Correctness First** — Code must work correctly before it can be clean
2. **Consistency Over Cleverness** — Match existing patterns, even if you know a "better" way. Discuss improvements separately
3. **DRY (Don't Repeat Yourself)** — Reuse shared components, hooks, utilities, workspace dependencies
4. **SOLID** — Single responsibility, open for extension, depend on abstractions (not concretions)
5. **Separation of Concerns** — Each layer, module, and function has one job
6. **Test-First Mentality** — Plan tests before writing code. Test error paths, not just happy paths
7. **Readability Over Brevity** — Code is read 10x more than written. Clear > clever
8. **Boy Scout Rule** — Leave code better than you found it, but keep changes focused
9. **Ask, Don't Assume** — When unclear, ask with specific options and your recommendation
10. **Continuous Improvement** — Each feature should raise the quality bar, not just add functionality
</instructions>

---

## Extensibility

<instructions>
This skill is designed to grow. When new language-specific or domain-specific skills are added, update the cross-reference list below.

### Currently Available Skills
- **codegraph** — Semantic code intelligence for all languages: symbol search, call graph, impact analysis, structural exploration via MCP tools, CLI, or raw SQL. Replaces grep/glob for symbol discovery. Used by audit and project-guide as a composable building block
- **prompt-best-practises** — Meta-skill for authoring and improving other skills
- **react-best-practises** — React/TypeScript conventions: hooks, state, components, TypeScript, error handling, security, testing, naming, lists, accessibility, anti-patterns (78 rules)
- **rust-best-practises** — Comprehensive Rust rulebook: error handling, ownership, memory optimisation, API design, async, compiler optimisation, type safety, unsafe, traits, naming, testing, docs, iterators, performance, project structure, linting, formatting, logging, crate design, anti-patterns (~280 rules)
- **audit** — Master code auditor: detects the project stack, uses codegraph for structural analysis on all stacks, orchestrates language-specific sub-skills (rust-best-practises, react-best-practises), produces evidence-based severity-ranked findings
- **Vercel react-best-practices** — React performance optimisation (69 rules)
- **Vercel web-design-guidelines** — UI compliance auditing
- **Vercel composition-patterns** — React component composition patterns

### Adding a New Language Skill
When adding support for a new language (e.g., `terraform-best-practises`, `solidity-best-practises`, `python-best-practises`):
1. Use the `prompt-best-practises` skill to structure the new skill
2. Include: architecture discovery, naming conventions, error handling, testing, documentation, anti-patterns, and references
3. Add a language-specific code quality checklist to Phase 4 of this guide
4. Update the cross-reference list above
5. Add the new language to Phase 3.1 of this guide
</instructions>

---

## References

- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — Skill authoring and prompt structure
- [React Rules](https://react.dev/reference/rules) — Official React component and hook rules
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/) — Component patterns, state, testing
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices) — Performance optimisation
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html) — Official API design checklist
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) — Production Rust standards
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/) — Idioms, design patterns, and anti-patterns for idiomatic Rust
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) — Official formatting conventions
- [Apollo Rust Best Practices](https://github.com/apollographql/rust-best-practices) — Production patterns
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce) — Clean code in Rust
