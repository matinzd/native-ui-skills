# Wear OS

Scope: designing and reviewing Wear OS apps: what a watch app is for, surfaces (app, tile, widget, complication, notification), round-screen layout and sizes, the Wear Material 3 Expressive library, navigation and scrolling, inputs, colour and type, the Wear OS quality requirements (stated by Google as required for publishing), and which phone conventions do not apply.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Principles
- Choose the surface
- Library and scaffolding
- Round-screen layout and sizes
- Navigation, Back and scrolling
- Inputs
- Colour and theme
- Typography
- Tiles, widgets and complications
- Quality requirements
- What does not apply
- Common mistakes

## Principles

- [MD] Design for critical tasks only. Do not port the phone app: pick the few tasks that suit the wrist and let people finish them within seconds.
- [MD] Keep the hierarchy shallow (no deeper than two levels) and linear, with most content and navigation shown inline.
- [MD] Expect offline and poor-connectivity use (exercise, commuting without the phone); keep content relevant to time, place and activity.
- [MD] Use haptics to confirm actions such as start, stop and auto-pause; consider touch lock during workouts.
- [MD] A watch fitness app mostly gathers data; leave detailed analysis to the phone app.
- [API] Wear OS 6 is based on Android 16 (API 36). Compose for Wear OS runs on Wear OS 3 (API 30) and on Wear OS 2 devices at API 25+.

Source: https://developer.android.com/training/wearables/principles, https://developer.android.com/training/wearables/wear-v-mobile, https://developer.android.com/training/wearables/versions/6/changes, https://developer.android.com/training/wearables/compose

## Choose the surface

| Surface | Use it for | Built with |
|---|---|---|
| Complication | One piece of data on the watch face (for a weather app: the current conditions) | Complication data source; the watch face decides rendering |
| Notification | A timely event the user should know about | Standard notifications; ongoing work pairs with `OngoingActivity` |
| Tile | The one or two most needed facts or actions, read in a few seconds | ProtoLayout and tiles libraries, not Compose |
| Wear Widget | Successor format to tiles in small (2x1) and large (2x2) cards | Jetpack Glance and Remote Compose |
| App | The fuller flow when more interaction is needed | Compose for Wear OS |

- [MD] Decide per task which surface answers it fastest, and send the user into the app only when more action is required.
- [API] Tiles are reached by swiping from the watch face; a tile itself cannot scroll.

Source: https://developer.android.com/training/wearables/principles, https://developer.android.com/training/wearables/tiles, https://developer.android.com/training/wearables/widgets, https://developer.android.com/training/wearables/complications

## Library and scaffolding

- [API] Compose for Wear OS is Google's recommended way to build watch UI. Artifacts: `androidx.wear.compose:compose-material3` instead of the phone `material3`; `androidx.wear.compose:compose-navigation` instead of `navigation-compose`; `androidx.wear.compose:compose-foundation` in addition to Compose foundation. Stable line 1.7.2.
- [API] Do not mix phone Compose Material with Wear Compose Material: each has its own `MaterialTheme`, so colours, type and shapes drift apart. Component names collide (`androidx.wear.compose.material3.Button` versus `androidx.compose.material3.Button`): check imports.
- [API] Material 3 Expressive is the current design system for the watch. The older Material 2.5 library is `androidx.wear.compose:compose-material`; the migration guide says to stop using the Horologist composables, layout and material libraries and use the Material 3 components instead.
- [API] Structure: `AppScaffold` at the top (owns the time text and coordinates transitions), `ScreenScaffold` per screen (scroll indicator slot, computes percentage-based content padding), `TransformingLazyColumn` for lists, `EdgeButton` as the round-screen bottom action (four sizes), `SwipeDismissableNavHost` for navigation.
- [API] Wear `MaterialTheme` takes a `ColorScheme`, `Typography`, `Shapes` and `MotionScheme`; `dynamicColorScheme(context)` returns the system-derived scheme or null, so supply brand colours as fallback.
- [Conv] If Google's Android skill for Wear Compose Material 3 (`wear-compose-m3` in android/skills) is installed, prefer it for migration and implementation steps; use this file for design and review rules.

Source: https://developer.android.com/training/wearables/compose, https://developer.android.com/training/wearables/compose/migrate-to-material3, https://developer.android.com/design/ui/wear/guides/get-started, https://developer.android.com/jetpack/androidx/releases/wear-compose

## Round-screen layout and sizes

- [MD] Design small first: for the small round emulator at 204dp to 216dp. Check dense layouts at 192dp, also with larger font sizes, then optimise for bigger screens.
- [MD] Define top, bottom and side margins as percentages of the screen so they follow the curve and nothing clips; keep spacing between elements in fixed dp.
- [MD] Use 225dp as the breakpoint between smaller screens (192dp to 224dp) and larger ones (225dp to 240dp and above) to add content, buttons or glanceability.
- [MD] A larger screen must never show less than a smaller one, including after custom breakpoint behaviour.
- [MD] Non-scrolling screens: let the middle content stretch to fill the available height; components fill the available width.
- [MD] Three design quality tiers for screens: ready for all screen sizes, responsive and optimized, adaptive and differentiated.
- [API] In Compose, pass the `contentPadding` that `ScreenScaffold` supplies into `TransformingLazyColumn`; test on the Wear OS small round (192dp) and large round (227dp) emulators named by the quality page.

Source: https://developer.android.com/design/ui/wear/guides/foundations/adaptive-design, https://developer.android.com/training/wearables/compose/screen-size, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Navigation, Back and scrolling

- [API] Back is swipe to dismiss: swiping from left to right closes the current screen and moves down the back stack. Activities support it automatically; in Compose use `SwipeDismissableNavHost`. Pressing the power button returns to the watch face.
- [Req] Users can swipe to close from almost all screens (`WO-V3`). Exempt: ongoing fitness activities and panning screens such as an interactive map, which must offer a clear close action instead.
- [MD] Scroll in one direction only: vertical layouts; do not combine vertical and horizontal scrolling.
- [MD] Show the time at the top of screens, not on brief dialogs, confirmations or pickers.
- [MD] Put a clear primary action near the top rather than at the end of a long page; show all entry points inline with icon and label, including settings.
- [Req] Display the scroll indicator while the user interacts with a scrollable view (`WO-V8`). [MD] Do not show it on non-scrolling screens.
- [API] Dialogs in Wear Material 3 (`AlertDialog`, `ConfirmationDialog`, `OpenOnPhoneDialog`) are full-screen overlays with their own animations and swipe-to-dismiss. Declare them inside the screen that opens them, driven by a visibility state, not as separate navigation destinations.
- [API] App resume: users can return to recent apps with a hardware-button shortcut; the app must remember scroll position. [Req] Preserve state when leaving the foreground (`WO-V5`).
- [Req] Long-running work the user started (workout, navigation, playback) is surfaced with an `OngoingActivity` or a Live Update notification (`WO-V4`).

Source: https://developer.android.com/training/wearables/views/exit, https://developer.android.com/training/wearables/compose/navigation, https://developer.android.com/design/ui/wear/guides/surfaces/apps/best-practices, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Inputs

| Input | Notes | Tag |
|---|---|---|
| Touch | Primary input; small screen | [API] |
| Rotary (rotating side button, crown or bezel) | Scrolls the current view. Support it for all essential interactions and give visual feedback. Scrolling lists placed in `AppScaffold` / `ScreenScaffold` handle it by default | [MD] |
| Physical buttons | Always at least the power button; some watches add multifunction buttons | [API] |
| Voice and IME | Text entry through voice, emoji, canned responses and small on-screen keyboards, launched with the `RemoteInput` API. Prefer speech for messaging | [API] |
| One-handed gestures (Wear OS 7) | Two types: primary action and dismiss action; on Pixel Watch mapped to double pinch and wrist turn. Map one main task per screen to the primary action | [API] |

- [API] Rotary support was removed from the quality requirements in February 2024 (`WO-V7` retired); it remains a recommendation.

Source: https://developer.android.com/training/wearables/wear-v-mobile, https://developer.android.com/training/wearables/compose/rotary-input, https://developer.android.com/training/wearables/user-input/wear-ime, https://developer.android.com/design/ui/wear/guides/patterns/gestures, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Colour and theme

- [API] Wear OS provides only a dark theme; the interface is built on a black background.
- [Req] Use a black background for all apps and tiles (`WO-V13`).
- [API] Dynamic colour on the watch derives a scheme from two seed colours defined by the watch face (primary and tertiary palettes) and is applied to system UI, tiles and apps that opted in.
- [MD] Design against the baseline scheme first so roles map correctly, then check with other seed colours; or derive the scheme from a brand colour.
- [MD] The watch palette is more limited than on phones because fewer hover and focus states are needed; use the Wear-specific colour roles.

Source: https://developer.android.com/design/ui/wear/guides/styles/color/system, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Typography

- [API] The Wear Material 3 Expressive type scale has 21 styles (display, title, label, body, numeral, arc) and defaults to Roboto Flex. Arc styles are for curved text such as the time.
- [API] The user-configurable font size moves styles in steps of plus or minus 6%. Styles of 20sp and larger do not scale: display and numeral styles never scale, `LabelLarge` does not, the title, body, arc and smaller label styles do. (On the type-scale page the scaling notes under Body and Arc name each other's style; read them as applying to both.)
- [Req] Honour the user's font size without overlap or clipping (`WO-V1`); minimum 12sp for essential text and 10sp for non-essential text (`WO-V14`).
- [MD] Element heights change non-linearly with font scaling and bold text; test at the largest setting on the smallest screen. With auto-sizing text set explicit minimum and maximum sizes.
- [MD] Use tabular or monospaced numerals where digits change or scroll (timers, pickers).

Source: https://developer.android.com/design/ui/wear/guides/styles/typography/type-scale-tokens, https://developer.android.com/design/ui/wear/guides/styles/typography/accessibility, https://developer.android.com/training/wearables/accessibility, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Tiles, widgets and complications

- [MD] A tile shows a small amount of key information that can be read in a few seconds; do not overcrowd it. Tapping leads to another surface for more.
- [API] Tiles are declared with ProtoLayout and rendered remotely by the system, so the app does not control final rendering; do no long-running work in the tile service (cache results, schedule background work).
- [Req] A tile shown to a signed-out user prompts sign-in when opened (`WO-V9`); every tile ships a preview for the tile manager (`WO-V10`).
- [API] Wear Widgets are the announced next step after tiles: Glance plus Remote Compose, small and large cards matching the 2x1 and 2x2 phone formats. A tile's main slot content can be adapted to the 2x2 widget.
- [API] A complication data source supplies typed data (for example `SHORT_TEXT`, `LONG_TEXT`, `RANGED_VALUE`, `SMALL_IMAGE`); the watch face chooses how to draw it. Offer the types that fit the data.
- [Req] Watch faces built with the Watch Face Format have at most 8 complication slots (`WO-P10`) and an always-on mode that lights at most 15% of pixels (`WO-P7`).

Source: https://developer.android.com/training/wearables/tiles, https://developer.android.com/training/wearables/widgets, https://developer.android.com/training/wearables/complications, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Quality requirements

The Wear OS quality page words these as requirements: a watch app "must satisfy all the applicable requirements" to publish, and failing them "might lead to rejection". IDs most relevant to UI:

| ID | Requirement |
|---|---|
| `WO-V1` | Conform to the user's font size; no overlap, no clipping at screen edges |
| `WO-V2` | Touch targets of at least 48x48dp |
| `WO-V3` | Swipe to close from almost all screens (exceptions above) |
| `WO-V4` | `OngoingActivity` or Live Update for long-running operations |
| `WO-V5` | Preserve and restore state |
| `WO-V6` | Correct icon and name in the app launcher |
| `WO-V8` | Scroll bar shown during interaction with scrollable views |
| `WO-V9`, `WO-V10` | Tile signed-out state; tile preview |
| `WO-V13` | Black background for apps and tiles |
| `WO-V14` | 12sp minimum essential text, 10sp non-essential |
| `WO-V15` | Splash: 48x48dp app icon on black, matching the launcher icon |
| `WO-V16` | Content fits the physical display, no overlap or clipping, on a circle of 192dp or larger |
| `WO-P1` | Meets Google Play's target API level |
| `WO-P6` | Never ask for a username or password typed on the watch |
| `WO-G7` | Same package name and signing key as the accompanying phone app |

- [API] Retired IDs: `WO-V7` (rotary), `WO-V11` (show the time in apps), `WO-P4`, `WO-P9`.
- [API] Dated items on the same page: Watch Face Format required since January 2026; 64-bit support since 2026-09-15.
- [API] Contradiction: that page's target-SDK paragraph still cites API 34 from 2025-08-31, while the Google Play target API page requires API 35 for Wear OS from 2026-08-31. `WO-P1` defers to Google Play's requirement, so use 35.
- [Conv] Report a violation as "Wear OS quality requirement WO-xx"; do not predict the review outcome.

Source: https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/google/play/requirements/target-sdk

## What does not apply

- [API] Light theme and light/dark switching: dark only.
- [Conv] Phone navigation containers (navigation bar, rail, drawer, top app bar with Up arrow) and floating action buttons: Wear uses inline lists, `EdgeButton` and swipe to dismiss.
- [Conv] Window size classes, panes, multi-window and desktop input: the watch has its own size guidance (192dp to 240dp and above, 225dp breakpoint).
- [API] `android.webkit` APIs are not supported on Wear OS.
- [Req] Typed credential entry (`WO-P6`): authenticate through the phone or other documented options.
- [Conv] Phone `androidx.compose.material3` components and phone `navigation-compose`.

Source: https://developer.android.com/training/wearables/wear-v-mobile, https://developer.android.com/docs/quality-guidelines/wear-app-quality

## Common mistakes

| Mistake | Fix |
|---|---|
| Phone screens shrunk to the watch, three or more levels deep | Critical tasks only, at most two levels, inline navigation |
| Fixed-dp outer margins clipping on the curve | Percentage margins; `ScreenScaffold` content padding |
| Coloured, grey or light backgrounds | Black background (`WO-V13`) |
| On-screen back or close button on every screen, swipe disabled | Swipe to dismiss; explicit close only where swipe is exempt |
| `androidx.compose.material3` or `navigation-compose` in the wear module | Wear `compose-material3` and `compose-navigation` |
| Horologist or Material 2.5 scaffolds in new code | `AppScaffold`, `ScreenScaffold`, `TransformingLazyColumn` |
| Dialog added as a navigation destination | Dialog composable inside the screen, driven by state |
| Login form with username and password | Phone-assisted or token-based sign-in (`WO-P6`) |
| Text below 12sp to fit more | Fewer items; essential text at 12sp or more |
| Tile crammed like an app screen | One glanceable purpose; tap through to the app |
| Larger watch shows less after a breakpoint | Only add content at 225dp and above |
| Calling rotary input a requirement | Recommended; `WO-V7` was retired |
