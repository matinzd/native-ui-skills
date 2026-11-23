// Presentations.swift
//
// Purpose: the three standard modal presentations done with system API: a resizable sheet
// with Cancel and Save, an alert with a specific title and verb buttons, and a
// confirmation dialog for a destructive action with a Cancel button.
//
// Minimum OS: iOS 16, iPadOS 16, macOS 13, tvOS 16, watchOS 9, visionOS 1
//   (presentationDetents and NavigationStack set the floor; alert and confirmationDialog
//   in this form are available from iOS 15 / macOS 12).
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/sheets
//   https://developer.apple.com/design/human-interface-guidelines/alerts
//   https://developer.apple.com/design/human-interface-guidelines/action-sheets
//   https://developer.apple.com/design/human-interface-guidelines/modality
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

struct PresentationsExample: View {
    @State private var notes: [String] = ["Groceries", "Trip ideas"]
    @State private var isComposing = false
    @State private var isConfirmingDelete = false
    @State private var showsSyncError = false

    var body: some View {
        NavigationStack {
            List(notes, id: \.self) { note in
                Text(note)
            }
            .navigationTitle("Notes")
            .toolbar {
                // Semantic placements: the system puts each item where the platform
                // expects it.
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        isComposing = true
                    } label: {
                        Label("New Note", systemImage: "square.and.pencil")
                    }
                }
                ToolbarItem(placement: .destructiveAction) {
                    Button("Delete All", role: .destructive) {
                        isConfirmingDelete = true
                    }
                    .disabled(notes.isEmpty)
                }
            }
            .sheet(isPresented: $isComposing) {
                ComposeSheet { title in
                    notes.append(title)
                    // Demo only: pretend the upload failed to show the alert.
                    showsSyncError = true
                }
                // Medium plus large: the sheet can rest at half height and expand.
                .presentationDetents([.medium, .large])
                // Keep the grabber visible on a resizable sheet; it also lets VoiceOver
                // users resize it.
                .presentationDragIndicator(.visible)
            }
            // Alert: interrupts, so use it only for something people must know now. The
            // title says what happened; buttons are verbs, not a bare OK.
            .alert("Couldn't Sync Note", isPresented: $showsSyncError) {
                Button("Try Again") { showsSyncError = false }
                // The cancel role gives the standard Cancel behavior and keyboard handling.
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("The note is saved on this device. Check your connection, then try again.")
            }
            // Confirmation dialog (action sheet): choices that follow an action the person
            // started on purpose. The destructive role marks the risky choice; Cancel is
            // always present when data could be lost.
            .confirmationDialog(
                "Delete all notes?",
                isPresented: $isConfirmingDelete,
                titleVisibility: .visible
            ) {
                Button("Delete All Notes", role: .destructive) { notes.removeAll() }
                Button("Cancel", role: .cancel) { }
            } message: {
                Text("This can't be undone.")
            }
        }
    }
}

private struct ComposeSheet: View {
    let onSave: (String) -> Void

    @Environment(\.dismiss) private var dismiss
    @State private var title = ""

    var body: some View {
        // A sheet gets its own navigation stack so it has a title and a toolbar.
        NavigationStack {
            Form {
                TextField("Title", text: $title)
            }
            .navigationTitle("New Note")
            .toolbar {
                // Cancel on the leading edge and the confirming button on the trailing
                // edge in iOS and iPadOS; these placements also map correctly on Mac.
                // The confirming button is always paired with Cancel.
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        onSave(title)
                        dismiss()
                    }
                    // Inactive until the task can be completed.
                    .disabled(title.isEmpty)
                }
            }
        }
        // Once there is unsaved text, a swipe down must not silently discard it.
        .interactiveDismissDisabled(!title.isEmpty)
    }
}
