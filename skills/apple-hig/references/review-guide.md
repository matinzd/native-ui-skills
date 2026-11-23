# Review guide

How to review an existing Apple-platform interface (code, screenshot, or description) and report findings.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Procedure
- What evidence allows which claims
- Choosing the class
- Choosing the severity
- Checkable rules: accessibility
- Checkable rules: appearance and layout
- Checkable rules: navigation and presentation
- Checkable rules: controls, flows, and code
- Refactoring after a review
- Common mistakes

## Procedure

1. Establish platform, minimum OS, and framework (`references/platforms-detection.md`). State any assumption at
   the top of the report.
2. Read the whole screen before judging parts of it: what is the content, what is the main task, how does a
   person get in and out.
3. For Swift code, optionally run `python3 scripts/hig_lint.py <path>` to collect leads. Confirm each lead by
   reading the surrounding code; drop leads that the context makes fine (a deprecated API inside an availability
   fallback, a fixed size on a decorative shape, a tap gesture that is not an action).
4. Walk the checkable rules below in order. Open the linked reference only for areas where something looks off.
5. Write findings in the format given in `SKILL.md`: class, severity, where, why, source, fix. Group repeated
   instances into one finding and list the locations.
6. Finish with what could not be verified and what already works. Do not pad the report: five findings that
   matter are more useful than twenty.

Source: https://developer.apple.com/design/human-interface-guidelines

## What evidence allows which claims

| Evidence | You can assess | You cannot assess |
|----------|----------------|-------------------|
| Source code | Components used, API availability and deprecation, text styles, semantic colors, labels, structure | Rendered contrast, real sizes after layout, how it feels |
| Screenshot | Hierarchy, density, visible labels, approximate sizes and contrast, platform fit | Accessibility labels, Dynamic Type behaviour, Dark Mode, interaction, exact point values |
| Description | Structure and component choice | Almost everything visual |

- [Conv] Say which kind of evidence you had. Sizes and contrast read from a screenshot are estimates: report
  them as "appears to be" and ask for the value or the code.
- [Conv] A claim about how the interface behaves at large text sizes, in Dark Mode, or with VoiceOver needs
  either the code or a test. If you have neither, list it under "Not verified" with what to test.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Choosing the class

Use exactly one class per finding. Ask the questions in order and stop at the first yes.

| Question | Class |
|----------|-------|
| Does it use an API that is unavailable or deprecated for the stated minimum OS, or contradict an explicit HIG statement you can link? | Confirmed guideline or API violation |
| Is a person using an assistive setting or technology blocked or disadvantaged? | Accessibility issue |
| Does it work but differ from what people expect on this platform? | Platform convention mismatch |
| Would following a HIG recommendation make it better, though nothing is broken? | Recommended improvement |
| Is it your judgment, with no source? | Subjective design suggestion |

- [Conv] When a problem is both an accessibility barrier and a HIG statement, class it as an accessibility
  issue and cite the HIG page; the effect on people matters more than the label.
- [Conv] "Confirmed" means you can link the statement or the API page. HIG guidance is mostly recommendation,
  so name the strength in the Source line: requirement, recommendation, or API documentation.
- [Conv] Patterns the HIG does not mention, such as a "hamburger" button that reveals a drawer on iPhone, are
  convention mismatches. Do not present them as HIG violations.
- [Conv] A deprecated API is a violation only as "deprecated, replacement available for this target". If the
  replacement needs a newer OS than the project supports, it is not a finding.

Source: https://developer.apple.com/design/human-interface-guidelines

## Choosing the severity

| Severity | Meaning | Typical examples |
|----------|---------|------------------|
| High | Blocks a task, excludes people, or does not build or run on the target | Control with no accessible name; text pinned to one size; modal with no way out; API newer than the minimum OS with no availability check; essential state shown by color alone |
| Medium | Friction or inconsistency people will notice | Custom tab bar replacing the system one; phone layout stretched on iPad; hard-coded colors that break in Dark Mode; alert used for routine information |
| Low | Polish | Deprecated modifier with a drop-in replacement; title wording; missing grabber on a resizable sheet |

- [Conv] Rank accessibility barriers and unavailable APIs above convention mismatches, and those above taste.
- [Conv] Lower the severity when the evidence is weak (an estimate from a screenshot) and say so.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Checkable rules: accessibility

Details: `references/accessibility-guidelines.md` and `references/accessibility-implementation.md`.

- [HIG] Tappable regions meet the platform's default control size (44x44 pt on iPhone, iPad, and Apple Watch;
  28x28 pt on Mac; 66x66 pt on Apple TV; 60x60 pt on Apple Vision Pro). Below the default is a recommendation;
  below the published minimum is an accessibility issue.
- [HIG] Text is no smaller than the platform minimum (11 pt on iPhone and iPad, 10 pt on Mac, 12 pt on Apple
  Watch and Apple Vision Pro, 23 pt on Apple TV).
- [HIG] Text uses text styles or scales with the person's text size; layouts reflow instead of truncating at
  the largest sizes. Not applicable on macOS, which has no Dynamic Type.
- [HIG] Text contrast is at least 4.5:1 up to 17 pt and 3:1 for 18 pt or bold text, in light and dark
  appearances.
- [HIG] Color is never the only signal for state, validity, or interactivity; add a symbol, shape, or text.
- [HIG] Every control and meaningful image has an accessible label; decorative images are hidden from
  assistive technologies.
- [HIG] Every gesture-driven action (swipe, long press, drag, custom gesture) also has a visible control.
- [HIG] Motion respects Reduce Motion, and nothing essential is conveyed only by motion, sound, or haptics.
- [HIG] Essential information does not disappear on a timer; media does not play automatically without
  controls.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility
Source: https://developer.apple.com/design/human-interface-guidelines/voiceover
Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Checkable rules: appearance and layout

Details: `references/foundations-layout.md`, `references/foundations-color-materials.md`,
`references/foundations-typography.md`.

- [HIG] Colors are system or asset-catalog colors that adapt to light, dark, and increased contrast. Hard-coded
  values for text and backgrounds are a recommended improvement, and an accessibility issue when contrast fails.
- [HIG] The app follows the system appearance rather than offering its own light and dark switch.
- [HIG] Content and controls respect safe areas; only backgrounds extend to the edges.
- [HIG] Layout adapts to size classes and available space, not to device idiom or orientation.
- [HIG] Bars keep the system background. Custom opaque bar backgrounds and tinted bar items work against the
  current design (OS 26+, Liquid Glass) and its scroll edge effects.
- [HIG] Liquid Glass (OS 26+) is used for navigation and controls, not for content such as cards and rows.
- [HIG] Light font weights (Ultralight, Thin, Light) are avoided, especially at small sizes.
- [HIG] Layout mirrors correctly for right-to-left languages: use leading and trailing, not left and right.

Source: https://developer.apple.com/design/human-interface-guidelines/layout
Source: https://developer.apple.com/design/human-interface-guidelines/color
Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode
Source: https://developer.apple.com/design/human-interface-guidelines/materials

## Checkable rules: navigation and presentation

Details: `references/components-navigation.md`, `references/components-presentation.md`, and the platform file.

- [HIG] A tab bar is for navigation between sections, not for actions. Tabs are not hidden or disabled when
  their content is unavailable; explain the empty state instead.
- [HIG] Tabs do not overflow into a More tab in the default configuration. The HIG gives no fixed maximum count.
- [HIG] The system tab bar, toolbar, and navigation containers are used rather than hand-built replicas, so
  the interface keeps system behaviour (adaptation on iPad, glass appearance, accessibility).
- [HIG] Toolbar titles are short (the HIG suggests under 15 characters) and do not repeat the app name.
- [HIG] Every modal presentation has an obvious way to dismiss it. Sheets that change data offer both a
  confirming and a cancelling action.
- [HIG] Alerts are for important, actionable situations: not for routine information, not at launch, and not
  for actions that can be undone. An alert has a title, optional message, and at most three buttons.
- [HIG] Alert button titles are specific verbs; the button that cancels is titled Cancel; a destructive action
  is styled as destructive and is not the default.
- [HIG] A resizable sheet shows a grabber.
- [HIG] A choice that follows a person's action (for example confirming a deletion) uses an action sheet or
  confirmation dialog rather than an alert with many buttons.
- [HIG] On iPad, a phone layout is not simply stretched: use the available width (sidebar-adaptable tab bar,
  split view, multiple columns), and support the pointer, keyboard, and resizable windows.
- [HIG] On Mac, commands are in the menu bar with standard keyboard shortcuts, windows resize, and app-level
  options live in a Settings window opened from the app menu.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars
Source: https://developer.apple.com/design/human-interface-guidelines/toolbars
Source: https://developer.apple.com/design/human-interface-guidelines/alerts
Source: https://developer.apple.com/design/human-interface-guidelines/sheets
Source: https://developer.apple.com/design/human-interface-guidelines/modality

## Checkable rules: controls, flows, and code

Details: `references/components-controls.md`, `references/patterns-flows.md`,
`references/implementation-availability.md`.

- [HIG] A view has one or two prominent buttons at most, used for the most likely action. A destructive action
  is not given the prominent style.
- [HIG] On iOS, the switch style of toggle appears in list rows.
- [HIG] A segmented control has about five segments or fewer on iPhone and does not mix actions with selection.
- [HIG] Text fields have a visible label or clear placeholder plus the right keyboard and content type;
  passwords use secure fields.
- [Req] An app that lets people create an account must also let them delete it within the app. The HIG states
  this as an obligation.
- [HIG] Permission requests appear in context, when the feature needs them, with a clear purpose string.
- [HIG] Sign-in is delayed until the app needs it.
- [API] No API newer than the minimum OS is used without an availability check and a working fallback.
- [API] Deprecated APIs are replaced where the replacement is available on the minimum OS.
- [Conv] Actions use `Button` (or a system control) rather than a tap gesture on a text, image, or stack, so
  they keep traits, focus, keyboard, and pointer behaviour.

Source: https://developer.apple.com/design/human-interface-guidelines/buttons
Source: https://developer.apple.com/design/human-interface-guidelines/toggles
Source: https://developer.apple.com/design/human-interface-guidelines/segmented-controls
Source: https://developer.apple.com/design/human-interface-guidelines/managing-accounts
Source: https://developer.apple.com/design/human-interface-guidelines/privacy
Source: https://developer.apple.com/documentation/swiftui/button

## Refactoring after a review

- [Conv] Fix what was asked and what is confirmed. Keep names, structure, architecture, and behaviour.
- [Conv] Make the smallest change that resolves a finding: swap a fixed font for a text style on that line;
  do not restyle the view.
- [Conv] List further improvements as optional, with their class and severity, instead of applying them.
- [Conv] When a fix needs an API newer than the minimum OS, add the availability check and keep the old path.
- [Conv] After the change, say what to build and test: the affected screen with VoiceOver, the largest text
  size, Dark Mode, and Increase Contrast.

Source: https://developer.apple.com/design/human-interface-guidelines/design-principles

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Calling every departure from the HIG a "violation" | State the strength: most guidance is recommendation |
| Citing numbers from memory (tab counts, corner radii, button heights) | Cite only numbers from a linked Apple page; otherwise say the HIG gives none |
| Reporting unconfirmed lint leads | Read the code around each lead first |
| Judging contrast or point sizes from a screenshot as fact | Report as an estimate and ask for the values |
| Reviewing an iPad, Mac, or Apple Watch screen by iPhone rules | Load the platform file first |
| Redesigning instead of reviewing | Report findings; propose larger changes separately and label them |
| Predicting App Review results | Say the HIG is not the App Review Guidelines |
| Twenty low-value findings burying two serious ones | Order by severity and cut the noise |
