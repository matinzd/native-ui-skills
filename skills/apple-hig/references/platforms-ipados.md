# iPadOS (iPad)

Scope: what is specific to designing for iPad: top tab bar and sidebar-adaptable navigation, split views, resizable windows and multitasking, the iPad menu bar, keyboard focus, pointer, Apple Pencil, drag and drop, popovers and sheets, and the "stretched iPhone app" failure modes.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Navigation: tab bar first, sidebar when needed
- Split views and toolbars
- Windows and multitasking
- Menu bar
- Keyboard and focus
- Pointer
- Apple Pencil and Scribble
- Drag and drop
- Presentations and search
- Numbers and appearance
- Not available on iPad
- Common mistakes

## Device and context

- [HIG] Large, high-resolution display; held, set on a surface or on a stand; people are typically within about 3 feet.
- [HIG] Inputs combine freely: Multi-Touch, virtual keyboard, hardware keyboard, pointing device, Apple Pencil, voice. Support them together, not one at a time.
- [HIG] Sessions run from a few quick actions to hours of creation or productivity; several apps are often onscreen at once and people use drag and drop between them.
- [HIG] Use the large display to elevate content: minimize modal interfaces and full-screen transitions, and place controls where they are reachable but not in the way.
- [HIG] Let viewing distance and input mode set size and density.
- [HIG] Adapt to orientation, multitasking modes, Dark Mode and Dynamic Type, and make the design carry over cleanly to running in macOS.
- [HIG] Lay out by size class and available space. An iPad window can be compact width; do not assume regular width or a particular orientation, and never change functionality with size.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados, https://developer.apple.com/design/human-interface-guidelines/layout

## Navigation: tab bar first, sidebar when needed

- [HIG] The tab bar sits near the top of the screen on iPad, not at the bottom.
- [HIG] Prefer a tab bar for top-level navigation. For more complex apps, offer the form that converts to a sidebar so people can reach a wider set of destinations.
- [API] SwiftUI tab view styles: `tabBarOnly` (fixed bar) and `sidebarAdaptable` (bar with a button that converts it to a sidebar); `sidebarAdaptable` is iOS/iPadOS 18.0+.
- [HIG] With `sidebarAdaptable` you choose whether the app opens showing the sidebar or the tab bar; the control adapts to rotation and window width by itself.
- [HIG] For a sidebar with no tab-bar form, use a navigation split view (`NavigationSplitView` or `UISplitViewController`) instead of a tab view.
- [HIG] Let people customize the tab bar in apps with many sections; keep the default set to five or fewer so compact and regular widths stay consistent.
- [HIG] Sidebars show at most two levels of hierarchy; deeper structures need a content-list column. Let people hide the sidebar, but do not hide it by default.
- [HIG] Same tab bar rules as iPhone: destinations only, no hidden or disabled tabs.

See `references/components-navigation.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/sidebars, https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable

## Split views and toolbars

- [HIG] Split views have two or three vertical panes (sidebar, optional content list, detail). Keep the current selection highlighted in each pane that leads to the detail.
- [HIG] Because windows resize fluidly, design every split view for narrow, compact and intermediate widths and make moving between panes logical at each.
- [HIG] A toolbar and the tab bar can share the same row at the top, which keeps the full window width for content.
- [HIG] Do not add your own overflow menu; the system adds one when toolbar items do not fit. Avoid layouts that overflow by default.
- [HIG] If the app also ships on the Mac through Mac Catalyst, present an inspector next to the main content there instead of a popover.

Source: https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/mac-catalyst

## Windows and multitasking

- [HIG] People choose in Multitasking & Gestures settings between Full screen (each app window fills the screen; switch with the app switcher) and Windowed (freely resizable, overlapping, repositionable windows; the system remembers size and placement).
- [Req] Apps cannot control the multitasking configuration and receive no indication of which one is in use. The only correct strategy is a layout that adapts to any size.
- [HIG] In windowed mode the system draws window controls at the leading edge of the toolbar. Move leading toolbar buttons inward when the controls appear so they are not covered.
- [HIG] The frontmost window is identified by colored window controls and a drop shadow on windows behind it; do not draw custom window chrome or imitate system window UI.
- [HIG] An app can have several windows. Open a new window when it helps people multitask or keep context (compose alongside the inbox); do not open windows by default without that benefit.
- [HIG] Offer "open in new window" in a context menu or the File menu, and consider a gesture such as pinch-to-expand an item into its own window.
- [HIG] Primary windows carry navigation; auxiliary windows hold one task, offer no navigation elsewhere and include a close/done button.
- [HIG] Say "window" in user-facing text, never "scene".
- [API] `UIRequiresFullScreen` is deprecated (iOS/iPadOS 26.0). On iPadOS 26+ it no longer makes the app full screen: the system keeps a fixed scene size and scales the app. Remove it and support resizing.
- [API] Multiple windows require `UIApplicationSupportsMultipleScenes` set to true in the scene manifest (iOS 13.0+).
- [HIG] Picture in Picture video and FaceTime float above content in either mode. Save and restore context, pause attention-demanding activity on switch-away, and finish user-started tasks in the background.

Source: https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/multitasking, https://developer.apple.com/documentation/bundleresources/information-property-list/uirequiresfullscreen

## Menu bar

- [HIG] iPad has a menu bar: people reveal it by moving the pointer to the top edge of the screen or swiping down from it. It shows system-provided menus plus the app's custom menus.
- [HIG] Use the same menu order and item sets as the Mac: app menu, File, Edit, Format, View, app-specific menus, Window, Help. Keyboard shortcuts follow the same patterns as macOS.
- [HIG] The menu bar is often hidden, so every function must also be reachable in the app's UI. Never make the menu bar the only path, and always provide another way to do what a dynamic (modifier-key) menu item does, since those need a hardware keyboard.
- [HIG] Always show the same set of items; disable unavailable ones instead of hiding them.
- [HIG] Reserve the app menu's Settings item for opening the app's page in iPadOS Settings. Link an in-app preferences area with a separate item directly beneath it.
- [HIG] For tab-based apps, list each tab in the View menu and consider giving each a key binding.
- [HIG] Menu rows are taller than on the Mac; group related items into submenus more readily to save vertical space.
- [API] SwiftUI `commands` and `CommandMenu` are available on iOS/iPadOS 14.0+; UIKit uses `UIMenuBuilder`, `UICommand` and `UIKeyCommand`.

Source: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/documentation/swiftui/commandmenu

## Keyboard and focus

- [HIG] iPadOS 15 and later has a keyboard focus system for text fields, text views, sidebars, collection views and custom views.
- [HIG] Focus groups: Tab moves between groups (sidebar, grid, list) in reading order, leading to trailing and top to bottom; arrow keys move among items inside the current group.
- [HIG] Support focus for content elements (list items, text fields, search fields). Do not add your own keyboard navigation for buttons, segmented controls, sliders and switches; Full Keyboard Access covers those.
- [HIG] Focus appearance: the halo (focus ring) for text and search fields and for opaque cell content such as images; a highlight for rows in lists and collections. Rely on system focus effects.
- [HIG] Do not move focus without the person's interaction. For custom views, set focus group identifiers and priorities so Tab order and the group's primary item make sense.
- [HIG] Keep standard shortcuts for their standard commands; add custom shortcuts only for frequent commands, with Command as the main modifier. iPad users find commands in the app UI or in the shortcut interface shown while holding the Command key.
- [HIG] Do not auto-focus a search field in a dedicated search area when only the virtual keyboard is available; the keyboard would cover the view unexpectedly.

Source: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/keyboards, https://developer.apple.com/design/human-interface-guidelines/search-fields

## Pointer

- [HIG] The pointer is an additional input and does not replace touch; behaviour must be consistent whether people use touch, pointer or keyboard, including modifier-key drags.
- [HIG] System content effects: highlight (a Liquid Glass shape behind bar buttons, tab bars, segmented controls, edit menus), lift (scale, shadow and specular highlight) and hover (custom scale, tint or shadow).
- [HIG] Choose by element: highlight for controls grouped inside a Liquid Glass container; lift for a standalone glass control or small opaque element; hover for large elements. Do not scale elements that cannot grow without overlapping neighbours, such as table rows.
- [HIG] Hit regions: add padding of about 12 pt around bezeled elements and about 24 pt around elements without a bezel. Make hit regions of adjacent custom bar buttons contiguous so the highlight does not flicker between them.
- [HIG] Let the pointer reveal controls that auto-minimize or fade, but never make hover the only way to reach them.
- [HIG] Support band selection (click and drag a rectangle) for multiple selection in custom views; standard non-list collection views do this already.
- [HIG] Distinguish pointer from finger input only when it adds value (a precise scrub position). Keep custom pointer shapes simple, avoid decorative effects and never attach instructional text to the pointer.
- [HIG] Context menus open on touch and hold or on secondary click. On iPad, a context menu on empty space is a good way to create a new object.

Source: https://developer.apple.com/design/human-interface-guidelines/pointing-devices, https://developer.apple.com/design/human-interface-guidelines/context-menus

## Apple Pencil and Scribble

Apple Pencil guidance applies to iPadOS only.

- [HIG] Mark the moment the Pencil touches the screen: no mode switch or button first. Controls must also respond to Pencil so people need not switch to a finger.
- [HIG] Respond to tilt, force, orientation and barrel roll where it affects strokes; barrel roll only modifies marking, never navigation.
- [HIG] Hover previews what a mark would look like; never trigger an action from hover. Prefer hover previews for Pencil, not for the pointer.
- [HIG] Respect the person's double-tap setting; do not use double tap or squeeze for actions that modify content destructively. Treat squeeze as one quick discrete action and show any resulting UI near the Pencil tip.
- [HIG] Design for left- and right-handed use: avoid controls where either hand hides them, or let people move them.
- [HIG] Scribble works in standard text components by default (not password fields). While people write: keep the field still, do not autoscroll, avoid distracting autocompletion, and give enough room to write.

Source: https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble

## Drag and drop

- [HIG] Support drag and drop widely, between and within apps, and always provide a non-drag alternative. As a general rule a drop in the same container moves content and a drop in a different container copies it.
- [HIG] Support multi-item drags: people add items to a drag in progress, so show flocking feedback and accept multiple simultaneous drops.
- [HIG] Show valid and invalid destinations clearly and make drops undoable where possible.
- [HIG] Supporting drag and drop on iPad also gives the Mac Catalyst version drag and drop.

Source: https://developer.apple.com/design/human-interface-guidelines/drag-and-drop, https://developer.apple.com/design/human-interface-guidelines/mac-catalyst

## Presentations and search

- [HIG] Prefer the page or form sheet styles: a default-size sheet centered over a dimmed background. Avoid full-screen modal flows where a sheet, popover or split-view column would keep context.
- [HIG] Popovers suit regular width: small amount of content, arrow pointing at the source, one at a time, never a cascade. In compact-width windows present a sheet instead, deciding by size class.
- [HIG] Sheet button placement matches iPhone: Cancel leading, Done trailing; support swipe to dismiss.
- [HIG] Search placement: trailing side of the toolbar for most apps (especially split views); top of the sidebar when it filters the sidebar; a dedicated sidebar or tab item when search is a discovery area. Keep it consistent with the Mac version.
- [HIG] When the window becomes compact, move search to where it is contextually useful (above the content-list column).

Source: https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/popovers, https://developer.apple.com/design/human-interface-guidelines/search-fields

## Numbers and appearance

| Item | Value | Tag |
|---|---|---|
| Default / minimum text size | 17 pt / 11 pt | [HIG] |
| Default / minimum control size | 44x44 pt / 28x28 pt | [HIG] |
| Pointer hit-region padding, bezeled / no bezel | about 12 pt / about 24 pt | [HIG] |
| Default customizable tab set | five or fewer | [HIG] |
| Image scale factor | @2x | [HIG] |

- [HIG] Dynamic Type and Dark Mode are supported, as on iPhone; the Always On display is not.
- [API] Liquid Glass (OS 26+) applies to standard bars, sidebars and controls as on iPhone; the same content-layer and bar-background rules apply (see `references/platforms-ios.md`).
- [HIG] Extend rich content and backgrounds beneath sidebars and bars.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/images, https://developer.apple.com/design/human-interface-guidelines/always-on, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass

## Not available on iPad

[HIG] Marked not supported in iPadOS: panels, tab views (use a segmented control), column views, outline views, combo boxes, token fields, path controls, image wells, Dock menus, the Digital Crown, the Action button, Camera Control, Always On, CarPlay, complications, Top Shelf, ornaments and immersive spaces.

Source: https://developer.apple.com/design/human-interface-guidelines/panels, https://developer.apple.com/design/human-interface-guidelines/tab-views

## Common mistakes

| Mistake (often a stretched iPhone app) | Fix |
|---|---|
| One phone-width column centered or stretched across the display | Split view with two or three columns in regular width; collapse in compact |
| Tab bar forced to the bottom, or sidebar-only when a tab bar would do | System tab bar at the top; `sidebarAdaptable` for many sections |
| Every flow presented as a full-screen modal | Form/page sheet, popover, inspector or a split-view column |
| Assuming full screen, a fixed size or one orientation; `UIRequiresFullScreen` | Resizable layout by size class; remove the key |
| Leading toolbar buttons hidden under window controls | Inset them when the window controls appear |
| Commands reachable only from the menu bar, or no menu bar commands at all | Provide both: UI for everything, menus and shortcuts for everything important |
| App menu Settings item opens an in-app screen | Reserve it for the system Settings page; add a separate item below |
| No keyboard focus, shortcuts, pointer effects or secondary-click menus | Add focus groups, standard shortcuts, system pointer effects, context menus |
| Hover-only controls | Also show on touch and offer the action in a context menu |
| Popover in a narrow window | Sheet in compact width |
| Touch-only assumptions with a Pencil or pointer attached | Controls respond to Pencil and pointer; consistent behaviour across inputs |
| Layout branching on `userInterfaceIdiom == .pad` | Branch on size class and available width |
