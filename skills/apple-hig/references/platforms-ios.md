# iOS (iPhone and iPhone Duo)

Scope: what is specific to designing for iPhone: device context, inputs, navigation model, presentations, numbers, OS 26+ Liquid Glass behaviour, what does not exist on iPhone, and the iPhone Duo foldable (two displays, side bars, reserved regions).
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Inputs
- Navigation model
- Presentations and search
- Numbers
- Liquid Glass era notes (OS 26+)
- System surfaces
- Not available on iPhone
- iPhone Duo: anatomy and layout
- iPhone Duo: vertical controls
- iPhone Duo: arrangement views and API availability
- Common mistakes

## Device and context

- [HIG] Medium-size, high-resolution display, held in one or both hands, in portrait or landscape, viewed from no more than a foot or two.
- [HIG] Sessions range from a minute or two (checking, messaging) to an hour or more (media, games); people switch apps constantly, so save and restore state.
- [HIG] Limit onscreen controls so the primary task and content dominate; keep secondary details and actions discoverable with minimal interaction.
- [HIG] Reach: controls in the middle or bottom of the display are easier to reach than the top. Support swipe-to-go-back and swipe actions on list rows for that reason.
- [HIG] Adapt to orientation, Dark Mode and Dynamic Type; let people keep the configuration they chose.
- [HIG] With permission, use device capabilities (location, biometrics, payments) instead of asking people to type data.
- [HIG] Decide layout from size classes, not from "this is an iPhone" or from orientation; do not change functionality with the available space, only how much is visible.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ios, https://developer.apple.com/design/human-interface-guidelines/layout

## Inputs

- [HIG] Primary: Multi-Touch gestures, virtual keyboards, voice. Also personal data, gyroscope and accelerometer, spatial interactions.
- [HIG] Use the standard gestures (tap, swipe, drag, touch and hold, double tap, zoom, rotate) for their standard meanings; do not redefine three-finger undo/redo swipes, three-finger copy/paste pinch or shake to undo, and avoid conflicts with screen-edge system gestures.
- [HIG] Every gesture needs a visible alternative (a swipe-to-dismiss view also has a button).
- [HIG] Match the virtual keyboard type to the content and lay out against the keyboard layout guide so the keyboard never covers the active field.
- [HIG] There is no keyboard focus system on iOS and pointing devices have no iOS-specific guidance; design for touch first.
- [HIG] Full-screen games may defer system edge gestures so one accidental swipe does not exit; keep the default single swipe unless exits are a real problem.

Source: https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/going-full-screen

## Navigation model

- [HIG] Flat top-level sections: a tab bar, which floats above content at the bottom of the screen (OS 26+). Tabs are destinations only, never actions; do not hide or disable tabs; avoid overflow into a More tab; short single-word labels.
- [HIG] A tab bar may carry a dedicated search tab at its trailing end, and, when it has an attached accessory (a mini player), may minimize on scroll with the accessory moving inline (`TabBarMinimizeBehavior`, iOS 26.0+).
- [HIG] Hierarchy: push list levels in a stack. The top toolbar is what used to be called the navigation bar; the HIG no longer has a separate navigation bar page.
- [HIG] Use a large title for orientation; by default it collapses to a standard title on scroll and returns at the top.
- [HIG] Put only the most important items in the top toolbar; move the rest into a More menu. Use the standard Back and Close buttons with their symbols, not text labels "Back" or "Close".
- [HIG] Prefer split views in regular width, not in compact width such as iPhone in portrait.
- [HIG] There are no tab views on iOS; switch closely related sub-views with a segmented control (about five segments at most on iPhone).
- [HIG] Sidebars: consider a tab bar first.

See `references/components-navigation.md` for the component rules.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/tab-views

## Presentations and search

- [HIG] Sheets: the system detents are large (full height) and medium (about half); custom detents are allowed. Sheets support large automatically; add medium for progressive disclosure, omit it when content needs full height (compose views).
- [HIG] Show a grabber on resizable sheets and support swipe to dismiss; if there are unsaved changes when the swipe starts, confirm with an action sheet.
- [HIG] In a single-view sheet, Cancel goes on the leading edge of the top toolbar and Done on the trailing edge.
- [HIG] Avoid popovers in compact width; present a sheet instead.
- [HIG] Choices that follow an intentional action use an action sheet, not an alert and not a menu; avoid alerts and action sheets that scroll.
- [HIG] Give an item either a context menu or an edit menu, not both. Context menus can show a preview of the item.
- [HIG] Search has three possible entry points: a search tab (standard tab that opens a landing page, or button appearance that focuses the field immediately), a toolbar (bottom if there is room, otherwise top), or an inline field above the list it filters.
- [HIG] Switches belong in list rows; elsewhere use a button that behaves like a toggle. Do not use a slider for audio volume.

Source: https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/popovers, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/search-fields, https://developer.apple.com/design/human-interface-guidelines/context-menus

## Numbers

| Item | Value | Tag |
|---|---|---|
| Default / minimum text size | 17 pt / 11 pt | [HIG] |
| Default / minimum control size | 44x44 pt / 28x28 pt | [HIG] |
| Button hit region | at least 44x44 pt | [HIG] |
| Padding around bezeled / non-bezeled controls | about 12 pt / about 24 pt | [HIG] |
| Body text style at the default (Large) size | 17 pt, 22 pt leading | [HIG] |
| Large Title at the default size | 34 pt, 41 pt leading | [HIG] |
| Minimum text contrast | 4.5:1 for text up to 17 pt; 3:1 for 18 pt text and for bold text of any size | [HIG] |
| Text enlargement to support | at least 200% | [HIG] |
| Image scale factors | @2x and @3x | [HIG] |
| System font | SF Pro (New York also available) | [HIG] |

- [HIG] Dynamic Type runs xSmall to xxxLarge plus accessibility sizes AX1 to AX5; use text styles so layouts follow it, let rows grow and restack horizontal groups vertically at large sizes.
- [HIG] The HIG gives no tab bar height, bar icon size or screen margin value for iOS; it defers to system safe areas, layout margins and Apple Design Resources. Do not quote fixed values such as a 49 pt tab bar as HIG guidance.
- [HIG] Respect the safe area so the Dynamic Island, sensors and system UI never cover controls or text; extend backgrounds under bars.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/images

## Liquid Glass era notes (OS 26+)

- [API] Apps built with the current SDK get Liquid Glass on standard bars and controls automatically when running on iOS 26 or later.
- [API] `UIDesignRequiresCompatibility` (iOS 26.0+) kept the previous appearance temporarily; the system ignores it when you build for iOS 27 or later, so there is no opt-out in the current cycle.
- [HIG] Liquid Glass is the functional layer: tab bars, toolbars and controls float above content. Do not use it in the content layer; use standard materials (ultra-thin, thin, regular, thick) there.
- [HIG] Do not put a solid or semi-opaque background under bars; rely on the scroll edge effect and let content and backgrounds extend beneath them. Reduce custom bar backgrounds and tinted bar items.
- [HIG] Glass has no inherent color: emphasize one primary action by coloring its background (prominent style) rather than tinting several controls.
- [HIG] Provide light, dark and increased-contrast variants of every custom color even for a single-appearance app, because glass adapts to what is behind it.
- [Conv] When the deployment target is below iOS 26, the same code shows the earlier opaque-bar design on older systems: guard glass-only APIs with availability checks and check both looks.

See `references/platforms-detection.md` for finding the deployment target.

Source: https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/design/human-interface-guidelines/materials, https://developer.apple.com/documentation/bundleresources/information-property-list/uidesignrequirescompatibility

## System surfaces

- [HIG] iOS system features to integrate with: widgets, Home Screen quick actions, Spotlight, Shortcuts, activity views.
- [HIG] Lock Screen widgets come in inline, circular and rectangular styles; they follow complication principles and should show information, not act as a launcher.
- [HIG] Live Activities start on iPhone or iPad and show on the Lock Screen and in the Dynamic Island, and also appear in the Apple Watch Smart Stack, a paired Mac's menu bar and CarPlay. End them as soon as the task ends.
- [HIG] StandBy shows small-family widgets scaled up; mark the widget background removable and favor large text over color.
- [HIG] Always On display (iPhone models that have it): hide sensitive data, dim secondary content, keep the layout stable and make updates infrequent.
- [HIG] Multitasking on iPhone is app switching plus Picture in Picture for video and FaceTime; pause attention-demanding activity when people switch away and finish user-started tasks in the background.
- [HIG] A launch screen is required on iOS and should look nearly identical to the first screen, with no text and no branding.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ios, https://developer.apple.com/design/human-interface-guidelines/widgets, https://developer.apple.com/design/human-interface-guidelines/live-activities, https://developer.apple.com/design/human-interface-guidelines/always-on, https://developer.apple.com/design/human-interface-guidelines/multitasking, https://developer.apple.com/design/human-interface-guidelines/launching

## Not available on iPhone

[HIG] The HIG marks these as not supported in iOS; do not design them into an iPhone UI: windows, the menu bar, panels, tab views, keyboard focus and selection (focus system), Apple Pencil and Scribble, Mac Catalyst, the Digital Crown, remotes and Top Shelf, complications and watch faces, ornaments and immersive spaces, column views, outline views, combo boxes, token fields, path controls, image wells, Dock menus.

Source: https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/design/human-interface-guidelines/panels, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection

## iPhone Duo: anatomy and layout

iPhone Duo is a foldable iPhone (HIG page added September 9, 2026). It is still iPhone: all iOS guidance above applies.

- [HIG] Two displays: an outer display used when closed and a larger inner display used when open, joined by a center hinge. Each has a front camera: the outer one sits in a corner and is always visible; the inner one is behind the display and hidden until active.
- [HIG] Size classes: design a compact-width layout for the outer display and a regular-width layout for the inner display. Those two cover every pose (closed, open, partially folded like a book, set on a surface, standing on an edge).
- [HIG] Build to resize: the app also appears at other sizes in Split View multitasking on the inner display. Use size classes, layout margins and safe area insets; avoid fixed widths and anything tied to one display.
- [HIG] Do not design a custom layout per pose and do not reinvent the app when it resizes; let the existing layout expand.
- [HIG] Keep functionality and element state identical across displays and poses. Keep the information hierarchy, optionally showing one more level on the inner display (list or detail when closed, both side by side when open).
- [HIG] A split view expands on the inner display and collapses to one pane on the outer display, exactly as between regular and compact width elsewhere; standard split views also adjust column widths and margins around the fold.
- [HIG] Reserved regions shape the usable area in addition to the safe area: (1) the outer camera, always present, which expands into the Dynamic Island for Live Activities; (2) the inner camera, present only while the camera is active, when UI moves aside; (3) the folding region, present when the device is partially open, splitting the inner display into usable regions on either side of the center.
- [HIG] Alerts, context menus and sheets move away from the fold automatically. For custom components use `ReservedRegion` (SwiftUI) or `UIView.ReservedRegion` (UIKit) to keep important elements clear.
- [HIG] In grids prefer an even number of columns so content divides cleanly at the fold.
- [HIG] Avoid extreme layout changes while folding: move only what is needed to stay visible and tappable.
- [HIG] Games: locking to portrait or landscape is allowed, but fill the screen in every pose, keep text and control sizes consistent, and prefer changing aspect ratio to letterboxing; if bars are unavoidable, fill them with artwork.
- [HIG] Preview poses with Device Hub in Xcode.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo

## iPhone Duo: vertical controls

- [HIG] On the outer display, and on the inner display in landscape, the system moves the toolbar (including navigation buttons), the tab bar, the status bar and the Dynamic Island to the side to preserve vertical space. The inner display in portrait keeps standard horizontal bars.
- [HIG] Standard components get this automatically. In general do not override the default bar placement.
- [HIG] Side controls stay aligned with the hardware: same position relative to the outer camera, and the same side in right-to-left languages (they do not mirror).
- [HIG] In Split View multitasking on the inner display each app puts its controls on its outer edge, so content space is asymmetric; use safe areas so controls on either edge never cover content.
- [HIG] Order on the vertical axis: navigation controls (Back, Close) at the top, then prominent actions (Done), then the remaining items in their original groups.
- [HIG] Items overflow from bottom to top by default. Assign visibility priorities (groups first, then items) so frequent actions such as compose, and items carrying badges, stay visible longest.
- [HIG] Group related items with `ToolbarItemGroup` / `UIBarButtonItemGroup` instead of fixed spacing.
- [HIG] Give every non-text toolbar item both a title and a symbol; the title is used in overflow menus and expanded forms. Keep text-only buttons to a minimum because text labels stay in a horizontal bar.
- [HIG] Keep controls that act on a specific pane next to that pane (above the list they affect) instead of moving them to the side.
- [HIG] When space is tight, decide per screen: navigation-focused screens keep the tab bar and overflow toolbar items (the default); task-focused screens minimize the tab bar and keep the toolbar.
- [HIG] Use the system overflow menu; move any custom overflow menu's actions into it and reserve the ellipsis symbol for overflow.
- [HIG] Full-width layouts without bars suit non-scrolling, immersive screens (a calculator) as long as nothing collides with the Dynamic Island or status bar; a background or header may span the full width while scrolling content stays inset.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo

## iPhone Duo: arrangement views and API availability

- [HIG] An arrangement view holds a primary and a secondary view and arranges them by display size, orientation and reserved regions. Split arrangement: side by side when wider than tall, stacked when taller than wide (axes can be limited). Overlay arrangement: primary on top of secondary, moving to opposite sides of the fold when partially folded (the secondary view can be collapsed).
- [HIG] Reach for one when the layout already is two views side by side or stacked (split) or one layered over another (overlay).
- [HIG] Arrangement views do layout only: keep navigation containers (split views, tab views) around them, never inside them.

| API | Introduced | Tag |
|---|---|---|
| `ArrangementView`, `ReservedRegion` (SwiftUI) | iOS 27.1 | [API] |
| `UIArrangementViewController` (UIKit) | iOS 27.1 | [API] |
| `ToolbarVerticalCompressionBehavior` (SwiftUI) | iOS 27.1 | [API] |
| `ToolbarItemVisibilityPriority`, `ToolbarOverflowMenu` (SwiftUI) | iOS 27.0 | [API] |

- [Conv] A project whose deployment target is below 27.1 needs availability guards around these; the size-class and standard-bar guidance above needs no new API.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo, https://developer.apple.com/documentation/swiftui/arrangementview, https://developer.apple.com/documentation/swiftui/reservedregion, https://developer.apple.com/documentation/swiftui/toolbaritemvisibilitypriority

## Common mistakes

| Mistake | Fix |
|---|---|
| Actions in the tab bar, hidden or disabled tabs, a More tab | Tabs are destinations; put actions in a toolbar; trim sections |
| Opaque or tinted custom bar backgrounds on OS 26+ | Remove them; use the scroll edge effect and let content extend under bars |
| Glass effects on cards and content backgrounds | Glass is for controls and navigation; use standard materials in content |
| Primary actions only at the top of a tall screen | Keep frequent actions reachable (bottom toolbar, swipe actions) |
| Popover or multi-column split view in compact width | Sheet; single column that pushes |
| Text "Back"/"Close" buttons, crowded top bar | Standard symbols; essential items only, rest in a More menu |
| Fixed font sizes and layouts that clip at large Dynamic Type sizes | Text styles; rows grow; restack |
| Layout chosen by device model or orientation | Size classes and available space |
| iPhone Duo: hard-coded widths, display-specific layouts, features missing on one display | Size classes, margins, safe areas; same functionality everywhere |
| iPhone Duo: forcing bars back to top and bottom, custom ellipsis overflow menu | Keep default side placement; system overflow menu |
| iPhone Duo: important content across the fold or under the outer camera | Reserved regions; even column counts |
| Designing windows, a menu bar or keyboard focus for iPhone | Not supported on iOS |
