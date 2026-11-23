# Navigation components: navigation bar, rail, app bars, toolbars, tabs, search

Scope: choosing and configuring primary navigation (navigation bar, navigation rail, the retired navigation drawer), app bars, toolbars, tabs and search, by window size class and destination count. API names are in `references/implementation-navigation.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How to read this file
- Primary navigation by window size class and destination count
- Components that are not shown together
- Renamed and retired navigation components
- Navigation bar
- Navigation rail
- Navigation drawer (no longer recommended)
- App bars
- Toolbars
- Tabs
- Search
- Common mistakes

## How to read this file

- [Conv] `[MD]` covers Material's "should", "avoid" and "Don't" captions: recommendations. `[Req]` is used only where the page itself says "must", "require" or "Material requires". `[API]` marks availability and status facts from the overview pages.
- [Conv] Numbers are in dp and come from the token tables or measurement tables of the specs pages unless a bullet says "prose". Dimensions that exist only inside diagrams (images) are not reported. Window size class names are used as the component pages use them; their breakpoints are in `references/foundations-layout.md`.

Source: https://m3.material.io/components

## Primary navigation by window size class and destination count

| Window size class | 3 to 5 destinations | More than 5 destinations |
|---|---|---|
| Compact | Navigation bar with vertical items (icon above label) | Do not overfill the bar. Reorganize related content into tabs inside a page, or put navigation behind a menu icon that opens a modal expanded navigation rail |
| Medium | Navigation bar with horizontal items, or a collapsed navigation rail. Decide by whether horizontal or vertical space matters more; the rail page suggests the bar when there are few destinations | Collapsed rail (3 to 7 items); consider a modal expanded rail |
| Expanded, large, extra-large | Navigation rail, not a navigation bar. Collapsed rail, or a standard expanded rail when there is room | Collapsed rail up to 7 items; expanded rail (standard or modal, chosen by horizontal space and destination count) can reveal secondary destinations |
| Any, fewer than 3 destinations | Tabs, not a navigation bar | n/a |

- [MD] A navigation bar is for compact and medium windows only ("mobile or tablet only"); it is not meant for desktop layouts, where a rail or tabs are used instead.
- [MD] A rail is for medium windows and larger. A standard (non-modal) rail is not used in compact windows; a modal expanded rail may open from a menu button on phones.
- [MD] Past five destinations in a rail-based layout, consider a modal expanded rail.
- [Conv] The pages give no rule for which destinations stay in a compact navigation bar when a product has more than five, and no upper limit for an expanded rail. Do not invent one; say the choice is the product's.
- [Conv] Material surfaces one tension here: the rail guidelines say compact windows "should always use a navigation bar", while the rail overview shows collapsed and expanded rails transitioning "on any device", including phones in portrait. Read it as: bar by default in compact, modal expanded rail as the menu-driven alternative.
- [MD] Secondary navigation inside a destination: primary tabs, then secondary tabs. A floating toolbar may act as local tabs between related sub-pages.

Source: https://m3.material.io/components/navigation-bar/guidelines, https://m3.material.io/components/navigation-rail/guidelines

## Components that are not shown together

| Pair | Page wording (strength) | Do instead |
|---|---|---|
| Navigation bar + navigation rail | "Never" use them simultaneously (rail guidelines) | Swap one for the other as the window resizes |
| Navigation bar + toolbar | Both sit at the bottom, so they "should not" be shown at the same time | Navigation bar on primary pages, toolbar on subsequent pages that have actions |
| Navigation bar + toolbar that carries navigation controls | "Don't" caption | Keep global navigation in the bar; use a floating toolbar for local navigation on a deeper page |
| Docked toolbar + any other bottom-aligned element | "don't use a docked toolbar" | Floating toolbar, or drop one of the bars |
| Navigation rail + FAB menu; toolbar + FAB menu | "Don't" caption on the FAB menu page | See `references/components-controls.md` |
| Floating toolbar + extended FAB | "Don't" caption; a floating toolbar pairs with a FAB only | Use a plain FAB |
| Several toolbars in a compact window | "Don't" | One toolbar for all actions |
| Navigation drawer + another primary navigation component | "Avoid" (legacy page) | One component per breakpoint |

- [MD] A rail "should be the only visible navigation element", yet tabs may be used alongside a rail as an extra visible layer. Tabs are not counted as primary navigation.
- [MD] A vertical floating toolbar and a rail can coexist: put the toolbar on the edge opposite the rail and use the rail's center-aligned configuration.

Source: https://m3.material.io/components/toolbars/guidelines, https://m3.material.io/components/navigation-rail/guidelines, https://m3.material.io/components/fab-menu/guidelines

## Renamed and retired navigation components

| Older name or variant | Current status (Material 3 Expressive) | Use now |
|---|---|---|
| Bottom navigation (Material 2) | Renamed navigation bar | Navigation bar |
| Baseline navigation bar (80 high) | "No longer recommended" | Flexible navigation bar (64 high, horizontal items in medium windows) |
| Baseline navigation rail (80 wide) | "No longer recommended" | Collapsed navigation rail (96 wide; narrow 80) |
| Navigation drawer, standard and modal | "No longer recommended"; still documented | Expanded navigation rail, standard or modal |
| Top app bar | Renamed app bar (May 2025) | App bar |
| Center-aligned top app bar | Merged into the small app bar | Small app bar with centered text |
| Medium and large app bars (baseline) | "No longer recommended" | Medium flexible, large flexible |
| Bottom app bar | "No longer recommended", "still supported" | Docked toolbar |
| Search bar and search view | One component named search (February 2025) | Search; contained style |
| Search, divided style (baseline) | "Not recommended" | Contained style |

- [API] Old URLs redirect: `top-app-bar` to `app-bars`, `bottom-app-bar` to `toolbars`.
- [Conv] "No longer recommended" is Material's wording for new Expressive work. It is not a deprecation of the code, so do not rewrite an existing drawer or bottom app bar unless asked.

Source: https://m3.material.io/components/app-bars/overview, https://m3.material.io/components/toolbars/overview, https://m3.material.io/components/navigation-rail/overview, https://m3.material.io/components/search/overview

## Navigation bar

- [API] The overview lists Jetpack Compose and Android Views as available, each with an Expressive entry.
- [MD] Use for three to five top-level destinations of equal importance. Destinations stay the same on every screen and keep fixed positions; do not scroll or reorder them.
- [MD] Not for a single task (viewing one email). Fewer than three destinations: use tabs.
- [MD] Place it at the bottom, spanning the full window width, with items centered.
- [MD] Compact windows use vertical items (icon above label). Medium windows should use horizontal items (icon beside label inside the indicator); horizontal items have a fixed width and stay centered, so extra space goes to the ends of the bar.
- [Req] Every item has label text (the page says items "require" one); it should be one or two words. Do not remove, wrap, truncate or shrink labels.
- [MD] Active item: filled icon plus the active indicator; inactive items use outlined icons. If no filled version exists, the icon weight "must increase" (semibold). Use the indicator on exactly one item.
- [Req] Active and inactive icons "must" have at least 3:1 contrast with the container. Do not use multiple or low-contrast colors.
- [MD] Badges sit at the upper trailing corner of the icon: small for "something new", large for a count. See `references/components-content.md`.
- [MD] A FAB sits above the bar, right-aligned; it never covers the bar.
- [MD] The bar may be covered temporarily by dialogs, sheets or the keyboard; it should not be permanently obstructed on any screen.
- [MD] Selecting an item uses a top-level transition. Whether a destination restores its state (scroll position, tab, inline search) or resets is a product choice; preserve state when people switch often.
- [MD] Re-selecting the active destination should scroll that page to the top. Swiping across the screen does not move between destinations.
- [MD] The bar may hide on downward scroll and return on upward scroll. Do not hide it while a screen reader is active.
- [MD] Accessibility: keep the full label visible up to 2x text size (it may wrap and the bar grows taller); beyond that it may truncate. The accessibility label normally equals the visible label; make it more descriptive when the label is ambiguous.

| Measurement (token) | Value |
|---|---|
| Flexible navigation bar height | 64 |
| Baseline navigation bar height | 80 |
| Icon size | 24 |
| Vertical item active indicator | 56 x 32 |
| Horizontal item active indicator height; leading and trailing space | 40; 16 |
| Icon to label space | 4 |
| Baseline active indicator | 64 x 32 |
| State layers: hovered, focused, pressed | 8%, 10%, 10% |

Source: https://m3.material.io/components/navigation-bar/guidelines, https://m3.material.io/components/navigation-bar/specs, https://m3.material.io/components/navigation-bar/accessibility

## Navigation rail

- [API] The overview lists Jetpack Compose and Android Views as available, each with an Expressive entry. Two variants: collapsed and expanded; the expanded rail is standard (beside content) or modal (over content).
- [MD] Collapsed rail: three to seven items plus an optional menu button and FAB; it should not be hidden. Keep it in the same place on every screen.
- [MD] Expanded rail: should always open from a menu icon and can reveal secondary destinations. Use standard in large windows with spare room; use modal for dense layouts or many items. In immersive experiences the expanded rail may be hidden until the menu icon is selected.
- [MD] Place the rail on the leading edge of the window (left in left-to-right, right in right-to-left), outside any panes, never inside body content, and never horizontal.
- [MD] Items align as a group to the top or the center; use center alignment on tablets. The menu icon and FAB are always top-aligned; avoid placing the FAB below the items.
- [MD] A FAB nested in the rail rests at elevation level 0. When the rail expands, the FAB should become an extended FAB and page content adjusts to fit.
- [MD] Do not use a logo as the menu button; a logo at the top must not look like a button.
- [Req] Every item has label text (the page says items "require" a one-word label; the navigation bar page says one or two words). Do not truncate, ellipsize or shrink it; if unavoidable, break a longer phrase onto two lines.
- [MD] Exactly one active indicator. The item's target area always spans the full rail width even when the indicator hugs the label.
- [MD] Badges: at the icon's upper corner in the collapsed rail, next to the label in the expanded rail.
- [MD] Destinations stay fixed while content scrolls vertically. Over horizontally scrolling content, separate the rail with a divider or elevation level 1.
- [MD] The container fill can be removed; then every item needs at least 3:1 contrast. Do not use more than two colors for destinations.
- [API] Predictive back applies only to the modal expanded rail.
- [MD] Accessibility: initial focus lands on the first interactive item (menu, FAB or first destination); the 2x text rule matches the navigation bar.

| Measurement (token) | Value |
|---|---|
| Collapsed rail width; narrow | 96; 80 |
| Expanded rail width | min 220, max 360 |
| Item height; short | 64; 56 |
| Icon size | 24 |
| Vertical item active indicator | 56 x 32 |
| Horizontal item active indicator height | 56 |
| Baseline rail width | 80 |

Source: https://m3.material.io/components/navigation-rail/guidelines, https://m3.material.io/components/navigation-rail/specs, https://m3.material.io/components/navigation-rail/accessibility

## Navigation drawer (no longer recommended)

- [MD] Every tab of the page carries a note that the drawer is no longer recommended in Material 3 Expressive and that an expanded navigation rail replaces it.
- [API] The overview lists Jetpack Compose and Android Views as available, with no Expressive entry.
- [MD] Baseline guidance, for maintaining existing drawers: standard drawer in expanded, large and extra-large windows; modal drawer (with scrim) in compact and medium. It was recommended for five or more top-level destinations or two or more hierarchy levels.
- [MD] A modal drawer is opened by an action outside it (a menu icon) and dismissed by choosing an item, tapping the scrim, or swiping toward its anchoring edge. It opens from the start edge.
- [MD] Do not put dividers between individual destinations, wrap or shrink labels, or give icons to only some destinations.
- [MD] Measurements table: container width 360, active indicator 336 x 56, icon 24.
- [Conv] The page says to avoid a drawer alongside other primary navigation, and also allows a modal drawer "alone or with a navigation rail" in medium and expanded windows. Report both when reviewing a legacy layout.

Source: https://m3.material.io/components/navigation-drawer/guidelines, https://m3.material.io/components/navigation-drawer/specs

## App bars

| Variant | Use | Height (token) | Headline type style |
|---|---|---|---|
| Search app bar | Home pages where search is key; opens the search view | Search container 56 inside the bar | Body large |
| Small | Dense layouts, or the scrolled state of a page | 64 | Title large |
| Medium flexible | Larger headline; can collapse to small on scroll | 112 (136 with subtitle) | Headline medium |
| Large flexible | Emphasize the page headline | 120 (152 with subtitle) | Display small |
| Medium, large (baseline) | No longer recommended | 112, 152 | n/a |

- [API] The overview lists Jetpack Compose and Android Views as available, each with an Expressive entry.
- [MD] An app bar describes the current page and holds navigation (Back or Menu) plus one or two essential actions: one action, two if necessary. The primary action alters or exits the whole page (Send, Save, Edit).
- [MD] Many actions belong in a toolbar. Avoid an overflow menu in the app bar when possible, and avoid using trailing buttons to open a menu of more actions.
- [Conv] The same page's adaptive section says trailing actions "may" collapse into an overflow menu at smaller breakpoints. Treat overflow as a resizing fallback, not as the design.
- [MD] Up to two trailing icon buttons, most used closest to the leading edge. To promote one action, make it a filled or tonal (optionally wide) icon button, and then show only that one. Never more than one filled or tonal button.
- [MD] Leading button: a menu icon that opens a modal expanded rail, or a back arrow.
- [MD] Always use the default height and span the full window width. Keep straight corners; curved shapes suggest the bar can expand.
- [MD] Headline: brief; do not truncate it. Do not wrap it in a small app bar. In flexible app bars it may wrap, to two lines at most. It may be leading-aligned or centered.
- [MD] Subtitle styles: Label medium (small), Label large (medium flexible), Title medium (large flexible). Avoid resizing the headline or subtitle.
- [MD] Prefer filled icons; outlined icons are acceptable, in particular for unselected toggles.
- [MD] The layout mirrors in right-to-left languages. Token values: icon 24, avatar 32, left and right padding 4.
- [MD] Accessibility: initial focus lands on the leading button; the title's accessibility label equals the title text.

Search app bar:
- [MD] The hint always includes the word "Search" ("Search inbox", "Search Photos").
- [MD] With a trailing avatar, up to two trailing icons on mobile; up to four trailing icons on larger screens. Three icons plus an avatar is a "Don't". Extra actions go in a toolbar.
- [MD] The leading element may be a product logo; avoid using a logo to open the expanded rail.
- [MD] The search container fills all the space between leading and trailing elements until it reaches 312, then grows only to 50% of that space.
- [MD] Search text needs at least 3:1 contrast against its container when colors are customized.

Scroll behaviour:
- [MD] Start with the same color as the page background, then fill with a contrasting color (surface container) on scroll. Separation is by color, not by a shadow.
- [MD] The bar may stay in place or hide and reappear while scrolling.
- [MD] Alternative: keep the container transparent on scroll so content shows through; then give the icon buttons a container fill and consider narrow icon buttons.
- [MD] Medium flexible and large flexible bars may compress into a small app bar and should stay small until the page is back at the top. Do not transform an app bar into a search app bar.

Source: https://m3.material.io/components/app-bars/guidelines, https://m3.material.io/components/app-bars/specs, https://m3.material.io/components/app-bars/accessibility

## Toolbars

- [API] The overview lists the docked toolbar and the floating toolbar as available under the Expressive entries for Jetpack Compose and Android Views; the non-Expressive entries list the bottom app bar.
- [MD] A toolbar holds actions for the current page and can hold many, scaling up in larger windows. When actions do not fit, add a menu.
- [MD] Docked toolbar: full window width, bottom only, straight corners; best for global actions that stay the same across pages. On the web and on large screens it may be rounded.
- [MD] Floating toolbar: floats over body content; best for contextual actions. It must stay fully visible inside the window or pane; overflow goes into a menu in the trailing slot. Horizontal or vertical.
- [MD] Color: standard (low emphasis) or vibrant (high emphasis; can signal a temporary mode such as editing).
- [MD] Emphasize one action only: a different icon button color style, a wide button, or a paired FAB. Do not combine a bold button with a FAB.
- [MD] Slots accept buttons, icon buttons, text fields, images or custom content; avoid mixing many control types or adding too many controls.
- [MD] Avoid square icon buttons in a floating toolbar (fine in a docked one). No wide icon buttons in a vertical toolbar.
- [MD] Vertical floating toolbars are not recommended in compact windows; in larger windows place them on either side.
- [MD] Docked layout: evenly spaced items in compact; from medium up, center the items or center a key action and push the others to the edges.
- [MD] Right-to-left: mirror the items that need it, and reverse the order of actions when order matters.
- [MD] On scroll: a docked toolbar stays or animates off screen; a floating toolbar stays, animates off, or collapses into a single high-emphasis action. Do not both collapse and scroll off.
- [Req] The page says all elements "need" a minimum 48 x 48 target area.

| Measurement | Value |
|---|---|
| Toolbar height, docked and floating (token and prose) | 64 |
| Docked leading and trailing padding | min 16 |
| Docked space between actions (token) | default and max 32, min 4 |
| Floating horizontal toolbar margin from window edge | min 16 |
| Floating vertical toolbar margin | min 24 |
| Space between floating toolbar and FAB (token) | 8 |
| Baseline bottom app bar height (token) | 80 |

Source: https://m3.material.io/components/toolbars/guidelines, https://m3.material.io/components/toolbars/specs

## Tabs

- [API] The overview lists Jetpack Compose and Android Views as available; there is no Expressive section.
- [MD] Tabs group related content at the same level of hierarchy. They are not for sequential content that must be read in order.
- [MD] Primary tabs sit at the top of the content pane under an app bar and are used when one set of tabs is enough. Secondary tabs sit inside a content area, always below primary tabs, when a second level is needed.
- [MD] Fixed tabs show every tab at once and divide the container into equal sections. Avoid more than four; five or more make the container cramped.
- [MD] Scrollable tabs are for sets that do not fit; tab width follows the label, and the first tab is offset 52 from the leading edge to hint at more. No maximum count is stated.
- [MD] The container extends the full width, with a divider on its bottom edge; content may scroll under it.
- [MD] Give all tabs icons and labels, or none; do not mix. Icon-only tabs need globally recognized icons.
- [MD] Labels are short. Do not truncate them unless required; the page also allows a second line with truncation, so prefer scrollable tabs for long labels.
- [MD] Badges on tabs hold at most four characters including a "+", and update or disappear once the content is viewed.
- [MD] People can swipe the content area to change tab, so avoid other horizontally swipeable content (maps, swipeable list items) inside it.
- [MD] On vertical scroll, tabs stay pinned or scroll away and return on upward scroll. Do not scroll tabs behind an app bar; attached tabs move with it as one unit.
- [MD] Accessibility: arrow keys or Tab move between tabs, Space or Enter activates; do not loop a scrollable tab set; do not apply density by default (48 x 48 targets).

| Measurement table | Value |
|---|---|
| Container height, label only; icon and label | 48; 64 |
| Icon size | 24 |
| Divider height | 1 |
| Active indicator height, primary; secondary | 3; 2 |
| Active indicator minimum length | 24 |

Source: https://m3.material.io/components/tabs/guidelines, https://m3.material.io/components/tabs/specs, https://m3.material.io/components/tabs/accessibility

## Search

- [API] The overview lists Jetpack Compose (and its Expressive entry) and Android Views as available, and Android Views Expressive as unavailable.
- [MD] Entry points: a search bar for searching one view; a search app bar when search is the primary, global function; a search icon button when search is secondary. When search is the primary action, focused search can be its own destination in the navigation bar.
- [MD] Focused search layouts: full-screen is the default in compact windows; docked (list below the bar, over a scrim) suits medium and expanded windows. Switch between them as the window resizes.
- [MD] Suggestions and results use the list component; add leading icons, category labels, avatars or filter chips, and gaps between groups.
- [MD] Leading slot: a navigation icon button (menu or back) or a non-functional search icon.
- [MD] Trailing slot: one or two icons or icon buttons, two at most; an avatar counts and pairs with at most one other. Focused search may show a clear icon.
- [Conv] The search app bar page allows an avatar plus two trailing icons on mobile, while the search page allows an avatar plus one. Follow the page for the component in use.
- [MD] Hint text states what can be searched. Typed text replaces it and stays visible, without focus, after the query runs.
- [MD] The back icon releases focus, dismisses suggestions and restores the bar. Android predictive back is supported.
- [MD] Container color is surface container high; pick container roles more than one step apart from the background.
- [MD] The bar may stay fixed or scroll away and return. Keep it inside its pane and close to the content it searches.
- [Req] When suggestions or results appear, the screen reader "must" announce the change. The hint text serves as the accessibility label.

| Measurement table | Value |
|---|---|
| Search bar height | 56 |
| Search bar and docked container width | min 360, max 720 |
| Bar margins, contained style: unfocused; focused | 24; 12 |
| Avatar size (token: target 48) | 30 |
| Docked results container height | min 240, max two thirds of screen height |

Source: https://m3.material.io/components/search/guidelines, https://m3.material.io/components/search/specs, https://m3.material.io/components/search/accessibility

## Common mistakes

| Mistake | Fix |
|---|---|
| Navigation bar with two items, or with six or more | Tabs for fewer than three; above five, restructure or use a modal expanded rail |
| Icon-only navigation items, or labels shrunk or truncated to fit | Always a visible label of one or two words |
| Navigation bar stretched across an expanded or desktop window | Navigation rail from expanded up |
| Navigation bar and rail visible together | One at a time, swapped by window size class |
| Navigation bar plus a docked toolbar or bottom app bar on the same screen | Bar on top-level pages, toolbar on deeper pages |
| New Expressive design built on a navigation drawer, bottom app bar, or baseline medium or large app bar | Expanded rail, docked toolbar, medium flexible or large flexible app bar |
| Quoting 80 as "the" navigation bar height or rail width | 80 is the baseline value; flexible bar 64, collapsed rail 96 |
| App bar with three or more actions and an overflow menu | One or two actions; move the rest to a toolbar |
| Two filled or tonal icon buttons in an app bar | One emphasized action at most |
| Small app bar title wrapped or truncated | Shorten it, or use a flexible app bar with up to two lines |
| App bar with a drop shadow on scroll | Color fill change on scroll |
| Rail placed inside a pane, drawn horizontally, or hidden when collapsed | Leading window edge, vertical, always visible |
| FAB below the rail items; logo used as the rail's menu button | FAB and menu top-aligned; a real menu icon |
| Five or more fixed tabs; tabs used as wizard steps | Scrollable tabs; a stepped flow is not a tab set |
| Swipeable rows or a map inside a tabbed, swipeable content area | Remove the gesture conflict |
| Hiding the navigation bar on scroll while a screen reader is on | Keep it visible |
