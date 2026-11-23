# 04 - Agent Skills architecture, packaging and cross-agent loading

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Research date: 2026-11-23. Workstream 4 of 6.

**Tags**: `[V]` fetched and read in this session. `[T]` verified by running the tool in this session's sandbox
(skills-ref 0.1.1, `skills` CLI 1.9.0, Claude Code 2.1.330). `[W]` taken from a WebSearch summary of the official page
(the page itself could not be fetched: host blocked) - treat as unverified-secondary. `[M]` memory / inference.
**Strength**: `MUST` = spec or tool hard-fails; `SHOULD` = documented recommendation; `CONV` = community convention.

Blocked hosts (need allow-listing to upgrade `[W]` to `[V]`): agentskills.io (source read from GitHub instead),
developers.openai.com, cursor.com, docs.github.com (source read from github/docs instead), opencode.ai,
code.visualstudio.com, geminicli.com (source read from GitHub instead), ampcode.com, cli.github.com.

## 0. Decisions for the lead (TL;DR)

1. **Layout: `skills/apple-hig/SKILL.md`, not SKILL.md at repo root.** A root SKILL.md makes the cloned directory
   (`apple-hig-skill`) the skill directory, which violates "name must match the parent directory" and fails
   `skills-ref validate` `[T]`. `skills/<name>/` is also the default plugin layout for Claude Code `[V]`, the first
   container the `skills` CLI scans `[V]`, and the layout `openai/plugins` uses `[V]`.
2. **Frontmatter: only the six spec fields** (`name`, `description`, `license`, `compatibility`, `metadata`,
   `allowed-tools`). Any Claude Code extension field (`user-invocable`, `paths`, `when_to_use`, ...) makes
   `skills-ref validate` fail `[T]` and makes claude.ai upload / Skills API / `package_skill.py` hard-error `[V]`.
3. **Description: one field, <= 1024 chars, key use case first**, third-person capability sentence + "Use when ..."
   triggers + near-miss exclusion. Draft in section 7 is 953 chars and passes validation `[T]`.
4. **Ship a Claude Code plugin + marketplace from the same repo** (`.claude-plugin/plugin.json` +
   `.claude-plugin/marketplace.json`, plugin `source: "./"`). Both validate with `claude plugin validate` `[T]`.
5. **Keep evals and repo tooling outside the skill directory** so installers do not copy them into users' agents.
6. **Budgets**: SKILL.md body < 500 lines and < 5000 tokens; most important rules in the first ~5000 tokens;
   every reference file linked directly from SKILL.md; reference files > 100 lines get a table of contents.

## 1. Sources

| ID | Source | Status |
|----|--------|--------|
| S1 | Spec: https://agentskills.io/specification (read as https://raw.githubusercontent.com/agentskills/agentskills/main/docs/specification.mdx) | [V] |
| S2 | Client implementation guide: .../agentskills/main/docs/client-implementation/adding-skills-support.mdx | [V] |
| S3 | Optimizing descriptions: .../agentskills/main/docs/skill-creation/optimizing-descriptions.mdx | [V] |
| S4 | Evaluating skills: .../agentskills/main/docs/skill-creation/evaluating-skills.mdx | [V] |
| S5 | Using scripts: .../agentskills/main/docs/skill-creation/using-scripts.mdx | [V] |
| S6 | skills-ref: .../agentskills/main/skills-ref/README.md, src/skills_ref/validator.py, parser.py, pyproject.toml | [V] |
| S7 | Claude Code skills: https://code.claude.com/docs/en/skills.md | [V] |
| S8 | Claude Code plugin manifest: https://code.claude.com/docs/en/plugins/manifest-reference.md | [V] |
| S9 | Claude Code marketplace: https://code.claude.com/docs/en/plugins/marketplace-reference.md | [V] |
| S10 | Claude Code plugin components / install / create: .../plugins/components.md, install.md, create.md | [V] |
| S11 | Anthropic authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md | [V] |
| S12 | Anthropic skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md | [V] |
| S13 | anthropics/skills: README.md, .claude-plugin/marketplace.json, skills/skill-creator/SKILL.md, references/schemas.md, scripts/quick_validate.py (raw.githubusercontent.com/anthropics/skills/main/...) | [V] |
| S14 | `skills` CLI (vercel-labs/skills): README.md, docs/creating-skills.md, docs/agents.md, docs/commands.md | [V] |
| S15 | Codex source: raw.githubusercontent.com/openai/codex/main/codex-rs/skills/src/parser.rs and assets/samples/skill-installer/SKILL.md; docs/skills.md is only a pointer | [V] |
| S16 | openai/skills README (repo **deprecated**), openai/plugins README + plugins/build-ios-apps/.codex-plugin/plugin.json | [V] |
| S17 | Copilot: raw.githubusercontent.com/github/docs/main/data/reusables/copilot/creating-adding-skills.md and content/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills.md | [V] |
| S18 | Gemini CLI: raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md | [V] |
| S19 | Goose: raw.githubusercontent.com/block/goose/main/documentation/docs/guides/context-engineering/using-skills.md | [V] |
| S20 | Codex docs https://developers.openai.com/codex/skills | [W] |
| S21 | Cursor docs https://cursor.com/docs/skills | [W] |
| S22 | opencode docs https://opencode.ai/docs/skills | [W] |
| S23 | VS Code docs https://code.visualstudio.com/docs/copilot/customization/agent-skills | [W] |

## 2. SKILL.md frontmatter

### 2.1 Spec fields (S1, enforced by S6)

| Field | Req | Constraint | Strength |
|-------|-----|-----------|----------|
| `name` | yes | 1-64 chars; lowercase alphanumerics and `-`; no leading/trailing `-`; no `--`; **must match parent directory name** | MUST [V][T] |
| `description` | yes | 1-1024 chars, non-empty; what it does + when to use; include task keywords | MUST [V] |
| `license` | no | Short: license name or bundled file name | SHOULD [V] |
| `compatibility` | no | 1-500 chars; only if there are real environment requirements ("Most skills do not need" it) | MUST (len) [V] |
| `metadata` | no | Map of string keys to **string** values (quote versions: `"1.0"`); use reasonably unique keys | MUST [V] |
| `allowed-tools` | no | Space-separated string, e.g. `Bash(git:*) Read`. Experimental; support varies | [V] |

Validator behaviour that goes beyond the prose spec:
- skills-ref rejects **any other top-level key** ("Unexpected fields in frontmatter") `[V][T]`.
- skills-ref parses with `strictyaml` (no flow style, no duplicate keys, stricter than PyYAML) `[V]`.
- skills-ref accepts Unicode lowercase letters in `name` (`isalnum`), wider than the spec's `a-z0-9` `[V]`. Use ASCII.
- Anthropic surfaces (claude.ai, API) additionally forbid XML tags in `name`/`description` and the reserved words
  `anthropic` / `claude` in `name` (S11, S12 `[V]`); `quick_validate.py` rejects `<` or `>` in the description (S13 `[V]`).
- Clients are told to be lenient: name/dir mismatch or over-long name -> warn and load; missing description or
  unparseable YAML -> skip the skill (S2 `[V]`). Unquoted `key: value: more` colons are the most common breakage (S2).

### 2.2 Claude Code extensions (S7 `[V]`) - do not use in the portable skill

All fields are optional in Claude Code (`name` defaults to the directory name). Unknown fields are silently ignored.
Extensions: `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`,
`disallowed-tools`, `model`, `effort`, `context` (`fork`), `agent`, `background`, `hooks`, `paths`, `shell`.

| Fact | Detail |
|------|--------|
| Listing cap | `description` + `when_to_use` combined are truncated at **1,536 chars** per skill in the listing (configurable: `skillListingMaxDescChars`). "Put the key use case first." |
| Listing budget | Whole listing budget = **1% of the model context window** (`skillListingBudgetFraction`, or env `SLASH_COMMAND_TOOL_CHAR_BUDGET`). On overflow all names stay but descriptions are dropped starting with the least-invoked skills. |
| `allowed-tools` semantics | Pre-approves tools for the invoking turn only; it does **not** restrict tools. Accepts space/comma string or YAML list. |
| Angle brackets | `<`/`>` in descriptions render as `&lt;`/`&gt;`. Use square brackets. |
| Malformed YAML | Skill loads with empty metadata: `/name` works but auto-activation cannot match. |
| Outside Claude Code | claude.ai upload, Skills API and `package_skill.py` accept only the six spec fields and hard-error otherwise. |
| Lifecycle | Skill body enters context once and stays; not re-read on later turns. After auto-compaction only the **first 5,000 tokens** of each invoked skill are re-attached (25,000 tokens shared across skills) -> critical rules go at the top. |
| Body-only features | `$ARGUMENTS`, `${CLAUDE_SKILL_DIR}`, and `` !`cmd` `` injection are Claude Code only; other agents see the literal text. |

### 2.3 Other agents' frontmatter handling

| Agent | Reads | Notes |
|-------|-------|-------|
| Codex | `name` (<= 64, falls back to dir name), `description` (required), `metadata.short-description` | From parser source S15 `[V]`. Whitespace is collapsed to one line; a line-oriented repair handles unquoted colons. No description length check in the parser on `main`. |
| Copilot | `name`, `description`, `license`, `allowed-tools` (e.g. `shell`) | S17 `[V]`. Docs warn against pre-approving `shell`/`bash`. |
| Gemini CLI | `name`, `description` | S18 `[V]`. Activation asks the user for consent, then adds the skill directory to allowed paths. |
| Cursor | spec fields + `disable-model-invocation` | S21 `[W]`. Forum reports of the flag being ignored under `.agents/skills/` `[W]`. |
| opencode | `name` (regex `^[a-z0-9]+(-[a-z0-9]+)*$`, must match dir), `description` 1-1024 | S22 `[W]`. |
| `skills` CLI | `name`, `description`, `metadata.internal` (hides the skill from discovery) | S14 `[V]`. |
| `gh skill` | writes provenance (source repo, ref, tree SHA) into the installed SKILL.md frontmatter | S17 `[V]`. Exact keys not verified. |

## 3. Directory conventions and progressive disclosure

- Skill = directory with `SKILL.md`; optional `scripts/` (executable code), `references/` (docs read on demand),
  `assets/` (templates, images, data); "any additional files or directories" are allowed (S1 `[V]`).
- File name: `SKILL.md` exactly (S2, S17); skills-ref also accepts `skill.md` (S6 `[V]`). Use uppercase.
- **Tiers** (S1, S2, S12 `[V]`):

| Tier | Loaded | Budget |
|------|--------|--------|
| 1 Metadata | `name` + `description`, at startup, for every installed skill | ~100 tokens (S1); ~50-100 per skill (S2) |
| 2 Instructions | Whole SKILL.md body, on activation | < 5000 tokens recommended; **< 500 lines** (S1, S7, S11) |
| 3 Resources | Individual files, when the body points to them | Unbounded; scripts cost only their output |

- **One level deep** (S1, S11 `[V]`): the rule is about link chains, not folder depth. Every reference file SHOULD be
  linked directly from SKILL.md, because agents may only partially read a file reached through another file.
  Subfolders are not forbidden by the spec; S11's own example uses a `reference/` folder with domain files.
- Reference files > 100 lines SHOULD start with a table of contents (S11 `[V]`).
- Keep reference files focused; smaller files = less context (S1 `[V]`).
- No time-sensitive statements in the body; put superseded guidance in an "old patterns" section (S11 `[V]`).
  Relevant to us: HIG/OS-version facts need "as of" dates in references, not in SKILL.md prose.
- Paths: relative to the skill root, forward slashes only (S1, S5, S11 `[V]`). Script paths inside reference files are
  also relative to the skill root (S5 `[V]`). Clients are instructed to resolve against the SKILL.md parent directory
  and use absolute paths in tool calls (S2 `[V]`).
- Scripts (S1, S5 `[V]`): self-contained or dependencies documented; no interactive prompts (hard requirement:
  agents run non-interactive shells); `--help`; data on stdout, diagnostics on stderr; meaningful exit codes; bounded
  output (harnesses truncate at roughly 10-30K chars); PEP 723 inline metadata + `uv run` for Python dependencies; pin
  versions for `uvx`/`npx` one-offs. Recommendation `[M]`: Python 3 standard library only, so no install step exists.
- How scripts run: the agent executes them with its shell tool; only output enters context (S12 `[V]`). Whether a
  prompt appears depends on the client (Claude Code `allowed-tools`, Copilot `allowed-tools: shell`, Gemini consent).

## 4. Discovery, activation and loading per agent

Common model (S2 `[V]`): scan project + user scopes -> parse frontmatter -> put name/description catalog in the
system prompt or in an activation tool's description -> the **model** decides (no harness keyword matching) ->
load the body by file read or a dedicated tool -> load resources on demand. Project overrides user on name collision
(universal convention per S2; Claude Code is the exception: enterprise > personal > project, S7 `[V]`).

| Agent | Project paths | User paths | Activation / invocation | Tag |
|-------|---------------|-----------|-------------------------|-----|
| Claude Code | `.claude/skills/<n>/` (plus parents to repo root; nested dirs load lazily) | `~/.claude/skills/<n>/` | `Skill` tool; `/name`; plugins as `/plugin:name` | [V] S7 |
| Claude Code plugin | `<plugin>/skills/<n>/SKILL.md` (default) or root SKILL.md | plugin cache | `/apple-hig:apple-hig` | [V] S7, S8 |
| claude.ai / Cowork / cloud | account skills (zip upload); repo `.claude/skills/` in cloud sessions; **not** `~/.claude/skills` | - | automatic | [V] S7 |
| Codex | `.agents/skills` from CWD up to repo root | `$HOME/.agents/skills`; admin `/etc/codex/skills`; bundled system skills | `$skill` mention, `/skills`, implicit | [W] S20 |
| Codex (installer) | - | `$CODEX_HOME/skills/<n>` (default `~/.codex/skills`) is where the bundled `skill-installer` writes | - | [V] S15 |
| Cursor | `.agents/skills/`, `.cursor/skills/`; compat `.claude/skills/`, `.codex/skills/` | `~/.agents/skills/`, `~/.cursor/skills/`; compat `~/.claude/skills/`, `~/.codex/skills/` | automatic; `/skill-name` | [W] S21 |
| GitHub Copilot (cloud agent, code review, CLI, app, VS Code agent mode) | `.github/skills`, `.claude/skills`, `.agents/skills` | `~/.copilot/skills`, `~/.agents/skills` | automatic; `/skill-name` in prompt; CLI `/skills list|info|add|reload` | [V] S17 |
| VS Code | `.agents/skills/` "by default" (agentskills quickstart [V]); also `.github/skills`, `.claude/skills` | `~/.copilot/skills`, `~/.claude/skills`, `~/.agents/skills` | automatic; `/skills` | [W] S23 |
| Gemini CLI | `.gemini/skills/`, `.agents/skills/` (alias wins within a tier) | `~/.gemini/skills/`, `~/.agents/skills/` | `activate_skill` tool + user consent; `/skills` | [V] S18 |
| opencode | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.claude/skills/`, `~/.agents/skills/` | `skill` tool | [W] S22 |
| Goose | `.agents/skills/`; compat `.goose/skills/`, `.claude/skills/` | `~/.agents/skills/`; compat `~/.claude/skills/` | automatic | [V] S19 |
| Amp | `.agents/skills/` | `~/.config/agents/skills/` | - | [V] S14 table only |

`.agents/skills/` is the de-facto cross-client location; the spec itself does not mandate any location (S2 `[V]`).
Claude Code's own docs do **not** list `.agents/skills` (S7 `[V]`), so Claude Code needs `.claude/skills` or a plugin.
The `skills` CLI bridges this: it writes a canonical copy to `.agents/skills/<name>` and symlinks
`.claude/skills/<name>` to it `[T]`.

## 5. Layout decision: root SKILL.md vs `skills/apple-hig/`

| Criterion | (a) SKILL.md at repo root | (b) `skills/apple-hig/SKILL.md` |
|-----------|---------------------------|----------------------------------|
| Spec "name == parent dir" on a clone | **Fails**: `Directory name 'apple-hig-skill' must match skill name 'apple-hig'` [T] | Passes [T] |
| `npx skills add owner/repo` | Works (root is scanned first and shadows nested) [V] | Works (`skills/` is a standard container) [V][T] |
| Claude Code plugin | Works only with no `skills/` dir and no `skills` key; needs `name` or the skill is named after the cache dir [V] | Default layout, no manifest keys needed [V][T] |
| What gets installed | Whole repo (README, docs/research, CI, evals) becomes the skill directory | Only the skill directory |
| Codex `skill-installer`, Gemini `--path`, manual copy | Directory basename is wrong after clone | `--path skills/apple-hig` gives the right basename [V] |
| Room for a second skill later | No | Yes |

Decision: **(b)**. The only cost is one more path segment in manual-install commands.

## 6. Recommended repository layout

```
apple-hig-skill/
├── .claude-plugin/
│   ├── plugin.json            # Claude Code plugin manifest (plugin root = repo root)
│   └── marketplace.json       # single-plugin marketplace, source "./"
├── skills/
│   └── apple-hig/             # THE skill; only this directory is installed
│       ├── SKILL.md           # < 500 lines, < 5000 tokens; routing table to references
│       ├── references/        # one topic per file, each linked directly from SKILL.md
│       │   ├── foundations-layout.md
│       │   ├── foundations-typography.md
│       │   ├── ...            # ToC at top of every file > 100 lines
│       │   └── platforms-visionos.md
│       ├── scripts/           # optional; only scripts the agent runs for the user (stdlib Python, --help)
│       └── assets/            # optional; checklists/templates the agent copies into output
├── tests/
│   └── evals/
│       ├── evals.json                 # output-quality cases (schema in section 9)
│       ├── trigger-queries.train.json
│       └── trigger-queries.validation.json
├── tools/
│   └── validate_skill.py      # repo validator implementing section 10 (not shipped)
├── docs/research/             # this research (not shipped)
├── .github/workflows/validate.yml
├── README.md                  # install matrix (section 8) + compatibility statement (section 11)
└── LICENSE
```

Justification:
- `skills/apple-hig/` satisfies the spec name rule and every installer in section 8.
- Flat `references/` with prefixed file names keeps every file one link from SKILL.md and avoids relying on agents
  following an index-of-indexes. If the count grows past ~30 files, one sub-level (`references/components/`) is
  allowed by the spec, but each file must still be linked from SKILL.md.
- Evals live outside the skill: installers copy the entire skill directory (the `skills` CLI skips only
  `metadata.json`, `.git`, `__pycache__`, `__pypackages__` `[V]`), Copilot exposes every file in the skill directory
  on activation `[V]`, and Gemini injects the folder structure `[V]`. skill-creator expects
  `<skill>/evals/evals.json` (S4, S13 `[V]`); copy or symlink during an iteration session and do not commit it there.
- `tests/evals/` rather than root `evals/`: a plugin-root `evals/` is the default directory for `claude plugin eval`,
  whose format is different and "not interchangeable" with skill-creator's (S7 `[V]`; that format was not researched).
- Plugin root = repo root means Claude Code caches the whole repo for plugin users. Acceptable (docs are small); the
  alternative `plugins/apple-hig/skills/apple-hig/` adds depth for no functional gain.
- No `CLAUDE.md` at the plugin root: it is not loaded and `claude plugin validate` warns (S8 `[V]`).
- Optional later: `.codex-plugin/plugin.json` with `"skills": "./skills/"` for Codex plugins. Only an example was
  seen (S16 `[V]`); the schema is not verified. Prior art to review: `openai/plugins` ships `build-ios-apps` and
  `build-macos-apps` plugins (SwiftUI, Liquid Glass, AppKit workflows) `[V]`.

### 6.1 `.claude-plugin/plugin.json` (validated `[T]`)

```json
{
  "name": "apple-hig",
  "displayName": "Apple HIG",
  "version": "0.1.0",
  "description": "Agent Skill for designing, implementing, reviewing and adapting native Apple-platform UIs per Apple's Human Interface Guidelines.",
  "author": { "name": "<author>" },
  "repository": "https://github.com/<owner>/apple-hig-skill",
  "license": "MIT",
  "keywords": ["apple", "hig", "swiftui", "uikit", "appkit", "ios", "macos", "accessibility", "design"]
}
```

Schema facts (S8 `[V]`): `name` is the only required key (kebab-case; no spaces, `@`, `:`; must not start with
`claude-`/`anthropic-`); `author.name` required if `author` is present; `homepage` must parse as a URL; unknown
top-level keys are stripped with a warning; component paths must start with `./`; `skills` **adds to** the default
`skills/` scan. Setting `version` pins users to it until it changes, so bump it on every release (or omit it).
`claude plugin validate` emits a non-fatal "no icon" directory warning unless `.claude-plugin/icon.png` exists `[T]`.

### 6.2 `.claude-plugin/marketplace.json` (validated `[T]`)

```json
{
  "name": "apple-hig-skill",
  "owner": { "name": "<author>" },
  "description": "Marketplace for the apple-hig Agent Skill.",
  "plugins": [
    {
      "name": "apple-hig",
      "source": "./",
      "description": "Design, implement, review and adapt native Apple-platform UIs per Apple's Human Interface Guidelines.",
      "category": "design",
      "tags": ["apple", "hig", "swiftui", "uikit", "appkit"]
    }
  ]
}
```

Schema facts (S9 `[V]`): required top-level `name`, `owner` (`owner.name` required), `plugins`; each entry requires
`name` + `source`. Marketplace `name`: letters, digits, `.`, `_`, `-`; many names are reserved (anything imitating
official Anthropic/Claude marketplaces, `agent-skills`, names starting `claudeai-`). Relative sources resolve from the
marketplace root and need `./`; they work for `github`/`git`/local marketplace sources but **not** for a marketplace
added by direct URL to the JSON file. Do not set `version` in both files (plugin.json wins, validator warns). With a
`plugin.json` present and default `strict: true`, entry component fields append to the manifest; anthropics/skills
instead uses no plugin.json, `"strict": false` and an explicit `"skills": [...]` list per entry (S13 `[V]`).

## 7. Frontmatter draft for `apple-hig`

```yaml
---
name: apple-hig
description: Designs, implements, reviews, and adapts native Apple-platform user interfaces according to Apple's Human Interface Guidelines (HIG) for iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. Use when building or changing SwiftUI, UIKit, or AppKit screens and components; choosing navigation, tab bars, sidebars, toolbars, sheets, alerts, menus, lists, or forms; applying layout, safe areas, typography, Dynamic Type, SF Symbols, color, Dark Mode, materials, or Liquid Glass; auditing accessibility such as VoiceOver, contrast, hit targets, and Reduce Motion; reviewing an app, screenshot, or pull request for HIG compliance; or adapting a design between iPhone, iPad, Mac, Apple Watch, Apple TV, and Apple Vision Pro. Also use when the user asks whether a UI "feels native" or "follows Apple's guidelines", even if the HIG is not mentioned by name. Not for web, Android, or cross-platform toolkit styling unless the goal is matching native Apple conventions.
license: MIT
metadata:
  author: <author>
  version: "0.1.0"
  short-description: Apple HIG guidance for SwiftUI, UIKit and AppKit UI work
---
```

- 953 characters; no `<`/`>`; no `: ` sequence inside the unquoted scalar; passes skills-ref 0.1.1 `[T]`.
- First sentence carries the core use case, so it survives truncation in any listing.
- `metadata.short-description` is read by Codex (S15 `[V]`); other clients ignore it.
- `compatibility` omitted on purpose (spec: most skills do not need it). Add only if scripts ship, e.g.
  `compatibility: Bundled scripts require Python 3.9+. No network access needed.`
- `allowed-tools` omitted: experimental, differing tool names per agent, and Copilot warns about shell pre-approval.
- Wording of the trigger list must be re-checked against the HIG vocabulary delivered by workstreams 1-3
  (e.g. whether "Liquid Glass" and "hit targets" match current HIG terms).

### 7.1 Description-writing guidance (sources disagree)

| Guidance | Source |
|----------|--------|
| State what it does **and** when to use it; include keywords users would say | S1, S7, S11 [V] |
| "Always write in third person" (description is injected into the system prompt) | S11 [V] |
| "Use imperative phrasing ... 'Use this skill when...'" ; focus on user intent; "err on the side of being pushy"; name cases where the user does not mention the domain | S3 [V] |
| Models tend to under-trigger; make descriptions somewhat pushy | S13 skill-creator [V] |
| Put the key use case first (truncation at 1,536 chars; descriptions may be dropped entirely) | S7 [V] |
| A few sentences to a short paragraph; hard limit 1024 | S3 [V] |
| Agents may skip skills for simple one-step tasks they can do unaided | S3 [V] |

Resolution used in the draft: third-person capability sentence, then "Use when ..." clauses (the form both S1's and
S11's own good examples use), then an explicit implicit-trigger sentence and one near-miss exclusion.

## 8. Install commands for the README

Replace `<owner>`. "[T]" here means the same command form was run against a local copy of the layout.

| Agent / route | Command | Tag |
|---------------|---------|-----|
| Any agent (Node >= 22.20) | `npx skills add <owner>/apple-hig-skill` (interactive agent picker; project scope) | [V] S14, [T] local path |
| Any agent, scripted | `npx skills add <owner>/apple-hig-skill --skill apple-hig -a claude-code -a codex -a cursor -g -y` | [V] S14, [T] without `-g` |
| Claude Code plugin (in session) | `/plugin marketplace add <owner>/apple-hig-skill` then `/plugin install apple-hig@apple-hig-skill` | [V] S10 |
| Claude Code plugin (shell) | `claude plugin marketplace add <owner>/apple-hig-skill && claude plugin install apple-hig@apple-hig-skill` | [V] S10 |
| Claude Code plugin (one step, >= 2.1.292) | `claude plugin install apple-hig --marketplace <owner>/apple-hig-skill` | [V] S10 |
| Claude Code manual, personal | `git clone https://github.com/<owner>/apple-hig-skill && cp -R apple-hig-skill/skills/apple-hig ~/.claude/skills/` | [V] path S7 |
| Claude Code manual, project | `cp -R apple-hig-skill/skills/apple-hig .claude/skills/` | [V] path S7 |
| Claude Code, try without installing | `claude --plugin-dir ./apple-hig-skill` | [V] S10 |
| claude.ai / Cowork | zip `skills/apple-hig/` and upload under Customize > Skills | [V] constraint S7; UI path [M] |
| Codex manual | `cp -R apple-hig-skill/skills/apple-hig ~/.agents/skills/` (or `<repo>/.agents/skills/`) | [W] S20 |
| Codex via bundled installer | `$skill-installer install https://github.com/<owner>/apple-hig-skill/tree/main/skills/apple-hig` (writes `~/.codex/skills/apple-hig`; restart Codex) | [V] S15, S16 |
| Cursor manual | `cp -R apple-hig-skill/skills/apple-hig ~/.cursor/skills/` (or `.cursor/skills/`, `.agents/skills/`) | [W] S21; global path also in S14 [V] |
| GitHub Copilot via gh (gh >= 2.90.0, public preview) | `gh skill install <owner>/apple-hig-skill apple-hig` ; other hosts: `--agent claude-code --scope user` | [V] S17; repo layout it expects [M] |
| GitHub Copilot manual | `cp -R apple-hig-skill/skills/apple-hig .github/skills/` (or `~/.copilot/skills/`) | [V] S17 |
| Copilot CLI | `copilot skill add <directory-or-URL>` or `/skills add <dir>` | [V] S17 |
| Gemini CLI | `gemini skills install https://github.com/<owner>/apple-hig-skill.git --path skills/apple-hig` (default scope user; `--scope workspace`) | [V] S18 |
| opencode manual | `cp -R apple-hig-skill/skills/apple-hig ~/.config/opencode/skills/` (or `.opencode/skills/`) | [W] S22; global path also in S14 [V] |
| Goose manual | `cp -R apple-hig-skill/skills/apple-hig ~/.agents/skills/` | [V] S19 |
| Generic fallback | copy to `.agents/skills/apple-hig/` (project) or `~/.agents/skills/apple-hig/` (user) | [V] S2 convention |

Not testable here: `gh skill` (sandbox has gh 2.89.0), anything needing github.com. Before publishing the README, run
each command once against the real repository.

## 9. Evals and trigger testing

**Output-quality evals** (`evals.json`; S4, S13 `[V]`):

```json
{
  "skill_name": "apple-hig",
  "evals": [
    {
      "id": 1,
      "prompt": "realistic user message",
      "expected_output": "human-readable description of success",
      "files": ["evals/files/SettingsView.swift"],
      "assertions": ["objectively checkable statement", "..."]
    }
  ]
}
```

- Field-name discrepancy: agentskills.io and skill-creator's SKILL.md use `assertions`; skill-creator's
  `references/schemas.md` documents `expectations` for the same list `[V]`. Use `assertions`.
- Process: run each case with and without the skill in clean contexts, grade into `grading.json`
  (`text`/`passed`/`evidence` per assertion), aggregate into `benchmark.json`; start with 2-3 cases (S4 `[V]`).
- Workspace output goes next to the skill (`<skill>-workspace/iteration-N/...`), never inside it (S4 `[V]`).

**Trigger evals** (S3, S13 `[V]`): JSON array of `{"query": "...", "should_trigger": true|false}`; about 20 queries
(8-10 each way); negatives should be near-misses (for us: React Native styling, Material Design, web CSS, Android
Compose, App Store metadata copy); run each 3 times; pass = trigger rate above/below 0.5; 60/40 train/validation
split; at most ~5 optimisation rounds. Claude Code detection: `claude -p "<query>" --output-format json` and look for
a `Skill` tool call with the skill name (S3 `[V]`). Plugin route: `claude plugin eval` with a `tool_used: Skill`
grader (S7 `[V]`, format not researched).

## 10. Validation checklist (for `tools/validate_skill.py` and CI)

External tools:
- `pip install skills-ref` (PyPI 0.1.1, Python >= 3.11) then **`agentskills validate skills/apple-hig`**. The spec and
  README say `skills-ref validate`, but the PyPI build installs the executable as `agentskills` `[T]`. The README
  labels the library "demonstration purposes only" `[V]`. It checks frontmatter only.
- `claude plugin validate .` and `claude plugin validate .claude-plugin/marketplace.json` (`--strict` turns warnings
  into failures); also checks the frontmatter of every skill in the plugin (S8, S10 `[V]`, both pass `[T]`).
- `npx skills add . --list` must print exactly one skill named `apple-hig` `[T]`.
- `gh skill publish --dry-run` validates against the spec plus repository settings (S17 `[V]`, not run).

Rules for our own script (E = error, W = warning):

| # | Rule | Sev | Basis |
|---|------|-----|-------|
| 1 | `skills/apple-hig/SKILL.md` exists, starts with `---` on line 1, has a closing `---` | E | S1, S7 |
| 2 | Frontmatter parses as YAML and is a mapping; no duplicate keys, no flow style | E | S6 |
| 3 | Top-level keys are a subset of the six spec fields | E | S6, S7 |
| 4 | `name` matches `^[a-z0-9]+(-[a-z0-9]+)*$`, length 1-64, equals the directory name | E | S1 |
| 5 | `name` does not contain `anthropic` or `claude` | E | S11 |
| 6 | `description` is a non-empty string, <= 1024 chars | E | S1 |
| 7 | `description` contains no `<` or `>`; no `: ` unless the scalar is quoted | E | S13, S2 |
| 8 | `description` contains a "Use when" clause; first sentence <= ~250 chars | W | S3, S7 |
| 9 | `compatibility`, if present, is a string of 1-500 chars | E | S1 |
| 10 | `metadata`, if present, is a flat map with string values | E | S1 |
| 11 | Body <= 500 lines | E | S1 |
| 12 | Body estimated tokens <= 5000 (chars / 4 as a conservative proxy [M]) | W | S1, S7 |
| 13 | Every relative link or backticked path in SKILL.md resolves to a file inside the skill directory | E | S1 |
| 14 | No absolute paths, `..` segments or backslashes in links | E | S1, S11 |
| 15 | Every file under `references/` is linked from SKILL.md (no orphans, no reference reachable only via another reference) | E/W | S1, S11 |
| 16 | Reference files > 100 lines begin with a table of contents | W | S11 |
| 17 | Links inside reference files resolve; script paths are written relative to the skill root | E | S5 |
| 18 | No Claude-Code-only syntax in the body: `$ARGUMENTS`, `${CLAUDE_`, `` !` `` | E | S7 |
| 19 | Scripts: shebang, executable bit, `--help` exits 0, no `input()`/`read -p`, stdlib-only imports | W | S5 |
| 20 | `plugin.json` and `marketplace.json` parse; plugin name equals marketplace entry name; versions match the SKILL.md `metadata.version` | E | S8, S9 |
| 21 | No `evals/`, workspace output, or files > 1 MB inside the skill directory | W | section 6 |
| 22 | Per-file size report for `references/` (flag files > ~400 lines for splitting) | W | S1 |

## 11. Compatibility

### 11.1 Feature matrix

| Capability used by `apple-hig` | Claude Code | Codex | Cursor | Copilot | Gemini CLI | opencode | Goose |
|--------------------------------|-------------|-------|--------|---------|------------|----------|-------|
| SKILL.md `name` + `description` discovery | [V] | [V] source | [W] | [V] | [V] | [W] | [V] |
| Model-driven auto activation | [V] | [W] | [W] | [V] | [V] (asks consent) | [W] | [V] |
| On-demand `references/` reads | [V] | [M] | [M] | [V] | [V] | [M] | [M] |
| Explicit invocation | `/apple-hig`, `/apple-hig:apple-hig` [V] | `$apple-hig` [W] | `/apple-hig` [W] | `/apple-hig` in prompt [V] | not documented in S18 | [M] | [M] |
| Native install from this repo | plugin marketplace [V] | skill-installer [V] | manual / `skills` CLI | `gh skill` [V] | `gemini skills install --path` [V] | manual / `skills` CLI | manual / `skills` CLI |
| `.agents/skills` read | no (not in S7) | [W] | [W] | [V] | [V] | [W] | [V] |
| `allowed-tools` honoured | [V] (pre-approval) | n/a in parser | S14 says yes | [V] | - | S14 says yes | - |
| Claude Code extensions (`context: fork`, hooks, `paths`) | [V] | no | no | no | no | no | no (S14 table) |

The `skills` CLI's own matrix lists "Basic skills: Yes" for 18 agents and `context: fork` for Claude Code only (S14 `[V]`).

### 11.2 Honest compatibility statement for the README (proposed wording)

> `apple-hig` follows the Agent Skills specification (agentskills.io) and uses only spec-defined frontmatter, plain
> Markdown and relative file links, so it should load in any client that implements the specification. It is
> validated in CI with the reference validator and Claude Code's plugin validator. Activation is decided by each
> agent's model from the skill description, so triggering behaviour differs between agents and models and is only
> measured on the agents listed under "Tested with" (agent, version, date). Other agents are expected to work but
> are untested. The skill needs no network access; bundled scripts (if any) need Python 3.

Rules for the statement: list only agents where an install plus a trigger test was actually run; give versions and
dates; do not claim "works with N agents" from the `skills` CLI table.

## 12. Contradictions with common lore / things that look stale

- The validator CLI installed from PyPI is `agentskills`, not `skills-ref` `[T]`; it is frontmatter-only and
  officially a demo, so our own link/size checks are still required.
- `openai/skills` is deprecated in favour of `openai/plugins` and plugin packaging (S16 `[V]`).
- Codex's documented user path is `~/.agents/skills` `[W]`, yet the bundled skill-installer on `main` still writes to
  `~/.codex/skills` `[V]`, and Cursor's docs list `.codex/skills` as a compat path `[W]`. Document `.agents/skills`
  first and mention `~/.codex/skills` as the installer's target.
- Claude Code's listing limits are a 1,536-char per-skill cap and a 1%-of-context budget (S7 `[V]`), not a fixed
  character budget; `name` is optional there and `allowed-tools` grants rather than restricts.
- "Third person" (Anthropic) vs "imperative" (agentskills.io) description advice conflict; see 7.1.
- `evals.json` list field: `assertions` vs `expectations`; see section 9.
- "One level deep" concerns link chains from SKILL.md, not directory depth.
- Claude Code does not read `.agents/skills`; cross-agent installs rely on the `skills` CLI symlink or a plugin.

## 13. Not verified

- Codex, Cursor, opencode, VS Code first-party pages (all `[W]`); Amp's own manual; Cline, Zed, Windsurf details.
- `gh skill` repository-layout expectations and the provenance keys it writes; `gh skill publish` checks.
- `.codex-plugin/plugin.json` schema; `claude plugin eval` case format; claude.ai upload UI path and zip rules.
- Real-world trigger rates of the draft description on any agent (needs section 9 evals).
- Whether each non-Claude agent truncates long descriptions in its catalog.
