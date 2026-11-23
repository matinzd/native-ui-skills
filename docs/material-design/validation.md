# material-design: validation

What was checked, how, and what the results were. Everything here was run on 2026-11-23 in a Linux container
with network access to m3.material.io and developer.android.com, Python 3, and Claude Code 2.1.330. There was no
Android SDK, no emulator, and no other coding agent, and Google's Maven host was unreachable. Raw outputs are in
[`eval-results/`](eval-results/).

## Summary

| Check | Result |
|-------|--------|
| Agent Skills reference validator (`skills-ref` 0.1.1) | Valid. Run locally and in CI |
| Claude Code plugin validator (`claude plugin validate`) | Passed for the repository plugin, which contains both skills. Run locally only |
| Repository validator, offline | 0 errors. One warning: `SKILL.md` is above the 4,000-token warning threshold (limit 5,000) |
| Repository validator, online | Every m3.material.io and developer.android.com URL cited in the skill resolved. Run locally; in CI on a weekly schedule only |
| Independent accuracy audit against the cached official pages | 14 corrections in 10 files, almost all tag strength or consistency; no wrong number found. All applied |
| Independent Kotlin review (no compiler) | 7 corrections; all 157 imports in the examples resolve; no wrong overload or missing opt-in found |
| Independent architecture and consistency review | No critical findings, 10 major, 15 minor; addressed, see below |
| Activation in Claude Code with both skills installed, held-out queries | 13 of 14 correct (7 of 7 negatives, 6 of 7 positives), one run each, before any tuning |
| Task scenarios in Claude Code, 6 of 16 | With the skill 35 of 37 assertions passed; without it 30 of 36. One run each, before the fixes the results prompted |
| Kotlin examples compiled | **Not done.** No Android SDK |
| Other agents (Codex, Cursor, Copilot, Gemini CLI, Android Studio, and so on) | **Not tested** |

## Static validation

The same validator as for `apple-hig` (`tools/validate_skill.py`; see
[`../apple-hig/validation.md`](../apple-hig/validation.md) for what it checks), with two differences for this
skill: Kotlin code fences and `.kt` files get the bracket-balance check, and the online check requests
m3.material.io and developer.android.com pages directly, because both answer 404 for missing pages. That check
caught several renamed Material pages during writing (for example the window size classes page, now breakpoints),
whose old URLs only redirect inside a browser.

Current size: `SKILL.md` is 247 lines, about 20 KB (roughly 4,600 tokens by the validator's estimate). The 25
references total about 560 KB and average about 22 KB each (roughly 5,500 tokens), so a task that loads two or
three adds roughly 11,000 to 17,000 tokens.

## Independent reviews

**Accuracy audit.** Checked about 370 statements against the cached official pages: every number and bullet in
the numbers and lore sections of `SKILL.md`, every rule in the review guide, every `[Req]` tag in the skill,
every `targetSdk` and Play target-API statement, and spot checks of eight more files. Fourteen corrections, for
example: edge-to-edge enforcement was tagged as a requirement in two files and is platform behaviour; themed
icons were tied to `targetSdk` 33 although they depend on the device and launcher; "pull to refresh cannot be the
only way to refresh" was tagged mandatory where the page only advises it. In `SKILL.md`, "surface tint is gone"
became "deprecated", and the claim that 48dp is a requirement "only" for Wear OS and widgets was widened, because
Material uses "must" for 48dp on several component pages. Not verified either way: a handful of token values and
the full text of some quality-guideline rows.

After the audit the skill has 88 rules tagged `[Req]`: quality-guideline items marked required (Wear OS, TV,
cars, widgets), Play target-API levels, and statements where a Material page itself says "must" or "requires"
(for example that navigation items have a text label).

**Kotlin review.** Read all seven examples and 22 code blocks against the androidx API signature files, fetching
six more signature files for modules that were not cached. Fixes included an accessibility test call that needs
an API 34 guard, an undeclared variable in one snippet, and example headers that misstated which calls need
version 1.5. Constructs the reviewer still considers at risk, most risky first: anything new in 1.5, because it
was verified against a beta snapshot; `currentWindowAdaptiveInfoV2()`, which needs adaptive 1.3 on the classpath;
the accessibility-checks test call; composable lambdas chosen by an `if` expression in `FormScreen.kt`.

One discrepancy is recorded rather than resolved: the 1.5.0 release notes describe a `SplitButton` composable,
while the API snapshot and the source on the development branch contain only `SplitButtonLayout`. The references
say so and tell the agent not to guess a signature.

**Architecture and consistency review.** Read-only. Major findings and what was done:

| Finding | Action |
|---------|--------|
| Navigation at medium width was stated four different ways | One working rule in `SKILL.md` and the references, with a note that Material's pages disagree |
| Three sentences said material3 1.4 has no Expressive API, against tables listing two that are stable in 1.4 | Corrected against the 1.4 API file |
| `SKILL.md` said the references are "already verified" although they contain `[Unverified]` bullets and API status comes from a snapshot | Reworded to say exactly that |
| Implementation files described their evidence as the reference website | Headers now say signatures came from the API snapshot |
| A lore bullet (Material 2 Compose deprecated, Views in maintenance mode) had no backing reference | Sourced bullets added to the references |
| The `targetSdk` behaviour table existed in three files | One full table, two short summaries with pointers |
| No routing row for the "numbers Material does not publish" table, and several rows omitted topics | Routing table updated |
| Three eval scenarios depended on facts or references the skill did not provide | Assertions and expected references corrected |

Also addressed: two trigger queries marked "should not trigger" that the skill legitimately covers were removed
(38 queries remain); one eval prompt that a shipped example nearly answered now asks for a different form; an
example composable that shared a name with a fixture was renamed; three close paraphrases were reworded. The
skill has no link outside its own folder and does not assume `apple-hig` is installed, and the reverse holds.

## Activation

Method: `tools/run_evals.py triggers --skill <skill> --all-skills --split validation` starts a fresh
non-interactive Claude Code session per query in an empty project that contains **both** skills, and records
which skill was invoked. Each query ran once, so these are indications, not rates. The `material-design`
description had not been tuned on any result before this run, so the held-out split is a fair first measurement.

| Skill, with both installed | Held-out result |
|----------------------------|-----------------|
| `material-design` | 13 of 14: all 7 negatives correct, 6 of 7 positives |
| `apple-hig` | 11 of 14: all 7 negatives correct, 4 of 7 positives |

- Neither skill fired on the other's queries. A `UITabBarController` question in the Material negatives invoked
  `apple-hig` and not `material-design`.
- The Material miss was a request to refactor a Compose screen so sizes and colors come from the theme; the
  model answered directly.
- `apple-hig` scored 12 of 14 on the same queries when installed alone. The extra miss with both installed was
  a SwiftUI badge-color question that the model answered directly. With one run per query this cannot be told
  apart from run-to-run variance.
- One of the Material negatives in this run (Compose UI tests) was later removed from the set as ambiguous; it
  was counted as correct above.

## Task scenarios

Method: `tools/run_evals.py tasks --skill material-design` ran six scenarios twice each, once in a project
containing the skill and once in an empty project. A separate grader agent scored every assertion with quoted
evidence, applying the same standard to both, and checked API claims against the signature files.

| Scenario | With skill | Without | Cost with / without |
|----------|------------|---------|---------------------|
| 5 Review a flawed Compose screen | 6/7 | 6/7 | $0.55 / $0.32 |
| 9 Adapt a phone shell for tablets and foldables | 5/6 | 5/6 | $0.68 / $0.57 |
| 12 Experimental and unavailable APIs on a pinned version | 6/6 | 5/6 | $0.71 / $0.82 |
| 14 Made-up APIs and numbers Material does not publish | 6/6 | 6/6 | $0.51 / $0.35 |
| 15 Quick factual question | 6/6 | 3/5 | $0.28 / $0.16 |
| 16 Port an iOS tab bar design to Android | 6/6 | 5/6 | $0.86 / $0.26 |
| **Total** | **35/37 (95%)** | **30/36 (83%)** | **$3.58 / $2.47** |

How to read this:

- **The measured gain is modest and is mostly output discipline.** Both configurations found all six planted
  problems in the review scenario; the skill added classification, severity, and sources. Counting two
  borderline calls as passes, the baseline reaches 32 of 36.
- **The skill removed errors the assertions do not measure.** The grader found no fabricated or wrong API claim
  in any run with the skill. Without it, one scenario's code would not compile (a parameter of the wrong
  function type), two used an icons library that Material 3 no longer bundles without saying so, and several
  answers stated recommendations as limits.
- **Three scenarios showed no gain** (5, 9, 14), and the skill cost more on five of six.
- **The skill caused or failed to prevent three problems.** One run labelled a finding "Recommended improvement
  (functionally a bug)" and lumped three suggestions together without severities; the format now requires a
  class and severity for every finding and gives plain bugs their own list. One run made five failed attempts
  to fetch an API file for a fact the skill's own table already stated; the availability reference now says its
  tables are the answer for anything they list. One run could not tell from the references how the adaptive
  navigation scaffold treats insets; that is now stated.
- **In the adaptation scenario the skill run made the weaker product decision**: it kept six destinations in a
  crowded navigation bar where the baseline moved one to a floating action button, probably because of the
  skill's minimal-change guidance. Not changed; noted as a limitation.
- **Reference loading could not be measured reliably.** The agent often read skill files through shell commands
  and relative paths, which the runner does not fully capture.

Not run: scenarios 1 to 4, 6 to 8, 10, 11, and 13; the training split of trigger queries; repeated runs; other
models; a re-run after the fixes.

## Manual procedures not yet performed

**Build the examples.** Create an Android app in Android Studio with the Compose BOM named in the example
headers, add each file from `skills/material-design/examples/` with the string and drawable resources its header
lists, and build. Record deprecation warnings and any opt-in the compiler asks for that a header does not list.
Repeat with material3 1.4 where a header gives a fallback.

**Accessibility pass on each example screen.** TalkBack swipe-through; Accessibility Scanner; font size at the
largest setting; dark theme; a resized, split-screen, and unfolded window; Switch Access; a hardware keyboard.

**Other agents.** As for `apple-hig`: install, start a new session, run a positive prompt, the review prompt
from scenario 5, the quick question from scenario 15, and a negative such as a SwiftUI question, and confirm
from the tool log which skill and files were loaded.

## Reproducing

```bash
python3 tools/validate_skill.py --skill material-design --online
```

```bash
python3 tools/run_evals.py triggers --skill material-design --all-skills --split validation
```

```bash
python3 tools/run_evals.py tasks --skill material-design --ids 5 9 12 14 15 16
```

The last two start real Claude Code sessions and cost tokens (about $3 and $6 respectively at the time of
writing).
