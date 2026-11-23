# visionOS (Apple Vision Pro)

Scope: what is specific to designing for Apple Vision Pro: windows, volumes and spaces; eyes and hands input; ornaments, tab bars and toolbars; ergonomics and comfort; sizes; the system glass material (no Liquid Glass APIs, no Dark Mode); immersion styles; and compatible iPad and iPhone apps.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Windows, volumes and spaces
- Eyes and hands
- Navigation, ornaments and toolbars
- Sheets, alerts and menus
- Sizes and spacing
- Ergonomics and comfort
- Materials, color and type
- Immersion
- Other inputs and system behaviours
- Compatible iPad and iPhone apps
- Not available on visionOS
- Common mistakes

## Device and context

- [HIG] A limitless 3D canvas: windows, volumes and 3D objects placed in the wearer's surroundings, with optional deeper immersion.
- [HIG] Apps launch into the Shared Space, where several apps run side by side and people open, close and move windows. An app can move to a Full Space, where it runs alone.
- [HIG] Passthrough shows live video of the surroundings; the Digital Crown adjusts how much is visible. Spatial Audio makes sound seem to come from places in the room.
- [HIG] The system places content relative to the wearer's head whatever their height or posture; content comes to people, so they can stay at rest.
- [HIG] Find the minimum level of immersion that suits each key moment; do not assume every moment should be fully immersive.
- [API] Safety notes Apple states for the device: not for use while operating a vehicle or heavy machinery or while moving around unsafe environments, and designed for people 13 and older.
- [API] No launch screen is required on visionOS.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos, https://developer.apple.com/design/human-interface-guidelines/launching

## Windows, volumes and spaces

| Container | Use for | Key rules |
|---|---|---|
| Window (default style) | Familiar, UI-centric interfaces; 2D content with shallow 3D | Upright plane with the system glass background, close button, window bar, resize controls; can carry a tab bar, toolbar, ornaments |
| Volume (volumetric style) | Bounded 3D content viewed from any angle (a game board, a model) | Controls turn to face the viewer; prefer dynamic scaling unless the object represents a real-world size |
| Immersive space | Unbounded content in a Full Space | See Immersion below |

- [HIG] Keep the window's glass background. Removing it hurts legibility and cohesion; an opaque background blocks surroundings and feels heavy. (A plain window style without glass exists for special cases.)
- [HIG] Default window size is 1280x720 pt; a new window is placed about two meters in front of the wearer, where it appears about three meters wide. Choose an initial size and shape that fit the content and minimize empty area.
- [HIG] Support resizing. Set a minimum and maximum size so the layout never breaks, but do not use them to prevent resizing. Keep content horizontally centered at very large sizes.
- [HIG] Dynamic scale keeps a window's apparent size constant with distance; visionOS defines a point as an angle. Use fixed scale sparingly, for non-interactive objects that should look life-size.
- [HIG] Minimize the depth of 3D content inside a window: the system clips content that extends too far from the surface. Use 3D sparingly in windows and inset it; deeper content belongs in a volume.
- [HIG] Avoid displaying too many windows; they obscure surroundings and make the app cumbersome to move. Prefer a split view to a new window for supplementary information; if a separate view is needed, open an adjacent window rather than using an ornament.
- [HIG] Do not change the appearance of a window's edges: the system feathers the edge of the window people look away from. Only one window is active at a time; the others become more translucent and recede.
- [HIG] Closing a window in the Shared Space sends the app to the background without quitting. Do not pause a window's video because people looked away; expect audio to duck unless the app is the Now Playing app.
- [HIG] Volumes (visionOS 2 and later): a baseplate glow marks the edges when content does not fill the volume; a volume can have a toolbar, tab bar and one extra ornament, not on the same edge as the toolbar or tab bar; pin 2D content with attachments so it reads from any angle.
- [API] `ImmersiveSpace`, `VolumetricWindowStyle` and the `ornament` modifier are visionOS 1.0+ only.

Source: https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/spatial-layout, https://developer.apple.com/design/human-interface-guidelines/multitasking, https://developer.apple.com/documentation/swiftui/immersivespace

## Eyes and hands

- [HIG] Primary interaction: look at an element to target it, then make an indirect gesture such as a tap (finger and thumb together) with a hand resting anywhere. Indirect gestures work at any distance with minimal movement.
- [HIG] Direct gestures (touching content with a finger) suit nearby objects and short, infrequent use; raised arms tire quickly. Standard components accept both; offer both where possible and prefer indirect for UI.
- [HIG] Looking at an interactive element shows the system hover effect. Some components expand when looked at (a tab bar reveals labels; a button can reveal a tooltip).
- [API] The system does not tell the app where people are looking before they tap. No design may depend on gaze position; hover effects run outside the app's process.
- [HIG] Custom hover effects define two appearances the system switches between; they cannot run code. Use them rarely, keep at least one primary view unchanged between states, and pick a delay: none for subtle affordances, short for quick expansion, long for extra information. Buttons do not support custom hover effects.
- [HIG] A multi-part interactive component needs one containing shape the system can highlight.
- [HIG] Support the standard gestures everywhere; tap is the first thing people try. Always give people multiple ways to interact, including accessibility features.
- [HIG] Custom gestures require a Full Space and permission to access hand data. Keep them comfortable, avoid requiring both hands or a specific hand, and never require specific body movements or positions without an alternative.
- [HIG] The area around the hand is reserved for system overlays (Home and Control Center, visionOS 2 and later): avoid anchoring content to hands or wrists, and avoid custom gestures that roll the hand, wrist and forearm.

Source: https://developer.apple.com/design/human-interface-guidelines/eyes, https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/buttons

## Navigation, ornaments and toolbars

- [HIG] The tab bar is always vertical, floating at a fixed position on the window's leading side. It expands when looked at and can briefly cover content behind it.
- [HIG] Every tab needs a symbol and a short text label: the symbol is always visible, the label appears on expansion.
- [HIG] For deep hierarchies use a sidebar inside a tab, and never let a sidebar selection change the current tab.
- [HIG] The system toolbar appears along the bottom edge of the window, above the window-management controls, slightly in front of the window. Items can be a symbol or a text label; looking at a symbol reveals its label.
- [HIG] Prefer the system toolbar. Avoid vertical toolbars (tab bars are vertical) and avoid pull-down menus in the toolbar (they can cover the window controls below).
- [HIG] Try not to let a window resize narrower than its toolbar: there is no menu bar listing all actions, so the toolbar must stay reliable.
- [HIG] Ornaments float in a plane parallel to and slightly in front of their window, move with it and do not scroll with content. Tab bars, toolbars and playback controls are system ornaments; do not rebuild those by hand.
- [HIG] Use custom ornaments for frequently needed controls or information in a consistent place; keep them visible in general (hiding is fine while people watch a video or view a photo).
- [HIG] Keep an ornament the same width as its window or narrower; limit the number of ornaments for visual balance; consider borderless buttons, since the ornament background is glass.
- [HIG] Page controls show position only; people do not interact with them. Scrolling: the indicator is small and fixed-size at a predictable edge. Add Look to Scroll to reading and browsing views (it is off by default), not to dense control views, and apply it consistently.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/ornaments, https://developer.apple.com/design/human-interface-guidelines/sidebars, https://developer.apple.com/design/human-interface-guidelines/page-controls, https://developer.apple.com/design/human-interface-guidelines/scroll-views

## Sheets, alerts and menus

- [HIG] A sheet floats in front of its parent window, which dims. Do not make it emerge from the window's bottom edge; center it in the field of view. Do not let it cover most or all of the window; resizing may be allowed.
- [HIG] Alerts appear in front of the app's window, slightly forward on the z-axis, and stay anchored to the window if it moves. In a Full Space they are centered in the field of view.
- [HIG] An alert accessory view is at most 154 pt high with a 16 pt corner radius.
- [API] Action sheets are not supported on visionOS.
- [HIG] Prefer a context menu to a panel or inspector window for frequent functions; keep its height within the window's height.
- [HIG] There is no menu bar. With a hardware keyboard, holding Command shows a shortcut interface organized into the familiar categories (File, Edit, View) that lists only commands that have shortcuts, flat, without submenu titles: write shortcut titles that stand on their own.

Source: https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/alerts, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/context-menus, https://developer.apple.com/design/human-interface-guidelines/keyboards

## Sizes and spacing

| Item | Value | Tag |
|---|---|---|
| Default / minimum control size | 60x60 pt / 28x28 pt | [HIG] |
| Button hit region | at least 60x60 pt | [HIG] |
| Spacing between interactive items | centers at least 60 pt apart, or a margin of at least 16 pt around each | [HIG] |
| Padding around buttons 60 pt or larger | 4 pt | [HIG] |
| Button sizes | mini 28, small 32, regular 44, large 52, extra large 64 pt | [HIG] |
| Default / minimum text size | 17 pt / 12 pt | [HIG] |
| Default window | 1280x720 pt, placed about 2 m away | [HIG] |
| Comfortable distance for sustained reading | at least 1 m | [HIG] |
| Alert accessory view | 154 pt maximum height, 16 pt corner radius | [HIG] |
| Boundary in progressive and full immersion | about 1.5 m from the initial head position | [HIG] |
| Progressive immersion range (default); widget scaling by the wearer | 120 to 360 degrees; 75 to 125 percent | [HIG] |
| Image scale factor | @2x or higher | [HIG] |

- [Conv] Read the two numbers together: a regular button is drawn 44 pt, while 60 pt is the hit region and center spacing, so the extra area comes from the space around the control.
- [HIG] Do not let controls overlap other interactive elements or views.
- [HIG] Give interactive items rounded shapes (circle, capsule, rounded rectangle): eyes are drawn to corners, which makes the center harder to hold.
- [HIG] Prefer buttons with a visible background shape and fill, except in toolbars, context menus, alerts and ornaments. Never make a custom button with a white fill and black content: that style means "toggled on".
- [HIG] Icon-only buttons are circles; text-only buttons are rounded rectangles or capsules; use rounded rectangles in vertical stacks and capsules in horizontal rows.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/eyes, https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/immersive-experiences, https://developer.apple.com/design/human-interface-guidelines/widgets

## Ergonomics and comfort

- [HIG] Keep content within the field of view and centered; do not make people turn their head or change position to interact. The system gives the app no information about the field of view.
- [HIG] Do not anchor content to the wearer's head: it feels confining, hides passthrough and blocks assistive technologies such as Pointer Control. Anchor content in the person's space.
- [HIG] Prefer horizontal layouts to vertical ones that strain the neck; avoid demanding attention in different places in quick succession or across several depths.
- [HIG] Place content people read or use for a while at least one meter away; keep very close content brief.
- [HIG] Let people use the app with minimal or no physical movement and with hands resting in their lap or at their sides.
- [HIG] Motion: avoid motion at the edges of the field of view; avoid sustained oscillation, especially around 0.2 Hz; do not rotate the virtual world (fade and change direction instantly); provide a stationary frame of reference; fade objects out and in to relocate them; reduce contrast or add translucency for large moving objects.
- [HIG] Depth: use it for hierarchy on large elements, not small ones; avoid depth on text; do not change depth often, since refocusing is tiring.
- [HIG] Minimize visual distraction: do not reveal content next to a control someone is looking at, and avoid repeating patterns or textures that fill the field of view.

Source: https://developer.apple.com/design/human-interface-guidelines/spatial-layout, https://developer.apple.com/design/human-interface-guidelines/eyes, https://developer.apple.com/design/human-interface-guidelines/motion, https://developer.apple.com/design/human-interface-guidelines/accessibility

## Materials, color and type

- [HIG] Windows use an unmodifiable system material called glass that lets light, surroundings and virtual content show through and adapts its brightness to what is behind it.
- [HIG] There is no Dark Mode on visionOS: do not design light and dark variants. System colors use their dark values.
- [API] The glass effect and glass button style APIs (`glassEffect(_:in:)`, `GlassEffectContainer`, `buttonStyle(.glass)`; 26.0 on other platforms) list no visionOS availability, and Apple's adoption guide names iOS, iPadOS, macOS, tvOS and watchOS only. Some other OS 26 APIs do list visionOS 26 (`references/implementation-availability.md`). Do not apply Liquid Glass material guidance or those APIs to visionOS; use the system glass and materials.
- [HIG] Prefer translucency to opaque colors in windows. For custom components: thin material for interactive elements and selected items, regular to separate sections such as a sidebar, thick for a dark element on a regular background.
- [HIG] Vibrancy has three levels: label for standard text, secondary label for descriptive text, tertiary label for inactive elements only.
- [HIG] Use color sparingly, especially on glass; prefer it in bold text and large areas. In full immersion keep brightness balanced and avoid bright objects on very dark backgrounds.
- [HIG] Text is white by default for contrast on glass; test any other color in several contexts. Prefer 2D text; make text without a background bold rather than adding shadows; billboard text attached to points in space so it faces the wearer.
- [HIG] SF Pro is the system font, with bolder Body and Title styles and two extra styles, Extra Large Title 1 and 2. Dynamic Type is supported.
- [HIG] Standard controls play sound feedback; the system plays no haptics, so audible feedback matters.

Source: https://developer.apple.com/design/human-interface-guidelines/materials, https://developer.apple.com/design/human-interface-guidelines/dark-mode, https://developer.apple.com/design/human-interface-guidelines/color, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/documentation/swiftui/glass

## Immersion

| Style | What people see | System boundary |
|---|---|---|
| Shared Space (windows, volumes; optional dimmed or tinted passthrough) | The app beside other apps | None |
| `mixed` (Full Space) | Unbounded app content blended with passthrough; other apps hidden | None; nearby content turns semi-opaque when people approach physical objects |
| `progressive` (Full Space) | A custom environment partly replacing passthrough; the Crown adjusts the amount | About 1.5 m |
| `full` (Full Space) | A 360-degree environment replacing passthrough | About 1.5 m |

- [HIG] Prefer launching in the Shared Space, or in `mixed`; even a fully immersive app should consider opening a window first with a control to enter immersion.
- [HIG] Reserve immersion for meaningful moments. Let people choose when to enter and exit with a clear control; never require system controls to get out. Label whether an exit returns to a less immersive context or quits the experience, and make transitions between styles smooth and predictable.
- [HIG] Do not use `progressive` or `full` if people may need to move beyond the 1.5 m boundary; as the head nears it the experience fades and passthrough returns. Do not encourage movement in those styles; bring objects to people.
- [HIG] In `mixed`, do not obscure passthrough too much; if content would, use `progressive` or `full` instead.
- [Req] Access to surroundings or hand data (ARKit) requires asking for permission.
- [HIG] Environments: keep animation subtle, avoid movement near the edges of the field of view, make them expansive, always provide a ground plane, avoid flat 360-degree images, and lower or stop the soundscape when other audio plays.
- [HIG] Virtual hands should match the real hands' position and gestures; fade them out to reveal real hands if tracking is interrupted.

Source: https://developer.apple.com/design/human-interface-guidelines/immersive-experiences, https://developer.apple.com/design/human-interface-guidelines/launching

## Other inputs and system behaviours

- [API] The Digital Crown is system-only on Apple Vision Pro (volume, immersion amount, recentering, Accessibility settings, Home View); apps receive no Crown input.
- [HIG] With a connected keyboard or game controller, the same focus system as iPadOS and tvOS applies. It is separate from the gaze hover effect.
- [HIG] With an attached pointing device, where people look sets the pointer's context; the pointer hides during gestures. No app work is needed.
- [HIG] The virtual keyboard appears in its own movable window; layouts need not make room for it. A physical keyboard brings a typing-completion overlay.
- [HIG] Widgets are 3D objects people place on horizontal or vertical surfaces and that persist there. Design for two distance thresholds (simplified far, default near), two mounting styles (elevated, the default; recessed, vertical surfaces only) and two treatments (paper, glass).
- [HIG] Drag and drop: handle content dropped into empty space by opening a window for it. Accessibility features include VoiceOver, Switch Control, Dwell Control, Guided Access, head and hand Pointer Control and Zoom.

Source: https://developer.apple.com/design/human-interface-guidelines/digital-crown, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/pointing-devices, https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards, https://developer.apple.com/design/human-interface-guidelines/widgets, https://developer.apple.com/design/human-interface-guidelines/drag-and-drop

## Compatible iPad and iPhone apps

- [API] A compatible app links the iOS SDK and runs on visionOS unmodified ("Designed for iPad" destination); it keeps its iPadOS or iOS appearance and appears in a window in the person's surroundings. Only a build against the visionOS SDK gets the standard visionOS appearance, 3D content and immersion.
- [API] Unavailable to compatible apps: Core Motion services, barometer and magnetometer data, location services other than the standard service, HealthKit data, video and still capture from device cameras.
- [API] visionOS does not load App Clips, keyboard extensions, Messages extensions or widgets from compatible apps, ignores bundled watchOS apps, has no Picture in Picture and hides AirPlay; ActivityKit (Live Activities) is iOS-only.
- [API] Handle missing features gracefully: availability checks, error handling, and removing or explaining feature-specific views instead of leaving them empty.
- [API] Less suitable app types: containers for extensions, turn-by-turn navigation, camera-centric apps. Availability on Apple Vision Pro can be turned off in App Store Connect.
- [Conv] For a compatible app, give iPad guidance (`references/platforms-ipados.md`) and say that visionOS conventions such as ornaments need a native visionOS destination.

Source: https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos, https://developer.apple.com/documentation/visionos/determining-whether-to-bring-your-app-to-visionos, https://developer.apple.com/documentation/visionos/bringing-your-app-to-visionos

## Not available on visionOS

[API] Marked not supported in visionOS: Dark Mode, action sheets, the menu bar, status bars, panels, tab views, full-screen mode, Live Activities, Mac Catalyst, Apple Pencil, remotes and Top Shelf, complications, Always On, controls (Control Center controls), App Clips, Home Screen quick actions. [API] The glass effect and glass button style APIs (`glassEffect`, `GlassEffectContainer`, `buttonStyle(.glass)`) list no visionOS availability.

Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/design/human-interface-guidelines/going-full-screen, https://developer.apple.com/design/human-interface-guidelines/live-activities

## Common mistakes

| Mistake | Fix |
|---|---|
| iPhone-density UI: 44 pt targets packed tightly | 60 pt target areas, 16 pt margins, rounded shapes |
| Opaque full-window backgrounds or removing glass | Keep the glass background; use materials and vibrancy |
| Light and dark themes, or Liquid Glass APIs | No Dark Mode; system glass only |
| Head-locked HUDs or content that follows the head | Anchor in space; rely on recentering |
| Logic that depends on where the user is looking | Not available; use tap events and system hover effects |
| Bottom-edge sheets, vertical toolbars, pull-down menus in the toolbar | Centered sheets; system bottom toolbar; system vertical tab bar |
| Supplementary content in ornaments; many windows | Adjacent window or split view; few windows |
| Launching straight into full immersion with no exit | Start in the Shared Space; clear enter and exit controls |
| Motion at the periphery, world rotation, oscillation | Centered, subtle motion; fades; stationary frame of reference |
| Requiring raised arms, both hands, a specific hand or walking | Indirect gestures first; alternatives for every custom gesture |
| 3D depth on text and small controls; deep 3D inside a window | 2D text; depth for large elements; volumes for deep content |
| Blocking window resizing with equal minimum and maximum sizes | Allow resizing within sensible limits |
| Treating a "Designed for iPad" app as native visionOS | Check the destination; apply iPad guidance or add a visionOS target |
