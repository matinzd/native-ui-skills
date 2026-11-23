# Accessibility implementation and testing

Scope: the SwiftUI, UIKit and AppKit APIs that implement the guidance in `references/accessibility-guidelines.md` (labels, values, traits, grouping, actions, focus, text size, motion and contrast settings), short correct snippets, and how to test.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Start from system components
- Describing elements: label, value, hint, traits
- Structure: grouping, hiding, order, headings, rotors
- Actions and custom controls
- Focus and announcements
- Text size in code
- Environment values for accessibility settings
- Snippets
- UIKit and AppKit equivalents
- Testing
- Common mistakes

Availability is `introducedAt` for the oldest overload, written as iOS / macOS; tvOS, watchOS and visionOS have matching entries unless noted. The design rules and numbers (sizes, contrast) are in `references/accessibility-guidelines.md` and are not repeated here.

## Start from system components

- [HIG] Standard controls (`Button`, `Toggle`, `Picker`, `Slider`, `Stepper`, `List`, `TabView`, system bars and sheets) already expose a role, state, actions, focus behavior and Dynamic Type. Use them before writing any accessibility modifier.
- [API] A custom style keeps that support: Apple's example is a custom `ToggleStyle`, which inherits the accessibility of `Toggle`. Prefer a custom style to a shape with a tap gesture.
- [Conv] `onTapGesture` on a `Text`, `Image` or stack creates something that looks like a button but has no button trait, no keyboard or pointer behavior and no pressed state. Use `Button` with a custom label instead.
- [Conv] Add modifiers only where the default is wrong or missing: icon-only controls, images, custom-drawn controls, rows read in fragments.

Source: https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:) , https://developer.apple.com/documentation/swiftui/accessibility-fundamentals , https://developer.apple.com/design/human-interface-guidelines/accessibility

## Describing elements: label, value, hint, traits

| Modifier | Minimum OS | Use |
|---|---|---|
| `accessibilityLabel(_:)` | iOS 14 / macOS 11 | The element's name. Required for icon-only controls and meaningful images. |
| `accessibilityValue(_:)` | iOS 14 / macOS 11 | Current state or amount ("3 of 5", "On", "40 percent"). Update it when state changes. |
| `accessibilityHint(_:)` | iOS 14 / macOS 11 | Optional short phrase for what happens after the action. Not a substitute for a label. |
| `accessibilityAddTraits(_:)`, `accessibilityRemoveTraits(_:)` | iOS 14 / macOS 11 | `.isButton`, `.isHeader`, `.isSelected`, `.isLink`, `.isImage`, `.isModal`, `.updatesFrequently` (iOS 13); `.isToggle` (iOS 17). |
| `accessibilityInputLabels(_:)` | iOS 14 / macOS 11 | Alternative names for Voice Control and Full Keyboard Access, most important first. |
| `accessibilityIdentifier(_:)` | iOS 14 / macOS 11 | UI-test hook only. It is not spoken and does not label anything. |
| `accessibilityCustomContent(_:_:importance:)` | iOS 15 / macOS 12 | Extra detail VoiceOver offers on request, so the label stays short. |

- [HIG] Write labels that describe the function ("Add to Favorites"), keep them current as state changes, and replace generic default labels.
- [Conv] Do not put the control type in the label ("Add button"); the trait supplies it. Do not put state in the label when a value or a selected trait carries it.
- [API] `Label("Add", systemImage: "plus")` keeps its title for assistive technologies even when a toolbar or `labelStyle(.iconOnly)` shows only the icon. `Image(systemName:)` alone has no meaningful name.
- [API] The `accessibility(label:)`, `accessibility(hidden:)` and `accessibility(addTraits:)` family is deprecated; use the `accessibilityLabel(_:)` family.

Source: https://developer.apple.com/documentation/swiftui/view/accessibilitylabel(_:) , https://developer.apple.com/documentation/swiftui/view/accessibilityhint(_:) , https://developer.apple.com/documentation/swiftui/accessibilitytraits , https://developer.apple.com/documentation/swiftui/view/accessibilityinputlabels(_:) , https://developer.apple.com/design/human-interface-guidelines/voiceover

## Structure: grouping, hiding, order, headings, rotors

- [API] `accessibilityElement(children:)` (iOS 13 / macOS 10.15): `.combine` merges the children's properties into one element (one stop per row); `.ignore` (the default argument) replaces them with a blank element you must label yourself; `.contain` keeps the children and makes the view a container.
- [API] With `.combine`, not every trait is merged and a child's default action can become a named action. Check the result with VoiceOver when a row contains its own buttons.
- [API] `accessibilityHidden(_:)` (iOS 14 / macOS 11) removes decoration. `Image(decorative:bundle:)` (iOS 13) creates an image that is never exposed.
- [API] `accessibilitySortPriority(_:)` (iOS 14 / macOS 11): higher numbers are read first among elements at the same level; the default is 0. Use it only when the visual order and the logical order differ.
- [API] Headings: `accessibilityAddTraits(.isHeader)`; `accessibilityHeading(_:)` (iOS 15 / macOS 12) sets a level.
- [Conv] `navigationTitle` and `Section` headers come from system components, so they need no heading trait; add the trait to custom section titles.
- [API] `accessibilityRotor(_:entries:)` with `AccessibilityRotorEntry` (iOS 15 / macOS 12) adds a custom rotor, for example to jump between unread items.
- [API] `accessibilityLabeledPair(role:id:in:)` (iOS 14 / macOS 11) links a visible label to its control when they are separate views.

Source: https://developer.apple.com/documentation/swiftui/view/accessibilityelement(children:) , https://developer.apple.com/documentation/swiftui/accessibilitychildbehavior/combine , https://developer.apple.com/documentation/swiftui/view/accessibilitysortpriority(_:) , https://developer.apple.com/documentation/swiftui/view/accessibilityrotor(_:entries:)

## Actions and custom controls

- [API] `accessibilityAction(_:_:)` (iOS 13 / macOS 10.15) supplies the default activation for a custom element; `accessibilityAction(named:_:)` (iOS 14 / macOS 11) adds a named custom action; `accessibilityActions(_:)` (iOS 16 / macOS 13) adds several from a view builder.
- [HIG] Anything reachable only by swipe, long press, drag or hover needs another route. Add a visible control or menu item, and a named accessibility action for custom gestures.
- [API] `accessibilityAdjustableAction(_:)` (iOS 13 / macOS 10.15) makes an element adjustable; the handler receives `.increment` or `.decrement`. Pair it with a label and a value.
- [API] `accessibilityRepresentation(representation:)` (iOS 15 / macOS 12) replaces a custom view's accessibility elements with those of a standard control you supply (for example a `Slider` or `Toggle` bound to the same state). The representation is never drawn.
- [API] `accessibilityRespondsToUserInteraction(_:)` (iOS 15 / macOS 12) states whether Switch Control, Voice Control and Full Keyboard Access should treat an element as interactive; by default that is inferred from traits, actions and gestures.
- [Conv] Choose in this order: system control, custom style on a system control, `accessibilityRepresentation`, then hand-built label, value, traits and actions.
- [HIG] Keep the hit region at the platform default size (44x44 pt on iPhone, iPad and Apple Watch) with `frame(minWidth:minHeight:)` and `contentShape(_:)`; the visible glyph can be smaller.

Source: https://developer.apple.com/documentation/swiftui/view/accessibilityadjustableaction(_:) , https://developer.apple.com/documentation/swiftui/view/accessibilityrepresentation(representation:) , https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:) , https://developer.apple.com/design/human-interface-guidelines/gestures

## Focus and announcements

- [API] `@AccessibilityFocusState` with `accessibilityFocused(_:)` or `accessibilityFocused(_:equals:)` (iOS 15 / macOS 12) moves assistive-technology focus, for example to an error message that just appeared. The wrapped value must be `Bool` or optional.
- [API] `AccessibilityNotification.Announcement("Upload finished").post()` (Accessibility framework, iOS 17 / macOS 14) speaks a message; `AccessibilityNotification.LayoutChanged` and `.ScreenChanged` report layout and screen changes. An `AttributedString` announcement can carry a speech priority.
- [HIG] Announce content or layout changes that are only visible, so people using VoiceOver keep an accurate picture of the screen.
- [Conv] Before iOS 17, post through UIKit (`UIAccessibility.post(notification:argument:)`) behind `#if canImport(UIKit)`.

Source: https://developer.apple.com/documentation/swiftui/accessibilityfocusstate , https://developer.apple.com/documentation/accessibility/accessibilitynotification , https://developer.apple.com/design/human-interface-guidelines/voiceover

## Text size in code

- [API] Text styles (`.font(.body)`, `.headline`, ...) scale with Dynamic Type. `Font.custom(_:size:relativeTo:)` (iOS 14 / macOS 11) scales a custom font with a text style; `Font.custom(_:fixedSize:)` never scales.
- [API] `@ScaledMetric` (iOS 14 / macOS 11) scales a number (icon size, spacing, a custom control's height) with a text style.
- [API] `@Environment(\.dynamicTypeSize)` and `isAccessibilitySize` (iOS 15 / macOS 12) tell a view when to restack. `ViewThatFits` and `AnyLayout` (iOS 16 / macOS 13) switch layout without hard-coded breakpoints.
- [API] `dynamicTypeSize(_:)` with a range limits a subtree. [HIG] Use it only for chrome that cannot grow, and pair it with `accessibilityShowsLargeContentViewer()` (iOS 15 / macOS 12), which Apple describes as for items that must stay small, such as tab bar buttons.
- [Conv] Avoid `lineLimit(1)` with `minimumScaleFactor` on content text and avoid fixed heights around text; use `frame(minHeight:)` and let rows grow.
- [API] `\.sizeCategory` and `ContentSizeCategory` are deprecated; use `\.dynamicTypeSize`.

Source: https://developer.apple.com/documentation/swiftui/dynamictypesize , https://developer.apple.com/documentation/swiftui/scaledmetric , https://developer.apple.com/documentation/swiftui/view/accessibilityshowslargecontentviewer() , https://developer.apple.com/design/human-interface-guidelines/typography

## Environment values for accessibility settings

All are read with `@Environment(\.key)`; standard components already respond to them, so read them only for custom drawing, custom animation and custom colors.

| Key | Setting | Minimum OS |
|---|---|---|
| `accessibilityReduceMotion` | Reduce Motion | iOS 13 / macOS 10.15 |
| `accessibilityReduceTransparency` | Reduce Transparency | iOS 13 / macOS 10.15 |
| `accessibilityDifferentiateWithoutColor`, `accessibilityInvertColors` | Differentiate Without Color, Invert Colors | iOS 13 / macOS 10.15 |
| `colorSchemeContrast` (`.standard`, `.increased`) | Increase Contrast | iOS 13 / macOS 10.15 |
| `legibilityWeight` (`.regular`, `.bold`, optional) | Bold Text | iOS 13 / macOS 10.15 |
| `dynamicTypeSize` | Text size | iOS 15 / macOS 12 |
| `accessibilityVoiceOverEnabled`, `accessibilitySwitchControlEnabled` | VoiceOver, Switch Control running | iOS 15 / macOS 12 |
| `accessibilityEnabled` | An assistive technology is enabled | iOS 13 / macOS 10.15 |
| `accessibilityDimFlashingLights`, `accessibilityPlayAnimatedImages` | Dim Flashing Lights; whether animated images may play automatically | iOS 17 / macOS 14 |
| `accessibilityAssistiveAccessEnabled` | Assistive Access | iOS 18 / macOS 15 |
| `accessibilityLargeContentViewerEnabled` | Large Content Viewer enabled | iOS 15 / macOS 12 |
| `accessibilityShowButtonShapes` | Button Shapes | iOS 14 / macOS 11; marked deprecated with a placeholder version, avoid in new code |

- [HIG] With Reduce Motion on, replace movement, scaling and parallax with a fade or no animation; keep the state change visible.
- [HIG] With Reduce Transparency or Increase Contrast on, system materials and colors adapt by themselves; custom translucent backgrounds need an opaque, higher-contrast alternative.
- [Conv] Do not branch behavior on `accessibilityVoiceOverEnabled` to offer a "VoiceOver version" of a screen. Build one interface that works for everyone and use the value only for things like pausing auto-advancing content.

Source: https://developer.apple.com/documentation/swiftui/environmentvalues , https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion , https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityvoiceoverenabled , https://developer.apple.com/design/human-interface-guidelines/motion

## Snippets

Not compiled; every symbol was checked in the documentation data. Minimum OS: iOS 15, macOS 12 (the announcement needs iOS 17, macOS 14). Full controls: `examples/AccessibleCustomControl.swift`, `examples/AccessibleList.swift`.

```swift
import SwiftUI

// Icon-only button: Label keeps a name; the style hides the title visually.
Button(action: addItem) {
    Label("Add Item", systemImage: "plus")
}
.labelStyle(.iconOnly)

// Row read as one element instead of three fragments.
HStack {
    Text(contact.name)
    Spacer()
    Text(contact.city).foregroundStyle(.secondary)
}
.accessibilityElement(children: .combine)

// Decorative image: hidden. Meaningful image: described by what it shows.
Image(systemName: "sparkles").accessibilityHidden(true)
Image("route-map").accessibilityLabel("Map of the route from the harbor to the old town")

// Custom adjustable control (a hand-drawn level meter).
LevelMeter(level: level)
    .accessibilityElement(children: .ignore)
    .accessibilityLabel("Input Level")
    .accessibilityValue("\(level) of 10")
    .accessibilityAdjustableAction { direction in
        switch direction {
        case .increment: level = min(level + 1, 10)
        case .decrement: level = max(level - 1, 0)
        @unknown default: break
        }
    }

// Status that does not depend on color: symbol shape plus text.
Label(isOnline ? "Online" : "Offline",
      systemImage: isOnline ? "checkmark.circle.fill" : "xmark.circle")
    .foregroundStyle(isOnline ? Color.green : Color.secondary)
```

```swift
import SwiftUI

// Reduce Motion: keep the state change, drop the movement.
struct DetailsDisclosure: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion
    @State private var isExpanded = false

    var body: some View {
        VStack(alignment: .leading) {
            Button(isExpanded ? "Hide Details" : "Show Details") {
                withAnimation(reduceMotion ? nil : .easeOut(duration: 0.2)) {
                    isExpanded.toggle()
                }
            }
            if isExpanded {
                Text("Details").transition(.opacity)
            }
        }
    }
}

// Announce a change that is only visible (iOS 17, macOS 14).
func announceUploadFinished() {
    if #available(iOS 17, macOS 14, tvOS 17, watchOS 10, *) {
        AccessibilityNotification.Announcement("Upload finished").post()
    }
    // Fallback for earlier systems: UIAccessibility.post(notification:argument:) on UIKit platforms.
}
```

Source: https://developer.apple.com/documentation/swiftui/label , https://developer.apple.com/documentation/swiftui/view/accessibilityhidden(_:) , https://developer.apple.com/documentation/accessibility/accessibilitynotification/announcement

## UIKit and AppKit equivalents

| Purpose | SwiftUI | UIKit | AppKit |
|---|---|---|---|
| Expose or hide an element | `accessibilityHidden(_:)` | `isAccessibilityElement`, `accessibilityElementsHidden` | `setAccessibilityElement(_:)` |
| Name | `accessibilityLabel(_:)` | `accessibilityLabel` | `setAccessibilityLabel(_:)` |
| Value | `accessibilityValue(_:)` | `accessibilityValue` | `setAccessibilityValue(_:)`, `setAccessibilityValueDescription(_:)` |
| Hint or help | `accessibilityHint(_:)` | `accessibilityHint` | `setAccessibilityHelp(_:)` |
| Role or traits | `accessibilityAddTraits(_:)` | `accessibilityTraits` (`.button`, `.header`, `.selected`, `.adjustable`) | `setAccessibilityRole(_:)` |
| Grouping | `accessibilityElement(children:)` | `accessibilityElements`, `shouldGroupAccessibilityChildren`, `UIAccessibilityElement` | `setAccessibilityChildren(_:)` |
| Adjustable | `accessibilityAdjustableAction(_:)` | `.adjustable` trait + `accessibilityIncrement()`, `accessibilityDecrement()` | `accessibilityPerformIncrement()`, `accessibilityPerformDecrement()` |
| Custom actions | `accessibilityAction(named:_:)` | `accessibilityCustomActions` (`UIAccessibilityCustomAction`, iOS 8) | `setAccessibilityCustomActions(_:)` (macOS 10.13) |
| Rotor | `accessibilityRotor(_:entries:)` | `accessibilityCustomRotors` (iOS 10) | `setAccessibilityCustomRotors(_:)` (macOS 10.13) |
| Voice Control names | `accessibilityInputLabels(_:)` | `accessibilityUserInputLabels` (iOS 13) | `setAccessibilityUserInputLabels(_:)` (macOS 14) |
| Modal scope | `.isModal` trait | `accessibilityViewIsModal` | Sheets and alerts handle this |
| Announce | `AccessibilityNotification.Announcement` | `UIAccessibility.post(notification: .announcement, argument:)`; `.layoutChanged`, `.screenChanged` | `NSAccessibility.post(element:notification:userInfo:)` with `.announcementRequested` and the `.announcement` key |
| Reduce Motion | `\.accessibilityReduceMotion` | `UIAccessibility.isReduceMotionEnabled`; `prefersCrossFadeTransitions` (iOS 14) | `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` |
| Reduce Transparency | `\.accessibilityReduceTransparency` | `UIAccessibility.isReduceTransparencyEnabled` | `accessibilityDisplayShouldReduceTransparency` |
| Increase Contrast | `\.colorSchemeContrast` | `traitCollection.accessibilityContrast`, `UIAccessibility.isDarkerSystemColorsEnabled` | `accessibilityDisplayShouldIncreaseContrast` |
| Differentiate Without Color | `\.accessibilityDifferentiateWithoutColor` | `UIAccessibility.shouldDifferentiateWithoutColor` (iOS 13) | `accessibilityDisplayShouldDifferentiateWithoutColor` |
| Bold Text | `\.legibilityWeight` | `traitCollection.legibilityWeight`, `UIAccessibility.isBoldTextEnabled` | No entry found |
| VoiceOver running | `\.accessibilityVoiceOverEnabled` | `UIAccessibility.isVoiceOverRunning` | `NSWorkspace.shared.isVoiceOverEnabled` (macOS 10.13) |
| Dynamic Type | text styles, `\.dynamicTypeSize` | `preferredFont(forTextStyle:)` + `adjustsFontForContentSizeCategory`, `UIFontMetrics` | Not available on macOS |
| Large Content Viewer | `accessibilityShowsLargeContentViewer()` | `UILargeContentViewerInteraction`, `showsLargeContentViewer`, `largeContentTitle` (iOS 13) | Not applicable |
| Do not invert | `accessibilityIgnoresInvertColors(_:)` | `UIView.accessibilityIgnoresInvertColors` (iOS 11) | No entry found |

- [API] UIKit settings change at run time: observe `UIAccessibility.reduceMotionStatusDidChangeNotification`, `voiceOverStatusDidChangeNotification` and related notifications, or trait changes. AppKit posts `NSWorkspace.accessibilityDisplayOptionsDidChangeNotification`.
- [API] `UIAccessibility.buttonShapesEnabled` is deprecated since iOS 26.1.
- [Conv] Standard UIKit and AppKit controls are accessible by default; the properties above matter for custom views, image-only buttons and custom drawing.

Source: https://developer.apple.com/documentation/uikit/uiaccessibility , https://developer.apple.com/documentation/uikit/accessibility-for-uikit , https://developer.apple.com/documentation/appkit/nsaccessibilityprotocol , https://developer.apple.com/documentation/appkit/accessibility-for-appkit , https://developer.apple.com/documentation/appkit/nsworkspace/accessibilitydisplayshouldreducemotion

## Testing

Automated checks find missing labels and small targets; they do not tell you whether the app is usable. Do both.

- [API] Accessibility Inspector (Xcode > Open Developer Tool > Accessibility Inspector) inspects each element's label, value and traits and runs an audit for problems such as clipped text, unlabeled elements, text size and contrast.
- [API] `XCUIApplication.performAccessibilityAudit(for:_:)` (XCUIAutomation; iOS 17, macOS 14, tvOS 17, watchOS 10) runs an accessibility audit of the current screen inside a UI test; it is declared `throws`. Audit types `.contrast`, `.hitRegion`, `.sufficientElementDescription`, `.elementDetection` and `.all` are available on all of those platforms; `.dynamicType`, `.textClipped` and `.trait` have no macOS entry.
- [Unverified] The documentation page has a declaration but no discussion. That audit issues fail the test, and what the `Bool` returned by the optional `XCUIAccessibilityAuditIssue` handler means, could not be confirmed; check Xcode's Quick Help before using the handler to suppress known issues.

```swift
import XCTest

final class AccessibilityAuditTests: XCTestCase {
    @MainActor
    func testHomeScreenPassesAudit() throws {
        let app = XCUIApplication()
        app.launch()
        // Navigate to each screen you want audited, then:
        try app.performAccessibilityAudit()
        // A narrower audit: try app.performAccessibilityAudit(for: [.contrast, .hitRegion])
    }
}
```

Manual passes, one setting or technology at a time, completing the main task of each screen (Apple's testing guide uses this matrix):

1. [API] VoiceOver on a physical device (Apple notes it is not available in Simulator): every control has a name, role and state; order follows the visual logic; nothing is unreachable; custom gestures have actions.
2. [HIG] Largest text: Larger Accessibility Sizes at maximum on iPhone and iPad. Nothing clips or overlaps; rows restack; bars use the Large Content Viewer.
3. [API] Bold Text, Increase Contrast, Reduce Transparency, Differentiate Without Color, and the color filters, in light and dark appearance.
4. [HIG] Reduce Motion: no parallax, zoom or bounce remains; state changes are still visible.
5. [HIG] Full Keyboard Access (iOS, iPadOS, macOS, visionOS): every action is reachable from the keyboard alone, focus is visible, and no system shortcut is overridden.
6. [Conv] Voice Control: every control can be activated by saying its name, and spoken names match visible text.
7. [Conv] Switch Control: the scan order is logical and no action needs a timed or multi-finger gesture.
8. [API] Button Shapes and On/Off Labels: custom buttons and switches still read as controls.
9. [Conv] Tell the user which of these passes were run and which were not; an agent without a device cannot run any of them.

Source: https://developer.apple.com/documentation/accessibility/accessibility-inspector , https://developer.apple.com/documentation/accessibility/performing-accessibility-testing-for-your-app , https://developer.apple.com/documentation/xcuiautomation/xcuiapplication/performaccessibilityaudit(for:_:) , https://developer.apple.com/design/human-interface-guidelines/accessibility

## Common mistakes

| Mistake | Fix |
|---|---|
| `Button { } label: { Image(systemName: "plus") }` with no name | `Label("Add", systemImage: "plus")`, or add `accessibilityLabel` |
| `onTapGesture` on text, an image or a stack acting as a button | `Button` with that view as its label |
| Label that repeats the role or the symbol name ("plus button") | Name the action: "Add Item" |
| Row announced as separate fragments | `accessibilityElement(children: .combine)` on the row |
| `.ignore` grouping with no label, or `accessibilityHidden(true)` on a container that holds controls | Label the new element; hide only decoration |
| Custom slider, rating or toggle drawn from shapes | System control or custom style; otherwise `accessibilityRepresentation` or label + value + adjustable action |
| Hard-coded font sizes, fixed row heights, `lineLimit(1)` plus `minimumScaleFactor` | Text styles, `frame(minHeight:)`, wrapping, restack at `isAccessibilitySize` |
| Capping `dynamicTypeSize` for a whole screen | Fix the layout; cap only non-growing chrome and add the Large Content Viewer |
| Red and green dots as the only status | Symbol or text as well; honor `accessibilityDifferentiateWithoutColor` |
| Animation that ignores Reduce Motion, or removing the state change with it | Fade or no animation when `accessibilityReduceMotion` is true; keep the change |
| Custom translucent panel unreadable with Reduce Transparency | Opaque background when `accessibilityReduceTransparency` is true |
| Tap target equal to a 20 pt glyph | `frame(minWidth: 44, minHeight: 44)` plus `contentShape` |
| Action available only by swipe, long press or context menu | Visible control or menu item, plus `accessibilityAction(named:)` for custom gestures |
| Decorative image read aloud; informative image silent | `accessibilityHidden(true)` or `Image(decorative:)`; label the informative one |
| Using `accessibilityIdentifier` as the label | Identifier is for tests; add a real label |
| Error shown only by turning a field red | Text message, and move focus to it with `@AccessibilityFocusState` |
| Claiming accessibility after an automated audit only | Run the manual passes, or state they were not run |
