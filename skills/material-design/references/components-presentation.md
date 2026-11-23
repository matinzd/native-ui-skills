# Presentation components: dialogs, sheets, snackbars, menus, tooltips

Scope: choosing between and configuring dialogs (basic, full-screen), bottom sheets, side sheets, snackbars, menus and tooltips, with action counts, dismissal and wording rules. API names are in `references/implementation-components.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How to read this file
- Which presentation
- Action counts, order and wording
- Dismissal
- Dialogs (basic)
- Full-screen dialogs
- Bottom sheets
- Side sheets
- Snackbars
- Menus
- Tooltips
- Date and time pickers as dialogs
- Common mistakes

## How to read this file

- [Conv] `[MD]` covers Material's "should", "avoid" and "Don't" captions: recommendations. `[Req]` is used only where the page itself says "must" or "Material requires". `[API]` marks availability and fixed behaviour stated on the pages.
- [Conv] Numbers are in dp, from the specs measurement tables or token tables unless a bullet says "prose". Where a token and the prose disagree, both are given.
- [API] None of the six components in this file has an Expressive section except menus (vertical menus, November 2025).

Source: https://m3.material.io/components

## Which presentation

| Need | Use | Window size note | Not |
|---|---|---|---|
| Brief, low-priority feedback about a process; nothing has to be done; optional single action such as Undo | Snackbar | Up to two lines in compact; aim for one line from medium up | Dialog |
| Critical information, or a decision or acknowledgement that must block the app | Basic dialog, at most two actions | All sizes; 280 to 560 wide | Snackbar, tooltip |
| A task with keyboard input, changes that are not saved instantly, or content that opens further dialogs | Full-screen dialog | Compact only; a basic dialog from medium up | Basic dialog on a phone |
| A temporary, short set of actions or choices opened from a control (overflow, select, text field dropdown, context menu) | Menu | Works best from medium up; on small screens consider a bottom sheet | Dialog; a toolbar when actions must stay visible |
| A long list of actions, or items needing icons and longer descriptions, on a phone | Modal bottom sheet | "Mobile apps only"; initial height at most 50% of the screen | Menu, simple dialog |
| Supplementary content used together with the main region (audio player, place details over a map) | Standard bottom sheet | Compact and medium; max width 640 | Modal sheet |
| Supplementary content or controls that stay visible beside the main content (filters, details) | Standard side sheet | Mostly medium to expanded | Bottom sheet on desktop-size windows |
| The same supplementary content where space is short | Modal side sheet | Preferred in compact | Standard side sheet |
| A label for an icon-only control | Plain tooltip | Hover, or touch and hold | Tooltip on a control that already has a text label |
| A longer explanation or a feature introduction, with optional actions | Rich tooltip | Up to two text buttons | Anything critical |
| Actions that must stay on screen | Toolbar (`references/components-navigation.md`) | Not together with a navigation bar | Menu |
| Non-critical information in general | Inline, in the flow of content | n/a | Dialog |

- [MD] Dialogs interrupt on purpose; use them sparingly. The dialog page names a dropdown menu as a less disruptive way to offer options, and a snackbar for low or medium priority messages.
- [MD] The dialog and snackbar pages share one table: snackbar = low priority, action optional, disappears on its own; dialog = high priority, action required, blocks content.
- [MD] On larger expanded windows a bottom sheet can be swapped for a side sheet showing similar content; a modal side sheet can become a standard side sheet as the window grows; a full-screen dialog becomes a basic dialog at larger breakpoints.
- [MD] Only a full-screen dialog may have another dialog appear over it. One snackbar at a time; one tooltip at a time.

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/snackbar/guidelines, https://m3.material.io/components/bottom-sheets/guidelines, https://m3.material.io/components/side-sheets/guidelines, https://m3.material.io/components/menus/guidelines

## Action counts, order and wording

| Component | Actions | Order and style | Wording |
|---|---|---|---|
| Basic dialog | Maximum two. One only if it is an acknowledgement; two = one confirming + one dismissing. A third action such as "Learn more" is not recommended | Text buttons at the trailing edge; confirming action closest to the edge, dismissive action before it. Stacked (for long labels): confirming on top | Headline is a brief, clear statement or question; no apology, alarm ("Warning!") or ambiguity ("Are you sure?") |
| Full-screen dialog | Close icon (the only navigation) plus one confirming action in the header | Both live in the header region (56 high); the confirming action is a text button | Specific verb: Save, Send, Create. Avoid Done, OK, Close |
| Snackbar | A single action; a separate dismiss action is optional and usually unnecessary | Text button only, colored differently from the message; never filled or elevated | Short status message; "Undo" to amend |
| Rich tooltip | Up to two text buttons | Side by side; avoid stacking | Brief, tied to the supporting text |
| Side sheet | Optional action buttons (Save, Edit, Download) in a bottom action area | Left-aligned per the measurement table | n/a |
| Menu | Items only; no buttons, switches or other direct controls nested in an item | Group with a divider or gap | Item label equals its accessibility label |

- [Req] The dialog page uses "must" for the two count rules above (a single action must be an acknowledgement; of two, one must confirm and one dismiss). The limit of two itself is a "should".
- [MD] Disable the confirming action of a basic dialog until a choice is made; dismissive actions are never disabled. In a full-screen dialog do not disable the confirming button.
- [MD] Do not offer Cancel when no action is being proposed; a lone acknowledgement is enough.
- [MD] Instead of a third action, expand more information inline or give it before the dialog opens.
- [MD] In right-to-left languages button alignment mirrors, so the confirming action sits at the left edge.

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/snackbar/guidelines, https://m3.material.io/components/tooltips/guidelines

## Dismissal

| Component | How it goes away |
|---|---|
| Basic dialog | Stays until confirmed, dismissed or the required action is taken; Escape closes it |
| Full-screen dialog | Close icon or a dismissive action; with unsaved changes a basic dialog asks to discard; the confirming action completes, it does not dismiss |
| Modal bottom sheet | Choosing an item or action, tapping the scrim, swiping down, or a close affordance in its app bar; predictive back is supported |
| Standard bottom sheet | Coexists with content; at full height it shows a collapse icon in an app bar |
| Modal side sheet | Must be dismissed to reach the content behind; close affordance; predictive back is supported |
| Snackbar without action | May auto-dismiss after 4 to 10 seconds "depending on platform" |
| Snackbar with action | Stays until the action is taken or it is dismissed; Escape dismisses it when focused |
| Menu | Selecting an item, Escape, tapping outside, or system Back; a multi-select menu stays open until dismissed |
| Plain or transient rich tooltip | 1.5 seconds after leaving the target region; opening another tooltip closes it at once |
| Persistent rich tooltip | Stays until the person interacts with another element |

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/bottom-sheets/guidelines, https://m3.material.io/components/snackbar/guidelines, https://m3.material.io/components/menus/accessibility, https://m3.material.io/components/tooltips/guidelines

## Dialogs (basic)

- [API] The overview lists Jetpack Compose and Android Views as available. Two variants: basic and full-screen.
- [MD] A dialog is dedicated to one task; common uses are alerts, quick selection and confirmation of high-risk actions.
- [MD] The headline is optional; when present keep it succinct. It may wrap to a second line.
- [MD] Supporting text is part of the anatomy; an optional icon centers the content, otherwise it is start-aligned.
- [MD] Avoid scrolling. If content must scroll, the title stays pinned at the top and the buttons at the bottom; the dialog never scrolls with the page behind it.
- [MD] A dialog should not be obscured or shown partly off screen.
- [MD] Position: centered by default; from medium up it may be custom-positioned, keeping a 56 margin from the screen edges.
- [MD] It appears with an enter and exit transition over a scrim; no duration is given on the page.
- [MD] Accessibility: focus moves to the first interactive element and cycles inside the dialog; the accessibility label is normally the headline. On Android the headline should fit within four lines at 200% text size, with a one-tap way to reach the full text if it truncates.

| Measurement table | Value |
|---|---|
| Container width | min 280, max 560 |
| Container shape | 28 corner radius |
| Padding, all sides | 24 |
| Padding between buttons | 8 |
| Title to body; icon to title | 16; 16 |
| Body to actions | 24 |
| Icon size | 24 |

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/dialogs/specs, https://m3.material.io/components/dialogs/accessibility

## Full-screen dialogs

- [MD] For compact windows only; at medium and expanded use a basic dialog.
- [MD] Use when any of these holds: the content needs keyboard input (form fields); changes are not saved instantly; components inside open further dialogs. Example: creating a calendar event.
- [MD] The close "X" icon button is the only navigation in the header.
- [MD] Closing with unsaved changes shows a basic dialog to confirm discarding. Do not use the confirming action as the way to dismiss.
- [MD] Do not open a basic dialog when the confirming action is selected, unless the action failed.
- [MD] Errors about fields appear inline where they occur, all at once; general errors (network) appear in a basic dialog when the confirming action fails.
- [MD] Put long or variable-length headlines in the content area, not in the header.
- [MD] A FAB can open a full-screen dialog with a container transform.
- [MD] Measurement table: header height 56; bottom action bar height 56; close icon 24; corner radius 0; top, left and right padding 24; container width capped at 560.

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/dialogs/specs

## Bottom sheets

- [API] The overview lists Jetpack Compose and Android Views as available. Two variants: standard and modal; they share specs except for the modal scrim.
- [MD] Content is supplementary, never the app's main content. Use in compact and medium windows.
- [MD] Standard: coexists with the main region so both can be used, especially when the main region is scrolled or panned.
- [MD] Modal: blocks the app until acted on or dismissed; an alternative to inline menus or simple dialogs on mobile. It opens from a user action (a button, an overflow icon).
- [MD] The initial position of a modal sheet is capped at 50% of the screen height; taller content can then be pulled to full screen and scrolled inside the sheet.
- [MD] Show a close affordance in a full-screen modal bottom sheet.
- [MD] The container is the only required element; the drag handle is optional.
- [MD] Selecting the drag handle cycles through the preset heights or closes the sheet; selecting the scrim always closes it. Sheets should be able to change height and close without dragging.
- [Req] If a sheet has several preset heights and cannot use a drag handle, "Material requires" a single-pointer alternative for changing height (a button).
- [MD] Sheets should scroll internally when content exceeds the visible height.
- [MD] From medium up the sheet has a default maximum width, which may be overridden; for complex flows consider a non-transient surface.
- [MD] Accessibility: label only the drag handle (role button); it is focusable, and Space or Enter toggles heights. The top 48 of the sheet is the interactive resize area when a handle is present.
- [Conv] No peek height, detent fraction or animation duration is published; see `references/components-content.md`.

| Measurement | Value |
|---|---|
| Width | Full window width up to 640 |
| Above 640 window width: top margin; side margins | 56; 56 |
| Top margin (measurement table) | 72 |
| Drag handle (token) | 32 x 4 |
| Drag handle top and bottom padding | 22 |
| Top corner radius (overview, "Differences from M2") | 28 |

Source: https://m3.material.io/components/bottom-sheets/guidelines, https://m3.material.io/components/bottom-sheets/specs, https://m3.material.io/components/bottom-sheets/accessibility

## Side sheets

- [API] The overview lists Android Views as available and Jetpack Compose as unavailable.
- [MD] Standard: mostly medium to expanded windows; stays visible while people use the primary content; the body shrinks to make room when it opens. Typical content: filters, details, supplementary features.
- [MD] Modal: preferred in compact windows; same content, over a scrim.
- [MD] Place on the trailing edge (usually the right, to stay clear of navigation on the left); the left edge with all elements reversed in right-to-left languages. It may be inset by 16; do not inset it much further.
- [MD] Fixed width, normally full height. Vertical internal scrolling only; never horizontal.
- [Req] The accessibility page says "Material requires" a close affordance, such as a close icon button, in every side sheet. (The guidelines anatomy labels the close button optional and "highly recommended".)
- [MD] An optional back icon button navigates within the sheet. Dividers separate action buttons from content.
- [API] Accessibility role: Dialog.

| Measurement | Value |
|---|---|
| Max width (measurement table) | 400 |
| "Docked container width" (token table) | 256 |
| Start and end padding | 24 |
| Bottom action area height | 72 |
| Margins when detached | 16 |
| Modal corner radius (overview, "Differences from M2") | 16 |

- [Conv] The 400 maximum and the 256 token are both on the specs page and the page does not reconcile them. Report both; do not present either as "the" side sheet width.

Source: https://m3.material.io/components/side-sheets/guidelines, https://m3.material.io/components/side-sheets/specs, https://m3.material.io/components/side-sheets/accessibility

## Snackbars

- [API] The overview lists Jetpack Compose and Android Views as available.
- [MD] A snackbar reports something the app has done or will do, without interrupting; people keep using the page.
- [MD] Only one at a time; consecutive snackbars appear one after another, never stacked or side by side. A snackbar with newer information may replace an outdated one immediately.
- [MD] A snackbar must not be the only way to reach a core function.
- [MD] Text: one line when possible; up to two lines in compact windows; a long action may drop to a third line. Avoid icons, styled text and inline links (use the action, or another component).
- [MD] Container: opaque (slight transparency only if the text stays legible); do not change its shape much.
- [MD] Placement: bottom of the UI, in front of the main content, above a FAB (never in front of or behind it), and not in front of navigation or frequently used targets. It can be nudged up to clear FABs or docked toolbars.
- [MD] It may span the full width only when there are no persistent navigation components.
- [MD] From medium up: grow horizontally for longer text (ideal line length 40 to 60 characters), aim for one line, and place it left-aligned or centered at a consistent spot, never flush to one edge.
- [MD] Do not animate other components (such as the FAB) along with the snackbar.
- [MD] Timing: without an action it can auto-dismiss after 4 to 10 seconds, depending on platform; with an action it should stay until acted on or dismissed. No single duration is published.
- [MD] Accessibility: announce the message without moving focus (a polite live region on Android), never trap focus. On the web, an auto-dismissing snackbar "must" be backed by inline feedback.

| Measurement | Value |
|---|---|
| Single-line height (token and prose) | 48 |
| Two-line height (token) | 68 |
| Two-line height (guidelines prose: "from 48dp to 64dp") | 64 |

- [Conv] The 68 versus 64 difference is on Material's own pages. No margin, width or maximum width value is published; only "a fixed distance" from the edges.

Source: https://m3.material.io/components/snackbar/guidelines, https://m3.material.io/components/snackbar/specs, https://m3.material.io/components/snackbar/accessibility

## Menus

- [API] The overview lists Jetpack Compose (with an Expressive entry) and Android Views as available, and Android Views Expressive as unavailable.
- [MD] Vertical menus (November 2025: rounded shapes, standard or vibrant color, selection states, gaps) are recommended for new designs. The baseline menu is still available and keeps working in existing products.
- [MD] Dropdown menu and exposed dropdown menu are both just "menu" in Material 3; they differ only in the element that opens them.
- [MD] A menu is a temporary set of actions, opened by selecting an element (icon, button, text field, filter chip, split button) or by a trigger such as secondary click or press and hold. Uses: overflow, text field dropdown, select, context menu.
- [MD] A menu takes less space than a set of radio buttons or chips.
- [MD] Items that are unavailable under some conditions should appear disabled, not be removed.
- [MD] Vibrant color is more prominent; use it sparingly.
- [MD] Grouping: a gap (at most one or two, default size, never in a scrollable menu) or a divider (scrollable menus, text field dropdowns).
- [MD] A menu that cannot show all items scrolls and shows a persistent scrollbar.
- [MD] Placement: below, beside or in front of its trigger; it repositions automatically instead of being cut off. The trigger keeps its appearance, plus a pressed state, while the menu is open.
- [MD] Submenus open beside the parent item and suit large screens. [API] The page notes submenus are not currently available on Jetpack Compose and gaps are not available on the web.
- [MD] Single-select menus keep one selected item; multi-select menus stay open until dismissed. Show selection with more than color (the default is a shape and color change at 3:1; a checkmark is recommended).
- [MD] A text field can filter the menu (autocomplete).
- [MD] Custom slots suit simple content (images, progress indicators, color swatches); slot targets should be 48 x 48 or larger.
- [MD] Compact windows: consider turning the menu into a bottom sheet, which has room for more items and longer labels.
- [MD] Accessibility: focus goes to the first item on open; disabled items can take focus but cannot be selected; dividers and gaps cannot take focus; mark an icon next to item text as decorative.
- [Conv] No maximum item count or menu height is published.

| Measurement | Vertical menu (token) | Baseline menu (measurement table) |
|---|---|---|
| Item height | 44 | 48 |
| Leading and trailing icon size | 20 | 24 |
| Gap between groups | 2 | n/a |
| Container width | not stated in text | min 112, max 280 |
| Corner radius | not stated in text | 4 |
| Left and right padding | 16 leading and trailing space | 12 |

Source: https://m3.material.io/components/menus/guidelines, https://m3.material.io/components/menus/specs, https://m3.material.io/components/menus/accessibility

## Tooltips

- [API] The overview lists Jetpack Compose as available and Android Views as unavailable. Two variants: plain and rich.
- [MD] Plain: a brief label for elements without text (icon-only buttons). Not needed when the element already has a text label. Avoid wrapping to several lines.
- [MD] Rich: longer explanations or definitions, with an optional subhead (one line), up to two text buttons and hyperlinks.
- [MD] Never hide critical information in a tooltip; the page points to a dialog instead.
- [MD] Trigger: hover on desktop, touch and hold on mobile; also keyboard focus.
- [MD] Persistent rich tooltips appear only on click or tap of the parent, or on page load to introduce a feature (include a subhead then). Avoid them on icon buttons.
- [MD] Plain tooltip position: above the element by default, below it when the element is in an app bar. Rich tooltip: below and to the trailing side by default, never covering the parent. Both shift in 8 increments to stay on screen.
- [MD] Accessibility: tooltip role; do not trap focus in a rich tooltip; it must not block important information.

| Measurement | Value |
|---|---|
| Plain tooltip distance from an element with a visual boundary; without one | 4; 8 |
| Plain tooltip height (measurement table; token min height) | 24 |
| Plain tooltip max width (token) | 320 |
| Rich tooltip padding: top; bottom; left and right | 12; 8; 16 |
| Time on screen after leaving the target | 1.5 seconds |

Source: https://m3.material.io/components/tooltips/guidelines, https://m3.material.io/components/tooltips/specs, https://m3.material.io/components/tooltips/accessibility

## Date and time pickers as dialogs

- [MD] The dialog page lists date pickers and time pickers among the content a basic dialog can hold; people confirm the selection with the dialog's action.
- [MD] Modal date picker, modal date input and the dial time picker are dialog presentations; the docked date picker and the scroll time picker are inline. Which to use, their sizes and their text-entry rules are in `references/components-controls.md`.

Source: https://m3.material.io/components/dialogs/guidelines, https://m3.material.io/components/date-pickers/guidelines, https://m3.material.io/components/time-pickers/guidelines

## Common mistakes

| Mistake | Fix |
|---|---|
| Dialog for a success message or other low-priority information | Snackbar or inline status |
| Dialog titled "Are you sure?" or "Warning!" | A specific question or statement naming what happens |
| Three buttons in a dialog ("Learn more") | Two at most; expand details inline or give them beforehand |
| Dismissive action placed after (to the right of) the confirming action | Confirming action at the trailing edge, dismissive before it |
| Lone "Cancel" on an informational dialog | A single acknowledgement action |
| Full-screen dialog shown on a tablet or desktop window | Basic dialog from medium up |
| Full-screen dialog confirmed with "Done" or "OK", or with a disabled confirm button | Specific verb (Save, Send, Create), kept enabled; show errors inline |
| Closing a full-screen dialog silently drops edits | Basic dialog to confirm the discard |
| Modal bottom sheet that opens at full height | Initial position at most half the screen; expand on pull |
| Sheet resizable only by dragging | Drag handle that cycles heights on tap, or a button |
| Side sheet with no close button, or scrolling sideways | Always a close affordance; vertical scroll only |
| Long action menu squeezed into a dropdown on a phone | Modal bottom sheet |
| Unavailable menu items removed | Show them disabled |
| Switches or buttons nested inside menu items | One action per item |
| Snackbar with two actions, a filled button, or an icon | One text-button action; no icon |
| Snackbar with an action that times out | Keep it until acted on or dismissed |
| Snackbars stacked, covering the navigation bar, or sitting behind the FAB | One at a time, above the FAB, clear of navigation |
| Hard-coding "snackbar duration is 4 seconds" or "peek height 56dp" as Material rules | Only "4 to 10 seconds, depending on platform" and the 50% initial cap are published |
| Tooltip on a labelled button, or carrying essential instructions | Tooltips label icon-only controls; essentials go inline or in a dialog |
