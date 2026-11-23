# 03 — SwiftUI & implementation: mapping HIG guidance to real APIs

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Research date 2026-11-23. Agent 3 (SwiftUI and Implementation Specialist).

## 0. Method, sources, caveats (read first)

- **Source of truth**: Apple DocC render JSON, `https://developer.apple.com/tutorials/data/documentation/<path>.json`
  (human page: `https://developer.apple.com/documentation/<path>`). Every symbol below was fetched in this session and its
  name, declaration, `metadata.platforms[].introducedAt/deprecatedAt` read from JSON. Rows are **[V]** unless tagged **[M]**.
  The `<path>` is the lowercase symbol path, e.g. `swiftui/view/presentationdetents(_:)`, `uikit/uifontmetrics`.
- HIG statements: `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json` (fetched; cited as `HIG:<slug>`).
- **No Swift compiler in this environment.** Nothing here was compiled. Examples only use symbols/labels whose declaration
  was read from the docs, and stay deliberately plain. The skill should say the same and tell agents to build before claiming success.
- Availability shorthand: `i`=iOS (iPadOS and Mac Catalyst identical unless noted), `m`=macOS, `tv`, `w`=watchOS, `v`=visionOS.
  A missing platform letter means the docs list no availability for it (treat as unavailable).
- **Overloads**: Apple now merges overloads on one page; the default page often shows the newest overload
  (e.g. `LocalizedStringResource`, iOS 16). I followed `otherDeclarations` and report the **earliest** overload
  (usually the `LocalizedStringKey`/`StringProtocol` one). Do not conclude "iOS 16+" from the landing page alone.
- **Current SDK generation is 27** (iOS/iPadOS/macOS/tvOS/watchOS/visionOS 27, Xcode 27; SwiftUI "June 2026" + "September 2026"
  update notes at `documentation/updates/swiftui`). Liquid Glass shipped in the 26 releases (June 2025 notes).
- **Metadata quirks to know** (do not over-trust a single number):
  - Back-deployed symbols show the back-deployed version: `ToolbarItemPlacement.topBarTrailing` shows i14 with
    `@backDeployed(before: iOS 17.0)`; `Button(_:systemImage:action:)` shows i14; `Animation.snappy/smooth/bouncy` show i13.
  - A large batch of long "soft-deprecated" SwiftUI API now carries **`deprecatedAt: 27.3`** (see section 8). The JSON is
    unambiguous about the number; what the compiler does at lower deployment targets is not verified here **[M]**.
  - `EnvironmentValues.accessibilityShowButtonShapes` carries `deprecatedAt: 1000.0` (placeholder; treat as "discouraged, no version").

---

## 1. Navigation and presentation

### 1.1 Structure

| API | Availability | Notes |
|---|---|---|
| `NavigationStack` (`init(root:)`, `init(path:root:)`) | i16 m13 tv16 w9 v1 | Push/pop hierarchy. Path is `NavigationPath` or a typed collection. |
| `NavigationPath` | i16 m13 tv16 w9 v1 | Type-erased path. |
| `navigationDestination(for:destination:)` | i16 m13 tv16 w9 v1 | Pair with `NavigationLink(value:label:)` / `NavigationLink(_:value:)` (i16). |
| `navigationDestination(isPresented:destination:)` | i16 m13 | Boolean-driven push. |
| `navigationDestination(item:destination:)` | **i17** m14 tv17 w10 v1 | Optional-item push. Commonly assumed to be iOS 16; it is not. |
| `NavigationSplitView` (`init(sidebar:detail:)`, `init(sidebar:content:detail:)`, `init(columnVisibility:…)`, `init(preferredCompactColumn:…)`) | i16 m13 tv16 w9 v1 | Docs: on watchOS/tvOS and "narrow sizes like on iPhone or on iPad in Slide Over" it **collapses all columns into a stack** automatically. So one split view already gives "stack on compact, split on regular". |
| `navigationSplitViewStyle(_:)`, `navigationSplitViewColumnWidth(_:)` / `(min:ideal:max:)`, `NavigationSplitViewVisibility` | i16 m13 | |
| `NavigationView`, `navigationViewStyle(_:)` | i13, **deprecatedAt 27.3** (all platforms) | Message: "use NavigationStack or NavigationSplitView instead". |
| `NavigationLink(destination:isActive:label:)`, `…(destination:tag:selection:label:)` | **deprecated i16 / m13 / w9** | Hard-deprecated since 16. Use value links + `navigationDestination`. |
| `navigationTitle(_:)` | i14 m11 tv14 w7 (Key/String/Text overloads) | `Binding<String>` overload i16 (editable title). |
| `navigationBarTitleDisplayMode(_:)` | i14 w8 v1 (**no macOS/tvOS**) | Wrap in `#if os(iOS)` for multiplatform code. `toolbarTitleDisplayMode(_:)` is i17 m14 tv17 w10. |
| `navigationSubtitle(_:)` | **i26**, m13 | Was macOS-only before 26. |
| `inspector(isPresented:content:)`, `inspectorColumnWidth(_:)` | i17 m14 (no tv/w/v listed) | Trailing column on regular width; sheet on compact [M for the compact behaviour]. |
| `@Environment(\.dismiss)` (`DismissAction`) | i15 m12 tv15 w8 v1 | `presentationMode` is deprecatedAt 27.3. |

### 1.2 Tabs

| API | Availability | Notes |
|---|---|---|
| `TabView` | i13 m10.15 tv13 w7 v1 | |
| `Tab` (`init(_:systemImage:content:)`, `init(_:systemImage:value:content:)`, `…role:content:` variants, `init(value:content:)`, `init(role:content:)`) | **i18 m15 tv18 w11 v2** | `TabView(selection:content:)` with `Tab` content is i18; the old `TabView(selection:)` + `.tag` initializer is deprecatedAt 27.3. |
| `tabItem(_:)` | i13, **deprecatedAt 27.3** (not marked on visionOS) | Message: "Use `Tab(title:image:value:content:)` and related initializers instead". |
| `TabRole.search` | i18 m15 tv18 w11 v2 | In the 26 design the search tab is separated at the trailing end and a search field replaces the tab bar (SwiftUI June 2025 notes; HIG:tab-bars, HIG:search-fields). |
| `TabRole.prominent` | **i27** m27 tv27 w27 v27 | Places the tab in a separate trailing position (June 2026 notes). |
| `TabSection` | i18 m15 tv18 w11 v2 | Hierarchy for sidebar-adaptable tab views. |
| `tabViewStyle(_:)` | i14 m11 tv14 w7 v1 | `.sidebarAdaptable` i18 m15 tv18 v2 (no watchOS); `.tabBarOnly` i18 m15 tv18 v2; `.page` i14 tv14 w7 v1 (no macOS); `.verticalPage` w10; `.grouped` m15 only. |
| `TabViewCustomization`, `tabViewCustomization(_:)` | i18 m15 v2 | User-customisable sidebar tabs. |
| `tabBarMinimizeBehavior(_:)` / `TabBarMinimizeBehavior` | **i26** m26 tv26 w26 v26 (type) | Values: `.automatic` (all), `.onScrollDown` and `.never` list **iOS 26 only**. |
| `tabViewBottomAccessory(content:)` | **i26** (iOS/iPadOS/Catalyst only) | `tabViewBottomAccessory(isEnabled:content:)` is i26.1. Read `\.tabViewBottomAccessoryPlacement` (i26) to adapt content. |
| `TabSearchActivation` | i26 | Configures search activation in the search tab. |
| `badge(_:)` on `Tab` (`TabContent`) | i18 m15 v2 | View `badge(_:)` is i15 m12. |
| UIKit: `UITab` i18, `UITabBarController.mode` i18, `.tabBarMinimizeBehavior` i26, `.bottomAccessory` i26 | | |

### 1.3 Toolbars

| API | Availability | Notes |
|---|---|---|
| `toolbar(content:)`, `ToolbarItem(placement:content:)`, `ToolbarItemGroup` | i14 m11 tv14 w7 v1 | |
| Semantic placements `.automatic`, `.primaryAction`, `.confirmationAction`, `.cancellationAction`, `.destructiveAction` | i14 m11 tv14 w7 v1 | Prefer these; the system positions them per platform. |
| `.principal`, `.navigation` | i14 m11 tv14 v1 (no watchOS) | |
| `.secondaryAction` | i16 m13 v1 | |
| `.topBarLeading`, `.topBarTrailing` | i14 (back-deployed before 17) tv14 w10 v1, **no macOS** | |
| `.bottomBar` | i14 tv18 w10 v1, no macOS | |
| `.keyboard` | i15 m12 | |
| `.navigationBarLeading`, `.navigationBarTrailing` | i14, **deprecatedAt 27.3** | Use `.topBarLeading` / `.topBarTrailing`. |
| `.topBarPinnedTrailing` | **i27** v27 | Stays pinned while other items overflow. |
| `ToolbarSpacer` | **i26 m26** | Visual break between Liquid Glass item groups. |
| `ToolbarOverflowMenu` | **i27** v27 | Send secondary actions straight to overflow. |
| `DefaultToolbarItem` | i26 m26 tv26 w26 v26 | |
| `toolbarRole(_:)`, `toolbarBackground(_:for:)` (ShapeStyle), `toolbarColorScheme(_:for:)` | i16 m13 | HIG:toolbars now says to *reduce* custom toolbar backgrounds and tinted controls. |
| `toolbarVisibility(_:for:)`, `toolbarBackgroundVisibility(_:for:)` | i18 m15 tv18 w11 v2 | Replace `toolbar(_:for:)` and the `Visibility` overload of `toolbarBackground` (both deprecatedAt 27.3). |
| `toolbar(removing:)` | i17 m14 | |

### 1.4 Search

| API | Availability | Notes |
|---|---|---|
| `searchable(text:placement:prompt:)` | **i15** m12 tv15 w8 v1 | `SearchFieldPlacement`: `.automatic`, `.toolbar` (no tvOS), `.sidebar` (i15 m12 v1), `.navigationBarDrawer` (i15 w8 v1, no macOS). |
| `searchable(text:isPresented:placement:prompt:)` | i17 m14 v1 | |
| `searchScopes(_:scopes:)` | i16 m13 tv16.4 v1 | |
| `searchSuggestions(_:)` | i16 m13 tv16 w9 v1 | |
| `\.isSearching`, `\.dismissSearch` | i15 m12 | Only valid inside the searchable hierarchy [M]. |
| `searchToolbarBehavior(_:)` | i26 | |
| `ContentUnavailableView.search`, `.search(text:)` | i17 m14 tv17 w10 v1 | Standard "no results" state. |

### 1.5 Modality

| API | Availability | Notes |
|---|---|---|
| `sheet(isPresented:onDismiss:content:)`, `sheet(item:onDismiss:content:)` | i13 m10.15 tv13 w6 v1 | |
| `presentationDetents(_:)`, `presentationDetents(_:selection:)`, `PresentationDetent` (`.medium`, `.large`, `.fraction(_:)`, `.height(_:)`) | i16 m13 tv16 w9 v1 | Takes a `Set<PresentationDetent>`. |
| `presentationDragIndicator(_:)` | i16 | |
| `presentationBackgroundInteraction(_:)`, `presentationCompactAdaptation(_:)`, `presentationBackground(_:)`, `presentationCornerRadius(_:)`, `presentationContentInteraction(_:)` | i16.4 m13.3 tv16.4 w9.4 v1 | |
| `presentationSizing(_:)` (`.form`, `.page`, …) | i18 m15 tv18 w11 v2 | |
| `interactiveDismissDisabled(_:)` | i15 m12 | |
| `fullScreenCover(isPresented:onDismiss:content:)` | i14 tv14 w7 v1, **no macOS** | |
| `popover(isPresented:attachmentAnchor:arrowEdge:content:)` | i13 m10.15 v1 (no tv/w) | On compact width a popover adapts to a sheet unless `presentationCompactAdaptation` says otherwise [M]. |
| `confirmationDialog(_:isPresented:titleVisibility:actions:)` and `…actions:message:`, `…presenting:actions:message:` | **i15** m12 tv15 w8 v1 | HIG:action-sheets — use for choices related to an intentional action; include Cancel for destructive choices. |
| `alert(_:isPresented:actions:)`, `…actions:message:`, `…presenting:actions:message:`, `alert(isPresented:error:actions:)` | **i15** m12 tv15 w8 v1 | |
| `alert(_:item:actions:)` / `…message:` | i15 metadata (listed as new in June 2026 notes; back-deployed) | Conservative choice: use `isPresented:presenting:`. |
| `alert(error:actions:)` with `Binding<E?>` | i15 for the `LocalizedError` form; another overload i27 | |
| `dismissalConfirmationDialog(_:shouldPresent:actions:)` | **i27**, m15 | |
| `alert(isPresented:content:)` + `Alert`, `actionSheet(isPresented:content:)` + `ActionSheet` | i13, **deprecatedAt 27.3** | |

HIG anchors [V]: sheets — Cancel on leading edge, Done on trailing edge of the top toolbar in iOS/iPadOS; always pair Done with
Cancel or Back; never show Cancel, Done and Back together (HIG:sheets). Alerts — use sparingly; do not alert for common undoable
actions even if destructive; never give the primary role to a destructive button (HIG:alerts, HIG:buttons). Tab bars — navigation
only, never actions; do not hide or disable tabs; avoid overflow (HIG:tab-bars). There is **no `navigation-bars` HIG page any more**
(slug 404s); navigation-bar guidance lives in HIG:toolbars.

---

## 2. Typography and Dynamic Type

| API | Availability | Notes |
|---|---|---|
| `Font` text styles `.largeTitle .title .headline .subheadline .body .callout .footnote .caption` | i13 m10.15 tv13 w6 v1 | |
| `.title2 .title3 .caption2` | i14 m11 tv14 w7 v1 | |
| `Font.TextStyle.extraLargeTitle`, `.extraLargeTitle2` | **visionOS 1 only** | Guard with `#if os(visionOS)`. |
| `Font.system(_:design:weight:)` (text style) | i16 m13 tv16 w9 v1 | Scales with Dynamic Type. |
| `Font.system(size:weight:design:)` | i13 (non-optional form deprecatedAt 27.3; optional form i16) | **Fixed size — does not scale** [M]; avoid for body content. |
| `Font.custom(_:size:relativeTo:)` | i14 m11 tv14 w7 v1 | Custom font that scales with the given text style. |
| `Font.custom(_:size:)` | i13 | Scales relative to body [M]. `Font.custom(_:fixedSize:)` (i14) never scales. |
| `fontWeight(_:)`, `bold(_:)` on View | i16 m13 | `fontDesign(_:)` i16.1. `Font.weight(_:)` i13, `Font.leading(_:)` i14. |
| `DynamicTypeSize`, `\.dynamicTypeSize`, `dynamicTypeSize(_:)` (single value and range overloads) | i15 m12 tv15 w8 v1 | Range overload caps/limits the size for a subtree; use sparingly and never to disable scaling. |
| `DynamicTypeSize.isAccessibilitySize` | i15 | Switch layout at accessibility sizes. |
| `\.sizeCategory`, `ContentSizeCategory` | i13, **deprecatedAt 27.3** | Use `dynamicTypeSize`. |
| `@ScaledMetric` (`init(wrappedValue:)`, `init(wrappedValue:relativeTo:)`) | i14 m11 tv14 w7 v1 | Scale icon sizes, paddings, custom control dimensions with text. |
| `ViewThatFits` (`init(in:content:)`) | i16 m13 tv16 w9 v1 | Picks the first child that fits. |
| `AnyLayout`, `HStackLayout`, `VStackLayout`, `Layout` | i16 m13 tv16 w9 v1 | Switch axis without losing view identity. |
| `lineLimit(_:)` | Int i13; range overloads i16; `lineLimit(_:reservesSpace:)` i16 | |
| `minimumScaleFactor(_:)`, `truncationMode(_:)`, `fixedSize(horizontal:vertical:)` | i13 | |
| `monospacedDigit()` | i15 | Stable numeric columns. |
| `accessibilityShowsLargeContentViewer()` / `(_:)` | i15 m12 tv15 w8 v1 | For bar-like items that must not grow. `\.accessibilityLargeContentViewerEnabled` i15. |
| UIKit `UIFont.preferredFont(forTextStyle:)` | i7 | |
| UIKit `adjustsFontForContentSizeCategory` (`UIContentSizeCategoryAdjusting`) | i10 | Must be `true` for live updates. |
| UIKit `UIFontMetrics` (`scaledFont(for:)`, `scaledValue(for:)`) | i11 tv11 w4 v1 | Custom fonts and metrics. |
| UIKit `UIContentSizeCategory.isAccessibilityCategory` | i11 | `UITraitCollection.preferredContentSizeCategory` i10. |
| UIKit `minimumContentSizeCategory` / `maximumContentSizeCategory` on `UIView` | i15 | |
| UIKit `UILargeContentViewerInteraction`, `showsLargeContentViewer`, `largeContentTitle` | i13 | |
| AppKit `NSFont.preferredFont(forTextStyle:options:)` | m11 | macOS has text styles but **no Dynamic Type** (HIG:typography lists Dynamic Type for iOS, iPadOS, tvOS, visionOS, watchOS). |

HIG anchors [V]: default/minimum sizes table (iOS minimum 11 pt), avoid Ultralight/Thin/Light weights, prefer built-in text
styles, custom fonts must implement Dynamic Type and Bold Text behaviour (HIG:typography). "Ideally, give people the option to
enlarge text by at least 200 percent (or 140 percent in watchOS apps)" (HIG:accessibility). Layout must adapt to text-size
changes (HIG:layout).

---

## 3. Color, Dark Mode, materials, Liquid Glass

### 3.1 Semantic styles and colors

| API | Availability | Notes |
|---|---|---|
| `foregroundStyle(_:)`, `foregroundStyle(_:_:)` | i15 m12 tv15 w8 v1 | `foregroundColor(_:)` (View and Text) is deprecatedAt 27.3. |
| `ShapeStyle.primary` and `.secondary/.tertiary/.quaternary` (type properties) | i15 m12 | `.quinary` exists too (see `shapestyle/quinary-swift.type.property`). Instance forms (e.g. `.tint.secondary`) are separate symbols. |
| `ShapeStyle.tint` | i15 | Current tint / accent. |
| `ShapeStyle.background` (`BackgroundStyle`) | i14 | `backgroundStyle(_:)` i16. |
| `.separator`, `.placeholder`, `.link`, `.fill`, `.windowBackground` | i17 m14 tv17 w10 (`separator` m10.15; `windowBackground` not visionOS) | |
| `.selection` | i15 m12 v1 | |
| `background(_:ignoresSafeAreaEdges:)`, `background(_:in:fillStyle:)`, `background(alignment:content:)`, `overlay(alignment:content:)` | i15 | The `background(_:alignment:)` / `overlay(_:alignment:)` view-argument forms are deprecatedAt 27.3. |
| `Color.primary`, `Color.secondary`, `Color.accentColor` | i13 | |
| `Color(uiColor:)` | i15 tv15 w8 v1 | e.g. `Color(uiColor: .systemBackground)`. |
| `Color(nsColor:)` | m12 | |
| `Color(_: UIColor)` / `Color(_: NSColor)` / `Color(_: CGColor)` unlabelled | i13 / m10.15 / i14, **deprecatedAt 27.3** | `Color(.systemBackground)` is the unlabelled UIColor form: now flagged. Prefer `Color(uiColor:)`. |
| `Color(_:bundle:)` (asset name) | i13 | Stringly typed. |
| `Color(_ resource: ColorResource)`; `ColorResource` (DeveloperToolsSupport) | i17 m14 tv17 w10 v1 | Xcode-generated asset symbols, e.g. `Color(.brandPrimary)` [M for generated-name syntax]. |
| `tint(_:)` | i15 m12 tv15 w8 v1 | |
| `accentColor(_:)` modifier | i13, **deprecatedAt 27.3** | Message: use the asset catalog's accent color or `tint(_:)`. |
| `\.colorScheme`, `ColorScheme` | i13 | Read-only use is fine. `colorScheme(_:)` modifier deprecatedAt 27.3. |
| `preferredColorScheme(_:)` | i13 m11 | HIG:dark-mode: "Avoid offering an app-specific appearance setting". |
| `\.colorSchemeContrast` (`ColorSchemeContrast`) | i13 | Increase Contrast. |
| `Color.mix(with:by:in:)` | i18 m15 | `Color.resolve(in:)` i17. |
| UIKit `UIColor.label/.secondaryLabel/.separator/.link/.placeholderText` | i13 tv13 v1 | |
| UIKit `UIColor.systemBackground/.secondarySystemBackground/.systemGroupedBackground/.systemFill` | i13 v1 (**no tvOS listed**) | |
| UIKit `UIColor.tintColor` (class var) | i15 | `UIView.tintColor` i7. `UIColor(dynamicProvider:)` i13. |
| UIKit `overrideUserInterfaceStyle`, `UITraitCollection.userInterfaceStyle`, `.accessibilityContrast`, `.legibilityWeight` | i13 / i12 / i13 / i13 | |
| AppKit `NSColor.labelColor`, `.windowBackgroundColor`, `.textBackgroundColor`, `.controlBackgroundColor`, `.separatorColor`, `.controlAccentColor` | macOS (separator/accent 10.14) | `NSAppearance`, `NSApplication.appearance` m10.14. |

HIG anchors [V]: do not redefine semantic meanings of dynamic system colors; do not rely solely on color (HIG:color). Custom
colors go in an asset-catalog Color Set with light/dark variants; "Avoid using hard-coded color values or colors that don't
adapt"; contrast no lower than 4.5:1, strive for 7:1 for custom colors in small text (HIG:dark-mode, HIG:accessibility).

### 3.2 Materials (content layer)

`Material` (`.ultraThin .thin .regular .thick .ultraThick`) i15 m12 tv15 w10 v1; `.bar` i15 m12 v1. As ShapeStyle:
`.regularMaterial`, `.thinMaterial`, `.ultraThinMaterial`, `.thickMaterial`, `.ultraThickMaterial`. UIKit `UIVisualEffectView` +
`UIBlurEffect` i8; AppKit `NSVisualEffectView` m10.10. visionOS: `glassBackgroundEffect(displayMode:)` v1.
HIG:materials [V]: two kinds of material — Liquid Glass (controls/navigation layer) and standard materials (content layer).
"Don't use Liquid Glass in the content layer"; choose materials by semantic purpose, not apparent color.

### 3.3 Liquid Glass (26+)

| API | Availability | Notes |
|---|---|---|
| `glassEffect(_:in:)` — `func glassEffect(_ glass: Glass = .regular, in shape: some Shape = DefaultGlassEffectShape())` | i26 m26 tv26 w26 (**not visionOS**) | Custom views only. |
| `Glass` (`.regular`, `.clear`, `.identity`, `.tint(_:)`, `.interactive(_:)`) | i26 m26 tv26 w26 | HIG: only use clear over visually rich backgrounds. |
| `GlassEffectContainer` | i26 m26 tv26 w26 | Group nearby glass shapes so they blend/morph. |
| `glassEffectID(_:in:)`, `glassEffectUnion(id:namespace:)`, `glassEffectTransition(_:)` | i26 m26 tv26 w26 | |
| `buttonStyle(.glass)`, `buttonStyle(.glassProminent)` (`GlassButtonStyle`, `GlassProminentButtonStyle`) | i26 m26 tv26 w26 | |
| `backgroundExtensionEffect()` | i26 m26 tv26 w26 v26 | Mirror/blur content under sidebars and inspectors (HIG:layout). |
| `scrollEdgeEffectStyle(_:for:)`, `scrollEdgeEffectHidden(_:for:)`, `ScrollEdgeEffectStyle` | i26 m26 tv26 w26 | HIG: prefer scroll edge effect over solid bar backgrounds. |
| `safeAreaBar(edge:alignment:spacing:content:)` | i26 m26 tv26 w26 v26 | Custom bar that participates in the edge effect [M for behaviour]. |
| `ConcentricRectangle`, `containerShape(_:)` (rounded-rect overload) | i26 | Concentric corners. (`containerShape` generic overload is i15.) |
| `ButtonRole.close`, `ButtonRole.confirm`, `Button(role:action:)` | i26 m26 tv26 w26 v26 | System-styled Close/Confirm buttons. |
| `buttonSizing(_:)` | i26 | |
| UIKit `UIGlassEffect`, `UIGlassContainerEffect` | i26 tv26 | Used with `UIVisualEffectView`. |
| UIKit `UIButton.Configuration.glass()`, `.prominentGlass()` | i26 tv26 | |
| UIKit `UIScrollEdgeEffect`, `UIScrollView.topEdgeEffect`, `UIBackgroundExtensionView` | i26 tv26 v26 | |
| UIKit `UIBarButtonItem.sharesBackground`, `.hidesSharedBackground`, `UIBarButtonItem.Style.prominent` | i26 | `UIBarButtonItem.Style.done` is **deprecated in 26.0**. |
| AppKit `NSGlassEffectView`, `NSGlassEffectContainerView`, `NSBackgroundExtensionView` | m26 | |
| Info.plist `UIDesignRequiresCompatibility` | i26 m26 tv26 | Docs: temporary opt-out; **"The system ignores this key when you build for iOS 27 or later"** (also iPadOS, Mac Catalyst, macOS, tvOS 27). Do not recommend it for new work. |

Guidance [V] (`documentation/technologyoverviews/adopting-liquid-glass`, HIG:materials): standard components adopt the material
automatically when built with the current SDK; remove custom backgrounds from bars, tab bars, split views; apply glass effects
to custom controls sparingly; test with Reduce Transparency and Reduce Motion.

---

## 4. SF Symbols

| API | Availability | Notes |
|---|---|---|
| `Image(systemName:)` | i13 m11 tv13 w6 v1 | `Image(systemName:variableValue:)` i16. |
| `Label` (`init(_:systemImage:)`, `init(_:image:)`) | i14 m11 tv14 w7 v1 | Keeps a text title for VoiceOver even when only the icon shows. |
| `labelStyle(_:)` `.iconOnly`, `.titleOnly` | i14 | `.titleAndIcon` i14.5 m11.3 w7.4. |
| `symbolRenderingMode(_:)` `.monochrome .hierarchical .palette .multicolor` | i15 m12 tv15 w8 v1 | HIG:sf-symbols names the same four modes. |
| `symbolVariant(_:)` / `SymbolVariants` | i15 | e.g. `.fill`, `.circle`, `.slash`. |
| `imageScale(_:)` / `Image.Scale` (`.small .medium .large`) | i13 m11 | Scales relative to the font. |
| Font-matched sizing: apply `font(_:)` to the image | i13 | Symbols take size and weight from the font [M for mechanism; HIG:typography confirms weight matching]. |
| `symbolEffect(_:options:value:)`, `symbolEffect(_:options:isActive:)`, `symbolEffectsRemoved(_:)` | i17 m14 tv17 w10 v1 | `BounceSymbolEffect` i17; `WiggleSymbolEffect` i18; `DrawOnSymbolEffect` i26. |
| `contentTransition(.symbolEffect(_:options:))` | i17 (`contentTransition` i16) | |
| `symbolColorRenderingMode(_:)`, `symbolVariableValueMode(_:)` | i26 | |
| UIKit `UIImage(systemName:)`, `UIImage.SymbolConfiguration` | i13 | |
| AppKit `NSImage(systemSymbolName:accessibilityDescription:)` | m11 | |
| `Image(decorative:bundle:)` | i13 | Hidden from accessibility. |

HIG:sf-symbols [V]: "Availability of individual symbols and features varies based on the version of the system you're targeting.
Symbols and symbol features introduced in a given year aren't available in earlier operating systems." A missing name renders
nothing and does not fail the build [M]. The skill must not assert that a symbol name exists; tell agents to check the SF Symbols
app for the name and its minimum OS. HIG:icons [V]: provide alternative text labels for custom interface icons.

---

## 5. Accessibility APIs

### 5.1 SwiftUI

| API | Availability | Notes |
|---|---|---|
| `accessibilityLabel(_:)`, `accessibilityValue(_:)`, `accessibilityHint(_:)` | i14 m11 tv14 w7 v1 | The `accessibility(label:)`-style family is deprecatedAt 27.3. |
| `accessibilityLabel(_:isEnabled:)` | i18 | |
| `accessibilityElement(children:)` — `.ignore` (default), `.combine`, `.contain` | i13 | |
| `accessibilityAddTraits(_:)`, `accessibilityRemoveTraits(_:)` | i14 | `AccessibilityTraits`: `.isButton .isHeader .isSelected` i13, `.isToggle` i17. |
| `accessibilityHidden(_:)` | i14 | |
| `accessibilityAction(_:_:)` (kind, default `.default`) | i13 | |
| `accessibilityAction(named:_:)` | i13 (Text) / i14 (Key/String) | Custom actions (e.g. mirror swipe actions). `accessibilityActions(_:)` i16. |
| `accessibilityAdjustableAction(_:)` | i13 | Handler gets `AccessibilityAdjustmentDirection` (`.increment`, `.decrement`). |
| `accessibilityRepresentation(representation:)` | i15 m12 tv15 w8 v1 | Replace a custom control's elements with those of a standard control. |
| `accessibilityRotor(_:entries:)` | i15 | |
| `accessibilitySortPriority(_:)` | i14 | Higher value is read first [M]. |
| `@AccessibilityFocusState`, `accessibilityFocused(_:)`, `accessibilityFocused(_:equals:)` | i15 | |
| `accessibilityHeading(_:)` | i15 | |
| `accessibilityInputLabels(_:)` | i14 | Voice Control names. |
| `accessibilityIdentifier(_:)` | i14 | UI tests only, not spoken. |
| `accessibilityCustomContent(_:_:importance:)` | i15 [M: earliest overload not resolved; landing page says i16] | |
| `accessibilityLabeledPair(role:id:in:)` | i14 | |
| `accessibilityIgnoresInvertColors(_:)` | i14 | Photos/video. |
| `accessibilityRespondsToUserInteraction(_:)` | i15 | |
| `accessibilityDirectTouch(_:options:)` | i17 | |
| `accessibilityZoomAction(_:)` i16, `accessibilityScrollAction(_:)` i13, `accessibilityChartDescriptor(_:)` i15, `accessibilityTextContentType(_:)` i15 | | |
| `AccessibilityNotification.Announcement(…).post()` (Accessibility framework) | i17 m14 tv17 w10 v1 | Also `.LayoutChanged`. Path `accessibility/accessibilitynotification`. |

Environment values (all read-only unless noted):

| Key | Availability |
|---|---|
| `\.accessibilityReduceMotion`, `\.accessibilityReduceTransparency`, `\.accessibilityDifferentiateWithoutColor`, `\.accessibilityInvertColors` | i13 m10.15 tv13 w6 v1 |
| `\.colorSchemeContrast` (`.standard` / `.increased`) | i13 |
| `\.legibilityWeight` (`LegibilityWeight`, Bold Text) | i13 |
| `\.accessibilityShowButtonShapes` | i14 m11; **marked deprecated (deprecatedAt 1000.0)** |
| `\.accessibilityEnabled` | i13 |
| `\.accessibilityVoiceOverEnabled`, `\.accessibilitySwitchControlEnabled` | i15 m12 |
| `\.accessibilityDimFlashingLights`, `\.accessibilityPlayAnimatedImages` | i17 m14 |
| `\.accessibilityAssistiveAccessEnabled` | i18 m15 |
| `\.accessibilityQuickActionsEnabled` | i16 |
| `\.dynamicTypeSize` | i15 |

### 5.2 UIKit / AppKit / testing

| API | Availability | Notes |
|---|---|---|
| `isAccessibilityElement`, `accessibilityLabel`, `accessibilityValue`, `accessibilityHint`, `accessibilityTraits` (NSObject informal protocol; path `objectivec/nsobject-swift.class/…`) | iOS (version not in metadata) | `UIAccessibilityTraits`. |
| `accessibilityCustomActions` / `UIAccessibilityCustomAction` | i8 | `UIAccessibilityCustomRotor` i10. |
| `UIAccessibility.post(notification:argument:)`; `.announcement`, `.layoutChanged`, `.screenChanged` | iOS | |
| `UIAccessibility.isVoiceOverRunning` i4, `.isReduceMotionEnabled` / `.isReduceTransparencyEnabled` / `.isBoldTextEnabled` / `.isDarkerSystemColorsEnabled` / `.isSwitchControlRunning` i8 | | |
| `UIAccessibility.shouldDifferentiateWithoutColor` i13, `.prefersCrossFadeTransitions` i14 | | |
| `UIAccessibility.buttonShapesEnabled` | i14, **deprecated 26.1** | |
| AppKit `NSAccessibilityProtocol` (`setAccessibilityLabel(_:)` m10.10), `NSAccessibility` | macOS | Standard AppKit controls are accessible by default [M]. |
| AppKit `NSWorkspace.accessibilityDisplayShouldReduceMotion` m10.12; `…ShouldIncreaseContrast`, `…ShouldReduceTransparency`, `…ShouldDifferentiateWithoutColor` m10.10 | | |
| `XCUIApplication.performAccessibilityAudit(for:_:)` | i17 m14 tv17 w10 | `func performAccessibilityAudit(for auditTypes: XCUIAccessibilityAuditType = .all, _ issueHandler: ((XCUIAccessibilityAuditIssue) throws -> Bool)? = nil) throws`. |
| `XCUIAccessibilityAuditType` `.contrast`, `.hitRegion`, `.sufficientElementDescription` (i17 m14), `.dynamicType` (i17 tv17 w10 — **not macOS**) | | More members exist; only these were checked. |
| Accessibility Inspector (Xcode tool) | — | HIG:accessibility recommends auditing with it. |

HIG:accessibility control-size table [V]: iOS/iPadOS default 44x44 pt, minimum 28x28; macOS 28x28 / 20x20; tvOS 66x66 / 56x56;
visionOS 60x60 / 28x28; watchOS 44x44 / 28x28. HIG:buttons: hit region at least 44x44 pt, 60x60 pt in visionOS.
HIG:motion: "Make motion optional".

---

## 6. Adaptive layout, windows, platform specifics

| API | Availability | Notes |
|---|---|---|
| `\.horizontalSizeClass`, `\.verticalSizeClass` (`UserInterfaceSizeClass?`: `.compact`, `.regular`) | i13; back-deployed before m14 / tv17 / w10 | Optional value. Prefer over device idiom checks. |
| `ViewThatFits`, `AnyLayout`, `Layout` | i16 m13 | See section 2. |
| `Grid`, `GridRow` | i16 m13 tv16 w9 v1 | Eager aligned grid. |
| `LazyVGrid`, `GridItem`, `GridItem.Size.adaptive(minimum:maximum:)` | i14 m11 | Column count follows width. |
| `GeometryReader` | i13 | Greedy; breaks intrinsic sizing. Alternatives: `containerRelativeFrame`, `ViewThatFits`, `onGeometryChange(for:of:action:)` (metadata i16 m13, back-deployed). |
| `containerRelativeFrame(_:alignment:)`, `containerRelativeFrame(_:count:span:spacing:alignment:)` | i17 m14 tv17 w10 v1 | |
| `safeAreaInset(edge:alignment:spacing:content:)` | i15 m12 | Pin bars without covering scroll content. |
| `safeAreaPadding(_:)` | i17 m14 | |
| `ignoresSafeArea(_:edges:)` | i14 m11 | Backgrounds only. `edgesIgnoringSafeArea(_:)` deprecatedAt 27.3. |
| `contentMargins(_:_:for:)` | i17 m14 | Inset scroll content, not the scroll view. |
| `scenePadding(_:)` | i15 m12 tv15 w8 v1 | Platform-appropriate edge padding. |
| `padding(_:_:)` with nil length | i13 | System default spacing. |
| `scrollBounceBehavior(_:axes:)` i16.4; `scrollDismissesKeyboard(_:)` i16 (no visionOS); `scrollContentBackground(_:)` i16 (no tvOS); `scrollIndicators(_:axes:)` i16; `scrollTargetBehavior(_:)` i17 | | `ScrollView(_:showsIndicators:content:)` deprecatedAt 27.3. |
| `\.layoutDirection` | i13 | RTL. Use leading/trailing, never left/right. |
| Readable width in SwiftUI | — | **No dedicated SwiftUI modifier found.** `List`/`Form` handle it; otherwise cap with `frame(maxWidth:)` [M]. UIKit has `readableContentGuide`. |
| UIKit `readableContentGuide`, `layoutMarginsGuide` i9; `safeAreaLayoutGuide` i11; `keyboardLayoutGuide` i15 | | |
| `UIScreen.main` | **deprecated 26.0** | Docs: "Apple discourages the use of this symbol. Use a UIScreen instance found through context" (`UIWindowScene.screen`). `UIWindowScene.effectiveGeometry` i16. |
| **ArrangementView**, `arrangementViewStyle(_:)`, split/overlay arrangement modifiers | 27 (Sept 2026 notes) | New adaptive primary/secondary container. Seen only in release notes; **not examined** — do not ship examples. |
| `ReservedRegion`, `onHingeChange(isEnabled:_:)`, `toolbarVerticalEdge` | 27 (Sept 2026 notes) | Foldable ("iPhone Duo") support; not examined. |

Scenes, windows, keyboard:

| API | Availability | Notes |
|---|---|---|
| `WindowGroup` | i14 m11 tv14 w7 v1 | Multiple windows on iPadOS/macOS/visionOS. |
| `Window` | m13, v26 | Single unique window. |
| `Settings` (`init(content:)`) | **macOS 11 only** | Wrap in `#if os(macOS)`. Enables the app-menu Settings item. `SettingsLink`, `\.openSettings` m14. |
| `MenuBarExtra` | m13 | `UtilityWindow` m15. `DocumentGroup` i14 m11 v1. |
| `commands(content:)`, `CommandMenu`, `CommandGroup(after:addition:)` / `(replacing:addition:)`, `CommandGroupPlacement` (`.newItem`, `.appSettings`, `.help`, …) | i14 m11 v1 | On iPadOS these feed the hardware-keyboard shortcut overlay / menu bar [M]. |
| `SidebarCommands`, `ToolbarCommands`, `TextEditingCommands` | i14 m11 v1 | `InspectorCommands` i17 m14. |
| `keyboardShortcut(_:modifiers:)` (default `.command`), `keyboardShortcut(_:)`, `.defaultAction`, `.cancelAction` | i14 m11 v1 (no tv/w) | |
| `defaultSize(width:height:)`, `windowResizability(_:)` | i17 m13 v1 | `windowStyle(_:)` m11 v1; `windowToolbarStyle(_:)` m11. |
| `\.openWindow` i16 m13 v1; `\.dismissWindow` i17 m14 v1; `\.supportsMultipleWindows` i16 | | |
| `onKeyPress(_:action:)` | i17 m14 tv17 v1 | |
| `help(_:)` (tooltip) | i14 m11 | |
| `Table`, `TableColumn` | i16 m12 v1 | Collapses to first column on compact width [M]. |

Focus / tvOS / watchOS / visionOS:

| API | Availability | Notes |
|---|---|---|
| `@FocusState`, `focused(_:)`, `focused(_:equals:)` | i15 m12 tv15 w8 v1 | |
| `focusable(_:)` | **i17**, m12, tv15, w8, v1 | `focusable(_:interactions:)` i17 m14 tv17 w10. |
| `focusSection()` | m13, tv15 only | Guides directional focus across gaps. |
| `defaultFocus(_:_:priority:)` | i17 m13 tv16 w9 v1 | `prefersDefaultFocus(_:in:)` + `focusScope(_:)` m12 tv14 w7. |
| `onMoveCommand(perform:)`, `onExitCommand(perform:)` | m10.15 tv13 | `onPlayPauseCommand(perform:)` tv13. |
| `buttonStyle(.card)` | tv14 | |
| `digitalCrownRotation(_:)` and `(_:from:through:by:sensitivity:isContinuous:isHapticFeedbackEnabled:)` | **watchOS 6 only** | Needs a focusable view [M]. |
| `tabViewStyle(.verticalPage)` | w10 | `.carousel` tab style deprecatedAt 27.3. `listStyle(.carousel)` w6, `.elliptical` w7. |
| `containerBackground(_:for:)` / `containerBackground(for:alignment:content:)` | i17 m14 tv17 w10 v1 | |
| `handGestureShortcut(_:isEnabled:)` | i18 m15 tv18 w11 | Double Tap on watchOS. |
| `ornament(visibility:attachmentAnchor:contentAlignment:ornament:)` | **visionOS 1 only** | |
| `windowStyle(.volumetric)` | v1 | |
| `ImmersiveSpace` | v1 | `\.openImmersiveSpace`, `immersionStyle(selection:in:)` v1 and m26. |
| `hoverEffect(_:)` | i13.4 tv16 v1 (**no macOS**) | `hoverEffect(_:isEnabled:)` i17. `onHover(perform:)` i13.4 m10.15 v1. `pointerStyle(_:)` m15 v2. |
| `contentShape(_:eoFill:)` i13; `contentShape(_:_:eoFill:)` (kinds) i15 | | Defines hit/hover shape. |
| `glassBackgroundEffect(displayMode:)` | v1 | |

---

## 7. Native controls

| API | Availability | Notes |
|---|---|---|
| `Button(_:action:)`, `Button(action:label:)` | i13 | |
| `Button(_:role:action:)`, `Button(role:action:label:)`; `ButtonRole.destructive`, `.cancel` | i15 m12 tv15 w8 v1 | `.confirm`, `.close` i26. |
| `buttonStyle(_:)` `.automatic`, `.plain` i13; `.borderless` i13 (tv17); `.bordered` i15 m10.15 tv13 w7; `.borderedProminent` i15 m12 tv15 w8; `.glass`, `.glassProminent` i26 | | HIG:buttons: prominent style for the most likely action; keep prominent buttons few. |
| `controlSize(_:)` / `ControlSize` | i15 m10.15 tv15 w9 v1 | `.extraLarge` i17. |
| `buttonBorderShape(_:)` | i15 m12 | `buttonRepeatBehavior(_:)` i17. |
| `Toggle` (`init(_:isOn:)`, `init(isOn:label:)`, `init(_:systemImage:isOn:)` i14) | i13 | `toggleStyle`: `.switch` i13 (tv18), `.button` i15 (no tvOS), `.checkbox` macOS only. |
| `Picker(_:selection:content:)` + `tag(_:)` | i13 | `pickerStyle`: `.segmented` i13 (no watchOS), `.menu` i14 m11 tv17, `.wheel` i13 w6 v1 (no macOS/tvOS), `.inline` i14, `.navigationLink` i16 (no macOS), `.palette` i17 m14, `.radioGroup` macOS only. |
| `Menu` (`init(_:content:)`, `init(_:systemImage:content:)`, `init(_:content:primaryAction:)` i15) | i14 m11 tv17 v1 (**no watchOS**) | `menuOrder(_:)` i16, `menuActionDismissBehavior(_:)` i16.4, `menuIndicator(_:)` i15. |
| `contextMenu(menuItems:)` | i13 m10.15 tv14 v1 (watchOS deprecated since 7) | `contextMenu(menuItems:preview:)` i16; `contextMenu(forSelectionType:menu:primaryAction:)` i16 m13. `contextMenu(_:)` + `ContextMenu` deprecatedAt 27.3. HIG:context-menus: items must also be available in the main interface. |
| `DatePicker` (`init(_:selection:displayedComponents:)`, `…in:…`) | i13 m10.15 w10 v1 (**no tvOS**) | Styles `.graphical` i14, `.compact` i14, `.wheel` i13 (no macOS). `MultiDatePicker` i16. |
| `Stepper(_:value:in:step:)` | i13 m10.15 w9 v1 (no tvOS) | |
| `Slider(value:in:step:)` | i13 m10.15 w6 v1 (no tvOS) | Tick marks appear automatically with `step` in 26. |
| `ColorPicker` | i14 m11 v1 | |
| `Form`, `Section(_:content:)` (i15), `Section(content:header:footer:)` (i13) | i13 | `formStyle(_:)` `.grouped`, `.columns` i16 m13. |
| `List`, `listStyle(_:)` `.plain` i13; `.grouped` i13 tv13 v1; `.insetGrouped` i14 v1 (**no macOS**); `.sidebar` i14 m10.15; `.inset` i14 m11; `.bordered` m12 | | |
| `swipeActions(edge:allowsFullSwipe:content:)` | i15 m12 w8 v1 (no tvOS) | Mirror with `accessibilityAction(named:)` when not using standard rows [M]. A container-agnostic variant with `onPresentationChanged` arrived in 27. |
| `refreshable(action:)` | i15 m12 | |
| `listRowSeparator(_:edges:)`, `listRowSeparatorTint(_:edges:)`, `listSectionSeparator(_:edges:)` | **i15 m13** v1 | Not deprecated. |
| `listRowInsets(_:)`, `listRowBackground(_:)` i13; `listSectionSpacing(_:)` i17 w10 v1; `listRowSpacing(_:)` i15 tv27 v1 | | |
| `onDelete(perform:)`, `onMove(perform:)`, `EditButton` (i13, no macOS) | | |
| `ProgressView` (`init(value:total:)`, `init(_:value:total:)`) | i14 m11 tv14 w7 v1 | |
| `Gauge`, `gaugeStyle(_:)` | i16 m13 w7 v1 (no tvOS) | |
| `ShareLink` | i16 m13 w9 v1 | |
| `PhotosPicker` (PhotosUI, `photosui/photospicker`) | i16 m13 w9 | No photo-library permission prompt needed [M]. |
| `PasteButton` i16 m10.15; `RenameButton` i16; `Link` i14; `\.openURL` i14 | | |
| `TextField(_:text:)` i13; `TextField(_:text:axis:)` i16; `TextField(_:text:prompt:)` i15; `TextField(_:value:format:prompt:)` i15 | | `SecureField` i13; `TextEditor` i14 m11 v1. |
| `textContentType(_:)` | `UITextContentType` overload i13; `NSTextContentType` overload m11 | Different parameter types per platform: guard with `#if`. |
| `keyboardType(_:)` | i13 tv13 v1 (**no macOS / watchOS**) | |
| `submitLabel(_:)`, `onSubmit(of:_:)` | i15 m12 | |
| `textInputAutocapitalization(_:)` | i15 tv15 w8 v1 | `autocapitalization(_:)` deprecatedAt 27.3. |
| `autocorrectionDisabled(_:)` | i13 metadata (back-deployed) | `disableAutocorrection(_:)` deprecatedAt 27.3. |
| `textFieldStyle(_:)` | i13 | `.roundedBorder` **deprecatedAt 27.3** (i/m); replacement `textFieldStyle(.bordered)` + `textInputBorderShape(.roundedRectangle)` is **27-only**. |
| `LabeledContent` (`init(_:value:)`, `init(_:content:)`) | i16 m13 tv16 w9 v1 | |
| `ControlGroup` | i15 m12 tv17 v1 | Styles `.navigation` i15, `.compactMenu` i16.4. |
| `DisclosureGroup`, `OutlineGroup` | i14 m11 v1 (no tv/w) | `GroupBox` i14 m10.15 v1. |
| `ContentUnavailableView` (`init(_:systemImage:description:)`, `init(label:description:actions:)`) | **i17** m14 tv17 w10 v1 | |
| `sensoryFeedback(_:trigger:)`, `SensoryFeedback` (`.success`, `.selection`, `.impact`, …) | i17 m14 tv17 w10, **visionOS 26** | UIKit: `UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator`, `UISelectionFeedbackGenerator` i10. HIG:playing-haptics: use system patterns per documented meaning. |
| `labelsHidden()` i13; `disabled(_:)` i13; `redacted(reason:)` i14; `selectionDisabled(_:)` i17 | | |

---

## 8. Platform availability, versioning, and stale API

### 8.1 Rules for the skill

1. **Find the deployment target before choosing APIs** (`IPHONEOS_DEPLOYMENT_TARGET` etc. in the project file,
   `platforms:` in `Package.swift`). If unknown, ask or state the assumption explicitly.
2. If the target is unknown and cannot be asked: write to the **previous-major floor that the project evidently uses**; otherwise
   default examples to iOS 17 / macOS 14 era API and gate anything newer. Label each snippet with its minimum OS.
3. Gate at the use site: `if #available(iOS 26, macOS 26, *) { … } else { … }`. Annotate declarations with
   `@available(iOS 18, macOS 15, *)`. Use `#if os(macOS)` for symbols that do not exist on a platform (e.g. `Settings`,
   `navigationBarTitleDisplayMode`, `keyboardType`). Syntax is standard Swift **[M]** (docs.swift.org was unreachable here).
4. `#available` is a runtime check, `#if os` is compile time; a modifier that is unavailable needs a small `ViewModifier`
   or helper function with the availability branch inside [M].
5. Never claim a symbol exists for a version from memory. Phrase as "requires iOS N (per Apple docs)"; if unverified, say so.
6. Prefer semantic API that degrades by itself (standard bars, `Label`, semantic placements) over version branches.
7. Always provide the `else` path with real UI, not an empty view.

### 8.2 Deprecated or commonly mis-remembered API (all [V] from JSON metadata)

| Stale / hallucinated | Status in docs | Use instead |
|---|---|---|
| `NavigationView`, `navigationViewStyle(_:)` | deprecatedAt **27.3** | `NavigationStack`, `NavigationSplitView` (i16) |
| `NavigationLink(destination:isActive:label:)`, `(destination:tag:selection:label:)` | deprecated **16.0** (m13, w9) | `NavigationLink(value:)` + `navigationDestination` |
| `navigationBarTitle(_:)`, `navigationBarTitle(_:displayMode:)` | deprecatedAt 27.3 | `navigationTitle(_:)` + `navigationBarTitleDisplayMode(_:)` |
| `navigationBarItems(leading:trailing:)` | deprecatedAt 27.3 | `toolbar` + `ToolbarItem(placement:)` |
| `navigationBarHidden(_:)` | deprecatedAt 27.3 | `toolbarVisibility(.hidden, for: .navigationBar)` (i18); `toolbar(.hidden, for:)` (i16) is itself deprecatedAt 27.3 |
| `.navigationBarLeading` / `.navigationBarTrailing` | deprecatedAt 27.3 | `.topBarLeading` / `.topBarTrailing` |
| `tabItem(_:)`; `TabView(selection:)` with `.tag` | deprecatedAt 27.3 | `Tab` (i18) |
| `accentColor(_:)` | deprecatedAt 27.3 | asset-catalog AccentColor, `tint(_:)` (i15) |
| `foregroundColor(_:)` (View and Text) | deprecatedAt 27.3 | `foregroundStyle(_:)` (i15) |
| `cornerRadius(_:antialiased:)` | deprecatedAt 27.3 | `clipShape(.rect(cornerRadius:))` (`clipShape(_:style:)` i13; `.rect(cornerRadius:style:)` i13 metadata) or `background(_:in:)` |
| `actionSheet(isPresented:content:)`, `ActionSheet` | deprecatedAt 27.3 | `confirmationDialog` (i15) |
| `alert(isPresented:content:)`, `alert(item:content:)`, `Alert` | deprecatedAt 27.3 | `alert(_:isPresented:actions:message:)` (i15) |
| `onChange(of:perform:)` (one-parameter closure) | deprecated **17.0** (m14, w10) | `onChange(of:initial:_:)` with zero or two closure parameters (i17) |
| `animation(_:)` without value | deprecated **15.0** (m12) | `animation(_:value:)` or `withAnimation` |
| `edgesIgnoringSafeArea(_:)` | deprecatedAt 27.3 | `ignoresSafeArea(_:edges:)` (i14) |
| `autocapitalization(_:)` | deprecatedAt 27.3 | `textInputAutocapitalization(_:)` (i15) |
| `disableAutocorrection(_:)` | deprecatedAt 27.3 | `autocorrectionDisabled(_:)` |
| `background(_:alignment:)`, `overlay(_:alignment:)` (view argument) | deprecatedAt 27.3 | `background(alignment:content:)`, `overlay(alignment:content:)` (i15) |
| `mask(_:)` | deprecatedAt 27.3 | `mask(alignment:_:)` (i15) |
| `colorScheme(_:)` modifier | deprecatedAt 27.3 | `preferredColorScheme(_:)` |
| `\.sizeCategory`, `ContentSizeCategory` | deprecatedAt 27.3 | `\.dynamicTypeSize`, `DynamicTypeSize` (i15) |
| `\.presentationMode` | deprecatedAt 27.3 | `\.dismiss`, `\.isPresented` (i15) |
| `accessibility(label:)`, `accessibility(hidden:)`, `accessibility(addTraits:)` … | deprecatedAt 27.3 | `accessibilityLabel(_:)` etc. (i14) |
| `Color(_: UIColor)`, `Color(_: NSColor)`, `Color(_: CGColor)` | deprecatedAt 27.3 | `Color(uiColor:)` (i15), `Color(nsColor:)` (m12), `Color(cgColor:)` |
| `Font.system(size:weight:design:)` non-optional overload | deprecatedAt 27.3 | optional-parameter overload (i16); better: text styles |
| `statusBar(hidden:)`, `statusBarHidden(_:)` | deprecatedAt 27.3 | `toolbarVisibility(_:for: .statusBar)` |
| `coordinateSpace(name:)` | deprecatedAt 27.3 | `coordinateSpace(_:)` taking `NamedCoordinateSpace` (i17) |
| `ScrollView(_:showsIndicators:content:)` | deprecatedAt 27.3 | `scrollIndicators(_:axes:)` (i16) |
| `MagnificationGesture`, `RotationGesture` | deprecatedAt 27.3 | `MagnifyGesture`, `RotateGesture` (i17) |
| `textFieldStyle(.roundedBorder)` | deprecatedAt 27.3 | `.bordered` + `textInputBorderShape(_:)` (27 only) — keep `.roundedBorder` below 27 |
| `Text + Text` concatenation | deprecated **26.0** | string interpolation: `Text("Hello \(name)")` |
| `PreviewProvider` | deprecated **27.0** | `#Preview` macro |
| `contextMenu(_:)` with `ContextMenu` | deprecatedAt 27.3 | `contextMenu(menuItems:)` |
| `dropDestination(for:action:isTargeted:)` | deprecatedAt 27.3 | newer drop API (not examined) |
| `listRowSeparator(_:edges:)` | **not deprecated**, i15 m13 | — (lore sometimes claims otherwise) |
| `UIScreen.main` | deprecated **26.0** | `view.window?.windowScene?.screen`, trait collection, SwiftUI layout |
| `UIApplication.keyWindow` / `.windows` | deprecated 13.0 / 15.0 | window scene's windows |
| `UIApplication.statusBarOrientation` | deprecated 13.0 | `UIWindowScene.interfaceOrientation` (itself deprecated 26.0 → `effectiveGeometry.interfaceOrientation`) |
| `traitCollectionDidChange(_:)` | deprecated **17.0** | `registerForTraitChanges(_:handler:)` (i17) |
| `UITableViewCell.textLabel` | deprecated (27.0 on iOS in metadata) | `UIListContentConfiguration` (i14) |
| `UIButton.contentEdgeInsets` | deprecated 15.0 | `UIButton.Configuration` (i15) |
| `UIBarButtonItem.Style.done` | deprecated 26.0 | `.prominent` (i26) |
| `UIMenuController` | deprecated 16.0 | `UIEditMenuInteraction` (i16) |
| `UIAlertView`, `UIActionSheet`, `UIPopoverController`, `UIWebView`, `UISearchDisplayController` | deprecated 9.0 / 8.3 / 9.0 / 12.0 / 8.0 | `UIAlertController`, popover presentation, `WKWebView`, `UISearchController` |
| `topLayoutGuide`, `automaticallyAdjustsScrollViewInsets` | deprecated 11.0 | `safeAreaLayoutGuide`; scroll-view inset adjustment [M] |
| `UIAccessibility.buttonShapesEnabled` | deprecated 26.1 | — |
| `UIDesignRequiresCompatibility` | ignored when building for 27 | adopt Liquid Glass |

Names that do **not** exist as written (404 in docs; do not emit): `ShapeStyle.secondary` as a plain path resolves only via
`-swift.type.property`; `View.task(priority:_:)` page is now `task(name:priority:file:line:_:)` (i15; call site
`.task { }` unchanged); `tag(_:)` is `tag(_:includeOptional:)` (call site `.tag(x)` unchanged).

---

## 9. When to drop to UIKit / AppKit

Drop down only when SwiftUI lacks the capability at the deployment target; wrap with `UIViewRepresentable` /
`UIViewControllerRepresentable` (i13) or `NSViewRepresentable` (m10.15), or host SwiftUI inside existing code with
`UIHostingController` (i13), `UIHostingConfiguration` (i16, cells), `NSHostingView` (m10.15). Typical reasons [M]: complex
collection layouts, text-system customisation, camera/map/web specifics, fine control of sheet or pointer behaviour, existing
UIKit codebases.

- **Navigation/search**: `UINavigationBar.prefersLargeTitles`, `UINavigationItem.largeTitleDisplayMode` i11; `UINavigationItem.subtitle` i26; `UISearchController` i8, `UINavigationItem.searchController` i11; `UITabBarController`, `UITab` i18, `UISplitViewController`.
- **Sheets**: `UISheetPresentationController` i15 (`detents`, `prefersGrabberVisible`, `Detent.medium()`), `Detent.custom(identifier:resolver:)` i16, `UIViewController.sheetPresentationController` i15.
- **Menus**: `UIMenu`, `UIAction` i13; `UIButton.menu` i14; `UIControl.showsMenuAsPrimaryAction` i14; `UIContextMenuInteraction`, `UIContextMenuConfiguration` i13 (tv17); `UIEditMenuInteraction` i16.
- **Pointer/hover**: `UIPointerInteraction`, `UIPointerStyle` i13.4; `UIHoverStyle` i17.
- **Lists/cells**: `UIListContentConfiguration`, `UIBackgroundConfiguration`, `UICollectionLayoutListConfiguration` i14; `UICollectionViewCompositionalLayout` i13; `UIContentUnavailableConfiguration` i17.
- **Buttons**: `UIButton.Configuration` (`.filled()`, `.bordered()`) i15; `.glass()`, `.prominentGlass()` i26.
- **Traits/layout**: `UITraitCollection` (`horizontalSizeClass` i8, `userInterfaceStyle` i12, `preferredContentSizeCategory` i10, `accessibilityContrast`, `legibilityWeight` i13); `registerForTraitChanges(_:handler:)` i17; `layoutMarginsGuide`, `readableContentGuide` i9; `safeAreaLayoutGuide` i11; `keyboardLayoutGuide` i15.
- **Keyboard**: `UIResponder.keyCommands`, `UIKeyCommand` i7. **Other**: `UICalendarView` i16, `UIColorWell` i14, `UIFindInteraction` i16, `UIScribbleInteraction` i14.
- **AppKit toolbar/sidebar**: `NSToolbar`, `NSToolbarItem`, `NSSearchToolbarItem` m11, `NSTrackingSeparatorToolbarItem` m11, `NSWindow.toolbarStyle` m11; `NSSplitViewController` m10.10, `NSSplitViewItem(sidebarWithViewController:)` m10.11, `NSSplitViewItem(inspectorWithViewController:)` m11.
- **AppKit menus/windows**: `NSMenu`, `NSMenuItem`, `NSUserInterfaceValidations`; `NSWindow.tabbingMode`, `.tabbingIdentifier`, `NSWindow.allowsAutomaticWindowTabbing` m10.12; `titlebarAppearsTransparent`, `NSTitlebarAccessoryViewController` m10.10.
- **AppKit misc**: `NSPopover` m10.7, `NSAlert`, `NSTableView`, `NSOutlineView`, `NSStatusItem`, `NSSharingServicePicker` m10.8, `NSVisualEffectView` m10.10, `NSDocument`.

---

## 10. Implementation anti-patterns (review checklist)

Sev: H = breaks accessibility/usability or HIG "don't"; M = HIG recommendation; L = convention. Sources are HIG slugs and API paths verified above.

| # | Anti-pattern | Native fix | Source | Sev |
|---|---|---|---|---|
| 1 | Hard-coded font sizes (`.font(.system(size: 14))`) for content | Text styles (`.body`, `.headline`); `Font.custom(_:size:relativeTo:)` for brand fonts | HIG:typography; `swiftui/font` | H |
| 2 | Fixed heights/widths around text (`.frame(height: 44)` on a row) | `frame(minHeight:)`, padding, `@ScaledMetric` | HIG:layout (be prepared for text-size changes) | H |
| 3 | `lineLimit(1)` + `minimumScaleFactor` to "fit" text | Allow wrapping; `ViewThatFits`; stack vertically at `isAccessibilitySize` | HIG:typography, HIG:accessibility (200%) | H |
| 4 | Capping Dynamic Type globally with `dynamicTypeSize(...)` range | Fix the layout; cap only bar-like chrome and add Large Content Viewer | HIG:accessibility; `accessibilityShowsLargeContentViewer` | H |
| 5 | Hard-coded colors (`Color(red:…)`, `.black`, `.white`, hex) for text/backgrounds | Semantic styles, asset Color Sets with dark variants | HIG:dark-mode, HIG:color | H |
| 6 | Using a semantic color for another purpose (separator as text) | Use each as intended | HIG:color | M |
| 7 | In-app light/dark toggle or forced `preferredColorScheme` | Follow system appearance | HIG:dark-mode | M |
| 8 | Status conveyed by color only (red/green dot) | Add symbol/shape/text; honor `accessibilityDifferentiateWithoutColor` | HIG:color, HIG:accessibility | H |
| 9 | `onTapGesture` on `Text`/`Image`/`HStack` as a button | `Button` (traits, focus, keyboard, hover, pressed state for free) | `swiftui/button`; HIG:buttons | H |
| 10 | Icon-only button with no accessible name (`Button { } label: { Image(systemName:) }`) | `Label("Add", systemImage:)` (toolbar shows icon), or `.accessibilityLabel` | HIG:icons, HIG:accessibility | H |
| 11 | Tap targets under 44x44 pt (60 visionOS) | Standard controls; padding + `contentShape`; `controlSize` | HIG:buttons, HIG:accessibility table | H |
| 12 | Custom tab bar (HStack of buttons at bottom) | `TabView` + `Tab`; gets Liquid Glass, sidebar adaptation, search role, minimise | HIG:tab-bars; `swiftui/tabview` | H |
| 13 | Tabs that trigger actions, or hiding/disabling tabs | Tabs navigate only; actions go in toolbars; show an empty state instead | HIG:tab-bars | M |
| 14 | Custom navigation bar / hand-drawn back button | `NavigationStack` + `toolbar`; standard Back/Close | HIG:toolbars | M |
| 15 | Custom bar backgrounds, tinted bar items, opaque bars | Remove; rely on system bars and scroll edge effect | HIG:toolbars; adopting-liquid-glass | M |
| 16 | `glassEffect` on content (cards, list rows) or everywhere | Standard materials in content; glass only for a few custom controls | HIG:materials | M |
| 17 | `.ignoresSafeArea()` on whole screens, content under notch/home indicator | Apply only to backgrounds; `safeAreaInset` for pinned bars | HIG:layout | H |
| 18 | `GeometryReader` wrapping screens for proportional sizing | Stacks, `Grid`, `containerRelativeFrame`, `ViewThatFits`, `Layout` | `swiftui/geometryreader` (greedy) [M]; HIG:layout | M |
| 19 | `UIScreen.main.bounds` for layout | Size classes, container-relative layout, window scene | `uikit/uiscreen/main` (deprecated 26.0) | H |
| 20 | Device checks (`UIDevice.current.userInterfaceIdiom == .pad`) for layout | `horizontalSizeClass`, `NavigationSplitView`, `ViewThatFits` | HIG:layout (size classes) | M |
| 21 | Fixed left/right padding or `.leading` hacks that break RTL; manual mirroring | Leading/trailing, `layoutDirection`, standard components | HIG:right-to-left, HIG:layout | M |
| 22 | Custom alert/sheet overlays (ZStack with dimmed background) | `alert`, `confirmationDialog`, `sheet`, `popover` | HIG:alerts, HIG:sheets, HIG:modality | H |
| 23 | Alert for every delete, or destructive button as default | Undo for common actions; `role: .destructive`, never primary | HIG:alerts, HIG:buttons | M |
| 24 | Sheet with no way out, or Done without Cancel | `.cancellationAction` + `.confirmationAction` items | HIG:sheets, HIG:modality | H |
| 25 | Actions only in context menu or swipe | Also expose in main UI / toolbar; add accessibility actions | HIG:context-menus | M |
| 26 | Animations that ignore Reduce Motion (parallax, large slides, spinning) | Check `accessibilityReduceMotion`; use fade/none | HIG:motion | H |
| 27 | Custom toggles/sliders/pickers drawn from shapes with no a11y | Standard control or custom `ToggleStyle`; else `accessibilityRepresentation` / adjustable action | `accessibilityrepresentation(representation:)` | H |
| 28 | Decorative images read by VoiceOver; meaningful images unlabeled | `Image(decorative:)` / `accessibilityHidden(true)`; labels for meaningful ones | HIG:accessibility | M |
| 29 | Rows read as fragments (each Text separately) | `accessibilityElement(children: .combine)` | `accessibilityelement(children:)` | M |
| 30 | Custom search bar (TextField + magnifier) | `searchable`; `Tab(role: .search)`; `ContentUnavailableView.search` | HIG:search-fields | M |
| 31 | Hand-built empty state / spinner / share sheet / photo picker | `ContentUnavailableView`, `ProgressView`, `ShareLink`, `PhotosPicker` | section 7 | L |
| 32 | Generic keyboard for email/number/OTP fields; passwords in `TextField` | `keyboardType`, `textContentType`, `SecureField`, `submitLabel` | HIG:text-fields | M |
| 33 | Placeholder as the only label | Visible label (`LabeledContent`, Form row title) | HIG:text-fields | M |
| 34 | Deprecated API in new code (`NavigationView`, `foregroundColor`, `tabItem`, …) | Section 8.2 table | JSON metadata | M |
| 35 | New API without availability guard or fallback | `#available` + real fallback | section 8.1 | H |
| 36 | macOS app without menu commands, shortcuts or Settings scene; iOS-style settings screen on Mac | `commands`, `keyboardShortcut`, `Settings` | HIG:the-menu-bar, HIG:keyboards, HIG:settings | M |
| 37 | Hover/focus ignored on iPadOS, tvOS, visionOS (custom tappable shapes) | `Button` + styles; `hoverEffect`, `focusable`, `contentShape` | HIG:pointing-devices, HIG:focus-and-selection | M |
| 38 | Custom haptics for everything / wrong meaning | `sensoryFeedback` with semantic values | HIG:playing-haptics | L |
| 39 | Assuming an SF Symbol name exists on all OS versions | Verify in SF Symbols app; provide fallback | HIG:sf-symbols | M |
| 40 | Shipping `UIDesignRequiresCompatibility` as a long-term fix | Adopt the current design | bundleresources key doc | M |

---

## 11. Example snippets (conservative; NOT compiled)

Every modifier and initializer label below was checked against the docs JSON. Model/child views (`HomeView`, `ContentView`, …) are placeholders.

### 11.1 Adaptive navigation — iOS 16 / macOS 13
`NavigationSplitView` collapses to a stack at compact width (documented), so no size-class branch is needed.
```swift
struct Folder: Identifiable, Hashable { let id: UUID; var name: String }

struct LibraryView: View {
    let folders: [Folder]
    @State private var selectedID: Folder.ID?
    var body: some View {
        NavigationSplitView {
            List(folders, selection: $selectedID) { folder in
                Label(folder.name, systemImage: "folder")
            }
            .navigationTitle("Library")
        } detail: {
            if let folder = folders.first(where: { $0.id == selectedID }) {
                Text(folder.name).navigationTitle(folder.name)
            } else {
                Text("Select a folder").foregroundStyle(.secondary)
            }
        }
    }
}
```

### 11.2 TabView with `Tab` and fallback — `Tab` needs iOS 18 / macOS 15; fallback iOS 14
```swift
struct RootView: View {
    var body: some View {
        if #available(iOS 18, macOS 15, tvOS 18, watchOS 11, visionOS 2, *) {
            TabView {
                Tab("Home", systemImage: "house") { HomeView() }
                Tab("Library", systemImage: "books.vertical") { LibraryRootView() }
                Tab("Search", systemImage: "magnifyingglass", role: .search) { SearchView() }
            }
        } else {
            // tabItem(_:) is marked deprecated from 27.3; it is correct for older targets.
            TabView {
                HomeView().tabItem { Label("Home", systemImage: "house") }
                LibraryRootView().tabItem { Label("Library", systemImage: "books.vertical") }
                SearchView().tabItem { Label("Search", systemImage: "magnifyingglass") }
            }
        }
    }
}
```
Optional: `.tabViewStyle(.sidebarAdaptable)` on the first branch (iOS 18; not watchOS); `.tabBarMinimizeBehavior(.onScrollDown)` behind `#available(iOS 26, *)`.

### 11.3 Dynamic-Type-resilient row — iOS 16 / macOS 13
```swift
struct SettingRow: View {
    let title: String
    let value: String
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize
    @ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 28
    var body: some View {
        let layout = dynamicTypeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading))
            : AnyLayout(HStackLayout())
        layout {
            Image(systemName: "bell")
                .frame(width: iconSize, height: iconSize)
                .accessibilityHidden(true)
            Text(title)
            if !dynamicTypeSize.isAccessibilitySize { Spacer() }
            Text(value).foregroundStyle(.secondary)
        }
        .font(.body)
        .accessibilityElement(children: .combine)
    }
}
```
No `lineLimit`, no fixed height: text wraps and the row grows; the icon scales with `@ScaledMetric`.

### 11.4 Accessible custom control (rating) — iOS 15 / macOS 12
```swift
struct RatingControl: View {
    @Binding var rating: Int
    let maximum = 5
    var body: some View {
        HStack {
            ForEach(1...maximum, id: \.self) { index in
                Button { rating = index } label: {
                    Image(systemName: index <= rating ? "star.fill" : "star")
                }
                .buttonStyle(.plain)
            }
        }
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("Rating")
        .accessibilityValue("\(rating) of \(maximum)")
        .accessibilityAdjustableAction { direction in
            switch direction {
            case .increment: rating = min(rating + 1, maximum)
            case .decrement: rating = max(rating - 1, 1)
            @unknown default: break
            }
        }
    }
}
```
Alternative when a standard control maps well: `.accessibilityRepresentation { Slider(value:in:step:) }` (iOS 15). Give each star a 44x44 pt hit area on iOS.

### 11.5 Icon-only toolbar button done right — iOS 14 / macOS 11
```swift
struct InboxView: View {
    @State private var isComposing = false
    var body: some View {
        List { Text("Message") }
            .navigationTitle("Inbox")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button { isComposing = true } label: {
                        Label("Compose", systemImage: "square.and.pencil")
                    }
                }
            }
            .sheet(isPresented: $isComposing) { Text("New Message") }
    }
}
```
`Label` gives VoiceOver, Voice Control and tooltips a name; the toolbar decides whether to show the title. Outside a toolbar use `.labelStyle(.iconOnly)`, not a bare `Image`.

### 11.6 Semantic colors and Dark Mode — iOS 15 / macOS 12
```swift
struct SummaryCard: View {
    let title: String
    let detail: String
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).font(.headline).foregroundStyle(.primary)
            Text(detail).font(.subheadline).foregroundStyle(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
    }
}
```
No color literals. Brand colors: asset-catalog Color Set with light/dark/high-contrast variants (`Color("BrandPrimary")`). UIKit semantic colors: `Color(uiColor: .secondarySystemBackground)` inside `#if canImport(UIKit)`.

### 11.7 Form / settings screen — iOS 16 / macOS 13
```swift
struct PreferencesView: View {
    @State private var notificationsEnabled = true
    @State private var sortOrder = 0
    @State private var itemsPerPage = 20
    var body: some View {
        Form {
            Section("General") {
                Toggle("Notifications", isOn: $notificationsEnabled)
                Picker("Sort By", selection: $sortOrder) {
                    Text("Name").tag(0)
                    Text("Date").tag(1)
                }
                Stepper("Items per page: \(itemsPerPage)", value: $itemsPerPage, in: 10...100, step: 10)
            }
            Section("About") {
                LabeledContent("Version", value: "1.0")
            }
        }
        .navigationTitle("Settings")
    }
}
```
`Stepper` is unavailable on tvOS. On macOS consider `.formStyle(.grouped)` (macOS 13).

### 11.8 Sheet with detents — iOS 16
```swift
struct FilterHost: View {
    @State private var showsFilters = false
    var body: some View {
        Button("Filters") { showsFilters = true }
            .sheet(isPresented: $showsFilters) {
                FilterSheet()
                    .presentationDetents([.medium, .large])
                    .presentationDragIndicator(.visible)
            }
    }
}

struct FilterSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var onlyUnread = false
    var body: some View {
        NavigationStack {
            Form { Toggle("Unread Only", isOn: $onlyUnread) }
                .navigationTitle("Filters")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) { Button("Cancel") { dismiss() } }
                    ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } }
                }
        }
    }
}
```

### 11.9 Confirmation dialog for a destructive action — iOS 15 / macOS 12
```swift
struct DraftActions: View {
    @State private var isConfirmingDelete = false
    let deleteDraft: () -> Void
    var body: some View {
        Button("Delete Draft", role: .destructive) { isConfirmingDelete = true }
            .confirmationDialog("Delete this draft?", isPresented: $isConfirmingDelete, titleVisibility: .visible) {
                Button("Delete Draft", role: .destructive) { deleteDraft() }
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("This action can't be undone.")
            }
    }
}
```
Use only for uncommon, non-undoable actions (HIG:alerts); prefer undo for routine deletes.

### 11.10 Reduce-Motion-aware animation — iOS 15 / macOS 12
```swift
struct ExpandableNote: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var isExpanded = false
    var body: some View {
        VStack(alignment: .leading) {
            Button(isExpanded ? "Show Less" : "Show More") {
                if reduceMotion {
                    isExpanded.toggle()
                } else {
                    withAnimation { isExpanded.toggle() }
                }
            }
            if isExpanded {
                Text("Additional details").transition(.opacity)
            }
        }
    }
}
```

### 11.11 macOS commands and Settings scene — macOS 13 (multiplatform-safe)
```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .commands {
                SidebarCommands()
                CommandMenu("Note") {
                    Button("Pin Note") { /* perform action */ }
                        .keyboardShortcut("p", modifiers: [.command, .shift])
                }
            }
        #if os(macOS)
        Settings {
            PreferencesView().scenePadding().frame(minWidth: 360)
        }
        #endif
    }
}
```
`Settings` exists only on macOS and supplies the app-menu Settings item with its standard shortcut; do not add your own. `commands` also works on iPadOS (hardware keyboard).

### 11.12 Searchable list with empty state — iOS 17 / macOS 14
```swift
struct ContactList: View {
    let names: [String]
    @State private var query = ""
    private var results: [String] {
        query.isEmpty ? names : names.filter { $0.localizedCaseInsensitiveContains(query) }
    }
    var body: some View {
        NavigationStack {
            List(results, id: \.self) { name in Text(name) }
                .navigationTitle("Contacts")
                .searchable(text: $query, prompt: "Search contacts")
                .overlay {
                    if results.isEmpty && !query.isEmpty {
                        ContentUnavailableView.search(text: query)
                    }
                }
        }
    }
}
```
`searchable` alone works from iOS 15; `ContentUnavailableView` needs iOS 17 (gate it or show a plain `Text` below 17).

---

## 12. Could not verify / open items

- Nothing compiled. Everyday call shapes (`List(_:id:rowContent:)`, `.tag`, string-literal `prompt:`) rely on overload
  families whose pages were sampled, not exhaustively fetched.
- Compiler behaviour of `deprecatedAt: 27.3` at lower deployment targets (warning or not) — unverified.
- Swift `#available` / `@available` grammar — from memory (docs.swift.org unreachable via curl).
- 27-only layout additions (`ArrangementView`, reserved regions, hinge, vertical toolbars, `reorderable()`) — seen in release
  notes only; no signatures recorded. Keep out of shipped examples until checked.
- Behavioural claims tagged [M] (popover adaptation, inspector on compact, symbol fallback rendering, `Font.custom(_:size:)` scaling).
- SF Symbol names used in examples (`house`, `books.vertical`, `magnifyingglass`, `folder`, `bell`, `star`, `star.fill`,
  `square.and.pencil`) are long-standing names from memory **[M]**; the docs JSON does not list symbol catalogs.
