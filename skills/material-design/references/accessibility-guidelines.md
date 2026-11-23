# Accessibility guidelines (design side)

Scope: what Material Design and Android design guidance ask of a design for vision, mobility, hearing and cognition, with the exact numbers and the strength of each statement; semantics APIs, touch target APIs and testing tools are in `references/accessibility-implementation.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How strong these rules are
- Touch and pointer targets
- Contrast
- Color independence
- Text scaling
- Truncation and large type
- Structure and headings
- Focus order and keyboard
- TalkBack labels and content descriptions
- Gestures and alternative actions
- Motion and flashing
- Time limits
- Captions and media
- Per-form-factor notes
- Accessibility review checklist
- Common mistakes

## How strong these rules are

- [MD] Almost everything here is recommendation. Material phrases the 48dp target as "consider"; Android's design page says "ensure"; the Android accessibility guide says "we recommend". Report a miss as an accessibility issue or recommended improvement with the figure and source, not as a rule violation.
- [API] Three items also appear in Android's core app quality guidelines, which the page describes as the minimum quality all apps should meet: Touch_Target_Size (48dp), Visual_Contrast (3:1 and 4.5:1) and Content_Description. The page does not say that Google Play rejects apps that miss them. See `references/platforms-quality.md`.
- [Req] Where the 48dp target is worded as a requirement: Wear OS quality (WO-V2, a minimum of 48x48dp) and widget quality (WL-4.2, the minimum widget size must meet the 48x48dp touch target requirement).
- [API] Material says its accessibility framework draws on WCAG and industry practice, and treats WCAG minimums as a starting point. It does not claim that following Material yields WCAG conformance.
- [MD] Prefer standard platform controls and Material components: they carry the markup, roles, states and target sizing assistive technology needs. Non-standard elements (the example is a custom dialog doing a standard dialog's job) need extra testing.
- [MD] Assistive technologies to design and test for: TalkBack (screen reader, also drives braille displays), Switch Access, Voice Access, keyboards and D-pads, magnification. Android also names Accessibility Scanner for automated checks.

Source: https://m3.material.io/foundations/overview/principles , https://m3.material.io/foundations/designing/overview , https://m3.material.io/foundations/overview/assistive-technology , https://developer.android.com/docs/quality-guidelines/core-app-quality , https://developer.android.com/docs/quality-guidelines/wear-app-quality , https://developer.android.com/develop/adaptive-apps/quality-guidelines/widget-quality , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility

## Touch and pointer targets

| Target | Figure | Wording and source |
|--------|--------|--------------------|
| Touch target | at least 48x48dp | Material: "consider" for most platforms; about 9mm physical, within a recommended 7-10mm. Android design: ensure all touch targets are at least 48dp even if this extends past the visual. Android accessibility guide: recommended, and larger is better |
| Icon in a target | 24dp icon inside a 48dp target | Material: symbols of 24dp should have a 48dp target by default |
| Pointer target | at least 44x44dp | Material: "consider" |
| Pointer, dense | 20dp symbol in a 40dp target | Material: allowed when mouse and keyboard are the primary inputs |
| Spacing | 8dp or more between targets | Material: "in most cases" |
| State layer | 40dp visual inside the 48dp target | Material spec |

- [MD] The target may extend beyond the visible bounds; the visual can stay small. Material components do this for interactive elements.
- [MD] Android's desktop guidance: pointer targets can be smaller than the standard 48x48dp touch target for cursor-specific interactions such as an action that appears on hover. It gives no minimum figure.
- [MD] Density: do not apply component scaling by default if it brings a target under 48x48; dense layouts are opt-in, and the settings that control density keep default target sizes. See `references/foundations-layout.md`.
- [MD] Larger targets than 48dp may be appropriate to serve more people. XR asks for 56x56dp targets.
- [API] Material's page notes that iOS recommends 44x44 targets; do not carry 44 over to Android touch UI.
- [Conv] Adjacent 48dp targets may touch; the 8dp spacing figure is given for "most cases" and is shown between icon targets. Do not report a row of standard icon buttons as a violation.

Source: https://m3.material.io/foundations/designing/structure , https://m3.material.io/styles/icons/applying-icons , https://m3.material.io/foundations/interaction/states/state-layers , https://m3.material.io/foundations/layout/grids-spacing/density , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://developer.android.com/guide/topics/ui/accessibility/apps , https://developer.android.com/design/ui/desktop/guides/interaction/pointer-interactions

## Contrast

| Content | Minimum ratio | Source wording |
|---------|---------------|----------------|
| Small text | 4.5:1 | Material, citing the W3C; Android "we recommend" |
| Large text | 3:1 | Material: 14pt bold or 18pt regular and up. Android guide: text that is not smaller than 18sp, or bold and not smaller than 14sp. Core quality: 18pt, or 14pt bold |
| Graphics and essential non-text elements | 3:1 | Material groups graphics with large text; Android design: 3:1 between surfaces and non-text elements, such as an icon on its background |
| Clustered component containers (a group of buttons) | 3:1 container against background | Material "should" |
| Standalone prominent element (a FAB) | no container minimum | Material: does not need 3:1 against the background |
| Boundary of a target with nothing contrasting inside | 3:1 | Material color roles: use outline, not outline variant |
| Disabled states | exempt | Material |
| Decorative parts of an image | exempt | Material |

- [API] The large-text threshold is written in pt on the Material page and the core quality page, and in sp on the Android accessibility guide. The numbers are the same; the units differ between Google's pages.
- [MD] Android's design page states the simpler pair: text to background at least 4.5:1, and 3:1 between surfaces and non-text elements.
- [MD] Use color roles in their intended pairs; "on" roles are designed to contrast with their partner, and wrong pairs fail when the user raises the contrast level. See `references/foundations-color.md`.
- [API] Material color roles support three user contrast levels: standard, medium (a 3:1 minimum) and high (7:1 on essential elements). A static scheme is listed as not offering user-controlled contrast.
- [Req] Icons in a navigation bar must have at least 3:1 against the container (component page wording); see `references/components-navigation.md`.

Source: https://m3.material.io/foundations/designing/color-contrast , https://m3.material.io/styles/color/roles , https://m3.material.io/styles/color/system/how-the-system-works , https://m3.material.io/foundations/writing/best-practices , https://developer.android.com/guide/topics/ui/accessibility/apps , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://developer.android.com/docs/quality-guidelines/core-app-quality

## Color independence

- [MD] Do not let color be the only cue. Android: distinguish elements with shape, size, text, patterns, or audio and haptic feedback in addition to color.
- [MD] Use more than one visual affordance for actions such as links (Android design). [Req] Material states that hyperlinked text must also be underlined.
- [MD] Material states have two visual indicators for accessibility; a focused element shows a state layer plus a ring-like focus indicator.
- [MD] Text fields in error: an error icon is strongly recommended as a second indicator next to the error color.
- [MD] Do not replace colors with conventional meaning (error red, positive green) with dynamic content-based color.
- [MD] Color meanings vary by culture; red is not a warning color everywhere.

Source: https://developer.android.com/guide/topics/ui/accessibility/principles , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://m3.material.io/foundations/interaction/states/overview , https://m3.material.io/components/text-fields/guidelines , https://m3.material.io/styles/color/advanced/apply-colors , https://m3.material.io/styles/icons/applying-icons

## Text scaling

- [MD] UIs should support a text increase of at least 200% (Material).
- [API] Android 14 and later scales fonts up to 200% with a non-linear curve, so already-large text grows less than small text. Android says to test with the maximum font size.
- [MD] Specify text in sp so the user's font size applies; do not use sp for padding (Android).
- [MD] Android design: do not make body text smaller than 12sp.
- [API] How Material components respond: text size and line height scale; padding and the spacing between elements stay at 1x; components without text (checkboxes, radio buttons, progress indicators) do not grow.
- [MD] Spacing tokens keep the same values when text is scaled to 200%.
- [MD] Remedies when enlarged text does not fit: grow the container, reflow (stack buttons that sat side by side), scroll in one direction (vertical preferred), or, for top app bars, navigation bars, navigation rails and fixed tabs, keep the label at 1x and show the enlarged text in a touch-and-hold tooltip.
- [MD] If the app controls text size itself, offer multipliers such as 1.5x and 2x.

Source: https://m3.material.io/foundations/writing/text-resizing , https://m3.material.io/styles/spacing/applying-spacing , https://developer.android.com/about/versions/14/features , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility

## Truncation and large type

- [Req] Material lists this under "Requirements" with must wording: content, understandability and functionality are not lost when people change their type settings. It allows for exceptions in non-Latin scripts.
- [MD] Wrap text when it is critical or when there is room. If it still does not fit, provide a way to see the rest.
- [MD] Do not cut text off without a way to read it. An ellipsis with no route to the full text is called not accessible; a tooltip or a link that reveals the text makes it acceptable, though Material notes this still adds difficulty for some people.
- [MD] Let component containers change size with their content; avoid size limits that do not use the available space.
- [MD] Translation and taller scripts cause the same failures as large type; see `references/foundations-typography.md`.

Source: https://m3.material.io/foundations/writing/text-truncation , https://m3.material.io/foundations/writing/text-resizing

## Structure and headings

- [MD] Keep a clear hierarchy: visible elements, sufficient contrast and size, key information discernible at a glance, related items of similar rank placed together.
- [MD] Place important actions at the top or bottom of the screen, where shortcuts reach them.
- [MD] Screen readers linearize the screen. Agree the reading order with developers so that it follows the intended order of the content, not only the visual arrangement.
- [MD] Identify headings by content hierarchy, not by visual styling, and do not skip levels. Material's numbered heading levels and its eight landmark roles are stated for web only.
- [MD] On Android, mark heading elements as headings so screen reader users can jump between them, and group related elements so they are announced as one unit (Android guidance).
- [MD] Give each visually distinct pane a unique, descriptive title for accessibility services; generic repeated titles such as "List" or "Details" cause unpredictable TalkBack behaviour.
- [MD] Consider granularity: grouping lets people skip between blocks of content and actions.

Source: https://m3.material.io/foundations/designing/structure , https://developer.android.com/guide/topics/ui/accessibility/principles , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility

## Focus order and keyboard

- [MD] People should be able to use the app without touch or a mouse: Tab moves between interactive elements (Shift+Tab reverses), arrow keys move within a component, Enter activates.
- [MD] Use the default focus order unless a journey needs tailoring. Material describes the default as following source order, generally left to right and top to bottom.
- [Req] Material's inputs page uses must wording: focus on interactive items follows a logical order when navigating with Tab.
- [MD] Define initial focus for each screen and for components with several interactive parts (a complex card, a dialog).
- [MD] Dialogs and other modals: focus moves into the component, typically to a specific element; on close it returns to the element that opened it. A modal that opened automatically returns focus to the next logical element.
- [MD] Multi-pane layouts: focus order matches the visual arrangement of panes; a non-modal floating pane stays reachable in reading order.
- [MD] A group of related controls may be one Tab stop with arrow keys moving inside it.
- [MD] Show a visible focus indicator on the focused element. Only one element is focused at a time; disabled components cannot take focus.
- [MD] Keyboard shortcuts should use two or more keys by default, and custom shortcuts should be documented. A single-key shortcut needs a way to remap it (most preferred), to limit it to when the relevant component has focus, or to turn it off (least preferred).
- [MD] Escape dismisses visible modal elements such as menus, dialogs and bottom sheets. Hide the virtual keyboard when a physical keyboard is attached.

Source: https://m3.material.io/foundations/designing/flow , https://m3.material.io/foundations/interaction/inputs , https://m3.material.io/foundations/layout/scaffold/panes , https://m3.material.io/foundations/interaction/states/applying-states

## TalkBack labels and content descriptions

What to label:

- [MD] Interactive icons and buttons with no visible text or too little context (an edit button shown as a pencil); interactive images; visual cues such as progress bars and error handling; meaningful icons such as status icons; meaningful images such as diagrams, substantive photos and illustrations.
- [MD] Text that needs more context: generic links ("Learn more") and generic buttons that repeat on a page (several "Save" buttons).
- [API] Core app quality (Content_Description): describe each UI element except plain text views with a content description.

What not to label, and what to hide:

- [MD] Non-interactive UI text and buttons with sufficient text are read automatically; do not add a second label.
- [MD] Mark decorative icons and images as decorative so they are hidden. Android: give a purely decorative image or icon a null description.
- [MD] An icon inside a labelled control (an icon next to the button's text) is decorative; labelling it too produces a duplicate announcement.

How to word labels:

- [MD] Describe purpose and result, not appearance: "Search", not "magnifying glass"; "Voice search" names the task and the input method.
- [MD] Do not include the control type ("button", "menu"). The role supplies it, and repeating it produces "Submit button button". Assign the correct role to every interactive element.
- [MD] Keep labels concise: they should describe the element's content, purpose and behaviour in few words.
- [MD] Make each description unique; items in a list each get a label reflecting their own content (the Android example is the city name in a list of locations).
- [MD] For a touch-and-hold or other non-obvious action, give the action a meaningful label, so TalkBack announces what it does instead of a generic hint.
- [MD] Text fields: a visible label describing the expected input; hint text may show an example.
- [MD] Image alt text length and wording: `references/foundations-icons-writing.md` (Material's pages give both 125 and 140 characters).

Source: https://m3.material.io/foundations/designing/elements , https://m3.material.io/foundations/writing/best-practices , https://developer.android.com/guide/topics/ui/accessibility/apps , https://developer.android.com/guide/topics/ui/accessibility/principles , https://developer.android.com/docs/quality-guidelines/core-app-quality

## Gestures and alternative actions

- [MD] Do not rely on gestures to complete actions. Every flow needs a path for TalkBack, Voice Access and Switch Access users; Android's example pairs swipe-to-delete with a visible delete button, and asks for accessibility actions for drag and swipe interactions.
- [MD] Desktop: every drag-and-drop action has a single-click alternative; hover is never the only way to reach an action; zoom has dedicated plus and minus buttons; refresh has a dedicated button.
- [MD] Carousels on desktop need a single-pointer alternative to scroll gestures.
- [MD] Consider haptic feedback as an additional, real-time channel (Android design).
- [MD] XR: actions achievable with one hand, voice or eye control; do not require two-handed gestures.

Source: https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://developer.android.com/guide/topics/ui/accessibility/principles , https://m3.material.io/foundations/desktop/interaction , https://m3.material.io/foundations/desktop/components , https://m3.material.io/foundations/xr/design/accessibility

## Motion and flashing

- [MD] Follow the platform's reduced animation setting. With it on, transitions should use subtle fades instead of strong sliding or scaling, and decorative effects such as parallax and shape morphing should be disabled.
- [MD] Carousel with reduced motion: no parallax, items do not expand as they enter, all items the same size.
- [MD] Avoid content that pops in or shifts position while loading; use skeleton loaders. Avoid jump cuts as a default.
- [MD] Keep common transitions simple, without overt effects such as bouncy springs.
- [Unverified] No flashing threshold was found on the Material foundations and styles pages or the Android accessibility pages read for this file. Do not quote a flashes-per-second rule as Material or Android guidance; cite WCAG directly if the project follows it.

Source: https://m3.material.io/styles/motion/transitions/applying-transitions , https://m3.material.io/components/carousel/accessibility

## Time limits

- [MD] Snackbars with an action should not auto-dismiss, so people can read and act at their own pace.
- [MD] Snackbars without an action may auto-dismiss after enough time to read them; Material gives 4-10 seconds as common acceptable durations and says each platform has its own requirements.
- [MD] Information in an auto-dismissing snackbar must also be available inline or near the trigger (Material's example changes a "Save" button's label to "Saved"). Material states this for web, where it calls auto-dismissing snackbars inaccessible without it.
- [Conv] Apply the same inline-feedback rule on Android: a message that disappears on a timer should never be the only place a result is shown.
- [MD] Notifications that reference relative time ("today") go stale; see `references/foundations-icons-writing.md`.
- [Unverified] No general rule on session timeouts or extendable time limits was found on the Material or Android pages read for this file.

Source: https://m3.material.io/components/snackbar/accessibility , https://m3.material.io/components/snackbar/guidelines

## Captions and media

- [MD] Media content (Android guidance, worded as "try to"): include controls to pause or stop, change the volume and toggle subtitles (captions); when a video carries information vital to a workflow, provide the same content in another format such as a transcript.
- [MD] Captions under images help everyone; alt text should not repeat them.
- [MD] Informative animations and GIFs get alt text; long-form video uses video description instead.
- [MD] Android TV quality lists audio descriptions, subtitle display with preferred styles, a high-contrast mode and adjustable playback speed as enhanced accessibility at its highest tier; see `references/platforms-tv.md`.

Source: https://developer.android.com/guide/topics/ui/accessibility/principles , https://m3.material.io/foundations/writing/best-practices , https://m3.material.io/foundations/content-design/alt-text , https://developer.android.com/docs/quality-guidelines/tv-app-quality

## Per-form-factor notes

| Form factor | Accessibility specifics | More |
|-------------|-------------------------|------|
| Phone | 48dp targets, sp text, test at maximum font size, TalkBack and Switch Access | this file |
| Tablet, foldable | limit interactions in the top 25% of the screen and avoid essential controls at the very bottom edge (medium breakpoint reachability); adaptive quality Tier 2 repeats the 48dp target | `references/platforms-large-screens.md` |
| Desktop window | pointer targets 44dp (20dp icon in 40dp when pointer-first); hover and focus states; keyboard access to everything; context menu on secondary click; single-click alternatives to drag | `references/platforms-large-screens.md` |
| Wear OS | required wording: 48x48dp minimum targets (WO-V2) and conforming to the user's font size without overlap or clipping (WO-V1); test all font sizes and bold text | `references/platforms-wear.md` |
| TV | no touch; focus-driven with a D-pad; evaluate with TalkBack without looking at the screen | `references/platforms-tv.md` |
| XR | targets 56x56dp or larger with a 48x48dp or larger visual and a 4dp offset; no overlapping targets; body text at least 14dp; high contrast against passthrough; seated, standing and reclined use | `references/platforms-auto-xr.md` |
| Cars | host-rendered templates with their own contrast requirements | `references/platforms-auto-xr.md` |

Source: https://m3.material.io/foundations/layout/breakpoints/medium , https://m3.material.io/foundations/designing/structure , https://m3.material.io/foundations/desktop/interaction , https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2 , https://developer.android.com/docs/quality-guidelines/wear-app-quality , https://m3.material.io/foundations/watches/layout , https://m3.material.io/foundations/xr/design/accessibility , https://developer.android.com/training/tv/accessibility/talkback

## Accessibility review checklist

Each item names the section that holds the figure and source. Tags show the strength to carry into a finding.

1. [MD] Every interactive element has a touch target of at least 48x48dp, even when the visual is smaller. (Touch and pointer targets)
2. [MD] Icon-only controls use a 24dp icon in a 48dp target; pointer-first dense UIs go no lower than 20dp in 40dp. (Touch and pointer targets)
3. [MD] Density or compact variants are opt-in and never reduce default targets below 48dp. (Touch and pointer targets)
4. [MD] Small text reaches 4.5:1 and large text 3:1 against its background, in light and dark theme. (Contrast)
5. [MD] Meaningful icons, graphics, clustered component containers and target boundaries reach 3:1. (Contrast)
6. [MD] Colors come from role pairs (X with on X), so user contrast levels keep working. (Contrast)
7. [MD] No information, state or error is conveyed by color alone; links are underlined; error fields show an icon and text. (Color independence)
8. [MD] Text sizes are in sp and the layout holds at 200% font scale. (Text scaling)
9. [Req] No content or function is lost at large text: no clipped or overlapping text. (Truncation and large type)
10. [MD] Truncated text has a way to be read in full; fixed-height text containers are absent. (Truncation and large type)
11. [MD] Padding and spacing do not scale with font size; text-free controls do not grow. (Text scaling)
12. [MD] Headings are marked as headings and related elements are grouped for a single announcement. (Structure and headings)
13. [MD] Reading and focus order follow the visual and logical order, including across panes. (Focus order and keyboard)
14. [MD] Dialogs, sheets and menus take focus when opened and return it to the trigger when closed. (Focus order and keyboard)
15. [MD] Everything works from a keyboard, with a visible focus indicator; Escape closes modal elements. (Focus order and keyboard)
16. [MD] Every icon-only control and meaningful image has a label; decorative images are hidden. (TalkBack labels and content descriptions)
17. [MD] Labels state purpose, omit the control type, and are unique within a list. (TalkBack labels and content descriptions)
18. [Conv] Selected, checked, expanded and error states reach assistive technology, not only the visuals. (TalkBack labels and content descriptions; `references/accessibility-implementation.md`)
19. [MD] Every swipe, drag, long-press or hover action has a visible or accessibility-action alternative. (Gestures and alternative actions)
20. [MD] The reduced animation setting replaces slides and scaling with fades and removes parallax and shape morph. (Motion and flashing)
21. [MD] Snackbars with actions do not auto-dismiss; auto-dismissing messages are also shown inline. (Time limits)
22. [MD] Media has pause or stop, volume and caption controls; essential video has a transcript or equivalent. (Captions and media)
23. [MD] Standard Material components are used where one exists; custom controls expose role, state and label. (How strong these rules are)
24. [Conv] The screen was checked with TalkBack, at the largest font size, in dark theme and at the target form factor's input method. (How strong these rules are)

Source: https://m3.material.io/foundations/designing/overview , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Calling a 44dp touch target acceptable on Android | 48dp for touch; 44dp is Material's pointer figure and the iOS figure |
| Reporting a 48dp miss as a Play policy violation | It is a recommendation and a core quality guideline; required wording exists only for Wear OS and widgets |
| Shrinking the icon button to the icon's 24dp bounds | Keep the visual; expand the target to 48dp |
| Outline variant as the only border of an empty target | Outline, or another 3:1 color |
| Content description "Search button" or "magnifying glass" | "Search" |
| Describing a decorative image, or an icon inside a labelled button | Hide it from accessibility services |
| Same description on every row's action ("Delete") | Make it specific to the row |
| Fixed heights and one-line truncation at large font sizes | Let containers grow, reflow, or scroll |
| Text in dp so it ignores the font setting | sp |
| Swipe as the only way to delete | Add a visible or accessibility action |
| Focus left behind a closed dialog | Return focus to the trigger |
| Error shown by red color only | Error text plus icon |
| Actionable snackbar that disappears | Keep it until acted on |
| Quoting a Material flashing or timeout rule | None was found; say so and cite WCAG if needed |
