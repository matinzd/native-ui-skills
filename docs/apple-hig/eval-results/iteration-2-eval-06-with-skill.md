## HIG review: `tests/evals/files/OrdersView.swift`
Target: iPhone, minimum iOS 17, SwiftUI. Evidence is the source only; nothing was built or run, and the skill's lint script was not run.

**Fix findings 1–4 before release.** They exclude VoiceOver, large-text and colour-blind users. Finding 5 is a quick win; 6 and 7 are cleanup that the fix for 1 and 2 mostly covers.

### 1. Menu control is an image with a tap gesture
- Class: Accessibility issue
- Severity: High
- Where: `OrdersView.swift:12`
- Why: VoiceOver gets no button trait and no meaningful name, so the menu is effectively unreachable. Separately, `showMenu` is toggled but nothing in this file reads it, so the tap does nothing visible here.
- Source: https://developer.apple.com/design/human-interface-guidelines/voiceover (recommendation); https://developer.apple.com/documentation/swiftui/button (API documentation)
- Fix: make it a `Button` with a `Label("Menu", systemImage: "line.3.horizontal")`, as in the sketch below.

### 2. Bar tap targets are too small
- Class: Accessibility issue
- Severity: High
- Where: `OrdersView.swift:12`, `OrdersView.swift:16-17`
- Why: the plus button is framed at 24×24 pt and the menu glyph has no frame at all. Apple's published iOS minimum is 28×28 pt and the default is 44×44 pt, so both are hard to hit, especially with motor impairments. The plus button also has no explicit label.
- Source: https://developer.apple.com/design/human-interface-guidelines/accessibility (recommendation)
- Fix: move both into the system toolbar, which sizes them for you; otherwise use `.frame(minWidth: 44, minHeight: 44)` and `.contentShape(Rectangle())`.

### 3. Paid/unpaid is shown by colour alone
- Class: Accessibility issue
- Severity: High
- Where: `OrdersView.swift:27-29`
- Why: a 10 pt red or green dot is the only payment signal. Red and green are the pair people most often cannot tell apart, and VoiceOver reads nothing for it.
- Source: https://developer.apple.com/design/human-interface-guidelines/accessibility (recommendation)
- Fix: use different shapes plus a label:
  ```swift
  Image(systemName: order.isPaid ? "checkmark.circle.fill" : "exclamationmark.circle.fill")
      .foregroundStyle(order.isPaid ? .green : .red)
      .accessibilityLabel(order.isPaid ? "Paid" : "Unpaid")
  ```

### 4. Fixed font sizes, one below the minimum
- Class: Accessibility issue
- Severity: High
- Where: `OrdersView.swift:14`, `OrdersView.swift:24`
- Why: `.system(size:)` does not scale with the person's text size. The customer name at 10 pt is also under Apple's 11 pt minimum for iOS.
- Source: https://developer.apple.com/design/human-interface-guidelines/typography (recommendation)
- Fix: use `.font(.caption)` for the customer name; the title goes away with finding 6, or use `.font(.title2.bold())`.

### 5. Alert on every appearance for routine information
- Class: Recommended improvement
- Severity: Medium
- Where: `OrdersView.swift:34-37`
- Why: "Orders synced." needs no decision, yet it blocks the screen each time the view appears. The HIG reserves alerts for important, actionable situations, and not at launch.
- Source: https://developer.apple.com/design/human-interface-guidelines/alerts (recommendation)
- Fix: delete the alert. If sync status matters, show it inline (for example a footer), and alert only on a failure the person must act on.

### 6. Hand-built navigation bar replaces the system one
- Class: Platform convention mismatch
- Severity: Medium
- Where: `OrdersView.swift:11-19`, `OrdersView.swift:33`
- Why: the custom `HStack` loses the system title behaviour, bar appearance, button sizing and accessibility that the real bar provides. The hamburger drawer is also not an iPhone convention (a tab bar is the expected top-level navigation), though the HIG does not prohibit it; that is your call.
- Source: https://developer.apple.com/design/human-interface-guidelines/toolbars (recommendation)
- Fix: this sketch resolves 1, 2 and 6 together (not compiled):
  ```swift
  NavigationStack {
      List(orders) { order in /* row */ }
          .navigationTitle("Orders")
          .navigationBarTitleDisplayMode(.inline)
          .toolbar {
              ToolbarItem(placement: .topBarLeading) {
                  Button { showMenu.toggle() } label: {
                      Label("Menu", systemImage: "line.3.horizontal")
                  }
              }
              ToolbarItem(placement: .topBarTrailing) {
                  Button { orders.append(.draft) } label: {
                      Label("New Order", systemImage: "plus")
                  }
              }
          }
  }
  ```

### 7. Deprecated APIs with replacements available on iOS 17
- Class: Confirmed guideline or API violation
- Severity: Low
- Where: `OrdersView.swift:9` (`NavigationView`), `OrdersView.swift:35-36` (`alert(isPresented:content:)` with `Alert`)
- Why: both still work today, so this is not a release blocker.
- Source: https://developer.apple.com/documentation/swiftui/navigationview (API documentation)
- Fix: use `NavigationStack` (iOS 16), and `alert(_:isPresented:actions:message:)` (iOS 15) if any alert survives finding 5. `navigationBarHidden` is also deprecated, but its replacement needs iOS 18, so it is not a finding for your target; it disappears with finding 6 anyway.

### Not verified
- What VoiceOver actually announces for the two symbols: needs a device test. Check: https://developer.apple.com/design/human-interface-guidelines/voiceover
- Row layout at the largest accessibility text sizes, and dot contrast in Dark Mode: needs a run. Check: https://developer.apple.com/design/human-interface-guidelines/accessibility

### What already works
- The content is a system `List`, so scrolling, separators and Dark Mode backgrounds come for free.
- It uses SF Symbols throughout, and the add action is already a real `Button`.
- Row order title uses the default body style, which scales with text size.

After the fixes, build it and test this screen with VoiceOver, the largest text size, Dark Mode and Increase Contrast.