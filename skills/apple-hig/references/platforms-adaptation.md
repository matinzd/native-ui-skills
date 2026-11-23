# Cross-platform adaptation playbook

Scope: how to take a design that exists on one Apple platform to another: the principles (share content and identity, not chrome), then keep / change / add / remove checklists for iPhone to iPad, iPad to Mac (native versus Mac Catalyst), iPhone to Apple Watch, to Apple TV, to Apple Vision Pro, and iPhone to iPhone Duo, with the common porting mistakes.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Principles
- What changes: one-table summary
- iPhone to iPad
- iPad to Mac: choose the route
- iPad to Mac: checklist
- iPhone to Apple Watch
- To Apple TV
- To Apple Vision Pro
- iPhone to iPhone Duo
- Porting review procedure
- Common mistakes

## Principles

- [HIG] Each platform deserves equal care: flexibility means adapting to each context and input, not reusing one layout everywhere.
- [Conv] Share content, data, terminology, iconography, color identity and core tasks. Do not share chrome: bars, navigation containers, modality, menus, density and input handling come from the destination platform's system components.
- [HIG] People expect the experience to stay familiar when they switch devices: keep the information hierarchy, names and symbols for the same things, and consistent placement of equivalent actions across platforms.
- [HIG] Keep functionality the same as the available space changes; change how much is visible, and keep layout changes recognizable for the platform. Size classes, not device type or orientation, drive layout on iOS and iPadOS.
- [HIG] Prefer system components: they adapt to the platform, input and OS design (Liquid Glass on OS 26+, glass on visionOS, focus effects on tvOS) without custom work.
- [HIG] Every interaction needs more than one path: gestures need visible controls, pointer hovers need touch and keyboard equivalents, menu bar commands need in-app UI on iPad.
- [Conv] Scope by context of use, not by feature parity. Apple Watch and Apple TV versions are usually a subset built around what people do on that device; iPad, Mac and Vision versions are usually a superset.
- [Conv] Establish the target first (`references/platforms-detection.md`): platform, flavour (native, Catalyst idiom, Designed for iPad) and minimum OS decide which of the moves below are even possible.

Source: https://developer.apple.com/design/human-interface-guidelines/design-principles, https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/toolbars

## What changes: one-table summary

| From iPhone | iPad | Mac | Apple Watch | Apple TV | Apple Vision Pro |
|---|---|---|---|---|---|
| Bottom tab bar | Tab bar near the top, optionally sidebar-adaptable | Sidebar in a split view; tabs listed in the View menu | Vertical tab pages or a list | Tab bar at the top | Vertical tab bar on the window's leading side |
| Stack push | Split view columns | Split view panes, multiple windows | Shallow list then detail | Split view or focus rows | Split view inside the window |
| Top and bottom toolbars | Top toolbar, can share the tab bar row | Window toolbar plus menu bar commands | Corner or bottom toolbar buttons | Few focusable buttons | Bottom toolbar ornament |
| Sheet with detents | Page or form sheet, popover | Sheet attached to its window, panel, inspector | Brief full-screen sheet | Full-screen view or alert (synthesized) | Centered sheet |
| Action sheet | Action sheet | Action sheet (no macOS-specific notes) | Action sheet, 4 buttons maximum | Action sheet | Not supported: alert or menu (synthesized) |
| Touch 44 pt default | 44 pt plus pointer and keyboard | 28 pt default, pointer precision | 44 pt, full-width buttons | 66 pt, focus | 60 pt, eyes and pinch |
| Body 17 pt | 17 pt | 13 pt, no Dynamic Type | 16 pt | 29 pt | 17 pt |
| Dark Mode | Yes | Yes | None | Yes | None |
| Widgets, Live Activities | Widgets, Live Activities | Widgets | Complications, Smart Stack | Top Shelf | Spatial widgets |

Cells marked (synthesized) follow from "not supported" notes and general guidance rather than one explicit HIG statement.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/typography

## iPhone to iPad

Keep
- [HIG] The same functionality, hierarchy and tab set (five or fewer default tabs keeps compact and regular widths consistent).
- [HIG] The compact-width layout itself: an iPad window can be compact, so the iPhone layout remains one of the iPad's layouts.

Change
- [HIG] Tab bar moves near the top (system behaviour); use the sidebar-adaptable form when there are more sections than a bar holds.
- [HIG] Push-only stacks become two- or three-column split views in regular width that collapse at narrow widths.
- [HIG] Full-screen modals become page or form sheets, popovers (regular width only), or columns; minimize modality and full-screen transitions.
- [HIG] Bottom-anchored controls placed for thumb reach get rethought: position controls where they are reachable but not in the way on a large display.

Add
- [HIG] Resizable windows and multiple windows; leading toolbar items that step aside for window controls.
- [HIG] Menu bar menus in Mac order with standard shortcuts, plus the same commands in the UI.
- [HIG] Keyboard focus groups, pointer effects, band selection, context menus on secondary click (including on empty areas to create objects).
- [HIG] Drag and drop with multi-item drags; Apple Pencil and Scribble where marking or handwriting is relevant.

Remove
- [API] `UIRequiresFullScreen`, orientation locks used to avoid layout work, and any assumption of full screen.
- [HIG] Layout branches on device idiom or orientation.

See `references/platforms-ipados.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados, https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/documentation/bundleresources/information-property-list/uirequiresfullscreen

## iPad to Mac: choose the route

| Route | What you get | Design latitude | Choose when |
|---|---|---|---|
| Native macOS target (SwiftUI or AppKit) | Full macOS SDK and conventions | Complete | A Mac-first experience matters; SwiftUI code can share a multiplatform target |
| Mac Catalyst, iPad idiom | UIKit app scaled to 77%; automatic menus, window management, pointer and keyboard support | Mac menus, toolbar, shortcuts, context menus; iPad-looking controls | Fast path from a good iPad app |
| Mac Catalyst, Mac idiom | Unscaled rendering; AppKit-like controls; sharper text | Same plus Mac-looking controls; needs a layout, font and asset audit | Text-heavy or detailed apps worth the audit |
| iPad app on Mac ("Designed for iPad") | Unmodified iOS binary on Apple silicon | None beyond the iPad app | No Mac work planned; the iPad app already resizes and supports keyboard |

- [API] Apple's guidance for a UIKit app that would need AppKit on the Mac is separate targets; a SwiftUI app can add a Mac destination to one multiplatform target.
- [HIG] Catalyst suits iPad apps that already handle drag and drop, keyboard navigation and shortcuts, resizing and multiple windows; apps built around device sensors, the rear camera, HealthKit, ARKit, marking, handwriting or navigation may not suit the Mac.
- [HIG] Whatever the idiom, do not stop at showing the iPad layout in a Mac window.

Source: https://developer.apple.com/design/human-interface-guidelines/mac-catalyst, https://developer.apple.com/documentation/xcode/configuring-a-multiplatform-app-target, https://developer.apple.com/documentation/uikit/choosing-a-user-interface-idiom-for-your-mac-app, https://developer.apple.com/documentation/apple-silicon/running-your-ios-apps-in-macos

## iPad to Mac: checklist

Keep
- [HIG] Sidebar and split-view structure (a sidebar on both keeps the two versions consistent), search placement, content and terminology.
- [HIG] Gestures people know from iPad and the trackpad; most iPad gestures map automatically in Catalyst (tap to click, touch and hold to click and hold, pan to drag; pinch and rotate on a trackpad).

Change
- [HIG] Tab bar becomes a sidebar split view (preferred) or, for flat hierarchies, a segmented control; list the former tabs in the View menu.
- [HIG] Controls in the main UI and at the bottom or side edges move into the window toolbar; adopt a top-down flow with the most important actions and content near the top.
- [HIG] One column becomes several; content reflows side by side as the window resizes; popovers that hold persistent detail become an inspector.
- [HIG] Density: 13 pt body and 28 pt default controls instead of 17 pt and 44 pt. In Catalyst's Mac idiom text renders at 100%, so sizes tuned for iPad look too large; prefer text styles to fixed sizes.
- [HIG] Sheets attach to one window and must not block the app's other windows; repeated-input tasks become panels.
- [HIG] Settings move to a Settings window opened from the App menu with Command-Comma.

Add
- [HIG] Every command in the menu bar with standard shortcuts; toolbar items are a subset of menu commands; Window and View menus even in simple apps.
- [HIG] Context menus on essentially every object.
- [HIG] Next and Previous buttons alongside swipe paging.
- [HIG] Window behaviour: resize, minimize, full screen, multiple windows, correct main/key/inactive appearance; a macOS app icon.
- [HIG] On a Mac with a touch display: same layout, larger tap targets, hover-revealed controls also revealed by tap and offered in a context menu.

Remove
- [HIG] Reliance on Dynamic Type (macOS does not support it), page controls (not supported; unavailable in the Catalyst Mac idiom), status bar assumptions, virtual keyboard handling.
- [HIG] Controls or status at the bottom of windows and sidebars; touch-only interactions; custom window chrome.

See `references/platforms-macos.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/mac-catalyst, https://developer.apple.com/design/human-interface-guidelines/designing-for-macos, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/design/human-interface-guidelines/settings, https://developer.apple.com/design/human-interface-guidelines/gestures

## iPhone to Apple Watch

Keep
- [Conv] Data, identity colors, symbols and names; the one or two tasks that make sense in a glance lasting well under a minute.

Change
- [HIG] Hierarchy flattens: vertical lists and vertical tab pages on the Digital Crown; open on the most relevant detail.
- [HIG] Tab bar and segmented control (neither exists) become vertical pages or a list.
- [HIG] Text entry becomes option lists, dictation or sensible defaults.
- [HIG] Buttons become full-width; at most two text or three glyph buttons side by side.
- [HIG] Sheets become brief, occasional full-screen interruptions; action sheets hold four buttons at most including Cancel.
- [HIG] In-app settings shrink to a few options at the bottom of the main view or a More menu.
- [HIG] Type follows watchOS text styles in SF Compact (16 pt default, 12 pt minimum).

Add
- [HIG] Complications in every family you can serve, each with its own deep link; Smart Stack widgets with relevance information.
- [HIG] Actionable notifications with short-look and long-look designs.
- [HIG] Always On behaviour: redaction, dimming, stable layout.
- [HIG] Crown feedback, watch haptics used for their defined meanings, an optional double-tap primary action in non-scrolling views.
- [HIG] Independent operation without the iPhone.

Remove
- [HIG] Context menus, popovers, drag and drop, keyboard shortcuts, multitasking assumptions, Dark Mode variants, loading screens.
- [Conv] Long-form reading, browsing and configuration flows: leave them on the phone.

See `references/platforms-watchos.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos, https://developer.apple.com/design/human-interface-guidelines/complications, https://developer.apple.com/design/human-interface-guidelines/always-on, https://developer.apple.com/design/human-interface-guidelines/layout

## To Apple TV

Keep
- [Conv] Content catalog, artwork, playback state and accounts; the top-level sections as tabs.

Change
- [HIG] Every interactive element becomes focusable and reachable by directional movement; design unfocused, focused, highlighted, selected and unavailable states and leave room for focus scaling.
- [HIG] Tab bar sits at the top with fixed metrics (68 pt high, 46 pt from the top).
- [HIG] Layout respects the 60 pt top/bottom and 80 pt side insets and uses the grid widths; body text is 29 pt, default controls 66 pt.
- [HIG] Artwork runs edge to edge; text is minimal and legible from across the room; images are layered so focus can animate them.
- [HIG] Search becomes a dedicated keyboard screen with suggestions; other typing is minimized.
- [HIG] Back opens the parent screen and the Home Screen at the top level; Play/Pause controls playback.

Add
- [HIG] Top Shelf content with a static fallback image; TV app integration; SharePlay where relevant.
- [HIG] Multiuser handling: easy, infrequent sign-in and profile switching.

Remove
- [HIG] Touch idioms: swipe actions, pull to refresh, drag and drop, popovers, edit menus, sliders, steppers, pop-up and pull-down buttons, web views, widgets and Live Activities (none exist on tvOS).
- [HIG] Any pointer-style cursor for navigating menus; color-only focus indication; programmatic focus changes.
- [Conv] Long forms, dense settings screens and text-heavy pages.

See `references/platforms-tvos.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/remotes, https://developer.apple.com/design/human-interface-guidelines/top-shelf

## To Apple Vision Pro

First decide the route: a compatible iPad/iPhone app runs unmodified in a window with its iOS look; a visionOS build gets the system appearance and spatial features. The checklist below is for a visionOS build.

Keep
- [HIG] Familiar window-based interface and standard components; the app's hierarchy and tabs; Dynamic Type and text styles.

Change
- [HIG] Tab bar becomes the system vertical bar on the leading side (symbol plus short label per tab); the toolbar becomes the bottom ornament.
- [HIG] Backgrounds become the system glass: remove opaque full-window fills, use materials and vibrancy, white text by default, color used sparingly.
- [HIG] Targets grow to 60 pt areas with 16 pt margins and rounded shapes; every interactive element, including custom ones, shows a hover effect with one containing shape.
- [HIG] Sheets are centered in front of the window, not sliding from the bottom edge, and do not cover the whole window. Action sheets do not exist: use an alert or a menu.
- [HIG] Supplementary content moves to a split view or an adjacent window, not an ornament.

Add
- [HIG] Indirect-gesture support everywhere (free with standard components), direct interaction for nearby objects.
- [HIG] Resizable windows with sensible minimum and maximum sizes.
- [HIG] Volumes or immersion only where they add value, launched from the Shared Space with clear enter and exit controls.
- [HIG] Descriptive keyboard shortcut titles for the Command-key shortcut list; spatial widgets if the app has widgets.

Remove
- [HIG] Dark Mode variants and any Liquid Glass styling or APIs.
- [HIG] Anything that depends on gaze position, head-locked content, peripheral motion, world rotation.
- [API] Features unavailable on the device: Live Activities, App Clips, Picture in Picture, device camera capture, Core Motion-dependent interactions.
- [HIG] Pull-down menus in the toolbar, vertical toolbars, context menus taller than the window.

See `references/platforms-visionos.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos, https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/eyes, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/documentation/visionos/determining-whether-to-bring-your-app-to-visionos

## iPhone to iPhone Duo

iPhone Duo is still iPhone; an app built from standard components that already resizes needs little work.

Keep
- [HIG] All iOS patterns, the same functionality and state on both displays, and the default bar placement the system chooses.

Change
- [HIG] Treat the outer display as compact width and the inner display as regular width; the split view that collapses on the outer display expands on the inner one, optionally showing one more level of hierarchy.
- [HIG] Expect bars on the side (outer display; inner display in landscape) and asymmetric content space: lay out with safe areas and margins.
- [HIG] Grids use an even number of columns; important elements stay clear of reserved regions (outer camera, inner camera when active, the fold when partially open).

Add
- [HIG] A title and a symbol for every non-text toolbar item; toolbar item groups; visibility priorities so frequent actions overflow last.
- [HIG] A per-screen choice of what compresses when space is tight: toolbar items into overflow (navigation-focused, the default) or the tab bar minimized (task-focused).
- [API] Optional 27.1 APIs behind availability checks: `ArrangementView`, `ReservedRegion`, `ToolbarVerticalCompressionBehavior`.

Remove
- [HIG] Fixed widths, display-specific code paths, a layout per pose, custom overflow menus (use the system one; keep the ellipsis for it), text-only toolbar buttons where a symbol works, dramatic rearrangement while folding.

See the iPhone Duo sections of `references/platforms-ios.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo, https://developer.apple.com/documentation/swiftui/arrangementview

## Porting review procedure

1. [Conv] Identify source and destination, flavour and minimum OS (`references/platforms-detection.md`).
2. [Conv] List the app's top-level sections, primary tasks and presentations (sheets, alerts, menus, popovers).
3. [Conv] Map each to the destination's component using the summary table; flag anything "not supported" there and choose the replacement.
4. [Conv] Re-derive metrics from the destination's numbers (text size, control size, safe insets); never scale the source layout.
5. [Conv] Walk the destination's inputs one at a time (touch, pointer, keyboard, Crown, remote, eyes and hands) and confirm every action is reachable with each input that platform supports.
6. [Conv] Add the destination's system surfaces (menu bar, complications, Top Shelf, widgets) and remove surfaces it lacks.
7. [Conv] Check appearance axes that exist there: Dark Mode, Dynamic Type, Liquid Glass or glass, Always On.
8. [Conv] State what was deliberately left out of the destination and why.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ios

## Common mistakes

| Mistake | Fix |
|---|---|
| Scaling the source layout up or down | Rebuild from the destination's components and metrics |
| iPad: stretched single column, bottom tab bar, full-screen modals | Split view, top tab bar or sidebar-adaptable, sheets and popovers |
| iPad: assuming full screen or one orientation | Resizable windows; layout by size class |
| iPad: menu bar as the only path, or no keyboard and pointer support | Commands in both UI and menus; focus groups, shortcuts, pointer effects |
| Mac: iPad layout in a window, no menu bar commands, toolbar-only actions | Menus for everything, window toolbar, sidebar, context menus, multiple columns |
| Mac: 17 pt text, 44 pt controls, bottom-edge actions, Dynamic Type assumptions | 13 pt body, 28 pt controls, top-down flow, in-app text sizing if needed |
| Mac: treating "Designed for iPad" as a Mac app | Classify the flavour; Mac conventions need Catalyst or a native target |
| Watch: the whole phone app, tab bars, deep stacks, text entry | One or two glanceable tasks, vertical pages, complications and notifications first |
| TV: unfocusable elements, pointer or touch idioms, content in overscan, small text | Focus engine, 60/80 pt insets, 29 pt body, 66 pt controls |
| TV: color-only focus, custom focus jumps, long forms | System focus effects, user-driven focus, minimal typing |
| Vision: phone-density targets, opaque backgrounds, Dark Mode variants, Liquid Glass APIs | 60 pt targets, system glass, vibrancy, no appearance variants |
| Vision: head-locked UI, gaze-dependent logic, forced immersion | Space-anchored content, tap events, Shared Space first with explicit entry and exit |
| iPhone Duo: fixed widths, per-display layouts, overriding side bars, content across the fold | Size classes, same functionality, default bar placement, reserved regions |
| Any: feature differences between sizes of the same app | Same functionality; change only what is visible |
