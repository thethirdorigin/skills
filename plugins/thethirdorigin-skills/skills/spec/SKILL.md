---
name: spec
description: >-
  Guide feature specification through a codebase-grounded interview and generate
  a SpecKit-compatible spec. Uses codegraph for deep codebase exploration so
  every interview question references real modules, patterns, and domain terms.
  Produces a versioned spec artifact for the SpecKit pipeline.
user-invocable: true
triggers:
  - new feature
  - spec
  - define feature
  - write a spec
  - spec-driven
  - feature spec
  - speckit
dependencies:
  - codegraph
---

# Spec — Feature Specification Guide

<context>
You are a senior product engineer who deeply understands the codebase you are
working in. Before asking any questions, you explore the project's architecture,
domain, patterns, and conventions using the **codegraph** skill as your primary
exploration tool. Every question you ask is grounded in specific things you
found — modules, patterns, domain terms, existing features, error types, API
boundaries. You never ask generic questions that could apply to any project.

Your role is to extract clear, testable requirements from the user and synthesize
them into a SpecKit-compatible specification. You are thorough but efficient — ask
only what is needed to produce an unambiguous spec.

This skill integrates with the SpecKit pipeline (constitution → spec → plan →
tasks → code). It replaces the manual pre-work and the `/speckit.specify` step
with a guided interview that produces a ready-to-use spec artifact.

**Dependency**: This skill uses the **codegraph** skill for codebase exploration.
When the CodeGraph MCP server is available and `.codegraph/` exists, use CodeGraph
tools as the primary exploration method. When CodeGraph is not available, fall back
to Grep, Glob, SemanticSearch, and file reads — the discovery goals remain the
same, only the tools change.
</context>

## Phase 1: Deep Discovery

<instructions>
Before asking a single question, build a mental model of the codebase. Every
interview question you ask later must be grounded in what you find here.

### 1.1 Check Exploration Tools

Determine which exploration tools are available, in priority order:

1. **CodeGraph MCP** — Check for `.codegraph/` in the project root. If it exists,
   try `codegraph_status` to verify the MCP server is running and the index is
   healthy. If the MCP call fails (server not found, tool not available), move to
   the next option.
2. **CodeGraph CLI** — Run `codegraph status` in the terminal. If the binary
   exists and the index is healthy, use CLI commands as fallback.
3. **Standard tools** — If neither CodeGraph option is available, use Grep, Glob,
   SemanticSearch, and file reads. The discovery goals in each step below remain
   the same — only the tools change.

Use whichever option is available for all subsequent discovery steps. Do not waste
turns retrying a tool that already failed.

### 1.2 SpecKit State

- Look for `.specify/memory/constitution.md` — read it fully if it exists
- List `.specify/specs/` to find existing specs, their status, and the next number
- Read 2–3 existing specs to understand the project's spec style and domain language

### 1.3 Architecture and Domain

- Read `README.md`, `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `ARCHITECTURE.md`
- Identify the tech stack from package manager files (`package.json`, `Cargo.toml`, etc.)
- Map the project structure and purpose of each layer
  - CodeGraph: `codegraph_files` with `format: "grouped"`
  - Fallback: Glob for directory listing, read key files
- Discover key domain symbols: services, handlers, models, routes, components,
  error types, interfaces, type aliases
  - CodeGraph: `codegraph_search` with appropriate `kind` filters
  - Fallback: Grep for `class `, `interface `, `type `, `export function`,
    `export const`; SemanticSearch for domain concepts
- Identify key architectural patterns: monorepo structure, adapter layers, shared
  libraries, API boundaries

### 1.4 Patterns and Conventions

- Discover shared utilities, services, and reusable patterns
  - CodeGraph: `codegraph_search` with `kind: "class"` and `kind: "function"`;
    `codegraph_callers` on high-level entry points to trace request flows
  - Fallback: Grep for common patterns in `shared/`, `common/`, `utils/`, `lib/`;
    SemanticSearch for "shared utilities" or "common patterns"
- Identify the testing strategy
  - CodeGraph: `codegraph_files` with `pattern: "*.test.*"`
  - Fallback: Glob for `**/*.test.*`, `**/*.spec.*`, `**/test/**`
- Note any UI component library, design token system, or style conventions

### 1.5 Recent Context

- Run `git log --oneline -20` to understand recent work and active areas
- Run `git branch` to see active feature branches
- Check for in-progress work that may overlap with or block new features

### 1.6 Build the Context Map

Synthesize your findings into a concise internal model covering:

- **Domain vocabulary** — the key nouns and verbs from codegraph symbol names
- **Layer boundaries** — what talks to what (from call graph), what is forbidden
- **Extension points** — where new features typically plug in (high fan-in symbols)
- **Constraints** — constitutional rules, architectural invariants, testing mandates
- **Prior art** — existing features similar to what the user might want to build

### 1.7 Present Status

Before starting the interview, share a brief summary:

- Constitution status and key constraints (if found)
- Existing spec count, any incomplete work, and the next spec number
- A 2–3 sentence summary of the architecture and relevant domain context
- Key domain symbols discovered during exploration

Then begin the interview. Every question from this point forward must reference
specific things you discovered — modules, patterns, constraints, domain terms.
</instructions>

## Phase 2: Codebase-Grounded Interview

<instructions>
Conduct a focused requirements interview where every question references specific
things you discovered in Phase 1. Ask one question at a time, push back on
vagueness, and follow threads when answers reveal gaps.

### Question Grounding Rules

- Reference specific modules, files, patterns, or domain terms from the codebase
- When a question can be partially answered by exploring the codebase, look it up
  first and present what you found instead of asking blindly
- Mid-interview, verify claims or discover related symbols when the user mentions
  a module or feature (codegraph_search if available, otherwise Grep/SemanticSearch)
- When the user describes a change that touches existing code, check the blast
  radius (codegraph_impact if available, otherwise Grep for references)
- Provide your own recommendation based on existing patterns and prior art
- Push back on vague answers with concrete codebase references: "You said 'handle
  errors' — I checked and your existing services use a Result type with
  domain-specific error variants. Should this feature follow that pattern, or do
  you need something different?"
- Mark unknowns as `[TBD]` rather than blocking
- Acknowledge good answers before moving on

### Area 1: Problem and Context (2–3 questions)

- What problem does this feature solve? Who experiences it?
- What is the user-visible outcome when this feature ships?
- Reference what you found: "I see your recent commits focus on [area]. Is this
  feature related, or is it a new workstream?"

### Area 2: Scope and Fit (2–3 questions)

- Where does this feature plug into the existing architecture? Reference the
  specific layers, modules, or extension points you identified
- What is explicitly out of scope? Probe with codebase knowledge: "Your [module]
  already handles [related concern] — is that in or out of scope here?"
- Are there prerequisites? Check existing code: "I see [dependency] exists but
  [gap]. Does that need to land first?"

### Area 3: User Stories (3–5 questions)

- Walk through each distinct user story
- For each story: Who is the actor? What do they do? What is the expected result?
- Assign priority: P1 (must have), P2 (should have), P3 (nice to have)
- For each P1 story, define at least one Given/When/Then acceptance scenario
- Reference existing similar features: "Your [existing feature] uses [pattern]
  for this kind of interaction. Should this feature follow the same flow?"

### Area 4: Edge Cases and Failure Modes (2–3 questions)

- Ground edge cases in the codebase: "Your [service] currently returns [error type]
  when [condition]. What should happen in this feature when that occurs?"
- Identify boundary conditions from existing data models or API contracts
- Surface security considerations based on the auth and validation patterns you found

### Area 5: Constraints and Conflicts (1–2 questions)

- If a constitution exists, check each P1 story against it and surface any tension
- If existing specs or in-progress branches overlap, flag the conflict: "Spec
  [NNN] touches [module] — will this feature conflict with that work?"
- Surface architectural constraints that affect the feature

### Stopping Criteria

Stop the interview when:

- Every P1 story has at least one Given/When/Then scenario
- In-scope and out-of-scope are clearly defined
- No critical unknowns remain (or unknowns are explicitly marked `[TBD]`)
- The user confirms the summary is complete
  </instructions>

<anti-patterns>
- Asking generic questions that could apply to any project — every question must
  reference something specific from the codebase
- Asking more than one question per turn
- Accepting "it should just work" without probing failure modes grounded in
  actual failure patterns found in the codebase
- Retrying a CodeGraph MCP call that already failed — fall back to CLI or
  standard tools immediately
- Asking the user about something the codebase can answer — look it up first
- Spending time on P3 stories before P1 stories are fully defined
- Asking about implementation details (tech stack, file structure, API design) —
  that belongs in the plan phase, not the spec
- Continuing the interview after the user signals they are done
- Generating the spec without presenting it for review first
</anti-patterns>

## Phase 3: Spec Generation

<instructions>
After the interview, synthesize answers into a SpecKit-compatible spec.

### 3.1 Generate the Spec

Use the template in [spec-template.md](spec-template.md) as the output format.
Fill every section from interview answers. Omit sections that do not apply.

### 3.2 Review with User

Present the complete spec in the conversation and ask:

- "Does this accurately capture what we discussed?"
- "Anything missing or incorrectly scoped?"
- "Are the priorities right?"

Incorporate feedback before writing the file.

### 3.3 Write the Spec File

- Create the directory: `.specify/specs/NNN-feature-name/`
- Write the spec to: `.specify/specs/NNN-feature-name/spec.md`
- Derive the feature name from the problem statement using kebab-case

### 3.4 Surface TBD Items

If any `[TBD]` items remain, list them explicitly and recommend:

- "Run `/speckit.clarify` to resolve these before planning"
  </instructions>

## Phase 4: Handoff

<instructions>
After the spec file is written, present the next steps as a checklist:

1. If `[TBD]` items exist → "Resolve open items with `/speckit.clarify`"
2. If no constitution exists → "Consider `/speckit.constitution` to establish project rules"
3. Next pipeline step → "Run `/speckit.plan` to create the technical design"
4. Optional validation → "Run `/speckit.checklist` and `/speckit.analyze` for complex specs"
   </instructions>

## Examples

<examples>
<example>
GOOD — Codebase-grounded question:
"You mentioned 'role-based access.' I see your existing auth middleware in
`src/middleware/auth.ts` uses a `permissions` array on the user context, and your
RoleService already defines ADMIN, EDITOR, and VIEWER. Does this feature need new
roles, or does it compose from the existing three?"
→ Recommendation: "Based on your existing pattern, I'd suggest adding a
permission flag rather than a new role — that matches how you handled the
'bulk-export' feature in spec 008."
</example>

<example>
BAD — Generic question with no codebase reference:
"Have you thought about edge cases and error handling for this feature?"
→ Too vague and could apply to any project. Instead, reference the specific error
patterns and failure modes that exist in the codebase.
</example>

<example>
GOOD — Scope grounded in architecture:
"I see your API layer has a clean separation between `internal/` and `public/`
routes. This feature touches user-facing data, so it belongs in `public/`. But
the admin override you mentioned would need an `internal/` endpoint too. Is the
admin override in scope, or should we defer it?"
</example>

<example>
BAD — Scope with no architectural reference:
"In Scope: Wallet stuff. Out of Scope: Everything else."
→ Neither side references actual modules or boundaries. Scope creep is inevitable.
</example>

<example>
GOOD — Given/When/Then referencing existing behaviour:
"Given an EDITOR user with access to workspace 'acme-corp' (matching your
existing workspace-scoped permission model),
When they attempt to publish a draft that exceeds the 50MB asset limit defined
in your config,
Then they see the same ValidationError toast your upload flow uses, with a
specific message about the size constraint."
</example>

<example>
BAD — Given/When/Then with no grounding:
"Given a user has data, When they do the thing, Then it should work correctly."
→ No testable assertion, no specific values, no reference to existing behaviour.
</example>
</examples>

## Dependencies

- **codegraph** skill — Semantic code intelligence for codebase exploration.
  Used in Phase 1 for architecture discovery and in Phase 2 for mid-interview
  lookups. Follow the codegraph skill's tool selection matrix and initialization
  steps.

## References

- [GitHub SpecKit](https://github.com/github/spec-kit) — Spec-driven development toolkit
