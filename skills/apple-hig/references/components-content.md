# Content components: lists, collections, scroll views, media and system surfaces

Scope: lists and tables, collections, outline and column views, scroll views, boxes, image and web views, charts, empty states, plus short pointers for status bars, widgets, Live Activities and notifications.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Which content container
- Lists and tables
- Collections
- Outline views and column views (macOS)
- Scroll views
- Scroll edge effects
- Boxes, grouping and "cards"
- Image views and web views
- Charts
- Empty states and status
- Status bars
- Widgets
- Live Activities
- Notifications
- Common mistakes

## Which content container

| Content | Use | Platforms |
|---|---|---|
| Mostly text rows, options, or a navigable hierarchy of rows | List or table | All |
| Many images, or items that vary widely in size | Collection (row or grid) | All except watchOS |
| Attributes in sortable columns | Multicolumn table | All; sorting and column-resizing rules are stated for macOS |
| Hierarchical data with expandable parents, optional attribute columns | Outline view | macOS only |
| Deep hierarchy browsed back and forth, no sorting needed | Column view (browser) | macOS only; on iPadOS and visionOS consider a split view |
| A very large set of choices | List or table rather than a picker | All |
| Ordered peer pages | Paging scroll view plus page control | See `references/components-controls.md` |
| A small group of related controls or information | Box | iOS, iPadOS, macOS, visionOS |
| Focusable media items on Apple TV | Lockup (card, caption button, monogram, poster) | tvOS only |

Source: https://developer.apple.com/design/human-interface-guidelines/lists-and-tables, https://developer.apple.com/design/human-interface-guidelines/collections, https://developer.apple.com/design/human-interface-guidelines/column-views

## Lists and tables

- [HIG] Prefer lists and tables for text; use a collection for image-heavy or irregularly sized items.
- [HIG] Let people edit when it makes sense; reordering is valued even if adding and removing are not possible. On iOS and iPadOS people enter an edit mode before selecting items.
- [HIG] Selection feedback depends on purpose: a navigation list keeps the selected row highlighted to show the path; an options list highlights briefly and then shows a mark such as a checkmark.
- [HIG] Keep row text succinct. If items are long, list titles only and show the full content in a detail view.
- [HIG] When a table can get narrow, keep text recognizable; a middle ellipsis can preserve both ends of a string.
- [HIG] Multicolumn tables need descriptive column headings: nouns or short noun phrases, title-style capitalization, no ending punctuation. A single-column table without a heading needs a label or header for context.
- [HIG] Pick a list style that fits the data and platform (for example grouped on iOS and iPadOS, elliptical on watchOS, bordered with alternating rows on macOS) and a row style that fits the information.

| Platform | Rules |
|---|---|
| iOS, iPadOS, visionOS | [HIG] An info (detail disclosure) button only reveals more information about the row; it is not navigation. Use a disclosure indicator for drilling into a row's subviews. Do not add a section index to a table whose rows have trailing controls such as disclosure indicators. |
| macOS | [HIG] Let people click a column heading to sort, and click again to reverse. Let people resize columns. Consider alternating row colors in multicolumn tables. Use an outline view for hierarchical data. |
| tvOS | [HIG] A focused row grows slightly and its corners may round; check adjacent images and do not add your own corner masks. |
| watchOS | [HIG] Limit the number of rows when possible; show the most relevant items and a way to see more. Vertical page-based navigation between detail views works only if the detail views do not scroll. |

Source: https://developer.apple.com/design/human-interface-guidelines/lists-and-tables

## Collections

- [HIG] Best for image-based content. Use the standard row or grid layout; avoid custom layouts that draw attention to themselves.
- [HIG] For text, consider a table instead.
- [HIG] Make items easy to choose: pad around images so focus and hover effects stay visible and content does not overlap.
- [HIG] Default interactions are tap to select, touch and hold to edit, swipe to scroll; add custom gestures only if required.
- [HIG] Consider animations for insert, delete and reorder.
- [HIG] iOS, iPadOS: be careful with dynamic layout changes; avoid changing layout while people are viewing or interacting unless they asked for it.
- [API] Not supported in watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/collections

## Outline views and column views (macOS)

- [HIG] Outline view: for hierarchical data; use a table when data is flat. Show hierarchy in the first column only; other columns hold attributes.
- [HIG] Always provide column headings in a multicolumn outline view (nouns, title-style capitalization, no trailing colon).
- [HIG] Let people sort by clicking headings and resize columns; consider alternating row colors.
- [HIG] Make expanding and collapsing easy (Option-click a disclosure triangle expands all subfolders in Finder) and remember people's expansion state.
- [HIG] In editable cells, a single click edits; a double click may do something else (open).
- [HIG] Prefer a centered ellipsis to clipping. Consider a toolbar search field for long outlines.
- [HIG] Column view: root level in the first column; show information about the selected item when it has no children; let people resize columns.
- [API] Neither is supported in iOS, iPadOS, tvOS, visionOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/outline-views, https://developer.apple.com/design/human-interface-guidelines/column-views

## Scroll views

- [HIG] Support the default scrolling gestures and keyboard shortcuts; custom scrolling keeps the elastic indicator behaviour people expect.
- [HIG] Make scrollability apparent, for example by showing partial content at the edge.
- [HIG] Do not nest a scroll view inside another with the same orientation. A horizontal scroller inside a vertical one (or the reverse) is fine.
- [HIG] Consider page-by-page scrolling where it suits the content; a small overlap unit (a line of text, a row of glyphs) preserves context.
- [HIG] Scroll automatically only to help people keep their place (a found search result, an offscreen insertion point, a selection dragged past the edge), and only as far as necessary.
- [HIG] If zooming is supported, set sensible minimum and maximum scale values.
- [HIG] iOS, iPadOS: in page-by-page mode consider a page control, and then hide the scroll indicator on that axis.
- [HIG] macOS: small or mini scroll bars are acceptable in panels if all controls in the panel use the same size.
- [API] tvOS has no scroll indicators; the system scrolls to keep the focused item visible.
- [HIG] visionOS: the scroll indicator is small and slightly thicker than on iOS; widen tight margins so it does not overlap content. Add Look to Scroll to reading and browsing views (it is off by default), keep it consistent across similar views, give such views the full window width or height or clear boundaries, and remove scroll-position-driven effects such as parallax first. Do not use it for control-dense secondary content.
- [HIG] watchOS: prefer vertical scrolling (Digital Crown). Use vertical tab views for page-by-page scrolling; aim for one screen height per page and put variable-height pages after fixed-height ones.

Source: https://developer.apple.com/design/human-interface-guidelines/scroll-views

## Scroll edge effects

(OS 26+, Liquid Glass; iOS, iPadOS, macOS)

- [HIG] A scroll edge effect separates floating elements such as toolbars from the scrolling content behind them. Standard bars get it; add it manually for custom bars that need the clarity.
- [HIG] Prefer the automatic style. If you choose the soft style, test legibility in many contexts. (Styles named on the page: automatic, hard, soft; API `ScrollEdgeEffectStyle`.)
- [HIG] Use it only where a scroll view sits behind floating interface elements. It is not decoration and does not dim like an overlay.
- [HIG] One scroll edge effect per view. In split views each pane can have its own; keep their heights consistent.
- [HIG] Do not put a solid or semi-opaque background under controls instead (Layout page; see `references/foundations-layout.md`).

Source: https://developer.apple.com/design/human-interface-guidelines/scroll-views, https://developer.apple.com/design/human-interface-guidelines/layout

## Boxes, grouping and "cards"

- [HIG] A box groups related information and controls with a visible border or background and an optional title.
- [HIG] Keep a box small relative to its containing view; a box approaching window size stops communicating grouping.
- [HIG] Do not nest boxes for subgroups; use padding and alignment inside the box.
- [HIG] Title only if it helps: a brief phrase in sentence-style capitalization, no ending punctuation (settings panes append a colon).
- [API] iOS and iPadOS boxes use the secondary and tertiary background colors by default; macOS shows the title above the box. Not supported in tvOS or watchOS.
- [Conv] The HIG has no general "card" component page. The only card it defines is a tvOS lockup type. Treat card-style containers in other apps as custom content-layer views and apply the Layout and Materials guidance; (OS 26+) do not use Liquid Glass for them, because the Materials page keeps Liquid Glass out of the content layer.
- [HIG] tvOS lockups: leave room for the focused (enlarged) size and keep sizes consistent within a row.

Source: https://developer.apple.com/design/human-interface-guidelines/boxes, https://developer.apple.com/design/human-interface-guidelines/lockups, https://developer.apple.com/design/human-interface-guidelines/materials

## Image views and web views

- [HIG] Image view: for displaying an image. If the image must act as a button, configure a system button with the image instead of adding tap behaviour to an image view.
- [HIG] For icons prefer SF Symbols or template interface icons over image views; they pick up accent colors.
- [HIG] Text over images needs strong contrast; consider a shadow or a background layer behind the text.
- [HIG] Animated sequences: use one consistent image size.
- [HIG] macOS: editable image is an image well; clickable image is an image button.
- [HIG] Web view: add back and forward controls if people will visit multiple pages (not provided by default).
- [HIG] Do not build a web browser from a web view; brief in-context web content is fine. [API] Web views are not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/image-views, https://developer.apple.com/design/human-interface-guidelines/web-views

## Charts

- [HIG] Use a chart to highlight important information about a dataset; keep it simple and let people ask for detail.
- [HIG] Prefer common chart types (bar, line); teach people how to read a novel one.
- [HIG] Add descriptive text: a title or summary that states the main message before people study the marks.
- [HIG] Axes: choose a fixed or dynamic range by meaning; a zero lower bound often works well for bar charts; use familiar tick sequences; avoid too many or too few grid lines.
- [HIG] Make the data the most prominent element; in compact width maximize the plot area and keep axis labels short.
- [HIG] Interaction may reveal details but must not be required to see critical information. If marks are small, extend the hit target to the whole plot area and let people scrub.
- [HIG] Never rely on color alone to separate data; separate adjacent color areas visually.
- [HIG] Every chart must be accessible: accessibility labels that serve the chart's purpose, Audio Graphs for VoiceOver, keyboard and Switch Control navigation; hide visible axis and tick labels from assistive technologies.
- [HIG] watchOS: avoid complex chart interactions.

Source: https://developer.apple.com/design/human-interface-guidelines/charts, https://developer.apple.com/design/human-interface-guidelines/charting-data

## Empty states and status

The HIG has no component page for empty states; its guidance is spread across these pages.

- [HIG] Give clear next steps on any blank screen: say what people can do and offer a button or link to do it. Empty states are temporary, so do not put crucial information there (Writing page).
- [HIG] An empty tab or section stays reachable and explains why content is unavailable (Tab bars page).
- [HIG] While content loads, show something immediately, such as placeholder text, graphics or animation, and replace it as content arrives (Loading page).
- [HIG] At launch with no network, show cached or placeholder data and a nonintrusive label, not an alert (Alerts page).
- [HIG] Put status near the items it describes so people see it without leaving context; reserve alerts for critical, ideally actionable information (Feedback page).
- [HIG] When a command cannot be carried out, show that and help people understand why (Feedback page).

Source: https://developer.apple.com/design/human-interface-guidelines/writing, https://developer.apple.com/design/human-interface-guidelines/loading, https://developer.apple.com/design/human-interface-guidelines/feedback, https://developer.apple.com/design/human-interface-guidelines/alerts

## Status bars

- [HIG] (iOS, iPadOS only) Keep the status bar readable: do not let interactive-looking content show behind it; prefer a scroll edge effect to blur what is underneath.
- [HIG] Hiding it temporarily for full-screen media is fine; do not hide it permanently, and let a simple gesture such as a tap bring it back.

Source: https://developer.apple.com/design/human-interface-guidelines/status-bars

## Widgets

Pointer only; read the page before designing a widget (sizes, rendering modes and per-platform tables live there).

- [HIG] A widget shows a small amount of timely, glanceable information tied to the app's main purpose; keep complexity in the app.
- [HIG] A widget interaction opens the app at the matching location (deep link), not the app's start screen.
- [HIG] Do not rely on specific colors for meaning; widgets can render monochrome, tinted or inverted. Support light and dark.
- [HIG] In general use text of 11 pt or larger, system fonts, text styles and SF Symbols; do not rasterize text.
- [HIG] Design placeholder content (static elements plus semi-opaque shapes) for the loading state, and a realistic gallery preview.
- [HIG] Do not place a widget look-alike inside the app.

Source: https://developer.apple.com/design/human-interface-guidelines/widgets

## Live Activities

Pointer only; presentations (compact, minimal, expanded, Lock Screen) and sizes are on the page.

- [HIG] For tasks and events with a defined beginning and end; they suit activities that do not exceed eight hours.
- [HIG] No ads or promotions. Avoid sensitive information; show a neutral summary and reveal details in the app.
- [HIG] Update only when content changes; alert only for essential updates, and do not send a push notification for the same update.
- [HIG] End the Live Activity immediately when the task ends. After ending it can stay on the Lock Screen for up to four hours; consider a custom dismissal time (the page suggests 15 to 30 minutes in most cases).
- [HIG] Tapping opens the app at the related content. Let people turn Live Activities off in the app.
- [HIG] Do not add in-app elements that point at or decorate the Dynamic Island.

Source: https://developer.apple.com/design/human-interface-guidelines/live-activities

## Notifications

Pointer only; permission, interruption levels and marketing rules are in `references/patterns-flows.md`.

- [HIG] Notifications carry timely, high-value information, concisely. Do not repeat a notification for the same thing.
- [HIG] No sensitive, personal or confidential content. Do not include the app name or icon in the content; the system shows the icon.
- [HIG] Show errors with an alert in the app, not with a notification.
- [HIG] When the app is in the foreground, surface the incoming information unobtrusively (update a badge, insert the new item).
- [HIG] Actions: useful without opening the app; none that merely opens the app; prefer nondestructive ones. watchOS long looks take up to four custom actions.
- [HIG] Badges count unread notifications only, must stay current, and must not be the sole carrier of essential information (people can turn badging off). Do not imitate badges with custom UI.

Source: https://developer.apple.com/design/human-interface-guidelines/notifications, https://developer.apple.com/design/human-interface-guidelines/managing-notifications

## Common mistakes

| Mistake | Fix |
|---|---|
| Grid of text-only cells | Use a list or table |
| Info button used to push a detail screen | Disclosure indicator for navigation; info button only for more information |
| Section index on a list with trailing chevrons or controls | Drop the index or move the trailing controls |
| Selection that flashes and disappears in a split view's list | Keep the selected row highlighted in navigation lists |
| Vertical scroll view nested in a vertical scroll view | One scroll view per axis; nest only across axes |
| Opaque header background painted behind a floating bar (OS 26+) | Use the automatic scroll edge effect, one per view |
| Scroll edge effect added as decoration where nothing floats over content | Remove it |
| Liquid Glass applied to content cards | Standard materials or plain backgrounds in the content layer |
| Boxes nested inside boxes | Padding and alignment within one box |
| Tappable image view | A button configured with the image |
| Full in-app browser built on a web view | Brief web content only; hand off real browsing |
| Chart whose key number appears only on touch, or encoded only by color | Show the main message in text; add non-color differentiation |
| Blank screen with no explanation, or an alert on empty or offline launch | Explain and offer the next action inline; show cached or placeholder content |
| Badge used for arbitrary numbers; notification used for an error | Badge only for unread notifications; alert for errors |
| Live Activity left running after the event, or used for promotion | End it at once; never promotional |
