# SwiftUI adaptive layout, safe areas, scenes and platform specifics

Scope: SwiftUI APIs for layouts that adapt to width, text size, safe areas and writing direction, plus scenes, windows, commands and per-platform input APIs, with verified minimum OS versions. Design guidance is in `references/foundations-layout.md`.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Reading availability
- Size classes
- Layouts that adapt by themselves
- Grids and container-relative sizing
- Safe areas and margins
- Background extension and scroll edge effects (OS 26+)
- GeometryReader cautions
- Right-to-left
- Scenes and windows
- Commands and keyboard shortcuts
- Platform-specific APIs
- Common mistakes

## Reading availability

- [API] Versions are `introducedAt` values from the documentation JSON. A platform that is not named has no availability entry: treat the API as missing there and compile it out with `#if os(...)`.
- [API] Documentation landing pages merge overloads and can show a newer minimum than the oldest overload. Example: `safeAreaInset(edge:alignment:spacing:content:)` has a horizontal-edge and a vertical-edge overload on one page (both iOS 15). Open the overload you call before quoting a version.
- [API] Some symbols are back-deployed and show the back-deployed version: `\.horizontalSizeClass` lists macOS 10.15, tvOS 13 and watchOS 6 with `@backDeployed(before: macOS 14.0, tvOS 17.0, watchOS 10.0)`.
- [Conv] Nothing here was compiled. Build before claiming it works; view and model names are placeholders.

Source: https://developer.apple.com/documentation/swiftui/layout-fundamentals, https://developer.apple.com/documentation/swiftui/environmentvalues

## Size classes

```swift
// iOS 13+, visionOS 1+; macOS, tvOS and watchOS through back-deployment (see above)
struct Dashboard: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass
    var body: some View {
        if horizontalSizeClass == .compact {
            VStack { SummaryPanel(); ActivityPanel() }
        } else {
            HStack(alignment: .top) { SummaryPanel(); ActivityPanel() }
        }
    }
}
```

- [API] `\.horizontalSizeClass` and `\.verticalSizeClass` are `UserInterfaceSizeClass?` (`.compact`, `.regular`); handle `nil`. SwiftUI sets them from the device type, orientation, and Slide Over or Split View on iPad.
- [HIG] In iOS and iPadOS a size class says how much space the app has in that dimension, not which device it runs on; an iPad window can be horizontally compact.
- [Conv] Branch on size class or available space, never on `UIDevice.current.userInterfaceIdiom` or screen bounds.
- [Conv] An `if`/`else` between two stacks gives the two branches different view identity, so state inside them resets on change. Use `AnyLayout` (next section) to keep identity.

Source: https://developer.apple.com/documentation/swiftui/userinterfacesizeclass, https://developer.apple.com/design/human-interface-guidelines/layout

## Layouts that adapt by themselves

```swift
// iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+
struct PriceRow: View {
    let title: String
    let price: String
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize   // iOS 15+
    var body: some View {
        let layout = dynamicTypeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading))
            : AnyLayout(HStackLayout())
        layout {
            Text(title)
            Text(price).foregroundStyle(.secondary)
        }
    }
}
```

```swift
// iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+
ViewThatFits(in: .horizontal) {
    HStack { Text(title); Spacer(); ActionButtons() }
    VStack(alignment: .leading) { Text(title); ActionButtons() }
}
```

- [API] `ViewThatFits` evaluates its children in order and shows the first whose ideal size fits the proposed size on the constrained axes (both axes by default). List the preferred, usually largest, arrangement first.
- [API] `AnyLayout` with `HStackLayout` / `VStackLayout` switches the arrangement without changing view identity.
- [HIG] Be prepared for text-size changes: layouts must adapt when people enlarge text. Switch from side-by-side to stacked at accessibility sizes instead of truncating.
- [Conv] Prefer `frame(minHeight:)` and padding over fixed heights around text so rows can grow.

Source: https://developer.apple.com/documentation/swiftui/viewthatfits, https://developer.apple.com/documentation/swiftui/anylayout, https://developer.apple.com/documentation/swiftui/dynamictypesize, https://developer.apple.com/design/human-interface-guidelines/layout

## Grids and container-relative sizing

```swift
// LazyVGrid and GridItem: iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+
ScrollView {
    LazyVGrid(columns: [GridItem(.adaptive(minimum: 160))], spacing: 16) {
        ForEach(albums) { AlbumCell(album: $0) }
    }
    .padding(.horizontal)
}
```

```swift
// Grid and GridRow: iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+
Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 8) {
    GridRow { Text("Name"); Text(item.name) }
    GridRow { Text("Modified"); Text(item.modified, style: .date) }
}
```

- [API] `GridItem(.adaptive(minimum:maximum:))` fits as many columns as the width allows, so the column count follows window size and orientation without size-class code.
- [API] `Grid` is eager and aligns cells across rows; `LazyVGrid` creates cells on demand inside a `ScrollView`. `gridCellColumns(_:)` (iOS 16+) spans columns.
- [API] `containerRelativeFrame(_:alignment:)` and `containerRelativeFrame(_:count:span:spacing:alignment:)` (iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+) size a view as a fraction of its nearest container, for example `.containerRelativeFrame(.horizontal, count: 3, span: 1, spacing: 16)` for three cards per page.
- [API] There is no dedicated SwiftUI readable-width modifier in the documentation checked. `List` and `Form` manage their own margins; [Conv] cap free-standing text with `frame(maxWidth:)`. UIKit has `readableContentGuide` (iOS 9+).

Source: https://developer.apple.com/documentation/swiftui/lazyvgrid, https://developer.apple.com/documentation/swiftui/griditem, https://developer.apple.com/documentation/swiftui/grid, https://developer.apple.com/documentation/swiftui/layout-adjustments

## Safe areas and margins

| API | Availability | Use for |
|---|---|---|
| `safeAreaInset(edge:alignment:spacing:content:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Pin a bar or button to an edge; the modified view's safe area shrinks so scroll content is not covered. |
| `safeAreaPadding(_:)`, `safeAreaPadding(_:_:)` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ | Add a fixed amount to the safe area a view sees. |
| `contentMargins(_:_:for:)` | same as `safeAreaPadding` | Inset scrollable content (placement `.scrollContent`) instead of padding the scroll view itself. |
| `scenePadding(_:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Platform-appropriate padding from the scene edge. |
| `padding()` with no length | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | System default spacing; prefer it to a hard-coded number. |
| `ignoresSafeArea(_:edges:)` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Backgrounds only. `edgesIgnoringSafeArea(_:)` is deprecated. |
| `background(_:ignoresSafeAreaEdges:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | A `ShapeStyle` background; ignores all safe-area edges by default. |
| `safeAreaBar(edge:alignment:spacing:content:)` | OS 26+ on all platforms | Like `safeAreaInset`, and also extends the scroll edge effect under the bar. |

```swift
// iOS 15+, macOS 12+, visionOS 1+ as written: .bar has no tvOS or watchOS entry.
// With .regularMaterial instead of .bar: also tvOS 15+, watchOS 10+.
ScrollView { ArticleBody(article: article).padding() }
    .background(.background)                      // fills under the safe area by default
    .safeAreaInset(edge: .bottom) {
        Button("Continue") { advance() }
            .buttonStyle(.borderedProminent)
            .padding()
            .frame(maxWidth: .infinity)
            .background(.bar)                     // .bar: iOS 15+, macOS 12+, visionOS 1+
    }
```

- [HIG] Respect system-defined safe areas, margins and guides so the layout adapts to devices, orientations and window sizes.
- [Conv] Apply `ignoresSafeArea` to a background color, image or material, never to the view that holds text and controls; content then stays clear of the sensor housing, home indicator and bars.
- [API] `ignoresSafeArea(.keyboard)` is a `SafeAreaRegions` value; the default region is `.all`.
- [API] `scrollDismissesKeyboard(_:)` is iOS 16+, macOS 13+, tvOS 16+, watchOS 9+ (not visionOS).

Source: https://developer.apple.com/documentation/swiftui/safearearegions, https://developer.apple.com/documentation/swiftui/scrollview, https://developer.apple.com/documentation/swiftui/layout-adjustments, https://developer.apple.com/design/human-interface-guidelines/layout

## Background extension and scroll edge effects (OS 26+)

- [API] `backgroundExtensionEffect()` (iOS 26+, macOS 26+, tvOS 26+, watchOS 26+, visionOS 26+) mirrors and blurs copies of a view into adjacent safe-area regions. Typical use: a banner image in the detail column of a `NavigationSplitView` that appears to continue under the sidebar or inspector. Apple's documentation says to use it with discretion, usually on a single background view; it clips the view.
- [API] `scrollEdgeEffectStyle(_:for:)` and `scrollEdgeEffectHidden(_:for:)` are iOS 26+, macOS 26+, tvOS 26+, watchOS 26+ (the modifiers list no visionOS availability). Styles: `.soft`, `.hard`.
- [HIG] (OS 26+, Liquid Glass) Instead of a solid or semi-opaque background beneath controls, use a scroll edge effect to separate controls from content; use a background extension effect when sidebars or inspectors would cover important parts of a full-bleed image.
- [Conv] Gate all three with `if #available(iOS 26, macOS 26, *)` inside a small `ViewModifier`; the fallback is simply the unmodified view. The two scroll edge modifiers also need `#if !os(visionOS)` in code that builds for visionOS.

Source: https://developer.apple.com/documentation/swiftui/scrolledgeeffectstyle, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/design/human-interface-guidelines/layout

## GeometryReader cautions

- [API] `GeometryReader` (iOS 13+) returns a flexible preferred size to its parent layout. [Conv] In practice it takes the space offered, so wrapping a row or a whole screen in one changes how the parent lays out.
- [Conv] Reach for it last. Proportional widths: `containerRelativeFrame` (iOS 17+). Alternate arrangements: `ViewThatFits` (iOS 16+). Column counts: adaptive `GridItem`. Custom arrangement: the `Layout` protocol (iOS 16+).
- [API] To read a size without affecting layout use `onGeometryChange(for:of:action:)`; the metadata lists iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+ (a second overload is iOS 18+).
- [API] `UIScreen.main` is deprecated (iOS 26.0); do not size SwiftUI views from screen bounds. A window can be smaller than the screen on iPad, Mac and Apple Vision Pro.

Source: https://developer.apple.com/documentation/swiftui/geometryreader, https://developer.apple.com/documentation/swiftui/layout-fundamentals, https://developer.apple.com/documentation/uikit/uiscreen

## Right-to-left

- [API] Use `.leading` / `.trailing` for alignment, padding edges and toolbar placements; SwiftUI resolves them against `\.layoutDirection` (`.leftToRight`, `.rightToLeft`; iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+).
- [HIG] System components flip automatically in a right-to-left context; with standard elements and layouts little extra work is needed.
- [HIG] Do not reverse the digits inside a number. Flip controls that show progress from one value to another, such as sliders and progress indicators.
- [API] `flipsForRightToLeftLayoutDirection(_:)` (iOS 13+) mirrors a custom image or shape that has a direction; leave logos and non-directional images alone.
- [Conv] Test with `.environment(\.layoutDirection, .rightToLeft)` in a preview and with a right-to-left pseudolanguage in the scheme. Avoid `offset(x:)` and absolute x positions for directional layout.

Source: https://developer.apple.com/documentation/swiftui/layoutdirection, https://developer.apple.com/design/human-interface-guidelines/right-to-left

## Scenes and windows

| Scene or modifier | Availability | Notes |
|---|---|---|
| `WindowGroup` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Main scene; supports multiple windows on iPadOS, macOS and visionOS. |
| `Window(_:id:content:)` | macOS 13+, visionOS 26+ | One unique window for supplemental content. |
| `Settings` | macOS 11+ only | Enables the app-menu Settings item and its shortcut. Wrap in `#if os(macOS)`. `SettingsLink` and `\.openSettings` are macOS 14+. |
| `MenuBarExtra` | macOS 13+ only | Persistent item in the system menu bar. |
| `DocumentGroup` | iOS 14+, macOS 11+, visionOS 1+ | Document-based apps. `UtilityWindow` is macOS 15+. |
| `\.openWindow` / `\.dismissWindow` | iOS 16+, macOS 13+, visionOS 1+ / iOS 17+, macOS 14+, visionOS 1+ | Check `\.supportsMultipleWindows` first. |
| `defaultSize(width:height:)`, `windowResizability(_:)` | iOS 17+, macOS 13+, visionOS 1+ | `.windowResizability(.contentSize)` ties the window to its content's size limits. |
| `windowStyle(_:)` | macOS 11+, visionOS 1+ | `.volumetric` is visionOS 1+ only. `windowToolbarStyle(_:)` is macOS 11+ only. |

```swift
// macOS 13+ for MenuBarExtra; the WindowGroup and commands also build for iOS 14+ and visionOS 1+
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .commands {
                SidebarCommands()
                CommandMenu("Note") {
                    Button("Pin Note") { pinSelectedNote() }
                        .keyboardShortcut("p", modifiers: [.command, .shift])
                }
            }
        #if os(macOS)
        Settings { SettingsView().scenePadding() }
        MenuBarExtra("Quick Note", systemImage: "note.text") { QuickNoteMenu() }
        #endif
    }
}
```

- [API] `Settings` supplies the standard Settings menu item; do not add your own menu item or shortcut for it.
- [HIG] On Mac the Settings item in the App menu opens a settings window (Command-Comma); avoid settings buttons in a window's toolbar.

Source: https://developer.apple.com/documentation/swiftui/scenes, https://developer.apple.com/documentation/swiftui/windows, https://developer.apple.com/documentation/swiftui/settings, https://developer.apple.com/documentation/swiftui/menubarextra, https://developer.apple.com/design/human-interface-guidelines/settings

## Commands and keyboard shortcuts

- [API] `commands(content:)`, `CommandMenu`, `CommandGroup(after:addition:)`, `CommandGroup(replacing:addition:)`, `CommandGroupPlacement` (for example `.newItem`, `.appSettings`, `.help`) and `SidebarCommands` are iOS 14+, macOS 11+, visionOS 1+.
- [API] `keyboardShortcut(_:modifiers:)` (default modifier `.command`) and `keyboardShortcut(.defaultAction)` / `.cancelAction` are iOS 14+, macOS 11+, visionOS 1+; there is no tvOS or watchOS availability.
- [API] `onKeyPress(_:action:)` is iOS 17+, macOS 14+, tvOS 17+, visionOS 1+. `help(_:)` (tooltip text) is iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+.
- [HIG] Mac users rely on the menu bar to learn what an app does and to find its commands; provide a consistent menu bar. [Unverified] How SwiftUI `commands` surface on iPadOS (shortcut overlay versus menu bar) was not checked against the documentation; test on device.

Source: https://developer.apple.com/documentation/swiftui/menus-and-commands, https://developer.apple.com/documentation/swiftui/keyboardshortcut, https://developer.apple.com/design/human-interface-guidelines/the-menu-bar, https://developer.apple.com/design/human-interface-guidelines/keyboards

## Platform-specific APIs

| API | Availability | Notes |
|---|---|---|
| `@FocusState`, `focused(_:)`, `focused(_:equals:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Programmatic focus on every platform. |
| `focusable(_:)` | iOS 17+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Makes a custom view focusable; `focusable(_:interactions:)` is iOS 17+, macOS 14+, tvOS 17+, watchOS 10+. Prefer `Button`, which is focusable already. |
| `focusSection()` | macOS 13+, tvOS 15+ only | Lets directional focus jump across a gap to a group of focusable views. |
| `defaultFocus(_:_:priority:)` | iOS 17+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+ | Initial focus. |
| `onMoveCommand(perform:)`, `onExitCommand(perform:)` | macOS 10.15+, tvOS 13+ only | Remote and keyboard commands; `onPlayPauseCommand(perform:)` is tvOS 13+ only. |
| `buttonStyle(.card)` | tvOS 14+ only | Focus-lifting card button. |
| `digitalCrownRotation(_:)` and the `from:through:by:...` form | watchOS 6+ only | Apple's example applies `.focusable()` before it. |
| `tabViewStyle(.verticalPage)` | watchOS 10+ only | Vertical pages driven by the Digital Crown. |
| `hoverEffect(_:)` | iOS 13.4+, tvOS 16+, visionOS 1+; not on macOS | Pointer or eye highlight for custom tappable views; `hoverEffect(_:isEnabled:)` is iOS 17+. |
| `onHover(perform:)` | iOS 13.4+, macOS 10.15+, visionOS 1+ | `pointerStyle(_:)` is macOS 15+, visionOS 2+. |
| `contentShape(_:_:eoFill:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Defines the shape used for hit testing and, by kind, hover effects. |
| `ornament(visibility:attachmentAnchor:contentAlignment:ornament:)` | visionOS 1+ only | Controls attached outside a window edge, for example `attachmentAnchor: .scene(.bottom)`. |
| `windowStyle(.volumetric)` | visionOS 1+ only | Bounded 3D volume; `defaultSize(width:height:depth:in:)` is visionOS 1+. |
| `ImmersiveSpace` | visionOS 1+ only | Unbounded space; open with the `\.openImmersiveSpace` action (visionOS 1+, macOS 26+). Default immersion style is mixed; set with `immersionStyle(selection:in:)`. |
| `glassBackgroundEffect(displayMode:)` | visionOS 1+ only | The visionOS glass material for custom views. |

```swift
// watchOS only: digitalCrownRotation is watchOS 6+, focusable() is watchOS 8+
#if os(watchOS)
Text("Volume \(Int(volume))")                     // volume: @State Double
    .focusable()
    .digitalCrownRotation($volume, from: 0, through: 10, by: 0.5)
#endif
```

- [HIG] Rely on system-provided focus effects and indicate focus the way the platform does. [Conv] Standard buttons and list rows get them without extra code.
- [Conv] Compile platform-only modifiers out with `#if os(...)`; `#available` cannot hide a symbol that does not exist for the platform being built.

Source: https://developer.apple.com/documentation/swiftui/focus, https://developer.apple.com/documentation/swiftui/immersivespace, https://developer.apple.com/documentation/swiftui/ornamentattachmentanchor, https://developer.apple.com/design/human-interface-guidelines/focus-and-selection, https://developer.apple.com/design/human-interface-guidelines/digital-crown, https://developer.apple.com/design/human-interface-guidelines/ornaments

## Common mistakes

| Mistake | Fix |
|---|---|
| Layout from `UIScreen.main.bounds` or a device-idiom check | Size classes, `ViewThatFits`, adaptive grids, `containerRelativeFrame`. |
| `.ignoresSafeArea()` on a whole screen | Apply it to the background only; pin bars with `safeAreaInset`. |
| A bottom button in a `ZStack` that covers the last rows of a list | `safeAreaInset(edge: .bottom)` so the list's safe area shrinks. |
| `GeometryReader` around a screen for proportional sizes | `containerRelativeFrame`, `Grid`, `Layout`. |
| Fixed `HStack` that truncates at large text sizes | `AnyLayout` switch on `dynamicTypeSize.isAccessibilitySize`, or `ViewThatFits`. |
| Fixed `.frame(height:)` around text | `frame(minHeight:)` plus padding. |
| `.padding(.left, 16)`-style thinking, `offset(x:)` for alignment | `.leading` / `.trailing`; test with `\.layoutDirection`. |
| `Settings`, `MenuBarExtra`, `digitalCrownRotation`, `ornament` in shared code without a guard | `#if os(macOS)`, `#if os(watchOS)`, `#if os(visionOS)`. |
| Mac app with no menu commands or shortcuts, settings pushed in a window | `commands`, `keyboardShortcut`, a `Settings` scene. |
| `if`/`else` between `HStack` and `VStack` that resets child state | `AnyLayout`. |
| `backgroundExtensionEffect` or `safeAreaBar` with a deployment target below 26 | `#available` check with the plain view as fallback. |
