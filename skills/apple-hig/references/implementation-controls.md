# Native controls in SwiftUI

Scope: SwiftUI controls and their styles (buttons, toggles, pickers, menus, text input, forms, lists, indicators, system pickers and feedback), with verified minimum OS versions, the platforms where each control is missing, and a HIG-component-to-API map. Design guidance is in `references/components-controls.md` and `references/components-content.md`.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Reading availability
- Buttons
- Toggles, pickers and value controls
- Menus and context menus
- Text input
- Forms and labeled content
- Lists
- Grouping, progress and system pickers
- Platform availability gaps
- HIG component to SwiftUI API
- Common mistakes

## Reading availability

- [API] Versions are `introducedAt` values from the documentation JSON. A dash or "not on" means the documentation lists no availability for that platform; compile the code out with `#if os(...)`.
- [API] Documentation landing pages merge overloads and can show a newer minimum than the oldest overload. Example: `Button(_:role:action:)`, `Toggle(_:isOn:)` and `Picker(_:selection:content:)` show iOS 16 (the `LocalizedStringResource` overload) while the `LocalizedStringKey` and `StringProtocol` overloads are iOS 15, 13 and 13. Minimums here are for the oldest overload.
- [Conv] Nothing here was compiled; build before claiming it works. Prefer a standard control over a custom one: it brings accessibility traits, focus, keyboard, pointer and the current system appearance.

Source: https://developer.apple.com/documentation/swiftui/controls-and-indicators, https://developer.apple.com/documentation/swiftui/view-styles

## Buttons

| API | Availability | Notes |
|---|---|---|
| `Button(_:role:action:)`, `Button(role:action:label:)`; `.destructive`, `.cancel` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Role conveys meaning; the system styles and places the button. |
| `ButtonRole.close`, `.confirm`; `Button(role:action:)` without a label | OS 26+ on all platforms | System-provided label and symbol. |
| `.buttonStyle(.plain)` / `.borderless` | iOS 13+, macOS 10.15+, visionOS 1+; plain: tvOS 13+, watchOS 6+; borderless: tvOS 17+, watchOS 8+ | |
| `.buttonStyle(.bordered)` / `.borderedProminent` | iOS 15+, visionOS 1+; bordered: macOS 10.15+, tvOS 13+, watchOS 7+; prominent: macOS 12+, tvOS 15+, watchOS 8+ | Prominent is filled with the tint. |
| `.buttonStyle(.glass)` / `.glassProminent` | iOS 26+, macOS 26+, tvOS 26+, watchOS 26+; not on visionOS | Liquid Glass buttons. |
| `controlSize(_:)`: `.mini`, `.small`, `.regular`, `.large` | iOS 15+, macOS 10.15+ (`.large`: macOS 11+), tvOS 15+, watchOS 9+, visionOS 1+ | `.extraLarge`: iOS 17+, macOS 14+, tvOS 17+, watchOS 10+. |
| `buttonBorderShape(_:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | `.capsule`: macOS 14+, tvOS 17+. `.circle`: iOS 17+, macOS 14+, tvOS 16.4+, watchOS 10+. |

```swift
// iOS 15+, macOS 12+, tvOS 15+, watchOS 9+, visionOS 1+. Glass: OS 26+, no visionOS entry (`*` would match it, hence #if).
HStack {
    Button("Cancel", role: .cancel) { dismiss() }
        .buttonStyle(.bordered)
    #if os(visionOS)
    Button("Save") { save() }.buttonStyle(.borderedProminent)
    #else
    if #available(iOS 26, macOS 26, tvOS 26, watchOS 26, *) {
        Button("Save") { save() }.buttonStyle(.glassProminent)
    } else {
        Button("Save") { save() }.buttonStyle(.borderedProminent)
    }
    #endif
}
.controlSize(.large)
```

- [HIG] Use a prominent style for the most likely action in a view and keep prominent buttons few. Distinguish the preferred choice by style, not by size.
- [HIG] Do not give the default (primary) role to a destructive action. Give buttons a hit region of at least 44x44 pt (60x60 pt in visionOS).
- [API] Icon-only button: `Button("Add", systemImage: "plus") { }` with `.labelStyle(.iconOnly)`, or a `Label`; never a bare `Image` without `accessibilityLabel(_:)`.
- [Conv] Use `Button`, not `onTapGesture` on a `Text` or `HStack`: a gesture has no button trait, focus, keyboard activation, hover effect or pressed state.

Source: https://developer.apple.com/documentation/swiftui/button, https://developer.apple.com/documentation/swiftui/buttonrole, https://developer.apple.com/documentation/swiftui/primitivebuttonstyle, https://developer.apple.com/documentation/swiftui/controlsize, https://developer.apple.com/design/human-interface-guidelines/buttons

## Toggles, pickers and value controls

| API | Availability | Notes |
|---|---|---|
| `Toggle(_:isOn:)`, `Toggle(isOn:label:)` | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | `.toggleStyle(.switch)`: tvOS 18+. `.button`: iOS 15+, macOS 12+, watchOS 9+, not tvOS. `.checkbox`: macOS only. |
| `Picker(_:selection:content:)` with `.tag(_:)` | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | [Conv] Each tag's type must match the selection type. |
| `.pickerStyle(.segmented)` / `.menu` | iOS 13+ / 14+, macOS 10.15+ / 11+, tvOS 13+ / 17+, visionOS 1+; not on watchOS | `.menu` is the HIG "pop-up button". |
| `.pickerStyle(.wheel)` | iOS 13+, watchOS 6+, visionOS 1+; not on macOS or tvOS | |
| `.pickerStyle(.inline)` / `.navigationLink` | inline: iOS 14+, macOS 11+, tvOS 14+, watchOS 7+; navigationLink: iOS 16+, tvOS 16+, watchOS 9+, not macOS | Both visionOS 1+. |
| `.pickerStyle(.palette)` / `.radioGroup` | palette: iOS 17+, macOS 14+, visionOS 1+; radioGroup: macOS 10.15+ only | Palette: one symbol per option, meant for menus; elsewhere it renders as a segmented picker. |
| `DatePicker(_:selection:displayedComponents:)`, `DatePicker(_:selection:in:displayedComponents:)` | iOS 13+, macOS 10.15+, watchOS 10+, visionOS 1+; not on tvOS | Styles: `.compact`, `.graphical` (iOS 14+, macOS 10.15+, visionOS 1+); `.wheel` (iOS 13+, watchOS 10+, visionOS 1+). `MultiDatePicker`: iOS 16+, visionOS 1+. |
| `Stepper(_:value:in:step:)` | iOS 13+, macOS 10.15+, watchOS 9+, visionOS 1+; not on tvOS | [Conv] Put the value in the title: `Stepper("Guests: \(count)", value: $count, in: 1...10)`. |
| `Slider(value:in:step:)`, `Slider(value:in:label:minimumValueLabel:maximumValueLabel:)` | iOS 13+, macOS 10.15+, watchOS 6+, visionOS 1+; not on tvOS | Default range `0...1`. Give it a label closure; it names the control. |

- [HIG] Use the switch style only in a list row, where the row says what the switch controls. Change the switch color only if necessary.
- [HIG] Date picker styles: compact is a button that opens a modal editor; inline shows wheels (time only) or a calendar.
- [Conv] Leave `pickerStyle` and `toggleStyle` unset inside a `Form` unless there is a reason: the automatic style is the platform's choice for that context.
- [API] `labelsHidden()` hides a control's visible label; keep the label itself so assistive technologies still have a name.

Source: https://developer.apple.com/documentation/swiftui/toggle, https://developer.apple.com/documentation/swiftui/pickerstyle, https://developer.apple.com/documentation/swiftui/datepicker, https://developer.apple.com/documentation/swiftui/stepper, https://developer.apple.com/documentation/swiftui/slider, https://developer.apple.com/design/human-interface-guidelines/toggles, https://developer.apple.com/design/human-interface-guidelines/pickers

## Menus and context menus

```swift
// Menu: iOS 14+, macOS 11+, tvOS 17+, visionOS 1+; not on watchOS.
// Buttons with systemImage and role: iOS 15+, macOS 12+.
Menu("Sort", systemImage: "arrow.up.arrow.down") {
    Picker("Sort By", selection: $sortOrder) {
        Text("Name").tag(SortOrder.name)
        Text("Date").tag(SortOrder.date)
    }
    Divider()
    Button("Reverse Order") { isReversed.toggle() }
}
MessageRow(message: message).contextMenu {
    Button("Reply", systemImage: "arrowshape.turn.up.left") { reply(to: message) }
    Button("Delete", systemImage: "trash", role: .destructive) { delete(message) }
}
```

- [API] `Menu(_:content:primaryAction:)` (iOS 15+, macOS 12+, tvOS 17+, visionOS 1+) runs an action on tap and opens the menu on a secondary gesture. `menuOrder(_:)` is iOS 16+; `menuActionDismissBehavior(_:)` is iOS 16.4+; `menuIndicator(_:)` is iOS 15+.
- [API] `contextMenu(menuItems:)` is iOS 13+, macOS 10.15+, tvOS 14+, visionOS 1+ and deprecated on watchOS since watchOS 7. `contextMenu(menuItems:preview:)` is iOS 16+, macOS 13+, tvOS 16+, visionOS 1+. `contextMenu(forSelectionType:menu:primaryAction:)` is iOS 16+, macOS 13+, visionOS 1+. The `contextMenu(_:)` form taking a `ContextMenu` value is deprecated.
- [HIG] Always make context menu items available in the main interface too. Hide unavailable context-menu items instead of dimming them.
- [HIG] A menu is for choices people reveal on purpose; use a confirmation dialog for choices that follow an action (see `references/implementation-navigation.md`).

Source: https://developer.apple.com/documentation/swiftui/menu, https://developer.apple.com/documentation/swiftui/menus-and-commands, https://developer.apple.com/design/human-interface-guidelines/menus, https://developer.apple.com/design/human-interface-guidelines/context-menus

## Text input

```swift
// iOS 15+, tvOS 15+, visionOS 1+. keyboardType and textInputAutocapitalization do not exist on macOS.
// State: @FocusState private var focus: Field?   (enum Field { case email, password })
TextField("Email", text: $email)
    .textContentType(.emailAddress)
    .keyboardType(.emailAddress)
    .textInputAutocapitalization(.never)
    .autocorrectionDisabled()
    .submitLabel(.next)
    .focused($focus, equals: .email)
    .onSubmit { focus = .password }
SecureField("Password", text: $password)
    .textContentType(.password)
    .submitLabel(.done)
    .focused($focus, equals: .password)
```

| API | Availability | Notes |
|---|---|---|
| `TextField(_:text:)`, `SecureField(_:text:)` | iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+ | `TextField(_:text:prompt:)`, `TextField(_:value:format:prompt:)`: iOS 15+. `TextField(_:text:axis:)` (grows vertically): iOS 16+. `TextEditor`: iOS 14+, macOS 11+, visionOS 1+. |
| `textContentType(_:)` | `UITextContentType` overload iOS 13+; `NSTextContentType` overload macOS 11+ | Different parameter type per platform: guard with `#if`. Enables AutoFill and one-time codes. |
| `keyboardType(_:)` | iOS 13+, tvOS 13+, visionOS 1+; not on macOS or watchOS | |
| `textInputAutocapitalization(_:)`, `autocorrectionDisabled(_:)` | iOS 15+ / 13+, tvOS 15+ / 13+, watchOS 8+, visionOS 1+; autocapitalization not on macOS | Replace deprecated `autocapitalization(_:)` and `disableAutocorrection(_:)`. |
| `submitLabel(_:)`, `onSubmit(of:_:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | `.next`, `.done`, `.search` and others. |
| `@FocusState`, `focused(_:)`, `focused(_:equals:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | Move focus between fields; dismiss the keyboard by setting it to `nil`. |
| `textFieldStyle(.roundedBorder)` | deprecated (iOS, macOS) | Replacement `.bordered` with `textInputBorderShape(_:)` is OS 27+ only. Below 27 use `.automatic`, or keep `.roundedBorder` in a fallback branch. |

- [HIG] Always use a secure field for sensitive data such as passwords. Show the keyboard type that matches the content (iOS, iPadOS, tvOS, visionOS).
- [HIG] Placeholder text disappears when typing starts, so also give the field a separate label. In a `Form`, `LabeledContent("Email") { TextField(...) }` (iOS 16+) or the row title does this.
- [Conv] Set `textContentType` on sign-in, address and one-time-code fields (`.username`, `.password`, `.newPassword`, `.oneTimeCode`, `.emailAddress`).

Source: https://developer.apple.com/documentation/swiftui/textfield, https://developer.apple.com/documentation/swiftui/securefield, https://developer.apple.com/documentation/swiftui/text-input-and-output, https://developer.apple.com/documentation/swiftui/submitlabel, https://developer.apple.com/design/human-interface-guidelines/text-fields

## Forms and labeled content

```swift
// iOS 16+, macOS 13+, watchOS 9+, visionOS 1+ (Stepper is not on tvOS)
Form {
    Section("General") {
        Toggle("Notifications", isOn: $notificationsEnabled)
        Picker("Sort By", selection: $sortOrder) {
            Text("Name").tag(SortOrder.name)
            Text("Date").tag(SortOrder.date)
        }
        Stepper("Items per page: \(itemsPerPage)", value: $itemsPerPage, in: 10...100, step: 10)
    }
    Section("About") { LabeledContent("Version", value: appVersion) }
}
```

- [API] `Form` is iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+. `Section(_:content:)` is iOS 15+, macOS 12+, tvOS 15+, watchOS 8+; `Section(content:header:footer:)` is iOS 13+.
- [API] `formStyle(_:)` with `.grouped` and `.columns` is iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+. [Conv] On macOS `.formStyle(.grouped)` gives the System Settings look; the default is a column of trailing-aligned labels.
- [API] `LabeledContent(_:value:)` and `LabeledContent(_:content:)` are iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+: a label plus a read-only value or any control, aligned like the system rows.
- [Conv] Build settings and data-entry screens from `Form` rows rather than hand-laid `HStack`s; rows then get platform spacing, Dynamic Type growth and right-to-left layout.

Source: https://developer.apple.com/documentation/swiftui/form, https://developer.apple.com/documentation/swiftui/labeledcontent, https://developer.apple.com/design/human-interface-guidelines/settings

## Lists

```swift
// iOS 15+, macOS 12+, watchOS 8+, visionOS 1+ (swipeActions is not on tvOS)
List {
    ForEach(messages) { message in
        MessageRow(message: message)
            .swipeActions(edge: .trailing) {
                Button("Delete", systemImage: "trash", role: .destructive) { delete(message) }
            }
            .swipeActions(edge: .leading) {
                Button("Flag", systemImage: "flag") { toggleFlag(message) }.tint(.orange)
            }
    }
}
.refreshable { await reload() }
```

| API | Availability | Notes |
|---|---|---|
| `.listStyle(.plain)` / `.grouped` | plain: iOS 13+, macOS 10.15+, tvOS 13+, watchOS 6+, visionOS 1+; grouped: iOS 13+, tvOS 13+, visionOS 1+ | |
| `.listStyle(.insetGrouped)` / `.sidebar` / `.inset` | insetGrouped: iOS 14+, visionOS 1+ only; sidebar: iOS 14+, macOS 10.15+; inset: iOS 14+, macOS 11+ | `.bordered`: macOS 12+ only. |
| `swipeActions(edge:allowsFullSwipe:content:)` | iOS 15+, macOS 12+, watchOS 8+, visionOS 1+ | Actions appear in order from the originating edge; a full swipe runs the first one by default. |
| `refreshable(action:)` | iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+ | On iOS and iPadOS a `List` gets pull-to-refresh; the indicator stays for the duration of the async handler. |
| `List(_:selection:rowContent:)`, `List(selection:content:)` | iOS 13+, macOS 10.15+, tvOS 13+, visionOS 1+ (no watchOS entry on the overloads checked) | Optional ID binding: single selection. `Set` binding: multiple selection. |
| `EditButton`, `\.editMode` | iOS 13+, visionOS 1+ (`editMode` also tvOS 13+); not on macOS | Toggles edit mode (needed for multi-select by tap); `onDelete(perform:)` / `onMove(perform:)` on `ForEach` supply delete and reorder. |
| `listRowSeparator(_:edges:)`, `listRowSeparatorTint(_:edges:)` | iOS 15+, macOS 13+, visionOS 1+ | Not deprecated. |
| `ContentUnavailableView`, `.search`, `.search(text:)` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+ | Empty and no-results states. |

- [Conv] Treat swipe actions like context menu items (which the HIG says must also be available in the main interface): offer the same action in a toolbar or detail view, and for custom rows expose it with `accessibilityAction(named:_:)`.
- [HIG] Let people edit and reorder a list when it makes sense; in iOS and iPadOS they enter an edit mode before selecting items.

Source: https://developer.apple.com/documentation/swiftui/list, https://developer.apple.com/documentation/swiftui/liststyle, https://developer.apple.com/documentation/swiftui/editbutton, https://developer.apple.com/documentation/swiftui/contentunavailableview, https://developer.apple.com/design/human-interface-guidelines/lists-and-tables

## Grouping, progress and system pickers

| API | Availability | Notes |
|---|---|---|
| `DisclosureGroup(_:content:)`, `DisclosureGroup(_:isExpanded:content:)` | iOS 14+, macOS 11+, visionOS 1+; not on tvOS or watchOS | Show and hide related content. `OutlineGroup` has the same availability. |
| `ControlGroup` | iOS 15+, macOS 12+, tvOS 17+, visionOS 1+; not on watchOS | Related buttons as one unit; styles `.navigation` (iOS 15+), `.compactMenu` (iOS 16.4+). |
| `ProgressView()`, `ProgressView(_:)` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | Indeterminate. |
| `ProgressView(value:total:)`, `ProgressView(_:value:total:)` | same | Determinate; `value` is optional and `total` defaults to 1.0. Styles `.linear`, `.circular`. |
| `Gauge(value:in:label:)`, `gaugeStyle(_:)` | iOS 16+, macOS 13+, watchOS 7+, visionOS 1+; not on tvOS | A level within a range, not task progress. |
| `ShareLink(item:subject:message:)` and titled forms | iOS 16+, macOS 13+, watchOS 9+, visionOS 1+; not on tvOS | System share sheet for a `URL`, `String` or other `Transferable`. |
| `PhotosPicker(selection:matching:...)` (`import PhotosUI`) | iOS 16+, macOS 13+, watchOS 9+; visionOS listed without a version; not on tvOS | Results are `PhotosPickerItem` placeholders loaded as `Transferable`. |
| `ColorPicker` | iOS 14+, macOS 11+, visionOS 1+ | |
| `sensoryFeedback(_:trigger:)` | iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 26+ | Haptic and/or audio feedback when the trigger value changes: `.success`, `.selection`, `.impact` and others. |

```swift
// iOS 17+, macOS 14+, watchOS 10+ (ShareLink and PhotosPicker alone: iOS 16+, macOS 13+, watchOS 9+)
VStack {
    ProgressView("Uploading", value: fractionCompleted)
    ShareLink(item: article.url)
    PhotosPicker(selection: $pickedItem, matching: .images) {
        Label("Choose Photo", systemImage: "photo")
    }
}
.sensoryFeedback(.success, trigger: uploadCount)
```

- [HIG] Prefer a determinate progress indicator when the duration is known; it lets people judge how long to wait.
- [HIG] Use system haptic patterns according to their documented meanings and consistently; standard controls such as switches, sliders and pickers already play their own.
- [Unverified] That `PhotosPicker` needs no photo-library permission prompt: widely stated, not confirmed in the pages checked.

Source: https://developer.apple.com/documentation/swiftui/disclosuregroup, https://developer.apple.com/documentation/swiftui/progressview, https://developer.apple.com/documentation/swiftui/gauge, https://developer.apple.com/documentation/swiftui/sharelink, https://developer.apple.com/documentation/photosui/photospicker, https://developer.apple.com/documentation/swiftui/sensoryfeedback, https://developer.apple.com/design/human-interface-guidelines/progress-indicators, https://developer.apple.com/design/human-interface-guidelines/playing-haptics

## Platform availability gaps

Minimum version per platform; a dash means no availability entry in the documentation.

| Control | iOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| `Menu` | 14 | 11 | 17 | - | 1 |
| `contextMenu(menuItems:)` | 13 | 10.15 | 14 | deprecated since 7 | 1 |
| `DatePicker` | 13 | 10.15 | - | 10 | 1 |
| `Stepper` / `Slider` | 13 | 10.15 | - | 9 / 6 | 1 |
| `TextEditor`, `ColorPicker`, `DisclosureGroup` | 14 | 11 | - | - | 1 |
| `ControlGroup` | 15 | 12 | 17 | - | 1 |
| `Gauge` / `ShareLink` | 16 | 13 | - | 7 / 9 | 1 |
| `PhotosPicker` | 16 | 13 | - | 9 | listed, no version |
| `Table` | 16 | 12 | - | - | 1 |
| `EditButton` | 13 | - | - | - | 1 |
| `swipeActions` | 15 | 12 | - | 8 | 1 |
| `keyboardType(_:)` | 13 | - | 13 | - | 1 |
| Segmented picker | 13 | 10.15 | 13 | - | 1 |
| Wheel picker | 13 | - | - | 6 | 1 |
| Checkbox toggle, radio-group picker | - | 10.15 | - | - | - |
| Inset grouped list | 14 | - | - | - | 1 |
| `sensoryFeedback` | 17 | 14 | 17 | 10 | 26 |

Source: https://developer.apple.com/documentation/swiftui/controls-and-indicators, https://developer.apple.com/documentation/swiftui/pickerstyle, https://developer.apple.com/documentation/swiftui/liststyle

## HIG component to SwiftUI API

"HIG link" means the HIG page itself links to that API as developer guidance; other rows are [Conv] mappings.

| HIG component | SwiftUI API | Basis |
|---|---|---|
| Buttons | `Button`, `buttonStyle`, `buttonBorderShape` | HIG link |
| Pop-up buttons / Pull-down buttons | `Picker` with `.pickerStyle(.menu)` / `Menu` | HIG link (`MenuPickerStyle`) / [Conv] |
| Menus / Context menus | `Menu` / `contextMenu(menuItems:)` | HIG link |
| Toggles | `Toggle`, `toggleStyle` | HIG link |
| Pickers / Segmented controls | `Picker`, `DatePicker` / `.pickerStyle(.segmented)` | HIG link |
| Sliders / Steppers | `Slider` / `Stepper` | HIG link / [Conv] |
| Text fields | `TextField`, `SecureField` | HIG link |
| Labels / Text views | `Text`, `Label` / `Text`, `TextEditor` for editing | HIG link; `TextEditor` is [Conv] |
| Lists and tables | `List`, `listStyle`, `Table` | HIG link |
| Outline views / Disclosure controls | `OutlineGroup` / `DisclosureGroup` | HIG link |
| Boxes / Scroll views | `GroupBox` / `ScrollView` | HIG link |
| Progress indicators / Gauges | `ProgressView` / `Gauge` | HIG link |
| Page controls | `TabView` with `.tabViewStyle(.page)` | HIG link (`PageTabViewStyle`) |
| Activity views / Color wells | `ShareLink` / `ColorPicker` | [Conv] |
| Collections | `LazyVGrid`, `LazyHGrid` in a `ScrollView` | [Conv] |
| Search fields, alerts, action sheets, sheets, popovers, tab bars, toolbars, sidebars, split views | see `references/implementation-navigation.md` | |

Source: https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons, https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons, https://developer.apple.com/design/human-interface-guidelines/segmented-controls, https://developer.apple.com/design/human-interface-guidelines/disclosure-controls, https://developer.apple.com/design/human-interface-guidelines/activity-views

## Common mistakes

| Mistake | Fix |
|---|---|
| `onTapGesture` on text, images or stacks used as a button | `Button` with a style; `.buttonStyle(.plain)` if it must look like content. |
| Destructive action styled as the prominent default | `role: .destructive`, a neutral style, and a Cancel choice. |
| Custom toggle, slider or segmented control drawn from shapes | The standard control with a style; if truly custom, see `references/accessibility-implementation.md`. |
| `Menu`, `DatePicker`, `Stepper`, `Slider`, `EditButton`, `.insetGrouped` in shared multiplatform code | Check the gap table; `#if os(...)` and a platform-appropriate alternative. |
| Passwords in a `TextField`; generic keyboard for email or numbers | `SecureField`; `keyboardType`, `textContentType`, `submitLabel`. |
| `.textFieldStyle(.roundedBorder)` in new code targeting OS 27 | `.bordered` with `textInputBorderShape(_:)` on 27+; `.automatic` or a marked fallback below. |
| Hand-built spinner, share sheet, photo grid picker or empty state | `ProgressView`, `ShareLink`, `PhotosPicker`, `ContentUnavailableView`. |
| Glass button styles without an availability check | `#available(iOS 26, macOS 26, *)` with `.borderedProminent` / `.bordered` fallback, inside `#if !os(visionOS)` when the file also builds for visionOS. |
