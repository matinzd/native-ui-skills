// AccessibleList.swift
//
// Purpose: a searchable list whose rows reflow at accessibility text sizes, read as one
// VoiceOver element, show status with a symbol plus text, and whose swipe actions are
// also reachable from a visible menu. Includes empty and no-results states.
//
// Minimum OS: iOS 17, iPadOS 17, macOS 14, visionOS 1 (ContentUnavailableView).
//   - Not for tvOS or watchOS as written: swipeActions is unavailable on tvOS and Menu is
//     unavailable on watchOS.
//   - Without ContentUnavailableView the rest works from iOS 16 / macOS 13.
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/lists-and-tables
//   https://developer.apple.com/design/human-interface-guidelines/accessibility
//   https://developer.apple.com/design/human-interface-guidelines/typography
//   https://developer.apple.com/design/human-interface-guidelines/search-fields
//
// Checked against Apple documentation on 2026-11-23; not compiled.

import SwiftUI

enum ShipmentStatus {
    case delivered, inTransit, delayed

    var title: String {
        switch self {
        case .delivered: return "Delivered"
        case .inTransit: return "In Transit"
        case .delayed: return "Delayed"
        }
    }

    // A different shape per state, so status never depends on color alone.
    var symbolName: String {
        switch self {
        case .delivered: return "checkmark.circle"
        case .inTransit: return "shippingbox"
        case .delayed: return "exclamationmark.triangle"
        }
    }
}

struct Shipment: Identifiable, Hashable {
    let id: UUID
    var title: String
    var destination: String
    var status: ShipmentStatus
    var isFlagged = false
}

struct ShipmentRow: View {
    let shipment: Shipment
    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        // At accessibility sizes, stack the status under the text instead of squeezing
        // both onto one line. AnyLayout switches axis without rebuilding the subviews.
        let layout = dynamicTypeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading, spacing: 4))
            : AnyLayout(HStackLayout(alignment: .firstTextBaseline, spacing: 8))
        layout {
            // Text styles, no line limits, no fixed heights: text wraps and the row grows.
            VStack(alignment: .leading, spacing: 2) {
                Text(shipment.isFlagged ? "\(shipment.title), flagged" : shipment.title)
                    .font(.headline)
                Text(shipment.destination)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }
            if !dynamicTypeSize.isAccessibilitySize {
                Spacer(minLength: 8)
            }
            // Symbol plus words; the symbol scales with the text style.
            Label(shipment.status.title, systemImage: shipment.status.symbolName)
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        // One element per row: VoiceOver reads title, destination and status together.
        .accessibilityElement(children: .combine)
    }
}

struct AccessibleList: View {
    @State private var shipments: [Shipment] = []
    @State private var query = ""

    private var results: [Shipment] {
        guard !query.isEmpty else { return shipments }
        return shipments.filter { $0.title.localizedCaseInsensitiveContains(query) }
    }

    var body: some View {
        NavigationStack {
            List(results) { shipment in
                HStack {
                    ShipmentRow(shipment: shipment)
                    // The same commands as the swipe actions, in a visible control, for
                    // people who cannot or do not swipe (pointer, keyboard, Switch Control).
                    Menu {
                        rowActions(for: shipment)
                    } label: {
                        Label("Actions for \(shipment.title)", systemImage: "ellipsis.circle")
                            .labelStyle(.iconOnly) // icon shown, title kept for VoiceOver
                            .frame(minWidth: 44, minHeight: 44) // 44 pt hit region
                            .contentShape(Rectangle())
                    }
                    .buttonStyle(.borderless) // only the menu, not the row, takes the tap
                }
                // Swipe is a shortcut, never the only route. No full swipe for Delete.
                .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                    rowActions(for: shipment)
                }
            }
            .navigationTitle("Shipments")
            .searchable(text: $query, prompt: "Search shipments")
            .overlay {
                if shipments.isEmpty {
                    // Nothing yet: say why and what will appear.
                    ContentUnavailableView(
                        "No Shipments",
                        systemImage: "shippingbox",
                        description: Text("Shipments you track appear here.")
                    )
                } else if results.isEmpty {
                    // The standard no-results state, including the search term.
                    ContentUnavailableView.search(text: query)
                }
            }
        }
    }

    @ViewBuilder
    private func rowActions(for shipment: Shipment) -> some View {
        Button {
            toggleFlag(shipment)
        } label: {
            Label(shipment.isFlagged ? "Unflag" : "Flag", systemImage: "flag")
        }
        // The destructive role gives the system styling; the title says what is removed.
        Button(role: .destructive) {
            shipments.removeAll { $0.id == shipment.id }
        } label: {
            Label("Delete Shipment", systemImage: "trash")
        }
    }

    private func toggleFlag(_ shipment: Shipment) {
        guard let index = shipments.firstIndex(where: { $0.id == shipment.id }) else { return }
        shipments[index].isFlagged.toggle()
    }
}
