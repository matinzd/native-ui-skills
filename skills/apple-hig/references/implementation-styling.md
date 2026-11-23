# Styling in code: fonts, Dynamic Type, color, materials, Liquid Glass, SF Symbols

Scope: SwiftUI APIs (with a short UIKit and AppKit table) for text styles and Dynamic Type, semantic color and Dark Mode, materials, Liquid Glass and SF Symbols, with verified minimum OS versions. Design guidance is in `references/foundations-typography.md`, `references/foundations-color-materials.md` and `references/foundations-icons-images.md`.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Reading availability
- Text styles and fonts
- Dynamic Type in layouts
- UIKit and AppKit text equivalents
- Semantic color
- Color scheme and contrast
- Materials
- Liquid Glass (OS 26+)
- SF Symbols
- Common mistakes

## Reading availability

- [API] Versions are `introducedAt` values from the documentation JSON; a platform that is not named has no availability entry.
- [API] Documentation landing pages merge overloads and can show a newer minimum than the oldest overload. Example: `Font.system(size:weight:design:)` shows iOS 16 (optional parameters); the older non-optional overload is iOS 13 and now marked deprecated. `tint(_:)` shows iOS 15 for `Color?`; the `ShapeStyle` overload is iOS 16.
- [API] Deprecated spellings to keep out of new code: `foregroundColor(_:)`, `accentColor(_:)`, `colorScheme(_:)`, `cornerRadius(_:)`, unlabelled `Color(_: UIColor)`, `\.sizeCategory`. Replacements are in the sections below and in `references/implementation-availability.md`.
- [Conv] Nothing here was compiled; build before claiming it works.

Source: https://developer.apple.com/documentation/swiftui/font, https://developer.apple.com/documentation/swiftui/color

## Text styles and fonts

| API | Availability | Notes |
|---|---|---|
| `.font(.largeTitle)`, `.title`, `.headline`, `.subheadline`, `.body`, `.callout`, `.footnote`, `.caption` | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | Text styles; scale with Dynamic Type where the platform has it. |
| `.title2`, `.title3`, `.caption2` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | |
| `Font.TextStyle.extraLargeTitle`, `.extraLargeTitle2` | visionOS 1+ only | Guard with `#if os(visionOS)`. |
| `Font.system(_:design:weight:)` (text style) | iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+ | Text style with a design (`.rounded`, `.serif`, `.monospaced`) or weight. |
| `Font.custom(_:size:relativeTo:)` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Custom font that scales relative to the text style you name. |
| `Font.custom(_:size:)` | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | Scales with the body text style. |
| `Font.custom(_:fixedSize:)` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Never scales with Dynamic Type. |
| `fontWeight(_:)`, `bold(_:)` on a view | iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+ | `Font.weight(_:)` is iOS 13+. `fontDesign(_:)` is iOS 16.1+. |
| `monospacedDigit()` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Stable-width digits for timers and columns. |

```swift
// iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+
VStack(alignment: .leading, spacing: 4) {
    Text(article.title).font(.headline)
    Text(article.summary).font(.subheadline)
    Text(article.byline).font(.custom("Avenir Next", size: 13, relativeTo: .footnote))
}
```

- [HIG] Prefer the built-in text styles; they carry the hierarchy and support Dynamic Type and the larger accessibility sizes where available.
- [HIG] Avoid Ultralight, Thin and Light weights; prefer Regular, Medium, Semibold or Bold. Follow the per-platform default and minimum sizes (iOS minimum 11 pt).
- [HIG] A custom font must still respond to Dynamic Type and Bold Text. Use `relativeTo:`; read `\.legibilityWeight` (iOS 13+) if you choose weights by hand.
- [Conv] `Font.system(size:)` with a literal does not follow the text styles; keep it for symbols and decorative numerals, not body content. [Unverified] The documentation checked does not state whether it scales with Dynamic Type; treat it as fixed.

Source: https://developer.apple.com/documentation/swiftui/font, https://developer.apple.com/design/human-interface-guidelines/typography

## Dynamic Type in layouts

```swift
// iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ (@ScaledMetric alone: iOS 14+)
struct SettingRow: View {
    let title: String
    let value: String
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize
    @ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 28
    var body: some View {
        HStack(alignment: .firstTextBaseline) {
            Image(systemName: "bell")
                .frame(width: iconSize, height: iconSize)
                .accessibilityHidden(true)
            if dynamicTypeSize.isAccessibilitySize {
                VStack(alignment: .leading) { Text(title); Text(value).foregroundStyle(.secondary) }
            } else {
                Text(title); Spacer(); Text(value).foregroundStyle(.secondary)
            }
        }
    }
}
```

- [API] `@ScaledMetric` (`init(wrappedValue:)`, `init(wrappedValue:relativeTo:)`; iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+) scales a number with the text size. Use it for icon frames, spacing and custom control dimensions.
- [API] `\.dynamicTypeSize`, `DynamicTypeSize` and `isAccessibilitySize` are iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+. They replace the deprecated `\.sizeCategory`.
- [API] `dynamicTypeSize(_:)` takes one size (useful in previews) or a range that limits a subtree, for example `.dynamicTypeSize(...DynamicTypeSize.accessibility1)`.
- [HIG] Ideally text can be enlarged by at least 200 percent (140 percent in watchOS). Limit a range only for chrome that truly cannot grow, never for a whole screen.
- [API] Large Content Viewer: `accessibilityShowsLargeContentViewer()` and the `(_:)` form with a custom view are iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+. The documentation says to rely on it only where items must stay small, such as tab-bar-like buttons.
- [Conv] Do not pair `lineLimit(1)` with `minimumScaleFactor` to make text "fit"; let it wrap and let the container grow. `lineLimit(_:reservesSpace:)` is iOS 16+.
- [HIG] Dynamic Type is listed for iOS, iPadOS, tvOS, visionOS and watchOS, not macOS. [API] macOS still has text styles (`NSFont.preferredFont(forTextStyle:options:)`, macOS 11+).

Source: https://developer.apple.com/documentation/swiftui/dynamictypesize, https://developer.apple.com/documentation/swiftui/scaledmetric, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/accessibility

## UIKit and AppKit text equivalents

| Need | UIKit / AppKit | Availability |
|---|---|---|
| Text-style font | `UIFont.preferredFont(forTextStyle:)` | iOS 7+, visionOS 1+, watchOS 2+ |
| Live updates when the size changes | `adjustsFontForContentSizeCategory = true` (`UIContentSizeCategoryAdjusting`) | iOS 10+, tvOS 10+, visionOS 1+ |
| Scale a custom font or a metric | `UIFontMetrics` (`scaledFont(for:)`, `scaledValue(for:)`) | iOS 11+, tvOS 11+, watchOS 4+, visionOS 1+ |
| Detect accessibility sizes | `UIContentSizeCategory.isAccessibilityCategory` | iOS 11+, tvOS 11+ |
| Limit the range for a view | `UIView.minimumContentSizeCategory` / `maximumContentSizeCategory` | iOS 15+, tvOS 15+, visionOS 1+ |
| Large Content Viewer | `UILargeContentViewerInteraction`, `showsLargeContentViewer`, `largeContentTitle` | iOS 13+, visionOS 1+ |
| Text-style font on Mac | `NSFont.preferredFont(forTextStyle:options:)` | macOS 11+ |

More UIKit and AppKit mappings: `references/implementation-uikit-appkit.md`.

Source: https://developer.apple.com/documentation/uikit/uifontmetrics, https://developer.apple.com/documentation/uikit/uifont, https://developer.apple.com/documentation/appkit/nsfont

## Semantic color

| API | Availability | Notes |
|---|---|---|
| `foregroundStyle(_:)`, `foregroundStyle(_:_:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Replaces the deprecated `foregroundColor(_:)`. |
| `.primary`, `.secondary`, `.tertiary`, `.quaternary` as `ShapeStyle` | same | Hierarchical levels of the current foreground style. `Color.primary` / `Color.secondary` are iOS 13+. |
| `.tint` (`ShapeStyle`), `tint(_:)` modifier | same | Current tint. Replaces `accentColor(_:)`; set the app-wide accent in the asset catalog's AccentColor. |
| `.background` (`ShapeStyle`) | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | `backgroundStyle(_:)` is iOS 16+. |
| `.separator`, `.link`, `.placeholder`, `.fill` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ (`separator`: macOS 10.15+) | `.windowBackground` has the same versions but no visionOS entry. |
| `.selection` | iOS 15+, macOS 12+, visionOS 1+ | |
| `Color("Name")` (`Color(_:bundle:)`) | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | Asset-catalog Color Set by name. |
| `Color(_ resource: ColorResource)` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ | Typed asset reference. [Unverified] The exact generated symbol names depend on Xcode; check the generated code. |
| `Color(uiColor:)` | iOS 15+, tvOS 15+, watchOS 8+, visionOS 1+ | For example `Color(uiColor: .secondarySystemBackground)`. |
| `Color(nsColor:)` | macOS 12+ | For example `Color(nsColor: .windowBackgroundColor)`. |
| `background(_:in:fillStyle:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Style clipped to a shape; no separate `clipShape` needed. |

```swift
// iOS 15+, macOS 12+, tvOS 15+, watchOS 10+ (materials), visionOS 1+
VStack(alignment: .leading, spacing: 4) {
    Text(title).font(.headline)
    Text(detail).font(.subheadline).foregroundStyle(.secondary)
    Label("Overdue", systemImage: "exclamationmark.triangle").foregroundStyle(.red)
}
.padding()
.frame(maxWidth: .infinity, alignment: .leading)
.background(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
```

- [API] The unlabelled `Color(_: UIColor)`, `Color(_: NSColor)` and `Color(_: CGColor)` initializers are marked deprecated; `Color(.systemBackground)` is that form. Write `Color(uiColor: .systemBackground)` inside `#if canImport(UIKit)`.
- [API] `UIColor.systemBackground` and `.secondarySystemBackground` list iOS 13+ and visionOS 1+ only (no tvOS or watchOS entry); `UIColor.label` lists iOS 13+, tvOS 13+, visionOS 1+.
- [HIG] Put custom colors in an asset-catalog Color Set with light and dark variants; avoid hard-coded values that do not adapt.
- [HIG] Use dynamic system colors for their intended purpose (do not use a separator color for text), and never rely on color alone to convey information: pair it with a symbol, shape or text, as the label above does.
- [Conv] Round corners with `clipShape(.rect(cornerRadius:))` or a shape-clipped background; `cornerRadius(_:)` is deprecated.

Source: https://developer.apple.com/documentation/swiftui/shapestyle, https://developer.apple.com/documentation/swiftui/color, https://developer.apple.com/documentation/uikit/uicolor, https://developer.apple.com/design/human-interface-guidelines/color, https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Color scheme and contrast

- [API] `@Environment(\.colorScheme)` (iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+) reads `.light` or `.dark`. Read it only when an asset cannot express the difference; semantic styles and Color Sets adapt without code.
- [API] `preferredColorScheme(_:)` (iOS 13+, macOS 11+, tvOS 13+, watchOS 6+, visionOS 1+) sets the scheme for the nearest enclosing presentation (window, sheet, popover) and overrides the person's Dark Mode choice there; pass `nil` for no preference. The `colorScheme(_:)` modifier is deprecated.
- [HIG] Avoid an app-specific appearance setting; follow the system appearance. [Conv] Force a scheme only for a presentation whose content is inherently dark or light, such as a media player.
- [API] `@Environment(\.colorSchemeContrast)` (iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+) is `.standard` or `.increased` (Increase Contrast). [Conv] Give Color Sets high-contrast variants in the asset catalog so most code never reads it.
- [HIG] Text contrast: at least 4.5:1 for text up to 17 pt; 3:1 is acceptable for 18 pt or bold text (Accessibility page table). The Dark Mode page separately asks for no lower than 4.5:1 in every appearance and 7:1 for custom foreground and background colors, especially small text. Test Dark Mode together with Increase Contrast and Reduce Transparency.
- [Conv] Preview both schemes with `.environment(\.colorScheme, .dark)` or `.preferredColorScheme(.dark)` in a preview only.

Source: https://developer.apple.com/documentation/swiftui/colorscheme, https://developer.apple.com/documentation/swiftui/colorschemecontrast, https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Materials

- [API] `Material`: `.ultraThin`, `.thin`, `.regular`, `.thick`, `.ultraThick` (iOS 15+, macOS 12+, tvOS 15+, watchOS 10+, visionOS 1+) and `.bar` (iOS 15+, macOS 12+, visionOS 1+). As a style: `.background(.regularMaterial)`, `.thinMaterial`, `.ultraThinMaterial`.
- [API] Foreground elements over a material exhibit vibrancy. Setting a custom `foregroundStyle` disables it, except for the hierarchical styles such as `.secondary`; prefer those on materials.
- [HIG] Standard materials belong to the content layer and provide structure beneath Liquid Glass. Choose a material for its semantic purpose, not for the color it seems to add; system settings can change how it looks.
- [API] `@Environment(\.accessibilityReduceTransparency)` (iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+) tells you when to swap a custom translucent effect for an opaque style. System materials adapt by themselves.
- [API] visionOS has its own glass: `glassBackgroundEffect(displayMode:)` (visionOS 1+ only). UIKit: `UIVisualEffectView` with `UIBlurEffect`; AppKit: `NSVisualEffectView`.

Source: https://developer.apple.com/documentation/swiftui/material, https://developer.apple.com/design/human-interface-guidelines/materials

## Liquid Glass (OS 26+)

| API | Availability | Notes |
|---|---|---|
| `glassEffect(_:in:)` | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+; not on visionOS | Defaults: `.regular` glass in a capsule. Apply after other appearance modifiers. |
| `Glass`: `.regular`, `.clear`, `.identity`, `.tint(_:)`, `.interactive(_:)` | same | `.interactive()` makes a custom component react to touch and pointer like a glass button. |
| `GlassEffectContainer(spacing:content:)` | same | Renders several glass shapes together so they blend and morph; better performance than separate effects. |
| `glassEffectID(_:in:)`, `glassEffectUnion(id:namespace:)`, `glassEffectTransition(_:)` | same | Morphing between glass shapes. |
| `buttonStyle(.glass)`, `buttonStyle(.glassProminent)` | same | See `references/implementation-controls.md`. |
| `ButtonRole.close`, `ButtonRole.confirm`, `Button(role:action:)` | OS 26+ on all platforms including visionOS | System-labelled Close and Confirm buttons. |
| `ConcentricRectangle`, `containerShape(_:)` (rounded-rectangle overload) | OS 26+ on all platforms | Corners concentric with the container. The generic `containerShape(_:)` overload is iOS 15+. |
| UIKit `UIGlassEffect`; AppKit `NSGlassEffectView` | iOS 26+, tvOS 26+; macOS 26+ | |

```swift
// Glass: iOS 26+, macOS 26+, tvOS 26+, watchOS 26+. Elsewhere a standard material
// (iOS 15+, macOS 12+, tvOS 15+, watchOS 10+, visionOS 1+).
struct FloatingBadge: View {
    let text: String
    var body: some View {
        let label = Text(text).padding(.horizontal).padding(.vertical, 8)
        #if os(visionOS)
        // glassEffect has no visionOS availability, and `*` in #available would match visionOS.
        label.background(.regularMaterial, in: Capsule())
        #else
        if #available(iOS 26, macOS 26, tvOS 26, watchOS 26, *) {
            label.glassEffect(.regular.interactive())
        } else {
            // Fallback for OS 18 and earlier: same shape, standard material.
            label.background(.regularMaterial, in: Capsule())
        }
        #endif
    }
}
```

- [API] Standard components (bars, sheets, popovers, controls) from SwiftUI, UIKit and AppKit adopt Liquid Glass automatically when built with the current SDK. Apple's adoption guide says to reduce custom backgrounds in tab bars, toolbars and split views; do that before adding any glass of your own.
- [HIG] Liquid Glass is the layer for controls and navigation. Do not use it in the content layer (cards, list rows, backgrounds); use standard materials there.
- [HIG] Apply glass to custom controls sparingly. Use the clear variant only over visually rich backgrounds such as photos or video, adding a dimming layer if legibility needs it.
- [API] The glass effect and glass button style rows above (`glassEffect` through `buttonStyle(.glass)`) have no visionOS availability; compile them out with `#if !os(visionOS)` and use `glassBackgroundEffect` there.
- [API] Info.plist key `UIDesignRequiresCompatibility` (iOS 26+, macOS 26+, tvOS 26+) temporarily runs an app with the previous design. The documentation states the system ignores the key when you build for OS 27 or later, so it is not an option for current SDK work.
- [Conv] Test glass with Reduce Transparency, Increase Contrast and Reduce Motion turned on.

Source: https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views, https://developer.apple.com/documentation/swiftui/glass, https://developer.apple.com/documentation/swiftui/glasseffectcontainer, https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/design/human-interface-guidelines/materials

## SF Symbols

| API | Availability | Notes |
|---|---|---|
| `Image(systemName:)` | iOS 13+, macOS 11+, tvOS 13+, watchOS 6+, visionOS 1+ | `Image(systemName:variableValue:)` is iOS 16+, macOS 13+, tvOS 16+, watchOS 9+. |
| `Label(_:systemImage:)` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Title plus icon. Containers may pick a default style, for example icon-only in toolbars on iOS and macOS. [Conv] The title still names the control for VoiceOver. |
| `labelStyle(.iconOnly)`, `.titleOnly` | same | `.titleAndIcon` is iOS 14.5+, macOS 11.3+, tvOS 14.5+, watchOS 7.4+. |
| `symbolRenderingMode(_:)`: `.monochrome`, `.hierarchical`, `.palette`, `.multicolor` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Palette layers take the primary, secondary and tertiary styles from `foregroundStyle(_:_:)`. |
| `symbolVariant(_:)`: `.fill`, `.circle`, `.slash` | same | Applies to all symbols in the subtree; avoids hard-coding `.fill` names. |
| `imageScale(_:)`: `.small`, `.medium`, `.large` | iOS 13+, macOS 11+, tvOS 13+, watchOS 6+, visionOS 1+ | Size relative to the surrounding font. |
| `symbolEffect(_:options:value:)`, `symbolEffect(_:options:isActive:)`, `symbolEffectsRemoved(_:)` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ | `.bounce`, `.pulse`, variable color: 17. Wiggle: iOS 18+. Draw On: OS 26+. |
| `contentTransition(.symbolEffect(_:options:))` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ | Animated replacement of one symbol by another. |
| UIKit `UIImage(systemName:)`; AppKit `NSImage(systemSymbolName:accessibilityDescription:)` | iOS 13+, tvOS 13+, watchOS 6+, visionOS 1+; macOS 11+ | Both are failable initializers. |

```swift
// iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ (drop symbolEffect for iOS 15-16)
Button { isFavorite.toggle() } label: {
    Label("Favorite", systemImage: "heart")
        .symbolVariant(isFavorite ? .fill : .none)
        .symbolRenderingMode(.hierarchical)
        .symbolEffect(.bounce, value: isFavorite)
}
.font(.title3)          // the symbol takes its size and weight from the font
```

- [API] Size a symbol with `font(_:)` (Apple's own samples do) or `imageScale(_:)`, not with `resizable()` and a fixed frame, so it tracks Dynamic Type and text weight. [HIG] Symbols use weights equivalent to the system font and align with adjacent text.
- [HIG] Symbol and feature availability depends on the system version: a symbol introduced in a given year does not exist on earlier systems. Check each name and its minimum OS in the SF Symbols app; this skill does not list symbol names.
- [Unverified] What SwiftUI draws for an unknown symbol name (commonly reported as nothing, with no build error). Do not rely on it; verify the name.
- [API] `Image(decorative:bundle:)` hides an asset image from accessibility. For a decorative symbol use `.accessibilityHidden(true)`; give a meaningful icon-only control a `Label` or `accessibilityLabel(_:)`.
- [HIG] Using system-provided colors with any rendering mode lets symbols adapt to Dark Mode, vibrancy and accessibility settings.

Source: https://developer.apple.com/documentation/swiftui/image, https://developer.apple.com/documentation/swiftui/label, https://developer.apple.com/documentation/swiftui/symbolrenderingmode, https://developer.apple.com/documentation/swiftui/symbolvariants, https://developer.apple.com/documentation/symbols, https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## Common mistakes

| Mistake | Fix |
|---|---|
| `.font(.system(size: 14))` for content | A text style, or `Font.custom(_:size:relativeTo:)` for a brand font. |
| `Font.custom(_:fixedSize:)` or UIKit fonts without `UIFontMetrics` | `relativeTo:`; `UIFontMetrics.scaledFont(for:)` plus `adjustsFontForContentSizeCategory`. |
| Fixed icon and row dimensions next to scalable text | `@ScaledMetric`, `frame(minHeight:)`. |
| A `dynamicTypeSize` range on the root view to "protect" the layout | Fix the layout; switch arrangement at `isAccessibilitySize`. |
| `foregroundColor`, `accentColor`, `Color(.systemBackground)` | `foregroundStyle`, `tint` or the asset AccentColor, `Color(uiColor:)`. |
| `Color.black` / `.white` / hex literals for text and surfaces | Semantic styles; Color Sets with dark and high-contrast variants. |
| In-app light/dark switch through `preferredColorScheme` | Follow the system; the HIG advises against an app-specific appearance setting. |
| Status shown by color only | Add a symbol or text; check `\.accessibilityDifferentiateWithoutColor` for custom drawings. |
| `glassEffect` on cards, rows or whole screens | Standard materials in content; glass only on a few custom controls. |
| Glass APIs with no availability check, or compiled for visionOS | `#available(iOS 26, macOS 26, *)` with a material fallback; `#if !os(visionOS)`. |
| Shipping `UIDesignRequiresCompatibility` as a fix | It is ignored when building for OS 27 or later; adopt the current design. |
| `Image(systemName:)` with `resizable().frame(...)` and an unverified name | `font` or `imageScale`; confirm the name and minimum OS in the SF Symbols app. |
