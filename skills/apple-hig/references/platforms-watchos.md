# watchOS (Apple Watch)

Scope: what is specific to designing for Apple Watch: glanceable, brief interactions; vertical navigation anchored to the Digital Crown; toolbar, sheet and input conventions; complications, Smart Stack widgets, notifications and Always On; sizes; and the long list of components that do not exist on the watch.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Device and context
- Inputs
- Navigation model
- Toolbars, sheets and alerts
- Layout, text entry and numbers
- Appearance
- Complications
- Smart Stack widgets and Live Activities
- Notifications
- Always On
- Not available on Apple Watch
- Common mistakes

## Device and context

- [HIG] Small wrist-worn display, usually no more than a foot from the eyes, operated with the opposite hand, often while moving.
- [HIG] Interactions are concise: people glance many times a day and an interaction can last less than a minute.
- [HIG] People frequently use an app's related experiences (complications, notifications, Siri) more than the app itself. Design those first-class, not as afterthoughts.
- [HIG] Aim for quick, glanceable, single-screen interactions that deliver the critical information and allow a targeted action in a gesture or two.
- [HIG] Anticipate needs: use on-device data to surface content relevant now or very soon.
- [HIG] Design the app to function independently of the iPhone; it complements notifications and complications with more detail.
- [API] `WKRunsIndependentlyOfCompanionApp` and `WKWatchOnly` (watchOS 6.0+) declare an independent or watch-only app.
- [HIG] No launch screen is required on watchOS. Avoid loading indicators; show content immediately.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos, https://developer.apple.com/design/human-interface-guidelines/launching, https://developer.apple.com/documentation/bundleresources/information-property-list/wkrunsindependentlyofcompanionapp

## Inputs

- [HIG] Digital Crown: since watchOS 10 it is the primary input for navigation. Turning it scrolls lists and variable-height pages and switches between vertically paginated tabs.
- [Req] Apps cannot respond to presses of the Digital Crown; the system reserves them (for example to show the Home Screen).
- [HIG] Back every Crown interaction with an equivalent touch interaction, and always show visual feedback when the Crown turns, at a rate matched to how fast it turns.
- [HIG] Where navigation is not needed, use the Crown to inspect data (advance a time value, scrub a chart).
- [HIG] Keep the default haptic detents unless they fight your animation; tables can use linear instead of row-based detents when row heights vary a lot.
- [HIG] Touch: standard tap, swipe and drag. The Action button starts an essential action without looking at the screen.
- [HIG] Double tap (watchOS 11 and later): by default it scrolls lists and scroll views and advances vertical tab views. A view may designate one toggle or button as the primary action, in the app or in a widget or Live Activity shown in the Smart Stack.
- [HIG] Do not set a primary action in views that contain lists, scroll views or vertical tabs, because it conflicts with the default double-tap navigation. In a non-scrolling view pick the most-used button (play/pause in media controls).
- [API] `handGestureShortcut(_:isEnabled:)` is watchOS 11.0+.
- [HIG] Haptics have defined meanings: Notification, Up, Down, Success, Failure, Retry, Start, Stop, Click. Use each only for its meaning.
- [HIG] Hardware keyboard shortcuts, pointing devices and the keyboard focus system are not supported.

Source: https://developer.apple.com/design/human-interface-guidelines/digital-crown, https://developer.apple.com/design/human-interface-guidelines/gestures, https://developer.apple.com/design/human-interface-guidelines/playing-haptics, https://developer.apple.com/documentation/swiftui/handgestureshortcut

## Navigation model

- [HIG] Minimize hierarchy depth. Lists, tabs and scroll views are vertically oriented so the Crown moves through them.
- [HIG] There is no tab bar and no sidebar. Peer screens are a vertical tab view: full-screen pages moved with the Crown, with a page indicator next to the Crown showing the number of pages and the current one.
- [API] The vertical paging style is `TabView` with `.verticalPage`, watchOS 10.0+.
- [HIG] Prefer vertical pagination over horizontal pagination or deep hierarchies; give each page one clear purpose and try to keep a page to a single screen height. Put variable-height pages after fixed-height ones where possible.
- [HIG] A split view shows either the list or a detail view full screen. On launch, show the most relevant detail automatically (by location, time or recent actions) instead of the list.
- [HIG] Several detail pages for one item go in a vertical tab view.
- [HIG] Lists: limit the number of rows; show the most relevant items and a way to see more. Keep detail views short if you want vertical page-based navigation between the details of adjacent rows.
- [HIG] Prefer vertically scrolling content; rotating the Crown scrolls a single list or content view.

Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos, https://developer.apple.com/design/human-interface-guidelines/split-views, https://developer.apple.com/design/human-interface-guidelines/page-controls, https://developer.apple.com/design/human-interface-guidelines/scroll-views, https://developer.apple.com/design/human-interface-guidelines/lists-and-tables, https://developer.apple.com/documentation/swiftui/tabviewstyle/verticalpage

## Toolbars, sheets and alerts

- [HIG] Toolbar buttons sit in the top corners or along the bottom (`topBarLeading`, `topBarTrailing`, `bottomBar`); above scrolling content they stay visible while content scrolls beneath. The system moves the time and title to make room.
- [HIG] A scrolling toolbar button (`primaryAction` placement) stays hidden above the content until people scroll up; use it for an important action that is not the view's primary function (compose above an inbox list).
- [HIG] Use toolbar buttons for navigation to related areas or for contextual actions on the view's content.
- [HIG] A sheet is a full-screen view that slides over the content with a blurring, desaturating material behind it. Use one only when a modal task needs a custom title or custom content; keep it brief and occasional; never use a sheet for navigation.
- [HIG] If you change the sheet's default dismiss label, prefer an SF Symbol; text in the top-leading corner that reads like a page title leaves people unable to tell how to dismiss.
- [HIG] For important information or a set of choices, use an alert or an action sheet rather than a sheet.
- [HIG] Action sheets: no more than four buttons including Cancel (so at most three choices). Button styles are default, destructive and cancel.
- [HIG] Do not remove or replace the default material backgrounds of modal sheets.

Source: https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/action-sheets, https://developer.apple.com/design/human-interface-guidelines/materials

## Layout, text entry and numbers

| Item | Value | Tag |
|---|---|---|
| Default / minimum text size | 16 pt / 12 pt | [HIG] |
| Default / minimum control size | 44x44 pt / 28x28 pt | [HIG] |
| Buttons side by side | at most 3 glyph buttons or 2 text buttons in a row | [HIG] |
| Action sheet buttons | at most 4 including Cancel | [HIG] |
| Text enlargement to support | at least 140% | [HIG] |
| Body at the Large Dynamic Type size (default on 40/41/42 mm) | 16 pt, 18.5 pt leading | [HIG] |
| Large Title at the Large size | 36 pt | [HIG] |
| Default Dynamic Type size by case | Small on 38 mm; Large on 40/41/42 mm; xLarge on 44/45/49 mm | [HIG] |
| Dynamic Type range | xSmall to xxxLarge plus AX1 to AX3 | [HIG] |
| Complication line width | 2 pt or greater | [HIG] |
| Smart Stack widget size | from 152x69.5 pt (40 mm) to 198x81.5 pt (49 mm, newest Ultra models) | [HIG] |
| Image scale factor | @2x | [HIG] |
| System font | SF Compact; SF Compact Rounded in complications (New York also available) | [HIG] |

- [HIG] Prefer text buttons that span the full width; two side-by-side buttons with short labels work only if the screen does not scroll, and they should share one height. Inline buttons always use the capsule shape.
- [HIG] Support autorotation only in views people show to someone else (a photo, a QR code).
- [HIG] Present a text field only when necessary; prefer a list of options. A text field shows a keyboard on larger screens and otherwise dictation or Scribble; you cannot choose the keyboard type but can set the content type.
- [HIG] A search field opens a full-screen text input and returns only after Cancel or Search.
- [HIG] The app cannot add entries to the system Settings app. Put a small number of essential options at the bottom of the main view, or use a More menu.
- [HIG] The HIG publishes no screen dimensions for Apple Watch in the layout page; lay out relative to the container and test on the smallest and largest sizes.

Source: https://developer.apple.com/design/human-interface-guidelines/layout, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/buttons, https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards, https://developer.apple.com/design/human-interface-guidelines/settings, https://developer.apple.com/design/human-interface-guidelines/widgets

## Appearance

- [HIG] Dark Mode is not supported on watchOS; there is no light variant to design.
- [HIG] Use background color to support content or carry extra information and to give a sense of place; use materials to show hierarchy.
- [API] Liquid Glass changes on watchOS are minimal and appear on the current release even without rebuilding; to be sure of picking them up, use the standard toolbar APIs and button styles available since watchOS 10. Toolbar buttons take the glass appearance.
- [HIG] Dynamic Type is supported; use text styles.
- [HIG] The app icon is circular; avoid full-screen loading states and indeterminate indicators.

Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode, https://developer.apple.com/design/human-interface-guidelines/color, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass

## Complications

- [HIG] A complication shows timely information on the watch face on every wrist raise; tapping it opens the app.
- [HIG] Since watchOS 9 complications are organized into families: circular (including extra-large layouts), corner, inline and rectangular. Build them with WidgetKit for watchOS 9 and later; ClockKit only for earlier versions.
- [HIG] Show essential, dynamic content. A complication that only launches the app is less valued than one with current data.
- [HIG] Support every family when possible; where a family has nothing useful to show, provide an image that represents the app so the complication can still launch it.
- [HIG] Consider several complications per family, and give each complication its own deep link to the most relevant place in the app.
- [HIG] Tinted mode: the system desaturates and tints text, gauges and images with one color. Never rely on color alone; supply a tinted-mode image when the full-color one desaturates badly.
- [HIG] Choose a gauge style by data: closed for a percentage of a whole, open for an arbitrary range, segmented for rapidly changing values.
- [HIG] Provide static placeholder images for each complication.
- [HIG] Privacy: the face is visible to others with Always On; keep sensitive data out or redactable.
- [HIG] From watchOS 10 a rectangular layout may also appear in the Smart Stack; give it a meaningful background and relevance information.
- [HIG] Offering shareable watch faces that feature your complications helps people discover the app.

Source: https://developer.apple.com/design/human-interface-guidelines/complications, https://developer.apple.com/design/human-interface-guidelines/watch-faces

## Smart Stack widgets and Live Activities

- [HIG] People reach the Smart Stack by turning the Crown on the watch face. Widgets there use a black background by default; a custom background color can carry meaning (red for falling, green for rising values).
- [HIG] Supply relevance information (location, ongoing activity such as a workout) so the system shows or elevates the widget when it is useful.
- [HIG] A Live Activity started on iPhone appears at the top of the Smart Stack on a paired watch, by default combining the leading and trailing elements of the iPhone compact presentation. Tapping opens the watchOS app if there is one.
- [HIG] Consider a custom watchOS layout with more information or a control. The same layout is used in CarPlay, where interactive elements are deactivated, so omit buttons if people are likely to see it while driving.
- [HIG] Show only essential information and significant updates: progress, simple controls, score changes.

Source: https://developer.apple.com/design/human-interface-guidelines/widgets, https://developer.apple.com/design/human-interface-guidelines/live-activities

## Notifications

- [HIG] Two stages: a short look appears briefly on wrist raise (keep it discreet, no sensitive data in the title, never the only carrier of important information); a long look adds detail and can scroll with the Crown.
- [HIG] The long look's structure is fixed: a sash at the top with the app icon and name, your content, your action buttons, and a system Dismiss button at the bottom.
- [HIG] Provide at least a static long-look interface and preferably a dynamic one; the system falls back to static when the dynamic one is unavailable.
- [HIG] Let people act from the notification without opening the app. On supported devices double tap performs the first nondestructive action.

Source: https://developer.apple.com/design/human-interface-guidelines/notifications

## Always On

- [HIG] When the wrist drops the system dims the display and keeps showing the app if it is frontmost or has a background session.
- [HIG] Hide sensitive information (balances, health data); keep useful personal data glanceable when it makes sense (pace and heart rate in a workout).
- [HIG] Keep important content legible and dim secondary text, images and fills; consider removing rich images and large color areas.
- [HIG] Keep the layout stable entering and leaving Always On: show an interactive element as unavailable instead of removing it; make updates infrequent and subtle.
- [HIG] Bring motion to a resting state smoothly instead of stopping it instantly.

Source: https://developer.apple.com/design/human-interface-guidelines/always-on

## Not available on Apple Watch

[HIG] Marked not supported in watchOS: tab bars, sidebars, windows, multitasking, popovers, context menus, edit menus, pop-up and pull-down buttons, segmented controls, steppers, collections, disclosure controls, the menu bar, panels, drag and drop, hardware keyboards and keyboard shortcuts, focus and selection, pointing devices, undo and redo, web views, printing, activity views, status bars, Dark Mode, game controllers, AirPlay and SharePlay.

Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/sidebars, https://developer.apple.com/design/human-interface-guidelines/context-menus, https://developer.apple.com/design/human-interface-guidelines/multitasking, https://developer.apple.com/design/human-interface-guidelines/drag-and-drop, https://developer.apple.com/design/human-interface-guidelines/keyboards

## Common mistakes

| Mistake | Fix |
|---|---|
| Porting the iPhone app screen for screen | Pick the one or two glanceable tasks; build complications and notifications first |
| Tab bar, sidebar, segmented control or context menu | Vertical tab pages, lists, toolbar buttons, a More menu |
| Deep navigation stacks | Shallow hierarchy; open on the most relevant detail |
| Horizontal paging as the main structure | Vertical pages on the Digital Crown |
| Crown-only interaction or no visible response to the Crown | Touch equivalent plus immediate visual feedback |
| Double-tap primary action in a scrolling or paged view | Only in non-scrolling views |
| Three text buttons in a row, tiny tap targets | Full-width buttons; at most 2 text or 3 glyph buttons per row |
| Text fields for input | Lists of options, dictation, sensible defaults |
| Sheets used as navigation; action sheet with five or more buttons | Sheets brief and occasional; four buttons maximum including Cancel |
| Complication that is only an app launcher, or one deep link for all | Live data; a distinct destination per complication |
| Sensitive data visible in Always On, or layout that jumps when dimming | Redact; dim secondary content; keep layout stable |
| Designing light and dark variants | Dark Mode does not exist on watchOS |
| Assuming the iPhone is nearby | Function independently |
| Loading spinners | Show content immediately; update in place |
