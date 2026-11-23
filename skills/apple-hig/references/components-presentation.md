# Presentation components: sheets, alerts, popovers, menus

Scope: choosing between and configuring sheets, alerts, action sheets (confirmation dialogs), popovers, menus, context menus, pull-down and pop-up buttons, edit menus, panels and activity views.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Which presentation
- Button order, default, cancel and destructive conventions
- Sheets
- Alerts
- Action sheets (confirmation dialogs)
- Popovers
- Menus (all kinds)
- Context menus
- Pull-down and pop-up buttons
- Edit menus
- Panels and inspectors (macOS)
- Activity views (share sheet)
- Common mistakes

## Which presentation

| Situation | Use | Not |
|---|---|---|
| Critical, unexpected information people must act on now (a problem, an uncommon irreversible destructive action, confirming a purchase) | Alert | Popover, notification, sheet |
| Information only, nothing to act on | Inline status in the relevant context (label, indicator) | Alert |
| Choices that follow an action the person just started on purpose (discard or save draft) | Action sheet / confirmation dialog (iOS, iPadOS, watchOS; SwiftUI offers it on all platforms; not supported in visionOS) | Alert, menu |
| A common, undoable action, even a destructive one (delete a message) | Just do it and support undo | Alert |
| A short scoped task or a request for specific input, then back to the parent | Sheet | Full-screen cover, new navigation level |
| Supplementary controls used while still working in the parent view | Nonmodal sheet (iOS, iPadOS), panel or inspector (macOS), split view pane (visionOS) | Modal sheet |
| Long or complex flow, immersive media, multistep editing | Full-screen modal (iOS, iPadOS), separate window or full-screen mode (macOS), Full Space (visionOS) | Sheet |
| A small amount of transient information or a few related controls anchored to an element, in regular width | Popover | Popover in compact width (use a sheet) |
| Commands or options people choose to reveal from a button | Pull-down button (actions) or pop-up button (mutually exclusive options) | Action sheet |
| Frequent commands for one item, also available elsewhere | Context menu | Context menu as the only access |
| Operations on selected text or content (Copy, Paste, Look Up) | System edit menu | Custom duplicate menu |
| Sharing and system actions on the current content | Activity view via the Share button | Custom share UI |
| A warning | Alert | Popover |
| Repeated input with visible results (find and replace) on macOS | Panel | Sheet |

- [HIG] Present content modally only when there is a clear benefit; keep modal tasks short. Full modality rules are in `references/patterns-flows.md`.
- [HIG] One modal at a time: close a sheet before showing another; never cascade popovers; nothing appears over a popover except an alert; never show two alerts at once.

Source: https://developer.apple.com/design/human-interface-guidelines/modality, https://developer.apple.com/design/human-interface-guidelines/alerts, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/popovers

## Button order, default, cancel and destructive conventions

| Context | Convention |
|---|---|
| Alert, buttons in a row | [HIG] Default button on the trailing side; Cancel typically on the leading side |
| Alert, buttons stacked | [HIG] Default button at the top; Cancel typically at the bottom |
| Action sheet | [HIG] Destructive choices at the top with the destructive style; Cancel at the bottom (upper-left corner on watchOS) |
| Sheet with one view (iOS, iPadOS) | [HIG] Cancel on the leading edge of the top toolbar; Done on the trailing edge |
| Context menu (iOS, iPadOS, visionOS) | [HIG] Destructive items at the end of the menu, marked destructive |
| Toolbar | [HIG] One primary action, trailing side (see `references/components-navigation.md`) |

- [HIG] The cancelling button is always titled "Cancel". Never make Cancel the default button.
- [HIG] Do not give the primary (default) role to a destructive button, even when it is the most likely choice (Buttons page).
- [HIG] In an alert, apply the destructive style only when the destructive action is one the person did not deliberately choose. When they chose it on purpose (Empty Trash), the confirming button is not styled destructive so Return can confirm it.
- [HIG] Any alert with a destructive action includes a Cancel button.
- [HIG] To make people read an alert instead of pressing Return, give it no default button. A single-button alert whose button is the default uses Done, not Cancel.
- [HIG] Support quick cancel paths: Esc or Command-Period with a keyboard (iOS, iPadOS, macOS, visionOS), Menu on the tvOS remote, exiting to the Home Screen (iOS, iPadOS).

Source: https://developer.apple.com/design/human-interface-guidelines/alerts, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/sheets

## Sheets

- [Req] Sheets are always modal on macOS, tvOS, visionOS and watchOS. On iOS and iPadOS a sheet can be modal or nonmodal.
- [HIG] Use a sheet for a scoped task closely related to the current context. For complex or long flows use a full-screen modal, a window, or full-screen mode instead.
- [HIG] Show one sheet at a time from the main interface. If an action in a sheet needs another sheet, close the first, show the second, and reopen the first afterwards if needed.
- [HIG] Button meanings: Cancel (or Close) dismisses without saving; Done dismisses after completing or saving; Back moves to a previous step and is not a dismiss control.
- [HIG] Never offer Done alone. Pair it with Cancel, or with Back in a multistep flow. Avoid showing Cancel, Done and Back all at once.

| Platform | Rules |
|---|---|
| iOS, iPadOS | [HIG] System detents: large (full height) and medium (about half); custom detents are possible. Large is supported automatically; adding medium lets the sheet rest at both; medium alone prevents full height. On iPhone consider medium for progressive disclosure, but not when content needs full height (compose views). Show a grabber on resizable sheets (it also lets VoiceOver users resize). Support swipe-to-dismiss, and confirm with an action sheet if there are unsaved changes. On iPad prefer the page or form sheet styles. |
| macOS | [HIG] The sheet floats over a dimmed parent window. Use a sensible default size; resizing support is welcome. People must still be able to use the app's other windows. Use a panel for repeated input-and-observe tasks. |
| visionOS | [HIG] The sheet floats in front of its dimmed window. Center it in the field of view rather than sliding it from the bottom edge; do not cover most of the window. |
| watchOS | [HIG] Full-screen, semitransparent with a blurring material. Use only when a custom title or custom content is needed (otherwise an alert or action sheet); keep it brief and occasional; do not use it for navigation. If you change the dismiss label prefer an SF Symbol and avoid text that looks like a page title. |
| tvOS | No additional considerations. |

Source: https://developer.apple.com/design/human-interface-guidelines/sheets

## Alerts

When to use:
- [HIG] Sparingly, for essential information with useful actions. Not for information alone, not at app start, not for common undoable actions even if destructive.
- [HIG] Do use one for an uncommon destructive action that cannot be undone.
- [HIG] At startup problems (no network), show cached or placeholder content plus a nonintrusive label instead.

Content:
- [Req] An alert has a title, optional informative text and up to three buttons. Text fields are available on iOS, iPadOS, macOS, visionOS; icon and accessory view on macOS and visionOS; suppression checkbox and Help button on macOS.
- [HIG] Title: specific and succinct (what happened, context, why). Not "Error" or an error code; no more than two lines. Full sentence: sentence-style capitalization with ending punctuation. Fragment: title-style capitalization, no ending punctuation.
- [HIG] Informative text only when it adds value; short complete sentences.
- [HIG] Do not explain the buttons in the text. Include a text field only when input is needed to resolve the situation.
- [HIG] Tone: direct, neutral, not accusatory, and not hiding severity.

Buttons:
- [HIG] One- or two-word titles describing the result, preferably verbs tied to the alert text ("Erase", "Delete", "View All").
- [HIG] "OK" only in purely informational alerts; avoid "Yes" and "No".
- [HIG] Placement and roles: see the conventions table above.

Platform notes:
- [HIG] iOS, iPadOS: use an action sheet, not an alert, for choices tied to an intentional action. Keep text short so the alert does not scroll at large text sizes.
- [HIG] macOS: the app icon is shown automatically. Use a caution symbol (`exclamationmark.triangle`) sparingly, not for tasks whose whole purpose is to overwrite or remove data. Repeating alerts can offer suppression.
- [HIG] visionOS: an accessory view has a maximum height of 154 pt and a 16 pt corner radius. In the Shared Space the alert appears in front of the window and stays anchored to it; in a Full Space it is centered in the field of view.

Source: https://developer.apple.com/design/human-interface-guidelines/alerts

## Action sheets (confirmation dialogs)

- [API] In SwiftUI the action-sheet role is filled by a confirmation dialog presentation modifier, available on all platforms; UIKit's action sheet style exists on iOS, iPadOS and tvOS (as stated in the HIG developer note).
- [HIG] Use for choices related to an action the person initiated; alerts are for the unexpected. Use sparingly.
- [HIG] Title short enough for one line; add a message only if necessary.
- [HIG] Provide Cancel when an action might destroy data; a SwiftUI confirmation dialog includes Cancel by default.
- [HIG] Destructive choices use the destructive style and go at the top.
- [HIG] iOS, iPadOS: use an action sheet, not a menu, for choices following an action (menus appear when people ask for them). Do not let it scroll.
- [HIG] watchOS: no more than four buttons including Cancel (Cancel is required there).
- [Req] Not supported in visionOS.

Source: https://developer.apple.com/design/human-interface-guidelines/action-sheets

## Popovers

- [HIG] For a small amount of information or a few related tasks; the popover goes away after interaction.
- [HIG] The arrow points as directly as possible at the source element; do not cover the source or content people need while using it.
- [HIG] A Close, Cancel or Done button is only for clarity (for example save vs discard). Otherwise the popover closes on an outside tap or on selection; if multiple selection is possible keep it open until dismissed.
- [HIG] When a nonmodal popover closes automatically, always save the work; discard only on an explicit Cancel.
- [HIG] One popover at a time; no popover from a popover; nothing on top of a popover except an alert.
- [HIG] Let a single tap close one popover and open another (several bar buttons each opening a popover).
- [HIG] Keep it only as large as its content; animate size changes.
- [HIG] Do not use a popover for a warning.
- [HIG] iOS, iPadOS: avoid popovers in compact width; present a sheet instead, deciding by size class.
- [HIG] macOS: consider detachable popovers that become panels; keep the detached look close to the original.
- [Req] Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/popovers

## Menus (all kinds)

- [HIG] Labels: verb or verb phrase for actions; title-style capitalization; drop articles (a, an, the).
- [HIG] Append an ellipsis when the command needs more input before it can complete.
- [HIG] Show unavailable items as unavailable (dimmed) rather than removing them; a menu or submenu stays openable even if all its items are unavailable. (Context menus differ, below.)
- [HIG] Icons: standard icons for standard actions; use sparingly; within one group give icons to all items or none.
- [HIG] Order: important and frequent items first; group related items with separators and keep related commands together even if some are used less.
- [HIG] Length: split overly long menus; long, scrolling menus are fine for user-generated lists (history, bookmarks).
- [HIG] Submenus: sparingly; one level; if a submenu exceeds about five items consider a separate menu; prefer a submenu to indented items.
- [HIG] Toggled items: one item whose label changes (Show Map / Hide Map), add a verb if ambiguous, or show both items; use a checkmark for attributes in effect.
- [HIG] iOS, iPadOS menu layouts: small (top row of four icon-only items), medium (top row of three icon-plus-label items), large (default, plain list). Use medium for three important actions; use small only for closely related grouped actions (Bold, Italic, Underline, Strikethrough) with recognizable symbols. visionOS supports small and large.
- [HIG] visionOS: show a menu near the content it controls.
- [HIG] macOS and iPadOS menu bar guidance lives on the menu bar page; see `references/platforms-*.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/menus, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar

## Context menus

- [HIG] Revealed by touch and hold (pinch and hold in visionOS), Control-click, or secondary click. Hidden by default, so:
- [HIG] Every context menu item must also be reachable in the main interface (toolbar, menu bar).
- [HIG] Include the most relevant, frequent commands for the item, not advanced or rare ones; keep the list short.
- [HIG] Support context menus consistently across the app.
- [HIG] Hide unavailable items instead of dimming them. macOS exception: Cut, Copy, Paste may appear unavailable.
- [HIG] Submenus: one level, with a predictable title. Separators: no more than about three groups.
- [HIG] Put the most used items nearest to where the menu opens; reverse the order if the menu opens above the content.
- [HIG] Do not show keyboard shortcuts in context menus.
- [HIG] Usually no title; add one only when it clarifies the effect (for example the number of selected items).
- [HIG] iOS, iPadOS, visionOS: put destructive items at the end and mark them destructive.
- [HIG] iOS, iPadOS: offer a context menu or an edit menu for an item, not both. Previews should clarify the target and keep a matching clipping shape during animation. On iPadOS a context menu on empty space can create new objects.
- [HIG] visionOS: keep the menu shorter than the window height; a context menu can replace a panel or inspector for frequent functions.
- [Req] Not supported in watchOS. No additional considerations for tvOS.

Source: https://developer.apple.com/design/human-interface-guidelines/context-menus

## Pull-down and pop-up buttons

| | Pull-down button | Pop-up button |
|---|---|---|
| Content | Actions or items directly related to the button (Add what, Sort by, Back to where) | Flat list of mutually exclusive options or states |
| After choosing | Menu closes, action runs | Menu closes, button shows the selection |
| Use the other when | Options are exclusive states, not commands | You need actions, multiple selection, or a submenu |

- [HIG] Pull-down: do not put all of a view's primary actions in one; list at least three items (for one or two use buttons or toggles); a title only if it adds meaning.
- [HIG] Pull-down: mark destructive items; the system then asks for confirmation with an action sheet (iOS) or popover (iPadOS).
- [HIG] A More ("ellipsis") pull-down saves space but hurts discoverability; use it for items that do not need prominence.
- [HIG] Pop-up: provide a useful default selection; make options predictable from an introductory label or the button label; a Custom item can hold rarely needed options.
- [HIG] iPadOS: inside a popover or modal view, a pop-up button can replace a disclosure-indicator row for a small, well-defined option set.
- [HIG] visionOS: avoid pull-down menus in toolbars.
- [Req] Neither is supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons, https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons

## Edit menus

- [HIG] Prefer the system edit menu and the system gestures that reveal it; do not build a custom menu with the same commands.
- [HIG] Show only commands relevant now; remove or dim the rest (no Copy without a selection, no Paste with nothing to paste).
- [HIG] Place custom commands next to related system ones (custom formatting after the system format items); keep custom commands few, with short verb labels.
- [HIG] Let people select and copy useful noneditable content text, but not control labels.
- [HIG] Support undo and redo; avoid other controls that duplicate edit menu commands.
- [HIG] iOS, iPadOS: the menu is a compact horizontal bar for touch and a vertical context-style menu for keyboard or pointer; make it work in both, and move it if it covers important content.
- [Req] tvOS and watchOS provide no edit menu.

Source: https://developer.apple.com/design/human-interface-guidelines/edit-menus

## Panels and inspectors (macOS)

- [Req] Panels are macOS only. On other platforms present supplementary content with a modal view, a nonmodal sheet (iOS, iPadOS) or a split view pane.
- [HIG] Use a panel for controls or information about the active window or selection. An inspector updates with the selection and fits a panel or a split view pane; an Info window (fixed content) is a regular window.
- [HIG] Prefer simple adjustment controls (sliders, steppers) over text entry in panels.
- [HIG] Give it a short noun title in title-style capitalization ("Inspector"). Bring panels forward when the app activates, hide them when it deactivates, keep them out of the Window menu's document list, and generally disable minimize.
- [HIG] Prefer standard panels; HUD-style only for media-centric apps, when a standard panel would hide essential content, or when no controls are needed. Keep HUDs small and sparing with color.

Source: https://developer.apple.com/design/human-interface-guidelines/panels

## Activity views (share sheet)

- [HIG] Open the activity view from the Share button; do not offer a second route to the same thing.
- [HIG] Do not duplicate system actions (Print, Copy). If yours differs, give it a distinct title ("Print Transaction").
- [HIG] Exclude system activities that make no sense for the content; show custom ones only when applicable.
- [HIG] Custom action titles: a verb or short verb phrase, no company or product name. Custom icons: prefer SF Symbols; a custom icon is centered in an area of about 70x70 px.
- [HIG] Extensions: keep interaction to a few steps; do not stack another modal over an extension (an alert is the exception); report long-running progress in the main app, not with a completion notification.
- [Req] Activity views are not supported in macOS (share and action extensions are), tvOS or watchOS. watchOS can present the share sheet through `ShareLink` (Collaboration and sharing page).

Source: https://developer.apple.com/design/human-interface-guidelines/activity-views, https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing

## Common mistakes

| Mistake | Fix |
|---|---|
| Alert for success messages or plain information | Inline status; confirm only significant completions |
| Alert titled "Error" with an "OK" button for an action choice | Specific title; verb buttons; "OK" only when purely informational |
| "Yes" / "No" buttons, or a cancel button titled "Dismiss", "No", "Close" | Name the action; the cancel button is "Cancel" |
| Cancel made the default; destructive button made default or primary | Default is the safe, likely action; destructive never gets the primary role |
| Confirmation alert on every delete | Skip the alert for common undoable actions; provide undo |
| Alert used to offer several follow-up choices on iOS | Action sheet / confirmation dialog |
| Menu used for choices that follow an action; action sheet opened from a "more options" button | Action sheet after an action; menu when people ask for options |
| Sheet over sheet; popover from popover; modal over a share extension | One at a time; close first |
| Sheet with only Done, or with Cancel, Done and Back together | Done plus Cancel, or Done plus Back |
| Resizable sheet without a grabber; swipe-to-dismiss that silently drops edits | Show the grabber; confirm unsaved changes with an action sheet |
| Popover in compact width; popover used for a warning | Sheet in compact width; alert for warnings |
| Feature reachable only through a context menu; dimmed items in a context menu | Mirror in the main UI; hide unavailable items |
| All actions hidden in one pull-down; pull-down with one or two items | Surface primary actions; use plain buttons for one or two |
| Pop-up button holding commands, or pull-down holding exclusive states | Swap them |
| Action sheet assumed to exist on every platform | The HIG lists it as not supported in visionOS and caps watchOS at four buttons; check the platform first |
