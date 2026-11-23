# Review guide

How to review an existing Android interface (Compose code, XML layout, screenshot, or description) and report findings.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive, Compose Material 3 1.5).

## Contents

- Procedure
- What evidence allows which claims
- Choosing the class
- Choosing the severity
- Checkable rules: accessibility
- Checkable rules: theme, color, type, and layout
- Checkable rules: navigation and presentation
- Checkable rules: controls, system behaviour, and code
- Refactoring after a review
- Common mistakes

## Procedure

1. Establish the form factor, minSdk and targetSdk, the toolkit (Compose or Views), and the library versions
   (`references/platforms-detection.md`). State any assumption at the top of the report.
2. Read the whole screen before judging parts of it: what is the content, what is the main task, how does a
   person get in and out, and what happens on Back.
3. Walk the checkable rules below in order, opening a linked reference only where something looks off. The
   rules assume a phone unless they name a breakpoint: for other form factors load that form factor's file first.
4. Before reporting an API finding, check the name against the project's library version
   (`references/implementation-availability.md`): deprecated, experimental, or absent.
5. Write findings in the format given in `SKILL.md`: class, severity, where, why, source, fix. Group repeated
   instances into one finding and list the locations.
6. Finish with what could not be verified and what already works. Do not pad the report: five findings that
   matter are more useful than twenty.

## What evidence allows which claims

| Evidence | You can assess | You cannot assess |
|----------|----------------|-------------------|
| Compose source | Components used, API availability, deprecation and opt-ins, theme use, text units, semantics, inset and Back handling | Rendered contrast of theme colors, real sizes after layout, how it feels |
| XML layout | Widgets, attributes, hard-coded colors and sizes, text units, hints, content descriptions set in XML | Anything set in code (state, tints, listeners, descriptions), what the theme attributes resolve to |
| Screenshot | Hierarchy, density, visible labels, component choice, approximate sizes and contrast | Content descriptions, font scaling, dark theme, insets on other devices, interaction, exact dp values |
| Description | Structure and component choice | Almost everything visual |

- [Conv] Say which kind of evidence you had. Sizes and contrast read from a screenshot are estimates: report
  them as "appears to be" and ask for the value or the code.
- [Conv] Contrast can be computed only when both colors are literal values. A theme role pair (for example
  on surface on surface) is designed to pass; a hard-coded color on a theme color cannot be judged from code.
- [Conv] A claim about behaviour at a large font size, in dark theme, with TalkBack, or in a resized window needs
  the code or a test. If you have neither, list it under "Not verified" with what to test.

## Choosing the class

Use exactly one class per finding. Ask the questions in order and stop at the first yes.

| Question | Class |
|----------|-------|
| Does it use an API that does not exist in the project's library version, or a deprecated API whose replacement is available in it, or break something Google states as mandatory (tagged `[Req]`)? | Confirmed guideline or API violation |
| Is a person using an assistive setting or technology blocked or disadvantaged? | Accessibility issue |
| Does it work but differ from what people expect on Android or on this form factor? | Platform convention mismatch |
| Does it depart from a Material or Android design recommendation you can link, though nothing is broken? | Recommended improvement |
| Is it your judgment, with no source? | Subjective design suggestion |

- [Conv] When a problem is both an accessibility barrier and a Material statement, class it as an accessibility
  issue and cite the page; the effect on people matters more than the label.
- [Conv] "Confirmed" means you can link the statement or the API entry. Material "Don't" captions and "should"
  sentences are recommendations, so name the strength in the Source line: requirement, recommendation, or API
  documentation.
- [Conv] A deprecated API is a violation only as "deprecated, replacement available in this library version".
  If the replacement needs a newer version than the project uses, it is not a finding.
- [Conv] Behaviour the platform changes by targetSdk (edge-to-edge, Back delivery, orientation on large screens)
  is a fact to state with the API level. Class the finding by its effect: content hidden under a system bar
  is a convention mismatch or worse, not a "violation of edge-to-edge".
- [Conv] Core app quality items (48dp targets, contrast, dark theme) are a published minimum that apps "should
  meet", not `[Req]`. Patterns carried over from iOS that Material does not mention are convention mismatches.

## Choosing the severity

| Severity | Meaning | Typical examples |
|----------|---------|------------------|
| High | Blocks a task, excludes people, or does not build or run on the target | Icon button with no content description; composable that does not exist in the project's Material 3 version; content or a button hidden under a system bar; text that cannot scale; essential state shown by color alone |
| Medium | Friction or inconsistency people will notice | Navigation bar with six destinations; dialog used for a routine message; hard-coded colors that break in dark theme; Back intercepted when nothing needs saving; switch whose label is a separate, untappable text |
| Low | Polish | Deprecated composable with a drop-in replacement; all-caps button label; third action in a dialog |

- [Conv] Rank accessibility barriers and code that does not build above convention mismatches, then taste.
- [Conv] Lower the severity when the evidence is weak (an estimate from a screenshot) and say so.

## Checkable rules: accessibility

Details: `references/accessibility-guidelines.md` and `references/accessibility-implementation.md`.

- [MD] Every interactive element has a touch target of at least 48x48dp, even when the visible element is
  smaller (a 24dp icon inside a 48dp target). [Conv] Report a smaller target as an accessibility issue.
- [API] Compose enlarges the touch area of a small clickable element but does not reserve layout space for it,
  so neighbouring touch areas can overlap. Check for a minimum size of 48dp, or
  `Modifier.minimumInteractiveComponentSize()` placed before any size modifier.
- [MD] Adjacent targets are separated by 8dp or more in most cases.
- [MD] Text contrast is at least 4.5:1 for small text and 3:1 for large text (18 and up, or 14 and up when
  bold; one Android page gives these in pt, another in sp) and for graphics and non-text elements.
- [MD] Icon-only controls and meaningful images have a content description that states the purpose and does
  not include the control type ("button"); decorative images pass `null`.
- [API] A custom control built with `Modifier.clickable` takes its role and click label from the `role` and
  `onClickLabel` parameters. A switch, checkbox, or radio button with a text label is one element: put
  `toggleable` or `selectable` on the parent row and pass `null` as the control's own callback.
- [MD] Color is never the only cue for state, selection, or validity; add text, a shape, or an icon. A text
  field in error shows error text, and Material strongly recommends an error icon as well.
- [MD] Text sizes are in sp, and the interface supports text enlarged to 200% without losing content.
  [Conv] A fixed height on a container that holds text is a lead: check that it can grow.
- [MD] An action reachable by a gesture (swipe on a list item, dragging a sheet) also has a single-tap
  alternative such as a button, a menu item, or an accessibility action.

Source: https://m3.material.io/foundations/designing/structure, https://m3.material.io/foundations/designing/elements, https://m3.material.io/foundations/writing/text-resizing
Source: https://m3.material.io/components/text-fields/guidelines, https://m3.material.io/components/lists/accessibility, https://m3.material.io/components/bottom-sheets/accessibility
Source: https://developer.android.com/design/ui/mobile/guides/foundations/accessibility, https://developer.android.com/guide/topics/ui/accessibility/principles, https://developer.android.com/guide/topics/ui/accessibility/apps
Source: https://developer.android.com/develop/ui/compose/accessibility/api-defaults, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Checkable rules: theme, color, type, and layout

Details: `references/foundations-color.md`, `references/foundations-typography.md`,
`references/foundations-layout.md`, `references/implementation-theming.md`, `references/platforms-system.md`.

- [MD] Colors come from the theme (`MaterialTheme.colorScheme` in Compose, theme attributes in Views), not
  from hard-coded values. Report hard-coded text and background colors as a recommended improvement, and as an
  accessibility issue when you can show that contrast fails.
- [MD] Color roles are applied in their intended pairs (primary with on primary, surface with on surface).
- [MD] The app supports both light and dark themes; core app quality lists this as a minimum.
- [API] `dynamicLightColorScheme` and `dynamicDarkColorScheme` require API 31. With a lower minSdk they need
  a version check and a static color scheme as the fallback.
- [MD] Font sizes are always in sp. [Conv] Prefer the theme's type styles (`MaterialTheme.typography`) over
  one-off sizes.
- [MD] The content of a `Scaffold` applies the `PaddingValues` it is given, so bars do not cover it.
- [API] An app targeting API 35 is edge-to-edge by default on Android 15, and an app targeting API 36 cannot
  opt out on Android 16, so content must handle insets. `setStatusBarColor` and `statusBarColor` are
  deprecated and have no effect on Android 15.
- [MD] No tap or drag targets sit under the system gesture insets.
- [MD] Layout changes with the window width breakpoint (600, 840, 1200, 1600dp), not with the device type or
  orientation; window size classes are not meant for "is tablet" logic.
- [API] For an app targeting API 36, orientation, resizability, and aspect ratio restrictions no longer apply
  on displays whose smallest width is 600dp or more.
- [MD] Product text is sentence case; avoid blocks of capitals.

Source: https://m3.material.io/styles/color/roles, https://m3.material.io/foundations/content-design/style-guide/grammar-and-punctuation
Source: https://developer.android.com/develop/ui/compose/designsystems/material3, https://developer.android.com/develop/ui/views/theming/darktheme, https://developer.android.com/docs/quality-guidelines/core-app-quality
Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/grids-and-units, https://developer.android.com/develop/ui/compose/components/scaffold, https://developer.android.com/about/versions/15/behavior-changes-15
Source: https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge, https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes

## Checkable rules: navigation and presentation

Details: `references/components-navigation.md`, `references/components-presentation.md`,
`references/platforms-large-screens.md`.

- [MD] A navigation bar has three to five destinations. For fewer than three use tabs; for more than five do
  not use a navigation bar.
- [MD] Navigation bars are for compact and medium breakpoints only; from expanded up use a navigation rail.
  A compact window uses a navigation bar, not a standard navigation rail.
- [MD] A navigation bar and a navigation rail are never shown together, and a toolbar at the bottom of the
  window is not shown at the same time as a navigation bar.
- [MD] Every navigation item keeps its text label, which is not wrapped or truncated. Material asks for one
  or two words and publishes no character limit.
- [MD] A collapsed navigation rail has three to seven items and is not hidden.
- [MD] The navigation drawer is no longer recommended (Material 3 Expressive); new work uses the expanded
  navigation rail. An existing drawer is not a violation.
- [MD] A dialog is for critical information or a decision that needs an answer. Low- and medium-priority
  information belongs in a snackbar.
- [MD] A dialog has at most two actions: a single action only as an acknowledgement, otherwise one confirming
  and one dismissing action with the confirming one nearest the trailing edge. A third action such as "Learn
  more" is not recommended.
- [MD] A dialog headline is a brief, specific statement or question, not "Are you sure?".
- [MD] Full-screen dialogs are for compact breakpoints only; from medium up use a basic dialog.
- [MD] Only one snackbar shows at a time, with at most one action, shown as a text button. A snackbar with an
  action does not dismiss by itself, and a snackbar is not the only way to reach a core function. Material
  gives a 4 to 10 second range for snackbars without actions, not one duration.
- [MD] The Up button never exits the app; it does not appear on the start destination.

Source: https://m3.material.io/components/navigation-bar/guidelines, https://m3.material.io/components/navigation-rail/guidelines, https://m3.material.io/components/toolbars/guidelines
Source: https://m3.material.io/components/navigation-drawer/overview, https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/snackbar/guidelines
Source: https://m3.material.io/components/snackbar/accessibility, https://developer.android.com/guide/navigation/principles

## Checkable rules: controls, system behaviour, and code

Details: `references/components-controls.md`, `references/implementation-availability.md`,
`references/implementation-navigation.md`, `references/platforms-system.md`, `references/platforms-quality.md`.

- [MD] A screen has one FAB at most, for its most important action. A FAB is not used for minor or destructive
  actions and is not shown disabled: when its action is unavailable it does not appear.
- [MD] Filled buttons mark the most important actions. Button labels are sentence case, on one line, never
  truncated, and ideally one to three words.
- [MD] Every text field has a label that stays visible. Error text replaces the supporting text instead of
  being added below it. [Conv] A placeholder alone is not a label, because it disappears on input.
- [MD] A switch is for a setting that takes effect immediately, without a save step. Use checkboxes to
  select several related options in a list.
- [MD] Material 2 (`androidx.compose.material`) and Material 3 composables are not mixed in one app long-term.
  A phased migration is the advised route, so report mixing as a recommended improvement.
- [API] Deprecated composables are replaced where the replacement exists in the project's version: `Divider`
  (`HorizontalDivider`), `TabRow` (`PrimaryTabRow` or `SecondaryTabRow`), `LinearProgressIndicator` with a
  `Float` progress (the lambda overload), and in material3 1.5 `ListItem(headlineContent = ...)` and
  `Slider(value = ...)`.
- [API] Names that are absent from Material 3, such as `SmallTopAppBar`, `BottomNavigation`, or a `Scaffold`
  with `scaffoldState`, do not compile. Report them with the Material 3 name (`TopAppBar`, `NavigationBar`).
- [API] Experimental APIs need an opt-in. In material3 1.5 `ModalBottomSheet` and `TooltipBox` are
  `@ExperimentalMaterial3Api` and `LoadingIndicator` is `@ExperimentalMaterial3ExpressiveApi`. A fix must not
  use an API that the project's library version lacks.
- [API] For an app targeting API 36 on Android 16, `onBackPressed` is not called and `KEYCODE_BACK` is not
  dispatched. Custom Back handling uses `BackHandler`, `PredictiveBackHandler`, or `OnBackPressedCallback`.
- [MD] A Back callback is enabled only while the interface state needs it (for example, a form with unsaved
  input) and is not used for logging or business logic.
- [Req] From 31 August 2026, new apps and updates submitted to Google Play must target API 36 or higher (API
  35 for Wear OS and Android Automotive OS, API 34 for Android TV and Android XR). This is the only rule in
  this file that concerns Play, and it says nothing about design review.

Source: https://m3.material.io/components/floating-action-button/guidelines, https://m3.material.io/components/floating-action-button/accessibility, https://m3.material.io/components/buttons/guidelines
Source: https://m3.material.io/components/text-fields/guidelines, https://m3.material.io/components/switch/guidelines
Source: https://developer.android.com/develop/ui/compose/designsystems/material2-material3, https://developer.android.com/jetpack/androidx/releases/compose-material3, https://developer.android.com/about/versions/16/behavior-changes-16
Source: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture, https://developer.android.com/google/play/requirements/target-sdk

## Refactoring after a review

- [Conv] Fix what was asked and what is confirmed. Keep names, structure, architecture, toolkit, and behaviour.
- [Conv] Make the smallest change that resolves a finding: swap one hard-coded color for a theme role on that
  line; do not restyle the screen or migrate it to another component set.
- [Conv] List further improvements as optional, with their class and severity, instead of applying them.
- [Conv] Write fixes for the project's library versions. Mark every experimental opt-in, and guard platform
  features with an API-level check that keeps the old path.
- [Conv] After the change, say what to build and test: the affected screen with TalkBack, the largest font
  size, dark theme, gesture and three-button navigation, and a resized or unfolded window.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Calling every departure from Material a "violation" | State the strength: "Don't" captions and "should" are recommendations |
| Citing numbers Material does not publish (minimum font size, FAB edge margin, one snackbar duration, a label character limit) | Cite only numbers from a linked page; otherwise say Material gives none |
| Reporting a deprecated API on a library version that lacks the replacement | Check the project's version first |
| Reviewing a tablet, foldable, watch, TV, or car screen by phone rules | Load the form factor's file first and review against the window size, not the device |
| Copying iOS conventions (a tab bar's rules, Cancel and Done placement, an in-app back button on every screen) | Review against Android navigation, system Back, and Material components |
| Judging contrast or dp sizes from a screenshot as fact | Report as an estimate and ask for the values |
| Treating Material 2 guidance or old component names as current | Map the old name to the current component and check the current page |
| Redesigning instead of reviewing | Report findings; propose larger changes separately and label them |
| Predicting Google Play review results | Say that design guidance is not Play policy; only the target API rule is a Play requirement here |
| Twenty low-value findings burying two serious ones | Order by severity and cut the noise |
