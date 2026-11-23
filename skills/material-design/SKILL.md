---
name: material-design
description: Material Design 3 and Android design guidance for designing, implementing, reviewing, and adapting native Android user interfaces in Jetpack Compose or Views (Material Components). Use when a question or task concerns how an Android interface should look, behave, or be built, even if Material is not mentioned. Covers making a screen feel native on Android; choosing between navigation bar, navigation rail, drawer, top app bar, tabs, dialogs, bottom sheets, snackbars, and menus; layout and window size classes across phones, foldables, and tablets; color, dynamic color, dark theme, type, and motion; Material 3 Expressive; edge-to-edge, insets, and predictive back; accessibility such as TalkBack, contrast, and touch targets; reviewing Compose or XML code; Material 2 to Material 3 migration; and Wear OS, TV, and cars. Consult it before answering from memory, because Material and Compose APIs changed in 2025 and 2026. Not for Apple platforms, Flutter, web Material libraries, or non-UI Android code.
license: MIT
metadata:
  author: matinzd
  version: "0.1.0"
  short-description: Material Design 3 guidance for Jetpack Compose and Android Views UI work
---

# Material Design 3 and Android design guidance

Help design, build, review, and adapt interfaces that behave the way people expect on Android devices. This
skill is an independent, paraphrased guide with links to Google's pages. It is not Google documentation, and
Google's own pages win whenever they disagree with it.

## Ground rules

These exist because Material folklore is widespread and often describes Material 2 or an older Compose release.

1. **Use only what you can source.** State an API, number, or guideline only if it appears in this skill's
   references or you verified it in the official documentation during the task. Otherwise say it is unverified
   and give the page to check. Never invent a composable, a parameter, a dp value, or a "Material rule".
2. **Say how strong each rule is.** Most Material and Android design guidance is recommendation ("should",
   "consider", "avoid"). Reference files tag each rule bullet: `[Req]` something Google states as mandatory (a
   quality guideline marked required, a Play target-API rule), `[MD]` Material or Android design recommendation,
   `[API]` documentation or platform fact (signature, stability, deprecation, behaviour tied to an API level,
   "not supported on this form factor"), `[Conv]` convention, interpretation, or this skill's own working rule,
   `[Unverified]`. Carry that strength into your answer; do not turn a recommendation into a violation.
3. **Respect the project's versions.** Check minSdk, targetSdk, and the Compose Material 3 version before
   choosing APIs. Do not use an API newer than the project's library version, say when an API is experimental
   and needs an opt-in, and guard platform features with an API-level check. A deprecated API is still correct
   on a library version that lacks the replacement.
4. **Prefer Material components and theme values.** Standard components bring accessibility semantics, touch
   target sizing, state layers, dark theme, dynamic color, and adaptation for free. Read colors, type, and shapes
   from the theme instead of hard-coding them. Customize only for a stated product reason.
5. **Form factors differ.** Do not stretch a phone layout onto a tablet, foldable, desktop window, watch, TV,
   or car display. Adapt to the window size class, not to the device type or orientation.
6. **Android is not iOS.** When a design comes from an Apple platform, rebuild navigation, Back behaviour, and
   system UI for Android instead of copying the chrome.
7. **Accessibility is part of every task**, not a separate pass.
8. **Do not predict Google Play review outcomes.** Design guidance is not Play policy.
9. **The user decides.** When the user or a brand wants something the guidance only discourages, explain the
   trade-off once, then do it well. Push back firmly only on `[Req]` items and accessibility barriers.

## Step 1: Establish form factor, versions, and toolkit

Do this before giving advice, because the right answer changes with each.

- Take them from the user's message if stated. Otherwise inspect the project: `build.gradle(.kts)` and
  `gradle/libs.versions.toml` for `minSdk`, `targetSdk`, `compileSdk`, the Compose BOM, `androidx.compose.material3`
  (Material 3) versus `androidx.compose.material` (Material 2), and `com.google.android.material` (Views);
  `AndroidManifest.xml` for watch, TV (leanback), and automotive features; theme parents in `themes.xml`. Details
  and commands: `references/platforms-detection.md`.
- If still unknown and the answer depends on it, ask one short question. If it barely matters, proceed, assume a
  phone app in Jetpack Compose with Material 3 on the current stable library line, mark anything experimental,
  and state the assumption in one line.
- Match the project's toolkit. Do not rewrite Views in Compose, or Material 2 in Material 3, unless asked.
- If Google's official Android skills are installed and one covers the task as a migration (for example
  edge-to-edge), use it for the mechanical steps and this skill for the design decisions and review.

## Step 2: Identify the task and follow its workflow

| Task | Workflow |
|------|----------|
| Design (no code yet) | Clarify content and goals. Choose navigation for each window size class, then the presentations, then the controls (the `components-*` files), checked against the form-factor file. Give the structure per size class, the reason for each choice with its source, and the accessibility implications. |
| Implement | Pick Material components first. Pair the `components-*` file for the design rule with the `implementation-*` file for the API, and start from the closest example. Write code for the project's library versions, with opt-ins for experimental APIs. Use theme colors, type styles in sp, and Scaffold insets. Add content descriptions and semantics for anything TalkBack cannot infer. |
| Review | Follow `references/review-guide.md`. Report findings in the format below. Review what exists; do not redesign. |
| Refactor or migrate | Change only what the request and the confirmed findings require. Keep behavior, naming, and structure. List other improvements as optional instead of applying them. |
| Accessibility audit | Use `references/accessibility-guidelines.md` and `references/accessibility-implementation.md`. Cover vision, mobility, hearing, and cognition, not only content descriptions. |
| Adapt to another form factor, or from iOS | Use `references/platforms-adaptation.md` plus the target form factor's file. Keep content and identity; rebuild navigation, input, and density for the target. |

## Step 3: Load only the references you need

Budget: a quick factual question needs zero or one file (check the tables below first); one screen needs two or
three; adaptation needs the target form-factor file plus the adaptation playbook. Never load every platform file.

| Need | Read |
|------|------|
| Detecting form factor, SDK levels, toolkit, and library versions; what is universal versus form-factor-specific | `references/platforms-detection.md` |
| System conventions: edge-to-edge, insets, system bars, Back and predictive back, splash, notifications, permissions | `references/platforms-system.md` |
| Tablets, foldables, desktop windows: window size classes, panes, navigation by size | `references/platforms-large-screens.md` |
| Wear OS | `references/platforms-wear.md` |
| Android TV and Google TV: focus, D-pad, 10-foot layout | `references/platforms-tv.md` |
| Android Auto, Automotive OS, and Android XR | `references/platforms-auto-xr.md` |
| What is required versus recommended: Play target API, core and adaptive app quality | `references/platforms-quality.md` |
| Moving a design to another form factor, or from an iOS design | `references/platforms-adaptation.md` |
| Window size classes, margins, spacing, panes, canonical layouts, right-to-left | `references/foundations-layout.md` |
| Color roles, dynamic color, dark theme, contrast | `references/foundations-color.md` |
| Type scale, sizes, font scaling | `references/foundations-typography.md` |
| Shape, elevation, motion, Material 3 Expressive | `references/foundations-shape-motion.md` |
| Material Symbols, interface copy, capitalization | `references/foundations-icons-writing.md` |
| Navigation bar, rail, drawer, app bars, tabs, search | `references/components-navigation.md` |
| Dialogs, bottom and side sheets, snackbars, menus, tooltips | `references/components-presentation.md` |
| Buttons, FABs, chips, switches, checkboxes, sliders, pickers, text fields | `references/components-controls.md` |
| Cards, lists, carousels, dividers, progress and loading indicators, badges | `references/components-content.md` |
| Accessibility guidance and audit checklist | `references/accessibility-guidelines.md` |
| Compose semantics, touch target APIs, accessibility testing | `references/accessibility-implementation.md` |
| Library versions, stable versus experimental, deprecated APIs and replacements | `references/implementation-availability.md` |
| Theme, color scheme, dynamic color, typography, shapes, icons in code | `references/implementation-theming.md` |
| Scaffold, app bars, navigation components, adaptive scaffolds, Back, insets in code | `references/implementation-navigation.md` |
| Buttons, selection controls, text fields, dialogs, sheets, snackbars, lists in code | `references/implementation-components.md` |
| Views and XML with Material Components for Android | `references/implementation-views.md` |
| Review procedure, severity, checkable rules | `references/review-guide.md` |

Worked examples to adapt (state the library versions and opt-ins when you reuse one):

| Example | File |
|---------|------|
| Top-level navigation that adapts between bar and rail | `examples/AdaptiveNavigation.kt` |
| List and detail that share the screen when there is room | `examples/ListDetail.kt` |
| App theme with dynamic color, a static fallback, and dark theme | `examples/AppTheme.kt` |
| Settings screen built from Material list items and switches | `examples/SettingsScreen.kt` |
| Form with labels, supporting text, errors, and keyboard options | `examples/FormScreen.kt` |
| Dialog, bottom sheet, and snackbar, each used for its purpose | `examples/Feedback.kt` |
| Custom control with full semantics and a 48dp touch target | `examples/AccessibleCustomControl.kt` |
| A complete review report | `examples/review-report.md` |

## Numbers Google publishes

All of these are recommendations unless a reference says otherwise (verified 2026-11-23).

| Window width | Breakpoint | Navigation | Panes |
|--------------|------------|------------|-------|
| Under 600dp | Compact | Navigation bar | One |
| 600 to 839dp | Medium | Navigation bar or navigation rail | One |
| 840 to 1199dp | Expanded | Navigation rail | Up to two |
| 1200 to 1599dp | Large | Navigation rail | Up to two |
| 1600dp and wider | Extra-large | Navigation rail | Up to three |

Material's pages disagree about medium width (the navigation bar page allows a bar or a rail; the navigation
rail and desktop pages say rail) and about pane counts at the largest sizes; `references/foundations-layout.md`
gives each page's wording. Breakpoints describe the window, not the device: the same app is compact in split screen and expanded when
unfolded. Material renamed "window size classes" to "breakpoints" in 2026; the Android libraries still say window
size class.

| Item | Published value |
|------|-----------------|
| Touch target | At least 48x48dp, whatever the visible size; 44x44dp for pointer input |
| Text contrast | 4.5:1 for small text; 3:1 for large text and for graphics |
| Navigation bar | Three to five destinations |
| Navigation rail (collapsed) | Three to seven items |
| Margins | 16dp at compact, 24dp above |
| Dialog | At most two actions |
| Text size unit | sp, so text follows the person's font size setting |

Sources: https://m3.material.io/foundations/layout/breakpoints/overview ,
https://m3.material.io/foundations/designing/structure ,
https://m3.material.io/components/navigation-bar/guidelines ,
https://developer.android.com/docs/quality-guidelines/core-app-quality

## Outdated or invented lore to avoid

- **Names changed.** "Bottom navigation" is the navigation bar; "top app bar" is now app bars; the bottom app bar
  is replaced by the docked toolbar; search bar and search view are one component, search. Map old names
  instead of treating them as different components.
- **Material 3 Expressive is not Material 4**, and it is no longer alpha-only: most Expressive components are
  stable in Compose Material 3 1.5.0. Some APIs people assume are stable are still experimental (modal bottom
  sheets, tooltips, the loading indicator, adaptive pane scaffolds). Check
  `references/implementation-availability.md` instead of guessing.
- **Several familiar components are "no longer recommended"**: the navigation drawer (use the expanded
  navigation rail), segmented buttons (use a connected button group), and the baseline medium and large app bars.
- **The 48dp touch target is a recommendation** in Material and the Android design docs. It is a stated
  requirement only in specific quality guidelines such as Wear OS and widgets.
- **Elevation overlays and surface tint are gone.** Tonal surface container roles replace them.
- **Component motion uses spring-based motion schemes**, not easing-and-duration tokens.
- **Do not set status bar or navigation bar colors, lock orientation on large screens, or override
  `onBackPressed`.** Edge-to-edge, large-screen resizability, and predictive back are platform behaviour tied to
  `targetSdk` 35 and 36; see `references/platforms-system.md`.
- **Compose renames and deprecations are frequent** (`Divider`, `TabRow`, older `ListItem`, `Slider`, and search
  bar overloads; the Material icons library is no longer bundled). Material 2 Compose is deprecated, and the
  Views library is in maintenance mode.
- **Interface text is sentence case.**
- **Material gives no** minimum font size, character limit for navigation labels, single snackbar duration (it
  gives a 4 to 10 second range), FAB edge margin, bottom sheet peek height, or component animation duration. If
  asked for one, say so and offer the component default instead.
- **Google's own pages sometimes disagree with each other** (for example TV overscan values, or prose versus
  token tables). The references report both values; do not pick one silently.

## Review output format

Classify every finding as exactly one of:

| Class | Use when |
|-------|----------|
| Confirmed guideline or API violation | The code uses an API that does not exist in the project's library version, or a deprecated API whose replacement is available in it; or it breaks something Google states as mandatory (tagged `[Req]` in the references). |
| Accessibility issue | A person using an assistive setting or technology is blocked or disadvantaged. |
| Platform convention mismatch | It works, but differs from what people expect on Android or on this form factor. |
| Recommended improvement | It departs from a Material or Android design recommendation you can link; nothing is broken. Most findings belong here. |
| Subjective design suggestion | Your judgment. No source required; say that it is opinion. |

Severity: **High** blocks a task, excludes people, or will not build or run on the target. **Medium** causes
friction or inconsistency that people will notice. **Low** is polish. Order findings by severity. A finding with
no source can only be a subjective design suggestion.

```markdown
## Material review: <screen or file>
Target: <form factor(s)>, minSdk <n> / targetSdk <n>, <Compose Material 3 x.y or Views>, <or "assumed ...">

### 1. <short title>
- Class: <one of the five>
- Severity: High | Medium | Low
- Where: <file:line or element>
- Why: <one or two sentences on the effect for people>
- Source: <official URL> (<requirement | recommendation | API documentation>)
- Fix: <concrete change, with code when short>

### Not verified
- <claim>: <why it could not be confirmed>. Check: <URL>

### What already works
- <one to three things worth keeping>
```

Group repeated instances of the same problem into a single finding, but keep different problems separate even
when one fix resolves several of them. Keep fixes minimal. A full example is in `examples/review-report.md`.

## Verifying and reporting uncertainty

- Each reference section ends with a `Source:` link and each file states when it was verified. Cite the official
  URL in your answer, not this skill.
- What the references state is already verified; do not fetch Google's pages to re-confirm it. Check online only
  when the answer depends on something this skill does not cover, and try once: if the fetch fails, say the
  point is unverified and move on.
- To check a claim: `https://m3.material.io/` pages are rendered by JavaScript, so a plain HTTP fetch returns an
  empty shell and needs a browser. `https://developer.android.com/` pages are plain HTML. Compose Material 3
  signatures, experimental annotations, and deprecations are in the public API file
  `https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/current.txt`
  (the development branch, which is ahead of the latest stable release), and per-version changes are in
  `https://developer.android.com/jetpack/androidx/releases/compose-material3`.
- If you cannot verify something, say so plainly: what is unverified, why, and where to check. Do not fill the
  gap with a plausible number or API name.
- Code in this skill was checked against the androidx API signature files but was not compiled. Tell the user to
  build it, and to test with TalkBack, the largest font size, dark theme, and a resized or unfolded window.
