// SettingsForm.swift
//
// Purpose: a settings screen built only from system controls: grouped sections, a toggle,
// a picker, read-only values, navigation rows, and a destructive action kept apart.
//
// Minimum OS: iOS 16, iPadOS 16, macOS 13, tvOS 16, watchOS 9, visionOS 1
//   (NavigationStack, LabeledContent and formStyle set the floor).
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/settings
//   https://developer.apple.com/design/human-interface-guidelines/toggles
//   https://developer.apple.com/design/human-interface-guidelines/pickers
//   https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
//   https://developer.apple.com/design/human-interface-guidelines/action-sheets
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

enum TextDensity: String, CaseIterable, Identifiable {
    case compact, standard, roomy

    var id: Self { self }

    var title: String {
        switch self {
        case .compact: return "Compact"
        case .standard: return "Standard"
        case .roomy: return "Roomy"
        }
    }
}

struct SettingsForm: View {
    // AppStorage persists each value in UserDefaults as soon as it changes.
    @AppStorage("notificationsEnabled") private var notificationsEnabled = true
    @AppStorage("textDensity") private var textDensity = TextDensity.standard
    @State private var isConfirmingReset = false

    var body: some View {
        NavigationStack {
            // Form lays out standard controls the way each platform expects, so rows,
            // labels and control sizes are not hand-built.
            Form {
                Section {
                    // A Toggle's title states what is on or off; the switch shows the state
                    // with position and fill, not color alone.
                    Toggle("Notifications", isOn: $notificationsEnabled)

                    // Picker chooses a platform-appropriate presentation (menu, pop-up
                    // button, pushed list). Each option is a short noun.
                    Picker("Text Density", selection: $textDensity) {
                        ForEach(TextDensity.allCases) { density in
                            Text(density.title).tag(density)
                        }
                    }
                } header: {
                    Text("General")
                } footer: {
                    // Explain the consequence of a setting below the group, in a sentence.
                    Text("Notifications tell you when a shared note changes.")
                }

                Section("Account") {
                    // Navigation rows push more detail instead of crowding this screen.
                    NavigationLink("Privacy") {
                        DetailPlaceholder(title: "Privacy")
                    }
                    NavigationLink("Storage") {
                        DetailPlaceholder(title: "Storage")
                    }
                }

                Section("About") {
                    // LabeledContent pairs a visible label with a read-only value and reads
                    // as one element in VoiceOver.
                    LabeledContent("Version", value: "1.0")
                }

                // Convention: keep a destructive action in its own section, away from
                // routine controls, so it is hard to hit by accident.
                Section {
                    Button("Reset All Settings", role: .destructive) {
                        isConfirmingReset = true
                    }
                }
            }
            // Grouped style keeps sections visually separate on every platform.
            .formStyle(.grouped)
            .navigationTitle("Settings")
            // A confirmation dialog suits a choice that follows an action the person took
            // on purpose. It names the action, marks it destructive, and offers Cancel.
            .confirmationDialog(
                "Reset all settings?",
                isPresented: $isConfirmingReset,
                titleVisibility: .visible
            ) {
                Button("Reset All Settings", role: .destructive) {
                    notificationsEnabled = true
                    textDensity = .standard
                }
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("Your notes are not affected.")
            }
        }
    }
}

private struct DetailPlaceholder: View {
    let title: String

    var body: some View {
        Form {
            Text("\(title) settings")
        }
        .formStyle(.grouped)
        .navigationTitle(title)
    }
}

// On Mac, present this content from a Settings scene (see MacAppScenes.swift) so it opens
// from the app menu with the standard Command-Comma shortcut. Do not build an in-window
// settings screen there.
