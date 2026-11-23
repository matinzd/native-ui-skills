---
name: apple-hig
description: Apple Human Interface Guidelines (HIG) expertise for designing, implementing, reviewing, and adapting native user interfaces on iOS, iPadOS, macOS, watchOS, tvOS, and visionOS. Use when a question or task concerns how an Apple-platform interface should look, behave, or be built in SwiftUI, UIKit, or AppKit, even if the HIG is not mentioned. Covers making a screen feel native; choosing between tabs, sidebars, toolbars, sheets, popovers, full-screen covers, alerts, and menus; layout, typography, Dynamic Type, SF Symbols, color, Dark Mode, and Liquid Glass; accessibility such as VoiceOver, contrast, and hit targets; reviewing code or screenshots for HIG compliance; fixing an iPad or Mac app that looks like a stretched iPhone app; and adapting designs across iPhone, iPad, Mac, Apple Watch, Apple TV, and Apple Vision Pro. Consult it before answering from memory, because Apple's guidance and APIs changed in OS 26 and 27. Not for web, Android, Flutter, or React Native styling, or non-UI Swift code.
license: MIT
metadata:
  author: matinzd
  version: "0.1.0"
  short-description: Apple HIG guidance for SwiftUI, UIKit and AppKit UI work
---

# Apple Human Interface Guidelines

Help design, build, review, and adapt interfaces that behave the way people expect on each Apple platform.
This skill is an independent, paraphrased guide with links to Apple's pages. It is not Apple documentation, and
Apple's own pages win whenever they disagree with it.

## Ground rules

These exist because HIG folklore is widespread and often wrong or outdated.

1. **Use only what you can source.** State an API, number, or guideline only if it appears in this skill's
   references or you verified it in Apple's documentation during the task. Otherwise say it is unverified and
   give the page to check. Never invent a modifier, a point size, or a "HIG rule".
2. **Say how strong each rule is.** Most of the HIG is recommendation ("prefer", "avoid", "consider"). Reference
   files tag each rule bullet: `[Req]` something Apple states as mandatory, `[HIG]` HIG recommendation, `[API]`
   documentation or platform fact (availability, deprecation, "not supported on this platform"), `[Conv]`
   convention, interpretation, or this skill's own working rule that Apple does not state, `[Unverified]`. Carry
   that strength into your answer; do not turn a recommendation into a violation.
3. **Respect the deployment target.** Do not use an API newer than the project's minimum OS without an
   availability check and a fallback. A deprecated API is still correct in a fallback branch for older systems.
4. **Prefer system components.** Standard controls bring accessibility, localization, Dark Mode, Dynamic Type,
   input-method support and the current system appearance for free. Customize only for a stated product reason.
5. **Platforms differ.** Do not copy iPhone chrome to iPad, Mac, Apple Watch, Apple TV, or Apple Vision Pro.
6. **Accessibility is part of every task**, not a separate pass.
7. **Do not predict App Review outcomes.** The HIG is not the App Review Guidelines.
8. **The user decides.** When the user or a brand wants something the HIG only discourages, explain the
   trade-off once, then do it well. Push back firmly only on `[Req]` items and accessibility barriers.

## Step 1: Establish platform, minimum OS, and framework

Do this before giving advice, because the right answer changes with each.

- Take them from the user's message if stated. Otherwise inspect the project: `Package.swift` `platforms:`,
  `*_DEPLOYMENT_TARGET`, `SUPPORTED_PLATFORMS` and `TARGETED_DEVICE_FAMILY` in `project.pbxproj`, `#if os(...)`
  blocks, and imports (`SwiftUI`, `UIKit`, `AppKit`, `WatchKit`, `RealityKit`). Details and commands:
  `references/platforms-detection.md`.
- If still unknown and the answer depends on it, ask one short question. If it barely matters, proceed, write
  for iOS 17, macOS 14, tvOS 17, watchOS 10, or visionOS 1, gate anything newer, and state the assumption in one
  line (for example "Assuming iPhone, iOS 17+, SwiftUI").
- Version numbers are year-aligned since 2025: iOS 18 was followed by iOS 26, then iOS 27, and the other
  platforms use the same numbers. "OS 26" in this skill means that generation on every platform.
- Match the project's framework. Do not rewrite UIKit or AppKit code in SwiftUI unless asked.

## Step 2: Identify the task and follow its workflow

| Task | Workflow |
|------|----------|
| Design (no code yet) | Clarify content and goals. Choose the navigation structure, then the presentations, then the controls (the `components-*` files), checked against the platform file. Give the structure per platform, the reason for each choice with its source, and the accessibility implications. |
| Implement | Pick system components first. Pair the `components-*` file for the design rule with the `implementation-*` file for the API, and start from the closest example. Write code for the stated minimum OS, with availability checks for newer APIs. Use text styles, semantic colors, SF Symbols, and safe-area-aware layout. Add labels for anything VoiceOver cannot infer. |
| Review | Follow `references/review-guide.md`. Report findings in the format below. Review what exists; do not redesign. |
| Refactor | Change only what the request and the confirmed findings require. Keep behavior, naming, and structure. List other improvements as optional instead of applying them. |
| Accessibility audit | Use `references/accessibility-guidelines.md` and `references/accessibility-implementation.md`. Cover vision, mobility, hearing, and cognition, not only labels. |
| Cross-platform adaptation | Use `references/platforms-adaptation.md` plus the target platform's file. Keep content and identity; rebuild navigation, input, and density for the target. |

## Step 3: Load only the references you need

Budget: a quick factual question needs zero or one file (check the tables below first); one screen needs two or
three; adaptation needs the target platform file plus the adaptation playbook. Never load every platform file.

| Need | Read |
|------|------|
| Platform and minimum-OS detection; what is universal versus platform-specific | `references/platforms-detection.md` |
| iPhone conventions, including the foldable iPhone Duo | `references/platforms-ios.md` |
| iPad: top tab bar and sidebar, windows, pointer, keyboard, menu bar | `references/platforms-ipados.md` |
| Mac: menu bar, windows, keyboard, density, Settings, Mac Catalyst | `references/platforms-macos.md` |
| Apple Watch | `references/platforms-watchos.md` |
| Apple TV: focus, remote, 10-foot layout | `references/platforms-tvos.md` |
| Apple Vision Pro: windows, volumes, spaces, eyes and hands | `references/platforms-visionos.md` |
| Moving a design from one platform to another | `references/platforms-adaptation.md` |
| Design principles; resolving trade-offs; branding | `references/foundations-design-principles.md` |
| Safe areas, margins, size classes, hierarchy, right-to-left | `references/foundations-layout.md` |
| Text styles, sizes, Dynamic Type, custom fonts | `references/foundations-typography.md` |
| Color, contrast, Dark Mode, materials, Liquid Glass | `references/foundations-color-materials.md` |
| SF Symbols, interface icons, app icons, images | `references/foundations-icons-images.md` |
| Motion, haptics, interface copy, privacy prompts | `references/foundations-motion-writing.md` |
| Tab bars, sidebars, toolbars and titles, split views, search fields and their placement | `references/components-navigation.md` |
| Sheets, alerts, action sheets, popovers, menus | `references/components-presentation.md` |
| Buttons, toggles, pickers, sliders, text fields, progress | `references/components-controls.md` |
| Lists, tables, collections, scroll views, empty states, widgets | `references/components-content.md` |
| Launch, onboarding, loading, settings, data entry, accounts, search behavior | `references/patterns-flows.md` |
| Feedback, undo, drag and drop, gestures, keyboard, pointer, focus | `references/patterns-interaction.md` |
| Accessibility guidance and audit checklist | `references/accessibility-guidelines.md` |
| Accessibility APIs and testing | `references/accessibility-implementation.md` |
| SwiftUI navigation, tabs, toolbars, search, presentations | `references/implementation-navigation.md` |
| Size classes, adaptive stacks and grids, safe areas, scenes and windows, menu commands and keyboard shortcuts, per-platform input APIs (hover, focus, Digital Crown) | `references/implementation-adaptive-layout.md` |
| Fonts, Dynamic Type, colors, symbols, materials and glass in code | `references/implementation-styling.md` |
| Buttons, forms, lists, pickers, menus, haptic feedback, share and photo pickers, empty states in code | `references/implementation-controls.md` |
| API availability, deprecated APIs and their replacements, version gating | `references/implementation-availability.md` |
| UIKit and AppKit equivalents | `references/implementation-uikit-appkit.md` |
| Review procedure, severity, checkable rules | `references/review-guide.md` |

Worked examples to adapt (state the minimum OS when you reuse one):

| Example | File |
|---------|------|
| Navigation that adapts between compact and regular widths | `examples/AdaptiveNavigation.swift` |
| Tab-based app root with an older-OS fallback | `examples/TabRoot.swift` |
| Settings form built from system controls | `examples/SettingsForm.swift` |
| List row that survives large text sizes, with search and an empty state | `examples/AccessibleList.swift` |
| Sheets, alerts, and a destructive confirmation | `examples/Presentations.swift` |
| Custom control with full accessibility and Reduce Motion support | `examples/AccessibleCustomControl.swift` |
| Mac app scenes: commands, keyboard shortcuts, Settings window | `examples/MacAppScenes.swift` |
| A complete review report | `examples/review-report.md` |

To scan Swift files for common, mechanically detectable problems before a review, run `scripts/hig_lint.py`
with Python 3, giving the script's absolute path (it sits in this skill's directory, next to this file) and the
path to scan, for example `python3 /path/to/apple-hig/scripts/hig_lint.py Sources`. It uses only the standard
library; `--help` lists options and known blind spots. Its output is a list of leads to confirm by reading the
code, not a verdict.

## Numbers Apple publishes

Both tables are recommendations from the HIG Accessibility page (verified 2026-11-23). The Dark Mode page
adds, for custom colors, a floor of 4.5:1 and a target of 7:1, especially for small text.

| Platform | Control size, default | Control size, minimum | Text size, default | Text size, minimum |
|----------|-----------------------|-----------------------|--------------------|--------------------|
| iOS, iPadOS | 44x44 pt | 28x28 pt | 17 pt | 11 pt |
| macOS | 28x28 pt | 20x20 pt | 13 pt | 10 pt |
| tvOS | 66x66 pt | 56x56 pt | 29 pt | 23 pt |
| visionOS | 60x60 pt | 28x28 pt | 17 pt | 12 pt |
| watchOS | 44x44 pt | 28x28 pt | 16 pt | 12 pt |

| Text | Minimum contrast |
|------|------------------|
| Up to 17 pt, any weight | 4.5:1 |
| 18 pt, any weight | 3:1 |
| Bold, any size | 3:1 |

The contrast table's second row reads "18 pts" in the HIG; reading it as "18 pt and larger" is the usual
interpretation, not Apple's wording. Aim for the default control size and treat the minimum as a floor for dense
layouts, not a target. The Buttons page separately asks for a hit region of at least 44x44 pt (60x60 pt in
visionOS); the HIG does not reconcile the two, so keep tappable regions at the default size. Source:
https://developer.apple.com/design/human-interface-guidelines/accessibility

## Outdated or invented lore to avoid

- **No fixed tab count.** The HIG says to avoid overflowing into a More tab, and suggests five or fewer default
  tabs only for customizable tab bars. Do not cite "maximum five tabs" as a rule.
- **44 pt is the default control size on iPhone, iPad, and Apple Watch, not a universal hard minimum.** See the table above.
- **There is no "navigation bars" HIG page.** That guidance lives in Toolbars.
- **On iPad, the tab bar sits near the top of the screen** and can adapt into a sidebar. Start from tabs, not a sidebar.
- **Liquid Glass (OS 26 and later) belongs to the navigation and control layer**, not to content. Standard bars
  and controls adopt it automatically. The glass effect and glass button style APIs (`glassEffect`,
  `GlassEffectContainer`, `buttonStyle(.glass)`) list no visionOS availability; visionOS has its own glass
  material. An `#available(iOS 26, *)` check passes on visionOS, so also wrap those calls in
  `#if !os(visionOS)` when the file builds for it.
- **Dark Mode is not a setting on watchOS or visionOS; Dynamic Type is not available on macOS.**
- **The design principles changed in 2026.** Read `references/foundations-design-principles.md` instead of
  quoting "clarity, deference, depth".
- **The HIG gives no** universal button height, card corner radius, spacing grid, or sheet animation duration.
  If asked for one, say so and offer the system default instead.
- **Many SwiftUI deprecations are recent and carry no meaningful version.** Say "deprecated, use X" and check
  `references/implementation-availability.md` rather than quoting a version from memory.

## Review output format

Classify every finding as exactly one of:

| Class | Use when |
|-------|----------|
| Confirmed guideline or API violation | The code uses an API that is unavailable on the minimum OS, or a deprecated API whose replacement is available on it; or it breaks something Apple states as mandatory (tagged `[Req]` in the references). |
| Accessibility issue | A person using an assistive setting or technology is blocked or disadvantaged. |
| Platform convention mismatch | It works, but differs from what people expect on this platform. |
| Recommended improvement | It departs from a HIG recommendation you can link; nothing is broken. Most HIG findings belong here. |
| Subjective design suggestion | Your judgment. No source required; say that it is opinion. |

Severity: **High** blocks a task, excludes people, or will not build or run on the target. **Medium** causes
friction or inconsistency that people will notice. **Low** is polish. Order findings by severity. A finding with
no source can only be a subjective design suggestion.

```markdown
## HIG review: <screen or file>
Target: <platform(s)>, minimum OS <version or "assumed ...">, <framework>

### 1. <short title>
- Class: <one of the five>
- Severity: High | Medium | Low
- Where: <file:line or element>
- Why: <one or two sentences on the effect for people>
- Source: <Apple URL> (<requirement | recommendation | API documentation>)
- Fix: <concrete change, with code when short>

### Not verified
- <claim>: <why it could not be confirmed>. Check: <URL>

### What already works
- <one to three things worth keeping>
```

Group repeated instances of the same problem into a single finding, but keep different problems separate even
when one fix resolves several of them. Keep fixes minimal. A full example is in
`examples/review-report.md`.

## Verifying and reporting uncertainty

- Each reference section ends with a `Source:` link and each file states when it was verified. Cite the Apple
  URL in your answer, not this skill.
- What the references state is already verified; do not fetch Apple's pages to re-confirm it. Check online only
  when the answer depends on something this skill does not cover, and try once: if the fetch fails, say the
  point is unverified and move on.
- To check a claim, fetch the JSON behind Apple's pages (the human pages are rendered by JavaScript):
  `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json` for a HIG page and
  `https://developer.apple.com/tutorials/data/documentation/<framework>/<symbol>.json` for an API, where
  `metadata.platforms` lists `introducedAt` and deprecation for each platform.
- If you cannot verify something, say so plainly: what is unverified, why, and where to check. Do not fill the
  gap with a plausible number or API name.
- Code in this skill was checked against Apple's documentation but was not compiled.
  Tell the user to build it, and to test with VoiceOver, the largest text size, Dark Mode, and Increase Contrast.
