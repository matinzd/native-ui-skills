# Example: a complete HIG review

An illustration of the review format from `SKILL.md`, applied to one SwiftUI file. The code under review is
shown first so the findings can be followed. Sources were checked on 2026-11-23.

## Input

Request: "Review OrdersView.swift against the HIG. iPhone only, minimum iOS 17."

```swift
// Before: the code under review (deliberately flawed; do not copy)
struct OrdersView: View {
    @State private var orders: [Order] = Order.samples
    @State private var showMenu = false
    @State private var showInfo = false

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                HStack {
                    Image(systemName: "line.3.horizontal").onTapGesture { showMenu.toggle() }
                    Spacer()
                    Text("Orders").font(.system(size: 22, weight: .bold))
                    Spacer()
                    Button(action: { orders.append(.draft) }) { Image(systemName: "plus") }
                        .frame(width: 24, height: 24)
                }
                .padding(.horizontal, 12)
                List(orders) { order in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(order.title)
                            Text(order.customer).font(.system(size: 10))
                        }
                        Spacer()
                        Circle()
                            .fill(order.isPaid ? Color.green : Color.red)
                            .frame(width: 10, height: 10)
                    }
                }
            }
            .navigationBarHidden(true)
            .onAppear { showInfo = true }
            .alert(isPresented: $showInfo) {
                Alert(title: Text("Info"), message: Text("Orders synced."), dismissButton: .default(Text("OK")))
            }
        }
    }
}
```

## Output

## HIG review: OrdersView.swift
Target: iPhone, minimum iOS 17 (stated), SwiftUI. Evidence: source code only, so rendered sizes and contrast
were not measured.

### 1. Payment status is shown by color alone
- Class: Accessibility issue
- Severity: High
- Where: the `Circle` filled green or red in each row
- Why: People who cannot tell red from green, and anyone using VoiceOver, get no payment status at all. The
  dot has no label and no shape or text difference.
- Source: https://developer.apple.com/design/human-interface-guidelines/accessibility (recommendation)
- Fix: Replace the dot with a symbol plus text, for example
  `Label(order.isPaid ? "Paid" : "Unpaid", systemImage: order.isPaid ? "checkmark.circle" : "exclamationmark.circle")`,
  and keep color as a secondary cue.

### 2. Menu and add controls have no accessible name, and one is not a button
- Class: Accessibility issue
- Severity: High
- Where: the `Image` with `onTapGesture` and the icon-only `Button` in the hand-built header
- Why: The menu image has no button trait, so VoiceOver, Voice Control, Switch Control, and a hardware keyboard
  do not treat it as actionable. Neither control has a text label, so assistive technologies have only the
  symbol to go on.
- Source: https://developer.apple.com/design/human-interface-guidelines/voiceover (recommendation);
  https://developer.apple.com/documentation/swiftui/button (API documentation)
- Fix: Make both real buttons with labels and put them in the system toolbar (see finding 4):
  `Button("Add Order", systemImage: "plus") { orders.append(.draft) }`.

### 3. Fixed font sizes, one below the platform minimum
- Class: Accessibility issue
- Severity: High
- Where: `.font(.system(size: 22, weight: .bold))` and `.font(.system(size: 10))`
- Why: Fixed sizes ignore the person's text size setting. The customer name is 10 pt, below the 11 pt minimum
  the HIG gives for iPhone.
- Source: https://developer.apple.com/design/human-interface-guidelines/typography (recommendation)
- Fix: Use text styles: `.font(.caption)` with `.foregroundStyle(.secondary)` for the customer name; the title
  becomes the navigation title (finding 4).

### 4. Hand-built header replaces the system navigation bar
- Class: Platform convention mismatch
- Severity: Medium
- Where: the `HStack` header together with `.navigationBarHidden(true)`
- Why: The system bar provides the title, large-title behaviour, the back button, the current system
  appearance, and correct safe-area handling. The replica provides none of these and will look out of place.
- Source: https://developer.apple.com/design/human-interface-guidelines/toolbars (recommendation)
- Fix: Delete the header and the hidden-bar modifier. Add `.navigationTitle("Orders")` and a
  `.toolbar { ToolbarItem(placement: .primaryAction) { ... } }` holding the add button.

### 5. Add button's tappable area is 24x24 pt
- Class: Accessibility issue
- Severity: Medium
- Where: `.frame(width: 24, height: 24)` on the add button
- Why: The HIG's default control size on iPhone is 44x44 pt and its published minimum is 28x28 pt; this is
  below both, so it is hard to hit, especially for people with reduced dexterity.
- Source: https://developer.apple.com/design/human-interface-guidelines/accessibility (recommendation)
- Fix: Remove the fixed frame. A toolbar button gets a suitable hit region from the system.

### 6. Alert used for routine information, shown on appearance
- Class: Recommended improvement
- Severity: Medium
- Where: `.onAppear { showInfo = true }` and the `"Info"` alert
- Why: An alert interrupts. The HIG reserves alerts for important situations that need a decision, and advises
  against using them merely to give information. "Orders synced" needs no action.
- Source: https://developer.apple.com/design/human-interface-guidelines/alerts (recommendation)
- Fix: Remove the alert. If sync status matters, show it inline, for example as a footer or a brief status in
  the list.

### 7. Top-level menu behind a "hamburger" icon
- Class: Platform convention mismatch
- Severity: Medium
- Where: the `line.3.horizontal` control
- Why: On iPhone, people expect top-level sections in a tab bar, where they stay visible. A hidden drawer makes
  sections harder to discover. The HIG does not mention this pattern by name; this finding rests on its
  guidance to use a tab bar for navigating between sections.
- Source: https://developer.apple.com/design/human-interface-guidelines/tab-bars (recommendation)
- Fix: If the menu holds top-level sections, move them to a `TabView`. If it holds occasional actions, use a
  `Menu` in the toolbar.

### 8. Deprecated APIs
- Class: Confirmed guideline or API violation
- Severity: Low
- Where: `NavigationView`, `navigationBarHidden`, `alert(isPresented:content:)` with `Alert`
- Why: All three are deprecated, and their replacements are available on the stated minimum of iOS 17.
- Source: https://developer.apple.com/documentation/swiftui/navigationview (API documentation)
- Fix: `NavigationStack` (iOS 16+). The other two disappear with findings 4 and 6.

### Not verified
- Contrast of the row text and status colors: needs the rendered screen. Check with Accessibility Inspector in
  light and dark appearances.
- Behaviour at the largest accessibility text sizes: test in the simulator after applying finding 3.
- Whether `showMenu` leads to sections or actions: the drawer's content was not provided (affects finding 7).

### What already works
- The order list uses the system `List`, so rows get standard spacing, separators, and scrolling behaviour.
- Row content is in a leading-aligned stack, which mirrors correctly for right-to-left languages.
