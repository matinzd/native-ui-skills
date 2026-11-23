# API availability, version gating and deprecated APIs

Scope: how to pick APIs that exist on the project's minimum OS, how to gate newer ones with real fallbacks, how to check availability in Apple's documentation data, the minimum OS of the APIs agents reach for most, and what replaces deprecated or stale spellings.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Find the deployment target first
- When the target is unknown
- Gating rules
- Gating patterns
- Verify availability in the documentation data
- Pitfalls when reading availability
- Minimum OS: SwiftUI structure and presentation
- Minimum OS: SwiftUI state, layout, feedback, styling
- Minimum OS: Liquid Glass and OS 27 additions
- Minimum OS: UIKit and AppKit anchors
- Deprecated or stale SwiftUI and its replacement
- Deprecated UIKit and its replacement
- Names that do not exist
- Common mistakes

## Find the deployment target first

- [Conv] Read the minimum OS before choosing any API. Look for `IPHONEOS_DEPLOYMENT_TARGET`, `MACOSX_DEPLOYMENT_TARGET`, `TVOS_DEPLOYMENT_TARGET`, `WATCHOS_DEPLOYMENT_TARGET` and `XROS_DEPLOYMENT_TARGET` in `project.pbxproj` and `.xcconfig` files, and `platforms:` in `Package.swift`. Apple's build settings reference does not list the per-platform names; commands and caveats are in `references/platforms-detection.md`.
- [API] A Swift package without a `platforms:` entry gets a predefined minimum, the oldest deployment target the installed SDK supports, so "no entry" does not mean "latest OS".
- [Conv] When targets or configurations disagree, use the lowest value that compiles the file being changed. State the result ("Target: iOS 16, macOS 13") and label every snippet with its own minimum OS.
- [Conv] Existing `#available` and `@available` lines in the code are evidence too: `if #available(iOS 17, *)` tells you the target is below iOS 17.

Source: https://developer.apple.com/documentation/packagedescription/supportedplatform , https://developer.apple.com/documentation/xcode/build-settings-reference

## When the target is unknown

- [Conv] If the answer depends on it, ask one short question. If asking is not possible, do not assume the newest OS.
- [Conv] Write to the floor the code evidently uses (for example, a file that already calls `NavigationStack` is at iOS 16 or later). With no evidence, write for iOS 17, macOS 14, tvOS 17, watchOS 10, visionOS 1, gate anything newer, and say the assumption in one line.
- [Conv] Prefer API that degrades by itself over version branches: standard bars and controls, `Label`, semantic toolbar placements and semantic styles pick up each OS's appearance without any check.
- [HIG] Standard components adopt the current system appearance (Liquid Glass on OS 26 and later) when built with the current SDK; that is not something to gate by hand.

Source: https://developer.apple.com/documentation/xcode/running-code-on-a-specific-version , https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass

## Gating rules

- [API] `#if os(iOS)` (also `targetEnvironment(macCatalyst)`, `canImport(UIKit)`) is a compile-time condition. Use it when a symbol does not exist on a platform at all: `Settings` (macOS only), `navigationBarTitleDisplayMode(_:)` (no macOS, no tvOS), `keyboardType(_:)` (no macOS, no watchOS), `fullScreenCover` (no macOS).
- [API] `if #available(iOS 18, macOS 15, *) { } else { }` is a run-time version check. List every platform the file compiles for; `*` means "any version" on the platforms you did not list.
- [API] Because `*` matches unlisted platforms, an API missing from one platform needs `#if os` as well as `#available`. Example: the glass effect modifiers have no visionOS availability, so `#available(iOS 26, macOS 26, *)` alone still fails to compile for visionOS.
- [API] `@available(iOS 18, macOS 15, *)` on a type, function or extension marks a whole declaration, which removes repeated checks inside it. Callers must then check before using it.
- [API] An API newer than the deployment target must not appear outside an availability check; the project will not build.
- [Conv] Always write the `else` branch as working UI with the same content and actions. An empty view, a missing button or a silently skipped feature is a regression for everyone on the older OS.
- [Conv] A deprecated API is the correct choice inside the fallback branch when its replacement needs a newer OS (`tabItem(_:)` below iOS 18). Mark the branch with a comment such as `// Fallback for iOS 17 and earlier`.
- [Conv] A modifier cannot be made conditional in the middle of a chain. Put the branch in a small `ViewModifier` or a `@ViewBuilder` helper and call that.
- [Conv] Gate on the API's own introduction version, and gate the smallest piece (one modifier, one container) so both branches share the content instead of forking a screen per OS.

Source: https://developer.apple.com/documentation/xcode/running-code-on-a-specific-version , https://docs.swift.org/swift-book/documentation/the-swift-programming-language/attributes/

## Gating patterns

Not compiled; every symbol was checked in the documentation data. Minimum OS for the file: iOS 15, macOS 12, watchOS 10 (`Material`).

```swift
import SwiftUI

// A custom floating control: Liquid Glass where the API exists, a standard material elsewhere.
struct FloatingControlBackground: ViewModifier {
    func body(content: Content) -> some View {
        #if os(visionOS)
        // The glass effect modifiers are not available on visionOS.
        content.background(.regularMaterial, in: Capsule())
        #else
        if #available(iOS 26, macOS 26, tvOS 26, watchOS 26, *) {
            content.glassEffect(.regular, in: Capsule())
        } else {
            // Fallback for OS 18 and earlier: same shape, standard material.
            content.background(.regularMaterial, in: Capsule())
        }
        #endif
    }
}

struct DetailTitle: ViewModifier {
    let title: String
    func body(content: Content) -> some View {
        content
            .navigationTitle(title)
            #if os(iOS)
            // Not available on macOS or tvOS, so this is a compile-time condition.
            .navigationBarTitleDisplayMode(.inline)
            #endif
    }
}

// A whole declaration that needs a newer OS; callers check with #available before using it.
@available(iOS 18, macOS 15, tvOS 18, watchOS 11, visionOS 2, *)
struct CurrentTabs: View {
    var body: some View {
        TabView {
            Tab("Home", systemImage: "house") { Text("Home") }
            Tab("Search", systemImage: "magnifyingglass", role: .search) { Text("Search") }
        }
    }
}
```

- [Conv] Apply the modifiers with `.modifier(FloatingControlBackground())`. `examples/TabRoot.swift` shows a complete `Tab` adoption with a marked fallback; `examples/AdaptiveNavigation.swift` gates `ContentUnavailableView`.

Source: https://developer.apple.com/documentation/swiftui/viewmodifier , https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:) , https://developer.apple.com/documentation/swiftui/tab

## Verify availability in the documentation data

Human pages are rendered by JavaScript; the data behind them is plain JSON.

- [API] URL pattern: `https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:)` becomes `https://developer.apple.com/tutorials/data/documentation/swiftui/view/presentationdetents(_:).json` (lowercase path, same symbol spelling).
- [API] `metadata.platforms` is a list of `{name, introducedAt, deprecatedAt, deprecated, beta}`. A platform that is absent has no availability: treat the API as unavailable there.
- [API] `deprecationSummary` holds the replacement Apple names. `primaryContentSections` holds the declaration; `topicSections` and `references` list members and related pages.
- [Conv] A 404 means the path is wrong, not that the API is missing: some symbols need a disambiguating suffix (`uikit/uilistcontentconfiguration-swift.struct`, `swiftui/shapestyle/secondary-swift.type.property`). Fetch the parent type's JSON and search its `references` for the exact path.
- [Conv] If the network is unavailable, say the availability is unverified and name the page to check. Do not quote a version from memory.

```bash
curl -s 'https://developer.apple.com/tutorials/data/documentation/swiftui/view/presentationdetents(_:).json' |
  python3 -c 'import json,sys; [print(p["name"], p.get("introducedAt"), p.get("deprecatedAt")) for p in json.load(sys.stdin)["metadata"]["platforms"]]'
```

Source: https://developer.apple.com/documentation/swiftui/view/presentationdetents(_:) , https://developer.apple.com/documentation/swiftui

## Pitfalls when reading availability

- [API] Merged overloads. One page covers every overload and shows the newest first. `alert(_:isPresented:actions:message:)`, `confirmationDialog`, `searchable`, `accessibilityLabel(_:)`, `Toggle(_:isOn:)` and `Button(_:role:action:)` all display iOS 16 (the `LocalizedStringResource` overload) although the `LocalizedStringKey` and `StringProtocol` overloads are iOS 13 to 15. Follow `otherDeclarations` in the declaration section and take the oldest overload you actually call.
- [API] Back-deployed symbols show the version they deploy back to, not the SDK that added them: `ToolbarItemPlacement.topBarLeading` and `.topBarTrailing` show iOS 14 with `@backDeployed(before: iOS 17.0)`; `onGeometryChange(for:of:action:)` shows iOS 16; the `#Preview` and `@Entry` macros show iOS 13. The number is safe as a deployment floor, but it does not tell you which Xcode is required.
- [API] Soft deprecations. A large batch of long-standing SwiftUI API carries a `deprecatedAt` equal to the current SDK release, and `accessibilityShowButtonShapes` carries `1000.0`. Read both as "deprecated, use the replacement" with no meaningful version; do not write "deprecated in iOS 27.3".
- [Unverified] Whether the compiler warns about those soft-deprecated symbols at lower deployment targets was not tested. Do not promise "no warnings" either way.
- [API] Platform gaps hide in the list: `sensoryFeedback` is visionOS 26 while iOS is 17; `Window` is macOS 13 but visionOS 26; `inspector` has only iOS and macOS entries; `swipeActions` has no tvOS entry.
- [HIG] SF Symbols are versioned too: a symbol introduced in a given year is not available on earlier systems. Check the symbol's availability in the SF Symbols app; the API documentation does not list symbol names.

Source: https://developer.apple.com/documentation/swiftui/view/alert(_:ispresented:actions:message:) , https://developer.apple.com/documentation/swiftui/toolbaritemplacement/topbartrailing , https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityshowbuttonshapes , https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## Minimum OS: SwiftUI structure and presentation

All values are `introducedAt` for the oldest overload, read on 2026-11-23. "-" means no availability entry.

| API | iOS, iPadOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| `NavigationStack`, `NavigationSplitView`, `navigationDestination(for:destination:)` | 16 | 13 | 16 | 9 | 1 |
| `navigationDestination(item:destination:)` | 17 | 14 | 17 | 10 | 1 |
| `Tab`, `TabRole.search`, `TabSection`, `TabView(selection:content:)` with `Tab` | 18 | 15 | 18 | 11 | 2 |
| `tabViewStyle(.sidebarAdaptable)`, `.tabBarOnly` | 18 | 15 | 18 | - | 2 |
| `searchable(text:placement:prompt:)` | 15 | 12 | 15 | 8 | 1 |
| `searchable(text:isPresented:placement:prompt:)` | 17 | 14 | - | - | 1 |
| `toolbar(content:)`, `ToolbarItem`, semantic placements (`.primaryAction`, `.confirmationAction`, `.cancellationAction`) | 14 | 11 | 14 | 7 | 1 |
| `.topBarLeading`, `.topBarTrailing` | 14 (back-deployed) | - | 14 | 10 | 1 |
| `toolbarVisibility(_:for:)`, `toolbarBackgroundVisibility(_:for:)` | 18 | 15 | 18 | 11 | 2 |
| `presentationDetents(_:)`, `presentationDragIndicator(_:)` | 16 | 13 | 16 | 9 | 1 |
| `presentationBackground(_:)`, `presentationCompactAdaptation(_:)` | 16.4 | 13.3 | 16.4 | 9.4 | 1 |
| `presentationSizing(_:)` | 18 | 15 | 18 | 11 | 2 |
| `inspector(isPresented:content:)` | 17 | 14 | - | - | - |
| `alert(_:isPresented:actions:message:)`, `confirmationDialog(...)`, `Button(role:)`, `swipeActions` (no tvOS), `refreshable` | 15 | 12 | 15 | 8 | 1 |
| `ContentUnavailableView` (including `.search`) | 17 | 14 | 17 | 10 | 1 |
| `Settings` scene; `SettingsLink`, `openSettings` | - | 11; 14 | - | - | - |
| `commands(content:)`, `CommandMenu`, `keyboardShortcut(_:modifiers:)` | 14 | 11 | - | - | 1 |

Source: https://developer.apple.com/documentation/swiftui/navigationstack , https://developer.apple.com/documentation/swiftui/tab , https://developer.apple.com/documentation/swiftui/view/inspector(ispresented:content:) , https://developer.apple.com/documentation/swiftui/contentunavailableview , https://developer.apple.com/documentation/swiftui/settings

## Minimum OS: SwiftUI state, layout, feedback, styling

| API | iOS, iPadOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| `onChange(of:initial:_:)` (zero or two closure parameters) | 17 | 14 | 17 | 10 | 1 |
| `@Observable` macro (Observation), `@Bindable` | 17 | 14 | 17 | 10 | 1 |
| `ViewThatFits`, `AnyLayout`, `Grid`, `LabeledContent`, `formStyle(_:)` | 16 | 13 | 16 | 9 | 1 |
| `containerRelativeFrame`, `scrollTargetBehavior(_:)`, `contentMargins`, `safeAreaPadding(_:)` | 17 | 14 | 17 | 10 | 1 |
| `safeAreaInset(edge:alignment:spacing:content:)`, `dynamicTypeSize`, `DynamicTypeSize.isAccessibilitySize` | 15 | 12 | 15 | 8 | 1 |
| `@ScaledMetric`, `Label`, `ignoresSafeArea(_:edges:)` | 14 | 11 | 14 | 7 | 1 |
| `foregroundStyle(_:)`, `tint(_:)`, `symbolRenderingMode(_:)`, `Material` styles (`Material` on watchOS: 10) | 15 | 12 | 15 | 8 | 1 |
| `symbolEffect(_:options:value:)`, `PhaseAnimator` | 17 | 14 | 17 | 10 | 1 |
| `sensoryFeedback(_:trigger:)` | 17 | 14 | 17 | 10 | 26 |
| `AccessibilityNotification` (`.Announcement`, `.LayoutChanged`, `.ScreenChanged`) | 17 | 14 | 17 | 10 | 1 |
| `navigationSubtitle(_:)` | 26 | 13 | - | - | - |

Source: https://developer.apple.com/documentation/swiftui/view/onchange(of:initial:_:) , https://developer.apple.com/documentation/observation/observable() , https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:) , https://developer.apple.com/documentation/swiftui/view/containerrelativeframe(_:alignment:)

## Minimum OS: Liquid Glass and OS 27 additions

| API | iOS, iPadOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| `glassEffect(_:in:)`, `Glass`, `GlassEffectContainer`, `glassEffectID(_:in:)` | 26 | 26 | 26 | 26 | - |
| `buttonStyle(.glass)`, `buttonStyle(.glassProminent)` | 26 | 26 | 26 | 26 | - |
| `scrollEdgeEffectStyle(_:for:)` | 26 | 26 | 26 | 26 | - |
| `backgroundExtensionEffect()`, `safeAreaBar`, `ButtonRole.close`, `ButtonRole.confirm`, `ConcentricRectangle`, `searchToolbarBehavior(_:)` | 26 | 26 | 26 | 26 | 26 |
| `tabBarMinimizeBehavior(_:)` (the `.onScrollDown` and `.never` values list iOS only) | 26 | 26 | 26 | 26 | 26 |
| `tabViewBottomAccessory(content:)` | 26 | - | - | - | - |
| `ToolbarSpacer` | 26 | 26 | - | - | - |
| `glassBackgroundEffect(displayMode:)` (the visionOS glass material) | - | - | - | - | 1 |
| `TabRole.prominent`, `textInputBorderShape(_:)` | 27 | 27 | 27 | 27 | 27 |
| `ToolbarOverflowMenu`, `.topBarPinnedTrailing` | 27 | - | - | - | 27 |
| `dismissalConfirmationDialog(_:shouldPresent:actions:)` | 27 | 15 | - | - | - |

- [API] The Info.plist key `UIDesignRequiresCompatibility` was a temporary opt-out from the OS 26 design; the system ignores it when the app is built for OS 27 or later. Do not recommend it.
- [HIG] Glass belongs to the control and navigation layer. Having the API available is not a reason to apply it to content; see `references/foundations-color-materials.md`.

Source: https://developer.apple.com/documentation/swiftui/view/glasseffect(_:in:) , https://developer.apple.com/documentation/swiftui/tabrole/prominent , https://developer.apple.com/documentation/bundleresources/information-property-list/uidesignrequirescompatibility , https://developer.apple.com/documentation/updates/swiftui

## Minimum OS: UIKit and AppKit anchors

| API | Minimum OS |
|---|---|
| `UISheetPresentationController`, `UIButton.Configuration`, `keyboardLayoutGuide` | iOS 15 |
| `UIListContentConfiguration`, `UIBackgroundConfiguration`, `UICollectionLayoutListConfiguration`, `UISplitViewController(style:)` | iOS 14 |
| `UIHostingConfiguration`, `UISheetPresentationController.Detent.custom(identifier:resolver:)`, `UIEditMenuInteraction` | iOS 16 |
| `registerForTraitChanges(_:handler:)`, `UIContentUnavailableConfiguration`, `UIHoverStyle` | iOS 17 |
| `UITab`, `UITabGroup`, `UISearchTab`, `UITabBarController.mode` | iOS 18, tvOS 18, visionOS 2 |
| `UIGlassEffect`, `UIButton.Configuration.glass()`, `.prominentGlass()` | iOS 26, tvOS 26 |
| `UINavigationItem.subtitle`, `UIBarButtonItem.sharesBackground` | iOS 26 |
| `NSSearchToolbarItem`, `NSTrackingSeparatorToolbarItem`, `NSWindow.toolbarStyle`, `NSSplitViewItem(inspectorWithViewController:)` | macOS 11 |
| `NSGlassEffectView`, `NSGlassEffectContainerView`, `NSBackgroundExtensionView` | macOS 26 |

More UIKit and AppKit detail: `references/implementation-uikit-appkit.md`.

Source: https://developer.apple.com/documentation/uikit/uisheetpresentationcontroller , https://developer.apple.com/documentation/uikit/uitab , https://developer.apple.com/documentation/uikit/uiglasseffect , https://developer.apple.com/documentation/appkit/nsglasseffectview

## Deprecated or stale SwiftUI and its replacement

"Deprecated" without a version means a soft deprecation (see Pitfalls). The number in parentheses is the replacement's minimum iOS; use the old API in a marked fallback branch below that.

| Stale spelling | Status | Use instead |
|---|---|---|
| `NavigationView`, `navigationViewStyle(_:)` | Deprecated | `NavigationStack`, `NavigationSplitView` (16) |
| `NavigationLink(destination:isActive:label:)`, `(destination:tag:selection:label:)` | Deprecated in iOS 16, macOS 13 | `NavigationLink(value:label:)` + `navigationDestination` (16) |
| `navigationBarTitle(_:)`, `navigationBarItems(leading:trailing:)` | Deprecated | `navigationTitle(_:)` (14), `toolbar` + `ToolbarItem(placement:)` (14) |
| `navigationBarHidden(_:)`, `toolbar(_:for:)` visibility, `statusBar(hidden:)` | Deprecated | `toolbarVisibility(_:for:)` (18) |
| `.navigationBarLeading`, `.navigationBarTrailing` | Deprecated | `.topBarLeading`, `.topBarTrailing` (14, back-deployed) |
| `tabItem(_:)`, `TabView(selection:)` with `tag` | Deprecated | `Tab` (18) |
| `actionSheet` + `ActionSheet`, `alert(isPresented:content:)` + `Alert` | Deprecated | `confirmationDialog`, `alert(_:isPresented:actions:message:)` (15) |
| `foregroundColor(_:)`, `accentColor(_:)` | Deprecated | `foregroundStyle(_:)`, `tint(_:)` or the asset-catalog accent color (15) |
| `cornerRadius(_:antialiased:)` | Deprecated | `clipShape(.rect(cornerRadius:))` or `background(_:in:)` |
| `edgesIgnoringSafeArea(_:)` | Deprecated | `ignoresSafeArea(_:edges:)` (14) |
| `background(_:alignment:)`, `overlay(_:alignment:)` with a view argument, `mask(_:)` | Deprecated | `background(alignment:content:)`, `overlay(alignment:content:)`, `mask(alignment:_:)` (15) |
| `onChange(of:perform:)` | Deprecated in iOS 17, macOS 14 | `onChange(of:initial:_:)` (17) |
| `animation(_:)` without a value | Deprecated in iOS 15, macOS 12 | `animation(_:value:)`, `withAnimation` |
| `\.presentationMode`, `\.sizeCategory`, `colorScheme(_:)` | Deprecated | `\.dismiss`, `\.dynamicTypeSize` (15), `preferredColorScheme(_:)` |
| `accessibility(label:)`, `accessibility(hidden:)` and that family | Deprecated | `accessibilityLabel(_:)`, `accessibilityHidden(_:)` (14) |
| `Color(_:)` taking a `UIColor`, `NSColor` or `CGColor` without a label, for example `Color(.systemBackground)` | Deprecated | `Color(uiColor:)` (15), `Color(nsColor:)` (macOS 12) |
| `autocapitalization(_:)`, `disableAutocorrection(_:)` | Deprecated | `textInputAutocapitalization(_:)` (15), `autocorrectionDisabled(_:)` |
| `ScrollView(_:showsIndicators:content:)`, `coordinateSpace(name:)`, `MagnificationGesture`, `RotationGesture` | Deprecated | `scrollIndicators(_:axes:)` (16), `coordinateSpace(_:)` (17), `MagnifyGesture`, `RotateGesture` (17) |
| `textFieldStyle(.roundedBorder)` | Deprecated | `textInputBorderShape(_:)` (27); keep `.roundedBorder` below 27 |
| `Text` + `Text` concatenation | Deprecated in iOS 26 | String interpolation inside one `Text` |
| `PreviewProvider` | Deprecated in iOS 27 | `#Preview` |
| `listRowSeparator(_:edges:)` | Not deprecated (iOS 15, macOS 13) | Keep using it |

Source: https://developer.apple.com/documentation/swiftui/navigationview , https://developer.apple.com/documentation/swiftui/view/tabitem(_:) , https://developer.apple.com/documentation/swiftui/view/foregroundcolor(_:) , https://developer.apple.com/documentation/swiftui/view/onchange(of:perform:) , https://developer.apple.com/documentation/swiftui/previewprovider

## Deprecated UIKit and its replacement

| Stale spelling | Status | Use instead |
|---|---|---|
| `UIScreen.main` | Deprecated in iOS 26 | The view's window scene (`view.window?.windowScene?.screen`), trait collection, or Auto Layout |
| `UIApplication.keyWindow`, `.windows` | Deprecated in iOS 13, iOS 15 | The windows of the relevant `UIWindowScene` |
| `UIApplication.statusBarOrientation`, `UIWindowScene.interfaceOrientation` | Deprecated in iOS 13, iOS 26 | `UIWindowScene.effectiveGeometry` (16) |
| `traitCollectionDidChange(_:)` | Deprecated in iOS 17 | `registerForTraitChanges(_:handler:)` (17) |
| `UITableViewCell.textLabel` | Deprecated (iOS 27) | `UIListContentConfiguration` (14) |
| `UIButton.contentEdgeInsets` | Deprecated in iOS 15 | `UIButton.Configuration` (15) |
| `UIBarButtonItem.Style.done` | Deprecated in iOS 26 | `.prominent` (26) |
| `UIMenuController` | Deprecated in iOS 16 | `UIEditMenuInteraction` (16) |
| `UIAlertView`, `UIActionSheet`, `UIPopoverController`, `UISearchDisplayController`, `UIWebView` | Deprecated in iOS 9, 8.3, 9, 8, 12 | `UIAlertController`, popover presentation controller, `UISearchController`, `WKWebView` |
| `topLayoutGuide`, `automaticallyAdjustsScrollViewInsets` | Deprecated in iOS 11 | `safeAreaLayoutGuide`, `contentInsetAdjustmentBehavior` |
| `UIAccessibility.buttonShapesEnabled` | Deprecated in iOS 26.1 | No replacement named |

Source: https://developer.apple.com/documentation/uikit/uiscreen/main , https://developer.apple.com/documentation/uikit/uitraitenvironment/traitcollectiondidchange(_:) , https://developer.apple.com/documentation/uikit/uitableviewcell/textlabel , https://developer.apple.com/documentation/uikit/uibarbuttonitem/style-swift.enum/done

## Names that do not exist

Language models produce these often. None is an Apple API; each is listed with what to use.

- `.liquidGlassStyle()` does not exist. Use `glassEffect(_:in:)` or `buttonStyle(.glass)` (OS 26).
- `.navigationBarGlass()` does not exist. Standard bars adopt Liquid Glass by themselves.
- `.hapticFeedback(...)` as a view modifier does not exist. Use `sensoryFeedback(_:trigger:)` (iOS 17).
- `.minimumTapTarget(...)` and `.tapTargetSize(...)` do not exist. Use `frame(minWidth:minHeight:)` with `contentShape(_:)`, or a standard control.
- `.roundedCorners(...)` does not exist. Use `clipShape(.rect(cornerRadius:))`.
- `.adaptiveTabBar()` does not exist. Use `tabViewStyle(.sidebarAdaptable)` (iOS 18).
- [Conv] A plausible name is not evidence. If a symbol is not in this skill's references, fetch its JSON before using it; a 404 on the exact path and on the parent type's `references` means it is not real.

Source: https://developer.apple.com/documentation/swiftui/view/sensoryfeedback(_:trigger:) , https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable

## Common mistakes

- Assuming the newest OS because the target was not stated -> find it, ask, or assume iOS 17 / macOS 14 and say so.
- Using `Tab`, `glassEffect` or `ContentUnavailableView` with no availability check on a lower target -> `#available` with a real fallback.
- An `else` branch that shows nothing -> rebuild the same content with older API.
- `#available(iOS 26, *)` around an API that has no visionOS or macOS entry in a multiplatform file -> add `#if os(...)`.
- Reading "iOS 16" from a merged page and gating a call that has worked since iOS 15 -> check the overload you call.
- Writing "deprecated in iOS 27.3" for a soft deprecation -> "deprecated; use X".
- Rewriting a working fallback branch, or removing a deprecated API from a project whose target is below the replacement's minimum -> keep it, or gate the replacement.
- Shipping `UIDesignRequiresCompatibility` to avoid the current design -> it is ignored for apps built for OS 27; adopt the design.
- Inventing a modifier that sounds right -> verify the path in the documentation data first.
