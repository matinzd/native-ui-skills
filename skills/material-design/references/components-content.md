# Content components: cards, lists, carousel, dividers, progress, badges

Scope: configuring cards, lists (baseline and expressive), carousels, dividers, progress indicators, the loading indicator and badges; plus the table of numbers Material does not publish. API names are in `references/implementation-components.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How to read this file
- Which container or indicator
- Cards
- Lists
- Carousel
- Dividers
- Progress indicators
- Loading indicator
- Badges
- Numbers Material does not specify
- Common mistakes

## How to read this file

- [Conv] `[MD]` covers Material's "should", "avoid" and "Don't" captions: recommendations. `[Req]` is used only where the page says "must", "need" or "requires". `[API]` marks availability stated on the overview pages.
- [Conv] Numbers are in dp from the specs measurement or token tables unless marked "prose". Shape, elevation-level and color token values render as swatches on the site and are not reported as numbers here.

Source: https://m3.material.io/components

## Which container or indicator

| Need | Use | Page statement |
|---|---|---|
| Content and actions about one subject, scanned as a unit; an entry point to detail | Card | One topic per card |
| Many discrete items to find, compare, select or act on | List | Vertical, optimized for reading |
| The same items in a compact window | List instead of cards | Cards page: consider swapping cards for lists |
| The same items in a larger window | Cards, a multi-column layout, list-detail side by side, or a carousel | Lists page: swap components at larger breakpoints |
| Browsing visual items (photos, media) horizontally | Carousel | Items are primarily visual; text is brief |
| Grouping where spacing alone is not enough | Divider (or a gap in expressive lists and menus) | Only if open space cannot group the items |
| Wait under 200 ms | No indicator | Show the content immediately |
| Wait between 200 ms and 5 s, progress unknown or unimportant | Loading indicator | Replaces most indeterminate circular indicators |
| Wait over 5 s, or measurable progress | Progress indicator, determinate when possible | Linear on a container edge, circular centered |
| Process that starts unknown and becomes measurable | Indeterminate progress indicator, then determinate | Never start with a loading indicator |
| Pull to refresh | Contained loading indicator | Jetpack Compose only, per the page |
| "Something new" or a count on a navigation item, tab or app bar icon | Small badge or large badge | Four characters at most |

Source: https://m3.material.io/components/progress-indicators/guidelines, https://m3.material.io/components/loading-indicator/guidelines, https://m3.material.io/components/cards/guidelines, https://m3.material.io/components/lists/guidelines

## Cards

- [API] The overview lists Jetpack Compose and Android Views as available; there is no Expressive section. Variants: elevated, filled, outlined.
- [MD] The three variants give the same legibility and function; choose by style. Elevated has a shadow, filled gives subtle separation (least emphasis), outlined has a visible boundary (can give the most emphasis).
- [MD] One card, one subject. Make hierarchy inside the card obvious; the container is the only required element.
- [MD] Do not force content into cards when spacing, headlines or dividers would give a simpler hierarchy.
- [MD] A card is either directly actionable (the whole surface is one target, typically opening detail) or a non-actionable container holding buttons and links. Do not place an action on an actionable surface.
- [MD] Cards may hold buttons, icon buttons, chips, sliders, checkboxes, linked text and an overflow menu (usually upper or lower trailing corner). A card does not get its own FAB.
- [MD] Placing text or icons on an image is not recommended; if needed, add a scrim or bounding shape for contrast.
- [MD] Inside a card: full-width dividers for expandable regions, inset dividers between related content.
- [MD] Collections: grid, vertical list or carousel; cards in a collection share the same resting elevation. Filter and sort controls sit outside the collection and apply to every card.
- [MD] Swipe: one swipe action per card (dismiss or change state); no swipeable content such as an image carousel inside a card; parts of a card do not detach on swipe.
- [MD] Pick up and move: raise the card's elevation; it floats over everything except app bars and navigation and does not push other elements aside.
- [Req] Dragging and swiping "need" a single-pointer alternative, such as the same actions in a menu.
- [MD] Scrolling: on mobile, content inside a card does not scroll; the card expands and the page scrolls. On desktop, content may scroll inside a card.
- [MD] Expanding a card with a container transform is for hero moments; ordinary navigation from a card uses a forward and backward transition.
- [MD] Adaptive: in expanded windows use multiple columns and avoid stretching one card across the screen; a horizontal card may become a larger vertical card.
- [MD] Accessibility: a directly actionable card is a tab stop with the button or link role; a container card needs no role; hide purely decorative images from screen readers.
- [MD] Measurement table: corner radius 12; left and right padding 16; padding between cards "8 max". No elevation value in dp appears in the page text.

Source: https://m3.material.io/components/cards/guidelines, https://m3.material.io/components/cards/specs, https://m3.material.io/components/cards/accessibility

## Lists

- [API] The overview lists Jetpack Compose and Android Views as available, each with an Expressive entry. December 2025: the expressive list (standard or segmented style, highlighted selection, slots) is "recommended for new designs".
- [Conv] Status wording differs between tabs: the overview and the baseline section say the baseline list "is still available" and keeps working; the specs variant table marks it "Not recommended. Use expressive lists instead." Do not rewrite an existing baseline list unless asked.
- [MD] Standard versus segmented is a visual choice and does not change behaviour.
- [MD] Keep items short and scannable, ordered logically (alphabetical, numerical). Put supporting visuals and primary text in the same position in every item; anchor visuals to the leading edge, not the center.
- [MD] Container and label text are required; everything else is optional. Supporting text: one to three lines; it may wrap or truncate.
- [MD] Avatars (circular or expressive shapes) represent people or entities; square or rectangular images are for other content.
- [MD] Trailing text carries meta-information (price, count, date); a trailing icon signals status or an action.

| Selection mode | Rules |
|---|---|
| Single-action | The whole item does one thing (navigate); no nested secondary actions; no persistent selected state |
| Multi-action | Primary action takes most of the leading and content space; supplementary actions (bookmark, menu) trail |
| Single-select | Radio buttons; no checkboxes; no nested actions |
| Multi-select | Checkboxes or switches; no radio buttons; no nested actions |
| Non-interactive | Information only |

- [MD] A list has one selection mode at a time, and one selection interaction per item. The selected state applies to the whole item, and selection must not rely on color alone.
- [MD] Switches in list items are for settings that toggle on or off.
- [MD] Gaps and dividers: use gaps for contained (segmented) lists; limit dividers to uncontained or complex lists that need stronger separation.
- [MD] Swipe (Android): items can reveal buttons; the primary action is the final end-aligned one and a full swipe triggers it. Swipeable items should offer another route to the hidden actions, such as a More icon. [API] Swipe-to-reveal is listed as available on Android Views only.
- [MD] Items containing other items can expand and collapse.
- [MD] Compact windows: lists run edge to edge and selecting an item opens a detail page. From medium up: list and detail can sit side by side; lists may show more content, become multi-column, or swap to cards or a carousel.
- [MD] Line length: 40 to 60 characters is ideal; large screens can take up to 120 (raise the line height near that length). Do not scale a list without adjusting line length.
- [Req] Slots: targets "must" be at least 48 x 48; the content slot "must" be the widest; do not add interactive elements that make the item hard to navigate.
- [MD] Accessibility: focus goes to the first item, or to the selected item if there is one; arrow keys move within the list; Space or Enter activates.

| Measurement | Value |
|---|---|
| Item height: one line, two lines, three lines (token) | 56, 72, 88 |
| Alignment | Middle; top-aligned at 88 or taller, or with three or more lines of text |
| Leading and trailing icon (token); expressive | 24; 20 |
| Leading avatar; leading image (token) | 40; 56 x 56 |
| Item leading and trailing space (token) | 16 |
| Targets | 48 |
| Expressive corner radius: selected; unselected | 16; 4 inner and 16 outer |

Source: https://m3.material.io/components/lists/guidelines, https://m3.material.io/components/lists/specs, https://m3.material.io/components/lists/accessibility

## Carousel

- [Unverified] Android availability: the availability table of the carousel overview did not render in the page text checked for this file. Check https://m3.material.io/components/carousel/overview before stating Compose or Views support.
- [MD] The overview names six layouts (November 2025 added uncontained multi-aspect ratio); the guidelines intro still says four.

| Layout | Best for | Scrolling |
|---|---|---|
| Multi-browse | Browsing many visual items at once; at least one large, medium and small item | Snap |
| Uncontained | Customized or text-heavy items of one size that run past the edge | Default (free); snap also works |
| Uncontained multi-aspect ratio | Items of varying width, from 9:16 to 16:9; only when widths really vary | Default |
| Hero | Spotlighting one large item with a peek of the next | Snap |
| Center-aligned hero | A centered large item with a small item on each side | Snap |
| Full-screen | Immersive vertical feeds; one edge-to-edge item | Snap, stated as "must" |

- [MD] Items are primarily visual; text is optional and brief, and adapts as items shrink. For lots of text use the uncontained layout or a series of cards.
- [MD] Except in the uncontained layouts, items stay fully visible and snap into the layout after scrolling. Keep the large item big enough to recognize.
- [MD] Compact windows comfortably show up to three items; with text, show more than three only if they stay easy to recognize. Avoid more than two lines of item text in compact unless the background is simple.
- [MD] Full-screen: portrait orientation only, compact and medium windows only, never landscape.
- [Req] On a vertically scrolling page a carousel "requires" a way to see all items without scrolling horizontally (not for full-screen). Material recommends a "Show all" button below the carousel that opens a vertically scrolling page, or an arrow icon button (48) in the carousel header.
- [MD] Do not put buttons or arrows inside or beside the carousel, cover it with other UI, or make the container focusable.
- [MD] With reduced motion on, drop the parallax effect and the size changes; all items are the same size.
- [MD] Measurement tables: small item width 40 to 56; item corner radius 28; leading and trailing padding 16 (0 for full-screen); 8 between items (16 for full-screen); top and bottom padding 8.
- [Conv] The overview's research note says participants expected "around 10 items" in a multi-item carousel. That is a finding, not a limit.

Source: https://m3.material.io/components/carousel/guidelines, https://m3.material.io/components/carousel/specs, https://m3.material.io/components/carousel/accessibility, https://m3.material.io/components/carousel/overview

## Dividers

- [API] The overview lists Jetpack Compose and Android Views as available; there is no Expressive section.
- [MD] Use a divider only when open space cannot group the items; dividers group things, they do not separate every individual item. Make them visible but not bold.
- [MD] Full-width: separates larger sections of unrelated content, or interactive from non-interactive areas of a container. Use sparingly.
- [MD] Inset: separates related content within a section (emails in a list); use with anchoring elements such as icons or avatars.
- [MD] Using both on one screen: full-width between different kinds of content, inset between nested items.
- [MD] List items with a repetitive format may need no divider at all.
- [MD] A vertical divider can arrange content on larger screens.
- [MD] Measurement table: inset left margin 16 (right 0); middle-inset 16 on both sides. Thickness 1 (token).

Source: https://m3.material.io/components/divider/guidelines, https://m3.material.io/components/divider/specs

## Progress indicators

- [API] The overview lists Jetpack Compose and Android Views as available, each with an Expressive entry (August 2024: configurable track thickness and the wavy shape).
- [MD] Variants: linear (best along the edge of a container) and circular (best centered in an element). Behaviour: determinate (the default) or indeterminate. Shape: flat (the default) or wavy.
- [MD] Use the same variant for the same process everywhere in the product.
- [Req] A determinate indicator "must" accurately represent progress.
- [MD] Switch from indeterminate to determinate as soon as progress information exists.
- [MD] One indicator for a group of loading items, typically at the top of the page; not one per element unless elements are activated independently. Do not put indicators on every button in a list.
- [MD] For a very long wait, let people leave the page while the process finishes.
- [MD] Linear: on the edge of the loading container (the edge that animates, if it changes shape), spanning the element's width. Not in elements smaller than 40. Mirrors in right-to-left languages.
- [MD] Circular: centered on the page or container that is loading; when loading more items, in the empty space where they will appear, not over existing content. Does not mirror.
- [MD] In a button: circular, flat shape in very small buttons, indicator in the color of the label or icon, no track.
- [MD] Wavy suits longer processes and a more expressive tone; it increases the component height and is hard to see at very small sizes.
- [Req] The stop indicator (linear determinate only) is "required" when the track has less than 3:1 contrast with its container or the surface behind it.
- [MD] Accessibility: progress bar role and a label naming the process and the content ("Loading news article"); active indicator contrast 3:1.

| Measurement | Value |
|---|---|
| Linear height (token); thick sample (token); with wave (token) | 4; 8; 10 |
| Stop indicator | 4 circle |
| Circular size (token); with wave (token) | 40; 48 |
| Circular size range (prose) | 24 to 240 |
| Linear end padding (prose) | min 4 |

Source: https://m3.material.io/components/progress-indicators/guidelines, https://m3.material.io/components/progress-indicators/specs, https://m3.material.io/components/progress-indicators/accessibility

## Loading indicator

- [API] The overview lists the loading indicator for Jetpack Compose and Android Views under the Expressive entries only (new in May 2025).
- [MD] A looping shape-morph for short, indeterminate waits (200 ms to 5 s). It should replace most uses of the indeterminate circular progress indicator.
- [MD] It always reflects a real ongoing process; it is never decoration.
- [MD] Do not turn a loading indicator into a determinate progress indicator; if the process can become measurable, start with an indeterminate progress indicator.
- [MD] Placement: centered on the page or container; in the empty space where new content will appear; or inside a button whose action takes a few seconds.
- [MD] Contained configuration (a circle behind the indicator): use it when the indicator sits over other content, and for pull to refresh; not needed directly on a surface.
- [MD] Size: default 48 (shape 38 inside it), flexible between 24 and 240; scale up in larger windows and reserve very large sizes for large and extra-large windows.
- [API] The page states the loading indicator is used for pull to refresh on Jetpack Compose only.
- [Req] Pull to refresh: the indicator "must" pass a threshold before the app refreshes; reversing the gesture past the threshold cancels.
- [MD] Keep the indicator in view until the refresh completes; do not let it scroll off screen. Pull to refresh belongs at the start of lists, grids and card collections with frequently updated content.
- [MD] Pull to refresh cannot be the only way to refresh: provide a single-pointer alternative, such as a refresh action in a menu or app bar.
- [Req] The indicator "must" have 3:1 contrast with its background (the container need not). Progress bar role, with a label such as "Refreshing page".

Source: https://m3.material.io/components/loading-indicator/guidelines, https://m3.material.io/components/loading-indicator/specs, https://m3.material.io/components/loading-indicator/accessibility

## Badges

- [API] The overview lists Jetpack Compose and Android Views as available; there is no Expressive section. Variants: small (a dot, no text) and large (with label text).
- [MD] Badges mark a notification, a count or a status on a navigation destination; they appear in navigation bars, navigation rails, app bars and tabs.
- [MD] A large badge holds at most four characters, including a "+" for "more". The page gives no example format.
- [MD] Anchor the badge inside the icon's bounding box at the upper trailing corner; the position is fixed (mirror it in right-to-left languages). Do not move it arbitrarily or center it over the icon.
- [MD] In an expanded navigation rail, or when the icon is followed by text, the large badge goes at the trailing edge, next to the label.
- [MD] Where space is tight (app bars) use a small badge; never let a badge be cut off or collide with a neighbor.
- [MD] In a navigation bar, hide the badge once its destination is selected; on tabs, update or remove it once the content is viewed.
- [MD] Keep the default color mapping (error and on error); custom roles need at least 3:1 contrast.
- [MD] Screen readers read the badge after its destination: the number for numeric badges, "New notification" for non-counting ones.
- [MD] Measurement table: small badge 6; large badge 16 high, 16 x 34 at the maximum character count.

Source: https://m3.material.io/components/badges/guidelines, https://m3.material.io/components/badges/specs, https://m3.material.io/components/badges/accessibility

## Numbers Material does not specify

"Absent" means the value is not in the guidelines, specs prose, measurement table or token table text of that component, checked 2026-11-23. Dimensions drawn only inside diagram images could not be read. Treat any such number in code or in a review as a product choice or a library default, never as a "Material rule".

| Commonly stated number | What the pages actually give | Evidence of absence |
|---|---|---|
| "FAB sits 16dp from the screen edges" | 16 margins are stated for the extended FAB, and on the FAB menu page (24 in large and extra-large windows) | "margin" occurs 0 times in the FAB guidelines, specs and token text |
| "Snackbar shows for 4 seconds" | Only a range: 4 to 10 seconds, "depending on platform" | That sentence is the only duration on the snackbar pages |
| Snackbar margin, width or maximum width | "A fixed distance" from the edges; 40 to 60 characters ideal line length | No margin, minimum or maximum width in guidelines, specs or tokens |
| Bottom sheet "peek height 56dp", detent fractions | Initial position of a modal sheet capped at 50% of screen height; unnamed "preset heights" | "peek" and "detent" occur 0 times on the bottom sheet pages |
| Button minimum width (64 or 88) or maximum width | Not narrower than its label; constrain width in large windows | No minimum or maximum width in the buttons pages or tokens (88 is a chip rule) |
| Text field minimum or maximum width ("280dp") | Should not span the full width of a large screen | No width value on the text field pages |
| Badge overflow "99+" or "999+" | Four characters maximum, including a "+" | Neither string occurs on the badge, tabs or navigation bar pages |
| Maximum number of scrollable tabs | "As many tabs as needed"; only fixed tabs get "avoid more than four" | No maximum on the tabs pages |
| Maximum destinations in an expanded rail or a drawer | Collapsed rail 3 to 7; drawer "5 or more" is a lower bound | No upper bound on either page |
| Maximum segments in a connected button group | None | "2 to 5 segments" is only on the retired segmented button page |
| Maximum number of menu items; menu maximum height | Baseline menu width 112 to 280 only | The only "max" on the menu specs is that width |
| Maximum number of chips, list rows, cards or carousel items | Carousel: up to three visible in compact; "around 10" is a research note | No "maximum number" on those pages |
| Card or dialog elevation in dp | Elevation tokens reference levels; their values are not in the page text | No dp value beside any elevation token |
| Navigation label character limit | Words only: "1-2 words" (bar), "one word" (rail) | No character count for labels |
| Dialog text length | Only: headline within four lines at 200% text size on Android | Dialog accessibility page |
| App bar title character limit | "Brief enough to easily fit"; two lines at most in flexible app bars | No character count |
| Generic spacing between touch targets ("8dp") | Only component-specific: 8 minimum between chips, group paddings | No general rule on the component pages |
| Animation durations for sheets, dialogs, menus | Pattern names only (enter and exit, container transform) | The only millisecond values on any guidelines page are the 200 ms and 5 s wait thresholds |
| A single side sheet width | 400 maximum (measurement table) and 256 (token) | Both on the specs page; see `references/components-presentation.md` |

Source: https://m3.material.io/components/floating-action-button/specs, https://m3.material.io/components/snackbar/guidelines, https://m3.material.io/components/bottom-sheets/specs, https://m3.material.io/components/buttons/specs, https://m3.material.io/components/text-fields/specs, https://m3.material.io/components/badges/guidelines

## Common mistakes

| Mistake | Fix |
|---|---|
| Everything on the screen wrapped in cards | Use spacing, headlines or dividers; cards for distinct subjects |
| Tappable card that also contains buttons | Either the card is the action or it holds the actions |
| Scrolling region or image pager inside a card on a phone | Expand the card; no swipeable content inside |
| Swipe or drag as the only way to act on a card or list item | Add a menu or More icon with the same actions |
| Divider after every list row | Group with space or gaps; dividers only for uncontained or complex lists |
| Radio buttons in a multi-select list, or checkboxes in a single-select list | Checkboxes or switches for multi-select; radio buttons for single-select |
| Selected row shown only by a color change | Add the control state or another cue |
| Carousel on a scrolling page with no "Show all" route | Add the button below it or an arrow in the header |
| Arrow buttons overlaid on a carousel | Controls go above or below the carousel |
| Spinner on every row or button while a page loads | One indicator for the group |
| Indeterminate circular spinner for a two-second wait in Expressive work | Loading indicator |
| Loading indicator that turns into a percentage bar | Start with an indeterminate progress indicator |
| Indicator flashed for an instant operation | None under 200 ms |
| Pull to refresh with no refresh button anywhere | Provide a refresh action |
| Badge reading "1000+" or moved to the icon's center | Four characters at most; upper trailing corner |
| Citing an unspecified number (FAB margin, snackbar seconds, sheet peek height) as a Material requirement | Say it is not published and name the page that was checked |
