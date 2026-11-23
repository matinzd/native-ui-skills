# Navigation components

Scope: choosing and configuring tab bars, sidebars, toolbars (including what used to be navigation bars), split views, search fields, tab views and path controls on every Apple platform.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Which container
- Tab bars
- Sidebars
- Toolbars: general rules
- Toolbars: titles, Back and Close (former navigation bar guidance)
- Toolbars: actions and item grouping
- Toolbars: platform differences
- Split views
- Search fields and search placement
- Tab views, path controls, page-based navigation
- Common mistakes

## Which container

The HIG has no "navigation bars" page any more (its guidance was merged into Toolbars on June 9, 2025) and no page that names "flat / hierarchical / content-driven" structures. The first column below is a [Conv] classification; the cells are what the component pages recommend.

| App structure | iOS (compact width) | iPadOS | macOS | tvOS | visionOS | watchOS |
|---|---|---|---|---|---|---|
| A few peer top-level sections (flat) | Tab bar (floats at the bottom) | Tab bar (near the top); prefer it over a sidebar | Sidebar; tab view for related panes inside a window | Tab bar (top) | Tab bar (vertical, leading side) | Vertical tab view (pages, Digital Crown); no tab bar |
| Many sections or user collections (folders, playlists) | Tab bar; avoid overflow into a More tab | Tab bar that converts to a sidebar (`sidebarAdaptable`) or a sidebar-only split view | Sidebar in a split view | Tab bar; split view for filtering | Tab bar plus a sidebar inside a tab | List, then detail |
| Hierarchy, drill-down | List rows with disclosure indicators, toolbar Back button, large title | Split view, 2 or 3 panes | Split view; outline or column view | Split view (1/3 + 2/3 by default) | Split view inside the window | Split view shows list or detail full screen |
| Hierarchy deeper than 2 levels | Push list levels | Split view with a content-list pane between sidebar and detail | Same | n/a | Same | Keep shallow |
| Switching related sub-views of one screen | Segmented control | Segmented control | Tab view in the window body; segmented control in toolbar or inspector | Split view preferred for filtering | Segmented control | Vertical tab view |
| Ordered peer pages (content-driven) | Page control over a paging scroll view | Same | Not supported (page control) | Page control on full-screen pages | Page control (display only) | Vertical pagination |

- [HIG] Tab bars are for navigation between sections; toolbars are for actions on the current view. Never swap the two roles.
- [HIG] Do not change what the app can do when the available space changes; only change presentation (for example tab bar to sidebar). See `references/components-content.md` for list, outline and column views.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/sidebars, https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/layout

## Tab bars

- [HIG] Use a tab bar only to switch between top-level sections. Controls that act on the current view belong in a toolbar.
- [HIG] Keep the tab bar visible as people move within a section; the only exception is a modal view that covers it.
- [HIG] No numeric tab limit is stated. Use as many tabs as the hierarchy needs, remembering that fewer are easier to navigate; for complex structures consider a sidebar or an adaptable tab bar.
- [HIG] Avoid overflow. When tabs do not fit on iOS or iPadOS the trailing tab becomes a More tab, which hides content; limit the cases where this happens.
- [HIG] Never hide or disable a tab because its content is unavailable. Keep it enabled and explain why the section is empty.
- [HIG] Give every tab a label, one word where possible.
- [HIG] Prefer SF Symbols, and prefer filled variants. Icons sit above labels in compact layouts and beside them in regular layouts; custom icon dimensions come from Apple Design Resources, not the HIG text.
- [HIG] A badge (red oval, white number or exclamation point) is for critical information only.
- [HIG] (OS 26+, Liquid Glass) Do not give tab labels a color close to the content behind the bar; over colorful content prefer the monochrome appearance or a clearly distinct accent.

| Platform | Behaviour and rules |
|---|---|
| iOS | [HIG] (OS 26+) Floats above content at the bottom on a Liquid Glass background. With an attached accessory (for example a mini player) the bar may minimize on scroll-down and restore on tab tap or scroll-to-top (`TabBarMinimizeBehavior`). May carry a dedicated search tab at the trailing end. |
| iPadOS | [HIG] Appears near the top. Choose fixed (`tabBarOnly`) or convertible to a sidebar (`sidebarAdaptable`). Prefer a tab bar; offer the sidebar conversion for complex apps. Let people customize tabs; if they can, ship a default set of five or fewer so compact and regular widths stay consistent. |
| macOS | No additional considerations on the page. |
| tvOS | [Req] Height is 68 pt and the top edge sits 46 pt from the top of the screen; neither can be changed. [HIG] The bar can scroll offscreen in single-view tabs, stays pinned above a split view, and regains focus when Menu is pressed. Extra items are truncated with a fade. Live-viewing apps order tabs: live, cloud DVR or recorded, other. |
| visionOS | [HIG] Always vertical, fixed to the window's leading side, expands when looked at. Supply both a symbol and a short text label per tab. A sidebar inside a tab may add secondary navigation, but its selections must not change the open tab. |
| watchOS | Not supported. |

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars

## Sidebars

- [HIG] A sidebar needs a lot of horizontal and vertical space. When space is limited prefer a tab bar, or a tab bar style that offers both.
- [HIG] Show at most two levels of hierarchy in a sidebar. Deeper data calls for a split view with a content list between sidebar and detail.
- [HIG] With two levels, title each group with a short descriptive label; collapse large groups with disclosure controls.
- [HIG] Let people customize sidebar contents and order when possible.
- [HIG] Let people hide the sidebar using platform conventions (iPadOS edge swipe; macOS show/hide button or View menu commands), but do not hide it by default.
- [HIG] Prefer SF Symbols or custom symbols over bitmap icons for rows.
- [HIG] Sidebar icons use the app accent color by default. On macOS they must follow the accent color the user chooses; use fixed colors only sparingly and for a clear purpose.
- [HIG] (OS 26+, Liquid Glass; iOS, iPadOS, macOS) The sidebar floats above content. Extend rich content beneath it by horizontal scrolling or a background extension effect (`backgroundExtensionEffect()`).

| Platform | Rules |
|---|---|
| iOS, iPadOS | [HIG] Consider a tab bar first. `sidebarAdaptable` lets you choose which form shows at launch and gives people a switch button. For a sidebar with no tab bar form, use a navigation split view (`NavigationSplitView`, `UISplitViewController`). |
| macOS | [HIG] Row height, text and glyph size follow the sidebar size (small, medium, large), which people can change in General settings. Consider auto-collapsing the sidebar when the window narrows. Keep critical information and actions away from the bottom of the sidebar. |
| visionOS | [HIG] For deep hierarchies put the sidebar inside a tab; sidebar selections must not switch tabs. |
| tvOS | No additional considerations. |
| watchOS | Not supported. |

Source: https://developer.apple.com/design/human-interface-guidelines/sidebars

## Toolbars: general rules

A toolbar holds three kinds of content: the view title, navigation controls (back, forward, search) and actions (buttons, menus). On iOS a navigation-specific top toolbar is what was called a navigation bar.

- [HIG] Choose items deliberately; do not overcrowd. Decide which items collapse first as width shrinks.
- [Req] iPadOS and macOS add the overflow menu automatically when items stop fitting. [HIG] Do not add your own overflow menu, and avoid layouts that overflow at the default size.
- [HIG] Add a More menu only when really needed, and fill it with the less important actions.
- [HIG] On iPadOS and macOS consider toolbar customization for apps with many items or long working sessions.
- [HIG] (OS 26+, Liquid Glass) Minimize custom toolbar backgrounds and tinted controls; let the content layer inform the bar's look and use a scroll edge effect (`ScrollEdgeEffectStyle`) when the bar needs separation from content.
- [HIG] (OS 26+) Do not color item labels similarly to the content beneath; over colorful content keep the default monochrome appearance.
- [HIG] Prefer standard components in bars; a custom component's corner radius should be concentric with the bar's corners.
- [HIG] Hiding toolbars for a distraction-free view is fine when contextual and reliably reversible (see `references/patterns-flows.md`, Going full screen).

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars

## Toolbars: titles, Back and Close (former navigation bar guidance)

- [HIG] Give each window or view a title that confirms location and distinguishes windows. Leaving the title area empty is acceptable when the content already supplies context.
- [HIG] Do not use the app name as a title.
- [HIG] Keep titles to a word or short phrase, under 15 characters, to leave room for controls.
- [HIG] Use the standard Back and Close buttons with their standard symbols. Do not label them with the words "Back" or "Close".
- [HIG] A custom Back or Close button must look and behave like the standard one and be used consistently across the app.
- [HIG] iOS: use a large title to keep people oriented; by default it collapses to a standard title on scroll and returns at the top (`prefersLargeTitles`).
- [HIG] A swipe-from-edge shortcut may accelerate going back, but the Back button must remain (Gestures page; see `references/patterns-interaction.md`).

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/gestures

## Toolbars: actions and item grouping

- [HIG] Offer the commands people most often want, or those for the most important objects.
- [HIG] Prefer simple recognizable symbols over text, except for actions such as Edit that symbols represent poorly.
- [HIG] Prefer system symbols without their own borders (no outlined-circle variants); the bar section already provides the container.
- [HIG] (OS 26+) Use the `.prominent` style for the key action such as Done or Submit. Specify only one primary action and place it on the trailing side.

| Area | What goes there | Customizable |
|---|---|---|
| Leading edge | Back / previous document, sidebar toggle, then the view title, optionally a document menu (Duplicate, Rename, Move, Export) | No |
| Center | Common controls; the title if it is not leading. Collapses into the system overflow menu as the window narrows | Yes (iPadOS, macOS, when enabled) |
| Trailing edge | Items that must stay available, inspector buttons, optional search field, the More menu, the primary action (Done) | Stays visible at all sizes |

- [HIG] Group items by function and frequency of use; aim for at most three groups.
- [HIG] Put navigation controls and critical actions (Done, Close, Save) in dedicated, visually distinct sections.
- [HIG] Keep grouping and placement consistent across platforms.
- [HIG] Do not place a text-labeled action directly next to a symbol action or another text action; separate text-labeled buttons with fixed space so they do not read as one control.

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars

## Toolbars: platform differences

| Platform | Rules |
|---|---|
| iOS | [HIG] Space is tight: include only essential actions in the main toolbar area and move the rest to a More menu. Use large titles. |
| iPadOS | [HIG] A toolbar and a tab bar can share the same row at the top, keeping full width for content. Window controls sit at the leading edge of a windowed app's toolbar; do not let leading items overlap them (Windows page). |
| macOS | [HIG] The toolbar lives in the window frame, below or integrated with the title bar; items have no bezel. Every toolbar item must also exist as a menu bar command, because the toolbar can be customized or hidden. The reverse is not required. |
| tvOS | No additional considerations. |
| visionOS | [HIG] The system toolbar sits along the window's bottom edge, slightly in front of it. Prefer the system toolbar; avoid vertical toolbars (tab bars are vertical); try to keep windows from resizing narrower than the toolbar; avoid pull-down menus in toolbars; restore standard controls when leaving a modal state. Items may be a symbol or a text label; looking at a symbol reveals its label. |
| watchOS | [HIG] Toolbar buttons go in the top corners or along the bottom and stay visible over scrolling content. A scrolling toolbar button (revealed by scrolling up) suits an important action that is not the view's primary function. |

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/windows

## Split views

- [HIG] Use a split view to show several hierarchy levels at once: primary pane selects, secondary (and optional tertiary) pane shows children or detail.
- [HIG] Persistently highlight the current selection in every pane that leads to the detail view.
- [HIG] Consider drag and drop between panes.

| Platform | Rules |
|---|---|
| iOS | [HIG] Prefer split views in regular, not compact, width. |
| iPadOS | [HIG] Two or three vertical panes. Windows resize fluidly, so design for narrow, compact and intermediate widths and keep pane-to-pane navigation logical at each. |
| macOS | [HIG] Panes may be arranged vertically, horizontally or both, with draggable dividers. Set sensible minimum and maximum pane sizes so the divider stays visible. Let people hide panes where it helps and offer more than one way to bring them back (toolbar button, menu command with shortcut). Prefer the thin divider (1 pt). |
| tvOS | [HIG] Good for filtering. Default is one third primary, two thirds secondary; half-and-half is available. Show a single title above the whole split view; center it over a collection, or place it above the primary pane when the secondary pane is one main view. |
| visionOS | [HIG] Prefer a split view to a new window for supplementary information; use a sheet for a short required task. |
| watchOS | [HIG] Shows either the list or a detail view full screen. Open on the most relevant detail automatically; put multiple detail pages in a vertical tab view. |

Source: https://developer.apple.com/design/human-interface-guidelines/split-views

## Search fields and search placement

- [HIG] Use placeholder text to say what can be searched.
- [HIG] Start searching as people type when possible.
- [HIG] Consider suggestions (recent searches before typing, predictions while typing); show the most relevant results first and consider categorizing them.
- [HIG] Scope bar: for clearly defined categories; default to the broader scope. Tokens: for common terms or attributes; pair them with suggestions so people discover them.
- [HIG] Aim for one clearly identified place to search the whole app; local filtering of one view is still acceptable (Searching page; see `references/patterns-flows.md`).

| Platform | Placement options and when to use them |
|---|---|
| iOS | [HIG] (1) Search tab in the tab bar: standard tab style opens a landing page for discovery and suggestions; button appearance focuses the field and shows the keyboard at once for quick lookups. (2) Toolbar: place search at the bottom when there is room (expanded field or button); place it at the top when bottom content must stay unobstructed or there is no bottom toolbar. (3) Inline field: when adjacency to the content it filters matters; put it above the list and consider pinning it to the top toolbar on scroll. |
| iPadOS, macOS | [HIG] Trailing side of the toolbar for most apps, especially split views. Top of the sidebar when filtering the sidebar's own content. A dedicated sidebar or tab bar item when search doubles as a discovery area; focus the field on arrival, except on iPad with only the virtual keyboard. In compact iPad widths keep search where it is most useful (for example above the content list column). Keep iPad and Mac behaviour consistent. |
| tvOS | [HIG] Search is a dedicated keyboard screen with results beneath; provide popular, contextual and recent suggestions because typing is slow. |
| watchOS | [Req] Tapping the field opens full-screen text input; the app returns after Cancel or Search. |
| visionOS | No additional considerations. |

Source: https://developer.apple.com/design/human-interface-guidelines/search-fields, https://developer.apple.com/design/human-interface-guidelines/searching

## Tab views, path controls, page-based navigation

- [HIG] Tab view (macOS; shown as pages on watchOS; not supported on iOS, iPadOS, tvOS, visionOS): for closely related panes in one area. Controls in a pane affect only that pane. Label tabs with nouns in title-style capitalization. Avoid more than six tabs. Do not replace the tabbed control with a pop-up button unless there are too many panes. Inset the tab view from the window edges.
- [HIG] On iOS and iPadOS use a segmented control for the tab-view role; for separate app sections use a tab bar (see `references/components-controls.md`).
- [HIG] Path control (macOS only): shows the file-system path of the selection, in standard (linear) or pop-up style. Use it in the window body, never in the toolbar or a status bar. The HIG defines no breadcrumb component for other platforms.
- [HIG] watchOS: prefer vertical pagination with the Digital Crown over horizontal paging or deep hierarchies; aim for one screen height per page.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-views, https://developer.apple.com/design/human-interface-guidelines/path-controls, https://developer.apple.com/design/human-interface-guidelines/page-controls

## Common mistakes

| Mistake | Fix |
|---|---|
| Action buttons (compose, add, scan) placed as tabs | Move actions to a toolbar; tabs only navigate |
| Stating or enforcing "max 5 tabs" as a HIG rule | The page gives no limit; avoid More-tab overflow, and use five or fewer only as the default for user-customizable iPad tab bars |
| Hiding the tab bar on pushed screens, or disabling a tab with no content | Keep it visible except under modals; keep tabs enabled and explain empty sections |
| Opaque or tinted bar backgrounds and colored bar items on OS 26+ | Remove custom backgrounds; rely on Liquid Glass and scroll edge effects |
| Hand-built overflow ("...") menu on iPadOS or macOS | Let the system overflow menu handle it; set item priorities instead |
| Back button with the text "Back", or a custom chevron that behaves differently | Use the standard Back and Close buttons and symbols |
| App name as the navigation title; titles of 15 characters or more | Short, view-specific title, or leave it empty when content gives context |
| More than three toolbar groups; text buttons touching symbol buttons | Regroup to three or fewer; add fixed space around text-labeled items |
| Two primary (prominent) toolbar actions | One, on the trailing side |
| Sidebar with three or more nested levels | Two levels in the sidebar; add a content-list pane |
| Split view forced into compact width on iPhone | Collapse to a single column or use a tab bar |
| macOS toolbar-only commands | Mirror every toolbar item in the menu bar |
| Vertical custom toolbar or pull-down menu in a visionOS toolbar | Use the system bottom toolbar |
| Search field with no placeholder, or several unrelated search entry points | Describe the scope in the placeholder; give search one primary location |
