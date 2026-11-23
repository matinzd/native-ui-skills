// TabRoot.swift
//
// Purpose: a tab-based app root that uses the current Tab API (a search-role tab and the
// sidebar-adaptable style) where it exists, with a working fallback for earlier systems.
//
// Minimum OS: iOS 16, iPadOS 16, macOS 13, tvOS 16, visionOS 1 (NavigationStack).
//   - Tab, TabRole.search and TabView(selection:) with Tab content need iOS 18, macOS 15,
//     tvOS 18, watchOS 11, visionOS 2.
//   - The sidebarAdaptable style needs the same versions and is not available on watchOS.
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/tab-bars
//   https://developer.apple.com/design/human-interface-guidelines/sidebars
//   https://developer.apple.com/design/human-interface-guidelines/search-fields
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

enum AppTab: Hashable {
    case home, library, search
}

struct TabRoot: View {
    // Tabs switch between top-level sections only. They never trigger actions, and no tab
    // is hidden or disabled (HIG tab-bars).
    @State private var selection: AppTab = .home

    var body: some View {
        if #available(iOS 18, macOS 15, tvOS 18, watchOS 11, visionOS 2, *) {
            CurrentTabs(selection: $selection)
        } else {
            // Fallback for iOS 16-17 / macOS 13-14: same sections, same order, older API.
            FallbackTabs(selection: $selection)
        }
    }
}

@available(iOS 18, macOS 15, tvOS 18, watchOS 11, visionOS 2, *)
private struct CurrentTabs: View {
    @Binding var selection: AppTab

    var body: some View {
        TabView(selection: $selection) {
            // Title plus SF Symbol: short, concrete nouns that name the section.
            Tab("Home", systemImage: "house", value: AppTab.home) {
                SectionScreen(title: "Home")
            }
            Tab("Library", systemImage: "books.vertical", value: AppTab.library) {
                SectionScreen(title: "Library")
            }
            // The search role tells the system which tab owns search. In the OS 26 design
            // the system sets this tab apart at the trailing end of the tab bar.
            Tab("Search", systemImage: "magnifyingglass", value: AppTab.search, role: .search) {
                SearchScreen()
            }
        }
        // On iPad this is a top tab bar that people can turn into a sidebar; on iPhone it
        // stays a bottom tab bar; on Mac and Apple TV it is a sidebar. One declaration
        // gives each platform its own convention.
        #if !os(watchOS)
        .tabViewStyle(.sidebarAdaptable)
        #endif
    }
}

private struct FallbackTabs: View {
    @Binding var selection: AppTab

    var body: some View {
        // Fallback only: tabItem and tag-based selection are deprecated in the current
        // SDK but are the correct API before iOS 18 / macOS 15.
        TabView(selection: $selection) {
            SectionScreen(title: "Home")
                .tabItem { Label("Home", systemImage: "house") } // fallback API
                .tag(AppTab.home)
            SectionScreen(title: "Library")
                .tabItem { Label("Library", systemImage: "books.vertical") } // fallback API
                .tag(AppTab.library)
            SearchScreen()
                .tabItem { Label("Search", systemImage: "magnifyingglass") } // fallback API
                .tag(AppTab.search)
        }
    }
}

private struct SectionScreen: View {
    let title: String

    var body: some View {
        // Each tab owns its navigation stack, so switching tabs keeps each section's place.
        NavigationStack {
            List {
                Text("\(title) content")
            }
            .navigationTitle(title)
        }
    }
}

private struct SearchScreen: View {
    @State private var query = ""

    var body: some View {
        NavigationStack {
            List {
                if query.isEmpty {
                    Text("Recent searches appear here")
                        .foregroundStyle(.secondary)
                } else {
                    Text("Results for \(query)")
                }
            }
            .navigationTitle("Search")
            // The system search field: standard placement, Clear button, keyboard and
            // VoiceOver behavior. The prompt says what can be searched.
            .searchable(text: $query, prompt: "Titles, authors, and notes")
        }
    }
}
