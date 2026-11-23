# Large screens: tablets, foldables, desktop windowing, ChromeOS

Scope: what changes when an Android app runs in a window larger or differently shaped than a phone screen: window size classes and their dp breakpoints, navigation by size class, panes and canonical layouts, foldable postures and the hinge, multi-window and desktop windowing (tablets, connected displays, ChromeOS, Googlebook), keyboard, mouse and stylus, the orientation and resizability rules by `targetSdk`, and what a "stretched phone app" looks like.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Principles
- Window size classes
- Navigation by size class
- Panes and canonical layouts
- Secondary elements at large sizes
- Foldables: postures and hinge
- Orientation, aspect ratio and resizability
- Multi-window and desktop windowing
- Keyboard, mouse, trackpad and stylus
- Stretched phone app: how to recognise it
- Common mistakes

## Principles

- [MD] Adaptive is the default, not an add-on: "mobile" covers phones, foldables, tablets and everything between, and the same app is resized in split screen, desktop windows and on connected displays.
- [API] Decide layout from the window the app has now, not from the device. One device yields many window sizes (split screen, folding, free-form windows), and the size changes while the app runs.
- [MD] Adapt by reflowing, revealing more content, or changing a component's presentation (bottom sheet to side sheet); never by scaling a phone layout up.
- [MD] Think in panes: compact width uses one pane, medium one or two, large and extra-large several.
- [MD] On desktop-class windows show more information in a denser layout; touch, pointer and keyboard are equally important because users switch between them.
- [Conv] Quality tiers that grade all of this (Adaptive ready, optimized, differentiated) are in `references/platforms-quality.md`.

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/adapt-layout, https://developer.android.com/design/ui/desktop/guides/foundations/design-principles

## Window size classes

- [API] Width classes: compact under 600dp, medium from 600dp, expanded from 840dp, large from 1200dp, extra-large from 1600dp. Full table with typical devices and pane counts: `references/foundations-layout.md`; code constants: `references/implementation-navigation.md`. Height classes are listed only here:

| Class | Height | Typical case |
|---|---|---|
| Compact | under 480dp | Phones in landscape |
| Medium | 480dp to under 900dp | Tablets in landscape, phones in portrait |
| Expanded | 900dp and up | Tablets in portrait |

- [API] Width and height are classified separately. Width usually matters most; check height too, because a phone or open flip phone in landscape is typically medium width with compact height, where two panes are not practical.
- [API] The classes describe the window, are "not intended for isTablet-type logic", and change during the app's lifetime (rotation, folding, multitasking, window resize).
- [API] Large and extra-large were added for desktop and connected displays. Compose: `androidx.compose.material3.adaptive`. The size-class guide computes the class with `currentWindowAdaptiveInfo()` and opts in to the two widest classes with `supportLargeAndXLargeWidth = true`; the adaptive do's and don'ts page says that function is deprecated and replaced by `currentWindowAdaptiveInfoV2()` (adaptive 1.3). Google's pages disagree here: use the V2 function on adaptive 1.3+, the older one on 1.2.x.
- [API] Contradiction to know about: the mobile design pages still describe three window size classes; the developer guide defines five widths.
- [MD] When extending an existing compact layout, design the expanded width first, then decide what medium needs.
- [API] Do not measure with the deprecated `Display.getSize()`, `getMetrics()`, `getRealSize()` or `getRealMetrics()`; use window metrics.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes, https://developer.android.com/develop/ui/compose/layouts/adaptive/adaptive-dos-and-donts, https://m3.material.io/foundations/layout/breakpoints/overview

## Navigation by size class

| Window | Primary navigation | Tag |
|---|---|---|
| Compact width | Navigation bar at the bottom (three to five destinations) or a modal expanded navigation rail (the Android design page still names a modal navigation drawer, which Material no longer recommends) | [MD] |
| Compact height (landscape phone), or tabletop posture | Navigation bar is the `NavigationSuiteScaffold` default; the design guidance also allows a rail here for ergonomics | [API] |
| Medium width | Navigation rail; a navigation bar with horizontal items is allowed (Material's pages disagree: details and working rule in `references/foundations-layout.md`) | [MD] |
| Expanded and wider | Navigation rail; on larger windows a rail that expands into a full navigation panel | [MD] |

- [MD] Do not use the bottom navigation bar on large screen sizes; the rail is easier to reach while holding a large device by its sides.
- [MD] Adaptive quality Tier 2 states that navigation rails replace navigation bars and that navigation drawers are updated to expanded navigation rails at large sizes.
- [API] `NavigationSuiteScaffold` (artifact `material3-adaptive-navigation-suite`) switches automatically: navigation bar when width or height is compact or the device is in tabletop posture, navigation rail otherwise. The navigation type can be overridden, for example a permanent drawer at expanded width.
- [API] The expanding rail is `WideNavigationRail`, with the modal variant `ModalWideNavigationRail`; both are stable from material3 1.4.
- [MD] In a desktop window, navigation or global actions such as search may move into the customisable middle of the window header bar.
- [Conv] Keep the same destinations, order, icons and labels across bar and rail; only the container changes.

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns, https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2, https://developer.android.com/design/ui/desktop/guides/system/system-bars, https://m3.material.io/foundations/layout/breakpoints/compact

## Panes and canonical layouts

| Layout | Use for | Behaviour by width | Compose scaffold |
|---|---|---|---|
| List-detail | Messaging, contacts, file or media browsers, settings | Expanded: list and detail side by side. Medium and compact: one at a time; Back from detail returns to the list | `ListDetailPaneScaffold` |
| Supporting pane | Document plus comments, video plus related list, editor plus tool palette | Expanded: about 70% main, 30% supporting. Medium: split equally. Compact: supporting content below the main content or in a bottom sheet | `SupportingPaneScaffold` |
| Feed | News, social, galleries | Grid whose column count follows the available width; one column on compact | Lazy grid with adaptive columns |

- [API] List-detail state rules on resize: expanded to narrower keeps the detail visible and hides the list; narrower with detail showing to expanded shows both with the item selected; narrower with only the list to expanded shows the list plus a placeholder detail.
- [API] The detail-to-list Back handling at small widths is window-size dependent and separate from the app's overall navigation graph.
- [API] The pane scaffolds live in `androidx.compose.material3.adaptive:adaptive-layout` and `adaptive-navigation` and are annotated `@ExperimentalMaterial3AdaptiveApi`: say so and opt in explicitly. Apps built from several activities can show them side by side with activity embedding.
- [MD] Supporting-pane content only makes sense next to the main content; list-detail detail content stands on its own. Choose accordingly.
- [MD] Preserve state across the change: the unfolded layout continues what the folded one showed and adds complementary content.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts, https://developer.android.com/develop/ui/compose/layouts/adaptive/foldables/learn-about-foldables

## Secondary elements at large sizes

- [MD] Set a maximum width on content and components; buttons, text fields and bottom sheets are not full width on large screens.
- [MD] Keep text lines readable: core app quality asks for 45 to 75 characters per line (`Line_Length`).
- [MD] Small edit menus and modals do not cover the whole screen; context menus appear next to the selected item; dialogs stay reachable.
- [MD] A filter or options bottom sheet becomes a side sheet; if it must stay full screen, give it a multi-column layout.
- [MD] Do not scale a small grid up into a few huge items; change the column count and density.
- [MD] Each pane gets its own status-bar protection matching its background (`references/platforms-system.md`).

Source: https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2, https://developer.android.com/design/ui/mobile/guides/layout-and-content/adapt-layout, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Foldables: postures and hinge

- [API] Fold states are `FLAT` (fully open) and `HALF_OPENED`. Half opened with a horizontal fold is tabletop posture; with a vertical fold it is book posture.
- [API] `FoldingFeature` (Jetpack WindowManager) reports `state`, `orientation`, `occlusionType` (`FULL` when a hinge hides content, as on dual-screen devices), `isSeparating` and `bounds`. The hinge angle is not exposed. In Compose collect it with `collectFoldingFeaturesAsState()`.
- [MD] Do not place dialogs, pop-up menus, controls or text across the fold. When half opened, split content into two areas: top and bottom in tabletop, left and right in book.
- [MD] In a two-pane layout widen the gutter so the hinge falls between panes; some devices (trifolds) have more than one hinge.
- [MD] An app does not have to support every posture; pick the one that helps (tabletop for video calls and playback, book for long reading).
- [API] Inner displays come in two families: square 1:1 (medium or expanded width in both orientations) and wide 4:3 (expanded in landscape). Test with the emulator profiles "Foldable (1:1 inner display)" and "Foldable (4:3 inner display)".
- [MD] Cover screens are compact and may be square: keep them focused on one task, edge to edge, and clear of camera cutouts. A small navigation rail can work better than a bar there.
- [API] Folding or unfolding stops and restarts the app on the other screen: state must survive it. Rear display mode and dual-screen mode are additional, optional display modes.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/foldables/learn-about-foldables, https://developer.android.com/develop/ui/compose/layouts/adaptive/foldables/make-your-app-fold-aware, https://developer.android.com/design/ui/mobile/guides/layout-and-content/postures-and-orientation

## Orientation, aspect ratio and resizability

| Target | On displays whose smallest width is 600dp or more | Tag |
|---|---|---|
| targetSdk 35 and lower | Restrictions are honoured; a restricted app is letterboxed or shown in compatibility mode on large screens | [API] |
| targetSdk 36 | `screenOrientation`, `resizeableActivity`, `minAspectRatio`, `maxAspectRatio`, `setRequestedOrientation()` and `getRequestedOrientation()` are ignored; the app fills the window. Temporary opt-out: manifest property `android.window.PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY` on an activity or the application | [API] |
| targetSdk 37 | Same, and the opt-out no longer applies | [API] |

- [API] Exceptions: games (by `android:appCategory`), users who choose the app's default behaviour in the device's aspect-ratio settings, and screens below sw600dp. So a portrait lock still works on a phone and stops working on tablets and unfolded foldables.
- [API] The Android 16 page says smallest width "at least" 600dp; the Android 17 change page says "greater than 600dp". Treat 600dp itself as included.
- [API] On Android 12 (API 31)+ large screens run every app in multi-window mode regardless of `resizeableActivity`; in desktop windowing an orientation-locked app is still freely resizable.
- [MD] Do not lock orientation and do not set `resizeableActivity="false"` at any API level; remove `minAspectRatio` and `maxAspectRatio`. A portrait lock can look like a bug and causes letterboxing when multitasking.
- [MD] The docs state that letterboxed apps are subject to decreased discoverability on Google Play for tablets, foldables and ChromeOS devices. That is a stated consequence, not a rejection rule.
- [MD] If content did not scroll in portrait, do not make it scroll in landscape; reflow or use panes.
- [API] More rotation means more activity recreation: save UI state. Camera previews that assume a fixed sensor orientation appear stretched or rotated.

Source: https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/about/versions/17/changes/ff-restrictions-ignored, https://developer.android.com/develop/ui/compose/layouts/adaptive/adaptive-dos-and-donts, https://developer.android.com/design/ui/mobile/guides/layout-and-content/postures-and-orientation

## Multi-window and desktop windowing

- [API] Split screen and picture-in-picture date from Android 7.0 (API 24). Multi-resume means several visible apps are resumed at once: keep updating UI and playback when the app is visible but not focused, and expect to lose exclusive resources such as the camera.
- [API] Desktop windowing puts apps in free-form, resizable windows with a taskbar and, on every window, a system header (caption) bar with minimise, maximise and close. It is available on tablets, on connected displays driven by a phone, on ChromeOS and on Googlebook (a device class built on the Android stack with ChromeOS desktop foundations).
- [API] The header bar is always present, even in immersive mode: handle `WindowInsets.captionBar` (included in `systemBars`). The app may make the header background transparent (`APPEARANCE_TRANSPARENT_CAPTION_BAR_BACKGROUND`) and draw a title, tabs or search in the free middle area; system buttons stay on top.
- [API] Multi-instance: declare `PROPERTY_SUPPORTS_MULTI_INSTANCE_SYSTEM_UI` (Android 15+) so the system offers a new-window action. New tasks open as new windows, so re-check flows that start tasks.
- [MD] Support several windows of the same app where it helps (documents, comparison, conversations), drag and drop between windows and apps, and continued media playback or picture-in-picture when minimised.
- [API] Connected displays: the display, its density and size can change while the app runs or when a window moves; use the activity context and dp, never values cached from the phone screen, and never device-model allowlists.
- [MD] Give windows a sensible default launch size when a large window adds nothing; offer a full-screen action for immersive content.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/support-desktop-windowing, https://developer.android.com/develop/ui/compose/layouts/adaptive/support-multi-window-mode, https://developer.android.com/develop/ui/compose/layouts/adaptive/support-connected-displays, https://developer.android.com/develop/adaptive-apps/guides/googlebook/overview, https://developer.android.com/design/ui/desktop/guides/system/multi-task

## Keyboard, mouse, trackpad and stylus

| Input | Expectation | Tag |
|---|---|---|
| Keyboard | Tab and arrow-key navigation through the main flows with a visible focus state; Enter sends in communication apps; Esc closes dialogs, menus, search and full-screen modes; Spacebar plays and pauses media; standard shortcuts (copy, paste, cut, undo, redo, save) | [MD] |
| Keyboard | Publish app shortcuts through Keyboard Shortcuts Helper | [MD] |
| Mouse, trackpad | Every primary journey works with primary click alone; context menus open on secondary click instead of long-press; hover states on actionable elements, tooltips on hover; scroll wheel works on custom components; Ctrl plus wheel and pinch zoom content | [MD] |
| Mouse, trackpad | Drag starts immediately on click-and-drag (no long-press); selection gets a dedicated click target such as a checkbox on hover; scrollbars appear while scrolling | [MD] |
| Pointer targets | May be smaller than the 48x48dp touch target for cursor-only affordances; do not stretch buttons full width or keep oversized invisible targets under a pointer. Material's layout guidance suggests considering 44x44dp as the pointer minimum | [MD] |
| Custom drawables | If interactive they must be focusable outside touch mode with a visible focus indication (Tier 2 `Drawable_Focus`) | [MD] |
| Stylus | Works as touch by default; handwriting into text fields is built in from Android 14; drawing apps add pressure, tilt, palm rejection and low latency | [API] |

- [API] Built-in Compose components such as `Button` are focusable by default; custom elements need the `focusable` modifier, and tab order in complex groups may need explicit focus handling.
- [MD] Touch targets stay at least 48dp on touch devices regardless of window size.

Source: https://developer.android.com/develop/ui/compose/touch-input/input-compatibility-on-large-screens, https://developer.android.com/design/ui/desktop/guides/interaction/pointer-interactions, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2, https://m3.material.io/foundations/designing/structure

## Stretched phone app: how to recognise it

- [Conv] One column of full-width rows, cards or text spanning a 1000dp window, with lines far beyond 75 characters.
- [Conv] Full-width buttons, text fields, sliders and bottom sheets; a dialog or sheet covering the whole tablet screen.
- [Conv] Bottom navigation bar with destinations spread across the full width at expanded size.
- [Conv] Push navigation from list to detail on a screen that could show both.
- [Conv] Letterboxing, or a layout that only works in portrait; state (scroll position, typed text, playback) lost on rotate, fold or resize.
- [Conv] Layout decided from device model, `isTablet` flags or orientation instead of the window size class.
- [Conv] Long-press as the only route to a context menu; no hover, focus or keyboard handling; content hidden under the caption bar.
- [Conv] Images or video scaled up or cropped instead of the layout gaining content.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/adaptive-dos-and-donts, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2

## Common mistakes

| Mistake | Fix |
|---|---|
| "Tablet layout" chosen by device type | Window size classes, re-evaluated at runtime |
| Only three size classes handled | Opt in to large and extra-large for desktop windows |
| Navigation bar kept at expanded width | Navigation rail; expanded rail on larger windows; `NavigationSuiteScaffold` |
| Modal navigation drawer as the tablet pattern | Expanded navigation rail |
| `android:screenOrientation="portrait"` to avoid layout work | Remove it; ignored at sw600dp+ from targetSdk 36 |
| `resizeableActivity="false"` | Never set it |
| Controls or text across the fold | Split at the fold; widen the gutter |
| Assuming the app owns the top edge in a desktop window | Handle caption bar insets |
| Bottom sheet stretched across a tablet | Maximum width or side sheet |
| Pane scaffolds used without noting the experimental opt-in | State `ExperimentalMaterial3AdaptiveApi` |
| Calling adaptive tiers "Play requirements" | Tier 3 is the stated baseline, Tier 2 and 1 earn badging: `references/platforms-quality.md` |
