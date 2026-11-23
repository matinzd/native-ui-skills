# Controls: buttons, FABs, chips, selection controls, sliders, pickers, text fields

Scope: choosing and configuring buttons, button groups, split buttons, icon buttons, FABs and the FAB menu, chips, checkboxes, radio buttons, switches, sliders, date and time pickers, scroll fields and text fields. API names are in `references/implementation-components.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How to read this file
- Button hierarchy
- Which selection control for which data
- Renamed and retired controls
- Buttons
- Button groups and split button
- Icon buttons
- FAB, extended FAB and FAB menu
- Chips
- Checkbox, radio button, switch
- Sliders
- Date pickers
- Time pickers and scroll fields
- Text fields
- Common mistakes

## How to read this file

- [Conv] `[MD]` covers Material's "should", "avoid" and "Don't" captions: recommendations. `[Req]` is used only where the page says "must", "need" or "Material requires". `[API]` marks availability stated on the overview pages ("Compose" = Jetpack Compose, "Views" = Android Views; "Expressive only" = listed only under the Expressive entries).
- [Conv] Numbers are in dp from the specs measurement or token tables unless marked "prose". Sizes XS, S, M, L, XL are written in that order.
- [MD] Shared by every control here: an interactive target of at least 48 x 48 even when the visual is smaller, and no density applied by default (the accessibility pages of chips, checkbox, radio button, switch, icon buttons and text fields each say so).

Source: https://m3.material.io/components

## Button hierarchy

| Emphasis | Control | Use for | Limit on the page |
|---|---|---|---|
| Highest | FAB or extended FAB | The most important constructive action on the screen | One per screen; not minor or destructive actions |
| High | Filled button | Important, final actions that complete a flow (Save, Join now, Confirm) | Sparingly, "ideally" one per page |
| Medium-high | Tonal button | A lower-priority action that needs more weight than outlined (Next in onboarding) | n/a |
| Medium | Outlined button | Important but not primary; the secondary action next to a filled button | Simple backgrounds only; easily mistaken for a chip |
| Low | Text button | Lowest-priority actions, several options; the button of dialogs, cards and snackbars | Never underlined; simple backgrounds |
| Situational | Elevated button | A tonal button with a shadow, to separate it from a busy background | "Only when absolutely necessary" |
| Icon only | Icon button: filled, tonal, outlined, standard (high to low) | Common, well-understood actions | Only a few at once; filled sparingly |
| Contextual | Assist or suggestion chip | Optional, dynamic shortcuts | Always in a set; never the step that progresses or finishes a task |

- [Conv] The buttons page lists the five styles "in order of emphasis" as elevated, filled, tonal, outlined, text, while its prose says filled has the most impact after the FAB and that elevated is tonal plus a shadow. Use the table above; do not pick elevated for emphasis.
- [MD] Too many buttons disrupt hierarchy; move low-priority actions to an overflow menu, icon buttons, chips or text links.
- [MD] In an app bar, at most one filled or tonal icon button (`references/components-navigation.md`). In a toolbar, emphasize one action only.

Source: https://m3.material.io/components/buttons/guidelines, https://m3.material.io/components/icon-buttons/guidelines, https://m3.material.io/components/chips/guidelines

## Which selection control for which data

| Data | Use | Page statement |
|---|---|---|
| One of up to five options, all visible | Radio buttons, listed vertically | "five or fewer options" |
| One of many, or space is tight | Menu (dropdown) | Costs extra taps and effort |
| One of a few opposing views or modes (list or map) | Connected button group, single-select | Switch page: not a switch |
| Several related options from a list | Checkboxes | Not switches |
| One standalone on/off setting with immediate effect | Switch | No Save step |
| On/off choices that are saved later | Checkboxes | Switches should be immediate |
| Filter a collection by tags | Filter chips | Alternative to segmented buttons or checkboxes |
| A value along a range, applied live | Slider: standard, centered or range | Effect is immediate |
| A number or measurement from a short scrollable set | Scroll field plus a text-input alternative | Up to four digits recommended |
| A date | Docked date picker (medium and up), modal date picker (compact), modal date input (far past or future) | Date pickers page |
| A time, any minute | Scroll picker inline, dial picker in a modal, input picker for typing | Time pickers page |
| A time from presets or intervals | Button group, menu or combo box | Not a time picker |
| A binary action on an item (favorite, save) | Toggle button or toggle icon button | n/a |

Source: https://m3.material.io/components/radio-button/guidelines, https://m3.material.io/components/switch/guidelines, https://m3.material.io/components/checkbox/guidelines, https://m3.material.io/components/time-pickers/guidelines

## Renamed and retired controls

| Older name or variant | Status (Material 3 Expressive) | Use now |
|---|---|---|
| Segmented button | "No longer recommended" (note on every tab) | Connected button group |
| Speed dial, stacked small FABs | Replaced | FAB menu |
| Small FAB | "No longer recommended", still available | FAB (56), medium FAB (80) or large FAB (96) |
| Surface-color FAB and extended FAB | "No longer recommended" | Primary, secondary or tertiary (container) color styles |
| Baseline extended FAB (56, label large type) | "No longer recommended" | Small extended FAB (56, title medium type, tighter padding) |
| Small button with 24 side padding | "Not recommended" | 16 side padding |
| Continuous slider; discrete slider | Renamed | Standard slider; stops configuration |
| Baseline dial and input time pickers | "No longer recommended" (October 2026 update) | Expressive dial, input and scroll time pickers |
| Action chip; choice chip (Material 2) | Split and merged | Assist chip and suggestion chip; filter chip |

Source: https://m3.material.io/components/button-groups/overview, https://m3.material.io/components/floating-action-button/overview, https://m3.material.io/components/extended-fab/specs, https://m3.material.io/components/buttons/specs, https://m3.material.io/components/sliders/overview, https://m3.material.io/components/time-pickers/specs

## Buttons

- [API] Compose and Views, each with an Expressive entry. Variants: default and toggle. Configurations: five colors (filled is the default), five sizes (small is the default), two shapes (round is the default; square).
- [MD] Label: describes the action, ideally one to three words, sentence case, always fully visible on one line. Do not truncate or wrap.
- [MD] One optional icon, on the leading side (mirrors in right-to-left). No second icon; no icon stacked above the label. Icon and label stay grouped and centered when the button widens.
- [MD] Width hugs the label or stretches responsively; never narrower than the label. In large windows constrain the width or place the button beside other content; avoid long, flat, stretched buttons. Keep buttons in the same order across window sizes.
- [MD] Outlined and text buttons belong on simple backgrounds, not on images or video; over an image give the button a contrasting fill or use filled.
- [MD] Do not underline a text button; links are hyperlinked body text. A text button's label color must stay distinguishable from non-button text.
- [MD] In dialogs, text buttons align to the trailing edge.
- [MD] Toggle buttons are for binary selections (Save, Favorite): outlined icon when unselected, filled when selected (or a heavier weight if no filled icon exists); shape flips between round and square on selection. Keep the label length similar in both states. There is no toggle text button.
- [MD] Enabled buttons need 3:1 against the background (container for elevated, filled and tonal; label for outlined and text). On Android a label should fit within two lines at 200% text size. The accessibility label matches the visible label.
- [Req] The specs page says extra small and small buttons "must" have a 48 x 48 or larger target.

| Size | Height | Icon | Leading and trailing space | Square corner | Pressed corner |
|---|---|---|---|---|---|
| XS | 32 | 20 | 12 | 12 | 8 |
| S (default) | 40 | 20 | 16 (24 not recommended) | 12 | 8 |
| M | 56 | 24 | 24 | 16 | 12 |
| L | 96 | 32 | 48 | 28 | 16 |
| XL | 136 | 40 | 64 | 28 | 16 |

Source: https://m3.material.io/components/buttons/guidelines, https://m3.material.io/components/buttons/specs, https://m3.material.io/components/buttons/accessibility

## Button groups and split button

- [API] Button groups and the split button are listed for Compose and Views as Expressive only (new in May 2025).
- [MD] Standard button group: a row of related buttons or icon buttons that react to each other; pressing one changes its width and shape and nudges its neighbors. It hugs its content. Keep one size and one shape across the group by default; mix sizes only for hero moments.
- [MD] Connected button group: for selecting options, switching views or sorting; single-select, multi-select or selection-required, built from toggle buttons. Avoid it when none of the buttons can be toggled. It replaces the segmented button.
- [MD] A connected group should span the width of its page or surface; cap the width in larger windows. Do not mix color styles inside it. Standard icon buttons and text buttons have no container, so avoid them in groups.
- [MD] A group stays on a single line and should not wrap; trailing buttons may collapse into an overflow menu at the trailing end. Keep the primary action the most prominent at every breakpoint.
- [MD] Each button keeps a 48 x 48 minimum target; do not reduce the inner padding of XS and S groups. The group container is neither focusable nor labelled.
- [MD] Measurements: group height matches the button size (32, 40, 56, 96, 136). Standard group space between buttons 18, 12, 8, 8, 8. Connected group space 2 at every size. XS and S connected buttons have a minimum width of 48.
- [Conv] No maximum number of buttons in a connected group is stated; the "2 to 5 segments" rule belongs to the retired segmented button page.
- [MD] Split button: a main action plus a trailing button that opens a menu of related actions. Leading label one or two words; the trailing button always keeps the expand and collapse icon, which rotates 180 degrees. Color styles: elevated, filled, tonal, outlined.
- [MD] Align the menu with the trailing button, 4 away from the split button. Heights 32, 40, 56, 96, 136; the space between the halves is always 2.
- [MD] Each half needs a 48 x 48 target. The trailing button's accessibility label says that more options exist ("More watch options") and exposes the expanded or collapsed state.

Source: https://m3.material.io/components/button-groups/guidelines, https://m3.material.io/components/button-groups/specs, https://m3.material.io/components/split-button/guidelines, https://m3.material.io/components/split-button/specs

## Icon buttons

- [API] Compose and Views, each with an Expressive entry. Variants: default and toggle. Colors: filled (default), tonal, outlined, standard. Widths: narrow, default, wide. Shapes: round, square.
- [Req] The overview says icon buttons "must" use a system icon with a clear meaning.
- [MD] Use for common, easily understood actions, a few at a time. In dense layouts group them in a toolbar or button group.
- [MD] Filled for key, high-emphasis actions (sparingly); tonal for a secondary action beside a filled one; outlined for medium emphasis; standard for low emphasis or on colorful surfaces. Give the button a container when it sits on an image.
- [MD] Default icon buttons use filled icons. Toggles go from outlined to filled; without a filled version use semibold, then bold, so selection never rests on color alone.
- [MD] Do not use a toggle icon button for an action with no selected state (an overflow menu).
- [MD] On hover show a tooltip that describes the action, not the icon's name. The accessibility label also describes the action ("Add to favorites"). Icon contrast at least 3:1.
- [MD] Sizes (height): 32, 40 (default), 56, 96, 136. Icon: 20, 24, 24, 32, 40. Square and pressed corners match the buttons table.
- [Req] XS and S icon buttons "must" have a 48 x 48 or larger target; the accessibility page asks for 48 "even when nested".

Source: https://m3.material.io/components/icon-buttons/guidelines, https://m3.material.io/components/icon-buttons/specs, https://m3.material.io/components/icon-buttons/accessibility

## FAB, extended FAB and FAB menu

| Variant | Size (token) | Icon | Guidance |
|---|---|---|---|
| FAB | 56 x 56 | 24 | Smallest; compact windows where other actions are also on screen |
| Medium FAB | 80 x 80 | 28 | "Most recommended"; most situations, best in compact and medium |
| Large FAB | 96 x 96 | 36 | A clear, prominent primary action; best in expanded and larger |
| Extended FAB small, medium, large | 56, 80, 96 high | 24, 28, 36 | When a label is needed; medium or large in larger breakpoints |

- [API] FAB and extended FAB: Compose and Views, each with an Expressive entry. FAB menu: Compose Expressive only; Views Expressive is listed as unavailable.
- [MD] A FAB carries the most important, constructive action of the screen (create, favorite, share, start a process). Not every screen needs one, and a screen has at most one; cards do not get their own.
- [MD] Avoid it for minor, overflow, unclear or destructive actions (archive, trash, alerts, cut text) and for controls that suit a toolbar.
- [MD] Do not show a disabled FAB; if the action is unavailable, do not show the FAB.
- [MD] Use a clear, filled icon; nothing (such as a badge) covers the container. Icon contrast 3:1 with the container. The accessibility label describes the action.
- [MD] Placement: lower trailing ("lower right") corner in compact and medium; in expanded consider the upper leading corner, as in the navigation rail. Above the navigation bar, right-aligned.
- [MD] The FAB stays in place on scroll. On a tab or page switch it disappears and reappears (only if relevant to the new content, in the same position). It can expand into a new surface with a container transform.
- [Conv] The FAB pages publish no edge margin. 16 appears only for the extended FAB and on the FAB menu page; see `references/components-content.md`.

Extended FAB:
- [MD] Use when a label is needed to understand the action, or for constant access to the primary action over long scrolling content (checkout).
- [MD] Label one or two words at most; do not wrap or truncate. The icon is optional, but an icon without a label is not an extended FAB.
- [MD] One per screen. Not an option within a set of actions (use filled buttons). Not on top of toolbars, in the upper half of a phone screen, on cards or inside containers, or together with a floating toolbar.
- [MD] Compact and medium: bottom of the screen, centered or trailing. Expanded and larger: bottom right in both left-to-right and right-to-left, or in the navigation rail.
- [MD] It can collapse to a FAB when scrolling down and expand again when scrolling up. Margins "should" be 16.
- [Req] The accessibility label "must" start with the same first word as the visible label.

FAB menu:
- [MD] Opens only from a FAB, never from an extended FAB or another component, and appears where the FAB was. It should replace the speed dial and stacked small FABs.
- [MD] Two to six closely related items; never one. Items always keep their label; keep the icon unless necessary; do not truncate, fix widths or change shapes.
- [MD] Do not use it when the FAB is paired with a toolbar or a navigation rail.
- [MD] Close button always 56; item height 56 (items share the medium button measurements). FAB and menu margins 16, rising to 24 in large and extra-large windows. Items scroll behind the close button when height is short.
- [MD] On Android the close button is labelled "Toggle menu", role button, with an expanded or collapsed state.

Source: https://m3.material.io/components/floating-action-button/guidelines, https://m3.material.io/components/floating-action-button/specs, https://m3.material.io/components/extended-fab/guidelines, https://m3.material.io/components/fab-menu/guidelines, https://m3.material.io/components/fab-menu/specs

## Chips

| Variant | Purpose | Label |
|---|---|---|
| Assist | A smart or automated action, shown contextually after primary content | Starts with a verb; may update (Save to Saved) |
| Filter | Filters a collection; selected chips gain a leading checkmark | Nouns naming the category; no negative phrasing |
| Input | A piece of information the person entered (a contact); editable, removable | The entity |
| Suggestion | A product-generated suggestion (reply, search refinement) | Noun or short phrase |

- [API] Compose and Views; no Expressive section (August 2024: outline changed to outline variant).
- [MD] Chips are not buttons: they are dynamic, appear as a set, and represent optional paths (buttons, by contrast: no more than three in one arrangement). Actions that move to the next or previous step, or finish a task, are buttons.
- [MD] Never show a single chip alone; a filter set never has one option. Filter chip sets on a page are all single-select or all multi-select.
- [MD] Label 20 characters or fewer.
- [MD] Lay chips out inline as a row, wrapping to new rows; beyond two rows of filter chips, or in a one-row field, scroll horizontally.
- [MD] A filter chip's trailing icon (remove, open a menu) is for medium and expanded windows; in compact windows make the whole chip perform the action.
- [MD] No elevation on a plain page (allowed over images); never use elevation as pressed feedback.
- [Req] An input chip's trailing icon is required and "must" remove the chip. Secondary actions "must" have a 48 x 48 target, achieved with a chip minimum width of 88.
- [Req] Chips "must" have a minimum 48 target regardless of placement or density; keep at least 8 between chips.
- [Req] "Material requires" a secondary indicator that chips are interactive: an introductory label, an action-like label or leading icon, or the outline color role for 3:1.
- [MD] Accessibility: label contrast 3:1; an action chip exposes button semantics; a horizontally scrolling set needs a way to show all chips (reflow or a menu).
- [MD] Measurements: height 32, corner radius 8, icon 18, avatar 24, side padding 16 (8 next to an icon).

Source: https://m3.material.io/components/chips/guidelines, https://m3.material.io/components/chips/specs, https://m3.material.io/components/chips/accessibility

## Checkbox, radio button, switch

- [API] All three: Compose and Views; no Expressive section.
- [MD] Checkbox: one or more related options from a list; a parent checkbox with an indeterminate state for sub-selections. Tapping the label also toggles it. When used as on/off the effect is immediate. Box 18, state layer 40, target 48.
- [MD] Radio button: one choice with every option visible; five or fewer options, otherwise consider a dropdown menu. List vertically (avoid horizontal lists). Do not nest, and never allow multi-select.
- [MD] Every radio button has an adjacent label; tapping the label selects it. Selection applies immediately unless the dialog or page has a Save step. Icon 20, state layer 40, target 48.
- [Conv] The radio guidelines say one option should always be pre-selected; the accessibility page says a group can start with one selected or none. Default to a pre-selected option and say that Material's pages differ.
- [MD] Switch: a standalone binary setting whose effect starts immediately, without saving. Not for opposing options (use a connected button group), not as a replacement for a button, and not for selections that need saving (use checkboxes).
- [MD] A switch always has an inline label saying what is on when it is on. An optional handle icon must read as on or off (check, X); no text inside the switch.
- [MD] Switch track 52 x 32; handle 16 unselected, 24 selected, 28 pressed; target 48.

Source: https://m3.material.io/components/checkbox/guidelines, https://m3.material.io/components/radio-button/guidelines, https://m3.material.io/components/radio-button/accessibility, https://m3.material.io/components/switch/guidelines, https://m3.material.io/components/switch/specs

## Sliders

- [API] Compose and Views, each with an Expressive entry. Variants: standard, centered, range. Configurations: horizontal or vertical, five sizes (XS is the default), stops, value indicator, inset icon.
- [Req] Changes "must" take effect immediately while the handle moves.
- [MD] Standard: one value, starting from zero or the start of a sequence. Centered: the default or zero sits in the middle. Range: two handles for a minimum and maximum; avoid vertical range sliders.
- [MD] Stops: the handle snaps to the nearest stop; avoid too many. End stops are present on the inactive track for 3:1 contrast and may be removed only if the track already has it.
- [MD] The value indicator appears while a handle is pressed or dragged, one at a time on a range slider; it is not needed when the value is shown elsewhere. A linked text field next to the slider must stay in sync and be next in tab order.
- [MD] Inset icon: standard sliders of size M, L or XL only; never on centered or range sliders or on tracks under 40.
- [MD] Track height 16, 24, 40, 56, 96. Handle width 4 (2 pressed); handle height 44, 44, 52, 68, 108.

Source: https://m3.material.io/components/sliders/guidelines, https://m3.material.io/components/sliders/specs

## Date pickers

| Variant | Presentation | Use | Size (token) |
|---|---|---|---|
| Docked | Text field with a dropdown calendar | Medium and expanded windows; near and distant dates | 360 x 456 |
| Modal | Dialog with a calendar; full-screen recommended in compact | Compact windows; single dates and ranges | 360 x 524 |
| Modal date input | Dialog with typed entry | Dates that need no calendar; distant past or future | 328 x 512 |

- [API] Compose and Views; no Expressive section.
- [MD] Do not use the modal calendar to ask for a distant date such as a date of birth; use the modal date input or the docked picker.
- [MD] The modal picker and modal input swap through the edit or calendar icon; keep the text-entry route available.
- [MD] Modal pickers close on OK, Cancel, or interaction outside the dialog; the full-screen version adds a close icon and Save.
- [MD] Do not scale a date picker up responsively. Date cell 40 with a 48 x 48 target.
- [MD] Typed entry: format after Enter or blur, never while typing (no input masks); accept dashes, spaces, slashes and dots; state the format in the supporting text. Date text contrast 4.5:1.

Source: https://m3.material.io/components/date-pickers/guidelines, https://m3.material.io/components/date-pickers/specs, https://m3.material.io/components/date-pickers/accessibility

## Time pickers and scroll fields

- [API] Time pickers: Compose and Compose Expressive available; Views available, Views Expressive unavailable. Scroll fields: Compose Expressive only (introduced with the Expressive update).
- [MD] Scroll time picker: compact, preferred inline so surrounding content stays visible; also fits sheets, menus and dialogs. Input time picker: keyboard entry, inline or modal. Dial time picker: modal only; avoid it for granular selection.
- [MD] Prefer inline placement; on touch devices fall back to a scroll picker in a menu; use a modal rarely. A modal picker closes on OK, Cancel or the scrim.
- [MD] Use a time picker only for hours and minutes when any time can be chosen; presets or intervals go in a button group, menu or combo box.
- [Req] "Material requires" direct text entry in addition to scroll or dial; the toggle icon button "must" be present (or another toggle nearby).
- [MD] Follow the 24-hour setting: no AM and PM buttons, and the dial gains an inner ring.
- [MD] Never crop or scroll the dial: swap to the horizontal layout, or to a scroll or input picker when height is short.
- [MD] Dial 256; dial items, AM and PM buttons and the toggle need 48 x 48 targets; inactive scroll values need a 48-high target.
- [MD] Scroll fields: for numbers and measurements (distance, weight, temperature); for time use a time picker. Label each field when several sit side by side. Inline preferred, then a non-modal dialog, a modal rarely.
- [MD] Scroll fields offer a nearby switch to text input. Up to four digits recommended; avoid consecutive values of five or more digits. Corner radius not below 16.
- [MD] Scroll field minimum width: small (1 to 2 digits) 100, large (4 digits) 186; medium (3 digits) is 144 in the guidelines prose and 120 in the token table.

Source: https://m3.material.io/components/time-pickers/guidelines, https://m3.material.io/components/time-pickers/accessibility, https://m3.material.io/components/scroll-fields/guidelines, https://m3.material.io/components/scroll-fields/specs

## Text fields

- [API] Compose and Views; no Expressive section. Variants: filled and outlined, functionally identical.
- [MD] Choose by visual style and by which is most distinct from nearby components; outlined has less emphasis and suits dense forms. Do not mix the two next to each other or within one form; separate them by region.
- [MD] Every field has a label, always visible, aligned with the input text, never truncated and never multi-line. A separate adjacent label, aligned to the field's leading edge, can replace it.
- [MD] Required fields: an asterisk on the label plus an explanation (supporting text or one note at the top of the form); mark all required fields.
- [MD] Single-line fields scroll horizontally and are not for long answers; multi-line fields grow; text areas have a fixed height and scroll.
- [MD] Supporting text: ideally one line, persistent or shown on focus. Show a character or word counter whenever there is a limit. Prefix (currency symbol) and suffix (unit, email domain) text are supported.
- [MD] Errors: replace the supporting text with the error text instead of adding a line; say how to fix the (most likely) error; an error icon is "strongly recommended".
- [MD] Icons are optional: input-type signifier, clear (only when there is input), voice, dropdown, valid or error. Images inside a field are 24 high.
- [MD] Width: full width is acceptable in compact windows; from medium up bound the field with margins or a container. A field should not span a large screen.
- [MD] Outline contrast 3:1 against the background. The accessibility label equals the label; an interactive trailing icon gets its own ("Show password").
- [MD] Measurements: container height 56 (also the target size), side padding 16 (12 with icons), supporting text and counter 4 below the field.

Source: https://m3.material.io/components/text-fields/guidelines, https://m3.material.io/components/text-fields/specs, https://m3.material.io/components/text-fields/accessibility

## Common mistakes

| Mistake | Fix |
|---|---|
| Several filled buttons competing on one screen | One filled primary; tonal, outlined or text for the rest |
| Elevated button chosen as "the strongest" | Filled for emphasis; elevated only to separate from a busy background |
| Button label in all caps, wrapped or truncated | Sentence case, one line, one to three words |
| New segmented button, speed dial or small FAB in Expressive work | Connected button group, FAB menu, FAB or medium FAB |
| Two FABs, a FAB on each card, or a FAB for delete | One constructive FAB per screen |
| Disabled FAB | Hide it when the action is unavailable |
| Chip used as the Next or Submit action, or shown alone | A button for flow steps; chips come in sets |
| Row of switches for a multi-choice list, or a switch before a Save button | Checkboxes |
| Switch between two views (list and map) | Connected button group |
| Seven radio buttons, or radios laid out in a row | A menu above five options; vertical list |
| Calendar grid used for date of birth | Modal date input or docked picker |
| Time dial as the only way to enter a time | Keep the input toggle |
| Placeholder used as the only label; error added under existing helper text | Persistent label; error text replaces supporting text, with an error icon |
| Text field stretched across a tablet or desktop window | Constrain its width |
| 32 or 40 high buttons, chips or 18 checkboxes with a target the size of the visual | 48 x 48 target |
