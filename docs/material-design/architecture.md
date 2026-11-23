# material-design: architecture and research synthesis

How the `material-design` skill is organised, why, and what the research behind it found. Research notes for each
workstream are in [`research/`](research/); validation results are in [`validation.md`](validation.md). The skill
follows the same structure as `apple-hig`; see [`../apple-hig/architecture.md`](../apple-hig/architecture.md) for
the decisions the two share (one skill per platform, flat prefixed references, strength tags, paraphrase and
link, evals outside the skill directory).

## How it was built

Five research workstreams ran in parallel as separate agents on 2026-11-23, each writing one findings file and
tagging every claim as fetched-and-verified or from memory:

| Workstream | Output | Method |
|------------|--------|--------|
| Material 3 foundations and styles | [`research/01-m3-foundations-styles.md`](research/01-m3-foundations-styles.md) | Rendered every foundations and styles page of m3.material.io in a headless browser, including expanded token tables |
| Material 3 components | [`research/02-m3-components.md`](research/02-m3-components.md) | Rendered the overview, guidelines, specs, and accessibility pages of every component (it reports 38 slugs) |
| Android platform, form factors, quality | [`research/03-android-platform-form-factors.md`](research/03-android-platform-form-factors.md) | About 360 developer.android.com pages: design guides, behaviour changes, quality guidelines, per-form-factor guides |
| Compose and Views implementation | [`research/04-compose-views-implementation.md`](research/04-compose-views-implementation.md) | The androidx public API signature files for each library and version, release notes, and the Material Components for Android docs |
| Evals and ecosystem | [`research/05-evals-and-ecosystem.md`](research/05-evals-and-ecosystem.md) | Eval assets with a table of the facts each assertion rests on; ten existing public skills read |

Five writer agents then produced the reference files, examples, and review guide with exclusive file ownership,
re-reading the cached page text and API files rather than the research summaries. The lead wrote `SKILL.md`.
Two reviewer agents then audited facts against the sources and read the Kotlin against the API signature
files.

## Decisions specific to this skill

| Decision | Why |
|----------|-----|
| Scope is Material 3 on Android, Compose first, Views second | Material's web and Flutter implementations have their own APIs and conventions; mixing them would blur activation and guidance. |
| Named `material-design`, with Android, Compose, and Views early in the description | The name was requested. It is common among public skills, mostly for web styling, so the description has to carry the Android scope. |
| Complement Google's official Android skills instead of duplicating them | Google publishes skills for specific workflows (edge-to-edge, adaptive layouts, Wear and TV migrations, iOS to Android). None covers component choice, design review, or general Material guidance. This skill covers those and defers to Google's for the migrations when they are installed. |
| A recommendation tag of its own, `[MD]` | It covers both Material and Android design guidance. `[Req]` is kept for what Google states as mandatory: quality guidelines marked required and Play target-API rules. |
| API status per library version, read from the API signature files | Compose Material 3 changes fast: stability annotations and deprecations differ between 1.4, 1.5, and 1.6 alpha. The reference pages and guides often lag. |
| Platform behaviour tied to `targetSdk` is tagged `[API]`, not `[Req]` | Edge-to-edge, predictive back, and large-screen resizability are enforced by the platform for apps targeting a given API level, not by store policy. |
| Contradictions between Google's pages are reported, not resolved | The research and writers found dozens (prose versus token tables, one page versus another). Picking a side silently would be inventing guidance. |
| A section for designs that come from iOS | Porting is a common task. It is written from the Android side only, using Google's own translation guide, so the skill works without `apple-hig` installed. |
| No bundled linter | The Apple skill's linter targets Swift. A Kotlin equivalent was not built; see open questions. |

## What the research changed

Findings that contradicted common assumptions, all read from the sources on 2026-11-23:

- Material 3 Expressive is an expansion of Material 3, not a new version, and most of its Compose APIs are stable
  in Compose Material 3 1.5.0 (released 18 November 2026).
- Several APIs widely assumed stable are still experimental in 1.5.0: modal bottom sheets, tooltips, the loading
  indicator, and the adaptive pane scaffolds.
- Material renamed components and concepts: top app bar became app bars, the bottom app bar gave way to the
  docked toolbar, window size classes became breakpoints.
- The navigation drawer, segmented buttons, and the baseline medium and large app bars are "no longer
  recommended".
- The 48dp touch target is worded as a recommendation in Material and the Android design docs; it is a stated
  requirement only in specific quality guidelines (Wear OS, widgets). Compose enlarges small touch targets by
  itself, so the usual real defect is unreserved space and overlapping targets.
- Edge-to-edge cannot be opted out of at `targetSdk` 36, predictive back is on by default there, and
  orientation and resizability locks are ignored on large screens.
- "Large screen app quality" was replaced by "Adaptive app quality" with new named IDs.
- Many Compose APIs agents reach for are deprecated: `Divider`, `TabRow`, older `ListItem`, `Slider`, and search
  bar overloads, `currentWindowAdaptiveInfo()`. The Material icons library is no longer bundled.
- Material publishes no minimum font size, no single snackbar duration, and no FAB edge margin.
- The Material site answers 404 for renamed pages when requested directly, which the validator's online check
  now catches.

## Unverified assumptions and open questions

- **Nothing was compiled.** There is no Android SDK in the build environment and Google's Maven host was
  unreachable. Kotlin was checked against API signature files only.
- **The 1.5.0 API surface is approximated.** No release branch was reachable, so "1.5.0" means the
  `1.5.0-beta01` signature snapshot cross-checked against release notes. One known mismatch: the release notes
  mention a `SplitButton` composable that the snapshot does not contain.
- **Numbers that appear only in images** on Material's pages (measurement diagrams) were not captured.
- **Wear OS, TV, cars, and XR are covered at overview depth**, with pointers. XR quality guidelines were not
  read.
- **Views coverage is thinner than Compose**, and several Views accessibility API names are tagged
  `[Unverified]`.
- **No Kotlin linter** equivalent to the Apple skill's `hig_lint.py`.
- **Google's Android skills were not read in full**, only their README and a list of skills.
- **Third-party skill metadata** (dates, popularity) could not be checked.

## Maintaining it

- Re-verify after each Compose Material 3 stable release and each Android release; the availability reference is
  the file most likely to go stale.
- When Google resolves one of its own contradictions, remove the "pages disagree" note rather than keeping both.
- The validator warns when a file's `Verified:` date is older than 270 days, and the scheduled CI job reports
  cited pages that no longer exist.
