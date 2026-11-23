// AccessibleCustomControl.swift
//
// Purpose: a custom star-rating control that behaves like a system control for assistive
// technologies: one adjustable element with a label and a value, hit regions at the
// platform default size, state shown by shape and text, and motion that respects
// Reduce Motion.
//
// Minimum OS: iOS 15, iPadOS 15, macOS 12, tvOS 15, watchOS 8, visionOS 1
//   (foregroundStyle and monospacedDigit set the floor).
//
// HIG pages applied:
//   https://developer.apple.com/design/human-interface-guidelines/accessibility
//   https://developer.apple.com/design/human-interface-guidelines/voiceover
//   https://developer.apple.com/design/human-interface-guidelines/buttons
//   https://developer.apple.com/design/human-interface-guidelines/motion
//
// Checked against Apple documentation on 2026-11-23; not compiled.
//
// Prefer a system control (Stepper, Slider, Picker) when one fits. Build a custom control
// only when the product needs it, and then supply everything below.

import SwiftUI

struct RatingControl: View {
    let label: String
    @Binding var rating: Int
    var maximum = 5

    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    // HIG accessibility table, default control sizes: 44 pt on iOS, iPadOS and watchOS,
    // 60 pt on visionOS, 66 pt on tvOS, 28 pt on macOS.
    private var hitSize: CGFloat {
        #if os(visionOS)
        return 60
        #elseif os(tvOS)
        return 66
        #elseif os(macOS)
        return 28
        #else
        return 44
        #endif
    }

    var body: some View {
        HStack(spacing: 8) {
            HStack(spacing: 0) {
                ForEach(1...maximum, id: \.self) { value in
                    // Real buttons: pressed state, pointer hover and focus come for free.
                    Button {
                        // Tapping the current rating again clears it.
                        rating = (value == rating) ? 0 : value
                    } label: {
                        // Filled versus outlined star: the state is a shape difference,
                        // not a color difference.
                        Image(systemName: value <= rating ? "star.fill" : "star")
                            .font(.title2) // a text style, so the symbol scales with text
                            .scaleEffect(value == rating && !reduceMotion ? 1.15 : 1)
                            // The visible star is smaller than its hit region.
                            .frame(minWidth: hitSize, minHeight: hitSize)
                            .contentShape(Rectangle())
                    }
                    .buttonStyle(.plain)
                }
            }
            // The value is also shown as text, so it never depends on reading the stars.
            Text("\(rating) of \(maximum)")
                .font(.subheadline)
                .monospacedDigit()
                .foregroundStyle(.secondary)
        }
        // With Reduce Motion on, the stars still change, without the scale animation.
        .animation(reduceMotion ? nil : .easeOut(duration: 0.15), value: rating)
        // Present the whole control as one element instead of five unlabeled buttons.
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(label)
        .accessibilityValue("\(rating) of \(maximum)")
        // Adjustable: VoiceOver users swipe up or down to change the value.
        .accessibilityAdjustableAction { direction in
            switch direction {
            case .increment:
                rating = min(rating + 1, maximum)
            case .decrement:
                rating = max(rating - 1, 0)
            @unknown default:
                break
            }
        }
    }
}

// Alternative when a system control describes the same value: keep the custom drawing and
// hand assistive technologies a standard control with accessibilityRepresentation
// (iOS 15, macOS 12), for example a Stepper bound to the same rating.

struct RatingExample: View {
    @State private var rating = 3

    var body: some View {
        Form {
            // A visible text label names the control for everyone; the control's
            // accessibility label repeats it so the stars are not announced without context.
            VStack(alignment: .leading, spacing: 4) {
                Text("Your Rating")
                    .font(.headline)
                    .accessibilityHidden(true) // already spoken as the control's label
                RatingControl(label: "Your Rating", rating: $rating)
            }
        }
    }
}
