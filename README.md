# thethirdorigin skills

Private skills marketplace for Claude Code. Best practices, code quality, and systematic project analysis.

## Skills

| Skill | Type | What it covers |
|-------|------|----------------|
| **project-guide** | Workflow | 6-phase workflow for analysing any codebase and building features systematically. Orchestrates all other skills. Includes codegraph-based discovery and audit quality gate. |
| **audit** | Workflow | Master code auditor. Detects the project stack, uses codegraph for structural analysis on all stacks, invokes language-specific sub-skills, and produces a severity-ranked findings report. |
| **reviewpr** | Workflow | Deep code review for GitHub PRs. Delegates analysis to audit, then posts findings as line-specific comments. |
| **grill-me** | Workflow | Stress-test a plan or design through relentless questioning. |
| **codegraph** | Tool | Semantic code intelligence for all languages. MCP tools, CLI, database schema, and reusable SQL query patterns for exploring any codebase via a knowledge graph. Replaces grep/glob for symbol search, call tracing, and structural exploration. Used by audit and project-guide as a composable building block. |
| **rust-best-practises** | Standards | ~280 rules across 20 categories. Error handling, ownership, memory optimisation, API design, async, compiler optimisation, type safety, unsafe, traits, naming, testing, docs, performance, project structure, linting, and anti-patterns. |
| **react-best-practises** | Standards | 78 rules across 11 categories. Hooks, state, components, TypeScript, error handling, security, testing, accessibility, and anti-patterns. Complements Vercel performance skill. |
| **prompt-best-practises** | Meta | Meta-skill for authoring other skills. XML structuring, examples, role assignment, agentic patterns. |

## Installation

### Option A: Manual install (recommended)

Clone the repo and symlink the skills into your global Claude Code skills directory:

```bash
# Clone (if not already cloned)
git clone git@github.com:thethirdorigin/skills.git ~/github/thethirdorigin/skills

# Symlink each skill to global skills directory
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/project-guide ~/.claude/skills/project-guide
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/audit ~/.claude/skills/audit
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/reviewpr ~/.claude/skills/reviewpr
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/grill-me ~/.claude/skills/grill-me
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/rust-best-practises ~/.claude/skills/rust-best-practises
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/react-best-practises ~/.claude/skills/react-best-practises
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/codegraph ~/.claude/skills/codegraph
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/prompt-best-practises ~/.claude/skills/prompt-best-practises
```

To update: `git -C ~/github/thethirdorigin/skills pull` — symlinks pick up changes automatically.

To install into a specific project instead of globally, symlink into `.claude/skills/` within the project directory.

### Option B: Plugin marketplace (if `/plugin` is available)

Run these commands in the Claude Code chat box:

```
/plugin marketplace add thethirdorigin/skills
/plugin install thethirdorigin-skills@thethirdorigin
```

> **Private repo**: Requires SSH keys or `GITHUB_TOKEN` / `GH_TOKEN` env variable with `repo` scope.

### Option C: Per-project install via `npx skills`

```bash
npx skills add thethirdorigin/skills
```

> **Note**: This installs per-project into `.claude/skills/`. Run in each repo where you need the skills.

## Companion skills (recommended)

Some skills reference external companion skills that complement them. These are maintained by third parties and installed separately.

### Vercel Agent Skills

The **react-best-practises** skill covers architecture, correctness, and quality but deliberately excludes performance — that's covered by Vercel's 69-rule performance skill. The **project-guide** also references Vercel's web-design-guidelines and composition-patterns.

Install Vercel skills in any project:

```bash
npx skills add vercel-labs/agent-skills
```

This installs (per-project, into `.claude/skills/`):
- `vercel-react-best-practices` — React/Next.js performance optimisation (69 rules across 8 priority tiers)
- `vercel-composition-patterns` — Component composition patterns that scale
- `web-design-guidelines` — UI compliance auditing (100+ accessibility and UX rules)
- `vercel-react-view-transitions` — View Transition API guide
- `vercel-react-native-skills` — React Native/Expo patterns
- `deploy-to-vercel` — Deployment automation
- `vercel-cli-with-tokens` — Vercel CLI with token auth

> **Note**: Vercel skills are installed per-project (not global). Run `npx skills add` in each repo where you need them.

## How the skills work together

```
project-guide (orchestrator)
├── Phase 1: Context Gathering
│   ├── discovers project structure, tech stack, git history
│   └── ALL projects: indexes codebase via codegraph skill (symbol graph, call tracing)
├── Phase 2: Pattern Identification ─── finds conventions, shared code, anti-patterns
├── Phase 3: Analysis ─── cross-references language-specific skills:
│   ├── rust-best-practises ─── ~280 Rust rules (ownership, API, memory, async, ...)
│   ├── react-best-practises ─── 78 React/TS rules (hooks, state, security, a11y, ...)
│   │   └── (companion) vercel-react-best-practices ─── for performance
│   └── (future) terraform-best-practises, python-best-practises, etc.
├── Phase 4: Implementation ─── enforces consistency, checklists, documentation
├── Phase 5: Questions ─── asks when requirements are unclear (with recommendations)
└── Phase 6: Quality Gate ─── runs audit skill to verify implementation

audit (code quality orchestrator)
├── Detects stack (Rust, React/TS, Python, Go, ...)
├── ALL stacks: codegraph (structural analysis, call graph, impact, symbol search)
├── Rust: rust-best-practises (language-specific rules)
├── React/TS: react-best-practises (language-specific rules)
├── Cross-correlates findings, deduplicates, ranks by severity
└── Produces evidence-based report with file:line references

codegraph (composable building block)
├── Invoked by audit, project-guide, or directly by user
├── Semantic search, call graph, impact analysis, file structure
├── MCP tools (primary) or CLI + raw SQL (fallback)
└── Supports 17+ languages: TS, JS, Python, Go, Rust, Java, C#, ...

reviewpr (PR wrapper)
├── Gathers PR context via gh CLI (diff, comments, changed files)
├── Delegates code analysis to audit skill (which uses codegraph)
├── Deduplicates against existing reviewer comments
└── Posts approved findings as inline GitHub comments

prompt-best-practises ─── used when creating or improving any of the above skills
```

## Skill triggers

Skills activate automatically based on what you're doing:

| Trigger phrase | Skill activated |
|----------------|-----------------|
| "I need to add a Rust endpoint" | rust-best-practises |
| "Create a new React component" | react-best-practises |
| "Starting work on a new feature" | project-guide |
| "What should I know about this project?" | project-guide |
| "Audit this codebase" | audit |
| "Find code smells" | audit |
| "Review this PR" | reviewpr |
| "Grill me on this design" | grill-me |
| "I want to create a new skill" | prompt-best-practises |
| "Use codegraph" / "Query knowledge graph" / "Find symbol" | codegraph |
| "Explore codebase" / "What calls this?" / "Trace callers" | codegraph |

## Adding new skills

1. Create a directory under `plugins/thethirdorigin-skills/skills/<skill-name>/`
2. Add a `SKILL.md` with frontmatter (`name`, `description`, `triggers`)
3. Use the **prompt-best-practises** skill to structure the content
4. If the skill is language-specific, add a checklist to **project-guide** Phase 4
5. Update **project-guide** Phase 3 and the Extensibility section to cross-reference it
6. If the skill provides coding standards, register it in **audit** Step 1 (stack detection table)
7. Bump the version in `marketplace.json`

## Repository structure

```
.claude-plugin/
  marketplace.json                    <- marketplace manifest
plugins/thethirdorigin-skills/
  .claude-plugin/
    plugin.json                       <- plugin manifest
  skills/
    project-guide/SKILL.md            <- orchestrator, 6-phase workflow
    audit/SKILL.md                    <- master code auditor
    reviewpr/SKILL.md                 <- PR review (delegates to audit)
    grill-me/SKILL.md                 <- design interviews
    rust-best-practises/
      SKILL.md                        <- ~280 Rust rules across 20 categories
      rules/                          <- individual rule files (287 .md files)
    react-best-practises/
      SKILL.md                        <- 78 React/TS rules across 11 categories
      rules/                          <- individual rule files
    codegraph/SKILL.md                <- codegraph semantic code intelligence (all languages)
    prompt-best-practises/SKILL.md    <- meta-skill for skill authoring
```

## Sources

These skills were built from authoritative sources:

**Rust**
- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) — C-\* rules for API design
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) — 60+ M-\* production rules
- [Rust Performance Book](https://nnethercote.github.io/perf-book/) — Practical performance optimisation
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) — Official formatting conventions
- [Apollo Rust Best Practices](https://github.com/apollographql/rust-best-practices) — Production patterns
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce)
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) — Concrete rules with code examples (MIT, merged into rust-best-practises)
- [CodeGraph](https://github.com/colbymchenry/codegraph) — Semantic code intelligence for all languages

**React/TypeScript**
- [React Rules](https://react.dev/reference/rules) — Official component and hook rules
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/)
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices)

**Prompt Engineering**
- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
