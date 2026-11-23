# Interaction patterns and inputs

Scope: feedback, undo and redo, drag and drop, file management, and input methods: gestures, keyboards, pointing devices, touch on Mac, focus, Apple Pencil, Digital Crown, remotes, eyes and hands.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Inputs by platform
- Feedback
- Undo and redo
- Drag and drop
- File management
- Gestures: rules and standard gestures
- Gestures: platform specifics
- Keyboards and shortcuts
- Pointing devices and hover
- Touch on Mac
- Focus and selection
- Apple Pencil and Scribble (iPadOS)
- Digital Crown
- Remotes (tvOS)
- Eyes and hands (visionOS)
- Common mistakes

## Inputs by platform

| Platform | Primary input | Also design for |
|---|---|---|
| iOS | Touch gestures | Hardware keyboard, Full Keyboard Access, voice, Switch Control |
| iPadOS | Touch gestures | Pointer (trackpad, mouse), hardware keyboard and focus system, Apple Pencil |
| macOS | Keyboard and pointing device | Trackpad gestures; touch as a secondary input on a Mac with a touch display or an iPad via Sidecar |
| tvOS | Siri Remote (focus, swipe, press) | Game controller, attached keyboard |
| visionOS | Eyes plus indirect hand gestures | Direct touch, pointer, keyboard, game controller |
| watchOS | Touch and Digital Crown | Double tap (watchOS 11+); no physical keyboard |

- [HIG] Never assume one input: give people more than one way to do everything (Gestures, Eyes, Accessibility pages).
- Per-platform detail lives in `references/platforms-*.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/inputs, https://developer.apple.com/design/human-interface-guidelines/gestures

## Feedback

- [HIG] Match delivery to significance: passive, in-place status for routine information; interruption only for warnings about possible data loss.
- [HIG] Make feedback accessible by using several channels (color, text, sound, haptics).
- [HIG] Integrate status near the items it describes (for example an update time and unread count in a toolbar).
- [HIG] Alerts are for critical and ideally actionable information; overuse weakens them.
- [HIG] Warn only when data loss is unexpected and irreversible. Do not warn when loss is the expected result of the action (moving a file to the Trash).
- [HIG] Confirm completion only for sufficiently important actions (a payment); people otherwise assume success and need to hear only about failure.
- [HIG] When a command cannot be carried out, say so and help people understand why.
- [HIG] watchOS: avoid indeterminate progress indicators; tell people a notification will arrive when the work is done.
- [HIG] Haptics have their own page (Playing haptics); visionOS plays no haptics, so standard control sounds matter there (Buttons page).

Source: https://developer.apple.com/design/human-interface-guidelines/feedback, https://developer.apple.com/design/human-interface-guidelines/playing-haptics

## Undo and redo

- [HIG] Help people predict the result: name the operation in menu items ("Undo Typing", "Redo Bold") and in the iPhone shake alert.
- [HIG] Show the result of each undo or redo, scrolling to it if it is offscreen, so people do not repeat it blindly.
- [HIG] Allow multiple undos; do not impose unnecessary limits. People expect to undo back to a logical point such as opening the document.
- [HIG] Consider reverting a batch of related changes at once, or all changes since open or save.
- [HIG] Add dedicated undo and redo buttons only when necessary; use the standard symbols and put them in a toolbar.
- [HIG] iOS, iPadOS: do not redefine the standard undo gestures (three-finger swipe, shake). The alert title gets an automatic "Undo " or "Redo " prefix; supply one or two words after it ("Undo Name").
- [HIG] macOS: Undo and Redo at the top of the Edit menu, with Command-Z and Shift-Command-Z.
- [API] Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/undo-and-redo

## Drag and drop

- [HIG] Support drag and drop throughout the app; system text fields and text views already do.
- [HIG] Always offer a non-drag alternative (menu commands such as copy and move); on iOS and iPadOS expose drag sources and drop points to assistive technologies.
- [HIG] Default semantics: within the same container a drop moves; to a different container it copies. [API] Between apps it is always a copy.
- [HIG] With a hardware keyboard, check the Option key at drop time: held means copy within the same container.
- [HIG] Support multi-item drags. iPadOS lets people add items to a drag in progress; accept multiple simultaneous drops.
- [HIG] Prefer making drops undoable; ask for confirmation before a drop that cannot be undone.
- [HIG] Offer dragged content in several representations ordered from highest to lowest fidelity; on drop take the richest one you support, and extract only the relevant part.
- [HIG] Feedback: show a translucent drag image once the selection has moved about 3 pt; highlight a destination only while content is over it and only if it can accept the content; show nothing or a "not allowed" image (`circle.slash`) otherwise; animate a failed drop (return to source, or scale up and fade).
- [HIG] Autoscroll a destination while an item is dragged within it.
- [HIG] After the drop: show progress or a placeholder for slow transfers; keep dropped content selected in the destination and deselect or remove it in the source as appropriate; keep text styling if both sides support it, else use the destination style.
- [HIG] Consider spring loading (dragging over a button or segmented control activates it; force click on a Magic Trackpad, hover on iPad).
- [HIG] macOS: let people drag to the Finder in a format the app can reopen; allow dragging from an inactive window without activating it; badge multi-item drags with a count; use the copy, link, disappearing-item and not-allowed pointers; select and drag in one motion.
- [HIG] visionOS: when content is dropped into empty space, open the app's window for it.
- [API] Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/drag-and-drop

## File management

- [HIG] Save automatically and periodically, and when closing or switching apps; do not make people save explicitly.
- [HIG] Offer New and Open through menus and keyboard shortcuts (iPadOS shortcut interface, macOS File menu) and also provide an Add (+) button.
- [HIG] Prefer the system file browser and open and save views; a custom browser must still let people reach the rest of the file system.
- [HIG] Hide file extensions by default, with an option to show them.
- [HIG] Use Quick Look to preview files the app cannot open; provide a Quick Look generator for custom file types.
- [API] iOS 18 and iPadOS 18 and later: document-based apps can use the system document launcher (`DocumentGroupLaunchScene`), as stated on the page.
- [HIG] macOS with autosave turned off by the user: show a dot on the close button and in the Window menu for unsaved documents and present a save dialog on close, quit, log out or restart. Do not show the dot when autosave is on.
- [HIG] A file provider extension shows only documents suited to the host context and adds no second top toolbar.

Source: https://developer.apple.com/design/human-interface-guidelines/file-management

## Gestures: rules and standard gestures

- [HIG] Respond to standard gestures the way every app does. Do not repurpose a familiar gesture (tap, swipe) for an app-unique action, and do not invent a gesture for a standard action such as activating a button or scrolling.
- [HIG] Respond immediately and give feedback that predicts the result.
- [HIG] Show when a gesture is unavailable (a locked object, a disabled button) so the app does not look frozen.
- [HIG] Custom gestures only when necessary (frequent, specialized tasks). They must be discoverable, easy to perform, distinct from other gestures, and never the only way to do something important.
- [HIG] Shortcut gestures supplement visible controls; they do not replace them. A swipe-back shortcut still needs the toolbar Back button.
- [HIG] Do not conflict with gestures that reach system UI (screen-edge swipes, the visionOS hand roll). Games and immersive apps may defer the system gesture in specific cases.

| Standard gesture | Common action | Platforms |
|---|---|---|
| Tap | Activate a control; select an item | All |
| Swipe | Reveal actions and controls; dismiss views; scroll | All |
| Drag | Move an element | All |
| Touch (or pinch) and hold | Reveal additional controls or functionality | All |
| Double tap | Zoom in, or out if already zoomed; open an item on a Mac with a touch display; primary action on Apple Watch Series 9 and later and Ultra 2 and later | All |
| Zoom | Zoom a view; magnify content | All except watchOS |
| Rotate | Rotate a selected item | All except watchOS |

Source: https://developer.apple.com/design/human-interface-guidelines/gestures

## Gestures: platform specifics

| Platform | Rules |
|---|---|
| iOS, iPadOS | [API] System gestures people expect: three-finger swipe (left undo, right redo), three-finger pinch (in copy, out paste), four-finger swipe to switch apps (iPadOS only), shake (undo, redo). [HIG] Do not redefine them. Simultaneous gesture recognition is mainly useful in games. |
| macOS | [HIG] Standard gestures work on Magic Trackpad and Magic Mouse; do not redefine systemwide trackpad gestures (Dock, Mission Control), which people can also customize. Touch is covered under Touch on Mac. |
| tvOS | [HIG] Standard gestures through the remote; see Remotes. |
| visionOS | [HIG] Support both indirect gestures (look, then pinch) and direct touch; prefer indirect for UI and standard components, and reserve direct and custom gestures for close-up objects. Do not require specific body movements or positions. Details under Eyes and hands. |
| watchOS | [API] watchOS 11 and later: double tap scrolls lists and scroll views, advances vertical tabs, or triggers the view's designated primary action. [HIG] Do not set a primary action in views with lists, scroll views or vertical tabs; elsewhere assign it to the most-used button. Avoid conflicts with edge swipes. |

Source: https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/pointing-devices

## Keyboards and shortcuts

- [HIG] Support Full Keyboard Access (iOS, iPadOS, macOS, visionOS) and test with it turned on.
- [HIG] iPadOS: support keyboard navigation for text fields, text views, sidebars, lists and collections, but do not add your own keyboard navigation for controls such as buttons, segmented controls and switches; Full Keyboard Access handles those.
- [HIG] Do not repurpose standard shortcuts. Redefine one only if its standard action makes no sense in the app (Command-I for Get Info in an app without text styling).
- [HIG] Define custom shortcuts only for the most frequently used app-specific commands.
- [HIG] Modifiers: Command is the main modifier; Shift is a secondary modifier for a related command; Option sparingly, for less common or power features; avoid Control, which the system uses heavily.
- [HIG] List modifiers in the order Control, Option, Shift, Command.
- [HIG] Do not add Shift to reach the upper character of a key: write Command-Question mark, not Shift-Command-Slash.
- [HIG] Do not build a new shortcut by adding a modifier to an existing shortcut for an unrelated command (Shift-Command-Z must stay related to undo and redo).
- [HIG] Let the system localize and mirror shortcuts; avoid extra modifiers with characters that are not on every keyboard layout.
- [HIG] Keep expected modifier behaviours while dragging (Shift constrains resizing; Option duplicates) and make them identical for touch and pointer.
- [HIG] visionOS: holding Command shows a flat shortcut list grouped by menu category, so write shortcut titles that stand alone (`discoverabilityTitle`).
- [API] Physical keyboards are not supported on watchOS.

Standard shortcuts agents most often collide with (the page has the full table):

| Shortcut | Standard action | Shortcut | Standard action |
|---|---|---|---|
| Command-Comma | Open app settings | Command-Q | Quit |
| Command-N | New document | Command-W | Close window |
| Command-O | Open | Command-H | Hide app |
| Command-S | Save | Command-M | Minimize window |
| Shift-Command-S | Duplicate or Save As | Command-P | Print |
| Command-Z | Undo | Shift-Command-Z | Redo |
| Command-X, Command-C, Command-V | Cut, Copy, Paste | Command-A | Select all |
| Command-F | Find | Command-G | Find next |
| Command-B, Command-I, Command-U | Bold, Italic, Underline | Command-T | Show Fonts |
| Control-Command-F | Enter full screen | Option-Command-T | Show or hide toolbar |
| Command-Question mark | Help menu | Esc or Command-Period | Cancel |
| Command-Tab | Next app | Command-Space | Spotlight |

Source: https://developer.apple.com/design/human-interface-guidelines/keyboards, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection

## Pointing devices and hover

- [HIG] Behave consistently across gestures, eyes, pointer and keyboard; people switch inputs freely.
- [HIG] Let the pointer reveal controls that auto-hide or minimize (playback controls, a minimized toolbar).
- [HIG] iPadOS: the pointer adds to touch and does not replace it. Distinguish pointer from finger input only when it adds value (click-to-seek on a scrubber).
- [HIG] iPadOS content effects and when to use them: highlight for a group of controls in a Liquid Glass container (default for bar buttons, tab bars, segmented controls, edit menus); lift for a standalone Liquid Glass control or a small opaque element; hover (custom scale, tint, shadow) for large elements.
- [HIG] iPadOS hit regions: add about 12 pt of padding around bezeled elements and about 24 pt around the visible edges of elements without a bezel. Make hit regions of adjacent custom bar buttons contiguous.
- [HIG] Custom elements that behave like standard ones use the standard pointer effects. No decorative pointer effects. Keep custom pointer shapes simple. Never attach instructional text to the pointer; value annotations (coordinates, dimensions) are acceptable.
- [HIG] Custom hover: scale only where there is room (not table rows); in tight spaces use tint alone; shadow without scale looks wrong.
- [HIG] Support band (click-and-drag) multiple selection in custom iPadOS views when needed (`UIBandSelectionInteraction`).
- [HIG] macOS: honour standard clicks and gestures (primary click selects or activates; secondary click opens context menus; scrolling, smart zoom, swipe between pages, force click). Use standard pointer styles to signal state: arrow, pointing hand for links, I-beam for text, open and closed hand for repositioning, resize pointers, drag copy, drag link, operation not allowed.
- [HIG] macOS and visionOS show tooltips on hover; see `references/patterns-flows.md` (Offering help).
- [API] visionOS: an attached pointer follows where people look; the hover highlight from eyes is separate. No additional considerations for iOS. Not supported in tvOS or watchOS.

Source: https://developer.apple.com/design/human-interface-guidelines/pointing-devices

## Touch on Mac

(Added to the HIG on October 28, 2026: Mac with a touch display, or iPad connected with Sidecar.)

- [HIG] Touch is secondary to keyboard and pointer. Keep the layout and size of interface elements the same when touch is supported.
- [HIG] Enlarge tap targets, not the controls. Standard framework controls get suitable tap targets automatically.
- [HIG] For small or dense controls consider a temporary expanded variant on tap; standard steppers, sliders and dials do this automatically.
- [HIG] Never make touch the only way to reach a control or feature. Conversely, give touch equivalents to pointer-only actions (modifier drags, hover menus).
- [HIG] Reuse gestures people know from iPhone, iPad and the trackpad; make custom gestures work for both touch and trackpad; test against macOS system gestures.
- [HIG] Hover-revealed controls: add touch support only for essential ones (not tooltips, not what touch can already do). Reveal on a tap in the control's general location, hide after use or a few seconds, and do not keep them permanently visible. Keep the current selection when revealing. Also put essential hidden controls in a context menu (touch and hold opens it).
- [HIG] Sidebar: tapping a header or row performs its normal action and reveals that item's hidden controls; a first tap on a hidden control's area only reveals it. Tabbed window: a tap anywhere reveals the selected tab's close button.

| Action | Trackpad | Touch display |
|---|---|---|
| Select | Primary click | Tap |
| Open | Double click | Double tap |
| Scroll | Two-finger slide | One-finger slide |
| Zoom, rotate | Pinch; two fingers around each other | Same |
| Context menu | Secondary click | Touch and hold |
| Drag | Click and drag | Touch and hold, then drag |

Source: https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/pointing-devices

## Focus and selection

- [HIG] Rely on system focus effects; create custom ones only when absolutely necessary.
- [HIG] Do not move focus without the person's interaction. Exception: with discrete directional input (keyboard, remote, controller), when the focused item disappears move focus to a nearby item; otherwise hide the focus indicator.
- [HIG] Use a focus ring for text and search fields; use a row highlight in lists and collections.
- [HIG] iPadOS, macOS: provide focus for content elements (list items, text fields, search fields), not for controls such as buttons, sliders and toggles.
- [API] iPadOS 15 and later has a focus system with focus groups: Tab moves between groups (sidebar, grid, list); arrow keys move within a group. Order is reading order; group custom views and set priorities where needed (as stated on the page).
- [HIG] tvOS: every onscreen element must be reachable by focus. Supply assets for the larger focused size and leave room so focused items do not crowd neighbours. Do not show a pointer for interface navigation. In full-screen content, gestures act on the content, not on focus.
- [API] The focus system is not supported in iOS or watchOS. In visionOS it applies to connected keyboards and controllers and is separate from the eye-driven hover effect.

Source: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection

## Apple Pencil and Scribble (iPadOS)

- [HIG] Marks start the instant Pencil touches the screen: no button, no mode switch.
- [HIG] All controls respond to Pencil as well as fingers, so people need not switch.
- [HIG] Design for left- and right-handed use; avoid controls a hand would cover, or make them movable.
- [HIG] Hover previews what a touch will do; never trigger an action from hover. Prefer hover previews for Pencil rather than for pointing devices.
- [HIG] Double tap and squeeze (Apple Pencil Pro): respect the system settings; only quick, discrete, nondestructive, easily undone actions; show squeeze-revealed UI near the tip. Barrel roll only modifies marking.
- [HIG] Scribble works in standard text components by default (not password fields). For custom fields: no tap-to-activate, no autocompletion or placeholder overlapping handwriting, no moving, resizing or autoscrolling while writing, and enough room to write.
- [HIG] In compact width the PencilKit tool picker has no undo or redo buttons; add them to a toolbar.

Source: https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble

## Digital Crown

- [HIG] watchOS 10 and later: the Crown is the primary navigation input. Lay out lists, tabs and scroll views vertically so it drives them, and back every Crown interaction with a touch equivalent.
- [HIG] Where navigation is not needed, use the Crown to inspect data or drive a control.
- [HIG] Always give visual feedback, and update at a rate that matches rotation speed so values stay selectable.
- [HIG] Keep default haptic detents unless they mismatch the animation.
- [API] Apps cannot respond to Crown presses on watchOS. On Apple Vision Pro the Crown is system-only (volume, immersion level, recenter, accessibility settings, Home View).

Source: https://developer.apple.com/design/human-interface-guidelines/digital-crown

## Remotes (tvOS)

- [HIG] Standard gestures for standard actions; custom gestures mainly in gameplay. Focus always moves in the direction of the gesture.
- [HIG] Distinguish press (intentional: activate, confirm) from tap (navigation, extra information); ignore inadvertent taps, especially during live video.
- [HIG] Back opens the parent of the current screen (at the top level, the Apple TV Home Screen). During gameplay it opens an in-game pause menu, and Back again resumes.
- [HIG] Play/Pause plays, pauses or resumes media.

| Button or area | In an app | In a game |
|---|---|---|
| Touch surface, swipe | Navigates; changes focus | Directional pad |
| Touch surface, press | Activates; navigates deeper | Primary button |
| Back | Previous screen; exits to Home Screen | Pauses or resumes; previous screen or main menu |
| Play/Pause | Starts, pauses, resumes playback | Secondary button; skips intro video |

Source: https://developer.apple.com/design/human-interface-guidelines/remotes

## Eyes and hands (visionOS)

Short pointers; the visionOS file among `references/platforms-*.md` goes deeper.

- [API] The system does not tell apps where people look before they tap; a hover effect is drawn by the system outside the app's process, so it cannot trigger app logic.
- [HIG] Prefer standard components; they highlight consistently when looked at.
- [HIG] Space interactive items: at least 16 pt of margin around each, or centers at least 60 pt apart. Prefer rounded shapes. A multi-element component needs one containing shape for the highlight.
- [HIG] For sustained viewing place content at least one meter away. Avoid patterns or textures that fill the field of view, and minimize motion near what people are looking at.
- [HIG] Use custom hover effects rarely, for special moments.
- [HIG] Custom hand gestures need a Full Space and permission for hand data; prioritize comfort, avoid requiring both hands or a specific hand, and offer a lower-effort alternative.
- [HIG] visionOS 2 and later: keep the area around the hand free for the system overlay (look at palm) and avoid custom gestures built on a rolling hand, wrist and forearm motion; do not anchor content to hands or wrists if possible.

Source: https://developer.apple.com/design/human-interface-guidelines/eyes, https://developer.apple.com/design/human-interface-guidelines/gestures

## Common mistakes

| Mistake | Fix |
|---|---|
| Swipe actions, long press or drag as the only route to a feature | Add a visible control or menu command |
| Custom edge swipe or bottom-edge gesture that fights system gestures | Move the gesture; defer system gestures only in games or immersive content |
| Navigation without a Back button because swipe-back exists | Keep the standard Back button |
| Overriding three-finger swipe or shake on iOS, or trackpad system gestures on macOS | Leave system gestures alone |
| Repurposing Command-W, Command-Q, Command-Comma or Command-Z | Keep standard meanings; choose a free combination with Command |
| Shortcuts built on Control, or written as "Cmd+Shift+X" order | Avoid Control; order is Control, Option, Shift, Command |
| Hand-rolled Tab navigation for buttons and switches on iPadOS | Leave controls to Full Keyboard Access; add focus for content only |
| Moving focus programmatically after an update | Leave focus where the person put it |
| Hover-only controls (pointer, Pencil hover, Mac touch) with no other access | Reveal on tap, mirror in a context menu, never act on hover alone |
| Mac controls enlarged for touch | Same size; larger tap targets |
| Decorative pointer effects or pointer-attached instructions on iPad | System highlight, lift or hover effects only where useful |
| Confirmation alert for every expected deletion; success alert after routine saves | Undo support and inline status |
| Single-level undo, or undo that changes something offscreen silently | Multiple levels; scroll to and highlight the result |
| Drop target that highlights for content it cannot accept | Highlight only valid destinations; show the not-allowed state |
| Explicit Save button as the only way to keep work | Autosave |
| Pencil drawing that needs a "draw mode" toggle first | Mark on first touch |
| watchOS primary double-tap action in a scrolling view | Only in nonscrolling views |
| tvOS screen with elements the focus engine cannot reach, or a visible cursor | Make everything focusable; use focus, not a pointer |
| visionOS controls packed closer than 60 pt center to center, or square-cornered targets | Space them out; round the shapes |
