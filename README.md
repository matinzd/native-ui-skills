# native-ui-skills

[Agent Skills](https://agentskills.io) that help AI coding agents design, implement, review, and adapt native
user interfaces according to each platform's official design guidelines.

| Skill | Covers | Status |
|-------|--------|--------|
| [`apple-hig`](skills/apple-hig/) | Apple's [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) for iOS, iPadOS, macOS, watchOS, tvOS, and visionOS, with SwiftUI, UIKit, and AppKit | Available. Verified against Apple's pages on 2026-11-23 |
| [`material-design`](skills/material-design/) | Google's [Material Design 3](https://m3.material.io/) (including Material 3 Expressive) and Android design guidance for phones, foldables, tablets, Wear OS, TV, and cars, with Jetpack Compose and Views | Available. Verified against Google's pages on 2026-11-23 |

> Independent project. Not affiliated with, endorsed by, or sponsored by Apple Inc. or Google LLC. The skills
> paraphrase and link to the official documentation instead of reproducing it; the official pages are
> authoritative. See [NOTICE.md](NOTICE.md).

Each platform gets its own skill on purpose. The guidelines disagree by design (navigation, back behaviour,
buttons, type scales), an agent loads a skill based on its description, and a task on one platform should not
pay context for the other.

## What a skill does

| Workflow | What the agent does with the skill |
|----------|-------------------------------------|
| Design | Chooses navigation, presentations, and controls per platform, with the reason and source for each choice |
| Implement | Writes code with system components, semantic type and color, and checks for the project's minimum OS or library version |
| Review | Reports findings classified as *confirmed guideline or API violation*, *accessibility issue*, *platform convention mismatch*, *recommended improvement*, or *subjective design suggestion*, each with severity, rationale, an official source link, and a fix |
| Refactor | Applies the smallest change that resolves a finding and lists the rest as optional |
| Accessibility | Audits vision, mobility, hearing, and cognitive needs, with the APIs to fix them |
| Adapt across devices | Rebuilds navigation, input, and density for the target device rather than stretching a phone layout |

What makes these different from a prompt that says "follow the guidelines":

- **Rules carry their strength.** Each rule bullet is tagged `[Req]` mandatory, `[HIG]` or `[MD]` recommendation
  (Apple's guidelines or Material and Android guidance), `[API]` documentation or platform fact, `[Conv]`
  convention or the skill's own interpretation, or `[Unverified]`. Most design guidance is recommendation, and
  the skills say so.
- **Contradictions are reported, not hidden.** Where the official pages disagree with each other, the skills
  give both statements instead of picking one.
- **Current guidance, with dates.** Each reference file states when it was verified against the official pages,
  and lists popular "rules" that the guidelines do not contain.
- **Version aware.** The agent finds the minimum OS or library version first and gates newer APIs.
- **Progressive disclosure.** A short entry point answers common questions on its own and routes to focused
  reference files, so a typical task opens only a few of them.
- **No bundled vendor text.** Summaries, short factual values, and links only.

## Install

Each skill is one directory under [`skills/`](skills/). Install the ones you need. In the commands below,
replace `apple-hig` with the skill you want.

Commands marked *verified* were checked against the tool's own documentation or run against a local copy of this
layout. Commands marked *unverified* come from secondary sources because the vendor's documentation could not be
reached while this was written; check the vendor's current instructions if one fails.

**Any agent, via the `skills` CLI** (verified against a local copy; it lists the skills and lets you choose):

```bash
npx skills add matinzd/native-ui-skills
```

**Claude Code, as a plugin** (verified format; run inside Claude Code). The plugin contains every skill in this
repository:

```
/plugin marketplace add matinzd/native-ui-skills
/plugin install native-ui-skills@native-ui-skills
```

**Claude Code, manual** (verified paths): copy into `~/.claude/skills/` for all projects or `.claude/skills/` for
one project.

```bash
git clone https://github.com/matinzd/native-ui-skills
```

```bash
mkdir -p ~/.claude/skills && cp -R native-ui-skills/skills/apple-hig ~/.claude/skills/
```

**claude.ai**: zip one skill directory and upload it in the skills settings (upload flow unverified).

**Other agents**: copy the skill directory into the agent's skills folder.

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
gemini skills install https://github.com/matinzd/native-ui-skills.git --path skills/apple-hig
```

Other public skills use the names `apple-hig` and `material-design` too. Two skills with the same name cannot
share one skills folder, so remove or rename the other before installing these.

## Use

A skill activates on its own when a request involves its platform's UI. You can also invoke one by name
(`/apple-hig` in Claude Code, or `/native-ui-skills:apple-hig` when installed as a plugin).

Example prompts for `apple-hig`:

- "Design the navigation for an iPhone and iPad recipe app with Browse, Favorites, Shopping List, and Settings."
- "Build a SwiftUI settings screen with notifications, appearance, and account sections. Minimum iOS 17."
- "Review `OrdersView.swift` against the HIG and list the findings by severity."
- "This screen breaks at large text sizes. Fix it with the smallest change."
- "Audit this player view for accessibility."
- "We're bringing our iPad app to the Mac. What has to change, and should we use Mac Catalyst?"
- "Does this feel native? It's an iPad app, but my designer says it looks like a stretched phone app."
- "Is it fine to put a big + button in the middle of the tab bar?"

Example prompts for `material-design`:

- "Design the navigation for an Android app with Home, Search, Library, and Profile that works on phones and tablets."
- "Build a Compose settings screen with notifications, appearance, and account sections. material3 1.5."
- "Review `InboxScreen.kt` against Material 3 and list the findings by severity."
- "Tablet users say our app looks like a blown-up phone. Make the root adaptive."
- "Should this be a dialog, a bottom sheet, or a snackbar?"
- "Is `ModalBottomSheet` stable in material3 1.5, and what do I use for a loading state?"
- "We're porting our iOS app to Android. It has a tab bar with a centre + button and large titles. What changes?"
- "Migrate this screen from Material 2 to Material 3 with the smallest diff."

`apple-hig` also bundles a small linter the agent can run for mechanically detectable leads in Swift sources.
It needs only Python 3:

```bash
python3 skills/apple-hig/scripts/hig_lint.py path/to/Sources
```

Its output is a list of leads to confirm by reading the code, not a verdict on HIG compliance.

## Compatibility

The skills use only the frontmatter fields defined by the Agent Skills specification, plain Markdown, and
relative file links, so they should load in any client that implements the specification.

| Checked | Result |
|---------|--------|
| Agent Skills reference validator (`skills-ref` 0.1.1) | Valid (local run and CI) |
| Claude Code plugin validator (`claude plugin validate`, Claude Code 2.1.330) | Passed (local run, not in CI) |
| Repository validator ([`tools/validate_skill.py`](tools/validate_skill.py)) | 0 errors (local run and CI). Its online check that every cited official page exists passed locally and runs weekly in CI |
| Activation and task evaluations in Claude Code | Per skill; see the validation reports below |
| Codex, Cursor, Copilot, Gemini CLI, and others | **Not tested.** Expected to load the skills; nothing was measured |

Activation is decided by each agent's model from the skill description, so triggering differs between agents and
models. Nothing in the skills needs network access. If the agent has it, the skills tell it how to verify a
claim against the official documentation.

## Repository layout

```
skills/<skill>/            One directory per skill
  SKILL.md                 Entry point: ground rules, workflows, routing table, review format
  references/              Focused reference files: foundations, components, patterns,
                           platforms, accessibility, implementation, review
  examples/                Code examples and a complete review report
  scripts/                 Optional helpers the agent can run
tests/evals/<skill>/       Trigger queries, task scenarios, and fixtures
tests/                     Self-tests for bundled scripts
tools/validate_skill.py    Repository validator (all skills)
tools/run_evals.py         Runs a skill's evals in Claude Code, with and without the skill
docs/<skill>/              Architecture decisions, validation results, research notes
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

Per skill:

| Skill | Evals | Validation report | Architecture and research |
|-------|-------|-------------------|---------------------------|
| `apple-hig` | [`tests/evals/apple-hig/`](tests/evals/apple-hig/): 40 trigger queries, 18 task scenarios, 5 Swift fixtures | [docs/apple-hig/validation.md](docs/apple-hig/validation.md) | [docs/apple-hig/architecture.md](docs/apple-hig/architecture.md), [docs/apple-hig/research/](docs/apple-hig/research/) |
| `material-design` | [`tests/evals/material-design/`](tests/evals/material-design/): 38 trigger queries, 16 task scenarios, 5 Kotlin and XML fixtures | [docs/material-design/validation.md](docs/material-design/validation.md) | [docs/material-design/architecture.md](docs/material-design/architecture.md), [docs/material-design/research/](docs/material-design/research/) |

Headline results in Claude Code, one run per query or scenario:

| Skill | Held-out trigger queries | Task scenarios, assertions passed with / without the skill |
|-------|--------------------------|-------------------------------------------------------------|
| `apple-hig` | 12 of 14 installed alone; 11 of 14 with both skills installed | 47 of 50 / 38 of 49 (8 scenarios) |
| `material-design` | 13 of 14 with both skills installed | 35 of 37 / 30 of 36 (6 scenarios) |

With both installed, neither skill activated on the other's queries. The reports explain what the skills did
not improve.

## Limitations

- **Code examples were not compiled.** Neither a Swift toolchain nor an Android SDK was available where the
  skills were built. Swift was checked against Apple's documentation and Kotlin against the androidx API
  signature files, by the writers and again by a reviewer, but build the examples before relying on them. The
  Compose Material 3 1.5.0 surface was read from a beta snapshot of the API file.
- **Only Claude Code was exercised**, on one model, with one run per query. Other agents are untested.
- **The measured benefit is narrow.** In both evaluations the skills mainly stopped the agent overstating rules
  or inventing API details and made it cite sources; on about half the scenarios they changed nothing measurable
  and cost more tokens.
- **Guidance dates quickly.** Each reference file states when it was verified. The scheduled CI job checks that
  cited pages still exist, but not that their content is unchanged.
- **Coverage is selective.** The skills cover interface design and the common components and patterns, not
  every technology page (for `apple-hig`: Apple Pay, HealthKit, CarPlay, games, and similar get pointers only;
  for `material-design`: Wear OS, TV, cars, and XR are covered at overview depth, and Views less deeply than
  Compose).
- **Google publishes its own Android skills** for specific migrations (edge-to-edge, adaptive layouts, Wear and
  TV, iOS to Android). `material-design` covers design guidance and review and is meant to sit alongside them.
- **A linter cannot judge design.** `hig_lint.py` finds a narrow set of code patterns.
- **This is not store-review guidance.** Following the guidelines does not guarantee approval by App Review or
  Google Play.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the content rules: verify against the official documentation,
paraphrase and link, tag the strength of every rule, and run the validator.

## License

[MIT](LICENSE) for this repository's original text and code. The official documentation and trademarks belong
to their owners; see [NOTICE.md](NOTICE.md).
