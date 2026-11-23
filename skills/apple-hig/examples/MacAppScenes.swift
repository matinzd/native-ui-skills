// MacAppScenes.swift
//
// Purpose: app-level structure a Mac app is expected to have: a window group, menu bar
// commands with keyboard shortcuts that act on the focused window, and a Settings scene.
// The same file builds for iPadOS, where the commands feed the hardware-keyboard
// shortcuts and the iPad menu bar.
//
// Minimum OS: macOS 13, iOS 16, iPadOS 16, visionOS 1 (NavigationSplitView sets the floor;
//   commands, CommandMenu, keyboardShortcut and Settings exist from macOS 11 / iOS 14).
//   - Settings is macOS only, so it is compiled only there.
//   - Commands and keyboardShortcut are not available on tvOS or watchOS.
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/the-menu-bar
//   https://developer.apple.com/design/human-interface-guidelines/menus
//   https://developer.apple.com/design/human-interface-guidelines/keyboards
//   https://developer.apple.com/design/human-interface-guidelines/settings
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

struct Note: Identifiable, Hashable {
    let id: UUID
    var title: String
    var isPinned = false
}

// Publishes the focused window's selected note to the menu bar commands.
struct SelectedNoteKey: FocusedValueKey {
    typealias Value = Binding<Note>
}

extension FocusedValues {
    var selectedNote: Binding<Note>? {
        get { self[SelectedNoteKey.self] }
        set { self[SelectedNoteKey.self] = newValue }
    }
}

@main
struct NotesApp: App {
    var body: some Scene {
        // WindowGroup lets people open several windows on Mac, iPad and Apple Vision Pro.
        WindowGroup {
            NotesWindow()
        }
        .commands {
            // System-provided commands for showing and hiding the window's sidebar.
            SidebarCommands()
            NoteCommands()
        }

        // The Settings scene adds the Settings item to the app menu with the standard
        // Command-Comma shortcut. Do not add your own menu item or toolbar button for it.
        #if os(macOS)
        Settings {
            SettingsPane()
        }
        #endif
    }
}

struct NoteCommands: Commands {
    @FocusedValue(\.selectedNote) private var selectedNote

    var body: some Commands {
        // App-specific commands belong in the menu bar even when they are also available
        // in the window, so people can find them and learn their shortcuts.
        CommandMenu("Note") {
            Button(selectedNote?.wrappedValue.isPinned == true ? "Unpin Note" : "Pin Note") {
                selectedNote?.wrappedValue.isPinned.toggle()
            }
            // Custom shortcut: Command as the main modifier, Shift as the secondary one,
            // and a combination the HIG does not list as a standard shortcut.
            .keyboardShortcut("l", modifiers: [.command, .shift])
            // An unavailable menu bar item stays visible and dimmed, never removed.
            .disabled(selectedNote == nil)
        }
    }
}

#if os(macOS)
struct SettingsPane: View {
    @AppStorage("showsPinnedFirst") private var showsPinnedFirst = true

    var body: some View {
        Form {
            Toggle("Show Pinned Notes First", isOn: $showsPinnedFirst)
        }
        .scenePadding() // platform-appropriate margins instead of a magic number
        .frame(minWidth: 360)
    }
}
#endif

struct NotesWindow: View {
    @State private var notes = [
        Note(id: UUID(), title: "Groceries"),
        Note(id: UUID(), title: "Trip ideas")
    ]
    @State private var selectedID: Note.ID?

    private var selectedNote: Binding<Note>? {
        guard let index = notes.firstIndex(where: { $0.id == selectedID }) else { return nil }
        return $notes[index]
    }

    var body: some View {
        NavigationSplitView {
            List(notes, selection: $selectedID) { note in
                // Symbol plus title; the pin is a shape, not a color cue.
                Label(note.title, systemImage: note.isPinned ? "pin.fill" : "note.text")
            }
            .navigationTitle("Notes")
        } detail: {
            if let note = selectedNote {
                Text(note.wrappedValue.title)
                    .navigationTitle(note.wrappedValue.title)
            } else {
                Text("Select a note")
                    .foregroundStyle(.secondary)
            }
        }
        // Each window reports its own selection, so the command targets the frontmost
        // window and dims when nothing is selected. Passing an optional value needs
        // iOS 16 / macOS 13.
        .focusedSceneValue(\.selectedNote, selectedNote)
    }
}
