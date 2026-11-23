# Architecture and research synthesis

How the `apple-hig` skill is organised, why, and what the research behind it found. Research notes for each
workstream are in [`research/`](research/); validation results are in [`validation.md`](validation.md).

## How it was built

Six research workstreams ran in parallel as separate agents on 2026-11-23, each writing one findings file and
tagging every claim as fetched-and-verified or from memory:

| Workstream | Output | Method |
|------------|--------|--------|
| HIG foundations, components, patterns | [`research/01-hig-foundations-components.md`](research/01-hig-foundations-components.md) | Downloaded all 171 HIG pages as JSON; read the core pages in full and the rest as rule headlines |
| Platforms | [`research/02-platforms.md`](research/02-platforms.md) | The "Designing for" pages, platform-specific pages, and build-setting documentation |
| SwiftUI and implementation | [`research/03-swiftui-implementation.md`](research/03-swiftui-implementation.md) | About 700 API symbols checked against documentation JSON for spelling, availability, and deprecation |
| Agent Skills architecture | [`research/04-agent-skills-architecture.md`](research/04-agent-skills-architecture.md) | Specification source, Claude Code documentation, and local runs of the reference validator, the `skills` CLI, and `claude plugin validate` |
| Ecosystem | [`research/05-ecosystem.md`](research/05-ecosystem.md) | Read 23 public repositories with Apple HIG, SwiftUI, and UI-review skills |
| Evaluation strategy | [`research/06-evaluation-strategy.md`](research/06-evaluation-strategy.md) | Upstream eval formats; every assertion backed by a fetched Apple fact |

Six writer agents then produced the reference files and examples with exclusive file ownership, re-reading the
full HIG page text for every topic (the research pass had only skimmed many component pages). The lead wrote
`SKILL.md`, the review guide, the linter, the validator, and these documents, and an independent reviewer
checked the result.

## Decisions

| Decision | Why |
|----------|-----|
| Skill lives at `skills/apple-hig/`, not the repository root | The specification requires the directory name to equal the skill name; a root `SKILL.md` in `apple-hig-skill/` fails the reference validator. This layout is also the default for Claude Code plugins and is scanned by the `skills` CLI. |
| Only specification frontmatter fields | Agent-specific fields fail the reference validator and other clients' loaders. |
| Flat `references/` with a group prefix, instead of nested folders | Every file is one link from `SKILL.md`, which is what the specification's "one level deep" guidance is about. Prefixes keep the grouping the brief asked for (foundations, components, patterns, platforms, accessibility, implementation). |
| Component families, not one file per component | One file per component means many reads per task; one file per platform holding everything is too large. Family files of 120 to 300 lines keep a typical task to two or three reads. |
| Design guidance and code are separate files | A design question should not pay for code, and a deprecation fix should not pay for design prose. |
| Every rule carries a strength tag | The HIG is mostly recommendation. Other skills present recommendations as hard rules, which produces false "violations". |
| A numbers table and a stale-lore list in `SKILL.md` | These are the commonest questions and the commonest fabrications; answering them without another file read is the cheapest win. |
| Paraphrase and link; no Apple text | Apple's documentation is copyrighted, and a copy goes stale. The most popular existing HIG skills bundle Apple's prose. |
| Evals and tooling outside the skill directory | Installers copy the whole skill directory, and some clients show the agent its file tree. |
| A bundled linter, labelled as producing leads | Deprecated APIs, fixed font sizes, and tap gestures used as buttons are mechanical to find. The label prevents it being read as a compliance check. |
| Name stays `apple-hig` | It was specified for this project. At least six other public skills use the same name, so the README warns about the collision. |
| MIT licence plus `NOTICE.md` | Matches the ecosystem and states the non-affiliation and trademark position. |

## What the research changed

Findings that contradicted common assumptions, all verified against Apple's live pages:

- The HIG has a design principles page again (since June 2026) with eight principles; "clarity, deference,
  depth" is no longer the framing.
- There is no navigation bars page. That guidance moved into Toolbars.
- The tab bars page contains no maximum tab count. It advises against overflowing into a More tab.
- 44x44 pt is the default control size on iPhone and iPad in the Accessibility page's table, which also lists a
  28x28 pt minimum and different values for each platform. The Buttons page separately asks for a 44x44 pt hit
  region. The HIG does not reconcile the two; the skill reports both and recommends the default.
- The contrast table's rows are "up to 17 pts", "18 pts", and bold. "18 pt and larger" is an interpretation.
- On iPad the tab bar sits at the top and can adapt into a sidebar; iPad has a menu bar and resizable windows.
- Liquid Glass (OS 26 and later) is for the navigation and control layer. Its SwiftUI APIs list no visionOS
  availability. The compatibility opt-out key is ignored when building for OS 27.
- Dark Mode does not apply on watchOS or visionOS, and macOS has no Dynamic Type.
- A large set of SwiftUI APIs (`NavigationView`, `tabItem`, `foregroundColor`, `cornerRadius`, `Alert`, and
  more) now carries a deprecation version equal to the current SDK, which is a placeholder rather than a real
  version. The skill says "deprecated, use X" without quoting it.
- Apple's documentation pages merge overloads and show the newest first, so the availability on a landing page
  can overstate an API's minimum OS.
- New surfaces appeared in 2026: a foldable iPhone ("iPhone Duo") with its own design page, and touch-display
  guidance for Mac.
- Very few HIG statements are hard requirements. The clearest is that an app that lets people create an account
  must let them delete it.

## What belongs where

| Location | Content |
|----------|---------|
| `SKILL.md` | Ground rules, platform and minimum-OS step, task workflows, routing table, published numbers, stale lore, review format, how to verify and report uncertainty |
| `references/foundations-*` | Principles, layout, typography, color and materials, icons, motion and writing |
| `references/components-*` | Navigation containers, presentations, controls, content views |
| `references/patterns-*` | Flows (launch, onboarding, settings, data entry, accounts) and interaction (feedback, gestures, keyboard, pointer, focus) |
| `references/platforms-*` | Detection, one file per platform, and the adaptation playbook |
| `references/accessibility-*` | Guidance and audit checklist; APIs and testing |
| `references/implementation-*` | Navigation, adaptive layout, styling, controls, availability, UIKit and AppKit |
| `references/review-guide.md` | Procedure, evidence limits, classification, severity, checkable rules |
| `examples/` | Seven Swift files and one complete review report |
| `scripts/hig_lint.py` | Regex-based lead finder |

## Unverified assumptions and open questions

- **Nothing was compiled.** No Swift toolchain was available. Whether the placeholder deprecations produce
  compiler warnings at lower deployment targets is unknown.
- **Install paths for Codex, Cursor, opencode, and VS Code** come from secondary sources; their documentation
  hosts were unreachable. `gh skill install` was not run.
- **Some platform-detection signals** could not be confirmed in Apple's documentation and are tagged
  `[Unverified]` in `references/platforms-detection.md`.
- **Absence claims** ("the HIG gives no card corner radius") rest on the pages that were read in full, not on
  an exhaustive search of every page.
- **SF Symbol names** in examples are not checked against the SF Symbols app.
- **Apple's legal pages** (site terms, trademark guidelines) were unreachable; `NOTICE.md` was written from
  general knowledge and should be reviewed before any commercial use.
- **System color values** are published as images and were not extracted; the skill refers to colors by name.
- **HIG technology pages** (Apple Pay, HealthKit, CarPlay, games, and others) were not read.

## Maintaining it

- Re-verify reference files against Apple's pages after each WWDC and each autumn release. The validator warns
  when a file's `Verified:` date is older than 270 days, and the scheduled CI job reports cited pages that no
  longer exist.
- When Apple's wording changes, update the rule and its tag; do not keep the old rule alongside.
- Add an eval scenario for any mistake the skill is seen to make, before fixing the text.
- Keep `SKILL.md` under roughly 250 lines and each reference under 300.
