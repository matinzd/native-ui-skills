# Controls: buttons, selection, input and status

Scope: choosing and configuring buttons, toggles, pickers, segmented controls, sliders, steppers, text input, progress indicators, gauges, disclosure controls, labels, page controls and the macOS-only controls.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Which control for which data
- Buttons: all platforms
- Buttons: platform specifics
- Toggles, checkboxes and radio buttons
- Pickers and date pickers
- Segmented controls
- Sliders and steppers
- Text fields, secure fields and text views
- macOS-only input controls
- Progress indicators
- Gauges, level indicators and rating indicators
- Disclosure controls
- Labels
- Page controls
- Common mistakes

## Which control for which data

| Data or intent | Control | Notes |
|---|---|---|
| Run an instantaneous action | Button | One or two prominent buttons per view at most |
| On/off state | Toggle: switch in a list row (iOS, iPadOS); button that behaves like a toggle elsewhere; checkbox or switch (macOS) | Never color-only state |
| One of 2 to about 5 closely related options, all visible | Segmented control (not watchOS); radio buttons (macOS) | About five segments on iPhone, five to seven in wide layouts |
| One option from a short list, space is tight | Pop-up button (see `references/components-presentation.md`) | Flat, mutually exclusive |
| A command chosen from a few related ones | Pull-down button | At least three items |
| One value from a medium-to-long ordered list | Picker | Very long lists: a list or table instead |
| Date, time, or both | Date picker | Compact style when space is constrained (iOS, iPadOS) |
| Several independent on/off options | Checkboxes (macOS); toggles in list rows (iOS, iPadOS) | Mixed state supported by checkboxes |
| Value in a continuous range | Slider (not tvOS) | Add a text field and stepper for wide ranges or exact entry |
| Small increments to a number | Stepper (not tvOS, watchOS) next to a visible value | Add a text field when large changes are likely |
| Short text (name, email) | Text field | Hint or label; correct keyboard type |
| Password or other sensitive text | Secure text field | Never prefill |
| Long or styled text | Text view | Editable or read-only |
| Text entry plus predefined choices | Combo box (macOS only) | Custom value is not added to the list |
| Color | Color well (iOS, iPadOS, macOS, visionOS) | System color picker preferred |
| PIN on Apple TV | Digit entry view (tvOS only) | Use secure digit fields for sensitive data |
| Progress of a task with known duration | Determinate progress indicator | |
| Activity of unknown duration | Indeterminate indicator (spinner) | Avoid on watchOS |
| A value within a range, read-only | Gauge (not tvOS); level indicator (macOS) | |
| Star rating | Rating indicator (macOS only) | No partial symbols |
| Show or hide detail | Disclosure control | Not tvOS, watchOS |
| Position in an ordered set of pages | Page control (not macOS) | More than about 10 dots is too many |

- [HIG] Prefer offering choices (picker, menu, other selection control) over requiring typed text (Entering data page).

Source: https://developer.apple.com/design/human-interface-guidelines/components, https://developer.apple.com/design/human-interface-guidelines/entering-data

## Buttons: all platforms

- [HIG] Hit region: as a general rule at least 44x44 pt, and 60x60 pt in visionOS. Leave enough space around a button to distinguish and target it. (The Accessibility page also lists smaller per-platform minimum control sizes; see the accessibility reference linked from `SKILL.md`.)
- [HIG] Always give a custom button a press state.
- [HIG] Use a prominent style (accent-colored background) for the most likely action in a view, and keep prominent buttons to one or two per view.
- [HIG] Signal the preferred choice with style, not size. Buttons that form a set are the same size.
- [HIG] (OS 26+, Liquid Glass) Do not color button labels similarly to the content behind them; over colorful content keep labels monochrome.
- [HIG] Content: a symbol, a text label, or both. Use familiar symbols for familiar actions (share is `square.and.arrow.up`). Use text when it is clearer: a few words, title-style capitalization, ideally starting with a verb ("Add to Cart").
- [API] Roles as listed in the HIG: normal, primary (the default button; uses the accent color; responds to Return and can close a temporary view), cancel, destructive (system red).
- [HIG] Give the primary role to the most likely choice. Do not give it to a destructive action even when that is the most likely choice.

Source: https://developer.apple.com/design/human-interface-guidelines/buttons

## Buttons: platform specifics

| Platform | Rules |
|---|---|
| iOS, iPadOS | [HIG] For an action that does not finish instantly, show an activity indicator inside the button, optionally with a changed label ("Checkout" to "Checking out..."). |
| macOS | [HIG] Standard type is the push button. Flexible-height push buttons only for tall or two-line content. Append an ellipsis to the title when the button opens another window, view or app. Square (gradient) buttons, help buttons and image buttons belong in the view, never in the toolbar or status bar. One help button per window at most, placed in a lower corner (opposite the dismissal buttons in a dialog). Image buttons: about 10 px of padding between image and button edges; any label goes below. Tooltips appear on hover. |
| tvOS | No additional considerations. |
| visionOS | [HIG] Sizes: mini 28 pt, small 32 pt, regular 44 pt, large 52 pt, extra large 64 pt. Shapes: circle for icon-only, rounded rectangle or capsule for text-only, capsule for icon plus text. Prefer a visible background shape and fill (thin material on glass), except in toolbars, context menus, alerts and ornaments. Do not build a custom white-fill, black-content button; that look means "toggled on". Prefer circular or capsule shapes; rounded rectangles in vertical stacks, capsules in horizontal rows. Keep centers at least 60 pt apart; buttons of 60 pt or more get 4 pt of padding around them. Avoid stacking or lining up small and mini buttons. Custom hover effects are not supported on buttons. No haptics exist, so keep the standard sounds. |
| watchOS | [HIG] Inline buttons use the capsule shape. Primary actions span the screen width. Two side-by-side buttons share one height and use images or short titles (the Layout page allows at most three glyph buttons or two text buttons in a row). Use the toolbar for corner buttons. Keep one- and two-line buttons in a stack the same height. |

Source: https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/layout

## Toggles, checkboxes and radio buttons

- [HIG] A toggle is only for two opposing states of a view or content. For choosing from a list use another control.
- [HIG] Make clear what the toggle affects; context usually suffices, macOS often adds a label.
- [HIG] State differences must be obvious and must not rely on color alone (add or remove a fill, background shape, checkmark or dot).
- [HIG] iOS, iPadOS: use the switch style only in a list row (the row content is its label). Change the default green only if necessary and keep enough contrast.
- [HIG] iOS, iPadOS: outside a list use a button that behaves like a toggle (icon plus changing background), with no explanatory label.
- [HIG] macOS: switches, checkboxes and radio buttons go in the window body, not the toolbar or status bar.
- [HIG] macOS switch: for settings you want to emphasize or that govern a group; mini switches for single rows in grouped forms. Do not replace an existing checkbox with a switch.
- [HIG] macOS checkbox: title on the trailing side; use for hierarchies of settings (align and indent dependents); show the mixed (dash) state when subordinate boxes differ; introduce an unclear group with a label.
- [HIG] macOS radio buttons: mutually exclusive options, typically two to five; beyond about five use a pop-up button. For one on/off setting prefer a checkbox. For multiple selection use checkboxes. Keep horizontal spacing consistent, sized to the longest label.

Source: https://developer.apple.com/design/human-interface-guidelines/toggles

## Pickers and date pickers

- [HIG] Use a picker for medium-to-long lists. Short list: pull-down or pop-up button. Very large set: a list or table (adjustable height, optional index).
- [HIG] Order values predictably (alphabetical, numeric) because most are hidden.
- [HIG] Show the picker in context, below or near the field (bottom of the window or a popover); do not switch views.
- [API] Minute interval can be coarsened only to values that divide evenly into 60 (default list is 0 to 59).
- [API] iOS, iPadOS date picker styles: compact (button that opens a modal editor), inline (calendar, or wheels for time-only), wheels, automatic. Modes: date, time, date and time, countdown timer (up to 23 hours 59 minutes; not available in inline or compact styles).
- [HIG] iOS, iPadOS: use the compact style when space is constrained.
- [HIG] macOS: textual style for limited space and specific values; graphical style for browsing days, picking ranges, or a clock-face look.
- [HIG] watchOS: pickers use the wheels style and the Digital Crown; long lists can appear as a navigation-link button.
- [API] tvOS: pickers are available with SwiftUI.

Source: https://developer.apple.com/design/human-interface-guidelines/pickers

## Segmented controls

- [HIG] For closely related choices that affect an object, state or view; good when grouping or a visible selection state matters.
- [HIG] Do not mix behaviours in one control: either every segment shows selection state or every segment performs an action.
- [HIG] Limit segments: no more than about five to seven in a wide interface, about five on iPhone.
- [HIG] Keep segment widths equal and content similar in size. Use text or images, not both, within one control.
- [HIG] Text segments: nouns or noun phrases, title-style capitalization, no introductory text needed.
- [HIG] iOS, iPadOS: suitable for switching closely related subviews; for separate app sections use a tab bar.
- [HIG] macOS: for view switching in the main window area use a tab view; use segmented controls in toolbars and inspectors. Selection may be single or multiple on macOS. Add introductory text, per-segment labels or tooltips for icon segments.
- [HIG] tvOS: segments select on focus, so keep other focusable elements away; prefer a split view for content filtering.
- [Req] Not supported in watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/segmented-controls

## Sliders and steppers

- [HIG] Slider direction: minimum on the leading side and maximum on the trailing side (horizontal); minimum at the bottom (vertical).
- [HIG] Customize track, thumb and end icons only when it adds meaning (small and large image icons for a size slider).
- [HIG] For wide ranges pair the slider with a text field showing the exact value, and optionally a stepper.
- [HIG] iOS, iPadOS: do not use a slider for audio volume; use the system volume view.
- [HIG] macOS: give live feedback while dragging; linear slider for a fixed start and end, circular slider for values that repeat or continue; use tick marks, label at least minimum and maximum, introduce with a label ending in a colon.
- [HIG] visionOS: prefer horizontal sliders. watchOS: sliders step by a preset amount via side buttons. Sliders are not supported in tvOS.
- [HIG] Stepper: it shows no value itself, so place it beside the value it changes. Pair with a text field when large changes are likely. macOS: consider Shift-click for a larger step (for example 10 times). Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/sliders, https://developer.apple.com/design/human-interface-guidelines/steppers

## Text fields, secure fields and text views

- [HIG] Text field for small, specific text; text view for long, multiline or specially formatted text; label for short read-only text.
- [HIG] Show a hint (placeholder). Because it disappears on typing, add a separate label when the purpose must stay visible.
- [HIG] Always use a secure text field for sensitive data such as passwords. Never prepopulate a password field (Entering data page).
- [HIG] Size the field to the expected amount of text; stack multiple fields vertically with even spacing and consistent widths.
- [HIG] Make Tab move through fields in a logical order (the system usually does).
- [HIG] Validate at a sensible moment: an email address when leaving the field; a user name or password before leaving it. Use a number formatter for numeric input and do not assume a locale's number format.
- [HIG] iOS, iPadOS, tvOS, visionOS: show the keyboard type that matches the content.
- [HIG] iOS, iPadOS: show a Clear button at the trailing end; leading end indicates purpose, trailing end offers extra features.
- [HIG] tvOS, watchOS: minimize text entry; on watchOS prefer a list of options.
- [HIG] Text views: keep text legible, adopt Dynamic Type, test with Bold Text; make useful text (error message, serial number) selectable. tvOS uses text fields, not text views, for editable text.
- [HIG] macOS: expansion tooltips can reveal clipped field text.

Source: https://developer.apple.com/design/human-interface-guidelines/text-fields, https://developer.apple.com/design/human-interface-guidelines/text-views, https://developer.apple.com/design/human-interface-guidelines/entering-data

## macOS-only input controls

- [HIG] Combo box (text field plus pull-down list): start with a meaningful default from the list; introduce with a title-style label ending in a colon; keep list items no wider than the field.
- [HIG] Token field: converts typed text into selectable tokens (comma by default; Return can be added); consider a context menu per token and a suitable suggestion delay.
- [HIG] Image well: an editable image view; restore a default image if a required image is cleared; keep standard Copy and Paste menu items working.
- [HIG] Color well: prefer the system color picker (also on iOS, iPadOS, visionOS); on macOS wells support dragging colors between them.
- [HIG] Path control: window body only (see `references/components-navigation.md`).

Source: https://developer.apple.com/design/human-interface-guidelines/combo-boxes, https://developer.apple.com/design/human-interface-guidelines/token-fields, https://developer.apple.com/design/human-interface-guidelines/image-wells, https://developer.apple.com/design/human-interface-guidelines/color-wells

## Progress indicators

- [HIG] Prefer determinate indicators; they let people decide whether to wait.
- [HIG] Report progress accurately and at an even pace; do not race to 90 percent and stall.
- [HIG] Keep indicators moving; if the process stalls, explain the problem and what to do.
- [HIG] Switch an indeterminate bar to determinate once duration is known. Never switch between the circular style and the bar style.
- [HIG] An optional description must add context; avoid vague words such as "loading" or "authenticating".
- [HIG] Keep indicator placement consistent.
- [HIG] Offer Cancel when interruption is safe; add Pause when cancelling would lose progress; warn (alert) when halting has a cost.
- [HIG] iOS, iPadOS refresh control: also refresh automatically; a title is optional and must not explain how to refresh.
- [HIG] macOS: both bar and spinner can be indeterminate; prefer a spinner for background work or tight spaces; do not label a spinner.
- [HIG] watchOS: avoid indeterminate indicators; tell people they will get a notification instead (Feedback page).

Source: https://developer.apple.com/design/human-interface-guidelines/progress-indicators, https://developer.apple.com/design/human-interface-guidelines/feedback

## Gauges, level indicators and rating indicators

- [HIG] Gauge: shows a value within a range on a circular or linear path; standard style marks the value, capacity style fills to it; the accessory variant suits Lock Screen widgets and complication-like contexts.
- [HIG] Write short labels for the current value and both endpoints; VoiceOver reads visible labels. A gradient can reinforce meaning (hot to cold).
- [HIG] macOS level indicator: capacity (continuous for large ranges, or discrete segments), rating, or rarely relevance; fill color defaults to green and may change at significant levels.
- [HIG] Rating indicator (macOS only): whole symbols only; let people change a rating inline; if you replace the star, make the meaning obvious.
- [Req] Gauges are not supported in tvOS.

Source: https://developer.apple.com/design/human-interface-guidelines/gauges, https://developer.apple.com/design/human-interface-guidelines/rating-indicators

## Disclosure controls

- [HIG] Hide detail until relevant; keep the most-used controls visible at the top of the hierarchy and advanced ones collapsed by default.
- [HIG] Disclosure triangle: points inward from the leading edge when collapsed, down when expanded; give it a descriptive label ("Advanced Options").
- [HIG] Disclosure button: points down when collapsed, up when expanded; place it next to the content it reveals; no more than one per view.
- [API] iOS, iPadOS, visionOS provide disclosure through SwiftUI `DisclosureGroup`. Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/disclosure-controls

## Labels

- [HIG] Label for a small amount of uneditable text; text field if editable; text view if long.
- [HIG] Prefer system fonts; labels support Dynamic Type where available.
- [HIG] Use the four system label colors by importance: label (primary), secondary label (subheading or supplemental), tertiary label (unavailable items), quaternary label (watermark text).
- [HIG] Make useful label text selectable (error message, location, IP address).
- [HIG] watchOS: use the system date and timer text components; they resize and update automatically.

Source: https://developer.apple.com/design/human-interface-guidelines/labels

## Page controls

- [HIG] Only for an ordered, flat list of peer pages; not for hierarchy.
- [HIG] Center it horizontally near the bottom of the view.
- [HIG] More than about 10 dots is hard to count; with more peer pages use another arrangement such as a grid.
- [HIG] Custom indicator images: simple, no negative space, text or inner lines; no more than two different images in one control; do not color them.
- [HIG] iOS, iPadOS: people tap or scrub. Do not animate page transitions during scrubbing. Background styles: automatic (shown during interaction), prominent (always; only when it is the primary navigation), minimal (never; then do not support scrubbing).
- [HIG] With a paging scroll view, do not also show the scroll indicator on the same axis.
- [HIG] tvOS: use on collections of full-screen pages. visionOS: display only, not interactive. watchOS: bottom for horizontal paging, beside the Digital Crown for vertical tab views. Not supported in macOS.

Source: https://developer.apple.com/design/human-interface-guidelines/page-controls, https://developer.apple.com/design/human-interface-guidelines/scroll-views

## Common mistakes

| Mistake | Fix |
|---|---|
| Several filled, accent-colored buttons in one view | One prominent button (two at most); others use quieter styles |
| Preferred action made larger than its siblings | Same size; differentiate by style |
| "Delete" given the primary role or made the Return-key default | Primary goes to a nondestructive action; destructive role only marks it |
| Tap target under 44x44 pt (60x60 pt visionOS) | Enlarge the hit region, not necessarily the glyph |
| Switch floating in a custom iOS layout or toolbar | Switch only in list rows; elsewhere a toggle-style button |
| On/off state shown by tint alone | Add a shape, fill or checkmark change |
| Segmented control with 8 options on iPhone, or mixing icons and text, or mixing actions with selection | About five; one content type; one behaviour |
| Segmented control or tab bar used interchangeably | Tab bar for app sections; segmented control for related subviews |
| Wheel picker for three options; picker pushed on a separate screen | Menu-style button for short lists; show pickers in context |
| Slider as the only way to enter an exact value | Add a text field and stepper |
| Volume slider on iOS | System volume view |
| Stepper with no visible value | Place the value next to it |
| Password in a plain text field, or prefilled | Secure field, never prefilled |
| Placeholder as the only label on a long form | Add a persistent label |
| Wrong keyboard for email, number or URL fields | Set the matching keyboard type |
| Spinner captioned "Loading..." for a measurable task | Determinate indicator with a specific description |
| Spinner replaced by a progress bar midway | Keep one shape; only indeterminate bar to determinate bar is fine |
| More than one disclosure button in a view; page control with dozens of dots | One disclosure button; use a grid for many pages |
