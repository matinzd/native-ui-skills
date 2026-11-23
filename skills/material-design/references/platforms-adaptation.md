# Cross-form-factor adaptation playbook

Scope: how to take an Android design from one form factor to another: principles, then keep / change / add / remove checklists for phone to tablet and foldable, to desktop windowing, to Wear OS, to Android TV, to cars and to Android XR; and a section for designs that arrive from iOS, stating what has to change on Android from the Android and Material side only.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Principles
- What changes: one-table summary
- Phone to tablet and foldable
- To desktop windowing, ChromeOS and Googlebook
- To Wear OS
- To Android TV
- To cars
- To Android XR
- Coming from an iOS design
- Adaptation review procedure
- Common mistakes

## Principles

- [Conv] Establish the target first (`references/platforms-detection.md`): form factor, `targetSdk`, toolkit and library versions decide which of the moves below are possible.
- [MD] Adaptive is the default. Design content in containers and panes that reflow, reveal or change presentation, so one design system covers windows of any size.
- [Conv] Share content, data, terminology, icons, colour identity and core tasks. Do not share chrome: navigation containers, modality, density, input handling and the component library come from the destination form factor.
- [MD] Core quality asks for a consistent experience across form factors (`Consistent_UX`) and feature parity across orientations and fold states (`Display_State_Parity`).
- [Conv] Scope by context of use. Tablet, desktop and XR versions are usually a superset of the phone app; watch, TV and car versions are a subset built around what people do there (seconds on the wrist, lean-back viewing, glances while driving).
- [MD] Every action needs a path for each input present: touch, keyboard, pointer, D-pad focus, rotary, voice. Gestures alone are never the only route.
- [API] The component library changes with the form factor: `androidx.compose.material3` (phone, tablet, desktop), `androidx.wear.compose.material3` (watch), `androidx.tv.material3` (TV), Car App Library templates (driving), `androidx.xr.compose` with experimental Material 3 for XR (headsets).

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/adapt-layout, https://developer.android.com/docs/quality-guidelines/core-app-quality, https://developer.android.com/design/ui/desktop/guides/foundations/design-principles

## What changes: one-table summary

| From phone | Tablet, foldable | Desktop window | Wear OS | TV | Car (driving) | XR |
|---|---|---|---|---|---|---|
| Bottom navigation bar | Navigation rail | Rail expanding to a panel | Inline list entries, at most two levels | Top tabs or left drawer | Tab template | Rail or bar, optionally in an orbiter |
| Push list to detail | List-detail panes | Panes, several windows | List then detail, swipe back | Rows and grids, details page | List then Pane template | Panels side by side |
| Bottom sheet | Sheet with maximum width, or side sheet | Menus, small modals, side sheet | Full-screen dialog | Overlay panel | Message or Pane template | Keep flat in the panel; spatial dialog for alerts |
| Long-press context menu | Same, plus right-click | Right-click, hover actions | Rare; inline actions | Select press-and-hold | None | Pinch and hold; hover states |
| Software keyboard | Plus hardware keyboard, stylus | Hardware keyboard first | Voice, emoji, canned replies | On-screen keyboard with voice | Voice, Search template | Voice, Bluetooth keyboard |
| 48dp touch targets | 48dp | 48dp touch; smaller pointer targets allowed | 48dp, required | Focus indicators | Host rendered | 56dp recommended |
| Light and dark | Same | Same | Dark only, black | Dark first | Host switches light and dark | Light and dark |
| System Back gesture | Same | Same plus Esc | Swipe to dismiss | Remote Back | Host back | Gesture menu Go back |

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns, https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv, https://developer.android.com/design/ui/cars/guides/templates/overview, https://developer.android.com/design/ui/xr/guides/spatial-ui

## Phone to tablet and foldable

Keep
- [MD] The same destinations, features and state; the compact layout itself, because a tablet window can be compact in split screen.
- [MD] 48dp touch targets, sp text, theme and colour roles.

Change
- [MD] Navigation bar to navigation rail from medium width; keep the bar when the window is compact in width or height. `NavigationSuiteScaffold` does this switch.
- [MD] Push navigation to canonical layouts: list-detail, supporting pane, feed with more columns.
- [MD] Cap widths of buttons, text fields, sheets and dialogs; turn bottom sheets into side sheets where suitable; keep lines at 45 to 75 characters.
- [MD] Per-pane status-bar protection; cutout insets in landscape.

Add
- [MD] State preservation across rotate, fold, unfold and resize, including combinations (scroll position, typed text, playback).
- [MD] Hinge awareness: nothing important across the fold; optional tabletop or book layout.
- [MD] Basic keyboard, mouse, trackpad and stylus support (adaptive Tier 3).

Remove
- [API] `screenOrientation`, `resizeableActivity="false"`, `minAspectRatio`, `maxAspectRatio` and `setRequestedOrientation()` calls: ignored at sw600dp and up from targetSdk 36.
- [MD] Layout branches on device type or orientation; use window size classes.

See `references/platforms-large-screens.md`.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation, https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-3, https://developer.android.com/about/versions/16/behavior-changes-16

## To desktop windowing, ChromeOS and Googlebook

Keep
- [MD] Everything from the tablet step; the app must already be adaptive.

Change
- [MD] Density: show more information instead of scaling up; shorten flows; make small transitions faster and large ones slower or simpler.
- [MD] Context menus on secondary click rather than long-press; drag starts immediately; selection through explicit click targets.
- [MD] Buttons and their targets get a maximum width under a pointer.

Add
- [API] Arbitrary window sizes including very small and extra-large: opt in to the large and extra-large width classes.
- [API] Caption bar insets; optionally draw app content into the window header.
- [MD] Keyboard: Tab and arrow traversal with visible focus, shortcuts for common actions, Esc to dismiss, Enter to send, Spacebar for playback; publish shortcuts in Keyboard Shortcuts Helper.
- [MD] Pointer: hover states and tooltips, scroll wheel, Ctrl plus wheel zoom, scrollbars, custom cursors.
- [MD] Multi-instance windows, drag and drop between windows, file picker and file handlers, printing (adaptive Tier 1, desktop experience).

Remove
- [Conv] Assumptions of full screen, of a single window, of touch as the only input, and device allowlists.

Source: https://developer.android.com/design/ui/desktop/guides/foundations/design-principles, https://developer.android.com/design/ui/desktop/guides/interaction/pointer-interactions, https://developer.android.com/develop/ui/compose/layouts/adaptive/support-desktop-windowing, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/experiences/desktop

## To Wear OS

Keep
- [Conv] Brand colour as a seed, terminology, the one to three tasks that matter on the wrist.

Change
- [MD] Choose the surface per task: complication, tile or widget, notification, app.
- [API] Rebuild with Wear Compose Material 3 (`AppScaffold`, `ScreenScaffold`, `TransformingLazyColumn`, `EdgeButton`); do not reuse phone composables.
- [MD] Navigation becomes shallow and linear (two levels at most), vertical scrolling only, time shown at the top.
- [MD] Margins as percentages of the round screen; design at 204dp to 216dp first, check 192dp, add content from 225dp.
- [Req] Black background (`WO-V13`); 48 x 48dp targets (`WO-V2`); essential text at 12sp or more (`WO-V14`).

Add
- [Req] Swipe to dismiss on almost every screen (`WO-V3`); scroll indicator on scrolling views (`WO-V8`); `OngoingActivity` for long-running work (`WO-V4`).
- [MD] Rotary scrolling, voice input, haptic confirmation, offline behaviour.
- [Req] Same package name and signing key as the phone app (`WO-G7`); manifest feature `android.hardware.type.watch`.

Remove
- [Conv] Navigation bar, drawer, top app bar, FAB, bottom sheets, light theme, dense forms.
- [Req] Username and password entry on the watch (`WO-P6`).

See `references/platforms-wear.md`.

Source: https://developer.android.com/training/wearables/principles, https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/design/ui/wear/guides/foundations/adaptive-design

## To Android TV

Keep
- [Conv] Content catalogue, artwork, brand colour (adapted to a dark scheme), account state.

Change
- [MD] Every interaction becomes focus plus D-pad: one focused element, predictable directions, strong focus indicators (scale, border, glow, colour).
- [MD] Navigation becomes top tabs or a left navigation drawer; content becomes rows, grids and a details page on a 960 x 540dp canvas with a 12-column grid.
- [MD] Larger type, dark-first palette, sRGB colours tested in Standard picture mode.
- [API] Build with Compose for TV (`androidx.tv.material3`), not Leanback.

Add
- [Req] `LEANBACK_LAUNCHER` activity, banner, touchscreen declared not required (`TV-ML`, `TV-LB`, `TV-MT`).
- [MD] Safe margins for overscan; media keys and D-pad centre for play and pause (`TV-PC`); voice search; sign-in by phone or Google Account.

Remove
- [MD] On-screen back buttons and exit confirmations.
- [Conv] Touch-only controls, swipe gestures, FAB, bottom navigation bar, portrait layouts, long typed forms.
- [Req] Links that open a browser (`TV-WB`).

See `references/platforms-tv.md`.

Source: https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv, https://developer.android.com/design/ui/tv/guides/styles/layouts, https://developer.android.com/docs/quality-guidelines/tv-app-quality

## To cars

Keep
- [Conv] The service the app provides, its data and account; app icon and accent colours.

Change
- [Req] First check the category: only media, messaging and calling, navigation, POI, IoT and weather apps may be used while driving; video, games and browsers only while parked (`PC-1`).
- [API] Driving UI is assembled from Car App Library templates rendered by the host; media apps expose a media browser and session instead of screens.
- [Req] Flows of 5 steps or fewer (2 to 3 is a SHOULD). [API] At most five screens on the stack.
- [MD] Text short enough to read at a glance (1 to 3 lines, 120 characters); voice entry points.

Add
- [Req] Light and dark variants when theming; contrast per the car requirements; voice commands for media and navigation (`VC-1`).
- [API] Two artifacts: `app-projected` (Android Auto) and `app-automotive` (Android Automotive OS).

Remove
- [Req] Animation, auto-scrolling text, decorative images (`SA-1`, `ST-1`, `IU-1`); advertising and irrelevant notifications (`NA-1`, `IN-1`); payment set-up (`PA-1`).
- [Conv] Custom layouts, fonts, gestures and navigation containers.

Parked apps instead follow the large-screen checklist plus `DD-3` (not usable while driving). See `references/platforms-auto-xr.md`.

Source: https://developer.android.com/training/cars, https://developer.android.com/design/ui/cars/guides/ux-requirements/overview, https://developer.android.com/docs/quality-guidelines/car-app-quality

## To Android XR

Keep
- [MD] The adaptive large-screen app: it runs in Home Space unmodified, in a window between 385 x 595dp and 2560 x 1800dp. Material components, theme and typography carry over.

Change
- [MD] Targets toward 56dp; text at 14dp or larger at normal weight or heavier; hover and focus states on everything interactive.
- [MD] In Full Space, split the UI into spatial panels and move a few navigation or control elements into orbiters.

Add
- [MD] A visible control to switch between Home Space and Full Space.
- [API] A capability check (`isSpatialUiEnabled`) with the 2D layout as fallback.
- [MD] Comfortable placement: panels 0.75 to 5 metres away, default 1.75 metres, slightly below eye level, content within the central 41 degrees.

Remove
- [MD] Fast or unexpected motion of UI and environments; many orbiters; elevated sheets and scrolling surfaces.
- [Conv] Reliance on touch-only gestures or on stable library APIs: Compose for XR is at release candidate and Material 3 for XR is experimental.

See `references/platforms-auto-xr.md`.

Source: https://developer.android.com/design/ui/xr/guides/foundations, https://developer.android.com/design/ui/xr/guides/spatial-ui, https://developer.android.com/design/ui/xr/guides/visual-design, https://developer.android.com/develop/xr/jetpack-xr-sdk/material-design

## Coming from an iOS design

Google publishes a guide for translating iOS designs to Android; the rows below state the Android side from that guide and the Android and Material guidance. They do not describe Apple's guidance; read the incoming design for what it does, then apply the Android column.

| Element in the incoming design | On Android | Tag |
|---|---|---|
| System status area and home indicator | Replace with the Android status bar and either the gesture handle or the 3-button navigation bar; design for both and go edge to edge with insets | [MD] |
| Frame size | Work at a 412dp-wide compact frame, also check 360dp, then adapt across window size classes | [MD] |
| Bottom tab bar | Navigation bar with three to five primary destinations, icons with labels; move secondary items such as profile or settings to the top app bar; avoid an overflow "more" destination. At medium width and up it becomes a navigation rail | [MD] |
| Top bar with title and buttons | Top app bar: navigation icon and title on the left (title left-aligned by default), actions on the right as icons, extra actions in an overflow menu | [MD] |
| Large collapsing title | Large flexible top app bar that starts expanded and collapses on scroll | [MD] |
| Back control in the top bar | Up arrow on child screens only, never on the start destination, never leaving the app. System Back (edge swipe from either side or the Back button) is separate, handled by the OS, previews its destination, and exits the app from the start destination. No other on-screen back prompts | [MD] |
| Edge swipe used for app features | Left and right screen edges belong to the Back gesture; keep app gestures out of gesture insets | [MD] |
| Full-screen modal with text buttons | Full-screen dialog with a close icon in the navigation position and an action on the right; Android tends toward icons for dismissal | [MD] |
| Modal sheet | Full-screen dialog for focused tasks, or a bottom sheet where it fits; dismissible with Back; maximum width or side sheet on larger windows | [MD] |
| Action or activity sheet | Bottom sheet or menu; for sharing, the system Sharesheet | [MD] |
| Alert | Dialog | [MD] |
| Segmented control switching sibling views | Tabs, usually attached to the top app bar, which can also be swiped | [MD] |
| Prominent primary action button | Consider a floating action button for the single most important action on a screen; otherwise the Material button hierarchy. Do not stretch buttons full width on large windows | [MD] |
| Toggles, checkmarks, pickers, text fields | Material switch, checkbox, radio button, date and time pickers, filled or outlined text fields | [MD] |
| List rows with chevrons and full dividers | Material lists: dividers used sparingly, no disclosure indicators, dimensions on the 8dp grid | [MD] |
| Point units and a fixed type size | dp for layout and sp for text; 16dp margins are a good standard on small screens; 8dp grid, 4dp for type and icons; text must survive user font scaling up to 200% | [MD] |
| System font and symbol set | Roboto is the default system font; brand fonts through theming; icons converted to Material Symbols or Icons | [MD] |
| Minimum target of 44 units | 48 x 48dp touch targets (Material's layout guidance itself notes that the iOS figure differs) | [MD] |
| Colour and appearance | Material colour roles in a light and a dark scheme; dynamic colour from Android 12 with a static fallback | [MD] |
| Motion | Material motion patterns (container transform, shared axis, fade through, fade) and ripple feedback; do not carry transitions over unchanged | [MD] |
| Photo and file access, sharing | System photo picker without storage permission; system Sharesheet | [MD] |
| Permission prompts at launch | Request in context with rationale; notification permission is a runtime request from Android 13 | [MD] |
| App icon and launch screen | Adaptive icon with foreground, background and monochrome layers; system splash screen generated from the icon | [API] |
| Settings | In-app "Settings" screen reached from the top app bar or overflow; do not duplicate system settings | [MD] |
| Orientation lock and fixed layout | Not respected on large screens from targetSdk 36; design adaptively | [API] |

- [MD] The translation guide's order of work: system UI, frame size, primary navigation, top app bars, modality, sibling content, content and controls, style, then re-check navigation with the difference between Up and Back in mind.
- [Conv] A brand design system may replace Material 3 visually, but the structural rules above (Back, Up, system bars, insets, targets, text scaling) still apply.

Source: https://developer.android.com/design/ui/mobile/guides/foundations/translate-designs, https://developer.android.com/guide/navigation/principles, https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns, https://developer.android.com/design/ui/mobile/guides/foundations/system-bars, https://m3.material.io/foundations/designing/structure

## Adaptation review procedure

1. [Conv] Detect source and destination targets (`references/platforms-detection.md`); list which libraries change.
2. [Conv] List the tasks that belong on the destination; drop the rest for watch, TV and car.
3. [Conv] Map navigation, Back, modality, input and theme using the summary table; note every phone-only pattern that remains.
4. [Conv] Apply the destination checklist and its reference file.
5. [Conv] Classify each finding as requirement, platform behaviour, quality guideline or recommendation (`references/platforms-quality.md`) and cite the ID where one exists.
6. [Conv] State what could not be verified from the code (focus order on a real remote, round-screen clipping, hinge behaviour) and how to test it: resizable emulator, foldable 1:1 and 4:3 profiles, Wear small and large round, desktop emulator.

Source: https://developer.android.com/docs/quality-guidelines/adaptive-app-quality

## Common mistakes

| Mistake | Fix |
|---|---|
| One layout scaled to every size | Reflow, reveal, or change presentation by window size class |
| Phone composables reused in Wear or TV modules | Use the form factor's Material library |
| Watch app with the phone's whole feature set | A few critical tasks; other surfaces for glances |
| TV app that needs a pointer | D-pad focus for everything; pointer is optional Tier 1 |
| Driving app designed as custom screens | Templates and category rules first |
| XR treated as a new app from scratch | Start from the adaptive app in Home Space, then spatialise |
| iOS design copied with a back chevron, bottom tab styling and sheets with text buttons | Up arrow plus system Back, navigation bar or rail, dialogs and bottom sheets with icon dismissal |
| pt values pasted as dp for text | Text in sp, tested with font scaling |
| Custom share and photo pickers ported over | Sharesheet and system photo picker |
| Same top-level destinations reordered per form factor | Keep names, icons and order; change only the container |
