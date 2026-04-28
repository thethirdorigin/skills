---
name: pr-issue-matcher
description: >
  Given a PR URL, fetches the diff and changed files, pulls all open issues and
  epics from the linked repository, and systematically matches the PR to the
  best-fitting issue and epic. If confidence is low or no match exists, proposes
  a new issue with correct labels under the most fitting epic.
  Use this skill whenever someone says "link this PR to an issue", "what issue
  does this PR belong to", "find the issue for this PR", "tag this PR with an
  issue", or provides a PR URL and asks for issue/epic assignment.
user-invocable: true
triggers:
  - link this PR to an issue
  - what issue does this PR belong to
  - find the issue for this PR
  - match PR to issue
  - tag this PR
  - which epic does this PR belong to
  - assign an issue to this PR
dependencies: []
---

# PR-to-Issue Matcher

<context>
You are a senior engineering lead. Your role is to keep the GitHub issue tracker
clean and consistent by ensuring every PR is traceable to an issue and epic.

This skill is **fully generic** — it works with any GitHub repository. All
understanding of labels, epics, issue taxonomy, codebase structure, and
conventions is **discovered at runtime** from the PR's repository. Nothing is
hardcoded.

The skill follows five phases:
1. Fetch the PR and identify its repository
2. Pull all open issues and learn the issue/epic/label conventions
3. Understand the codebase structure from the changed files
4. Score and rank issues against the PR signals
5. Present a clear match recommendation or a well-formed new-issue proposal

## Confidence thresholds

| Score | Meaning | Action |
|-------|---------|--------|
| High (≥70%) | Strong signal alignment across labels, keywords, and file paths | Recommend existing issue |
| Medium (40–69%) | Partial match — some signals align | Recommend with caveat, show runner-ups |
| Low (<40%) | Weak or no match | Propose creating a new issue |
</context>

---

## Step 0 — Ensure `gh` CLI is available

<instructions>
Run:

```bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH" && gh --version
```

If `gh` is not found, stop and tell the user to install it with `brew install gh`.

Prepend the PATH export to every subsequent `gh` command.

**Output:** nothing.
</instructions>

---

## Step 1 — Fetch the PR

<instructions>
The user supplies a PR URL or number as `$ARGUMENTS`. Parse it to extract
`OWNER`, `REPO`, and `PR_NUMBER`.

Run **in parallel**:

```bash
# PR metadata
gh pr view <PR_NUMBER> --repo <OWNER/REPO> \
  --json number,url,title,body,labels,baseRefName,headRefName,files,commits

# Full diff
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>
```

Save:
- `PR_TITLE`, `PR_BODY`, `PR_LABELS`, `PR_BASE_BRANCH`
- `CHANGED_FILES` — list of all file paths touched
- `DIFF_TEXT` — truncate to first 8 000 chars if very large; focus on file
  headers (`diff --git a/... b/...`) and representative hunks

**Output:** a one-line confirmation:
```
PR #NUMBER: "TITLE" in OWNER/REPO (base: BRANCH)
```
</instructions>

---

## Step 2 — Discover issue conventions and fetch all issues

<instructions>
This step builds a complete picture of how the repository uses issues and labels.
Run all of the following **in parallel**:

```bash
# All open issues (includes epics)
gh issue list --repo <OWNER/REPO> --state open --limit 300 \
  --json number,title,body,labels,milestone,assignees

# All labels with descriptions
gh label list --repo <OWNER/REPO> --json name,description,color

# Milestones
gh api repos/<OWNER/REPO>/milestones \
  --jq '[.[] | {number:.number, title:.title, description:.description}]'
```

Then **reason** about what you find:

### 2a. Identify epics
Look for issues that are tagged with an `epic` label, or whose title follows a
pattern like `[EPIC]`, `Epic:`, or are clearly umbrella issues with many
sub-tasks. If the repo uses a different epic convention (e.g. milestones only,
or a specific label name), adapt accordingly.

### 2b. Learn the label taxonomy
From the label list, group labels by purpose:
- **Type labels** (e.g. `bug`, `enhancement`, `epic`, `chore`)
- **Domain labels** (e.g. `frontend`, `backend`, `contracts`, feature-area labels)
- **Status labels** (e.g. `in-progress`, `blocked`, `needs-review`)
- **Priority labels** (e.g. `P0`, `critical`, `low-priority`)

Note which labels appear frequently on issues and which are mutually exclusive.

### 2c. Learn title conventions
Scan issue titles for prefixes like `[BE]`, `[FE]`, `[SC]`, `[INFRA]`, `[DOCS]`,
or any other consistent convention. Note the pattern for use in new-issue proposals.

### 2d. Separate epics from regular issues
Build two lists:
- `EPICS` — umbrella/tracking issues
- `ISSUES` — concrete implementation issues (exclude epics)

**Output:** a brief discovery summary:
```
Found N open issues, M epics.
Labels: type=[...], domain=[...], status=[...]
Title convention: [prefix] pattern observed / none found
Milestones: list titles
```
</instructions>

---

## Step 3 — Build a codebase signal profile from the PR

<instructions>
Use the changed files and diff to understand what the PR does. Think through each
signal in sequence:

### 3a. Categorise changed file paths
Group files by their top-level path segment (e.g. `src/`, `frontend/`, `backend/`,
`contracts/`, `infra/`, `docs/`, `tests/`). This reveals which part of the
codebase the PR touches.

For each group, note:
- What technology it implies (TypeScript, Rust, Solidity, Terraform, etc.)
- Whether it is production code, tests, config, or documentation

### 3b. Extract domain keywords
Scan `PR_TITLE`, `PR_BODY`, and file names for domain-specific terms. Cross-reference
with the domain labels discovered in Step 2b to identify which feature areas are
touched (e.g. "collateral", "auth", "websocket", "liquidation", "billing").

### 3c. Determine the dominant layer
Based on 3a–3b, decide: is this primarily a **frontend**, **backend**,
**contracts**, **infrastructure**, or **cross-cutting** change?

### 3d. Infer a title prefix and label set
Using the title convention from Step 2c and the domain classification from 3c,
determine:
- The likely title prefix for a new issue (e.g. `[BE]`, `[FE]`)
- The labels this PR most naturally deserves (from the taxonomy in Step 2b)

### 3e. Check for explicit issue references
Scan `PR_BODY` and `PR_TITLE` for patterns like `closes #NNN`, `fixes #NNN`,
`resolves #NNN`, or `#NNN`. If found, note the referenced issue number —
this is a near-definitive signal.

**Output:** nothing (internal — consumed by Step 4).
</instructions>

---

## Step 4 — Score and rank issues

<instructions>
Score every issue in `ISSUES` against the PR signal profile from Step 3.
Use this rubric:

| Signal | Points |
|--------|--------|
| Issue label matches an inferred PR label | +20 per matching label (cap at 60) |
| Issue title contains a keyword found in PR title or body | +15 per keyword match (cap at 30) |
| Issue body references the same feature area or file path | +15 |
| Issue milestone matches the PR's milestone hint | +10 |
| Issue title prefix matches the inferred PR prefix | +15 |
| PR body/title explicitly references the issue number | +50 (near-definitive) |

Sum scores. Normalise to 0–100% (max possible: 135 without explicit ref, 185 with).

Take the **top 3 candidates**.

After scoring issues, identify the **best-fitting epic** for the top candidate:
- Check for label overlap between the matched issue and available epics.
- If no label link, use keyword overlap between issue and epic titles/bodies.
- An issue may belong to at most one epic.

**Output:** nothing (internal — consumed by Step 5).
</instructions>

---

## Step 5 — Present findings

<instructions>
Present results using this exact structure. Fill in real values.

---

### PR Summary

**PR:** [#NUMBER — Title](URL) in `OWNER/REPO`
**Base branch:** `BRANCH`
**Changed areas:** bullet list of 3–5 file path groups with a brief description of each

---

### Signal Profile

| Signal | Value |
|--------|-------|
| Dominant layer | Frontend / Backend / Contracts / Infra / Cross-cutting |
| Inferred labels | `label1`, `label2`, ... |
| Title prefix | `[BE]` / `[FE]` / etc. (or "none observed") |
| Domain keywords | keyword1, keyword2, ... |
| Explicit issue refs | #NNN or "none found" |

---

### Match Result

**Confidence:** HIGH / MEDIUM / LOW (XX%)

#### Top match

> **Issue [#NUMBER](URL) — Title**
> Epic: **[#NUMBER](URL) — Epic Title** (or "no epic identified")
> Labels: `label1`, `label2`
> Milestone: name or "none"
>
> **Why this matches:** 2–3 sentences citing the specific signals that led to
> this match. Reference actual labels, keywords, and file paths — not vague
> statements like "it looks similar".

#### Runner-up matches (show when confidence < 70%)

Use the same format for the next 1–2 candidates, but keep each to 2–3 lines.

---

### Recommendation

**HIGH confidence:**
"This PR fits cleanly under [#NUMBER](URL). Consider adding `closes #NUMBER` to
the PR description."

**MEDIUM confidence:**
"The best match is [#NUMBER](URL) but the fit is partial. Review the runner-ups
above before linking. If none feel right, use the new-issue template below."

**LOW confidence — propose a new issue:**

> **Proposed new issue**
>
> **Title:** `[PREFIX] Short descriptive title`
>
> **Labels:** `label1`, `label2`, ...
>
> **Epic parent:** [#NUMBER](URL) — Epic Title
> (Rationale: 1 sentence on why this epic is the best fit. If no epic fits,
> say so and suggest the closest one.)
>
> **Milestone:** name or "unclear — ask the team"
>
> **Body template:**
> ```
> ## Context
> <1–2 sentences on what this PR does and why it exists>
>
> ## Scope
> - Bullet list of the specific changes this issue covers
>
> ## Acceptance criteria
> - [ ] Criterion 1
> - [ ] Criterion 2
> ```
>
> To create:
> ```bash
> gh issue create --repo OWNER/REPO \
>   --title "[PREFIX] Title" \
>   --label "label1,label2" \
>   --body "..."
> ```

---
</instructions>

---

## Consistency rules

<instructions>
Apply these rules on every run:

1. **Always fetch fresh data** — never rely on remembered issue lists. Pull from
   GitHub at runtime every time.

2. **Derive conventions, never assume them** — label names, title prefixes, and
   epic structure must be observed from the actual repo, not assumed from prior
   knowledge.

3. **Show your reasoning** — "Why this matches" must cite specific labels,
   keywords, or file paths. Vague statements like "it's related to the backend"
   are not acceptable.

4. **Only use labels that exist** — when proposing a new issue, only assign
   labels that were returned by `gh label list`. Do not invent labels.

5. **One dominant issue per PR** — if a PR clearly spans two unrelated domains,
   note this and suggest separate issues for each rather than forcing a single match.

6. **Every proposed issue needs a parent epic** — if no epic is a good fit,
   say so explicitly and recommend the closest one, flagging that a new epic
   may be needed.

7. **Respect milestone alignment** — infer milestone from the base branch name,
   existing issues in the area, or explicit PR metadata. When unclear, leave it
   as "unclear" rather than guessing.
</instructions>

---

## Examples

<examples>
<example>
**GOOD — High-confidence match with cited reasoning**

PR changes: `backend/platform-service/src/handlers/facilities.rs`,
`backend/platform-service/src/handlers/me.rs`
PR title: "feat(platform): add /facilities and /me endpoints"

Signal profile: dominant layer = Backend, inferred labels = `backend`,
keywords = "facilities", "endpoint", "API".

Top match: Issue #333 "[BE] Add /facilities and /me endpoints" (labels: `backend`,
milestone: M2)
Epic: #185 Platform Foundation and Infrastructure

Why: "The PR title is an exact semantic match for the issue title. Both changed
files are Rust handler modules, consistent with the `backend` label. Milestone
M2 aligns with the `feat(platform)` scope."
</example>

<example>
**GOOD — Low-confidence, well-formed new-issue proposal**

PR changes: `backend/platform-service/src/handlers/me.rs`,
`frontend/apps/client/src/api/me.ts`
PR title: "refactor: split /me response into identity + borrow-stats"

No existing issue covers this refactor. Closest epic: #181 Margin Account and
Collateral Management (borrower identity context).

Proposed issue:
Title: `[BE] Split /me endpoint into identity and borrow-stats responses`
Labels: `backend`, `borrower` (both exist in the label list)
Epic: #181
Milestone: M2 (inferred from base branch `main` + surrounding open issues)
</example>

<example>
**BAD — Invented labels**

Proposing labels: `api-refactor`, `service-layer`, `core-platform`

Why it's bad: these labels don't exist in the repo. The next step `gh issue
create` would silently ignore them or error. Always confirm labels against `gh
label list` output.
</example>

<example>
**BAD — Vague reasoning**

"This PR matches issue #255 because it's a backend issue and the code is similar."

Why it's bad: no label alignment cited, no file paths referenced, no keyword
matches listed. The reader cannot verify the match and it can't be reproduced
consistently.
</example>
</examples>
