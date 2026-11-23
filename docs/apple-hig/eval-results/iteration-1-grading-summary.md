# Grading summary - apple-hig, iteration 1

Graded 2026-11-23 from `output.json` of 16 runs (8 evals x 2 configs). Same standard applied to both configs. Apple facts re-checked against the live `tutorials/data` JSON where an assertion or a fabrication call depended on them. Full per-assertion evidence: `grading.json`.

## Per eval

| Eval | with_skill | without_skill | References read (with_skill) / budget | Cost with / without | Turns with / without |
|---|---|---|---|---|---|
| 6 review-orders-view | 7/8 | 4/8 | review-guide.md (1/5) | $0.52 / $0.25 | 7 / 2 |
| 8 refactor-minimal-diff-dynamic-type | 5/6 | 5/6 | none (0/2) | $0.39 / $0.27 | 8 / 6 |
| 12 adapt-to-visionos | 5/6 | 4/6 | platforms-visionos.md, platforms-adaptation.md (2/3) | $0.81 / $0.25 | 6 / 1 |
| 14 deployment-target-newer-api | 6/6 | 6/6 | implementation-availability.md, examples/TabRoot.swift (2/2) | $0.61 / $0.27 | 7 / 4 |
| 15 conflict-brand-vs-hig | 7/7 | 6/7 | none (0/3) | $0.96 / $0.72 | 11 / 3 |
| 16 hallucination-fake-modifier-and-rule | 6/6 | 5/6 | none (0/2) | $0.52 / $0.24 | 9 / 2 |
| 17 uncertainty-unspecified-numbers | 6/6 | 6/6 | none (0/2) | $0.31 / $0.20 | 3 / 1 |
| 18 token-efficiency-simple-question | 5/5 | 2/4 | none (0/1) | $0.28 / $0.16 | 3 / 1 |

Eval 18 without_skill: the reference-loading assertion is N/A and excluded, so its denominator is 4.

## Totals

| Config | Passed | Total | Pass rate | Cost | Output tokens |
|---|---|---|---|---|---|
| with_skill | 47 | 50 | 94.0% | $4.40 | 26540 |
| without_skill | 38 | 49 | 77.6% | $2.36 | 22747 |

Delta: +16.4 points pass rate for with_skill at 1.86x the cost. Four of the 11 without_skill failures and one of the 3 with_skill failures are marked borderline in the evidence; counting every borderline failure as a pass gives 48/50 vs 42/49 (96% vs 86%).

## Failed assertions

### with_skill

- **Eval 6** - "The Image with onTapGesture is flagged and replaced with a Button (or Menu), citing accessibility and/or the SwiftUI guidance to use Button for button-like controls"
  - Flagged ('The menu icon is an `Image` with `onTapGesture`, so VoiceOver does not announce it as a button') but the fix is deletion: 'Delete the `HStack`' / 'Remove the icon for this release, or move the destinations into a `TabView`'. No Button or Menu replacement for that control. Borderline: the assertion is over-specific.
- **Eval 8** - "No lines other than the three font lines are modified in the applied change (a diff shows at most 4 changed lines)"
  - diff vs fixture: 3 changed lines + 2 added @ScaledMetric property lines = 5 changed lines (> 4). No pre-existing line other than the three font lines was touched. Fails only on the parenthetical count; assertion is self-contradictory (see summary).
- **Eval 12** - "The response recommends keeping standard windows for the UI rather than a fully immersive space"
  - absent - windows are assumed ('The window already sits on system glass') but there is no recommendation to keep windows over an immersive space

### without_skill

- **Eval 6** - "Every finding carries exactly one of the five classification labels, a severity, a concrete fix, and a developer.apple.com URL or an explicit note that no source exists"
  - absent - numbered prose items with no classification label, no severity field, no URLs
- **Eval 6** - "NavigationView is flagged as deprecated with NavigationStack (or NavigationSplitView) named as the replacement, without asserting a specific deprecation version as fact"
  - 'Use `NavigationStack` (`NavigationView` is deprecated on iOS 17)' - ties the deprecation to iOS 17; Apple's JSON reports deprecatedAt 27.3 (rolling soft deprecation). Borderline wording.
- **Eval 6** - "The 24x24 frame on the add button is flagged as below the 44x44 pt hit-target guidance, classified as an accessibility issue"
  - Size flagged ('constrained to 24x24, well under the 44x44pt minimum') but filed under 'A hand-built header replaces the system navigation bar'; not classified as an accessibility issue (no classification at all)
- **Eval 6** - "The hamburger menu is classified as a platform convention mismatch or recommended improvement, not as a confirmed guideline or API violation"
  - 'The HIG also steers iPhone apps away from hamburger drawers' - presented as HIG guidance under 'Fix before release', not labelled convention/recommendation
- **Eval 8** - "No lines other than the three font lines are modified in the applied change (a diff shows at most 4 changed lines)"
  - diff vs fixture: 3 changed lines + 3 added lines (2 @ScaledMetric properties and a blank line) = 6 changed lines (> 4). Same caveat as with_skill.
- **Eval 12** - "The response recommends keeping standard windows for the UI rather than a fully immersive space"
  - absent - no statement about windows versus immersive spaces
- **Eval 12** - "The response cites at least one visionOS-specific HIG URL"
  - absent - no URLs in the answer
- **Eval 15** - "The 10 pt title is flagged as below the 11 pt minimum text size for iOS and as an accessibility concern"
  - '10pt titles | Guidance | HIG recommends an 11pt minimum. Not enforced; it's a legibility cost.' - 11 pt minimum stated, but not framed as an accessibility concern (no Dynamic Type or accessibility mention for the size). Borderline.
- **Eval 16** - "The response cites the 44x44 pt hit-region guidance and describes it as a guideline/general rule"
  - 'What the HIG actually says is that controls need a **minimum hit target of 44x44pt**... It is a floor' - 44x44 cited but stated as a need/minimum, not as a guideline or general rule. Borderline.
- **Eval 18** - "The answer includes one developer.apple.com HIG URL"
  - absent - no URL
- **Eval 18** - "The answer does not include an unrequested review, code listing longer than 5 lines, or multi-platform survey"
  - Unrequested cross-standard and cross-platform survey: 'WCAG 2.5.5 (AAA)... WCAG 2.2's 2.5.8 (AA)... Android's Material guidance is 48x48dp. visionOS differs: 60x60pt'. Borderline: 'multi-platform survey' is vague.

## Fabrications and demonstrably wrong claims (not counted as assertions)

### with_skill

- **Eval 12**: Demonstrably incomplete HIG reading: 'the spacing is the problem, not the size'. HIG Buttons (visionOS): 'it's usually best to avoid displaying small or mini buttons in a vertical stack or horizontal row' - a row of Small (32 pt) buttons is itself discouraged.

### without_skill

- **Eval 6**: Fabricated HIG rule: 'The HIG also steers iPhone apps away from hamburger drawers'. The strings 'hamburger' and 'drawer' occur in none of tab-bars.json, sidebars.json, toolbars.json (fetched 2026-11-23); research doc F22 says the same.
- **Eval 6**: Imprecise deprecation claim: '`NavigationView` is deprecated on iOS 17'. swiftui/navigationview.json metadata.platforms gives deprecatedAt '27.3' for every platform (rolling soft deprecation), not an iOS 17 deprecation.
- **Eval 12**: Demonstrably incomplete HIG reading: 'the spacing is the problem, not the size'. HIG Buttons (visionOS): 'it's usually best to avoid displaying small or mini buttons in a vertical stack or horizontal row' - a row of Small (32 pt) buttons is itself discouraged.
- **Eval 15**: Unhedged App Review prediction and overbroad claim: 'Nothing you asked for will get the app rejected. Apple's Human Interface Guidelines (HIG) are guidance, and App Review doesn't enforce them.' The App Review Guidelines do incorporate the HIG in places (e.g. Apple Pay: 'must use Apple Pay branding and user interface elements correctly, as described in the Apple Pay Marketing Guidelines and Human Interface Guidelines' - developer.apple.com/app-store/review/guidelines/), and no outcome can be guaranteed.
- **Eval 16**: Overstated rule strength: 'controls need a minimum hit target of 44x44pt'. HIG Buttons says 'As a general rule, a button needs a hit region of at least 44x44 pt', and the Accessibility table lists 44x44 as the default and 28x28 pt as the minimum control size for iOS.
- **Eval 18**: Overstated: '44x44 points - that's Apple's Human Interface Guidelines minimum for tappable controls'. The HIG Accessibility table lists 44x44 pt as the default and 28x28 pt as the minimum control size; the Buttons page phrases 44x44 'as a general rule'.

No run in either config invented an API name: `liquidGlassStyle` was rejected by both (404 confirmed), and `glassProminent`, `glassEffect(_:in:)`, `GlassEffectContainer`, `@ScaledMetric`, `toolbarBackgroundVisibility` all resolve with the availability the answers stated. with_skill's firm claim that `glassEffect` exists on iOS, macOS, tvOS and watchOS 26 but not visionOS matches `metadata.platforms` exactly.

## Observations

1. **The skill's clearest win is rule strength and sourcing, not facts.** Both configs knew the facts (iOS 17/18/26 gates, 11 pt, 44 pt, vertical visionOS tab bar, no `liquidGlassStyle`). Only with_skill consistently labelled them: "Class: Platform convention mismatch ... The HIG does not mention drawers, so this is convention, not a violation" (eval 6) against the baseline's invented "The HIG also steers iPhone apps away from hamburger drawers"; "I can't tell you how App Review will treat any of this" (eval 15) against "Nothing you asked for will get the app rejected ... App Review doesn't enforce them". Every fabrication entry unique to without_skill is a strength or sourcing overstatement of this kind; with_skill has none.

2. **No measurable gain on four of eight evals.** Evals 8, 14 and 17 scored identically (eval 8 produced the same `@ScaledMetric` edit almost line for line), and eval 16's one-point gap is a borderline wording call. These cost 1.4x to 2.2x more with the skill. Evals 14 and 17 are candidates for removal or hardening, since they do not discriminate.

3. **The review class table works against ground rule 2.** In eval 6 with_skill filed the informational alert as "Class: Confirmed guideline or API violation" while writing "Source: .../alerts (recommendation)" on the same finding. The table's definition ("contradicts an explicit HIG statement you can link") makes any linked "avoid" sentence a confirmed violation, which is the upgrade rule 2 forbids ("do not turn a recommendation into a violation"). Suggest restricting that class to `[Req]`/API facts and sending linked recommendations to "Recommended improvement".

4. **"Group repeated instances" and "Prefer system components" cost the one substantive with_skill miss in eval 6.** The `Image` + `onTapGesture`, the 24x24 frame and the hidden bar were merged into one finding whose fix is "Delete the `HStack`", and the menu control got "Remove the icon for this release" with no Button or Menu replacement. The baseline, with no format to follow, named the replacement ("a toolbar `Menu` if these are actions"). Distinct problems on distinct lines should stay separate findings.

5. **Ground rule 1 plus the "Verifying" section drive tool churn with no change in the answer.** Eval 16: 9 turns vs 2 and $0.52 vs $0.24 for the same conclusion, with a blocked curl surfaced to the user as "I couldn't check Apple's live docs from this session (the network call wasn't approved)". Eval 15: 11 turns and $0.96, including three reference greps, three contrast-script steps and another failed fetch ("I couldn't reach Apple's docs from here"). The skill should say when not to verify (the claim is already in SKILL.md or a reference) and not to report failed attempts unless they change confidence.

6. **Reference routing was light, and the metric under-reports it.** No run exceeded `max_reference_files`, but in evals 6, 12, 15 and 16 the model grepped reference files through Bash instead of reading them, which `skill_files_read` does not count (eval 15 shows 0 files read while grepping six). Eval 6 loaded only `review-guide.md` of the five expected files and still found every planted issue; evals 17 and 18 answered from the SKILL.md tables alone, eval 18 nearly verbatim ("Apple doesn't reconcile the two"). That suggests the inline tables carry most of the value for short questions. Eval 12 is the one case where a reference clearly paid off (visionOS button size names, eyes/ornaments links, firm availability), at $0.81 vs $0.25, and it still missed the HIG line against rows of small buttons, as did the baseline.

## Assertions that need rewriting

| Eval | Assertion | Problem | Suggested rewrite |
|---|---|---|---|
| 8 | "No lines other than the three font lines are modified ... (a diff shows at most 4 changed lines)" | Self-contradictory, and it conflicts with assertion 1, which allows "a size tied to a text style": `@ScaledMetric` needs one added declaration per distinct size (two here), so the approach that best honours "don't restyle" can never pass. Both configs failed on this alone. | "No pre-existing line other than the three font lines is modified or removed; added lines are limited to declarations the font change needs (at most 3)." |
| 6 | "The Image with onTapGesture is flagged and replaced with a Button (or Menu) ..." | Over-specifies the fix. `showMenu` is never read, so removing the dead control or moving it to a toolbar item is equally valid. | "... is flagged as not exposing button semantics to assistive technology, and the fix either uses a real control (Button, Menu, toolbar item) or removes it with a reason." |
| 6 | "NavigationView is flagged ... without asserting a specific deprecation version as fact" | "deprecated on iOS 17" (the stated target) is ambiguous between a version claim and "deprecated for your target". | "... and does not state the OS version in which it was deprecated (phrases such as 'deprecated in/since/on iOS N' fail)." |
| 12 | "The 32 pt buttons are flagged against the 60x60 pt visionOS target guidance" | Conflates visible size and hit region. HIG Buttons lists Small (32 pt) as a valid visionOS size; 60x60 is the hit region and 60 pt the centre spacing. Both configs said "not the size" and were passed leniently. | "States the 60x60 pt hit-region guidance (or centres at least 60 pt apart) and that the 32 pt / 8 pt row does not meet it." Optionally add: "notes the HIG advice against rows of small or mini buttons." |
| 12 | "The response recommends keeping standard windows ... rather than a fully immersive space" | The prompt never raises immersive spaces; a complete answer need not mention them. Failed in both configs, so it measures nothing. | Drop it, or add "should we make this immersive?" to the prompt. |
| 15 | "The response provides working SwiftUI code ..." | "Working" is untestable: nothing is compiled, new files are not captured in `edited`, and tool-call inputs are truncated near 300 characters. | "Writes or shows SwiftUI code covering both the coloured bar and the appearance switch" plus a harness change to capture created files. |
| 15 | "... does not state a contrast ratio it has not computed from given colour values" | The prompt gives no colour values, so every ratio is for a placeholder. Both configs quoted correct ratios for a named hex. | "Any contrast ratio is tied to an explicitly named colour value and is correct to within 0.2; the response says the real brand colour must be checked." |
| 15, 16 | "... as an accessibility concern" / "describes it as a guideline/general rule" | Pass or fail turns on one word ("legibility" vs "accessibility", "floor" vs "recommendation"). | Name the observable: "mentions Dynamic Type, low vision or accessibility for the 10 pt text"; "does not call 44x44 a requirement and uses recommendation / general rule / guideline wording." |
| 18 | "at most 120 words" and "multi-platform survey" | Word count is ambiguous with a Markdown table (115 tokens including pipes); "survey" is undefined. | "At most 120 words excluding table syntax and URLs"; "mentions no platform other than iOS/iPadOS beyond one clause". |
| all | `max_reference_files` | Only eval 18 has a matching assertion, and `skill_files_read` misses Bash/grep access. | Add a per-eval assertion and have the harness count any tool call touching `references/`. |
