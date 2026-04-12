# thethirdorigin skills

Private skills marketplace for Claude Code. Best practices, code quality, and systematic project analysis.

## Skills

| Skill | Lines | What it covers |
|-------|-------|----------------|
| **project-guide** | 300 | 5-phase workflow for analysing any codebase and building features systematically. Orchestrates all other skills. |
| **react-best-practises** | 348 | Architecture, hooks, state, TypeScript, error handling, security, accessibility. Complements Vercel performance skill. |
| **rust-best-practises** | 445 | API design (C-\*/M-\* rules), error handling, ownership, async, traits, testing, documentation, linting, crate design. |
| **rust-skills** | 179 rules | 179 concrete Rust rules with bad→good code examples. Memory optimisation, compiler tuning, async, testing, anti-patterns. Forked from [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) (MIT). |
| **prompt-best-practises** | 264 | Meta-skill for authoring other skills. XML structuring, examples, role assignment, agentic patterns. |
| **reviewpr** | 325 | Deep code review for GitHub PRs. Posts findings as line-specific comments. |
| **grill-me** | 77 | Stress-test a plan or design through relentless questioning. |

## Installation

### Option A: Manual install (recommended)

Clone the repo and symlink the skills into your global Claude Code skills directory:

```bash
# Clone (if not already cloned)
git clone git@github.com:thethirdorigin/skills.git ~/github/thethirdorigin/skills

# Symlink each skill to global skills directory
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/project-guide ~/.claude/skills/project-guide
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/prompt-best-practises ~/.claude/skills/prompt-best-practises
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/react-best-practises ~/.claude/skills/react-best-practises
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/rust-best-practises ~/.claude/skills/rust-best-practises
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/rust-skills ~/.claude/skills/rust-skills
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/reviewpr ~/.claude/skills/reviewpr
ln -s ~/github/thethirdorigin/skills/plugins/thethirdorigin-skills/skills/grill-me ~/.claude/skills/grill-me
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
├── Phase 1: Context Gathering ─── discovers project structure, tech stack, git history
├── Phase 2: Pattern Identification ─── finds conventions, shared code, anti-patterns
├── Phase 3: Analysis ─── cross-references language-specific skills:
│   ├── rust-best-practises ─── for Rust code (guidelines + principles)
│   │   └── rust-skills ─── 179 concrete rules with code examples
│   ├── react-best-practises ─── for React/TypeScript code
│   │   └── (companion) vercel-react-best-practices ─── for performance
│   └── (future) terraform-best-practises, solidity-best-practises, etc.
├── Phase 4: Implementation ─── enforces consistency, checklists, documentation
└── Phase 5: Questions ─── asks when requirements are unclear (with recommendations)

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
| "I want to create a new skill" | prompt-best-practises |
| "Review this PR" | reviewpr |
| "Grill me on this design" | grill-me |

## Adding new skills

1. Create a directory under `plugins/thethirdorigin-skills/skills/<skill-name>/`
2. Add a `SKILL.md` with frontmatter (`name`, `description`, `triggers`)
3. Use the **prompt-best-practises** skill to structure the content
4. If the skill is language-specific, add a checklist to **project-guide** Phase 4
5. Update **project-guide** Phase 3 and the Extensibility section to cross-reference it
6. Bump the version in `marketplace.json`

## Repository structure

```
.claude-plugin/
  marketplace.json                    ← marketplace manifest
plugins/thethirdorigin-skills/
  .claude-plugin/
    plugin.json                       ← plugin manifest
  skills/
    project-guide/SKILL.md            ← orchestrator (15KB)
    prompt-best-practises/SKILL.md    ← meta-skill for skill authoring (10KB)
    react-best-practises/SKILL.md     ← React/TypeScript quality (15KB)
    rust-best-practises/SKILL.md      ← Rust quality (21KB)
    rust-skills/SKILL.md + rules/     ← 179 concrete Rust rules (forked, MIT)
    reviewpr/SKILL.md                 ← PR review (14KB)
    grill-me/SKILL.md                 ← design interviews (3KB)
```

## Sources

These skills were built from authoritative sources:

**Rust**
- [Rust API Guidelines Checklist](https://rust-lang.github.io/api-guidelines/checklist.html) — C-\* rules for API design
- [Microsoft Rust Guidelines](https://microsoft.github.io/rust-guidelines/guidelines/index.html) — 60+ M-\* production rules
- [Rust Style Guide](https://doc.rust-lang.org/style-guide/) — Official formatting conventions
- [Apollo Rust Best Practices](https://github.com/apollographql/rust-best-practices) — Production patterns
- [Rust Clean Code](https://dev.to/mbayoun95/rust-clean-code-crafting-elegant-efficient-and-maintainable-software-27ce)
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills) — 179 concrete rules with code examples (MIT, forked into this repo)

**React/TypeScript**
- [React Rules](https://react.dev/reference/rules) — Official component and hook rules
- [freeCodeCamp React Best Practices](https://www.freecodecamp.org/news/best-practices-for-react/)
- [Vercel React Best Practices](https://vercel.com/blog/introducing-react-best-practices)

**Prompt Engineering**
- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
