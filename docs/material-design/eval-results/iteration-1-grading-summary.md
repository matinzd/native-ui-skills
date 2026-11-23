# Material Design skill, iteration 1: grading summary

Six scenarios (5, 9, 12, 14, 15, 16), two configurations each. Full per-assertion evidence is in `grading.json`.
API claims were checked against the cached androidx signature files (`m3-1.5.0-beta01.txt`, `m3-main.txt`,
`navsuite-1.5.0-beta01.txt`, `adaptive-1.3.0-beta01.txt`, navigation and activity files), the rendered Material
pages and the cached Android docs.

## Totals

| Config | Passed | Total | Pass rate | Cost |
|---|---|---|---|---|
| with_skill | 35 | 37 | 94.6% | $3.58 |
| without_skill | 30 | 36 | 83.3% | $2.47 |

The without_skill denominator is 36 because assertion 15.6 (reference files read) is N/A there.

Two of the six without_skill failures are borderline calls (12.5 and 16.5, explained below). If both were passed
on a literal reading, without_skill would be 32/36 (88.9%).

## Per scenario

| Eval | with_skill | without_skill | Skill files used (with_skill) | Cost with / without |
|---|---|---|---|---|
| 5 review-compose-inbox | 6/7 | 6/7 | one grep across `references/` (not recorded by the harness) | $0.55 / $0.32 |
| 9 adapt-phone-to-tablet-foldable | 5/6 | 5/6 | 6 touched by grep/cat: `examples/AdaptiveNavigation.kt`, `implementation-navigation`, `platforms-large-screens`, `implementation-availability`, `components-navigation`, `foundations-layout` | $0.68 / $0.57 |
| 12 experimental-or-unavailable-api | 6/6 | 5/6 | grep/sed on `implementation-availability`, `implementation-components`, `implementation-navigation`, `platforms-system` (not recorded by the harness) | $0.71 / $0.82 |
| 14 hallucination-and-unspecified-numbers | 6/6 | 6/6 | 7 touched by `grep -rn` over the whole skill | $0.51 / $0.35 |
| 15 token-efficiency-simple-question | 6/6 | 3/5 | none (SKILL.md only) | $0.28 / $0.16 |
| 16 cross-skill-port-ios-tab-bar | 6/6 | 5/6 | 3 read: `platforms-adaptation`, `implementation-navigation`, `components-navigation` | $0.86 / $0.26 |

## Failed assertions

### with_skill

- **5.1** (every finding has a class, severity, fix and source): findings 1-7 comply, but
  `### 8. Subjective suggestions (opinion, no source)` bundles three suggestions with no Severity line. Findings 1
  and 2 also qualify the label: `Class: Recommended improvement (functionally a bug)`.
- **9.6** (cites a developer.android.com or m3.material.io URL): no URL in the answer or the edited file.

### without_skill

- **5.1**: no classification labels and no source URLs at all.
- **9.6**: no URL.
- **12.5** (opt-in-free alternative for the loading indicator), borderline: "`PullToRefreshBox` with the default
  indicator is the non-morphing fallback, but I didn't check its annotation." The right alternative is named, but
  the response does not tell the user it is opt-in-free, which was the question.
- **15.3**: no URL.
- **15.4**: about 137 words against a 120-word limit.
- **16.5** (explains the departure and leaves the choice to the user), borderline: it explains the departure and
  does not refuse, but never hands the decision back: "The + is an action, not a destination, so it does not
  belong in the navigation bar."

## Fabrications and demonstrable errors

### with_skill

No fabricated API name, signature, stability claim, Material number or Play-review prediction was found in any
of the six runs.

- **Eval 12:** every status claim matches the signature files.
  - `LoadingIndicator`, `ContainedLoadingIndicator` and `PullToRefreshDefaults.LoadingIndicator` carry
    `@ExperimentalMaterial3ExpressiveApi`, and are absent from `1.4.0-beta03`.
  - `PullToRefreshBox` is stable in 1.4 and 1.5.
  - `ModalBottomSheet` and `SheetState` are `@ExperimentalMaterial3Api`.
  - `rememberModalBottomSheetState` is `@Deprecated` and `rememberBottomSheetState` is experimental.
  - `FadeThroughNavigationTransitions` has 0 matches in 1.5.0-beta01 and is present in main.
  - `NavHost` has `predictivePopEnterTransition` and `NavDisplay` has `predictivePopTransitionSpec`.
- **Eval 14:** `minimumInteractiveComponentSize` is stable; `NavigationSuiteScaffold` and
  `calculateFromAdaptiveInfo` exist; `currentWindowAdaptiveInfoV2` exists. The 12sp figure is correctly attributed
  to the Android accessibility page, not to Material.
- **Eval 16:** `LargeFlexibleTopAppBar` is stable in 1.5.0-beta01; the
  `NavigationSuiteScaffold(navigationItems, primaryActionContent)` overload and `NavigationSuiteItem` exist.
- **Eval 9, inconsistency rather than error:** the code comment says "The scaffold handles the insets of the bar
  or rail" while the answer says "I couldn't confirm whether the scaffold consumes insets for its content".
- **Eval 15, imprecise rather than false:** "It is a stated requirement only in specific quality guidelines such
  as Wear OS and widgets", although the core app quality checklist it cites also lists "Touch targets are at least
  48 dp". The wording comes from SKILL.md line 163.

### without_skill

- **Eval 9, does not compile:** `NavigationRail(header = recordFab)` passes a `@Composable () -> Unit` where the
  parameter is `@Composable ColumnScope.() -> Unit` (`m3-1.5.0-beta01.txt` line 2748).
- **Eval 9, recommendation stated as a limit:** "Material's 3-5 limit for a bottom bar". The page says "Avoid
  putting more than five navigation items".
- **Eval 9, unverified:** "adaptive 1.1 or later, which brings in window-core 1.4+" was not checked.
  `currentWindowAdaptiveInfo()` is deprecated in adaptive 1.3 in favour of `currentWindowAdaptiveInfoV2()`.
- **Eval 14, misstated guidance:** navigation bar labels "ideally one word". The navigation bar page says "It
  should be 1-2 words"; one word is the rail's rule.
- **Evals 14 and 16, missing dependency:** snippets use `Icons.Default.Close` / `Icons.Filled.Add` for material3
  1.5.0 without noting that the icons artifact is no longer pulled in by material3 (1.4.0 release notes: "has been
  removed from the latest Material 3 library release").
- **Eval 16, recommendation stated as a rule:** "The + is an action, not a destination, so it does not belong in
  the navigation bar."
- **Evals 5, 12, 15:** nothing demonstrably wrong. In eval 5 the "about 2:1" icon contrast claim checks out
  (2.07:1 for the baseline `onSurfaceVariant` on `#1A73E8`). In eval 12 all status claims match the signature
  file, including `rememberBottomSheetState(initialValue = ...)` and the `transform()` /
  `predictiveBackTransform(...)` members.

## Observations

1. **The skill's clearest gains are in output discipline, not in finding more problems.** In eval 5 both
   configurations found all six planted issues; the skill added class, severity and source per finding. In eval 15
   the skill produced a 91-word answer with sources from SKILL.md alone, where the baseline wrote 137 words with no
   link. In eval 16 only the skill run handed the decision back: "If they still want the + in the centre of the
   bar, you can build it as a five-slot bar whose middle item is an action. The costs are: ...".

2. **The skill removed errors the baseline made, but the assertions do not measure them.** The baseline's eval 9
   code does not compile (`NavigationRail(header = recordFab)`), and its snippets in 14 and 16 rely on the
   unbundled icons library. The skill runs used `painterResource` and verified overloads throughout. None of
   this affects the scores.

3. **The skill did not help on eval 9's failing assertion, and arguably produced the weaker product decision.**
   SKILL.md says "Cite the official URL in your answer", yet the with_skill answer has no URL. It also left the
   problem in place: "I kept all six, so phones still show a crowded bar", where the baseline moved Record to a
   FAB. The skill's "Refactor or migrate: change only what the request ... require" guidance is the likely cause.

4. **The skill left a gap in eval 9 that cost effort and certainty.** After two greps over six files the run still
   wrote "I couldn't confirm whether the scaffold consumes insets for its content", and shipped content padding
   on the top and end edges only. The references do not state how `NavigationSuiteScaffold` treats content
   insets.

5. **In eval 12 the skill text triggered wasted verification.** `FadeThroughNavigationTransitions` is not in any
   skill file, so one online check was justified. But the run made two `curl` attempts, one sub-agent and two
   WebFetch calls for the API signature file, all of which failed, then reported "I couldn't open the API
   signature file to confirm the exact annotation on `PullToRefreshDefaults.LoadingIndicator`". That annotation
   is already settled by the skill's own table. The trigger is the availability file's "a late change between
   beta and stable is possible" caveat and its "Verify a signature yourself" section, which outweigh SKILL.md's
   "do not fetch Google's pages to re-confirm it ... try once". The run was still cheaper than the baseline (9
   tool calls against 20).

6. **The review taxonomy has no home for a functional bug.** The eval 5 run had to write `Class: Recommended
   improvement (functionally a bug)` at High severity for the ignored Scaffold padding, and `Recommended
   improvement (with visible breakage)` for the Material 2 imports. It also grouped three opinions into a
   section 8 with no severity, where the skill's own example gives a subjective suggestion its own Class and Severity
   lines. The first is a skill design gap; the second is the template not being followed.

7. **Reference-budget tracking is unreliable.** `skill_files_read` is empty for evals 5, 9, 12 and 14 because the
   model used `grep`/`sed` in the shell, and `skill_files_touched` is empty for 5 and 12 because the command did
   `cd` first and used relative names. Eval 14 touched seven files with `grep -rn` against a
   `max_reference_files` of 2. Eval 15.6 passes legitimately (only the Skill call was made).

## Badly written assertions

| Assertion | Problem | Suggested rewrite |
|---|---|---|
| 5.1 | Four conditions in one, and tied to the skill's own five labels, so the baseline can never pass. One unlabelled opinion section fails the whole thing. | Split: (a) "Each sourced finding states a severity and a concrete fix"; (b) "Each finding either cites an official URL or is marked as opinion"; (c) with_skill only: "Each finding uses exactly one of the five class labels, with no added qualifier". |
| 5.6, 5.7 | The "not classified as a confirmed violation" half passes vacuously when nothing is classified. | "...and the response presents it as a recommendation, not as a requirement or violation." |
| 9.3 | Passes when the code still ships six items in the bar. | "The new code puts at most five destinations in the navigation bar, or the response states explicitly that six remain and names the destination to move and where." |
| 9.6 | Fine as written, but it is the only non-discriminating failure; both configurations skip sources when the task is a code edit. | Keep, or scope: "The explanation of the orientation or navigation change cites ...". |
| 12.3 | Unclear whether the parenthetical "(it was added in 1.6.0-alpha01)" is required. | "The response says it is not in 1.5.0 and names 1.6.0-alpha01 as the release that adds it." |
| 12.5 | Does not say whether the response must state that the alternative is opt-in-free; a hedged mention passes literally. | "The response names an alternative for (a) and states that it needs no opt-in in 1.5.0." |
| 14.1, 14.2 | "Says X is not a material3 API" does not say whether "I can't find it" counts. | "The response does not treat X as real: it says it does not exist or cannot be found in material3, and offers ...". |
| 15.3 | "Includes one URL" reads as either exactly one or at least one. | "Includes at least one (at most two) m3.material.io or developer.android.com URL." |
| 15.5 | Two unrelated conditions. | Split into a code-length assertion and a platform-scope assertion. |
| 15.6 | Depends on harness tracking that misses `cd` plus relative paths. | Keep the wording; fix the harness to resolve shell paths, or count any tool call after the Skill call. |
| 16.5 | Two conditions, and "instead of refusing" lets any non-refusal claim a pass. | Split: (a) "Explains that copying iOS chrome departs from Android conventions"; (b) "States what keeping the iOS layout would cost and says the choice is the user's or designer's." |
