// AdaptiveNavigation.swift
//
// Purpose: one navigation structure that is a sidebar plus detail at regular widths and a
// push/pop stack at compact widths, with selection-driven detail and an empty detail state.
//
// Minimum OS: iOS 16, iPadOS 16, macOS 13, visionOS 1.
//   - ContentUnavailableView needs iOS 17 / macOS 14, so it is gated with a real fallback.
//   - List selection is not available on watchOS; use a NavigationStack there.
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/split-views
//   https://developer.apple.com/design/human-interface-guidelines/sidebars
//   https://developer.apple.com/design/human-interface-guidelines/layout
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

struct Folder: Identifiable, Hashable {
    let id: UUID
    var name: String
    var notes: [String]
}

struct AdaptiveNavigationView: View {
    let folders: [Folder]

    // Selection is an ID, not an index, so it survives sorting and filtering.
    @State private var selectedFolderID: Folder.ID?

    private var selectedFolder: Folder? {
        folders.first { $0.id == selectedFolderID }
    }

    var body: some View {
        // NavigationSplitView collapses its columns into a single stack at narrow sizes
        // (iPhone, a narrow iPad window), so no size-class or device check is needed.
        // HIG split-views: prefer a split view in a regular environment and make sure
        // navigation still works at narrow widths.
        NavigationSplitView {
            // A List with a selection binding drives the detail column. When the split
            // view is collapsed, selecting a row pushes the detail.
            List(folders, selection: $selectedFolderID) { folder in
                // Label keeps a text title next to the symbol: readable by VoiceOver and
                // scaled with Dynamic Type.
                Label(folder.name, systemImage: "folder")
            }
            .navigationTitle("Folders")
            // Let the system choose the column width inside a sensible range instead of
            // hard-coding one size for every window.
            .navigationSplitViewColumnWidth(min: 200, ideal: 260, max: 360)
        } detail: {
            if let folder = selectedFolder {
                FolderDetail(folder: folder)
            } else {
                // At regular width the detail column is visible before anything is
                // selected. Explain what to do instead of leaving it blank.
                EmptyDetail()
            }
        }
    }
}

private struct FolderDetail: View {
    let folder: Folder

    var body: some View {
        List(folder.notes, id: \.self) { note in
            Text(note)
        }
        // Every screen gets its own title; it is also what VoiceOver announces first.
        .navigationTitle(folder.name)
        .overlay {
            if folder.notes.isEmpty {
                Text("No notes in this folder")
                    .foregroundStyle(.secondary)
            }
        }
    }
}

private struct EmptyDetail: View {
    var body: some View {
        if #available(iOS 17, macOS 14, tvOS 17, watchOS 10, *) {
            // The system empty-state view: standard layout, text styles and colors.
            ContentUnavailableView(
                "No Folder Selected",
                systemImage: "folder",
                description: Text("Choose a folder from the list to see its notes.")
            )
        } else {
            // Fallback for iOS 16 / macOS 13: same content from plain system pieces.
            VStack(spacing: 8) {
                Image(systemName: "folder")
                    .font(.largeTitle)
                    .foregroundStyle(.secondary)
                    .accessibilityHidden(true) // decorative; the text carries the meaning
                Text("No Folder Selected")
                    .font(.headline)
                Text("Choose a folder from the list to see its notes.")
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding()
        }
    }
}
