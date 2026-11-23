# 02 — Apple platform specifics (iOS, iPadOS, macOS, watchOS, tvOS, visionOS)

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Research date 2026-11-23. Agent 2 (platform specialist).

**Source convention.** `HIG:<slug>` = `https://developer.apple.com/design/human-interface-guidelines/<slug>`
(fetched as `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`).
`DOC:<path>` = `https://developer.apple.com/documentation/<path>` (fetched as `/tutorials/data/documentation/<path>.json`).
**[V]** = fetched this session and the source says it. **[M]** = memory / not verified.
Strength: **REQ** = hard requirement / API contract / HIG "must"; **REC** = HIG recommendation; **CONV** = community convention.
Unless marked REQ, every HIG item below is REC.

---

## 0. Headline findings (read these first)

| # | Finding | Tag | Source |
|---|---|---|---|
| 1 | OS numbering is year-based: Liquid Glass APIs are `introducedAt` **26.0** on iOS/iPadOS/macOS/tvOS/watchOS (`glassEffect`, `Glass`, `TabBarMinimizeBehavior`, `backgroundExtensionEffect`); the newest APIs are **27.1** (`ArrangementView`, `ReservedRegion`, `ToolbarVerticalCompressionBehavior`). Current cycle = OS 27. Older refs in the HIG still use old numbers (iOS 18, watchOS 10/11, visionOS 2, macOS 14). | [V] | DOC:swiftui/glass, DOC:swiftui/arrangementview, DOC:swiftui/reservedregion |
| 2 | **New form factor: iPhone Duo** (foldable, two displays, hinge). HIG page added 2026-09-09. Outer display = compact width, inner = regular width; bars move to the **side** (vertical toolbars/tab bars) except inner display in portrait; "reserved regions" (cameras, fold). It is still iOS: "you're still designing for iPhone". | [V] | HIG:designing-for-iphone-duo |
| 3 | **macOS now has touch input** ("a Mac with a touch display"), added to HIG 2026-10-28. Touch is *secondary*: keep layout/control size the same, enlarge tap targets not controls, never touch-only. | [V] | HIG:designing-for-macos (change log), HIG:gestures, HIG:pointing-devices |
| 4 | **iPadOS has a menu bar** and freely resizable windows with window controls (leading edge of toolbar); user chooses Full screen vs Windowed in Multitasking & Gestures settings. `UIRequiresFullScreen` is **deprecated**. | [V] | HIG:the-menu-bar, HIG:windows, HIG:multitasking, DOC:bundleresources/information-property-list/uirequiresfullscreen |
| 5 | **iPadOS tab bar is at the top**, optionally convertible to a sidebar (`sidebarAdaptable`, iOS/iPadOS 18.0, macOS 15.0, tvOS 18.0, visionOS 2.0). HIG says "Prefer a tab bar for navigation" / "Consider using a tab bar first". | [V] | HIG:tab-bars, HIG:sidebars, DOC:swiftui/tabviewstyle/sidebaradaptable |
| 6 | "Navigation bar" is no longer a separate HIG component: merged into **Toolbars** (2025-06-09). "In iOS, a navigation-specific toolbar is sometimes called a navigation bar." Slug `navigation-bars` is gone from the TOC. | [V] | HIG:toolbars |
| 7 | Liquid Glass: iOS, iPadOS, macOS, tvOS, watchOS get it via standard components. visionOS is **not** in the list and `glassEffect`/`Glass` have no visionOS availability; visionOS keeps its own "glass" window material. watchOS changes are "minimal". tvOS only on Apple TV 4K (2nd gen)+. | [V] | DOC:technologyoverviews/adopting-liquid-glass, DOC:swiftui/view/glasseffect(_:in:), HIG:materials |
| 8 | `UIDesignRequiresCompatibility` (opt out of the new design) is **ignored when building for OS 27+**. No more opt-out. | [V] | DOC:bundleresources/information-property-list/uidesignrequirescompatibility |
| 9 | Dark Mode exists on iOS, iPadOS, macOS, tvOS only. "Dark Mode isn't supported in visionOS or watchOS." Dynamic Type exists on iOS, iPadOS, tvOS, visionOS, watchOS; "macOS doesn't support Dynamic Type." | [V] | HIG:dark-mode, HIG:typography |
| 10 | Another new device appears in the HIG: **Apple HomeView** (household display; widgets on a Modular face and Home Screen, small system family). Mentioned only in HIG:widgets (2026-10-13). No "Designing for" page; treat as out of scope but do not be surprised by it. | [V] | HIG:widgets |

Current "Designing for …" pages in the TOC: `designing-for-ios`, `-ipados`, `-macos`, `-tvos`, `-visionos`, `-watchos`, `-games`, `-iphone-duo` [V] (HIG:getting-started).

---

## 1. Numbers that differ per platform (all [V])

| | iOS / iPadOS | macOS | tvOS | visionOS | watchOS | Source |
|---|---|---|---|---|---|---|
| Default / minimum text size | 17 / 11 pt | 13 / 10 pt | 29 / 23 pt | 17 / 12 pt | 16 / 12 pt | HIG:typography, HIG:accessibility |
| Default / minimum control size | 44x44 / 28x28 pt | 28x28 / 20x20 pt | 66x66 / 56x56 pt | 60x60 / 28x28 pt | 44x44 / 28x28 pt | HIG:accessibility, HIG:designing-for-games |
| Button hit region rule | "at least 44x44 pt" | (table above) | (table above) | "60x60 pt" | (table above) | HIG:buttons |
| Viewing distance | iPhone "no more than a foot or two"; iPad "within about 3 feet" | stationary, desk | "often 8 feet or more" | windows placed ~2 m away; keep reading content ≥1 m | "no more than a foot" | each HIG:designing-for-* ; HIG:windows; HIG:eyes |
| System font | SF Pro (+NY) | SF Pro (NY only via Catalyst) | SF Pro (+NY) | SF Pro (bolder body/title styles; Extra Large Title 1/2) | SF Compact (SF Compact Rounded in complications) | HIG:typography |
| Body style at default size | 17/22 | 13/16 | 29/36 (Medium weight) | 17 | 16/18.5 (Large; default for 40–42 mm), 17 (xLarge; 44/45/49 mm), 15 (Small; 38 mm) | HIG:typography specs |
| Large Title default | 34 | 26 | Title 1 = 76 | Extra Large Title styles exist | 36 (Large) | HIG:typography specs |
| Dynamic Type | Yes (xSmall…xxxLarge + AX1–AX5) | **No** | Yes | Yes | Yes (xSmall…xxxLarge + AX1–AX3) | HIG:typography |
| Dark Mode | Yes | Yes | Yes | **No** (glass adapts) | **No** | HIG:dark-mode, HIG:materials |
| Safe-area / margin numbers | use system safe areas; Dynamic Island; Duo reserved regions | avoid bottom of window; avoid camera housing | **60 pt top/bottom, 80 pt sides** (overscan) | default window 1280x720 pt; button centers ≥60 pt apart, ≥16 pt margin | ≤3 glyph buttons or ≤2 text buttons per row | HIG:layout, HIG:windows, HIG:eyes |

Spacing rule that is cross-platform: about 12 pt padding around bezeled elements, about 24 pt around non-bezeled [V] (HIG:accessibility). Contrast: 4.5:1 up to 17 pt, 3:1 at 18 pt+ [V] (HIG:accessibility; full table has more rows).

tvOS fixed numbers [V]: tab bar height 68 pt, top edge 46 pt from screen top, not changeable (HIG:tab-bars). Grid widths with 40 pt horizontal spacing and ≥100 pt vertical spacing: 2 col 860, 3 col 560, 4 col 410, 5 col 320, 6 col 260, 7 col 217, 8 col 184, 9 col 160 pt (HIG:layout). Top Shelf static fallback is fitted to a 1920 pt width (HIG:top-shelf).
visionOS fixed numbers [V]: alert accessory view max height 154 pt, 16 pt corner radius (HIG:alerts); button sizes mini 28, small 32, regular 44, large 52, extra large 64 pt; add 4 pt padding around buttons ≥60 pt (HIG:buttons); approx 1.5 m boundary in progressive/full immersion (HIG:immersive-experiences); avoid sustained oscillation near 0.2 Hz (HIG:motion).

---

## 2. Per-platform profiles

### 2.1 iOS (iPhone, including iPhone Duo)
- **Device**: medium-size high-res display, held in one or both hands, portrait and landscape, 1–2 ft [V] HIG:designing-for-ios.
- **Input**: Multi-Touch gestures, virtual keyboards, voice; gyro/accelerometer; Game controller optional [V] HIG:designing-for-ios, HIG:designing-for-games.
- **Navigation / containers**: tab bar floats at the **bottom** on Liquid Glass; can minimize on scroll with an accessory (MiniPlayer pattern); dedicated search tab at trailing end [V] HIG:tab-bars. Top toolbar (the "navigation bar") with large title that collapses on scroll; put only essential items in the bar, rest in a More menu [V] HIG:toolbars. Use standard Back/Close symbols, not text labels "Back"/"Close" [V] HIG:toolbars. Split view only in regular width [V] HIG:split-views.
- **Search**: three entry points: tab in tab bar (standard tab or button appearance), toolbar (bottom preferred "if there's room", else top), or inline [V] HIG:search-fields.
- **Modality**: sheets with detents (system: large, medium; custom allowed); include grabber for resizable sheets; support swipe-to-dismiss; Cancel leading, Done trailing in single-view sheets [V] HIG:sheets. Use action sheet (not alert) for choices tied to an intentional action; avoid scrolling alerts/action sheets [V] HIG:alerts, HIG:action-sheets. Avoid popovers in compact width; use a sheet [V] HIG:popovers.
- **Multitasking**: app switching plus Picture in Picture / FaceTime [V] HIG:multitasking. On Duo: Split View multitasking on the inner display [V] HIG:designing-for-iphone-duo.
- **System conventions**: widgets (Home/Lock Screen, StandBy), Home Screen quick actions, Spotlight, Shortcuts, activity views, Live Activities / Dynamic Island [V] HIG:designing-for-ios, HIG:widgets.
- **Ergonomics**: controls in middle/bottom are easier to reach; support swipe-back and row swipe actions [V] HIG:designing-for-ios.
- **Does not exist**: windows ("Not supported in iOS, tvOS, or watchOS"), menu bar, panels, focus system (keyboard focus "Not supported in iOS or watchOS"), tab *views* (use segmented control) [V] HIG:windows, HIG:the-menu-bar, HIG:panels, HIG:focus-and-selection, HIG:tab-views.
- **iPhone Duo rules** [V] HIG:designing-for-iphone-duo: design with size classes, margins, safe areas; no fixed widths; keep state/functionality identical across displays; do not override default side bar placement; give every toolbar item a title and a symbol; prefer symbols (text buttons stay in a horizontal bar); use `ToolbarItemGroup`, visibility priority and the *system* overflow menu (reserve ellipsis for overflow); even number of grid columns; keep navigation containers outside `ArrangementView`. Side controls stay on the same physical side in RTL.
- **Liquid Glass**: tab bars, toolbars, sidebars float in the glass layer; do not put glass in the content layer; use scroll edge effect instead of opaque bar backgrounds; extend backgrounds under bars [V] HIG:materials, HIG:layout.

### 2.2 iPadOS
- **Device**: large display; held, on a surface or stand; within about 3 ft [V] HIG:designing-for-ipados.
- **Input**: touch, virtual keyboard, hardware keyboard, pointer (trackpad/mouse), Apple Pencil, voice, often combined [V]. The pointer "doesn't replace touch" [V] HIG:pointing-devices.
- **Navigation**: tab bar "near the top of the screen"; fixed (`tabBarOnly`) or convertible to sidebar (`sidebarAdaptable`); prefer a tab bar, offer the sidebar for complex apps; user customization with ≤5 default tabs to match compact [V] HIG:tab-bars. Sidebar-only = `NavigationSplitView`/`UISplitViewController` [V] HIG:sidebars. Toolbar and tab bar can share the same top row [V] HIG:toolbars. Split views of 2 or 3 columns; design for narrow, compact and intermediate widths [V] HIG:split-views.
- **Windowing**: Full screen or Windowed (user setting); windows fluidly resizable to a minimum size; window controls at the leading edge of the toolbar, so move leading toolbar buttons inward; apps cannot detect or control the multitasking configuration; system remembers window size/placement [V] HIG:windows, HIG:multitasking, DOC:technologyoverviews/adopting-liquid-glass. Offer "open in new window" via context menu or File menu; pinch-to-open-window gesture [V] HIG:windows.
- **Menu bar**: revealed by moving the pointer to the top edge or swiping down; same menu order as Mac; because it is often hidden, every function must also be reachable in the UI; `AppName > Settings` is reserved for the app's page in iPadOS Settings; add tabs to the View menu with key bindings; use more submenus (rows are taller) [V] HIG:the-menu-bar.
- **Focus**: keyboard focus system since iPadOS 15: Tab moves between focus groups, arrows within a group; halo (focus ring) for fields, highlight for lists; only content elements need focus, not buttons/sliders [V] HIG:focus-and-selection.
- **Modality**: prefer page/form sheet styles; popovers fine in regular width; context menus on long press or secondary click, including on empty areas to create objects [V] HIG:sheets, HIG:popovers, HIG:context-menus.
- **Search**: trailing side of toolbar, or top of sidebar, or dedicated sidebar/tab item; do not auto-focus the field when only the virtual keyboard is available [V] HIG:search-fields.
- **Best practices**: minimize modality and full-screen transitions; density from viewing distance and input mode; adapt to orientation, multitasking, Dark Mode, Dynamic Type; "transition effortlessly to running in macOS" [V] HIG:designing-for-ipados.
- **Does not exist**: panels; digital crown; HIG says the menu bar may be hidden so do not make it the only path [V].

### 2.3 macOS
- **Device**: large display, multiple displays, Sidecar; stationary at a desk; optional touch display (brief, intentional touches) [V] HIG:designing-for-macos.
- **Input**: keyboard and pointing device primary; trackpad gestures, touch (secondary), Siri, Voice Control, game controller [V].
- **Navigation / containers**: sidebar (small/medium/large row sizes following the user's General setting) and split views with resizable dividers (prefer thin 1 pt divider; min/max pane sizes; hideable panes with toolbar button plus menu command plus shortcut) [V] HIG:sidebars, HIG:split-views. Toolbar lives in the window frame; items have no bezel; "Make every toolbar item available as a command in the menu bar" [V] HIG:toolbars. Tab views (not tab bars) for in-pane switching; panels and inspectors; outline views for hierarchy; sortable/resizable table columns [V] HIG:tab-views, HIG:panels, HIG:lists-and-tables.
- **Menu bar** (essential): order `AppName, File, Edit, Format, View, app-specific, Window, Help`; always show the same items and disable rather than hide; provide Window menu even with one window (Minimize, Zoom); provide View menu even for only Enter Full Screen; support standard shortcuts [V] HIG:the-menu-bar.
- **Settings**: own Settings window opened from the App menu (Command-Comma); no settings button in the toolbar; non-customizable toolbar of panes; dim minimize/zoom; title = pane name; restore last pane [V] HIG:settings.
- **Windows**: main / key / inactive states with distinct system appearances; people resize, move, minimize, full-screen; never custom window chrome; avoid controls or critical info at the **bottom** of windows or sidebars (often off-screen); avoid content behind the camera housing [V] HIG:windows, HIG:layout, HIG:sidebars. Full screen: use system support, user decides, Control-Command-F [V] HIG:going-full-screen.
- **Modality**: sheets are cards attached to the parent window; other app windows stay usable; alerts show the app icon, can have suppression checkbox, accessory view, Help button; popovers can detach into panels; use a panel for repeated input (Find) [V] HIG:sheets, HIG:alerts, HIG:popovers.
- **Other conventions**: context menus on every object (Catalyst page: "Mac users tend to expect every object … to offer a context menu"); drag to Finder; drag from inactive windows; Dock menus; expansion tooltips; app accent color is overridden by the user's accent choice; desktop tinting [V] HIG:mac-catalyst, HIG:drag-and-drop, HIG:color, HIG:dark-mode.
- **Touch on Mac** [V] HIG:gestures, HIG:pointing-devices: keep layout stable across inputs; enlarge tap targets, optionally expand controls on touch; reveal hover-only controls on tap and also offer them in a context menu; custom gestures must work on both touch and trackpad.
- **Does not exist**: Dynamic Type, status bars, page controls, virtual keyboards, action-sheet specifics, haptics except Magic Trackpad (3 patterns via `NSHapticFeedbackPerformer`) [V] HIG:typography, HIG:status-bars, HIG:page-controls, HIG:virtual-keyboards, HIG:playing-haptics.

### 2.4 watchOS
- **Device**: small wrist display, ≤1 ft, Always On when wrist is down; interactions under a minute; complications, notifications and Siri are used more than the app itself [V] HIG:designing-for-watchos.
- **Input**: Digital Crown (primary navigation since watchOS 10; apps cannot respond to Crown *presses*), tap/swipe/drag, Action button, double tap (watchOS 11+, Series 9+/Ultra 2+; do not set a primary action in views with lists/scroll/vertical tabs), dictation/Scribble/keyboard on larger screens [V] HIG:digital-crown, HIG:gestures, HIG:virtual-keyboards.
- **Navigation**: shallow hierarchy; vertically oriented lists, vertical tab views (`verticalPage`, watchOS 10.0) with page indicator next to the Crown; `NavigationSplitView` shows list *or* detail full screen and should open on the most relevant detail [V] HIG:split-views, HIG:tab-views, DOC:swiftui/tabviewstyle/verticalpage. Toolbar buttons in top corners or bottom (`topBarLeading`, `topBarTrailing`, `bottomBar`), or a scrolling `primaryAction` button revealed at top [V] HIG:toolbars.
- **Modality**: sheets are full-screen with a material background, brief and occasional, never for navigation; action sheets max 4 buttons including Cancel [V] HIG:sheets, HIG:action-sheets.
- **Layout**: ≤3 glyph buttons or ≤2 text buttons side by side; full-width text buttons preferred; autorotate only for content shown to others; avoid black icon background; limit list rows; prefer option lists over text entry [V] HIG:layout, HIG:app-icons, HIG:lists-and-tables, HIG:text-fields.
- **System surfaces**: complications (WidgetKit accessory families since watchOS 9; support all families; distinct deep link each), Smart Stack widgets, Live Activities from iPhone appear at top of Smart Stack, short-look / long-look notifications, Always On (redact sensitive data, dim secondary content, keep layout stable) [V] HIG:complications, HIG:live-activities, HIG:notifications, HIG:always-on.
- **Haptics**: named set (Notification, Up, Down, Success, Failure, …); Crown detents [V] HIG:playing-haptics.
- **Does not exist**: tab bars, sidebars, popovers, context menus, edit menus, windows, multitasking, Dark Mode toggle, drag and drop, hardware-keyboard shortcuts, custom entries in the Settings app (put a few options at the bottom of the main view or in a More menu) [V] HIG:tab-bars, HIG:sidebars, HIG:popovers, HIG:context-menus, HIG:edit-menus, HIG:multitasking, HIG:drag-and-drop, HIG:keyboards, HIG:settings.
- **Independence**: "Design your app to function independently" [V] HIG:designing-for-watchos. `WKRunsIndependentlyOfCompanionApp`, `WKWatchOnly` keys exist (watchOS 6.0) [V].
- **Liquid Glass**: minimal changes, automatic even without rebuilding; adopt standard toolbar APIs and button styles from watchOS 10 [V] DOC:technologyoverviews/adopting-liquid-glass.

### 2.5 tvOS
- **Device**: very large display viewed from 8 ft or more; long, immersive sessions; shared, multiuser device [V] HIG:designing-for-tvos.
- **Input**: Siri Remote (clickpad touch surface: swipe changes focus, press activates; Back; Play/Pause), game controller, voice, other devices; keyboard/mouse/trackpad as additional [V] HIG:remotes, HIG:designing-for-games.
- **Focus engine**: directional focus reaches *every* element; focused items scale up, so leave padding and supply larger assets; five states (unfocused, focused, highlighted, selected, unavailable); never move focus without interaction; "Avoid displaying a pointer"; do not use color alone for focus; in full-screen content gestures act on content, not focus [V] HIG:focus-and-selection, HIG:color, HIG:layout.
- **Navigation**: tab bar at the top (translucent, 68 pt, scrolls away unless the screen has a split view); Back opens the parent (Home Screen at top level) and returns focus to the tab bar; split views for filtering (1/3–2/3 default or half/half), single title above [V] HIG:tab-bars, HIG:remotes, HIG:split-views. Live-viewing tab order: Live, Cloud DVR, Other [V].
- **Text entry and search**: linear keyboard with Siri Remote; search is a dedicated keyboard screen with results below; provide suggestions since people avoid typing [V] HIG:virtual-keyboards, HIG:search-fields.
- **Layout**: 60 pt top/bottom, 80 pt side safe insets; column grids (section 1); partial off-screen items symmetrical [V] HIG:layout.
- **System surfaces**: Top Shelf (feature new content, no ads or prices, provide static fallback), TV app integration, SharePlay, TV provider accounts, Picture in Picture [V] HIG:designing-for-tvos, HIG:top-shelf, HIG:multitasking.
- **Does not exist**: widgets, popovers, edit menus, menu bar, windows, pointing devices as a UI model, drag and drop, Live Activities, status bars, scroll indicators (system scrolls to keep focus visible), full-screen mode API [V] HIG:widgets, HIG:popovers, HIG:edit-menus, HIG:the-menu-bar, HIG:windows, HIG:pointing-devices, HIG:drag-and-drop, HIG:live-activities, HIG:scroll-views, HIG:going-full-screen.
- **Game controllers**: tvOS and visionOS apps may *require* a controller (App Store badge) [V] HIG:game-controls.
- **Liquid Glass**: on navigation elements, Top Shelf, Control Center; controls adopt glass on focus; adopt standard focus APIs; Apple TV 4K 2nd gen or newer only [V] HIG:materials, DOC:technologyoverviews/adopting-liquid-glass.

### 2.6 visionOS
- **Device**: infinite 3D canvas; Shared Space (many apps) vs Full Space (one app); passthrough; Spatial Audio; content placed relative to the head; users 13+; not while moving in unsafe environments [V] HIG:designing-for-visionos.
- **Input**: eyes to target plus indirect pinch tap (primary); direct touch (near, infrequent); Digital Crown is system-only (immersion, recenter, Home); keyboard/trackpad/game controller optional; gaze position is private and never delivered before a tap [V] HIG:eyes, HIG:gestures, HIG:digital-crown.
- **Containers**: windows (glass background, default 1280x720 pt, set min/max size but never to block resizing), volumes (3D, viewable from all sides, baseplate glow, visionOS 2+ ornaments), immersive spaces with `mixed` / `progressive` / `full` styles [V] HIG:windows, HIG:immersive-experiences.
- **Navigation**: tab bar is always **vertical** on the window's leading side, expands on look (symbol plus short label required); sidebar inside a tab for deep hierarchies; toolbar is an ornament along the **bottom** edge; avoid vertical toolbars and pull-down menus in toolbars; keep window wider than its toolbar since there is no menu bar [V] HIG:tab-bars, HIG:sidebars, HIG:toolbars. Ornaments for controls, not supplemental content (use an adjacent window); ornament no wider than its window [V] HIG:ornaments, HIG:layout.
- **Modality**: sheets centered in front of the parent (not sliding from the bottom edge), not covering the whole window; alerts anchored in front of window (Shared Space) or centered in field of view (Full Space); prefer split view over a new window for supplementary info; context menu no taller than the window [V] HIG:sheets, HIG:alerts, HIG:split-views, HIG:context-menus.
- **Comfort / ergonomics**: keep content in the field of view, centered; never head-lock content; prefer horizontal over vertical layouts; no motion in peripheral vision; do not rotate the world; keep a stationary frame of reference; interactive items rounded, ≥60 pt, 16 pt margins; avoid depth on text; use minimum necessary immersion; launch in the Shared Space [V] HIG:spatial-layout, HIG:eyes, HIG:motion, HIG:accessibility, HIG:launching.
- **Hover vs focus**: gaze shows the *hover effect*; the focus system is separate and only for connected keyboard/controller [V] HIG:focus-and-selection.
- **Does not exist**: Dark Mode, action sheets, status bars, menu bar (shortcut overlay on holding Command instead), panels, Live Activities, full-screen mode, interactive page controls [V] HIG:dark-mode, HIG:action-sheets, HIG:status-bars, HIG:keyboards, HIG:panels, HIG:live-activities, HIG:page-controls.
- **Accessibility specifics**: VoiceOver, Switch Control, Dwell Control, Pointer Control (head/hand), Zoom; never require specific body movement or a specific hand [V] HIG:designing-for-visionos, HIG:accessibility, HIG:gestures.
- **Design language**: system "glass" material (unmodifiable window background, adapts to luminance); use color sparingly; white text by default; vibrancy levels label / secondaryLabel / tertiaryLabel [V] HIG:materials, HIG:color, HIG:typography.

---

## 3. Universal vs platform-specific matrix

Legend: "n/a" = HIG says "Not supported". Cells are [V] from the pages cited in section 2 unless marked, with these
exceptions that are my synthesis or memory [M]: the Settings row for iOS/tvOS/visionOS ("in-app"; HIG:settings only has
macOS and watchOS specifics), the tvOS modality cell, and the widget *locations* on macOS (HIG:widgets only confirms
widgets are supported on macOS and unsupported on tvOS).

| Concern | iOS | iPadOS | macOS | watchOS | tvOS | visionOS |
|---|---|---|---|---|---|---|
| Primary navigation | Bottom floating tab bar; or stack | Top tab bar, optionally sidebar-adaptable; or sidebar split view | Sidebar + split view; menu bar commands | Vertical list / vertical tabs driven by Crown | Top tab bar + focus | Vertical tab bar on leading edge |
| Secondary navigation | Push in navigation stack; segmented control | Split-view columns; segmented control | Split panes, tab views, outline views | Detail pages (short), vertical paging | Split view (filter), rows of shelves | Sidebar inside a tab; split view |
| Top-level bar for actions | Top toolbar ("navigation bar") + bottom toolbar | Top toolbar sharing row with tab bar | Window toolbar (customizable) + menu bar | Corner / bottom toolbar buttons | Few on-screen buttons; no toolbar guidance | Bottom toolbar ornament |
| Modality | Sheets with detents, full-screen cover, alerts, action sheets | Form/page sheets, popovers, alerts | Window-attached sheets, alerts, panels, detachable popovers | Full-screen sheet, alert, action sheet (≤4 buttons) | Full-screen views, alerts | Centered sheet, alert in front on z-axis |
| Menus | Pull-down, pop-up, context (long press), edit menu | Same + menu bar + secondary click | Menu bar (required), context, Dock menu, pop-up/pull-down | n/a context/edit menus; More menu button | Context menus allowed; n/a edit menu | Context menus, menus from 3D content; no menu bar |
| Search | Search tab, bottom toolbar, top toolbar, or inline | Toolbar trailing, sidebar top, or dedicated tab | Toolbar trailing or sidebar top | Field opens full-screen input | Dedicated search screen with keyboard | Same as iPad conventions ("No additional considerations") |
| Settings | In-app + Settings app bundle [M] | In-app; menu bar Settings item opens system Settings page | Settings window from App menu (Cmd-,) | No custom entries in Settings app; inline options | In-app | In-app |
| Selection / focus | Touch; no focus system | Touch + pointer effects + keyboard focus groups | Pointer + key window + Full Keyboard Access | Touch + Crown | Focus engine (mandatory) | Gaze hover effect + pinch; focus only with hardware input |
| Text entry | Virtual keyboard | Virtual / hardware keyboard, Pencil Scribble | Hardware keyboard | Dictation, Scribble, small keyboard; avoid | Linear remote keyboard; avoid | Floating virtual keyboard window; hardware keyboard |
| Minimum hit target (default / min) | 44 / 28 pt | 44 / 28 pt | 28 / 20 pt | 44 / 28 pt | 66 / 56 pt | 60 / 28 pt |
| Default body size | 17 pt | 17 pt | 13 pt | 16 pt | 29 pt | 17 pt |
| Dynamic Type | Yes | Yes | No | Yes | Yes | Yes |
| Dark Mode | Yes | Yes | Yes | No | Yes | No |
| Multi-window | No (Duo: Split View multitasking) | Yes, resizable windows | Yes, core model | No | No | Yes: windows, volumes, spaces |
| Multitasking | App switch, PiP | Windowed or full screen, PiP | Default | n/a | PiP | Shared Space |
| Haptics | System + UIFeedbackGenerator (notification, impact, selection), Core Haptics | Core Haptics available; standard components [V partial] | Magic Trackpad only | Named watch haptics + Crown detents | Core Haptics on controllers | Core Haptics available (per games page) |
| Liquid Glass | Yes | Yes | Yes | Minimal, automatic | Yes (4K 2nd gen+), on focus | No; own glass material |
| Widgets / glanceable | Home, Lock, StandBy, Live Activities | Home, Lock, Live Activities | Desktop/Notification Center widgets; iPhone Live Activities in menu bar | Complications, Smart Stack | Top Shelf (no widgets) | Spatial widgets on surfaces |

Universal (identical on all platforms, per HIG "No additional considerations" on all six): modality principles, searching pattern, standard alert button semantics, use of system components, SF Symbols, semantic colors, writing/tone [V] HIG:modality, HIG:searching.

---

## 4. Decision procedure: determine target platform(s)

Run steps in order; later evidence refines earlier. Output a set of platforms plus a "technology" tag per target (SwiftUI / UIKit / AppKit / Catalyst / Designed-for-iPad).

1. **Explicit prompt**. If the user names a device or OS, that wins. Ambiguous "app" with no codebase: ask, or default to iOS and state the assumption (CONV).
2. **Xcode project** (`*.xcodeproj/project.pbxproj`, `.xcconfig`): read per-target build settings.

| Signal | Meaning | Tag |
|---|---|---|
| `SDKROOT` | "name or path of the base SDK" | [V] DOC:xcode/build-settings-reference |
| `SDKROOT = iphoneos` / `macosx` / `watchos` / `appletvos` / `xros` / `auto` | iOS+iPadOS / macOS / watchOS / tvOS / visionOS / multiplatform target | [M] values not listed in the reference |
| `SUPPORTED_PLATFORMS` | "list of supported platforms from which a base SDK can be used"; multi-platform targets list several (e.g. `iphoneos iphonesimulator macosx xros xrsimulator`) | setting [V]; value strings [M] |
| `TARGETED_DEVICE_FAMILY` | `1` iPhone/iPod touch; `2` iPad, and Mac Catalyst "Scaled to Match iPad"; `3` Apple TV; `4` Apple Watch; `6` Mac Catalyst "Optimize for Mac" | [V] |
| `TARGETED_DEVICE_FAMILY` contains `7` | Apple Vision | [M] not in the fetched reference |
| `SUPPORTS_MACCATALYST = YES` | Mac Catalyst target; with family `6` = Mac idiom, with `2` only = iPad idiom scaled | [V] |
| `SUPPORTS_MAC_DESIGNED_FOR_IPHONE_IPAD` | "Show the Mac (Designed for iPhone) and Mac (Designed for iPad) destinations": unmodified iOS app on Apple silicon Mac; not a Mac design target | [V] |
| `SUPPORTS_XR_DESIGNED_FOR_IPHONE_IPAD` | same for Apple Vision: compatible iPad/iPhone app in a window; not a native visionOS design | [V] |
| `IPHONEOS_DEPLOYMENT_TARGET`, `MACOSX_DEPLOYMENT_TARGET`, `WATCHOS_DEPLOYMENT_TARGET`, `TVOS_DEPLOYMENT_TARGET`, `XROS_DEPLOYMENT_TARGET` | minimum OS; decides which APIs (26+ glass, 27.1 arrangement) can be used unguarded | [M] names |
| `IS_MACCATALYST` | read-only, for scripts | [V] |

3. **Swift package** (`Package.swift`): `platforms: [.iOS(.v17), .macOS(.v14), .watchOS(...), .tvOS(...), .visionOS(...), .macCatalyst(...)]`. `SupportedPlatform` has iOS, macOS, watchOS, visionOS, tvOS, macCatalyst, driverKit, custom [V] DOC:packagedescription/supportedplatform. Absent `platforms:` means SwiftPM default minimums for all platforms [V], so treat as "unspecified", not "all".
4. **Info.plist keys**.

| Key | Meaning | Tag |
|---|---|---|
| `LSRequiresIPhoneOS` | "app must run in iOS" | [V] |
| `UIDeviceFamily` | written by the build system from `TARGETED_DEVICE_FAMILY` | [V] (build settings ref) |
| `UIApplicationSceneManifest` | scene-based iOS/iPadOS/visionOS app; multiple-scene support flag inside it indicates multi-window iPad | key [V]; sub-key name `UIApplicationSupportsMultipleScenes` [M] |
| `UIRequiresFullScreen` | iPad opt-out of multitasking; **deprecated**; on iPadOS 26+ the system scales rather than going full screen | [V] |
| `UIDesignRequiresCompatibility` | temporary Liquid Glass opt-out (26.0); ignored when building for 27+ | [V] |
| `WKApplication` (watchOS 7.0), `WKWatchOnly`, `WKRunsIndependentlyOfCompanionApp`, `WKCompanionAppBundleIdentifier` | watchOS app; watch-only; independent; companion | [V] |
| `UIApplicationPreferredDefaultSceneSessionRole` (visionOS 1.0) | visionOS launching into a window, volume or immersive space | [V] |
| `LSUIElement` | macOS agent app (no Dock icon): likely a menu bar extra | [V] |
| `NSPrefersDisplaySafeAreaCompatibilityMode` | macOS camera-housing handling | [V] referenced by HIG:layout |

5. **Source code signals**.

| Signal | Indicates | Tag |
|---|---|---|
| `import AppKit`, `NSWindow`, `NSViewController`, `NSMenu`, `.xib` with NSWindow | native macOS (AppKit) | [M] |
| `import UIKit` + `#if targetEnvironment(macCatalyst)` or `UIMenuBuilder`/`UIKeyCommand` | iOS/iPadOS, possibly Catalyst | Catalyst APIs [V] HIG:mac-catalyst; condition [M] |
| `import WatchKit`, `WKInterfaceController`, `.digitalCrownRotation` (watchOS 6.0 only), `TabView` `.verticalPage` (watchOS 10.0 only) | watchOS | availability [V] |
| `import TVUIKit`, `TVServices` (Top Shelf), `UIFocusGuide`-heavy code | tvOS | [M] |
| `import RealityKit` + `ImmersiveSpace` (visionOS 1.0 only), `.ornament(...)` (visionOS 1.0 only), `windowStyle(.volumetric)` | visionOS. RealityKit alone is not decisive (also iOS/macOS AR) | availability [V]; caveat [M] |
| SwiftUI `Settings { }` scene (macOS 11.0 only), `MenuBarExtra` (macOS 13.0 only), `.commands { }` | macOS (commands also iPadOS menu bar) | availability [V] |
| `#if os(iOS)` / `os(macOS)` / `os(watchOS)` / `os(tvOS)` / `os(visionOS)` / `canImport(UIKit)` | multiplatform; enumerate all branches | [M] |
| `UIDevice.current.userInterfaceIdiom == .pad/.phone/.mac/.tv/.vision` | idiom branching (HIG discourages layout by idiom; use size classes) | recommendation [V] HIG:layout; enum cases [M] |
| `ArrangementView`, `ReservedRegion`, `UIArrangementViewController` | iPhone Duo-aware code, deployment 27.1+ | [V] |
| Multiple targets (app + Watch App + Widget extension + TopShelf extension) | each target is its own design surface | [M] |

6. **Classify the Mac flavor** (matters a lot for guidance):
   - AppKit or SwiftUI with macOS destination: full macOS conventions (section 2.3).
   - Mac Catalyst, iPad idiom (family 2): iPad layout scaled; still must add menu bar commands, shortcuts, toolbar, context menus [V] HIG:mac-catalyst.
   - Mac Catalyst, Mac idiom (family 6): text and views render at 100%; audit layout and font sizes [V].
   - "Designed for iPad/iPhone" on Mac or Vision: no design changes possible beyond the iPad app; apply iPadOS guidance and say so.
7. **Cross-check with the prompt**: if the code targets several platforms but the request concerns one screen, guide for every platform that compiles that file (check `#if os`).
8. **Report**: state detected platforms, minimum OS versions, and which evidence was used; flag unverifiable guesses.

---

## 5. Cross-platform adaptation guidance

### 5.1 iPhone to iPad
Change (all [V] unless noted):
- Bottom tab bar becomes a top tab bar; consider `sidebarAdaptable` for many sections; keep ≤5 default tabs for parity with compact (HIG:tab-bars).
- Replace push-only stacks with 2 or 3 column split views in regular width; collapse gracefully at narrow window widths (HIG:split-views).
- Replace full-screen modals with form/page sheets and popovers; minimize modality (HIG:sheets, HIG:designing-for-ipados).
- Support resizable windows and multiple windows; do not assume full screen or orientation; keep leading toolbar items clear of window controls (HIG:windows).
- Add keyboard shortcuts, menu bar menus, focus groups, pointer hover effects, band selection, context menus on secondary click, drag and drop, Pencil where relevant (HIG:the-menu-bar, HIG:focus-and-selection, HIG:pointing-devices).
- Drive layout from size classes, not idiom or orientation; keep functionality constant across sizes (HIG:layout).
Common mistakes: stretched single-column phone UI; bottom-anchored controls far from hands; modal full-screen flows; `UIRequiresFullScreen`; landscape-only assumptions; menu bar as the only path to a command.

### 5.2 iPad to Mac (HIG:mac-catalyst unless noted, [V])
- Tab bar becomes sidebar split view (preferred) or segmented control; list former tabs in the View menu.
- Put every command in the menu bar with standard shortcuts; toolbar items are a subset of menu commands (HIG:toolbars).
- Move controls from screen edges/bottom into the window toolbar; adopt top-down flow; avoid the window bottom (HIG:layout).
- Split single columns into multiple columns; inspector instead of popover.
- Add Settings window (Cmd-,), context menus everywhere, Next/Previous buttons in addition to swipe paging, macOS app icon.
- Smaller metrics: 13 pt body, 28x28 default controls; no Dynamic Type, so offer in-app font size where needed [M for the last clause] (HIG:typography).
- Support window resize/minimize/full screen, multiple windows, inactive-window appearance (HIG:windows).
- If touch-capable Mac: keep same layout, enlarge tap targets (HIG:gestures).
Common mistakes: iPad-size touch controls and 17 pt text on Mac idiom; no menu bar; toolbar-only commands; sheets that block other windows; custom window chrome; hover-only controls with no alternative.

### 5.3 iPhone to Watch ([V])
- Do not port the app; pick the one or two glanceable tasks; sessions under a minute (HIG:designing-for-watchos).
- Flatten hierarchy; vertical lists and vertical tabs on the Crown; detail pages short enough for vertical paging (HIG:lists-and-tables).
- Build complications/Smart Stack widgets and actionable notifications first; app second.
- Replace text entry with pickers/lists/dictation; ≤2–3 controls per row; full-width buttons.
- Handle Always On (redaction, dimming); use watch haptics; SF Compact via system text styles; no Dark Mode variant needed.
Common mistakes: tab bars or sidebars (unsupported); deep navigation; dense tables; sheets used as navigation; black icon background; relying on the phone being present.

### 5.4 To TV ([V])
- Every interactive element must be focusable and reachable by directional movement; design focused/unfocused states and spacing for scale-up (HIG:focus-and-selection).
- Respect 60/80 pt safe insets; 29 pt body, 66 pt controls; use grid specs (HIG:layout).
- Tab bar at top; content-forward, edge-to-edge artwork; minimal text entry; search screen with suggestions.
- Back returns to the parent, then the Home Screen; Play/Pause must work during playback (HIG:remotes).
- Add Top Shelf content; easy, infrequent sign-in; multiuser profiles (HIG:designing-for-tvos).
Common mistakes: touch metaphors (swipe actions, pull to refresh, pointers); small text; content in overscan; color-only focus; custom focus movement; long forms.

### 5.5 To Vision ([V])
- Start with a window using standard components; keep the glass background; no opaque full-window colors (HIG:windows, HIG:materials).
- Tab bar becomes vertical leading ornament; toolbar becomes bottom ornament; no bottom-edge sheets (HIG:tab-bars, HIG:toolbars, HIG:sheets).
- 60 pt targets with 16 pt margins; rounded shapes; hover effects on all interactive elements, including custom ones (HIG:eyes).
- Do not design a Dark Mode variant; use vibrancy and white text; use color sparingly (HIG:dark-mode, HIG:color).
- Use volumes/immersion only where they add value; launch in the Shared Space; minimum immersion; comfort rules (section 2.6).
- Never depend on knowing gaze location; support indirect gestures first.
Common mistakes: dense iPhone-size targets; head-locked HUDs; too many windows; motion at periphery; requiring arms raised; pull-down menus in the bottom toolbar; supplemental content in ornaments.

### 5.6 iPhone to iPhone Duo ([V] HIG:designing-for-iphone-duo)
Use standard bars so they move to the side automatically; compact (outer) and regular (inner) layouts; split view collapses on the outer display; test all poses in Device Hub; no display-specific code.

---

## 6. Recommended per-platform reference files for the skill (each under 200 lines)

Common skeleton for `references/platform-<name>.md`:
1. **When this file applies** (detection signals from section 4, 5 lines).
2. **Device and context** (display, distance, session length, 6 lines).
3. **Inputs** (primary, secondary, what to never rely on).
4. **Navigation and containers** (table: need, component, SwiftUI API, UIKit/AppKit API, min OS).
5. **Windows / multitasking model**.
6. **Modality, menus, search, settings** (one short rule each).
7. **Metrics table** (text sizes, target sizes, safe areas, fixed numbers).
8. **Appearance** (Dark Mode, Dynamic Type, Liquid Glass or glass, materials).
9. **System surfaces** (widgets, Live Activities, complications, Top Shelf, etc.).
10. **Accessibility specifics**.
11. **Not available / discouraged here**.
12. **Porting pitfalls** (checklist an agent can run in review).
13. **Sources** (HIG slugs).

Per-file emphasis:
- `platform-ios.md`: bottom floating tab bar, toolbar/large title, sheets and detents, search placement, reachability; a 30-line **iPhone Duo** section (vertical controls, reserved regions, `ArrangementView` 27.1).
- `platform-ipados.md`: top tab bar vs sidebar decision, split views across widths, windowing and window controls, menu bar, keyboard focus groups, pointer, Pencil.
- `platform-macos.md`: menu bar structure table, toolbar/menu parity, Settings window, window states, sidebar sizes, sheets/panels/popovers, touch-on-Mac rules, Catalyst vs AppKit vs Designed-for-iPad triage.
- `platform-watchos.md`: Crown-driven vertical model, toolbar placements, complications/Smart Stack, notifications, Always On, double tap, unsupported list.
- `platform-tvos.md`: focus engine rules, safe area and grid numbers, tab bar constants, remote button table, Top Shelf, text-entry avoidance.
- `platform-visionos.md`: windows/volumes/spaces decision, ornaments, eyes and hands, comfort checklist, metrics (60 pt, 16 pt, 1280x720), immersion styles, no Dark Mode.
- Plus `references/platform-matrix.md` (section 3 matrix + section 1 numbers) and `references/platform-detection.md` (section 4) so the main SKILL.md can link rather than inline.

---

## 7. Not verified / caveats

- `SDKROOT` and `SUPPORTED_PLATFORMS` literal values, `TARGETED_DEVICE_FAMILY = 7` for Apple Vision, `*_DEPLOYMENT_TARGET` names, `#if os(...)` spellings, `userInterfaceIdiom` cases: [M] (the build settings reference describes the settings but does not enumerate these values; `UIDeviceFamily` doc page returned 404).
- `UIApplicationSupportsMultipleScenes` doc path returned 404; "Preparing your app for iPhone Duo" article path not found (guessed path).
- Device screen-size specification tables (iPhone/iPad/Watch point sizes) exist in HIG:layout per its change log but were not captured by my text extraction; another pass should pull them from the JSON if the skill needs them.
- Exact OS release marketing names for version 27 and hardware details of iPhone Duo, touch Macs and Apple HomeView were not researched beyond the HIG text.
- HIG:multitasking no longer describes iPad Slide Over/Split View by name, but HIG:layout and HIG:mac-catalyst still mention "Slide Over"/"Split View" (stale wording inside the HIG itself).
- iPadOS haptics cell in the matrix: HIG:playing-haptics platform section lists iOS, macOS, watchOS specifics only; Core Haptics availability on iPadOS/tvOS/visionOS is from HIG:designing-for-games.

## 8. Contradictions with common lore

| Lore | Current HIG (verified) |
|---|---|
| "iPad apps should use a sidebar" | Tab bar first (at the top); sidebar is the optional expanded form |
| "Navigation bar" is a component | Folded into Toolbars |
| "iPad has no menu bar / windows" | Has both; windows freely resizable |
| "Macs have no touch" | Touch display guidance exists (secondary input) |
| "iPhone is one screen, bars top and bottom" | iPhone Duo puts bars on the side; compact and regular widths on one device |
| "Tab bar: 3–5 tabs, 49 pt high" | HIG gives no height for iOS; says avoid overflow (More tab); tvOS is the only platform with fixed tab bar numbers (68/46 pt) |
| "44 pt is the universal minimum" | 44 is the *default* on iOS/iPadOS/watchOS; table lists 28 pt minimum; macOS 28/20; tvOS 66/56; visionOS 60/28 |
| "Liquid Glass is everywhere" | Not on visionOS APIs; minimal on watchOS; never in the content layer; opt-out key dead at 27 |
| "Support Dark Mode on every platform" | Not on watchOS or visionOS |
| "Use device idiom/orientation to pick layout" | Use size classes; idiom and orientation "aren't useful for making layout decisions" |
