# apple-hig: validation

What was checked, how, and what the results were. Everything here was run on 2026-11-23 in a Linux container
with network access to developer.apple.com, Python 3, and Claude Code 2.1.330. There was no Swift toolchain, no
Xcode, and no other coding agent. Raw outputs are in [`eval-results/`](eval-results/).

## Summary

| Check | Result |
|-------|--------|
| Agent Skills reference validator (`skills-ref` 0.1.1, command `agentskills validate`) | Valid. Run locally and in CI |
| Claude Code plugin validator (`claude plugin validate`) | Passed for the plugin and the marketplace manifest. Run locally only, not in CI |
| Repository validator, offline | 0 errors, 0 warnings. Run locally and in CI |
| Repository validator, online | All 326 Apple URLs cited in the skill (references, examples, linter) resolved to an existing page. Run locally; in CI on a weekly schedule only |
| Linter self-test | Passed (fixtures, 19 crafted cases, exit codes). Run locally and in CI |
| Independent accuracy audit against Apple's live pages | 16 corrections in 4 files; all applied |
| Independent Swift review (no compiler) | 9 corrections in 6 files; all applied |
| Independent architecture and consistency review | 10 major and 34 minor findings; majors addressed, see below |
| Activation in Claude Code, held-out queries | 12 of 14 correct (7 of 7 negatives, 5 of 7 positives), one run each |
| Task scenarios in Claude Code, 8 of 18 | With the skill 47 of 50 assertions passed; without it 38 of 49. One run each, before the fixes that the results prompted; three scenarios re-run afterwards and inspected by hand |
| Swift examples compiled | **Not done.** No toolchain |
| Other agents (Codex, Cursor, Copilot, Gemini CLI, and so on) | **Not tested** |

## Static validation

`tools/validate_skill.py` checks:

- Frontmatter: only specification fields; `name` format and equality with the directory name; description
  length and characters; `metadata` shape.
- Budgets: `SKILL.md` under 500 lines and about 5,000 tokens; each reference at most 300 lines and 30 KB.
- Links: every relative link and skill path in `SKILL.md`, the references, and the examples resolves; every file
  under `references/`, `examples/`, and `scripts/` is linked from `SKILL.md`.
- Provenance: each reference has a title, a `Verified:` date, at least one Apple source URL, and a source in
  every section that states Apple guidance.
- Swift: code fences closed and brackets balanced; deprecated spellings appear only in samples explicitly marked
  as before, avoid, deprecated, or fallback; a list of made-up API names never appears as real.
- Packaging: plugin and marketplace manifests agree with the skill's name and version.
- Evals: schema, unique ids, fixtures exist, expected references exist.
- With `--online`: the JSON behind every cited Apple page exists. Apple's human pages return 200 even for
  missing pages, so the JSON endpoint is what gets checked.

Current size: `SKILL.md` is 219 lines, about 16 KB (roughly 4,000 tokens). The 29 references total about 590 KB
and average about 20 KB each (roughly 5,000 tokens), so a task that loads two or three of them adds roughly
10,000 to 20,000 tokens.

## Independent reviews

Three agents that had not written the content reviewed it.

**Accuracy audit.** Re-fetched Apple's pages and checked about 300 statements, concentrating on the two files
written from summaries rather than from the pages (`accessibility-guidelines.md`, `review-guide.md`), the
numbers and lore sections of `SKILL.md`, and spot checks of six more files. Sixteen corrections, including:
account deletion may be offered through a direct link when it cannot happen in the app; destructive actions
should not get the primary role (not "the prominent style"); a sheet's Done button needs Cancel or Back; and
"never ask for a rating at first launch" was really "avoid". Every figure in `SKILL.md` matched. A handful of
statements could not be confirmed either way and are listed in the audit notes.

An earlier problem made this audit necessary: the text dumps of Apple's pages used by the first writers
replaced link text with the linked page's title, dropped captions, and blanked merged table cells. Writers
re-checked their files against the JSON once this was found.

**Swift review.** Read all seven examples and 34 code blocks as a compiler would and checked about 150 symbols
against documentation metadata. The most important fix: `#available(iOS 26, *)` is true on visionOS, where the
glass effect APIs do not exist, so several snippets would not have built for visionOS. They now exclude it at
compile time. Constructs the reviewer still considers at risk without a compiler, most risky first: the focused
value plumbing in `MacAppScenes.swift`; `#if` inside result builders followed by `if #available`; postfix `#if`
on modifier chains; a view with private state initialised through its memberwise initialiser in
`Presentations.swift`; `nil`-or-animation ternaries; `AnyLayout` chosen by a ternary in `AccessibleList.swift`.

**Architecture review.** Read-only. Major findings and what was done:

| Finding | Action |
|---------|--------|
| The first review class ("contradicts an explicit HIG statement you can link") turned every recommendation into a violation, against the skill's own ground rule | Class redefined: unavailable API, deprecated API with an available replacement, or a `[Req]` item. Departures from recommendations are "Recommended improvement" |
| Three different defaults for an unknown deployment target | One default (iOS 17, macOS 14, tvOS 17, watchOS 10, visionOS 1), stated in `SKILL.md` |
| The lint command did not work from the user's project directory | `SKILL.md` now tells the agent to call the script by absolute path |
| Linter returned "0 leads" for projects under a directory named `build`, and for missing paths | Fixed; exit status 2 when nothing was scanned |
| Linter false positives and negatives (scaled sizes, current `alert` overloads, background `ignoresSafeArea`, block comments, 40 to 43 pt frames, one-parameter `onChange`) | Fixed and covered by crafted test cases; remaining blind spots are listed in `--help` |
| The shipped review example reproduced an eval fixture with its answer | Example rewritten around a different screen |
| Eval metadata contradicted the skill's routing | `references_expected` and budgets corrected |
| The eval runner counted only `Read` calls | It now also records skill files named in shell and search commands |
| README claims not supported by the repository | Corrected; this file added |
| `[Req]` used both for obligations and for "not supported on this platform" | Platform facts retagged `[API]`; tag definitions clarified |

Minor findings about duplicated sections, close paraphrases, and inconsistent wording between files were also
addressed. Not done: a byte-accurate token budget per file, and running the plugin validator in CI.

## Activation

Method: `tools/run_evals.py triggers --skill apple-hig` starts a fresh non-interactive Claude Code session per query in an empty
project that contains only this skill, and records whether the skill was invoked. Each query ran once, so these
are indications, not rates.

| Run | Description | Result |
|-----|-------------|--------|
| 1 | First description, 16 queries | 12 of 16. All 8 negatives correct; 4 positives missed |
| 2 | Revised description, all 40 queries | 38 of 40. All 20 negatives correct; 18 of 20 positives |

The description was revised after run 1 using the four missed queries, all of which were in the training
split, so the fair figure for run 2 is the held-out validation split: **12 of 14** (7 of 7 negatives, 5 of 7
positives). The two misses were a UIKit refactor for text size and a SwiftUI onboarding flow with a
notification prompt; in both the model answered directly without loading the skill. The negatives covered
Jetpack Compose, CSS, Flutter, React Native, Swift concurrency, App Store metadata, server-side Swift, and
non-UI code review.

## Task scenarios

Method: `tools/run_evals.py tasks --skill apple-hig` ran eight scenarios twice each, once in a project containing the skill and
once in an empty project, same model and prompt. A separate grader agent scored every assertion with quoted
evidence, applying the same standard to both, and checked factual claims against Apple's pages. One run per
configuration.

| Scenario | With skill | Without | Skill files read | Cost with / without |
|----------|------------|---------|------------------|---------------------|
| 6 Review a flawed list screen | 7/8 | 4/8 | review-guide | $0.52 / $0.25 |
| 8 Minimal-diff Dynamic Type refactor | 5/6 | 5/6 | none | $0.39 / $0.27 |
| 12 Adapt to visionOS | 5/6 | 4/6 | platforms-visionos, platforms-adaptation | $0.81 / $0.25 |
| 14 API newer than the deployment target | 6/6 | 6/6 | implementation-availability, one example | $0.61 / $0.27 |
| 15 Brand requirements against the HIG | 7/7 | 6/7 | none | $0.96 / $0.72 |
| 16 Made-up modifier and made-up rule | 6/6 | 5/6 | none | $0.52 / $0.24 |
| 17 Numbers the HIG does not give | 6/6 | 6/6 | none | $0.31 / $0.20 |
| 18 Quick factual question | 5/5 | 2/4 | none | $0.28 / $0.16 |
| **Total** | **47/50 (94%)** | **38/49 (78%)** | | **$4.40 / $2.36** |

How to read this:

- **The gain is in rule strength and sourcing, not in facts.** Both configurations knew the facts. Without the
  skill the model stated six things the grader could show were wrong, all of them overstatements: 44 pt as a
  hard minimum (twice), a HIG position on "hamburger" menus that the HIG does not take, a specific deprecation
  version for `NavigationView`, and a confident prediction about App Review. With the skill there was one
  wrong claim (about small buttons in visionOS, also made without the skill) and no invented API, number, or
  App Review prediction.
- **Four of the eight scenarios showed no measurable gain** (8, 14, 17, and arguably 16), and the skill cost
  1.4 to 2.2 times as much on them. On this model those scenarios do not discriminate.
- **Counting borderline wording calls as passes narrows the gap** to 48 of 50 against 42 of 49.
- **The comparison on scenario 6 is inflated.** At the time of the run a shipped example contained that
  fixture and a model answer. The example has since been replaced.
- **The skill caused two problems, both fixed afterwards.** The original review class definition led one run
  to label an informational alert a "confirmed violation" while citing the page as a recommendation. And the
  instruction to verify claims online made two runs spend extra turns on fetches that failed; the skill now says
  not to re-verify what the references state and to try at most once.
- **Reference loading was light.** No run exceeded its budget; three answered from `SKILL.md` alone. The
  runner at that time missed files reached through shell commands, so the "files read" column is a lower bound.
- Several assertions were ambiguous or over-specific and have been rewritten; the grader's notes are in
  [`eval-results/iteration-1-grading-summary.md`](eval-results/iteration-1-grading-summary.md).

**Re-run after the fixes.** Scenarios 6, 16, and 18 were run again with the skill only, and inspected by hand
rather than graded. In scenario 6 the informational alert is now classed "Recommended improvement", the
hand-built bar "Platform convention mismatch", and only the deprecated APIs "Confirmed guideline or API
violation"; the menu image and the small tap targets are separate findings again
([output](eval-results/iteration-2-eval-06-with-skill.md)). Scenario 16 took 6 turns instead of 9 and still
rejected the made-up modifier. Scenario 18 again answered from `SKILL.md` without opening a reference. This
run used the rewritten review example, so scenario 6 was no longer contaminated.

Not run: scenarios 1 to 5, 7, 9 to 11, and 13; repeated runs for variance; other models; a graded
with-and-without comparison after the fixes.

## Eval file format

`tests/evals/apple-hig/evals.json` follows the convention used by agentskills.io and Anthropic's skill-creator
(`skill_name`, `evals[]` with `id`, `prompt`, `expected_output`, `files`, `assertions`). Extra keys used here:
`name`, `category`, `references_expected` (skill files a good run is likely to need), and `max_reference_files`.
`tests/evals/apple-hig/trigger-queries.json` is an array of `{query, should_trigger}` with extra `split` and `note` keys;
strip those two before feeding the file to skill-creator's description optimiser.

## Manual procedures not yet performed

**Build the examples.** Create a multiplatform SwiftUI app in Xcode, add each file from
`skills/apple-hig/examples/`, set the deployment targets to the minimums in each file's header, and build for
every platform the header lists. Record deprecation warnings. Run on the oldest and newest simulators to
exercise the availability fallbacks.

**Accessibility pass on each example screen.** Xcode's Accessibility Inspector audit; VoiceOver swipe-through;
the largest accessibility text size; Increase Contrast, Reduce Motion, Differentiate Without Color, and Bold
Text; light and dark appearance; a right-to-left pseudolanguage; Full Keyboard Access on iPad and Mac.

**Other agents.** Install the skill (see the README), start a new session, and run three prompts: "make this
SwiftUI settings screen feel native", the review prompt from scenario 6, and "what's the minimum tap target on
iOS?". Confirm from the agent's tool log, not from its own account, that it loaded `SKILL.md`, that the review
loaded `references/review-guide.md`, and that the quick question loaded no more than one reference. Then try a
negative such as a Jetpack Compose question and confirm the skill stays out.

## Reproducing

```bash
python3 tools/validate_skill.py --online
```

```bash
python3 tests/test_hig_lint.py
```

```bash
pip install skills-ref==0.1.1 && agentskills validate skills/apple-hig
```

```bash
claude plugin validate .
```

```bash
python3 tools/run_evals.py triggers --skill apple-hig
```

```bash
python3 tools/run_evals.py tasks --skill apple-hig --ids 6 8 12 14 15 16 17 18
```

The last two start real Claude Code sessions and cost tokens (about $7 for the eight scenarios in both
configurations, and about $8 for the 40 trigger queries, at the time of writing).
