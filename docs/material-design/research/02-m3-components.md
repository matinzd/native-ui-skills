# M2 research: Material Design 3 components (m3.material.io/components)

Fetched 2026-11-23 with headless Chromium. Every statement is [V] (read in the rendered page text in this session)
unless tagged [M] (memory) or [Inference]. Material guidance is recommendation, not platform requirement; the wording
strength on the page is kept ("must", "should", "avoid", "don't", "Material requires").

- Canonical URL pattern: `https://m3.material.io/components/<slug>/<overview|guidelines|specs|accessibility>`. Every component below has all four sub-pages (verified: all 36 real slugs x 4 rendered with content).
- Rendered text kept in `/tmp/claude-0/-home-user-apple-hig-skill/4b8f6fc4-b934-5d7d-9f48-9d6e78d71918/scratchpad/m2/pages/` (see `_INDEX.txt` there): 152 sub-page files, 37 expanded token-table files (`<slug>--specs-tokens.txt`), 1 hub file. Cleaned copies with `[DO]` / `[DON'T]` / `[CAUTION]` caption tags are in `.../m2/clean/`.
- Numbers come from three places, in this order of trust: the specs "Measurements" tables, the token tables, guideline prose. Measurement diagrams are images, so dimensions shown only in diagrams are NOT captured. Shape, type-scale, elevation-level and colour-role token values render as swatches and are not in the text.
- Site footer shows only "Privacy Policy" and "Terms of Service"; no licence statement appears on any component page (grep for licens/Creative Commons/Apache over all 190 files: 0 hits).

## 1. Component catalogue and current status

The hub groups components as: Buttons (button groups, buttons, extended FABs, FAB menu, FABs, icon buttons, segmented
buttons, split buttons); Date & time pickers; Loading & progress; Navigation (bar, drawer, rail); Sheets (bottom, side);
All other components (app bars, badges, cards, carousel, checkbox, chips, dialogs, divider, lists, menus, radio button,
search, sliders, snackbar, switch, tabs, text fields, toolbars, tooltips). The hub intro names six purposes: action,
containment, communication, navigation, selection, text input.

Availability columns: C = Jetpack Compose, C-X = "Jetpack Compose: Expressive", V = Android Views (MDC-Android),
V-X = "Android Views (MDC-Android): Expressive", as listed on each overview page. "-" = row not listed.

| Component | Slug | M3 Expressive status (page wording) | C | C-X | V | V-X |
|---|---|---|---|---|---|---|
| App bars | `app-bars` | RENAMED from "top app bar" (May 2025). Variants now: search app bar (new), small, medium flexible (new), large flexible (new). Baseline medium and large "no longer recommended". Center-aligned merged into small (centred-text configuration) | yes | yes | yes | yes |
| Toolbars | `toolbars` | NEW: docked toolbar, floating toolbar. Bottom app bar "no longer recommended ... still supported"; replace with docked toolbar | yes (Bottom app bar) | yes (docked, floating) | yes (Bottom app bar) | yes (docked, floating) |
| Navigation bar | `navigation-bar` | Flexible navigation bar (new, 64dp, horizontal items in medium) replaces baseline nav bar (80dp), which is "no longer recommended" | yes | yes | yes | yes |
| Navigation rail | `navigation-rail` | Collapsed rail (replaces baseline rail) and expanded rail (replaces navigation drawer), standard or modal. Baseline rail "no longer recommended" | yes | yes | yes | yes |
| Navigation drawer | `navigation-drawer` | "No longer recommended in the Material 3 Expressive update ... use an expanded navigation rail" (banner on all tabs). Still documented | yes | - | yes | - |
| Tabs | `tabs` | No Expressive section. Primary and secondary | yes | - | yes | - |
| Search | `search` | Feb 2025: search bar + search view "now collectively named search". Styles: contained (recommended) or divided (baseline, "Not recommended. Use contained") | yes | yes | yes | no |
| Buttons | `buttons` | May 2025: default + toggle variants; colour styles are now configurations (elevated, filled, tonal, outlined, text); sizes XS, S, M, L, XL; shapes round, square; small-button padding 24dp "no longer recommended", use 16dp | yes | yes | yes | yes |
| Button groups | `button-groups` | NEW (May 2025): standard and connected. Connected replaces segmented button | - | yes | - | yes |
| Icon buttons | `icon-buttons` | May 2025: default + toggle; colours filled, tonal, outlined, standard; 5 sizes; widths narrow, default, wide; round, square | yes | yes | yes | yes |
| Split button | `split-button` | NEW (May 2025). Sizes XS-XL; colours elevated, filled, tonal, outlined | - | yes | - | yes |
| Segmented buttons | `segmented-buttons` | "No longer recommended ... use the connected button group instead" (banner on all tabs) | yes | - | yes | - |
| FAB | `floating-action-button` | May 2025: sizes FAB (56), medium FAB (80, new, "most recommended"), large FAB (96). Small FAB and surface-colour FABs "no longer recommended" | yes | yes | yes | yes |
| Extended FAB | `extended-fab` | May 2025: small (56), medium (80), large (96). Baseline extended FAB and surface extended FAB "no longer recommended" | yes | yes | yes | yes |
| FAB menu | `fab-menu` | NEW (May 2025). "Should replace the speed dial and any usage of stacked small FABs" | - | yes | - | no |
| Badges | `badges` | No Expressive section. Small and large | yes | - | yes | - |
| Progress indicators | `progress-indicators` | Aug 2024: configurable track height, wavy shape. Linear and circular | yes | yes | yes | yes |
| Loading indicator | `loading-indicator` | NEW (May 2025). "Should replace most uses of the indeterminate circular progress indicator"; used for pull-to-refresh | - | yes | - | yes |
| Snackbar | `snackbar` | No Expressive section | yes | - | yes | - |
| Tooltips | `tooltips` | No Expressive section. Plain and rich | yes | - | no | - |
| Bottom sheets | `bottom-sheets` | No Expressive section. Standard and modal | yes | - | yes | - |
| Side sheets | `side-sheets` | No Expressive section. Standard and modal | NO ("Unavailable") | - | yes | - |
| Cards | `cards` | No Expressive section. Elevated, filled, outlined | yes | - | yes | - |
| Carousel | `carousel` | Nov 2025: new "uncontained multi-aspect ratio" layout. Availability table did not render (unverified) | ? | ? | ? | ? |
| Dialogs | `dialogs` | No Expressive section. Basic and full-screen | yes | - | yes | - |
| Divider | `divider` | No Expressive section | yes | - | yes | - |
| Lists | `lists` | Dec 2025: expressive list "recommended for new designs" (standard or segmented style, highlighted selection, slots). Baseline list "still available" | yes | yes | yes | yes |
| Menus | `menus` | Nov 2025: vertical menus "recommended for new designs" (standard or vibrant colour, gaps, selection states). Baseline menu "still available" | yes | yes | yes | no |
| Checkbox | `checkbox` | No Expressive section | yes | - | yes | - |
| Chips | `chips` | Aug 2024: stroke colour outline -> outline variant. Assist, filter, input, suggestion | yes | - | yes | - |
| Radio button | `radio-button` | No Expressive section | yes | - | yes | - |
| Switch | `switch` | No Expressive section | yes | - | yes | - |
| Sliders | `sliders` | May 2025: "continuous" renamed standard; "discrete" is now the stops configuration; variants standard, centered, range; sizes XS-XL; vertical orientation; inset icon | yes | yes | yes | yes |
| Date pickers | `date-pickers` | No Expressive section. Docked, modal, modal input | yes | - | yes | - |
| Time pickers | `time-pickers` | Oct 2026: scroll time picker added; dial and input restyled; baseline dial/input variants "no longer recommended". Compose calls the expressive styling "vibrant" | yes | yes | yes | no |
| Scroll fields | `scroll-fields` | NEW ("introduced in the expressive update"; not linked from the hub's visible text but in its link list) | - | yes | - | no |
| Text fields | `text-fields` | No Expressive section. Filled and outlined | yes | - | yes | - |

Other slugs: `all-buttons` is a stub (title + "When choosing the right button for an action, consider the level of
emphasis each button type provides") on all four sub-paths. `top-app-bar/*` redirects to `app-bars/*`;
`bottom-app-bar/*` redirects to `toolbars/*`; `common-buttons/*` returns "This page cannot be found".

## 2. Navigation components

### Navigation bar (`navigation-bar`)

- Use: 3 to 5 top-level destinations "of equal importance", "mobile or tablet only", compact and medium windows. Not for single tasks ("such as viewing one email"). One destination is always active.
- Not: more than 5 items -> "consider using tabs ... or hide the navigation behind a menu icon using a modal expanded navigation rail". Fewer than 3 -> "Instead, use tabs". Desktop -> "use a navigation rail or tabs".
- Configurations: vertical items (icon above label; default, compact) and horizontal items (icon beside label inside the indicator; medium). "In medium windows, navigation bars should use horizontal items."
- Numbers (tokens): flexible nav bar height 64dp; baseline nav bar height 80dp; icon 24dp; vertical active indicator 56x32dp; horizontal active indicator height 40dp with 16dp leading/trailing space; icon-label space 4dp; baseline active indicator 64x32dp. State layers: hovered 8%, focused 10%, pressed 10%.
- Labels: "All navigation items require a label text. It should be 1-2 words." Don't remove, wrap, truncate or shrink labels. Icons: filled for active, outlined for inactive; if no filled version "the icon's weight must increase". Icons "must have a minimum 3:1 contrast ratio with the container".
- Placement: "should always be placed at the bottom" and "span the full length of the window"; items centred. FAB "should be right-aligned above the navigation bar". May be temporarily covered by dialogs, sheets, keyboard; "should not be permanently obstructed on any screen".
- Adaptive: Compact: "navigation bar or modal navigation rail". Medium: "navigation bar or navigation rail. Decide based on whether horizontal or vertical space is more important." Expanded and extra-large: "Use a navigation rail instead."
- Behaviour: selecting uses a top-level transition; state can be preserved or reset (product choice). "Re-selecting the currently active destination should reset the scroll position to the top of the page." Swiping between destinations is "not supported". Bar "can appear or disappear" on scroll; "Don't hide the navigation bar on scroll when a screen reader is active."
- Accessibility: full label visible "at up to 2x text sizing. Beyond this size, text can truncate"; scaled text may wrap and the bar grows vertically. Tab moves between items, Space/Enter selects. Views note: "a more descriptive accessibility label is not available and the role is not announced".

### Navigation rail (`navigation-rail`)

- Use: medium, expanded, large, extra-large windows. Collapsed rail "should contain 3-7 navigation items" plus an optional menu and FAB; "It should not be hidden." Expanded rail is standard (beside content) or modal (over content, "should always open from a menu icon"); it "can reveal secondary destinations".
- Not: "Compact windows should always use a navigation bar" (standard rail); a MODAL expanded rail may open from a menu button on mobile. "Never use the navigation rail and navigation bar simultaneously." "Don't use the navigation rail horizontally. Use a navigation bar instead."
- Numbers (tokens): collapsed width 96dp (narrow 80dp); expanded width min 220dp, max 360dp; item height 64dp (short 56dp); icon 24dp; vertical indicator 56x32dp; horizontal indicator height 56dp; baseline rail width 80dp.
- Labels: "All navigation items require a one word label text" (rail page; nav bar says 1-2 words). Don't truncate, ellipsize or shrink; "Break up longer phrases into two text lines if necessary" (caution).
- Layout: leading edge (left in LTR, right in RTL), "outside any panes"; items top- or centre-aligned ("On tablets, use center alignment"); menu icon and FAB "should always be top-aligned"; FAB nested in the rail rests at elevation level 0; don't place the FAB below items; don't use a logo as the menu button. Target area "should always span the full width".
- Adaptive: Medium: rail "especially if prioritizing persistent vertical navigation". Expanded to extra-large: "Use a navigation rail, not a navigation bar"; choose standard vs modal by horizontal space and destination count. More than five destinations: "consider using a modal expanded nav rail". When expanding, the FAB "should transition into an extended FAB" and page content adjusts.
- Behaviour: destinations stay fixed during vertical scroll; with horizontally scrolling content use a divider or elevation level 1. Predictive back "only applies to the modal expanded navigation rail".
- Accessibility: Tab/Arrows between items, Space/Enter selects; initial focus on first interactive item (menu, FAB or first item); same 2x text rule as nav bar; "Don't use more than two colors for destinations".

### Navigation drawer (`navigation-drawer`) - no longer recommended

- Page still describes: standard (expanded, large, extra-large) and modal (compact, medium; scrim; any breakpoint). "Recommended for: apps with 5 or more top-level destinations; apps with 2 or more levels of navigation hierarchy". "Avoid using a navigation drawer with other primary navigation components, such as a navigation bar" (caution: "Avoid using two navigation components on the same screen"), yet the same page allows "a modal navigation drawer alone or with a navigation rail on medium and expanded breakpoints".
- Numbers (measurements): container width 360dp; active indicator 336x56dp, shape 28dp; icon 24dp; left/right padding 28dp; container corners "0,16,16,0dp".
- Modal drawer dismissal: selecting an item, tapping the scrim, swiping toward the anchoring edge. Start edge always.
- Don'ts: dividers between individual destinations; wrapping labels; shrinking text; icons on some destinations only.
- Web-only: below 320 CSS px swap the drawer for a navigation bar.

### App bars (`app-bars`)

- Use: describe the current page plus navigation (Back or Menu) and "1-2 essential actions". "App bars should only have one action, two if necessary." "If the product has many actions, place those in a toolbar. Avoid placing an overflow menu in the app bar when possible." (Same page, Adaptive section: trailing actions "may ... collapse into an overflow menu at smaller breakpoints".)
- Variants: search app bar ("home pages when search is key"), small ("dense layouts or when a page is scrolled"), medium flexible ("larger headline ... can collapse into a small app bar on scroll"), large flexible ("emphasize the headline").
- Numbers (tokens): small 64dp; medium flexible 112dp (136dp with subtitle); large flexible 120dp (152dp with subtitle); baseline medium 112dp, baseline large 152dp; icon 24dp; avatar 32dp; search container 56dp inside the search app bar; left/right padding 4dp.
- Type: search Body large; small Title large; medium flexible Headline medium; large flexible Display small. Subtitle: Label medium / Label large / Title medium.
- Rules: "Always use the default height ... and make it span the full width of the window". Straight corners. Headline: don't truncate; don't wrap in a small app bar; flexible bars wrap "to two lines maximum". "Up to two icon buttons" trailing; most-used closest to the leading edge. Only one filled or tonal icon button. Leading button is Menu (opens a modal expanded rail) or Back.
- Search app bar: label always includes the word "Search"; with a trailing avatar "up to two trailing icons on mobile"; "up to four trailing icons on larger screens". Search container fills 100% of the space between leading and trailing elements "until it reaches 312dp. Then ... 50% of that space". 3:1 contrast between search text and container.
- Scrolling: starts the same colour as the background, fills with surface container on scroll (no shadow); may stay, hide and reappear, or stay transparent with container-filled icon buttons. Flexible bars compress to small and "should remain small until the page is scrolled back to the top". "Don't transform app bars into a search app bar."
- Accessibility: initial focus on the leading button; title's accessibility label equals the title.

### Toolbars (`toolbars`) - replaces bottom app bar

- Use: "actions related to the current page"; "can contain many actions". Docked toolbar: full width, "global actions that remain the same across multiple pages". Floating toolbar: "contextual actions relevant to the body content". Colour: standard (low emphasis) or vibrant (high emphasis; can signal a mode such as edit).
- Not: "should not be shown at the same time" as a navigation bar ("Show the navigation bar on primary pages, and toolbars on subsequent pages with actions"). "If using other bottom-aligned elements, such as a navigation bar, don't use a docked toolbar."
- Numbers: "By default all toolbars are 64dp high"; docked leading/trailing padding min 16dp; default space between items 32dp (token max 32dp, min 4dp); "All elements need a minimum 48x48dp target area"; floating horizontal margin from window edge min 16dp; vertical floating toolbar margin min 24dp; FAB-to-toolbar gap 8dp; baseline bottom app bar 80dp (72dp with FAB).
- Rules: docked only at the bottom, straight corners; floating must stay fully visible, overflow menu in the trailing slot; emphasize one action only; no square icon buttons in floating toolbars; no wide icon buttons in vertical toolbars; vertical toolbars "aren't recommended for compact windows" and sit opposite the navigation rail; "Don't use multiple toolbars in compact windows". Floating toolbar pairs with a FAB, never with an extended FAB.
- Scrolling: docked stays or animates off; floating stays, animates off, or (Compose) collapses to a FAB/key action. "Don't collapse actions and scroll at the same time."
- Accessibility: Tab or Arrows between elements; toolbar role on web, generic container on mobile.

### Tabs (`tabs`)

- Use: "groups of related content that are at the same level of hierarchy". Primary tabs: top of the content pane under an app bar. Secondary tabs: inside a content area, "always ... below primary tabs", when more than one level of tabs is needed.
- Not: "sequential content that needs to be read in a particular order".
- Fixed vs scrollable: fixed shows all tabs; "Avoid using more than four tabs at once. At five or more tabs, the container becomes cramped." Scrollable when tabs do not fit ("a UI can have as many tabs as needed"); first scrollable tab offset 52dp from the leading edge.
- Numbers: container 48dp (label only), 64dp (icon and label); icon 24dp; divider 1dp; primary indicator 3dp, secondary 2dp; indicator min length 24dp; badge max four characters.
- Rules: container extends full width; don't mix icon+label on only some tabs; don't truncate unless required; users can swipe the content area between tabs, so "Avoid placing swipeable items in the content area"; tabs may stay pinned or scroll off and return; "Don't scroll tabs behind an app bar".
- Accessibility: Arrow moves between tabs, Space/Enter activates ("Don't use Space/Enter for navigating tabs"); do not loop a scrollable tab set; don't apply density by default (48x48 targets).

### Search (`search`)

- Entry points: search bar (search within a view), search app bar ("primary, global function"), search icon button ("secondary action").
- Focused search layouts: full-screen ("default for compact breakpoints") or docked (list below the bar over a scrim; "best for medium and expanded windows").
- Numbers: bar height 56dp; width min 360dp, max 720dp; margins 24dp unfocused, 12dp focused (contained style); avatar 30dp (target 48dp); docked container height min 240dp, max 2/3 of screen height.
- Rules: container colour surface container high; use container roles "more than one step apart" from the background. Leading: navigation icon button or non-functional search icon. Trailing: "one or two"; "maximum of two"; an avatar with "up to one other". Hint text states what is searchable. Back icon releases focus. Input text stays visible after a query.
- Accessibility: "the screen reader must announce" when suggestions/results appear; hint text is the accessibility label; role is Text field on Android.

## 3. Action components

### Buttons (`buttons`)

- Emphasis order as listed on the page: elevated, filled, filled tonal, outlined, text. Filled "has the most visual impact after the FAB ... ideally for only one action on a page"; tonal for a lower-priority action needing more emphasis than outline (e.g. Next); outlined for medium emphasis, pairs with filled as the secondary; text for "the lowest priority actions", standard in dialogs, cards, snackbars; elevated = tonal with a shadow, "only when absolutely necessary" (separation from a busy background).
- Toggle buttons: binary selection (Save, Favorite); outlined icon unselected, filled icon selected; shape changes round <-> square on selection; no toggle text style.
- Numbers (tokens; height / icon / side padding / icon-label gap): XS 32 / 20 / 12 / 4; S 40 / 20 / 16 / 8; M 56 / 24 / 24 / 8; L 96 / 32 / 48 / 12; XL 136 / 40 / 64 / 16 dp. Square corner: 12, 12, 16, 28, 28dp; pressed: 8, 8, 12, 16, 16dp. "Extra small and small ... must have a target size of 48x48dp or larger". Small is the default size. Deprecated baseline tokens: 40dp height, 18dp icon.
- Label: "very brief, ideally 1-3 words"; sentence case; "Don't truncate or wrap label text"; one icon only, on the leading side; "Don't underline the text button" (use hyperlinked body text for links).
- Layout: width hugs the label or stretches responsively; never narrower than the label; constrain width in large windows; keep icon and label grouped and centred; keep element order the same across window sizes.
- Dialog: text buttons aligned to the trailing edge. Outlined and text styles on simple backgrounds, not images.
- Accessibility: enabled buttons need 3:1 against the background (container for elevated/filled/tonal, label for outlined/text); on Android labels should fit "within two lines after the text size is increased to 200%".

### Button groups (`button-groups`)

- Standard group: adjacent buttons react (width/shape) when one is pressed; hugs content; same size and shape for all buttons by default. Connected group: for selection, view switching, sorting; "single or multi-select patterns that use toggle buttons"; "should span the width of the page or surface" (cap the width on large windows); "Avoid using a connected group when none of the buttons can be toggled"; don't mix colour styles.
- Numbers: heights 32 / 40 / 56 / 96 / 136dp; standard inner padding 18 / 12 / 8 / 8 / 8dp; connected inner padding 2dp at every size; each button min 48x48dp target; XS and S connected min width 48dp.
- No segment-count limit is stated for connected groups (the old segmented button's 2-5 is not repeated here).
- Adaptive: single line, "shouldn't wrap to a second line"; trailing buttons may collapse into an overflow menu.
- Accessibility: Tab to the group, arrow keys between buttons; container not focusable and not labelled.

### Icon buttons (`icon-buttons`)

- "Must use a system icon with a clear meaning." Colour styles in order of emphasis: filled, tonal, outlined, standard.
- Sizes (guideline text): XS 32dp, S 40dp (default), M 56dp, L 96dp, XL 136dp; icon 20 / 24 / 24 / 32 / 40dp (tokens). Widths narrow, default, wide. "The target size of each icon button should be at least 48dp, even when nested."
- Default icon buttons use filled icons; toggles use outlined -> filled; if no filled version, semibold (then bold). Don't use a toggle for actions with no selected state (e.g. overflow menu).
- Hover/focus: tooltip describing the action (web: "should display a tooltip"). 3:1 icon contrast. Accessibility label describes the action. Don't apply density by default.

### FAB (`floating-action-button`), extended FAB (`extended-fab`), FAB menu (`fab-menu`)

- FAB use: "the most important action on a screen"; constructive actions (create, favorite, share, start a process). Not for "minor or destructive actions" (archive, trash, alerts, cutting text, controls suited to a toolbar). "FABs are not needed on every screen". "Don't display multiple FABs on a single screen". Cards "shouldn't have their own FAB". "Don't disable the FAB" (hide it if unavailable). Use a filled icon. Container must not be covered by badges.
- Sizes (tokens): FAB 56dp, icon 24dp; medium FAB 80dp, icon 28dp ("recommended for most situations ... compact and medium windows"); large FAB 96dp, icon 36dp ("best suited for expanded and larger"). Guidance also says "Use a medium FAB for mobile layouts, and large FAB for tablets and large screens."
- Placement: compact and medium "typically the lower right corner"; expanded "consider ... the upper left corner, like in the navigation rail". Above the navigation bar, right-aligned.
- Behaviour: stays in place on scroll; disappears and reappears on tab/page switch; container transform into a new surface or FAB menu. FAB icon 3:1 contrast with the container.
- Extended FAB: when a label is needed or for persistent access on long scrolling views. Heights 56 / 80 / 96dp; icon 24 / 28 / 36dp; "Extended FABs should have margins of 16dp". Label "1-2 words at most"; icon optional but never an icon without a label; one per screen; not "an option in a set of actions" (use filled buttons); not on top of toolbars, in the upper half of a mobile screen, on cards or inside containers; not with a floating toolbar. Compact/medium: bottom, centred or trailing. Expanded+: bottom right (LTR and RTL) or in the navigation rail. Collapses to a FAB when scrolling down, expands when scrolling up. Accessibility label "must include the same first word as the visible label".
- FAB menu: opens only from a FAB (not an extended FAB); "2-6 items", closely related; items always keep label text; don't use together with a toolbar or navigation rail; close button always 56dp; item height 56dp; FAB margins 16dp, 24dp in large and extra-large windows; gap FAB-to-menu 4dp recommended. Close button label "Toggle menu", role Button, state expanded/collapsed.

### Split button (`split-button`)

- Main action plus a menu of related actions. Leading button label "one or two words"; trailing button always keeps the expand/collapse icon (rotates 180 degrees). Menu aligned with the trailing button, 4dp away. Heights 32 / 40 / 56 / 96 / 136dp, 2dp gap. Each half needs a 48x48dp target. Trailing button's label conveys "more options" and the expanded/collapsed state.

### Segmented buttons (`segmented-buttons`) - no longer recommended

- Legacy facts still on the page: single-select or multi-select; "2-5 segments"; more than five -> chips; height 40dp; target 48dp; don't mix icon-only and text segments; don't span the full width of larger screens; with icon + label the icon is replaced by a checkmark when selected; roles Radiogroup (single) and Checkbox (multi).

## 4. Communication components

### Badges (`badges`)

- Small (6dp dot, no text) and large (16dp high; 16x34dp at max characters). "The maximum number of characters within large badge label text is four, including a +". No example such as "999+" is given.
- Anchored "inside the icon bounding box, at the upper trailing edge"; fixed position (mirror for RTL). Keep the default colour mapping; custom roles need 3:1. Hide the nav-bar badge once the destination is selected. In the expanded rail the badge sits next to the label. Use a small badge where space is tight (app bars).
- Screen reader: numeric badges read the number; non-counting badges announce "New notification".

### Progress indicators (`progress-indicators`) and loading indicator (`loading-indicator`)

- Wait-time table (both pages): under 200ms no indicator; 200ms to 5s loading indicator; over 5s progress indicator.
- Progress: linear ("on the edge of a container") or circular ("centered in an element"); determinate or indeterminate; "a process should be represented by the same variant ... throughout the product"; switch from indeterminate to determinate when information becomes available; determinate "must accurately represent the progress". One indicator per group, not one per item. Flat or wavy shape.
- Numbers: linear height 4dp (thick 8dp; 10dp with wave); stop indicator 4dp circle, "required if the track has a contrast below 3:1"; circular default 40dp (48dp wavy), allowed range 24dp to 240dp; linear not in elements smaller than 40dp; end padding min 4dp. Linear mirrors in RTL; circular does not.
- In a button: circular, flat shape, indicator in the label colour, no track.
- Loading indicator: shape-morphing, indeterminate only; "Don't transition a loading indicator into a progress indicator"; default 48dp, range 24dp to 240dp; contained variant when over content and for pull-to-refresh (Compose only). Pull-to-refresh needs a threshold and a non-gesture alternative (e.g. Refresh action). Keep it in view until the refresh completes.
- Accessibility (both): progress bar role; label names process and content ("Loading news article"); indicator 3:1.

### Snackbar (`snackbar`)

- Use: low-priority process feedback that needs no action; dialog for high priority/required action (table on page). "Only one snackbar may be displayed at a time." "A snackbar can contain a single action." Must not be the only way to reach a core use case.
- Numbers: single line 48dp, two lines 68dp (tokens; guideline prose says "expand vertically from 48dp to 64dp"). Text up to two lines in compact; a long action may go on a third line.
- Timing: "Snackbars without actions can auto-dismiss after 4-10 seconds, depending on platform." "Snackbars with actions should remain on the screen until the user takes an action ... or dismisses it."
- Rules: text button only (no filled or elevated); avoid icons, styled text, inline links; opaque container; bottom of the UI, above FABs, not in front of navigation; don't stack; don't put snackbars flush to an edge in wide layouts (left- or centre-aligned, consistent).
- Accessibility: announce without moving focus (polite live region on Android and web); never trap focus; Esc dismisses when focused. Web: auto-dismissing content must also appear inline.

### Tooltips (`tooltips`)

- Plain: label for icon-only elements; not needed when the element already has a text label. Rich: longer explanation, optional subhead, "up to two text buttons". Don't hide critical information in a tooltip ("Use an interruptive dialog instead").
- Numbers: plain 4dp from an element with a visual boundary, 8dp otherwise; plain min height 24dp, max width 320dp; "disappear 1.5 seconds after navigating away"; repositions in 8dp increments. One tooltip at a time.
- Trigger: hover on desktop, "tap and hold" on mobile; persistent rich tooltips only on click/tap or on page load; not on icon buttons. Tooltip role; don't trap focus.

## 5. Containment components

### Bottom sheets (`bottom-sheets`)

- Use: "supplementary content and actions on a mobile screen", compact and medium. Standard: coexists with the main region (e.g. audio player, map details). Modal: blocks the app; "an alternative to inline menus or simple dialogs on mobile, especially when offering a long list of action items, or when items require longer descriptions and icons". "Modal bottom sheets are used in mobile apps only."
- Numbers: full window width up to 640dp; above 640dp, 56dp top and side margins; top margin 72dp; drag handle 32x4dp with 22dp vertical padding and a 48dp interactive top area; 28dp top corner radius (overview). Initial height of a modal sheet "capped at 50% of the screen height".
- Dismiss (modal): item/action, scrim tap, swipe down, close affordance ("Display a close affordance in a full-screen modal bottom sheet"). Predictive back supported.
- Drag handle: selecting it cycles preset heights; "Material requires the inclusion of a single-pointer alternative" when heights exist without a handle. Label only the handle, role button.
- Adaptive: on larger expanded windows "a bottom sheet can be swapped for a side sheet".

### Side sheets (`side-sheets`)

- Standard: medium to expanded, stays visible beside content (filters, details). Modal: "preferred in compact breakpoints"; must be dismissed. Trailing edge ("usually on the right side"), left in RTL; optional 16dp inset.
- Numbers: max width 400dp; start/end padding 24dp; bottom action area 72dp; modal corner radius 16dp (overview); token "docked container width" 256dp.
- "Material requires that a close affordance, such as a close icon button, is always present". Vertical scroll only. Role Dialog. Compose availability: Unavailable.

### Dialogs (`dialogs`)

- Use: "critical information" or a required decision; "used sparingly". Not for low or medium priority ("Instead use a snackbar"); a dropdown menu is named as a less disruptive alternative.
- Basic dialog: width min 280dp, max 560dp; 28dp corners; 24dp padding; 8dp between buttons. Title optional; avoid "Are you sure?", apologies, alarm.
- Actions: "Dialogs should contain a maximum of two actions." One action only if it is an acknowledgement; two = one confirming + one dismissing. Confirming action at the trailing edge, dismissive to its left; stacked buttons put the confirming action on top. A third action ("Learn more") "is not recommended". Disable the confirming action until a choice is made; "Dismissive actions are never disabled."
- Full-screen dialog: "for compact breakpoints only"; use a basic dialog at medium and expanded. For tasks needing keyboard input, unsaved changes, or nested dialogs. Close "X" is the only navigation; confirm with a specific verb (Save, Send, Create), "Avoid ... Done, OK, or Close"; don't disable the confirm button here; closing with unsaved changes shows a discard confirmation. Header 56dp. Field errors inline; general errors in a basic dialog.
- Behaviour: avoid scrolling; if needed, title and buttons stay pinned. On larger screens custom positions respect a 56dp margin. Escape closes; focus goes to the first interactive element; Android titles fit within four lines at 200% text.

### Cards (`cards`)

- One subject per card; elevated, filled, outlined differ by style only. "Don't force content into cards when spacing, headlines, or dividers would create a simpler visual hierarchy."
- Numbers: 12dp corner radius; 16dp left/right padding; "Padding between cards: 8dp max".
- Either the whole card is actionable or it holds actions, not both ("An action shouldn't be placed on an actionable surface"). One swipe action per card; no swipeable content inside. On mobile, content inside a card does not scroll; cards expand instead. Drag and swipe need a single-pointer alternative. Compact windows: consider lists.

### Carousel (`carousel`)

- Layouts: multi-browse, uncontained, uncontained multi-aspect ratio, hero, center-aligned hero, full-screen. Snap scrolling for multi-browse, hero, full-screen; default scrolling only for uncontained.
- Numbers: small item 40-56dp; item corner 28dp; 16dp leading/trailing padding, 8dp between items; compact windows show "up to three carousel items" with text; multi-aspect widths 9:16 to 16:9; item text max two lines (caution).
- Full-screen: portrait only, compact and medium, "must use snap-scrolling".
- Accessibility: on vertically scrolling pages a "Show all" button (or header arrow, 48dp) is required; no buttons inside or beside the carousel; reduced motion removes parallax and size changes.

### Lists (`lists`) and divider (`divider`)

- List item heights (tokens): one line 56dp, two lines 72dp, three lines 88dp; elements top-align at 88dp or 3+ lines; leading icon 24dp (expressive 20dp), avatar 40dp, image 56dp; targets "at least 48x48dp". Supporting text one to three lines.
- Selection: checkboxes or switches for multi-select; radio buttons for single-select; the selected state applies to the whole item; show selection with more than colour. Multi-action items: primary action takes most space, supplementary action trailing. Swipe actions need an alternative (e.g. More icon).
- Expressive: gaps for contained/segmented lists; "Limit dividers to uncontained or complex lists". Selected corner 16dp; unselected 4dp inner, 16dp outer.
- Adaptive: edge to edge in compact, item opens a detail page; list-detail side by side from medium; line length 40-60 characters ideal, up to 120.
- Divider: full-width separates larger unrelated sections; inset separates related items (16dp inset); "Use full-width dividers sparingly"; group things, don't separate individual items; vertical dividers exist. Overview: "Only use dividers if items can't be grouped with open space".

### Menus (`menus`)

- Use: "a temporary set of actions. To show actions on screen at all times, use a toolbar instead." Overflow, text field dropdown, select, context menus (secondary click or press-and-hold).
- Numbers: expressive vertical menu item height 44dp, icons 20dp, gap 2dp; baseline item 48dp, icons 24dp, width 112dp min to 280dp max, 4dp corners; slot targets "48x48dp or larger".
- Rules: unavailable items "should appear disabled rather than be removed"; gaps: one or two, never in scrollable menus; scrollable menus show a persistent scrollbar; submenus best on large screens and "not currently available on Jetpack Compose"; multi-select menus stay open; no buttons or switches inside items.
- Adaptive: "Consider adapting menus into bottom sheets on small screens."
- Accessibility: focus first item on open; Escape, outside tap or system back closes; disabled items focusable.

## 6. Selection and input components

### Checkbox, radio button, switch

- Checkbox (`checkbox`): multiple related options; parent/child with indeterminate state; label is tappable. 18dp box, 40dp state layer, 48dp target. "If a list consists of multiple options, don't use switches."
- Radio (`radio-button`): single choice with all options visible; "Use radio buttons when there are five or fewer options"; otherwise consider a dropdown menu; vertical list ("Avoid using horizontal radio button lists"); "should always have one option pre-selected" (the accessibility tab allows a group to start with none selected); cannot be deselected, so offer a "None" option; 20dp icon, 48dp target. Don't nest.
- Switch (`switch`): standalone binary settings, effect immediate, no Save. 52x32dp track, 48dp target. Not for opposing options (list vs map): "Use a connected button group instead." Not a replacement for a button. Always an inline label; handle icon must be unambiguous (check / X). Use checkboxes when a Save is required.
- All three: "Don't apply density ... by default" (48x48 targets). Changes take effect immediately unless inside a dialog/page that must be saved (radio page).

### Chips (`chips`)

- Assist (action, verb label), filter (filter a collection; alternative to segmented buttons or checkboxes; single or multi-select but don't mix behaviours on a page), input (user-entered entity; trailing remove icon required), suggestion (product-generated).
- Numbers: height 32dp; 8dp corners; icon 18dp; avatar 24dp; 8dp minimum between chips; "minimum 48dp target size, regardless of placement or density"; label "20 characters or fewer"; min chip width 88dp when it has a 48x48 secondary target.
- Rules: chips are not buttons ("no more than 3 buttons in a single arrangement"; actions that progress a flow are buttons); never a single chip; not elevated on a plain page; inline row, wrap or scroll horizontally (over two rows
  -> scroll). "Material requires" a secondary cue that chips are interactive (label, context, outline role, or icon).
- Accessibility: chip label 3:1; horizontally scrolling sets need a "Show all" reflow or menu; action chips expose button semantics.

### Sliders (`sliders`)

- Standard (from zero/start), centered (default in the middle), range (two handles; "avoid using it in vertical orientation"). "Changes made with sliders must take effect immediately." Track height XS 16, S 24, M 40, L 56, XL 96dp; handle 4dp wide, height 44 / 44 / 52 / 68 / 108dp. Inset icon only on M, L, XL standard sliders. Stops: not too many; end stops required unless the inactive track has 3:1. Value label shows on interaction; one at a time for range. Arrow keys step; Home/End jump.

### Date pickers (`date-pickers`), time pickers (`time-pickers`), scroll fields (`scroll-fields`)

- Date: docked (text field + dropdown calendar; "works best for medium and expanded"), modal (dialog; full-screen modal "recommended" on compact for ranges), modal date input. "Don't use a modal date picker to prompt for dates in the distant past or future, such as a date of birth" -> modal input or docked. Modal 360x524dp; modal input 328x512dp; docked 360x456dp; date cell 40dp (modal), targets 48x48dp. "Don't scale the date picker responsively." Text entry must always be available; no input masks while typing; accept several formats; dates 4.5:1 contrast.
- Time: scroll (inline preferred), input (keyboard), dial (modal only; "avoid ... for granular time selection"). "Only use for selecting hours and minutes"; preset or limited times -> button group, menu or combo box. "Material requires time pickers to allow direct time entry through text input"; don't remove the toggle. Follow the 24-hour setting. Dial face 256dp; dial items and AM/PM targets 48x48dp. Don't crop or scroll the dial; swap orientation or variant.
- Scroll fields: numeric/measurement selection; inline preferred, then non-modal dialog, modal rarely. Min widths: small 100dp, medium 144dp (token: 120dp), large 186dp; inactive values need 48dp-high targets; always provide a text-input alternative; avoid five or more consecutive digits; "If using scroll fields to choose time, use a time picker instead."

### Text fields (`text-fields`)

- Filled and outlined: same function, choose by style; don't mix them "next to each other or within the same form".
- Numbers: container 56dp ("Target size 56dp"); icons 24dp; 16dp side padding (12dp with icons); supporting text 4dp below.
- Rules: "Every text field should have a label" (or an adjacent label); label always visible, never truncated or multi-line; required = asterisk plus an explanation; replace supporting text with error text (don't add a second line); "strongly recommended to show an error icon"; character counter when a limit exists; prefix/suffix for units; single-line vs multi-line vs text area; text fields "should not span the full width of a large screen"; don't apply density by default. Outline 3:1 against the background.

## 7. "Which component?" decision tables

### 7.1 Primary navigation by window size class and destination count

| Window size class | 3-5 destinations | More than 5 destinations | Source statement |
|---|---|---|---|
| Compact | Navigation bar, vertical items | Navigation bar for the top destinations + modal expanded rail opened from a menu icon, or modal expanded rail alone | nav-bar: "Compact: ... use a navigation bar or modal navigation rail"; rail: "Compact windows should always use a navigation bar"; ">5 ... hide the navigation behind a menu icon using a modal expanded navigation rail" |
| Medium | Navigation bar with horizontal items, or collapsed rail ("decide based on whether horizontal or vertical space is more important") | Collapsed rail (3-7) and/or modal expanded rail | nav-bar and rail Adaptive sections |
| Expanded, large, extra-large | Collapsed rail (3-7 items); expanded rail (standard) when space allows | Expanded rail, standard or modal ("consider available horizontal space and the number of destinations") | "Expanded and extra-large: Use a navigation rail instead"; "Use a navigation rail, not a navigation bar" |
| Fewer than 3 destinations (any) | Tabs, not a navigation bar | - | "Don't use a navigation bar for fewer than three destinations. Instead, use tabs." |

- Never show a navigation bar and a rail together; never a navigation bar together with a toolbar that has navigation.
- Navigation drawer appears in none of the rows for Expressive: "no longer recommended"; baseline guidance was modal drawer in compact/medium, standard drawer in expanded and up, for 5+ destinations or 2+ hierarchy levels.
- Secondary navigation inside a destination: tabs (primary, then secondary); a floating toolbar may act as local tabs.
- [Inference] The pages give no rule for exactly which destinations stay in a compact navigation bar when there are more than five; the >7 case for a collapsed rail is covered only by "can reveal secondary destinations" when expanded.

### 7.2 Dialog vs bottom sheet vs side sheet vs snackbar vs menu vs full-screen

| Need | Component | Window size note | Key statement |
|---|---|---|---|
| Brief, low-priority feedback, optional single action (Undo) | Snackbar | 1-2 lines compact; one line preferred medium+ | "minimally interruptive and don't require user action" |
| Critical information or a decision that must block | Basic dialog (max two actions) | all; 280-560dp wide | "Dialogs block app usage until the user takes a dialog action" |
| Multi-field task, unsaved changes, nested dialogs | Full-screen dialog | compact only; basic dialog from medium up | "Full-screen dialogs are for compact breakpoints only" |
| Short list of actions/choices from a control | Menu | best from medium up; compact -> consider a modal bottom sheet | "Consider adapting menus into bottom sheets on small screens" |
| Long action list, items with icons/descriptions, on a phone | Modal bottom sheet | "mobile apps only"; initial height <= 50% | "alternative to inline menus or simple dialogs on mobile" |
| Supplementary content that coexists with the main region (player, map details) | Standard bottom sheet | compact, medium (max width 640dp) | "co-exist with the screen's main UI region" |
| Persistent supplementary region (filters, details) | Standard side sheet | medium to expanded | "remain visible while people interact with primary content" |
| Same content where space is short | Modal side sheet | "preferred in compact breakpoints" | must be dismissed; close affordance required |
| Explain an unlabeled control | Plain tooltip | - | not for critical information |
| Introduce or explain a feature | Rich tooltip | - | up to two text buttons |
| Actions always visible for the page | Toolbar (docked or floating) | not together with a navigation bar | "To show actions on screen at all times, use a toolbar" |
| One main action plus variants | Split button | - | opens a menu from the trailing button |
| 2-6 related creation actions from the main action | FAB menu | any; not with toolbar or rail | "replace the speed dial" |

### 7.3 Button hierarchy

| Emphasis | Component / style | Use | Limit stated |
|---|---|---|---|
| Highest | FAB / extended FAB | Most important constructive action of the screen | One per screen; not destructive or minor |
| High | Filled button | "important, final actions that complete a flow" | "ideally for only one action on a page" |
| Medium-high | Filled tonal button | Lower-priority action needing more emphasis than outlined | - |
| Medium | Outlined button | Important but not primary; pairs with filled as secondary | Simple backgrounds; looks like a chip (caution) |
| Low | Text button | Lowest priority; dialogs, cards, snackbars | Never underlined |
| Special | Elevated button | Tonal + shadow for separation from a busy background | "only when absolutely necessary" |
| Icon-only | Icon button: filled > tonal > outlined > standard | Common, well-understood actions | "Only use a few icon buttons at once"; 48dp target |
| Dynamic/contextual | Assist or suggestion chip | Contextual options, never the step-completing action | Always in a set |
| App bar | One filled or tonal icon button at most | Primary page action | "Don't put multiple filled or tonal buttons in the app bar" |

Note: the page lists the five styles "in order of emphasis" as elevated, filled, tonal, outlined, text, but its prose
ranks filled highest and tells you to avoid elevated; treat elevated as a situational variant of tonal.

### 7.4 Selection controls by data type

| Data | Component | Statement |
|---|---|---|
| One of 2-5 visible options | Radio buttons (vertical) | "five or fewer options" |
| One of many, or space is tight | Menu (dropdown / exposed dropdown text field) | "Consider using a drop-down menu instead of radio buttons" |
| One of a few "opposing" views or modes (list vs map) | Connected button group (single-select) | switch page: "Use a connected button group instead" |
| Several independent options in a list | Checkboxes | "Checkboxes should be used instead of switches if multiple, related options" |
| Single on/off setting, immediate effect | Switch | "Switches are the best way to let people adjust settings" |
| On/off that needs Save | Checkbox | "Avoid using a switch to select multiple options that require people to save" |
| Filter a collection by tags | Filter chips (multi or single) | "alternative to segmented buttons or checkboxes" |
| Value in a continuous or stepped range | Slider (standard / centered / range) | effect immediate |
| Number or unit from a scrollable set | Scroll field (with text-input alternative) | up to four digits recommended |
| Date | Docked date picker (medium+), modal date picker (compact), modal date input (far dates such as birth date) | date-pickers guidelines |
| Time, any minute | Scroll (inline), dial (modal), input | "Only use time pickers when any time can be chosen" |
| Time from presets | Button group, menu, combo box | time-pickers guidelines |
| Free text | Text field (single-line, multi-line, text area) | - |
| Entities typed by the user (recipients) | Input chips in a text field | - |
| Binary action on an item (favorite) | Toggle icon button or toggle button | - |

## 8. The 30 highest-value checkable rules for an agentic UI review

Each is checkable from code or a screenshot. Strength is the page's wording. URL = component slug + tab.

| # | Rule | Strength | Source |
|---|---|---|---|
| 1 | Navigation bar has 3, 4 or 5 destinations | "Don't" (<3, >5) | navigation-bar/guidelines |
| 2 | Every navigation bar / rail item has a visible text label; no truncation, wrapping (bar) or shrinking | "require", "Don't" | navigation-bar, navigation-rail /guidelines |
| 3 | Navigation bar only in compact or medium windows; rail (or expanded rail) from expanded up | "Only use", "Use ... instead" | navigation-bar/guidelines |
| 4 | Never a navigation bar and a navigation rail on screen together | "Never" | navigation-rail/guidelines |
| 5 | Collapsed rail has 3-7 items, sits on the leading edge, is never hidden, is vertical | "should", "Don't" | navigation-rail/guidelines |
| 6 | Active destination: filled icon + active indicator; exactly one active item | "Don't" | navigation-bar/guidelines, /accessibility |
| 7 | New Expressive work does not introduce navigation drawer, segmented button, bottom app bar, baseline medium/large app bar, small FAB, surface FAB | "no longer recommended" | respective /overview |
| 8 | App bar has at most two trailing icon buttons and at most one filled/tonal one; no overflow menu if avoidable | "Up to two", "Don't", "Avoid" | app-bars/guidelines |
| 9 | App bar spans the full window width at its default height (64 / 112 / 120dp) with straight corners | "Always", "Don't" | app-bars/guidelines, /specs |
| 10 | Small app bar title is one line; long titles use a flexible app bar with max two lines; never truncated | "Don't" | app-bars/guidelines |
| 11 | A docked toolbar and a navigation bar are never shown together | "should not", "Don't" | toolbars/guidelines |
| 12 | At most one FAB (or extended FAB) per screen; action is constructive, not destructive | "Don't" | floating-action-button, extended-fab /guidelines |
| 13 | FAB is never shown disabled; it is hidden when its action is unavailable | "Don't" | floating-action-button/accessibility |
| 14 | Extended FAB always has a label (icon optional); FAB menu opens only from a FAB and has 2-6 labelled items | "can't", "Don't" | extended-fab, fab-menu /guidelines |
| 15 | At most one filled button per screen/region; destructive or secondary actions use lower-emphasis styles | "ideally" | buttons/guidelines |
| 16 | Button labels: sentence case, one line, not truncated, 1-3 words; one leading icon at most | "Don't", "ideally" | buttons/guidelines |
| 17 | Every interactive element has a touch target of at least 48x48dp, including XS/S buttons (32/40dp visual), 32dp chips, 18dp checkboxes, 20dp radios, nested icon buttons | "must", "should" | buttons/specs, chips, icon-buttons/accessibility, toolbars |
| 18 | Icon-only controls have an accessibility label describing the action (not the icon name) | should | icon-buttons/accessibility |
| 19 | Basic dialog has at most two actions; confirming action at the trailing edge, dismissive before it; single action only for acknowledgement | "should", "must", "Don't" | dialogs/guidelines |
| 20 | Dialog title is a specific statement/question, not "Are you sure?"; dialog used only for blocking/critical content | "Avoid", "Don't" | dialogs/guidelines |
| 21 | Full-screen dialog only in compact windows; switches to a basic dialog from medium up | "only" | dialogs/guidelines |
| 22 | One snackbar at a time; at most one action, as a text button; snackbars with an action do not auto-dismiss; placed above the FAB and not over navigation | "may", "should", "Don't" | snackbar/guidelines, /accessibility |
| 23 | Modal bottom sheet opens at no more than 50% of screen height, is dismissible by scrim/swipe/back, and has a single-pointer way to resize | "can't exceed", "Material requires" | bottom-sheets/guidelines, /accessibility |
| 24 | Side sheet always has a close affordance | "Material requires" | side-sheets/accessibility |
| 25 | Switch only for an immediate on/off setting; multiple options in a list use checkboxes; one-of-many uses radios (<=5) or a menu | "Don't", "Use" | switch, checkbox, radio-button /guidelines |
| 26 | Chips appear in a set (never one chip), labels <= 20 characters, not used for the flow's primary/next action | "Don't", "Avoid" | chips/guidelines |
| 27 | Fixed tabs: no more than four; more -> scrollable tabs; tabs not used for sequential steps; tab labels consistent (all icon+label or none) | "Avoid", "Don't" | tabs/guidelines |
| 28 | Text field always has a visible label; error replaces supporting text and shows an error icon; filled and outlined not mixed in one form | "should", "Don't", "strongly recommended" | text-fields/guidelines |
| 29 | Waits: <200ms none; 200ms-5s loading indicator; >5s progress indicator; determinate when progress is known; one indicator per group; accessibility label names what is loading | recommendation table, "must accurately represent" | progress-indicators, loading-indicator |
| 30 | Gesture-only interactions have a single-pointer alternative: pull-to-refresh (refresh action), swipe on list items/cards (menu or button), sheet drag (handle tap), carousel on a scrolling page (Show all), scroll field / dial (text input) | "Material requires", "need", "must" | loading-indicator, lists, cards, bottom-sheets, carousel, time-pickers /accessibility |

Runners-up: badge text max four characters; tooltip only one at a time and never for critical info; menu items
disabled not removed; date of birth not via modal calendar; text fields and connected button groups width-capped on
large windows; progress variant consistent per process; re-selecting the active nav item scrolls to top.

## 9. Numbers Material does NOT specify (absence demonstrated on the fetched pages)

"Absent" = not in the guidelines, specs prose, measurements table or token dump of that component. Diagram-only
dimensions cannot be excluded (images were not read).

| Number agents commonly state | What the page actually says | Absence check |
|---|---|---|
| "FAB sits 16dp from the screen edges" | FAB guidelines/specs/tokens contain no margin value. 16dp appears only for the extended FAB ("should have margins of 16dp") and the FAB menu page ("The FAB should always have 16dp margins", 24dp in large/XL windows) | grep "margin" in FAB guidelines+specs+tokens: 0 |
| "Snackbar shows for 4 seconds" / "LENGTH_SHORT = ..." | Only a range: "4-10 seconds, depending on platform" | grep seconds/ms/duration: only that range |
| Snackbar margins, width, max width | No value; only "fixed distance from the leading, trailing, and bottom edges" and line-length advice (40-60 characters) | grep margin/16dp/24dp in snackbar guidelines+specs: 0 |
| Bottom sheet "peek height 56dp" / detent fractions | No peek height; only "initial vertical position ... capped at 50% of the screen height" and unnamed "preset heights" | grep peek: 0 |
| Button minimum width (old 64dp / 88dp lore) and maximum width | No min or max width; only "shouldn't be narrower than its label text" and "constrain button width" | grep min/max width in buttons pages+tokens: 0 |
| Text field min/max width (e.g. "280dp") | None; only "should not span the full width of a large screen" | grep: 0 |
| Badge overflow format "99+" / "999+" | Only "maximum ... four, including a +" | grep 999 / 99+: 0 |
| Maximum number of tabs for scrollable tabs | None ("as many tabs as needed"); only fixed tabs get "avoid more than four" | tabs/overview, /guidelines |
| Maximum destinations in an expanded rail or a drawer | None. Collapsed rail 3-7; drawer "5 or more" is a lower bound | navigation-rail, navigation-drawer |
| Maximum segments in a connected button group | None on button-groups pages (2-5 belongs to the retired segmented button) | button-groups/guidelines, /specs |
| Maximum number of menu items / menu max height | None for count; baseline menu has width 112-280dp only | grep max/maximum in menus specs+tokens: 1 hit (width) |
| Maximum number of chips, list rows, cards, carousel items | None. Carousel research note: participants "expected around 10 items"; compact shows up to three at once | pages cited |
| Card elevation in dp, dialog elevation in dp | Elevation tokens are level references (swatches), no dp in page text | cards/specs has no dp elevation |
| Nav bar / rail label character limit | Words only: "1-2 words" (bar), "one word" (rail) | grep characters: none for labels |
| Dialog text length limits | None; only four lines for the title at 200% text on Android | dialogs/accessibility |
| Spacing between adjacent touch targets (generic "8dp") | Only chip-specific ("8dp minimum space between chips") and component paddings | component pages |
| App bar title character limit | None; "brief enough to easily fit" | app-bars/guidelines |
| Animation durations for sheets, dialogs, menus | Component pages name transition patterns only ("enter and exit", "container transform"); no ms | all guidelines pages |

Internal inconsistencies to report as-is rather than resolve: snackbar two-line height 64dp (prose) vs 68dp (token);
scroll field medium min width 144dp (prose) vs 120dp (token); side sheet 400dp max width (measurements) vs 256dp
(token "docked container width"); nav item label "1-2 words" (bar) vs "one word" (rail); radio group "always one
pre-selected" (guidelines) vs "one ... or none" (accessibility); app bar "avoid an overflow menu" vs "actions ...
collapse into an overflow menu at smaller breakpoints"; button-emphasis order list vs prose (section 7.3).

## 10. Explicit "Don't" captions (as shown on the pages, lightly shortened)

- Navigation bar: more than five items; remove labels; fewer than three destinations ("Instead, use tabs"); scroll or reposition destinations; multiple or low-contrast colours; active indicator on more than one destination; wrap or truncate labels; shrink long text; cover the bar with a FAB; use on desktop layouts; outlined icons on selected items.
- Navigation rail: use horizontally; FAB below navigation items (avoid); indicator on more than one item; truncate or ellipsize labels; reduce type size; more than two colours for destinations; same unfilled icon for selected and unselected.
- Navigation drawer: dividers between individual destinations; wrap label text; shrink text; icons on some destinations only.
- App bars: multiple filled or tonal buttons; three icons plus an avatar in a search app bar; curved container shapes; shorter than default height; wrap text in a small app bar.
- Toolbars: navigation bar together with a toolbar that has navigation controls; modify the container shape; overwhelm with too many controls; exceed the window or pane edge; emphasize multiple buttons (e.g. button + FAB); mix too many control types; square filled icon buttons in floating toolbars; wide buttons in vertical toolbars; extra space beyond the items; multiple toolbars in smaller windows; collapse and scroll off at once.
- Tabs: sequential content; icons+labels on only some tabs; truncate labels unless required; swipeable items in the content area; scroll tabs behind an app bar; Space/Enter for moving between tabs.
- Buttons: clutter with too many buttons; container narrower than its label; toggle label length changing dramatically; wrap text; icon stacked above text; two icons; ungroup icon and label; long flat stretched buttons.
- Button groups: mix colour styles in connected groups. Icon buttons: toggle for actions without a selected state; contrast below 3:1. Split button: unusual menu modifications; long labels or a changed trailing icon.
- FAB: multiple FABs on a screen; minor, overflow, unclear or destructive actions; confusing icons; FABs on individual cards; keep the FAB on screen when switching pages; obscure an actionable element's focus indicator.
- Extended FAB: multiple on one screen; as an option in a set of actions; icon without a label; wrap or truncate text; on top of toolbars; in the upper half of a mobile screen; on cards or inside containers; paired with a floating toolbar; over another actionable element.
- FAB menu: one item; with a toolbar or navigation rail; remove the label; expand container sizes; change shapes; block focus indicators; obstruct the close button.
- Segmented buttons (legacy): more than five segments; segments wrapping; mixing icon-only and text; full width on large screens; outline contrast under 3:1.
- Badges: change position arbitrarily or place over the icon; custom colours (avoid); cut off or collide; large badge overlapping a trailing element (avoid).
- Progress / loading: progress for each activity in a group; indicators on every button in a list; contrast below 3:1; removing the stop indicator at low contrast; loading indicator turning into a determinate indicator; scrolling the pull-to-refresh indicator off-screen.
- Snackbar: styled text or inline links; label same colour as the button; filled or elevated button; altered container shape; in front of navigation; in front of or behind a FAB; fully covering focused elements; flush to an edge; side by side; stacked; animating other components with it.
- Tooltips: plain tooltip on an element that already has a label; critical information; subhead over one line; more than one at a time; persistent rich tooltip on icon buttons.
- Dialogs: low or medium priority information; ambiguous titles; dismissive action to the right of the confirming action; unclear choices (a lone Cancel); a basic dialog on confirming a full-screen dialog; the confirming action used to dismiss; non-critical information.
- Sheets: side sheet inset far beyond 16dp; horizontal scrolling in a side sheet; side sheet without a close button.
- Cards: force content into cards; scroll within a card (mobile); swipeable content inside a card or detaching parts; cards bumping other elements when dragged.
- Carousel: items too small to recognise; free scrolling on full-screen carousels; buttons inside or beside the carousel; covering the carousel with UI; focusing the container.
- Lists: scale components without adjusting line length. Menus: focusable dividers or gaps.
- Checkbox: switches for a list of multiple options. Radio: nesting; multi-select with radios.
- Switch: opposing options; replacing a button; multi-option selections that need Save; ambiguous handle icons; text inside the switch.
- Chips: replace major actions; finish or progress a task; a single chip alone; elevation on a plain page or as pressed feedback; labels over 20 characters; a filter set with one option.
- Sliders: vertical range slider; inset icon on tracks under 40dp, on centered or on range sliders.
- Date / time: scale the date picker up responsively; remove the input toggle from dial or scroll pickers; crop the dial. Scroll fields: five or more consecutive digits.
- Text fields: both variants in one form; truncated or multi-line labels; error text added below supporting text; fixed margins / full width on large devices; outline colours under 3:1.

## 11. Proposed grouping into four reference files (each <= 300 lines)

Mirrors `skills/apple-hig/references/components-*.md`; each file opens with its decision table from section 7 and
ends with "Common mistakes" drawn from section 10.

| File | Components | Opening table | Est. lines |
|---|---|---|---|
| `components-navigation.md` | Navigation bar, navigation rail (collapsed, expanded, modal), navigation drawer (legacy note), app bars (incl. search app bar), tabs, search, toolbars' relation to navigation | 7.1 primary navigation by window size class and count | 280 |
| `components-presentation.md` | Dialogs (basic, full-screen), bottom sheets, side sheets, menus (incl. context menus), snackbar, tooltips, badges, progress indicators, loading indicator | 7.2 dialog vs sheet vs snackbar vs menu | 290 |
| `components-controls.md` | Buttons, button groups (and legacy segmented), icon buttons, split button, FAB / extended FAB / FAB menu, toolbars (docked, floating), checkbox, radio, switch, chips, sliders, date pickers, time pickers, scroll fields, text fields | 7.3 button hierarchy and 7.4 selection by data type | 300 (tightest; if it overflows, move pickers + text fields + scroll fields to a fifth file `components-input.md`) |
| `components-content.md` | Lists, cards, carousel, divider, plus cross-cutting rules: 48dp targets, density, label/icon rules, RTL mirroring, the legacy-vs-Expressive status table from section 1 | Status/rename table | 220 |

Rationale: toolbars are documented by Material as the home of page actions ("Use a toolbar to display page actions")
and replace the bottom app bar, so their rules live with controls, while the "never with a navigation bar" rule is
repeated in navigation. Badges and progress sit with presentation because the Apple skill's presentation file is
already the feedback/overlay file and the content file is the shortest.

## 12. Stale lore and items not verified

Stale lore contradicted by the current pages:
- "Top app bar" and "bottom app bar" are no longer the component names: app bar and (docked) toolbar. Old URLs redirect.
- Navigation bar height 80dp is the baseline value; the recommended flexible navigation bar is 64dp. Rail 80dp is baseline; collapsed rail is 96dp (80dp narrow).
- Navigation drawer for tablets/desktop: replaced by the expanded navigation rail in Expressive.
- Segmented button: replaced by the connected button group. Speed dial / stacked small FABs: replaced by FAB menu.
- Small FAB (40dp [M], no value rendered on the page) is no longer recommended; medium FAB 80dp is new and "most recommended"; large FAB stays 96dp.
- Button icon 18dp and one size (40dp) are baseline/deprecated tokens; Expressive small buttons use a 20dp icon and 16dp side padding (24dp "no longer recommended"), with five sizes.
- "Continuous / discrete slider" naming is gone (standard slider, stops configuration).
- "Search bar and search view" are one component ("search"); medium/large baseline app bar heights 112/152dp are replaced by flexible 112/120dp (136/152dp with subtitle).
- Indeterminate circular progress for short waits: the loading indicator "should replace most uses".
- Elevation overlays/shadows: app bars separate by colour fill on scroll, no shadow (stated on app-bars/overview).

Not verified in this workstream:
- Carousel implementation availability (table did not render). Compose/Views API names, `@Experimental` status and library versions for any component (belongs to the Compose/Views API workstreams); the overview pages only say "Available" / "Unavailable".
- Dimensions that exist only inside measurement diagrams (for example nav bar item margins, FAB padding diagrams, date/time picker paddings) and all shape, typography and elevation token values.
- Whether "window size class" breakpoints (dp widths) match the component pages' "compact / medium / expanded / large / extra-large" terms: the component pages use the names only and link to the adaptive-design foundations.
