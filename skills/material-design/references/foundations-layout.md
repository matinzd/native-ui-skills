# Layout foundations

Scope: Material breakpoints (formerly window size classes), margins and spacers, the spacing scale, panes, the layout scaffold, canonical layouts, navigation by breakpoint, density, and right-to-left mirroring; API names and form-factor detail live in `references/platforms-large-screens.md` and `references/implementation-navigation.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- Terms renamed in May 2026
- Breakpoints
- Margins, spacers and line length
- Adapting across breakpoints
- Layout scaffold: bars, rails, panes
- Pane rules
- Navigation region by breakpoint
- Canonical layouts
- Spacing system and scale
- Grouping, grids and rulers
- Density
- Bidirectionality and right-to-left
- Form-factor notes
- Common mistakes

## Terms renamed in May 2026

- [API] Material renamed "window size classes" to "breakpoints" and "responsive layout" to "adaptive design" in its May 2026 layout update. The Android libraries and developer.android.com may still say window size class; treat the two words as the same concept.
- [API] The same update introduced the layout scaffold (bars, rails, panes), the spacing system, and guidance for mobile, desktop and spatial experiences. Material states that its layout guidance is implemented on Android and applies to web.
- [MD] For a new layout: use the layout scaffold, start from a canonical layout, and make it scale across breakpoints.
- [API] Glossary: a pane is a layout container for a single destination; a spacer is the space between two panes; a margin is the space between the screen edge and the elements inside it; a gap is the space between elements in a container; a fold is the flexible area or hinge of a foldable; the safety region is the zone reserved for system UI such as the status bar or gesture bar.

Source: https://m3.material.io/foundations/layout/layout-overview/overview

## Breakpoints

A breakpoint is the window width at which the layout needs to change. All values are window widths in dp, not device or screen sizes.

| Breakpoint | Width | Devices Material lists | Recommended panes (panes page) | Other pane counts |
|------------|-------|------------------------|-------------------------------|-------------------|
| Compact | under 600dp | phone in portrait | 1 | none |
| Medium | 600-839dp | tablet in portrait, unfolded foldable in portrait | 1 | 2 |
| Expanded | 840-1199dp | phone in landscape, tablet in landscape, unfolded foldable in landscape, desktop | 2 | 1 |
| Large | 1200-1599dp | desktop | 2 | 1 |
| Extra-large | 1600dp and up | desktop, ultra-wide monitor | 2 | 1, 3 |

- [MD] Make the product adapt automatically to any breakpoint, and give each view a layout for the breakpoints that suit the platform and its users.
- [MD] Design for breakpoints, not devices: available window space changes with multi-window modes, folding and rotation, and one device falls into different breakpoints by orientation.
- [MD] Large and extra-large are described as most useful for laptop and desktop web experiences; some products may not need them.
- [API] On Android, compact, medium and expanded breakpoints also exist for height. Material says a layout rarely needs to react to height because most content scrolls vertically, and gives no dp values for height on its pages; see `references/platforms-large-screens.md`.
- [API] Each breakpoint page lists the events that force a live transition to another breakpoint: folding or unfolding, rotation, entering or leaving split-screen, multi-window mode, and resizing a free-form window. A layout has to handle every one without losing state.
- [Conv] The overview table says extra-large takes "1 to 3 (recommended)" panes and suggests considering three panes there, while the panes page recommends 2 with 1 or 3 as alternatives. Default to two panes and add a third only as described under Pane rules.

Source: https://m3.material.io/foundations/layout/breakpoints/overview , https://m3.material.io/foundations/layout/scaffold/panes

## Margins, spacers and line length

| Breakpoint | Leading and trailing margin | Spacer between panes |
|------------|-----------------------------|----------------------|
| Compact | 16dp | not applicable (single pane) |
| Medium | 24dp | 24dp |
| Expanded | 24dp | 24dp |
| Large, extra-large | 24dp | 24dp |

- [MD] Across all breakpoints, adjust margins and type styles so text stays between 40 and 60 characters per line. The large and extra-large page repeats the warning to watch line length.
- [MD] Margin rulers have some latitude: the standard margin can be narrowed or widened to add or remove negative space, and media such as a photo grid may run full width while components such as search keep wider margins.
- [MD] Medium reachability: on horizontal tablets and unfolded foldables the top 25% of the screen is hard to reach, so limit the interactions placed there, and avoid putting essential controls too close to the bottom edge.

Source: https://m3.material.io/foundations/layout/breakpoints/compact , https://m3.material.io/foundations/layout/breakpoints/medium , https://m3.material.io/foundations/layout/breakpoints/expanded , https://m3.material.io/foundations/layout/breakpoints/large-extra-large , https://m3.material.io/foundations/layout/grids-spacing/grids

## Adapting across breakpoints

Design one breakpoint first, then answer five questions for the next size: what to reveal, how to divide, what to resize, what to reposition, what to swap.

- [MD] Reveal: show what smaller windows hide (an open navigation rail, a second pane). Extra space is not a reason to make the same thing bigger.
- [MD] Divide: a single pane works best at compact and medium, two panes are recommended at expanded and large, consider three at extra-large. Do not use two panes at medium for content with high information density; low-density content with clear actions (the example is settings) is the stated good case.
- [MD] A single immersive pane is appropriate at any size for focused goals such as games, video, calls and creative tools.
- [MD] Resize cards, feeds, lists and panes; reposition content into more columns or toward the leading edge as ergonomics change.
- [MD] Swap only components that are functionally equivalent and only when the swap serves a functional and ergonomic purpose. Named don'ts: a button for a chip, a button for a menu. Be careful swapping list items and cards.

| Function | Compact | Medium | Expanded |
|----------|---------|--------|----------|
| Navigation | navigation bar | collapsed navigation rail | collapsed navigation rail |
| Navigation (expanded form) | modal expanded navigation rail | modal expanded navigation rail | standard expanded navigation rail |
| Communication | basic or full-screen dialog | basic dialog | basic dialog |
| Supplemental selection | bottom sheet | menu | menu |

- [MD] Components adapt by resizing, by showing and hiding content, and by presentation changes (the examples are a FAB becoming an extended FAB and a rail expanding as the window grows).
- [MD] Build for touch, pointer and physical keyboard together, because any device can end up in a desktop environment.

Source: https://m3.material.io/foundations/layout/breakpoints/overview , https://m3.material.io/foundations/layout/layout-overview/adaptive-design

## Layout scaffold: bars, rails, panes

| Region | Position | Holds |
|--------|----------|-------|
| Bars | top and bottom, adjacent to the safety regions; may span one pane or the full window width | app bar (a title and 1-2 essential actions), navigation bar (3-5 primary views at compact or medium) |
| Rails | the perimeter around panes, next to the bars, or floating above panes | compact: toolbars, chat inputs, FABs and other screen-level controls at top or bottom; larger windows: the navigation rail on the leading side, supporting controls or a vertical toolbar on the trailing side |
| Panes | the main region | all content |

- [Req] Material words this as a must: all content belongs in a pane.
- [MD] Keep primary content out of the safety region. Bar and safety rulers exist so that actionable content such as app bars is not covered by system UI; inset handling is in `references/platforms-system.md`.
- [MD] Fill the scaffold from the outside in: bars and rails first, then panes.
- [API] In XR, rail components can become orbiters that float outside the content area.

Source: https://m3.material.io/foundations/layout/scaffold/overview , https://m3.material.io/foundations/layout/scaffold/bars , https://m3.material.io/foundations/layout/scaffold/rails , https://m3.material.io/foundations/layout/layout-overview/parts-of-layout

## Pane rules

- [MD] Every layout has 1 to 3 visible panes. Do not use more than three.
- [MD] Every layout needs at least one flexible pane. A fixed pane keeps its width; a flexible pane grows and shrinks. Panes are also permanent or temporary (dismissible).
- [MD] Single pane: one flexible pane filling the width; allowed at every breakpoint, recommended for compact and medium.
- [MD] Split-pane (two flexible panes): keep the spacer visually centered; described as best for foldables and dynamic layouts. With a navigation bar or no navigation, each pane is 50% of the window width. With a navigation rail, the rail plus the first pane together take 50% so the spacer stays centered.
- [MD] Medium two-pane: each pane takes 50% of the window width; avoid custom widths. A drag handle may expand or collapse a pane to 100%.
- [MD] Fixed-and-flexible (common at expanded and above): the fixed pane defaults to 360dp at expanded and 412dp at large and extra-large. The fixed pane is often temporary, for side sheets or lists with light information density.
- [MD] Third pane: at extra-large a standard side sheet may act as a third pane; the rail may stay, collapse or hide. Material notes that fixed panes there are recommended at 412dp while side sheets have a default maximum width of 400dp.
- [MD] Drag handles resize, collapse and expand panes, and selecting the handle (tap, double tap or long press) should also toggle between layout sizes. Recommended snap widths at expanded and above: 360dp, 412dp, or a split with the spacer centered.
- [MD] Use persistent resizing (the chosen width survives closing the app and breakpoint changes) for most resizable layouts. Use temporary resizing, which returns to the default after the pane or product is reopened, mainly for supporting-pane layouts.
- [MD] Panes display co-planar (side by side), floating (above other panes, like a dialog) or docked (pinned to a window edge, like a bottom sheet). Keep persistent utilities such as tool panels co-planar with primary content; keep temporary tasks floating at every breakpoint.
- [MD] Adaptive strategies: show and hide, levitate, reflow. At medium and expanded a docked pane can become floating or co-planar; on large screens consider turning docked panes into co-planar panes; when width runs out, panes may stack vertically.
- [MD] On large screens floating panes are the default and the scrim behind one is optional. Give any control that moves or resizes a floating pane an accessible equivalent.
- [MD] Focus: focus order should match the visual arrangement of panes. A modal floating pane takes focus on its first element and returns it to the trigger on close (or to the next logical element if it opened automatically). A non-modal floating pane must be reachable in a logical reading order, with focus able to move in and out.

Source: https://m3.material.io/foundations/layout/scaffold/panes , https://m3.material.io/foundations/layout/breakpoints/medium , https://m3.material.io/foundations/layout/breakpoints/expanded , https://m3.material.io/foundations/layout/breakpoints/large-extra-large

## Navigation region by breakpoint

| Breakpoint | Per-breakpoint page | Overview table ("Navigation" column) |
|------------|---------------------|--------------------------------------|
| Compact | navigation bar, or modal expanded navigation rail; keep navigation near the bottom edge where it is easy to reach | navigation bar, modal expanded navigation rail |
| Medium | single pane: navigation rail; two panes: navigation bar (so both panes get the full width) | navigation bar, modal expanded navigation rail |
| Expanded | navigation rail, collapsed or expanded | modal or standard expanded navigation rail |
| Large | navigation rail, collapsed or expanded depending on content | modal or standard expanded navigation rail |
| Extra-large | an expanded rail suits this size best; collapse it when space is needed or deeper in the hierarchy | modal or standard expanded navigation rail |

- [Conv] Material's own pages disagree at medium: the overview table lists the navigation bar, the swap table and the medium page list a (collapsed) navigation rail for single-pane layouts, and the desktop page says to switch from bar to rail at medium and above. Working rule: bar at compact, rail from medium up, bar at medium only for a two-pane layout.
- [MD] The rail may be hidden on secondary destinations as long as the primary destination stays reachable with a back button (stated for medium and expanded).
- [MD] Put sorting, filtering and secondary navigation in tabs or other components inside the pane, not in the navigation region.
- [Conv] The navigation drawer does not appear in any breakpoint table; the expanded navigation rail fills that role. Component status and rules: `references/components-navigation.md`.

Source: https://m3.material.io/foundations/layout/breakpoints/overview , https://m3.material.io/foundations/layout/breakpoints/compact , https://m3.material.io/foundations/layout/breakpoints/medium , https://m3.material.io/foundations/layout/breakpoints/expanded , https://m3.material.io/foundations/layout/breakpoints/large-extra-large , https://m3.material.io/foundations/desktop/components

## Canonical layouts

There are three: list-detail, supporting pane, feed. Material lists Compose and Views implementations of the canonical layouts as available.

| Layout | Use when | Compact | Medium | Expanded and up |
|--------|----------|---------|--------|-----------------|
| List-detail | content is a parent-child pair: conversations and a thread, files and a folder, settings and a category, inbox and a message | 1 pane, list or detail | 1 pane (recommended, for dense content or deep focus) or 2 panes (to browse and switch quickly) | 2 panes |
| Supporting pane | secondary content is meaningful only in relation to the primary content: productivity, document editing with comments, media browsing | supporting pane below the focus pane, flexible; a bottom sheet is an option | below the focus pane, flexible | leading or trailing side, fixed 360dp |
| Feed | browsing and discovery of cards or list items in a grid: news, photos, social | items stack in one column and fill the pane width | multiple columns, mixed item widths | the number of columns should usually increase |

- [MD] Parent-child content takes list-detail, not supporting pane. The supporting-pane primary area typically takes about two-thirds of the window.
- [MD] List-detail: show a back button in the detail view only in single-pane layouts; show a selected state in the list only in two-pane layouts.
- [MD] List-detail with nothing selected: single pane shows the list; two panes show placeholder content in the detail pane.
- [MD] List-detail with an item selected: one to two panes shows both with the item's details; two to one should typically show the detail pane with an app bar. Products that select without deep navigation (multi-select) may show the list with the item selected. Return to whichever view the single-pane layout showed before.
- [MD] Keep state when moving between detail views in most cases (read and unread included); detail views keep their scroll position.
- [MD] List-detail at medium with two panes: use a bottom navigation bar or a modal navigation rail to keep horizontal space.
- [MD] Feed items reflow when available space changes (rotation, unfolding, multi-window); item order follows position.
- [MD] For custom layouts, build on a canonical layout or layer panes with the levitate strategy for focused tasks such as reviewing a basket or creating an event.

Source: https://m3.material.io/foundations/layout/canonical-examples/overview , https://m3.material.io/foundations/layout/canonical-examples/list-detail , https://m3.material.io/foundations/layout/canonical-examples/supporting-pane , https://m3.material.io/foundations/layout/canonical-examples/feed

## Spacing system and scale

(Material 3 Expressive, added May 2026.) A linear scale built on an 8dp base unit: the token `md.sys.measurement.space100` is 8dp and each name is a multiplier (space225 would be 18dp).

| Token | dp | Token | dp | Token | dp |
|-------|----|-------|----|-------|----|
| space0 | 0 | space150 | 12 | space450 | 36 |
| space25 | 2 | space175 | 14 | space500 | 40 |
| space50 | 4 | space200 | 16 | space600 | 48 |
| space75 | 6 | space250 | 20 | space700 | 56 |
| space100 | 8 | space300 | 24 | space800 | 64 |
| space125 | 10 | space400 | 32 | space900 | 72 |

- [API] The spacing system tokens are used only on Jetpack Compose; Material lists Views (MDC-Android) and web as unavailable, and says work to connect all components to the tokens is ongoing.
- [MD] Three categories: padding (inside an element), gap (between elements), margin (outside an element). Positions are vertical, horizontal, top, bottom, leading, trailing; leading and trailing swap in right-to-left.
- [MD] Use padding and gaps before margins: define them on the parent container, and avoid defining margins on child elements. Margins are for layouts or for spacing beyond the parent's padding.
- [MD] Apply system spacing tokens to custom components and layouts in place of hard-coded values; extend the scale with the multiplier pattern when a value is missing.
- [MD] When text scales up to 200%, keep the same spacing by default.
- [MD] Adapt spacing by context (mobile versus desktop, density setting) by remapping a component's spacing to different system tokens; density adapts vertical padding.

Source: https://m3.material.io/styles/spacing/overview , https://m3.material.io/styles/spacing/applying-spacing , https://m3.material.io/styles/spacing/tokens

## Grouping, grids and rulers

- [MD] Explicit grouping uses outlines, dividers and shadows; implicit grouping uses proximity and open space. Panes on most devices can blend with the background (implicit); XR spatial panels need explicit containment.
- [MD] Keep consistent spacing between related elements, give similar elements the same spacing and size, align leading elements such as thumbnails, avatars and icons, and place buttons close to the content they affect.
- [MD] The grid adapts across breakpoints: column count, width and spacing change with size. Material publishes no fixed column counts on these pages.
- [MD] Rulers are recommended global alignment lines: bar and safety rulers, a title ruler aligned with the app bar title, content rulers for major and supplementary content, and margin rulers. Material lists a Compose implementation of rulers as available.

Source: https://m3.material.io/foundations/layout/grids-spacing/spacing , https://m3.material.io/foundations/layout/grids-spacing/grids , https://m3.material.io/foundations/layout/layout-overview/parts-of-layout

## Density

- [MD] Default target size is at least 48x48 (the page writes both "48x48 CSS pixels" and "48x48dp"). Do not apply component scaling by default if it would bring a target below that, and do not scale layouts below it by default.
- [MD] Dense layouts are opt-in: people choose them in settings. Density should not change automatically across breakpoints or orientation.
- [Req] Stated as a must: the settings controls that change density use default target sizes, so the choice can always be reverted.
- [MD] The component density scale starts at 0 (default) and goes to -1, -2, -3; each step typically removes 4dp from the top and bottom padding or the overall height. Keep the content centered and do not change text size as the container shrinks.
- [MD] Do not increase density in focused tasks such as choosing from a menu, or in components that alert people to changes such as snackbars and dialogs.
- [MD] Information density can also be raised by layout decisions alone (margins, spacers, padding) without scaling components; consider it where people scan or compare a lot of data, such as tables, lists and long forms.
- [API] 1dp equals one physical pixel on a 160-density screen; dp = (width in pixels x 160) / screen density.

Source: https://m3.material.io/foundations/layout/grids-spacing/density

## Bidirectionality and right-to-left

- [MD] Support left-to-right and right-to-left by mirroring. Material components are named with leading and trailing so they mirror, but some cases need extra configuration.
- [MD] Mirror: overall layout and reading order, all three canonical layouts, app bars (and flip their arrows), toolbars (tool order), the navigation rail (leading edge, so the right side in RTL), badges, text-field and chip leading and trailing icons, swipe actions and the predictive back gesture.
- [MD] Mirror directional icons such as back, forward and send. Help icons mirror in some RTL languages (Urdu and Persian are named).
- [MD] Do not mirror: media playback controls (always LTR), clocks, circular progress, and clock, circular-refresh or clockwise-arrow icons. In 12-hour clocks, place AM/PM on the left.
- [MD] Linear progress fills from the right in most RTL languages; in Hebrew it stays LTR, as do timelines and media controls.
- [MD] Graphs and charts keep LTR direction for Persian and Urdu.
- [MD] Text needs both RTL alignment and RTL directionality; applying LTR directionality to RTL content scrambles word order. Do not reverse an email address: the domain stays to the right of the username.

Source: https://m3.material.io/foundations/layout/bidirectionality-rtl

## Form-factor notes

| Form factor | Layout notes from the Material pages | More |
|-------------|--------------------------------------|------|
| Foldable, tablet | unfolding, rotation and split-screen change the breakpoint; split-pane suits foldables; medium reachability zones apply | `references/platforms-large-screens.md` |
| Desktop window | apps typically open at medium or large and can grow to extra-large; use multi-column or multi-pane layouts; if a single pane is kept, cap and center the content width; keep default component widths (no full-width buttons or text fields); a bottom sheet, if used, must be detached from the window's bottom edge; prefer context menus, side sheets without a scrim, and dialogs | `references/platforms-large-screens.md` |
| Watch | design for the smallest round screen first (192dp), add content above 225dp, define margins and padding as percentages, test all font sizes | `references/platforms-wear.md` |
| XR | spatial panels launch at 1024x720dp with 32dp corners, maximum 2560x1800dp; rails become orbiters | `references/platforms-auto-xr.md` |

Source: https://m3.material.io/foundations/desktop/layout , https://m3.material.io/foundations/desktop/components , https://m3.material.io/foundations/watches/layout , https://m3.material.io/foundations/xr/design/layout

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Branching on device type or orientation | Branch on the window width breakpoint; handle live transitions |
| Calling the thresholds 600 and 840 only | There are five breakpoints: 600, 840, 1200 and 1600dp are the boundaries |
| Stretching a phone layout across a wide window | Add panes or columns, or cap and center a single pane; keep lines at 40-60 characters |
| Two dense panes at medium | One pane at medium unless content is low density |
| Four panes, or only fixed panes | Three at most, at least one flexible |
| Back button in the detail pane of a two-pane list-detail | Back button in single pane only; selected state in two-pane only |
| Supporting pane for parent-child content | Use list-detail |
| Navigation bar kept on a wide window | Navigation rail from medium up (bar at medium only with two panes) |
| Swapping a button for a chip or a menu at another size | Swap only functionally equivalent components |
| Dense components by default, or density that changes with rotation | Density is opt-in and stable; keep 48dp targets |
| Using left and right in RTL, or mirroring media controls | Use leading and trailing; keep media controls and clocks LTR |
