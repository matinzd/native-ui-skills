# Example: a complete HIG review

An illustration of the review format from `SKILL.md`, applied to one SwiftUI file. The code under review is
shown first so the findings can be followed. Sources were checked on 2026-11-23.

## Input

Request: "Review EventEditor.swift against the HIG. iPhone and iPad, minimum iOS 17. It is presented as a
sheet for both new and existing events."

```swift
// Before: the code under review (deliberately flawed; do not copy)
struct EventEditor: View {
    @Environment(\.dismiss) private var dismiss
    let store: EventStore
    @State var event: Event

    var body: some View {
        NavigationStack {
            Form {
                TextField("Title", text: $event.title)
                TextField("Video call link", text: $event.link)
                Button("All day") { event.isAllDay.toggle() }
                    .tint(event.isAllDay ? .green : .gray)
                HStack {
                    Text("Starts")
                    Spacer()
                    Text("-").onTapGesture { event.start.addTimeInterval(-3600) }
                    Text(event.start.formatted(date: .abbreviated, time: .shortened))
                    Text("+").onTapGesture { event.start.addTimeInterval(3600) }
                }
                Button("Delete Event") {
                    store.delete(event)
                    dismiss()
                }
                .buttonStyle(.borderedProminent)
            }
            .scrollContentBackground(.hidden)
            .background(Color.white)
            .navigationTitle("New Event")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { store.save(event); dismiss() }
                }
            }
            .onChange(of: event.start) { newStart in
                if event.end < newStart { event.end = newStart.addingTimeInterval(3600) }
            }
        }
        .preferredColorScheme(.light)
        .presentationSizing(.form)
    }
}
```

## Output

## HIG review: EventEditor.swift
Target: iPhone and iPad, minimum iOS 17 (stated), SwiftUI. Evidence: source code only, so rendered sizes,
contrast, and assistive-technology output were not measured.

### 1. `presentationSizing(_:)` needs iOS 18
- Class: Confirmed guideline or API violation
- Severity: High
- Where: `.presentationSizing(.form)` on the `NavigationStack`
- Why: The modifier and `PresentationSizing.form` were introduced in iOS 18.0. With a minimum of iOS 17 and no
  availability check, the target does not compile, so nobody gets the editor.
- Source: https://developer.apple.com/documentation/swiftui/view/presentationsizing(_:) (API documentation)
- Fix: Guard it and keep the iOS 17 path unchanged:
  `extension View { @ViewBuilder func formSizedSheet() -> some View {`
  `if #available(iOS 18.0, *) { presentationSizing(.form) } else { self } } }`

### 2. Start time is changed by tapping "-" and "+" text
- Class: Accessibility issue
- Severity: High
- Where: the two `Text` views with `onTapGesture` in the "Starts" row
- Why: These are plain text, not controls, so nothing identifies them as actionable to VoiceOver, Voice
  Control, Switch Control, or a hardware keyboard, and "-" and "+" do not say what they change. Everyone else
  can only move the start in one-hour steps and cannot pick a day directly.
- Source: https://developer.apple.com/documentation/swiftui/button (API documentation);
  https://developer.apple.com/design/human-interface-guidelines/pickers (recommendation)
- Fix: Replace the whole `HStack` with the system control: `DatePicker("Starts", selection: $event.start)`.

### 3. "All day" shows its state by color alone
- Class: Accessibility issue
- Severity: High
- Where: `Button("All day")` with `.tint(event.isAllDay ? .green : .gray)`
- Why: On and off differ only in tint, so people who cannot tell the two colors apart cannot see the setting,
  and a plain button gives assistive technologies no on or off value to report.
- Source: https://developer.apple.com/design/human-interface-guidelines/toggles (recommendation);
  https://developer.apple.com/design/human-interface-guidelines/accessibility (recommendation)
- Fix: `Toggle("All day", isOn: $event.isAllDay)`. The row is in a `Form`, which is where the HIG places the
  switch style.

### 4. "Delete Event" is the most prominent button and deletes at once
- Class: Recommended improvement
- Severity: Medium
- Where: `Button("Delete Event")` with `.buttonStyle(.borderedProminent)`
- Why: The HIG keeps the prominent style for the most likely action and says not to give a destructive action
  the primary role, because people sometimes choose a prominent button without reading it. Here one tap
  removes the event with no chance to back out.
- Source: https://developer.apple.com/design/human-interface-guidelines/buttons (recommendation);
  https://developer.apple.com/design/human-interface-guidelines/action-sheets (recommendation)
- Fix: Drop the prominent style and confirm first:
  `Button("Delete Event", role: .destructive) { confirmDelete = true }` with
  `.confirmationDialog("Delete this event?", isPresented: $confirmDelete, titleVisibility: .visible) {`
  `Button("Delete Event", role: .destructive) { store.delete(event); dismiss() } }`.
  A SwiftUI confirmation dialog includes Cancel by default.

### 5. Done has no Cancel beside it
- Class: Recommended improvement
- Severity: Medium
- Where: the `.toolbar` with a single `.confirmationAction` item
- Why: With Done alone, saving looks like the only way out. People who opened the sheet by mistake, or changed
  their mind, have no visible way to leave without saving.
- Source: https://developer.apple.com/design/human-interface-guidelines/sheets (recommendation)
- Fix: Add `ToolbarItem(placement: .cancellationAction) { Button("Cancel") { dismiss() } }`.

### 6. The sheet is pinned to a light appearance
- Class: Platform convention mismatch
- Severity: Medium
- Where: `.preferredColorScheme(.light)`, `.scrollContentBackground(.hidden)`, `.background(Color.white)`
- Why: The modifier overrides the person's Dark Mode choice for this presentation, so a white sheet appears
  over an otherwise dark app. It works, but people expect a sheet to follow the system appearance.
- Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode (recommendation);
  https://developer.apple.com/documentation/swiftui/view/preferredcolorscheme(_:) (API documentation)
- Fix: Delete all three modifiers. The `Form` then uses its system background in both appearances.

### 7. The link field shows the default keyboard
- Class: Recommended improvement
- Severity: Low
- Where: `TextField("Video call link", text: $event.link)`
- Why: A URL typed on the default keyboard is slower to enter. The HIG asks for the keyboard type that matches
  the content.
- Source: https://developer.apple.com/design/human-interface-guidelines/text-fields (recommendation)
- Fix: Add `.keyboardType(.URL)`, `.textContentType(.URL)`, `.textInputAutocapitalization(.never)`, and
  `.autocorrectionDisabled()`.

### 8. Deprecated `onChange(of:perform:)`
- Class: Confirmed guideline or API violation
- Severity: Low
- Where: `.onChange(of: event.start) { newStart in ... }`
- Why: The one-parameter form was deprecated in iOS 17.0, and its replacement `onChange(of:initial:_:)` is
  available from iOS 17.0, which is this project's minimum.
- Source: https://developer.apple.com/documentation/swiftui/view/onchange(of:perform:) (API documentation)
- Fix: `.onChange(of: event.start) { _, newStart in ... }`. Apple notes that the replacement's closure captures
  state after the change, not before; this body only uses the parameter and the current `event.end`.

### 9. Title and Delete do not depend on whether the event is new
- Class: Subjective design suggestion
- Severity: Low
- Where: `.navigationTitle("New Event")` and the Delete button
- Why: Opinion, no source. When the sheet edits an existing event the title is wrong, and a new event has
  nothing to delete yet.
- Fix: Pass an `isNew` flag; use "Edit Event" as the title and show Delete only when `isNew` is false.

### Not verified
- What VoiceOver actually announces for the "-" and "+" text and for the tinted button: run the screen with
  VoiceOver or Accessibility Inspector (affects findings 2 and 3).
- Whether a deleted event can be restored elsewhere in the app. If it can, undo may serve better than a
  confirmation (finding 4). Check: https://developer.apple.com/design/human-interface-guidelines/alerts
- What a swipe down on the sheet does with unsaved edits: the presenting view was not provided.
- How the sheet is sized on iPad under iOS 17 and iOS 18: run both in the simulator after applying finding 1.

### What already works
- The editor is a `Form` in a `NavigationStack`, so rows, spacing, scrolling, and the title bar are the system's.
- Done uses the `.confirmationAction` placement, so the system decides where it goes on each platform.
- Text uses default styles with no fixed font sizes, and the start time is formatted with the person's locale.
