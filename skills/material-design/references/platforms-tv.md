# Android TV and Google TV

Scope: designing and reviewing apps for Android TV OS (Android TV and Google TV devices): the 10-foot context, focus and D-pad navigation, Back, layout numbers including the overscan values that Google's page states inconsistently, colour and type, Compose for TV and the status of Leanback, text input, the TV quality tiers, and which phone conventions do not apply.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Context
- Remote and D-pad navigation
- Focus system
- Back and Home
- Layout numbers
- Layout structures and templates
- Navigation components
- Colour and typography
- Text input, voice and sign-in
- Toolkit: Compose for TV and Leanback
- Manifest essentials
- Quality tiers
- What does not apply
- Common mistakes

## Context

- [MD] TV is about content, viewed from about 3 metres (10 feet), usually leaning back. Complex layouts and controls do not suit it: make text and elements large, or reduce the amount of text.
- [MD] Input is a remote, not touch. The UI must give instant, distinct feedback on every button press.
- [MD] A TV is shared by the household: think about privacy before showing personal information, and offer controls for it.
- [API] Every app built for Android TV runs on Google TV devices; both run Android TV OS.

Source: https://developer.android.com/design/ui/tv/guides/foundations/design-for-tv, https://developer.android.com/training/tv/get-started/google-tv

## Remote and D-pad navigation

- [API] All controllers have a directional pad (up, down, left, right), Select, Home and Back; a microphone button invokes the assistant or voice input where present. Other buttons vary, so nothing may depend on them. Select press-and-hold can show more options.
- [API] The D-pad moves focus from one element to the nearest element in that direction.
- [MD] Every focusable element must be reachable; directions must be straightforward and predictable; in scrolling lists up and down scroll the whole list and every item can be selected.
- [MD] Give each axis one job: for example categories on the vertical axis, items within a category on the horizontal axis. Avoid complex nested hierarchies.
- [MD] If there is no straight path to a control (a search action stranded in a corner), move the control.
- [MD] Get people to content in as few clicks and screens as possible; do not reinvent navigation patterns.
- [API] In Views, focus order can be set explicitly with `nextFocusUp`, `nextFocusDown`, `nextFocusLeft` and `nextFocusRight` when the default nearest-neighbour result is wrong.

Source: https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv, https://developer.android.com/training/tv/get-started/navigation

## Focus system

- [MD] Focus is the key state on TV. Main states are default, focused and pressed (pressed lasts until the button is released), combined with enabled, disabled and selected.
- [MD] Exactly one element is focused at any time. Focusable elements (buttons, cards, list items, custom surfaces) are organised in focusable groups, which can nest, so that navigation is logical.
- [MD] Indicate focus by combining:

| Indicator | Parameters given by the guidance |
|---|---|
| Scale | Element grows when focused; default factors 1.025, 1.05 and 1.1, chosen by element size |
| Border / outline | Outline width, inset from the element, colour |
| Glow | Shadow under the element, level from 2dp to 32dp, colour from image or brand |
| Colour | Background (surface) colour and content colour change |

- [MD] Background colour stays static while surface colour may change on focus; surfaces at elevation levels +1 to +5 are tinted with the primary colour (tonal elevation).
- [MD] Leave room between grid items for the focused item's growth so it does not overlap neighbours.
- [MD] Disabled elements show lower-prominence colour and opacity.
- [Conv] A focus state that differs only by a faint colour change fails at 3 metres: combine at least two indicators for content cards.

Source: https://developer.android.com/design/ui/tv/guides/styles/focus-system, https://developer.android.com/design/ui/tv/guides/styles/layouts

## Back and Home

- [MD] Back goes to the previous destination; pressed repeatedly it ends at the Google TV home or launcher. The start destination is the last screen before the launcher; a splash screen is not part of the back path.
- [MD] With top navigation, Back scrolls to the top and moves focus to the menu. With left navigation, Back opens the side menu and focuses the active item.
- [MD] No exit gating: do not put a confirmation in front of leaving the app, and never trap Back in a loop.
- [MD] Do not draw a back button on screen; the remote has one. If the only visible actions are confirming, destructive or purchase actions, add a Cancel button that returns to the previous destination.
- [MD] Deep links simulate manual navigation: Back from a deep-linked details page goes to the app's home, then the launcher (live-tab direct playback has its own rule, quality ID `TV-DL`).
- [API] Home always returns to the Google TV home or launcher and suspends the app.

Source: https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv

## Layout numbers

| Item | Value | Tag |
|---|---|---|
| Aspect ratio | 16:9, fixed | [API] |
| Design canvas | 960 x 540 at MDPI, where 1px = 1dp; assets prepared for 1080p | [MD] |
| Grid | 12 columns of 52dp, 20dp gutters, 58dp side margins, 4dp vertical spacing between lines | [MD] |
| Card widths in that grid | 1 card 844dp; 2 cards 412dp; 3 cards 268dp; 4 cards 196dp; 5 cards 124dp | [MD] |
| Overscan safe margin | About 5% of each dimension; see below for the conflicting dp values | [MD] |

- [MD] Overscan values: the layouts page gives three different statements. (1) Position elements with "a 5% margin of 48dp" left and right and 27dp top and bottom. (2) Its arithmetic: 960 x 5% = 48dp, 540 x 5% = 27dp "round off to 24dp". (3) "Use a 5% margin layout (58dp on the sides and 28dp on the top and bottom edges)". The 58dp side value matches the grid margin. Google's page is internally inconsistent; this skill does not pick a winner. A safe reading is 58dp sides (grid margin, exceeds 5%) and 27dp or 28dp top and bottom.
- [MD] The same page notes that most modern TVs no longer have overscan issues. The quality rule is the outcome: no text or functionality partially cut off by the screen edges (`TV-OV`).
- [MD] Backgrounds fill the whole screen: do not clip or inset background elements to the safe area; let off-screen items show partially.

Source: https://developer.android.com/design/ui/tv/guides/styles/layouts, https://developer.android.com/docs/quality-guidelines/tv-app-quality

## Layout structures and templates

- [MD] Layout patterns: horizontal stack, vertical stack, grid.
- [MD] Single-pane for content-forward pages; two-pane for hierarchical, task-forward pages. Do not use many panels: it adds cognitive load. Group related content in one panel and align the focus path with reading order; do not bounce attention between panels.
- [MD] Named templates: Browse (rows of content clusters, up/down between rows, left/right within), Left overlay (navigation or actions over content), Right overlay, Center overlay (modal for urgent information or a decision), Bottom overlay (bottom sheet for a mini flow), Actions (title left, options right), Content details, Compilation, Grid, Alert (full-screen message requiring an action).
- [MD] Component guidance exists for buttons, cards, featured carousel, immersive list, lists, navigation drawer and tabs.

Source: https://developer.android.com/design/ui/tv/guides/styles/layouts, https://developer.android.com/design/ui/tv/guides/components

## Navigation components

- [MD] Top-level navigation on TV is either tabs along the top or a navigation drawer on the left.
- [MD] Navigation drawer: has a collapsed state (a rail of icons) and an expanded state (icon plus label), both visible to the user. Standard drawer pushes page content aside when expanded; modal drawer overlays content with a scrim. The top section holds the app logo and can switch profiles or trigger search.
- [API] Compose for TV: `NavigationDrawer`, `ModalNavigationDrawer`, `TabRow` (pill or bar indicator) in `androidx.tv.material3`.

Source: https://developer.android.com/design/ui/tv/guides/components/navigation-drawer, https://developer.android.com/design/ui/tv/guides/components/tabs

## Colour and typography

- [MD] Build from a dark theme for a cinematic experience; the theme builder still generates light and dark schemes from the same tokens.
- [API] Android TV has no wallpaper, so user-generated dynamic colour is not supported. [MD] Use content-based schemes (from posters, album art, hero images) for dynamic colour.
- [MD] Design basic UI in sRGB and test in the Standard picture mode; other modes (such as Vivid) change saturation. Watch for banding in gradients.
- [MD] Use larger type than on other screens. Roboto is the default typeface; the TV type scale has 15 styles. Choose fonts with large counters and sufficient stroke width; avoid thin and decorative fonts; do not use the largest display styles for section headings.
- [MD] Respect the user's text scaling preference and keep the app usable with TalkBack.
- [Unverified] Specific sp sizes for the TV type scale were not extracted for this file; take them from the TV typography page or the `androidx.tv.material3` defaults.

Source: https://developer.android.com/design/ui/tv/guides/styles/color-system, https://developer.android.com/design/ui/tv/guides/foundations/color-on-tv, https://developer.android.com/design/ui/tv/guides/styles/typography, https://developer.android.com/training/tv/accessibility

## Text input, voice and sign-in

- [API] Text entry uses the on-screen Gboard keyboard, which includes speech-to-text without the app requesting the audio permission. It supports a limited set of input types (email, password, text, numeric) and picks the layout from the type declared.
- [MD] Minimise typing. Tier 2 expects voice search (`TV-VS`), voice playback commands through `MediaSession` (`TV-VC`), sign-in with a phone or Google Account (`TV-LI`) and remembered credentials (`TV-LC`).
- [Req] Web content is shown only in `WebView`; the app must not try to launch a browser (`TV-WB`).
- [API] Multitasking on TV is picture-in-picture only (Android 14 APIs); the `TV-I*` quality items restrict what a PiP window may show.

Source: https://developer.android.com/training/tv/get-started/onscreen-keyboard, https://developer.android.com/training/tv/get-started/multitasking, https://developer.android.com/docs/quality-guidelines/tv-app-quality

## Toolkit: Compose for TV and Leanback

- [API] Compose for TV: `androidx.tv:tv-material` (package `androidx.tv.material3`), used instead of `androidx.compose.material3:material3`; works from Android 5.0 (API 21). Stable versions: `tv-material` 1.1.0, `tv-foundation` 1.0.0 (the Compose for TV guide's snippet still shows 1.0.0).
- [API] The Leanback library is deprecated and based on the Material 1 design language; Google points to Compose for TV. Do not start new UI on Leanback.
- [API] The TV-specific lazy layouts in `tv-foundation` are deprecated; the release notes link to the migration guidance.
- [MD] Use the TV versions of components where they exist: they carry the focus indications and sizes described here.

Source: https://developer.android.com/training/tv/playback/compose, https://developer.android.com/training/tv/playback/leanback, https://developer.android.com/jetpack/androidx/releases/tv

## Manifest essentials

- [Req] A launcher activity with `ACTION_MAIN` and category `LEANBACK_LAUNCHER` (`TV-ML`).
- [Req] `android.hardware.touchscreen` declared not required (`TV-MT`); the docs say this is required for the app to count as a TV app on Google Play.
- [API] `android.software.leanback` with `required="false"` when one app serves mobile and TV; `android:banner` on the application or activity.
- [Req] Launcher assets: a 320x180px banner containing the app name and an app icon of at least 160x160px at xhdpi (`TV-LB`, `TV-BN`).

Source: https://developer.android.com/training/tv/get-started/create, https://developer.android.com/docs/quality-guidelines/tv-app-quality

## Quality tiers

The TV quality page defines Tier 3 "TV Ready" as the fundamental requirements to run on Android TV OS devices, Tier 2 "TV Optimized" and Tier 1 "TV Differentiated". Items most relevant to UI:

| Tier | ID | Statement |
|---|---|---|
| 3 | `TV-LO` | Landscape without vertical letterboxing or pillarboxing; only black bars on original-format video |
| 3 | `TV-OV` | No text or functionality partially cut off by the screen edges |
| 3 | `TV-TR` | Fills the screen with a non-transparent background; does not partially obscure other apps |
| 3 | `TV-DP` | All functionality navigable with five-way D-pad controls (unless a game controller is required) |
| 3 | `TV-DM` | No dependence on a Menu button |
| 3 | `TV-DB` | Back button presses lead back to the Android TV home screen |
| 3 | `TV-PS` | `minSdkVersion` of 31 or lower, to cover commonly used TV devices |
| 3 | `TV-PC`, `TV-PP` | D-pad centre pauses and resumes playback, left and right seek; play/pause key toggles playback |
| 3 | `TV-AP`, `TV-AD` | Ads operable with the D-pad; full-screen non-video ads dismissible immediately |
| 3 | `TV-G1`, `TV-G6` | App bundles mandatory; 32- and 64-bit support and 16 KB page size from 2026-08-01 |
| 2 | `TV-4K`, `TV-VS`, `TV-VC`, `TV-LI`, `TV-LC` | High-resolution assets, voice search and commands, easy sign-in |
| 1 | `TV-TO` | Touch and click support for pointer remotes and touchscreens, with hover states |
| 1 | `TV-AX` | Enhanced accessibility: audio descriptions, subtitle styling, high-contrast mode, simplified navigation |

- [API] Google Play's target API floor for Android TV is 34 from 2026-08-31 (`references/platforms-quality.md`).
- [Conv] Cite the ID and tier; do not predict review outcomes.

Source: https://developer.android.com/docs/quality-guidelines/tv-app-quality, https://developer.android.com/google/play/requirements/target-sdk

## What does not apply

- [Conv] Touch-target sizing as the primary affordance: selection is by focus. (Tier 1 adds optional pointer and touch support.)
- [Conv] Bottom navigation bar, navigation rail as on tablets, floating action button, swipe gestures, pull to refresh, edge swipes.
- [MD] On-screen Up or Back arrows.
- [Req] Portrait orientation and letterboxed layouts (`TV-LO`).
- [API] Wallpaper-based dynamic colour.
- [Conv] Window size classes and multi-window layouts: the canvas is fixed at 960 x 540dp; only picture-in-picture exists.
- [Conv] Phone `androidx.compose.material3` components where a `androidx.tv.material3` equivalent exists.

Source: https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv, https://developer.android.com/design/ui/tv/guides/styles/color-system, https://developer.android.com/docs/quality-guidelines/tv-app-quality

## Common mistakes

| Mistake | Fix |
|---|---|
| Phone layout mirrored to the TV | Rebuild around focus rows, grids and a 960 x 540dp canvas |
| Elements that cannot receive focus, or focus that is hard to see | Make every interactive element focusable; scale plus border or glow |
| Focus jumps unpredictably or gets trapped | One job per axis; fix focus order explicitly where needed |
| Back arrow in the top-left corner | Remove; rely on the remote's Back |
| "Are you sure you want to exit?" dialog | No exit gating |
| Text and controls flush to the screen edge | Keep them inside the safe margin; backgrounds still bleed |
| Quoting one overscan number as "the" spec | The page gives 48/27, 24 and 58/28dp; say so |
| Light theme with thin fonts | Dark-first scheme, larger and heavier type |
| Opening links in a browser | `WebView` only (`TV-WB`) |
| Long forms typed with the D-pad | Voice input, phone or Google sign-in |
| New screens on Leanback fragments | Compose for TV (`androidx.tv.material3`) |
| Touch-only widgets (sliders dragged by finger, swipe carousels) | D-pad operable equivalents |
