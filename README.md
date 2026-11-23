# apple-hig-skill

An [Agent Skill](https://agentskills.io) that helps AI coding agents design, implement, review, and adapt native
Apple-platform interfaces in line with Apple's
[Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) (HIG), for iOS,
iPadOS, macOS, watchOS, tvOS, and visionOS.

> Independent project. Not affiliated with, endorsed by, or sponsored by Apple Inc. It paraphrases and links to
> Apple's documentation instead of reproducing it; Apple's pages are authoritative. See [NOTICE.md](NOTICE.md).

## What it does

| Workflow | What the agent does with the skill |
|----------|-------------------------------------|
| Design | Chooses navigation, presentations, and controls per platform, with the reason and source for each choice |
| Implement | Writes SwiftUI (or UIKit / AppKit) with system components, text styles, semantic colors, and availability checks for the project's minimum OS |
| Review | Reports findings classified as *confirmed guideline or API violation*, *accessibility issue*, *platform convention mismatch*, *recommended improvement*, or *subjective design suggestion*, each with severity, rationale, an Apple source link, and a fix |
| Refactor | Applies the smallest change that resolves a finding and lists the rest as optional |
| Accessibility | Audits vision, mobility, hearing, and cognitive needs, with the APIs to fix them |
| Adapt across platforms | Rebuilds navigation, input, and density for the target platform rather than copying iPhone chrome |

What makes it different from a prompt that says "follow the HIG":

- **Rules carry their strength.** Each rule bullet is tagged `[Req]` mandatory, `[HIG]` recommendation, `[API]`
  documentation or platform fact, `[Conv]` convention or the skill's own interpretation, or `[Unverified]`. Most
  of the HIG is recommendation, and the skill says so.
- **Current guidance.** Verified against Apple's live pages on 2026-11-23 (OS 27 SDK cycle), including the
  Liquid Glass design, the 2026 design principles, top tab bars on iPad, and the foldable iPhone Duo. It also
  lists popular "rules" that the HIG does not contain, such as a fixed maximum number of tabs.
- **Deployment-target aware.** The agent finds the minimum OS first and gates newer APIs.
- **Progressive disclosure.** A 219-line entry point (about 4,000 tokens) answers common questions on its own and
  routes to 29 reference files of about 5,000 tokens each. In the eight evaluated tasks the agent opened between
  zero and two of them.
- **No bundled Apple text.** Summaries, short factual values, and links only.

## Install

The skill is the directory [`skills/apple-hig/`](skills/apple-hig/). The manual routes below install only that
directory; the Claude Code plugin route caches the whole repository, of which Claude Code loads only the skill.

Commands marked *verified* were checked against the tool's own documentation or run against a local copy of this
layout. Commands marked *unverified* come from secondary sources because the vendor's documentation could not be
reached while this was written; check the vendor's current instructions if one fails.

**Any agent, via the `skills` CLI** (verified against a local copy):

```bash
npx skills add matinzd/apple-hig-skill
```

**Claude Code, as a plugin** (verified format; run inside Claude Code):

```
/plugin marketplace add matinzd/apple-hig-skill
/plugin install apple-hig@apple-hig-skill
```

**Claude Code, manual** (verified paths): copy into `~/.claude/skills/` for all projects or `.claude/skills/` for
one project.

```bash
git clone https://github.com/matinzd/apple-hig-skill
```

```bash
mkdir -p ~/.claude/skills && cp -R apple-hig-skill/skills/apple-hig ~/.claude/skills/
```

**claude.ai**: zip the `skills/apple-hig` directory and upload it in the skills settings (upload flow unverified).

**Other agents**: copy the same directory into the agent's skills folder.

| Agent | User-level folder | Project-level folder | Status |
|-------|-------------------|----------------------|--------|
| OpenAI Codex | `~/.agents/skills/` | `.agents/skills/` | Unverified (vendor documentation unreachable) |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` or `.agents/skills/` | Unverified (vendor documentation unreachable) |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` | Verified from GitHub's documentation source |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` or `.agents/skills/` | Verified from Gemini CLI's documentation source |
| Goose | `~/.agents/skills/` | `.agents/skills/` | Verified from Goose's documentation source |
| opencode | `~/.config/opencode/skills/` | `.opencode/skills/` | Unverified (vendor documentation unreachable) |

Gemini CLI can also install from the repository directly:

```bash
gemini skills install https://github.com/matinzd/apple-hig-skill.git --path skills/apple-hig
```

Several other public skills are also named `apple-hig`. Two skills with the same name cannot share one skills
folder, so remove or rename the other before installing this one.

## Use

The skill activates on its own when a request involves Apple-platform UI. You can also invoke it by name
(`/apple-hig` in Claude Code, or `/apple-hig:apple-hig` when installed as a plugin).

Example prompts:

- "Design the navigation for an iPhone and iPad recipe app with Browse, Favorites, Shopping List, and Settings."
- "Build a SwiftUI settings screen with notifications, appearance, and account sections. Minimum iOS 17."
- "Review `OrdersView.swift` against the HIG and list the findings by severity."
- "This screen breaks at large text sizes. Fix it with the smallest change."
- "Audit this player view for accessibility."
- "We're bringing our iPad app to the Mac. What has to change, and should we use Mac Catalyst?"
- "Does this feel native? It's an iPad app, but my designer says it looks like a stretched phone app."
- "Is it fine to put a big + button in the middle of the tab bar?"

The skill also bundles a small linter the agent can run for mechanically detectable leads. It needs only
Python 3:

```bash
python3 skills/apple-hig/scripts/hig_lint.py path/to/Sources
```

Its output is a list of leads to confirm by reading the code, not a verdict on HIG compliance.

## Compatibility

`apple-hig` uses only the frontmatter fields defined by the Agent Skills specification, plain Markdown, and
relative file links, so it should load in any client that implements the specification.

| Checked | Result |
|---------|--------|
| Agent Skills reference validator (`skills-ref` 0.1.1) | Valid (local run and CI) |
| Claude Code plugin validator (`claude plugin validate`, Claude Code 2.1.330) | Passed (local run on 2026-11-23, not in CI) |
| Repository validator ([`tools/validate_skill.py`](tools/validate_skill.py)) | 0 errors (local run and CI). Its online check that every cited Apple page exists passed locally and runs weekly in CI |
| Activation in Claude Code | 12 of 14 held-out trigger queries correct, one run each |
| Eight task scenarios in Claude Code, with and without the skill | 47 of 50 assertions against 38 of 49, one run each |
| Codex, Cursor, Copilot, Gemini CLI, and others | **Not tested.** Expected to load the skill; nothing was measured |

Details, caveats, and what the skill did not improve are in [docs/validation.md](docs/validation.md).

Activation is decided by each agent's model from the skill description, so triggering differs between agents and
models. Nothing in the skill needs network access. If the agent has it, the skill tells it how to verify a claim
against Apple's documentation.

## Repository layout

```
skills/apple-hig/          The skill
  SKILL.md                 Entry point: ground rules, workflows, routing table, review format
  references/              29 focused reference files: foundations, components, patterns,
                           platforms, accessibility, implementation, review
  examples/                Swift examples and a complete review report
  scripts/hig_lint.py      Optional linter for Swift sources
tests/evals/               Trigger queries, 18 task scenarios, and Swift fixtures
tests/test_hig_lint.py     Linter self-test
tools/validate_skill.py    Repository validator
tools/run_evals.py         Runs the evals in Claude Code, with and without the skill
docs/                      Architecture decisions, validation results, research notes
.claude-plugin/            Claude Code plugin and marketplace manifests
```

## Evaluating and validating

```bash
python3 tools/validate_skill.py
```

```bash
python3 tools/validate_skill.py --online
```

```bash
python3 tests/test_hig_lint.py
```

- [`tests/evals/trigger-queries.json`](tests/evals/trigger-queries.json): 40 queries (20 that should activate
  the skill, 20 near-misses that should not).
- [`tests/evals/evals.json`](tests/evals/evals.json): 18 scenarios with gradable assertions, covering platform
  selection, design, implementation, review, refactoring, accessibility, adaptation, unavailable APIs,
  conflicting guidance, hallucination traps, and context efficiency. The format follows the `evals.json`
  convention used by agentskills.io and Anthropic's skill-creator, with a few extra keys described in
  [docs/validation.md](docs/validation.md).
- [docs/validation.md](docs/validation.md): what was run, the results, and the manual procedures (Xcode build,
  Accessibility Inspector, cross-agent smoke tests).

## Limitations

- **The Swift examples were not compiled.** No Swift toolchain was available where the skill was built. API
  names and availability in the examples and code snippets were checked against Apple's documentation by the
  writers and again by a reviewer, but build the examples before relying on them.
- **Only Claude Code was exercised**, on one model, with one run per query. Other agents are untested.
- **The measured benefit is narrow.** In the evaluation the skill mainly stopped the agent overstating rules
  and made it cite sources; on half the scenarios it changed nothing measurable and cost more tokens.
- **Guidance dates quickly.** Each reference file states when it was verified. The scheduled CI job checks that
  cited Apple pages still exist, but not that their content is unchanged.
- **Coverage is selective.** The skill covers interface design and the common components and patterns. It does
  not cover the HIG's technology pages (Apple Pay, HealthKit, CarPlay, games, and similar) beyond pointers.
- **A linter cannot judge design.** `hig_lint.py` finds a narrow set of code patterns.
- **This is not App Review guidance.** Following the HIG does not guarantee approval.

More detail, including open questions from the research, is in [docs/architecture.md](docs/architecture.md) and
[docs/research/apple-hig/](docs/research/apple-hig/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the content rules: verify against Apple's documentation, paraphrase
and link, tag the strength of every rule, and run the validator.

## License

[MIT](LICENSE) for this repository's original text and code. Apple's documentation and trademarks belong to
Apple Inc.; see [NOTICE.md](NOTICE.md).
