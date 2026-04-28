# thethirdorigin skills

Private skills marketplace for Claude Code. Best practices, code quality, and systematic project analysis.

## Skills

| Skill                     | Type      | What it covers                                                                                                                                                                                                                                                                                                   |
| ------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **project-guide**         | Workflow  | 6-phase workflow for analysing any codebase and building features systematically. Orchestrates all other skills. Includes codegraph-based discovery and audit quality gate.                                                                                                                                      |
| **audit**                 | Workflow  | Master code auditor. Detects the project stack, uses codegraph for structural analysis on all stacks, invokes language-specific sub-skills, and produces a severity-ranked findings report.                                                                                                                      |
| **reviewpr**              | Workflow  | Deep code review for GitHub PRs. Delegates analysis to audit, then posts findings as line-specific comments.                                                                                                                                                                                                     |
| **grill-me**              | Workflow  | Stress-test a plan or design through relentless questioning.                                                                                                                                                                                                                                                     |
| **spec**                  | Workflow  | Codebase-grounded feature specification. Uses codegraph to explore the project, then runs a structured interview where every question references real modules, patterns, and domain terms. Produces a SpecKit-compatible spec artifact.                                                                          |
| **codegraph**             | Tool      | Semantic code intelligence for all languages. MCP tools, CLI, database schema, and reusable SQL query patterns for exploring any codebase via a knowledge graph. Replaces grep/glob for symbol search, call tracing, and structural exploration. Used by audit and project-guide as a composable building block. |
| **rust-best-practises**   | Standards | ~280 rules across 20 categories. Error handling, ownership, memory optimisation, API design, async, compiler optimisation, type safety, unsafe, traits, naming, testing, docs, performance, project structure, linting, and anti-patterns.                                                                       |
| **react-best-practises**  | Standards | 78 rules across 11 categories. Hooks, state, components, TypeScript, error handling, security, testing, accessibility, and anti-patterns. Complements Vercel performance skill.                                                                                                                                  |
| **prompt-best-practises** | Meta      | Meta-skill for authoring other skills. XML structuring, examples, role assignment, agentic patterns.                                                                                                                                                                                                             |
| **pr-issue-matcher**      | Workflow  | Given a PR URL, fetches the diff, pulls all open issues from the linked repo, and matches the PR to the best-fitting issue and epic with a scored confidence rating. If no good match exists, proposes a new issue with body template and `gh issue create` command. Works with any GitHub repository.           |

## Installation

There are three things to install: the skills themselves, the hooks that make
them compose automatically, and (optionally) companion skills from third parties.

### Step 1: Clone the repo

```bash
git clone git@github.com:thethirdorigin/skills.git ~/github/thethirdorigin/skills
```

### Step 2: Install skills

Choose one of the options below.

#### Option A: Manual symlinks (recommended)

Symlink each skill into your global Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills

for skill in project-guide audit reviewpr grill-me spec rust-best-practises \
             react-best-practises codegraph prompt-best-practises \
             ascend-frontend find-skills pr-issue-matcher; do
  ln -sf ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/$skill \
         ~/.claude/skills/$skill
done
```

To update: `git -C ~/github/thethirdorigin/skills pull` -- symlinks pick up changes automatically.

To install into a specific project instead of globally, symlink into `.claude/skills/` within the project directory.

#### Option B: Plugin marketplace (if `/plugin` is available)

Run these commands in the Claude Code chat box:

```
/plugin marketplace add thethirdorigin/skills
/plugin install thethirdorigin-skills@thethirdorigin
```

> **Private repo**: Requires SSH keys or `GITHUB_TOKEN` / `GH_TOKEN` env variable with `repo` scope.

#### Option C: Per-project install via `npx skills`

```bash
npx skills add thethirdorigin/skills
```

> **Note**: This installs per-project into `.claude/skills/`. Run in each repo where you need the skills.

### Step 3: Install hooks

Hooks make skills compose automatically. When you type "audit this codebase",
the hook detects the `audit` trigger, resolves its `codegraph` dependency, and
injects instructions telling Claude to load both skills via the Skill tool --
in the right order.

```bash
~/github/thethirdorigin/skills/hooks/install.sh
```

This does three things:

1. Symlinks `skill-activation.py` and `file-tracker.py` to `~/.claude/hooks/`
2. Registers the hooks in `~/.claude/settings.json`
3. Clears the manifest cache so it rebuilds on the next prompt

The installer is idempotent -- safe to run multiple times. It backs up existing
hook files before overwriting.

> **What the hooks do**: See [hooks/README.md](hooks/README.md) for full details.
> In short, they auto-discover every SKILL.md, parse its frontmatter for
> `triggers`, `dependencies`, and `file-patterns`, and inject the right Skill
> tool invocations into Claude's context. No manual config file to maintain.

### Step 4 (optional): Companion skills

Some skills reference external companion skills maintained by third parties.

#### Vercel Agent Skills

The **react-best-practises** skill covers architecture, correctness, and quality but deliberately excludes performance -- that's covered by Vercel's 69-rule performance skill. The **project-guide** also references Vercel's web-design-guidelines and composition-patterns.

Install Vercel skills in any project:

```bash
npx skills add vercel-labs/agent-skills
```

This installs (per-project, into `.claude/skills/`):

- `vercel-react-best-practices` -- React/Next.js performance optimisation (69 rules across 8 priority tiers)
- `vercel-composition-patterns` -- Component composition patterns that scale
- `web-design-guidelines` -- UI compliance auditing (100+ accessibility and UX rules)
- `vercel-react-view-transitions` -- View Transition API guide
- `vercel-react-native-skills` -- React Native/Expo patterns
- `deploy-to-vercel` -- Deployment automation
- `vercel-cli-with-tokens` -- Vercel CLI with token auth

> **Note**: Vercel skills are installed per-project (not global). Run `npx skills add` in each repo where you need them.

## How the skills work together

Skills compose via two mechanisms:

1. **Dependency resolution** -- Skills declare `dependencies` in their YAML
   frontmatter. The `skill-activation.py` hook resolves the full chain and
   tells Claude to load them in order.
2. **Explicit Skill tool invocation** -- Each parent skill has a "Step 0" or
   "Phase 0" that instructs Claude to invoke the Skill tool for its
   dependencies before proceeding.

```
project-guide (orchestrator)
 |  Phase 0: loads codegraph, then language-specific skills as detected
 |
 +-  Phase 1: Context Gathering
 |   +-  discovers project structure, tech stack, git history
 |   +-  ALL projects: indexes codebase via codegraph skill
 +-  Phase 2: Pattern Identification -- finds conventions, shared code
 +-  Phase 3: Analysis -- cross-references language-specific skills:
 |   +-  rust-best-practises -- ~280 Rust rules
 |   +-  react-best-practises -- 78 React/TS rules
 |   |   +-  (companion) vercel-react-best-practices -- for performance
 |   +-  (future) terraform-best-practises, python-best-practises, etc.
 +-  Phase 4: Implementation -- enforces consistency, checklists
 +-  Phase 5: Questions -- asks when requirements are unclear
 +-  Phase 6: Quality Gate -- runs audit skill to verify implementation

audit (code quality orchestrator)
 |  Step 0: loads codegraph + detected language skills via Skill tool
 |
 +-  Detects stack (Rust, React/TS, Python, Go, ...)
 +-  ALL stacks: codegraph (structural analysis, call graph, impact, SQL)
 +-  Rust: rust-best-practises (language-specific rules)
 +-  React/TS: react-best-practises (language-specific rules)
 +-  Cross-correlates findings, deduplicates, ranks by severity
 +-  Produces evidence-based report with file:line references

spec (feature specification)
 |  Loads codegraph via dependency
 |
 +-  Phase 1: Deep Discovery — indexes codebase with codegraph, reads
 |   constitution, existing specs, architecture, domain symbols
 +-  Phase 2: Codebase-Grounded Interview — every question references
 |   real modules, patterns, and domain terms found via codegraph
 +-  Phase 3: Spec Generation — synthesizes answers into SpecKit-format spec
 +-  Phase 4: Handoff — guides user to /speckit.plan, /speckit.tasks, etc.

codegraph (composable building block)
 +-  Invoked by audit, project-guide, spec, or directly by user
 +-  Semantic search, call graph, impact analysis, file structure
 +-  MCP tools (primary) or CLI + raw SQL (fallback)
 +-  Supports 17+ languages: TS, JS, Python, Go, Rust, Java, C#, ...

reviewpr (PR wrapper)
 |  Loads audit via Skill tool (which in turn loads codegraph)
 |
 +-  Gathers PR context via gh CLI (diff, comments, changed files)
 +-  Delegates code analysis to audit skill
 +-  Deduplicates against existing reviewer comments
 +-  Posts approved findings as inline GitHub comments

prompt-best-practises -- used when creating or improving any of the above skills

pr-issue-matcher (standalone)
 +-  Fetches PR diff + file list via gh CLI
 +-  Discovers issue/epic/label conventions from the repo at runtime
 +-  Scores all open issues against the PR signal profile
 +-  HIGH/MEDIUM/LOW confidence match with cited reasoning
 +-  LOW confidence: proposes new issue with body template + gh issue create
```

### Dependency graph

```
reviewpr
  -> audit
       -> codegraph

project-guide
  -> codegraph

spec
  -> codegraph

ascend-frontend
  (file-pattern: frontend/apps/*)

pr-issue-matcher
  (standalone — no dependencies)

react-best-practises
  (file-pattern: .tsx, .jsx, frontend/)

rust-best-practises
  (file-pattern: .rs, Cargo.toml, backend/)
```

## Hooks

The `hooks/` directory contains generic Claude Code hooks that make skill
composition work automatically. See [hooks/README.md](hooks/README.md) for
full documentation.

| Hook                  | Event                    | What it does                                                                                                                    |
| --------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `skill-activation.py` | UserPromptSubmit         | Matches prompt against all skills' `triggers`, resolves `dependencies` transitively, injects Skill tool invocation instructions |
| `file-tracker.py`     | PostToolUse (Edit/Write) | Matches edited file paths against skills' `file-patterns`, suggests relevant skills                                             |

**Key design**: No config file to maintain. The hooks auto-discover all
SKILL.md files, parse their YAML frontmatter, and cache a manifest that
refreshes when any skill file changes. Adding a new skill with the right
frontmatter fields is all that's required.

### Frontmatter fields used by hooks

```yaml
---
name: my-skill
triggers: # phrases that activate this skill
  - audit this codebase
dependencies: # skills to load before this one
  - codegraph
file-patterns: # file edits that suggest this skill
  - .tsx
  - frontend/
---
```

## Skill triggers

Skills activate automatically based on what you're doing:

| Trigger phrase                                            | Skill activated                      |
| --------------------------------------------------------- | ------------------------------------ |
| "I need to add a Rust endpoint"                           | rust-best-practises                  |
| "Create a new React component"                            | react-best-practises                 |
| "Starting work on a new feature"                          | project-guide                        |
| "What should I know about this project?"                  | project-guide                        |
| "Audit this codebase"                                     | audit (+ codegraph dependency)       |
| "Find code smells"                                        | audit (+ codegraph dependency)       |
| "Review this PR"                                          | reviewpr (+ audit + codegraph chain) |
| "Grill me on this design"                                 | grill-me                             |
| "New feature" / "Write a spec" / "Define feature"         | spec (+ codegraph dependency)        |
| "I want to create a new skill"                            | prompt-best-practises                |
| "Use codegraph" / "Query knowledge graph" / "Find symbol" | codegraph                            |
| "Explore codebase" / "What calls this?" / "Trace callers" | codegraph                            |
| "Link this PR to an issue" / "What issue does this PR belong to?" | pr-issue-matcher            |
| "Find the issue for this PR" / "Which epic does this PR belong to?" | pr-issue-matcher          |

## Adding new skills

1. Create a directory under `plugins/thethirdorigin-skills/skills/<skill-name>/`
2. Add a `SKILL.md` with frontmatter:
   - `name` and `description` (required)
   - `triggers` -- prompt phrases that should activate this skill
   - `dependencies` -- other skills that must be loaded first
   - `file-patterns` -- file extensions or directory prefixes that suggest this skill
3. Use the **prompt-best-practises** skill to structure the content
4. If the skill depends on others, add a "Step 0" / "Phase 0" section with
   explicit Skill tool invocation instructions (the hooks handle discovery,
   but the in-skill instructions are the belt to the hook's suspenders)
5. If the skill is language-specific, add a checklist to **project-guide** Phase 4
6. Update **project-guide** Phase 3 and the Extensibility section to cross-reference it
7. If the skill provides coding standards, register it in **audit** Step 1 (stack detection table)
8. Bump the version in `marketplace.json`

The hooks auto-discover new skills from frontmatter -- no config file updates needed.

## Repository structure

```
hooks/
  skill-activation.py                 <- UserPromptSubmit hook (auto-discovery)
  file-tracker.py                     <- PostToolUse hook (file-pattern matching)
  install.sh                          <- portable hook installer
  README.md                           <- hook documentation
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
    spec/
      SKILL.md                        <- codebase-grounded feature specification
      spec-template.md                <- SpecKit-compatible spec output template
    rust-best-practises/
      SKILL.md                        <- ~280 Rust rules across 20 categories
      rules/                          <- individual rule files (287 .md files)
    react-best-practises/
      SKILL.md                        <- 78 React/TS rules across 11 categories
      rules/                          <- individual rule files
    codegraph/SKILL.md                <- codegraph semantic code intelligence (all languages)
    prompt-best-practises/SKILL.md    <- meta-skill for skill authoring
    ascend-frontend/SKILL.md          <- Ascend Platform frontend guide
    find-skills/SKILL.md              <- skill discovery helper
    pr-issue-matcher/SKILL.md         <- PR-to-issue/epic matcher (any GitHub repo)
```

## Sources

These skills were built from authoritative sources:

**Rust**

- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) -- C-\* rules for API design
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) -- 60+ M-\* production rules
- [Rust Performance Book](https://nnethercote.github.io/perf-book/) -- Practical performance optimisation
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) -- Official formatting conventions
- [Apollo Rust Best Practices](https://github.com/apollographql/rust-best-practices) -- Production patterns
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce)
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) -- Concrete rules with code examples (MIT, merged into rust-best-practises)
- [CodeGraph](https://github.com/colbymchenry/codegraph) -- Semantic code intelligence for all languages

**React/TypeScript**

- [React Rules](https://react.dev/reference/rules) -- Official component and hook rules
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/)
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices)

**Spec-Driven Development**

- [GitHub SpecKit](https://github.com/github/spec-kit) -- Spec-driven development toolkit

**Prompt Engineering**

- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
