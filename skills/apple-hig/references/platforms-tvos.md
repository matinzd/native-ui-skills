# tvOS (Apple TV)

Scope: what is specific to designing for Apple TV: the focus engine, the Siri Remote, 10-foot layout numbers (safe insets, grids, tab bar constants), Top Shelf, text entry and search, appearance, and what does not exist on tvOS.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Focus engine
- Remote
- Navigation model
- Layout numbers
- Text entry and search
- Top Shelf
- Appearance, images and Liquid Glass
- Not available on tvOS
- Common mistakes

## Device and context

- [HIG] Very large, high-resolution display viewed from many feet away, often 8 feet or more; people may keep interacting while moving around the room.
- [HIG] Inputs: a remote, a game controller, voice, and apps on people's other devices. There is no touch screen and no pointer model.
- [HIG] Sessions are often hours long and immersive; Picture in Picture lets people follow a second video or app.
- [HIG] It is a shared device: make sign-in easy and infrequent, handle shared sign-in, and switch profiles automatically when the current viewer changes.
- [HIG] Deliver edge-to-edge artwork, subtle fluid animation and engaging audio that read clearly from across the room.
- [HIG] System experiences to integrate with: the TV app, SharePlay, Top Shelf, TV provider accounts.
- [Req] A launch screen is required on tvOS. [API] It is static (unlike the layered images used elsewhere).

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos, https://developer.apple.com/design/human-interface-guidelines/launching, https://developer.apple.com/design/human-interface-guidelines/multitasking

## Focus engine

- [HIG] Make sure every interactive element can receive focus (the page says "you need to"): people use directional gestures on the remote or controller (or arrow keys) to reach every onscreen element, unlike iPadOS and macOS where only content elements need focus.
- [HIG] Focusing and selecting are separate: moving focus only highlights; a press selects or activates, because selection opens things.
- [HIG] Rely on system focus effects. tvOS generally uses the parallax effect: the focused item rises to the foreground, sways gently and is illuminated. Layered images are required for parallax.
- [HIG] A focused item usually grows. Supply assets for the larger focused size and leave enough padding that it does not crowd or overlap neighbours.
- [HIG] Design for up to five visually distinct states: unfocused, focused, highlighted (the moment of choosing), selected, and unavailable.
- [HIG] Do not move focus without the person's interaction. The one exception: when the focused item disappears while people are moving with a discrete directional input, move focus to a nearby remaining item.
- [HIG] Always move focus in the direction of the gesture.
- [HIG] Avoid displaying a pointer. Free-form movement can make sense in gameplay, but menus and interface elements use the focus model. If a pointer is truly required, make it highly visible and integrated.
- [HIG] In a full-screen experience (a photo, a video) gestures act on the content, not on focus.
- [HIG] Never indicate focus with color alone; scaling and responsive animation are the primary signals.
- [HIG] In tables, a focused row highlights, grows slightly and may round its corners; check adjacent images and do not add your own corner masks.
- [HIG] On custom controls, adopt the standard focus APIs so they gain the same Liquid Glass focus appearance as system controls (OS 26+).

Source: https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/color, https://developer.apple.com/design/human-interface-guidelines/images, https://developer.apple.com/design/human-interface-guidelines/lists-and-tables

## Remote

| Button or area | In an app | In a game |
|---|---|---|
| Touch surface, swipe | Navigates; changes focus | Directional pad |
| Touch surface, press | Activates a control or item; navigates deeper | Primary button |
| Back | Returns to the previous screen; exits to the Home Screen | Pauses or resumes; returns to the previous screen, main menu or Home Screen |
| Play/Pause | Starts, pauses and resumes media playback | Secondary button; skips intro video |

- [HIG] Use standard gestures for standard actions; outside gameplay, do not redefine remote behaviour.
- [HIG] Back opens the parent of the current screen, which is defined by the app hierarchy and is not necessarily the previous screen. At the top level the parent is the Apple TV Home Screen. Pressing and holding Back always goes to the Home Screen.
- [HIG] In active gameplay, Back opens a pause menu instead (and closes it again), so accidental presses do not eject the player.
- [HIG] Distinguish press from tap. A press is intentional: use it to choose, confirm and act. Taps can happen by accident when someone rests a thumb or hands the remote over, so avoid responding to taps during live video playback.
- [HIG] The touch surface distinguishes up, down, left and right taps; use positional taps only when the behaviour is intuitive and discoverable.
- [HIG] Play/Pause must play, pause and resume during media playback.
- [HIG] Compatible remotes may have guide and page up/down buttons: open the EPG on guide/browse, page through it with page up/down, and change channel with page up/down while content plays.
- [HIG] tvOS and visionOS apps may require a game controller (the App Store shows a badge), but must still handle launch without one connected.

Source: https://developer.apple.com/design/human-interface-guidelines/remotes, https://developer.apple.com/design/human-interface-guidelines/game-controls

## Navigation model

- [HIG] Top-level navigation is a tab bar at the top of the screen. It is translucent by default with only the selected tab opaque; when focused, the selected tab gains a drop shadow.
- [HIG] The tab bar is customizable on tvOS (background tint, color or image; fonts; selected and unselected tints; button icons such as settings and search).
- [HIG] Scrolling: when a tab contains a single main view, people can scroll the tab bar offscreen. When the screen contains a split view, the tab bar stays pinned. Focus returns to the tab bar at the top when people press the remote's Menu (Back) button.
- [HIG] Too many tabs: the system truncates with a fade at the right edge, and at the left edge once the bar scrolls. Keep the count low enough to avoid it.
- [HIG] Live-viewing apps order tabs: live content, then cloud DVR or other recorded content, then other content.
- [HIG] Split views work well for filtering: categories in the primary pane, results in the secondary. Default proportions are one third and two thirds; half and half is also available.
- [HIG] Put one title above a split view, not a title per pane; center it when the secondary pane is a collection, or place it above the primary pane when the secondary pane is a single main view.
- [HIG] Page controls are for collections of full-screen peer pages; do not add other controls to such screens.
- [HIG] Context menus and action sheets exist on tvOS with no platform-specific guidance; alerts follow the general rules.
- [HIG] Lockups (cards, caption buttons, monograms, posters) are tvOS-only units of content view plus header and footer that expand together on focus; keep sizes consistent within a row and leave room for expansion.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/page-controls, https://developer.apple.com/design/human-interface-guidelines/lockups

## Layout numbers

| Item | Value | Tag |
|---|---|---|
| Safe area for primary content | inset 60 pt from top and bottom, 80 pt from the sides | [HIG] |
| Tab bar height | 68 pt, fixed | [API] |
| Tab bar top edge | 46 pt from the top of the screen, fixed | [API] |
| Default / minimum text size | 29 pt / 23 pt | [HIG] |
| Default / minimum control size | 66x66 pt / 56x56 pt | [HIG] |
| Body text style | 29 pt, 36 pt leading, Medium weight | [HIG] |
| Title 1 / Title 2 / Title 3 | 76 / 57 / 48 pt | [HIG] |
| Headline / Callout / Caption 1 / Caption 2 | 38 / 31 / 25 / 23 pt | [HIG] |
| Image scale factors | @1x and @2x | [HIG] |
| System font | SF Pro (New York also available) | [HIG] |

Grid layouts (unfocused content width per column; every grid uses 40 pt horizontal spacing and at least 100 pt vertical spacing):

| Columns | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| Unfocused content width (pt) | 860 | 560 | 410 | 320 | 260 | 217 | 184 | 160 |

- [HIG] The safe insets keep content visible regardless of TV compatibility settings and overscan cropping. Backgrounds and artwork still run edge to edge.
- [HIG] Space rows and columns so a focused item does not overlap its neighbours.
- [HIG] Titled rows need extra vertical space: between the previous row and the title, and between the title and the row's items.
- [HIG] Keep spacing consistent, and make partially hidden offscreen content the same width on both sides of the screen.
- [HIG] Views scroll, but there are no scroll indicators: the system scrolls automatically to keep the focused item visible.
- [HIG] Dynamic Type is supported on tvOS.

Source: https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/scroll-views

## Text entry and search

- [HIG] Minimize text entry. With the Siri Remote, selecting a text field shows a linear keyboard; other input devices get a grid keyboard and the layout adapts automatically.
- [HIG] Numeric codes use a digit entry view, which shows a digit-specific keyboard (tvOS-only component).
- [HIG] Search is a dedicated screen: a keyboard with fully customizable results displayed beneath it.
- [HIG] Offer popular, context-specific and recent search suggestions, because people do not want to type much.
- [HIG] Make sign-in easy and infrequent.
- [Conv] Prefer sign-in flows that avoid typing a password with the remote (for example completing sign-in on another device).
- [HIG] Sliders, steppers, pop-up buttons and pull-down buttons do not exist on tvOS; offer choices as focusable lists or buttons.

Source: https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards, https://developer.apple.com/design/human-interface-guidelines/search-fields, https://developer.apple.com/design/human-interface-guidelines/digit-entry-views, https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos

## Top Shelf

Top Shelf is the area of the Apple TV Home Screen that showcases an app's content when the app is in the Dock and focused.

- [HIG] Prefer full-screen, dynamic content: feature new releases and recommendations, and let people resume playback or jump back into a game.
- [HIG] Do not promote content people already bought, rented or watched. Avoid advertisements and prices; show a price only once people show interest.
- [HIG] Layout templates: carousel actions (full-screen video or images with a title, optional subtitle and two buttons: a primary play button and More Info), carousel details (adds summary and metadata, with the title near the top), sectioned content row (a labeled row of focusable items) and scrolling inset banner (large auto-scrolling images).
- [HIG] Sectioned content row: load enough images to span the screen width and include at least one label.
- [HIG] Scrolling inset banners: provide three to eight images; any text must be in the image (and in its accessibility label), because no labels are shown.
- [HIG] If you do not supply full-screen content, supply at least one static fallback image. It is not focusable, so do not make it look interactive.
- [HIG] Layered images are strongly encouraged, though optional, for Top Shelf and other focusable images.
- [Req] The tvOS app icon must use a layered image.

| Asset | Actual size | Focused / safe zone | Unfocused |
|---|---|---|---|
| Static fallback image | 2320x720 pt | n/a | n/a |
| Poster (2:3) | 404x608 pt | 380x570 pt | 333x570 pt |
| Square (1:1) | 608x608 pt | 570x570 pt | 500x500 pt |
| 16:9 | 908x512 pt | 852x479 pt | 782x440 pt |
| Scrolling inset banner | 1940x692 pt | 1740x620 pt | 1740x560 pt |

- [HIG] Sizes are in points; supply @1x and @2x pixels. The system flips and blurs the static image to fit a width of 1920 pixels at 16:9. Mixed sizes in one row scale up to the tallest image's height.

Source: https://developer.apple.com/design/human-interface-guidelines/top-shelf, https://developer.apple.com/design/human-interface-guidelines/images

## Appearance, images and Liquid Glass

- [HIG] Dark Mode is supported with no tvOS-specific considerations.
- [HIG] Liquid Glass (OS 26+) appears in navigation elements and system experiences such as Top Shelf and Control Center; image views and buttons adopt it when they gain focus.
- [API] Liquid Glass on tvOS requires Apple TV 4K (2nd generation) or newer; older hardware keeps the previous appearance, so check both.
- [API] `UIDesignRequiresCompatibility` is ignored when building for tvOS 27 or later.
- [HIG] Standard materials in the content layer: ultra-thin for full-screen views needing a light scheme; thin for light overlays; regular for overlays; thick for overlays needing a dark scheme.
- [HIG] Use a limited color palette that coordinates with the logo and defers to content.
- [HIG] Layered images have two to five layers; keep an app icon safe zone because focus scaling and motion can crop edges, foreground layers most.

Source: https://developer.apple.com/design/human-interface-guidelines/materials, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/design/human-interface-guidelines/images, https://developer.apple.com/design/human-interface-guidelines/app-icons

## Not available on tvOS

[API] Marked not supported in tvOS: windows, the menu bar, pointing devices, popovers, edit menus, pop-up and pull-down buttons, sliders, steppers, disclosure controls, tab views, panels, drag and drop, undo and redo, web views, printing, widgets, Live Activities, App Shortcuts, status bars, full-screen mode as a pattern, activity views, the Digital Crown, Apple Pencil, Always On.

Source: https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/pointing-devices, https://developer.apple.com/design/human-interface-guidelines/popovers, https://developer.apple.com/design/human-interface-guidelines/widgets, https://developer.apple.com/design/human-interface-guidelines/live-activities, https://developer.apple.com/design/human-interface-guidelines/drag-and-drop

## Common mistakes

| Mistake | Fix |
|---|---|
| Elements that cannot receive focus, or focus traps | Every interactive element focusable and reachable by directional movement |
| Touch metaphors: swipe actions, pull to refresh, hover, an onscreen pointer | Focus plus press; explicit focusable buttons |
| Text or controls inside the overscan margins | Inset primary content 60 pt top/bottom and 80 pt sides |
| Phone-size text (17 pt) and 44 pt controls | 29 pt body, 23 pt minimum; 66 pt default controls |
| Focused items overlapping neighbours or looking blurry | Grid spacing (40 pt, 100 pt minimum); assets for the focused size |
| Focus shown only by a color change | System focus effects: scale, elevation, animation |
| Moving focus programmatically while people browse | Leave focus where people put it |
| Back that pops to an arbitrary "previous" screen or is swallowed | Back opens the parent; Home Screen at top level; pause menu only in gameplay |
| Ignoring Play/Pause during playback, reacting to taps during live video | Honor Play/Pause; respond to presses, not accidental taps |
| Long forms and password entry | Minimize typing; suggestions; easy, infrequent sign-in |
| Custom tab bar height or position | Fixed by the system at 68 pt high, 46 pt from the top |
| Top Shelf used for ads, prices or already-watched content | New and recommended content; resume points |
| Designing widgets, popovers, sliders or a pointer UI for tvOS | Not supported; use focus-friendly alternatives |
