# macOS (Mac)

Scope: what is specific to designing for the Mac: the menu bar, windows and their states, toolbars, sidebars and split views, keyboard-first operation, pointer precision and density, the Settings window, no Dynamic Type, touch-display guidance, and notes for Mac Catalyst and iPad apps running on a Mac.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Menu bar
- Windows
- Toolbars, sidebars and split views
- Keyboard and pointer
- Density, type and appearance
- Settings window
- Sheets, alerts, popovers and panels
- Touch on a Mac with a touch display
- Mac Catalyst
- iPad and iPhone apps running on a Mac
- Not available on the Mac
- Common mistakes

## Device and context

- [HIG] Large, high-resolution display, often several displays (including an iPad through Sidecar); used while stationary at a desk or table.
- [HIG] Keyboard and pointing device are the primary inputs. Trackpad gestures, touch on a Mac with a touch display, Siri, Voice Control and game controllers are additional.
- [HIG] Sessions run from minutes to hours of concentration with many apps and windows open; people expect smooth transitions between active and inactive states.
- [HIG] Use the space to show more content with fewer nested levels and less modality, at a comfortable density. Let people resize, hide, show and move windows, and support full-screen mode.
- [HIG] Put every command in the menu bar; handle keyboard shortcuts and keyboard-only work styles; support high-precision selection and editing.
- [HIG] Allow personalization: customizable toolbars, window configurations, and the person's chosen colors and fonts.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-macos

## Menu bar

The menu bar is essential on the Mac: people use it to learn what an app does and to find every command.

| Menu, in order | Notes |
|---|---|
| Apple menu | System-owned, always first; cannot be modified |
| YourAppName | About (first, alone in its group; short name of 16 characters or fewer), Settings..., optional app-level items, Services, Hide, Hide Others, Show All, Quit |
| File | New, Open, Open Recent, Close, Save, Duplicate, Rename..., Move To..., Export As..., Revert To, Page Setup..., Print... Rename or drop the menu if the app has no files |
| Edit | Undo, Redo, Cut, Copy, Paste, Paste and Match Style, Delete, Select All, Find, Spelling and Grammar, Substitutions, Transformations, Speech. Useful even in non-document apps |
| Format | Only for apps with formatted text |
| View | Show/Hide Tab Bar, Show All Tabs, Show/Hide Toolbar, Customize Toolbar, Show/Hide Sidebar, Enter/Exit Full Screen |
| App-specific menus | Between View and Window, most general first, mirroring the app's hierarchy |
| Window | Minimize, Zoom, tab commands, Bring All to Front, list of open windows |
| Help | At the trailing end |

- [HIG] Keep the system-defined menus and their order. Always show the same items; disable an unavailable item instead of hiding it.
- [HIG] List custom commands in the menu bar even when they are available elsewhere.
- [HIG] Provide a View menu even if the only item is Enter/Exit Full Screen; make each Show/Hide title reflect the current state.
- [HIG] Provide a Window menu even for a single-window app, with Minimize and Zoom, so keyboard users can invoke them.
- [HIG] Support the standard shortcuts for the standard items you include; define custom shortcuts only when necessary. Prefer one-word menu titles and the system's standard icons for common actions.
- [HIG] Dynamic menu items (revealed by one modifier key, such as Option turning Minimize into Minimize All) must never be the only way to do something.
- [HIG] Menu bar extras: use a symbol; show a menu, not a popover, unless the function is too complex; let people decide whether the extra is shown; never rely on it being visible; consider a Dock menu as well.

Source: https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/design/human-interface-guidelines/dock-menus

## Windows

- [HIG] A window has a frame (title bar, window controls, toolbar; rarely a bottom bar) and a body. People move, resize, minimize and zoom windows constantly; design every window to adapt fluidly to size.
- [HIG] Three states: main (an app's frontmost window, one per app), key (the window receiving input, one onscreen at a time; may be a panel) and inactive. The system draws them differently (colored versus gray window controls; inactive windows do not use vibrancy).
- [HIG] Use system components so appearance follows window state automatically; custom views must implement the state appearances themselves.
- [HIG] Do not create custom window frames or controls, and do not imitate the system ones. Do not title a window with the app name.
- [HIG] Avoid controls or critical information at the bottom of a window (or in a bottom bar, or at the bottom of a sidebar): people often move windows so the bottom edge is offscreen. For more detail than a small bottom bar holds, use an inspector on the trailing side of a split view.
- [HIG] Avoid content behind the camera housing at the top of the display.
- [HIG] Open a new window when it helps multitasking or preserves context; offer "open in new window" in a context menu or the File menu; do not open windows by default without that benefit.
- [HIG] Full screen: use the system full-screen experience (it handles the camera housing); let people choose when to enter, through the window's button, the View menu or Control-Command-F; do not offer a custom menu of window modes; never resize windows programmatically; games must not change the display mode.
- [HIG] Multitasking is the default state on the Mac: keep working when inactive, and do not pause video because another window became key.

Source: https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/going-full-screen, https://developer.apple.com/design/human-interface-guidelines/multitasking

## Toolbars, sidebars and split views

- [HIG] The toolbar lives in the window frame, below or integrated with the title bar; titles can sit inline with controls; toolbar items have no bezel.
- [HIG] Make every toolbar item also available as a menu bar command, because people can customize or hide the toolbar. The reverse is not needed: not every menu command deserves a toolbar item.
- [HIG] The system adds an overflow menu when items do not fit; do not add one manually.
- [HIG] There are no tab bars on the Mac for app navigation. Use a sidebar in a split view for top-level navigation and tab views for switching closely related panes inside a window (no more than six tabs).
- [HIG] Sidebar rows come in small, medium and large sizes that follow the person's sidebar icon size in General settings; do not fix row metrics.
- [HIG] Consider hiding and revealing the sidebar automatically as the window resizes; let people hide it, but not by default.
- [HIG] Split views can be arranged vertically, horizontally or both, with draggable dividers. Set minimum and maximum pane sizes that keep the divider visible; prefer the thin divider (1 pt wide).
- [HIG] Let people hide panes, and give several ways to bring them back: a toolbar button and a menu command with a keyboard shortcut.
- [HIG] Hierarchies use outline views or column views; tables should support sorting and column resizing. Search goes at the trailing side of the toolbar, or at the top of the sidebar when it filters the sidebar.

See `references/components-navigation.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/sidebars, https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/tab-views, https://developer.apple.com/design/human-interface-guidelines/search-fields

## Keyboard and pointer

- [HIG] The whole app must be usable from the keyboard: menus with standard shortcuts, plus focus for content elements (lists, text fields, search fields). Full Keyboard Access reaches individual controls.
- [HIG] Focus appearance: focus ring for text and search fields; highlighted rows in lists (accent-colored highlight with white text when focused, gray highlight when not).
- [HIG] Do not repurpose standard shortcuts. For custom ones, Command is the main modifier, Shift secondary, Option sparingly, avoid Control; list modifiers in the order Control, Option, Shift, Command.
- [HIG] Support Esc and Command-Period for cancelling alerts and sheets, and undo/redo in the Edit menu with their standard shortcuts.
- [HIG] Do not redefine systemwide trackpad gestures; people can customize them and expect them everywhere, including in games.
- [HIG] Use the standard pointer styles to signal state and drag results (arrow, I-beam, open and closed hand, drag copy, drag link, operation not allowed, disappearing item).
- [HIG] Mac users expect a context menu (contextual menu) of relevant actions on essentially every object. In Mac context menus, keep Cut, Copy and Paste visible but dimmed when unavailable; hide other unavailable items.
- [HIG] Drag and drop: support dragging content to the Finder in a format the app can reopen; allow dragging a background selection out of an inactive window without activating it; let people select and drag in one motion; badge multi-item drags.

Source: https://developer.apple.com/design/human-interface-guidelines/keyboards, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/pointing-devices, https://developer.apple.com/design/human-interface-guidelines/context-menus, https://developer.apple.com/design/human-interface-guidelines/drag-and-drop

## Density, type and appearance

| Item | Value | Tag |
|---|---|---|
| Default / minimum text size | 13 pt / 10 pt | [HIG] |
| Default / minimum control size | 28x28 pt / 20x20 pt | [HIG] |
| Body | 13 pt, 16 pt leading | [HIG] |
| Large Title / Title 1 / Title 2 / Title 3 | 26 / 22 / 17 / 15 pt | [HIG] |
| Headline / Callout / Subheadline / Footnote / Caption | 13 (bold) / 12 / 11 / 10 / 10 pt | [HIG] |
| Image scale factors | @1x and @2x | [HIG] |
| System font | SF Pro (New York available to Mac Catalyst apps) | [HIG] |

- [HIG] macOS does not support Dynamic Type. Text styles exist but do not scale with a system text-size setting; do not promise Dynamic Type behaviour on the Mac.
- [Conv] If readable text size matters (editors, readers), offer an in-app text size or zoom command in the View menu, since the system will not scale the text.
- [HIG] Dark Mode is supported. The app accent color applies only when the person's accent setting is multicolor; otherwise their chosen accent wins. With the graphite accent, windows pick up desktop tinting, so include some transparency in custom component backgrounds.
- [API] Liquid Glass (macOS 26+) arrives through standard components; `UIDesignRequiresCompatibility` is ignored when building for macOS 27 or later.
- [HIG] Haptics: only when a Magic Trackpad is available, with three patterns (alignment, level change, generic) for drags and force clicks. Never rely on them.

Source: https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/color, https://developer.apple.com/design/human-interface-guidelines/dark-mode, https://developer.apple.com/design/human-interface-guidelines/playing-haptics

## Settings window

- [HIG] Settings open from the Settings item in the App menu with Command-Comma. Do not put a settings button in a window toolbar. Document-level options go in the File menu.
- [HIG] The settings window has a non-customizable, always-visible toolbar whose buttons switch between panes, and it always indicates the active pane.
- [HIG] Dim the minimize and zoom buttons; the window sizes itself to the current pane.
- [HIG] Title the window with the current pane's name; with a single pane, use "App Name Settings".
- [HIG] Reopen to the most recently viewed pane. [API] SwiftUI provides the `Settings` scene (macOS 11.0+).

Source: https://developer.apple.com/design/human-interface-guidelines/settings, https://developer.apple.com/documentation/swiftui/settings

## Sheets, alerts, popovers and panels

- [HIG] A sheet is a card attached to its parent window, which dims and is blocked; other windows of the app must stay usable and people must be able to bring them forward.
- [HIG] Give sheets a sensible default size; resizing is optional but welcome when content benefits.
- [HIG] For repeated input with visible results (find and replace), use a panel, not a sheet.
- [HIG] Popovers can be detachable: dragged away they become a panel that stays visible; keep the detached appearance close to the original.
- [HIG] Consider Window menu items for showing and hiding panels. A push button that opens another window, view or app gets a trailing ellipsis in its title.

Source: https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/popovers, https://developer.apple.com/design/human-interface-guidelines/panels

## Touch on a Mac with a touch display

Guidance added to the HIG on October 28, 2026. Touch is a secondary input: people reach forward for brief, intentional touches, not sustained work.

- [HIG] Keep layout and the size of interface elements the same when touch is supported; people switch inputs constantly and the interface must stay stable.
- [HIG] Make tap targets bigger, not the controls: extend the hit area beyond the visual bounds. Standard framework controls get suitable tap targets automatically.
- [HIG] For small or dense controls, consider a temporary expanded variant that appears on touch and lingers briefly after the finger lifts; system steppers, sliders and dials do this already.
- [HIG] Never make touch the only way to reach a control or feature; everything works with keyboard and pointing device. Conversely, give touch equivalents for pointer-only actions such as modifier drags and hover menus.
- [HIG] Hover-revealed controls: reveal essential ones when the person taps their general location, only those relevant to the current content, and hide them again after use or a few seconds. Keep the current selection when revealing. Also put essential hidden controls in a context menu (touch and hold opens it). Skip touch support for static information such as tooltips.
- [HIG] Sidebars reveal hidden controls when a section header or row is tapped; a tabbed window shows the selected tab's close button after a tap anywhere in the window.
- [HIG] Reuse gestures people know from iPhone, iPad and the trackpad; custom gestures must work for both touch and trackpad and must not conflict with system gestures.

Source: https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/pointing-devices, https://developer.apple.com/design/human-interface-guidelines/designing-for-macos

## Mac Catalyst

- [HIG] Good candidates are iPad apps that already support drag and drop, keyboard navigation and shortcuts, multitasking/resizing and multiple windows. Apps whose core depends on gyroscope, accelerometer, rear camera, HealthKit, ARKit, or on marking, handwriting or navigation may not suit the Mac.
- [HIG] Catalyst supplies pointer and keyboard focus support, window management, toolbars, rich text interaction, file management, menu bar menus and app settings in the system Settings app automatically; split views, activity views, form sheets and color pickers take a more Mac-like look.
- [HIG] iPad idiom ("Scale Interface to Match iPad", Xcode's default): iPadOS views and text are scaled to 77%, so 17 pt iPad text renders at 13 pt. Little layout work, slightly less crisp text and graphics.
- [HIG] Mac idiom ("Optimize Interface for Mac"): text and views render at 100%, controls look and behave like AppKit controls. Audit the whole layout, adjust font sizes (prefer text styles over fixed sizes), consider a separate asset catalog, and limit appearance customizations to ones macOS controls support.
- [API] In the Mac idiom `userInterfaceIdiom` is `.mac`; `UIPageControl` is unavailable there and throws if displayed.
- [HIG] Either way, go beyond showing the iPad layout in a window: replace the tab bar with a sidebar split view (preferred) or a segmented control, and list the former tabs in the View menu.
- [HIG] Put every command in the menu bar; pop-up and pull-down button menus and context menus convert automatically; add context menus to more objects.
- [HIG] Lay out for the wider window: multiple columns, side-by-side reflow as the window resizes, inspector instead of popover, top-down flow, controls moved from the bottom and side edges into the window toolbar. Offer Next and Previous buttons as well as swipe paging, and provide a macOS app icon.

Source: https://developer.apple.com/design/human-interface-guidelines/mac-catalyst, https://developer.apple.com/documentation/uikit/choosing-a-user-interface-idiom-for-your-mac-app

## iPad and iPhone apps running on a Mac

- [API] An unmodified iPhone or iPad app can run on a Mac with Apple silicon ("Designed for iPad" destination) using the same infrastructure as Catalyst, without recompiling for macOS. No Mac-specific UI can be added in this mode.
- [API] iPad apps that support multitasking get resizable windows; iPad apps that do not, and all iPhone apps, run in a fixed-size window.
- [API] The system adds a Touch Alternatives pane to the app's Settings window that maps keyboard keys to taps, swipes and drags; iOS keyboard shortcuts carry over.
- [API] Do not assume window size or position, multifinger touch, iOS-only hardware, or that the device is an iPhone or iPad. Prefer feature checks; `isiOSAppOnMac` is a last resort.
- [API] Developers can opt the app out of the Mac in App Store Connect when a native or Catalyst Mac app exists or the app depends on unavailable hardware or extensive custom multifinger gestures.
- [Conv] Design guidance for this mode is iPad guidance: resizable layout, keyboard shortcuts, pointer effects and context menus (see `references/platforms-ipados.md`). Say explicitly that Mac conventions such as a custom Settings window are out of reach without Catalyst or a native target.

Source: https://developer.apple.com/documentation/apple-silicon/running-your-ios-apps-in-macos

## Not available on the Mac

[HIG] Marked not supported in macOS: Dynamic Type, status bars, page controls, virtual keyboards, activity views, Home Screen quick actions, App Clips, Always On, the Digital Crown, Apple Pencil and Scribble, remotes and Top Shelf, complications, ornaments and immersive spaces. Tab bars have no macOS-specific guidance; app navigation uses sidebars.

Source: https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/status-bars, https://developer.apple.com/design/human-interface-guidelines/page-controls, https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards

## Common mistakes

| Mistake | Fix |
|---|---|
| Commands only in the toolbar or in buttons | Every command in the menu bar, with standard shortcuts |
| Menu items that appear and disappear | Keep them; disable when unavailable |
| No Window or View menu in a simple app | Provide both (Minimize, Zoom; Enter Full Screen) |
| Gear button in the toolbar for settings | App menu Settings item, Command-Comma, dedicated Settings window |
| Touch-sized controls and 17 pt body text | 13 pt body, 28 pt default controls, denser layout |
| Promising Dynamic Type on macOS | Not supported; offer in-app text sizing where it matters |
| Actions or status at the bottom of the window or sidebar | Move to the toolbar, the top of the content, or an inspector |
| Custom title bar or traffic-light look-alikes | System window frame and controls |
| Sheet that blocks the whole app, or used for repeated input | Sheet blocks only its parent; panel for repeated input |
| iOS-style bottom tab bar or page dots | Sidebar or tab view; Next/Previous controls |
| Hover-only controls with no alternative | Context menu entry; reveal on tap on touch displays |
| Enlarging controls for touch displays | Enlarge tap targets only; layout unchanged |
| Catalyst app left as an iPad layout in a window | Sidebar, menus, toolbar, context menus, multi-column layout |
