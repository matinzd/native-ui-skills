# 06 - Evaluation strategy and eval assets for `apple-hig`

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Agent 6 (QA/evaluation). Fetched 2026-11-23. Tags: **[V]** fetched this session and the source says this; **[M]** memory/secondary, unverified.
URL shorthand: `H:<slug>` = `https://developer.apple.com/design/human-interface-guidelines/<slug>` (read via
`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`); `A:<path>` =
`https://developer.apple.com/documentation/<path>` (read via `.../tutorials/data/documentation/<path>.json`).
Requirement levels: **HARD** = API contract / compile-time fact; **REC** = HIG recommendation; **CONV** = community convention.

## 0. Sources and how evals are done in practice

| Fact | Source | Tag |
|---|---|---|
| `evals/evals.json` = `{skill_name, evals:[{id, prompt, expected_output, files?, assertions?}]}`; start with prompts + expected output, add assertions after first run | https://raw.githubusercontent.com/agentskills/agentskills/main/docs/skill-creation/evaluating-skills.mdx | [V] |
| skill-creator's `references/schemas.md` names the same list **`expectations`** (not `assertions`); `id` is a unique integer; `files` relative to skill root. Its SKILL.md and `eval_metadata.json` say `assertions`. The two names coexist upstream | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/references/schemas.md , .../skill-creator/SKILL.md | [V] |
| `grading.json` items must use `text`, `passed`, `evidence` (agentskills wraps them in `assertion_results`, skill-creator in `expectations`) + `summary{passed,failed,total,pass_rate}` | both of the above | [V] |
| Each eval is run twice in clean context: `with_skill/` and `without_skill/` (or `old_skill/` from a snapshot when improving); workspace `<skill>-workspace/iteration-N/eval-<name>/{with_skill,without_skill}/{outputs/,timing.json,grading.json}` + `benchmark.json` with mean/stddev/delta of pass_rate, time, tokens | evaluating-skills.mdx; skill-creator SKILL.md | [V] |
| `timing.json` = `{total_tokens, duration_ms}` captured from the subagent completion notification | evaluating-skills.mdx | [V] |
| Drop assertions that pass in both configs; investigate those failing in both; high stddev = ambiguous instructions; blind A/B comparison as a complement | evaluating-skills.mdx | [V] |
| Trigger evals: JSON array of `{query, should_trigger}`; ~20 queries (8-10 each way); near-miss negatives; run each 3x; pass if trigger rate >0.5 (positives) / <0.5 (negatives); 60/40 train/validation split, pick description by validation score; max ~5 iterations | https://raw.githubusercontent.com/agentskills/agentskills/main/docs/skill-creation/optimizing-descriptions.mdx; skill-creator SKILL.md ("60% train / 40% held-out test", 3 runs, up to 5 iterations) | [V] |
| Trigger detection in Claude Code: `claude -p <query> --output-format stream-json`, triggered if a `Skill` tool call names the skill or a `Read` targets its file | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/run_eval.py | [V] |
| Agents only consult skills for tasks they cannot trivially do alone, so trigger queries must be substantive | optimizing-descriptions.mdx; skill-creator SKILL.md | [V] |
| Spec: `name` 1-64 chars `[a-z0-9-]`, no leading/trailing/consecutive hyphens, must equal parent directory; `description` 1-1024 chars; `compatibility` <=500; `metadata` string->string map; `allowed-tools` experimental | https://raw.githubusercontent.com/agentskills/agentskills/main/docs/specification.mdx | [V] |
| Budgets: metadata ~100 tokens; SKILL.md body <5000 tokens recommended and <500 lines; references one level deep from SKILL.md, "smaller files mean less use of context" | specification.mdx; best-practices.mdx | [V] |
| skill-creator `quick_validate.py` additionally rejects unknown frontmatter keys (allowed: name, description, license, allowed-tools, metadata, compatibility) and `<`/`>` in description | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/scripts/quick_validate.py | [V] |
| `skills-ref validate <dir>` exists but README says demo-only, not for production | https://raw.githubusercontent.com/agentskills/agentskills/main/skills-ref/README.md | [V] |
| Claude Code: skills in `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/`; listing truncates `description`+`when_to_use` at 1,536 chars, so lead with the key use case | https://code.claude.com/docs/en/skills.md | [V] |
| Cross-client convention `.agents/skills/` (project and `~`), some clients also scan `.claude/skills/` | https://raw.githubusercontent.com/agentskills/agentskills/main/docs/client-implementation/adding-skills-support.mdx | [V] |
| Codex and Cursor exact skill directories, activation UI and log locations | cursor.com / developers.openai.com blocked | [M] |

**Decision:** author `evals/evals.json` with the agentskills key `assertions`; the validator accepts `expectations` as an alias
and can emit a skill-creator copy. Extra keys below (`name`, `category`, `references_expected`, `max_reference_files`) are
additive extensions; neither upstream schema forbids extra keys, but neither documents them [V absence].

### Apple facts every assertion below depends on (all [V] on 2026-11-23)

| # | Fact | Level | Source |
|---|---|---|---|
| F1 | Buttons: "a hit region of at least 44x44 pt - in visionOS, 60x60 pt", phrased "as a general rule" | REC | H:buttons |
| F2 | Control size table (default / minimum): iOS+iPadOS 44x44 / 28x28; macOS 28x28 / 20x20; tvOS 66x66 / 56x56; visionOS 60x60 / 28x28; watchOS 44x44 / 28x28. Spacing: ~12 pt around bezeled, ~24 pt around unbezeled elements | REC | H:accessibility |
| F3 | Text size (default / minimum): iOS+iPadOS 17 / 11; macOS 13 / 10; tvOS 29 / 23; visionOS 17 / 12; watchOS 16 / 12 pt | REC | H:typography |
| F4 | Built-in text styles give Dynamic Type support; custom fonts must implement the same; macOS does not support Dynamic Type; enlarge text "at least 200 percent (or 140 percent in watchOS apps)" | REC | H:typography, H:accessibility |
| F5 | "Convey information with more than color alone" / "Avoid relying solely on color" | REC | H:accessibility, H:color |
| F6 | Contrast guidance (WCAG AA values used by Accessibility Inspector): up to 17 pt 4.5:1; 18 pt 3:1; bold 3:1. Wording is "strive to meet" | REC | H:accessibility |
| F7 | Tab bars: for navigation, not actions; include tab labels; "avoid overflow tabs" (More tab); do not hide/disable tabs; **no numeric maximum for iPhone** - "five or fewer" appears only for the default list of a customisable iPadOS tab bar; "Not supported in watchOS"; tvOS bar height 68 pt, "you can't change"; visionOS bar vertical on the leading side | REC (tvOS height = HARD) | H:tab-bars |
| F8 | Alerts: "avoid using an alert merely to provide information"; avoid uninformative titles like "Error"; up to three buttons; "OK" only for purely informational alerts; use an action sheet, not an alert, for choices tied to an intentional action | REC | H:alerts, H:action-sheets |
| F9 | Layout: decide by size classes, "not device type or orientation"; tvOS safe area 60 pt top/bottom, 80 pt sides | REC | H:layout |
| F10 | Sidebars/iPad: prefer tab bar first; `sidebarAdaptable` gives tab bar that converts to sidebar; `NavigationSplitView` for sidebar-only; split view preferred in regular, not compact, width | REC | H:sidebars, H:tab-bars, H:split-views |
| F11 | Dark Mode: "Avoid offering an app-specific appearance setting"; look good in both appearances; use dynamic system colours | REC | H:dark-mode, H:color |
| F12 | Toolbars: "Reduce the use of toolbar backgrounds and tinted controls"; system adds overflow menu, do not add one manually | REC | H:toolbars |
| F13 | Mac Catalyst: default iPad idiom scales views/text to 77%; Mac idiom renders at 100% and needs layout audit; "use text styles and avoid fixed font sizes"; automatic menu bar, pointer, keyboard, window support | REC | H:mac-catalyst |
| F14 | macOS: use the menu bar for all commands, keyboard shortcuts, resizable windows; app-level Settings item in the app menu | REC | H:designing-for-macos, H:the-menu-bar |
| F15 | watchOS: glanceable, minimise hierarchy depth, Digital Crown is primary navigation input since watchOS 10 | REC | H:designing-for-watchos, H:digital-crown |
| F16 | visionOS: windows for UI-centric tasks; rounded shapes; margin of at least 16 pt around interactive items or centres at least 60 pt apart; 60x60 pt targets | REC | H:designing-for-visionos, H:eyes, H:buttons |
| F17 | tvOS: embrace the focus system; rely on system focus effects | REC | H:designing-for-tvos, H:focus-and-selection |
| F18 | VoiceOver: label all key elements; hide decorative images. `accessibilityLabel(_:)` is for views that display no text "like an icon" (iOS 14+) | REC | H:voiceover, A:swiftui/view/accessibilitylabel(_:)-1d7jv |
| F19 | `onTapGesture`: "If you create a control that's functionally equivalent to a Button, use ButtonStyle to create a customized button instead" | REC (API doc) | A:swiftui/view/ontapgesture(count:perform:) |
| F20 | Reduce Motion: reduce automatic/repetitive animation when the setting is on; `accessibilityReduceMotion` env value iOS 13+ | REC | H:accessibility, H:motion, A:swiftui/environmentvalues/accessibilityreducemotion |
| F21 | Liquid Glass: not in the content layer; use sparingly on custom controls; standard components adopt it automatically | REC | H:materials |
| F22 | The string "hamburger" appears in none of the 35 HIG pages fetched; `navigation-bars.json` returns 404 (guidance now lives under H:toolbars) | absence | fetched set |

API availability from `metadata.platforms` (HARD):

| Symbol | Introduced | Note |
|---|---|---|
| `NavigationStack`, `NavigationSplitView`, `LabeledContent`, `presentationDetents`, `toolbarBackground(_:for:)` | iOS 16 / macOS 13 / watchOS 9 | |
| `ContentUnavailableView`, `@Observable` (Observation), `sensoryFeedback`, `symbolEffect`, `containerRelativeFrame`, `inspector`, `onChange(of:initial:_:)` | iOS 17 / macOS 14 | `sensoryFeedback` visionOS 26; `inspector` iOS/macOS only |
| `Tab`, `TabSection`, `TabViewStyle.sidebarAdaptable`, `tabViewSidebarHeader` | iOS 18 / macOS 15 / visionOS 2 | `sidebarAdaptable`: no watchOS |
| `glassEffect(_:in:)`, `GlassEffectContainer`, `PrimitiveButtonStyle.glass`, `tabBarMinimizeBehavior`, `tabViewBottomAccessory`, `ToolbarSpacer`, `scrollEdgeEffectStyle` | iOS 26 / macOS 26 | `glassEffect`, `GlassEffectContainer`, `.glass`: **no visionOS listed**; `tabViewBottomAccessory` iOS/iPadOS/Catalyst only |
| `glassBackgroundEffect(displayMode:)`, `ornament(...)` | visionOS 1 only | |
| `TabViewStyle.verticalPage`, `digitalCrownRotation` | watchOS 10 / watchOS 6 only | |
| `Settings`, `MenuBarExtra` | macOS 11 / macOS 13 only | `Commands`: no tvOS/watchOS |
| `NavigationView`, `foregroundColor(_:)`, `cornerRadius(_:antialiased:)`, `tabItem(_:)`, `Alert`, `ActionSheet`, `alert(isPresented:content:)`, `navigationBarHidden(_:)` | iOS 13 | deprecated, `deprecatedAt` = **"27.3"** (see below) |
| `onChange(of:perform:)`, `NavigationLink(destination:isActive:label:)` | iOS 14 / 13 | deprecated at fixed versions 17.0 / 16.0 |
| `liquidGlassStyle`, `hapticFeedback`, `navigationBarGlass`, `minimumTapTarget`, `tapTargetSize`, `roundedCorners`, `adaptiveTabBar` under `swiftui/view/` | - | all 404: used as hallucination traps |

**Contradiction with common lore:** `NavigationView` and friends report `deprecatedAt: "27.3"`, i.e. the current SDK, not
"iOS 16". This is the rolling value Apple's docs show for soft deprecations [M: `API_TO_BE_DEPRECATED`, likely no compiler
warning]. Evals therefore assert "deprecated, replacement is X (available from iOS N)" and never "deprecated in iOS N" for these.
Second contradiction: "max 5 tabs" is not in the current H:tab-bars text (F7).

## 1. Trigger eval set (`evals/trigger-queries.json`)

40 queries (double the upstream ~20 because the near-miss surface is large). Split roughly 60/40 (26 train / 14 validation, balanced labels), fixed, stored
in the file via `"split"`. Run 3x each; report recall on positives, false-trigger rate on negatives, per-query trigger rate.
`note` is for humans; strip it for skill-creator's `run_loop.py`, which only documents `query` + `should_trigger` [V].

```json
[
{"query":"make this SwiftUI settings screen feel native - right now it's a ScrollView with custom toggle rows I drew myself and my designer says it looks like a web page","should_trigger":true,"split":"train","note":"no 'HIG'; native-feel"},
{"query":"why does my iPad app look like a stretched phone app? it's a single NavigationStack with a list, runs on iPad Pro 13 and there's just a huge empty right side","should_trigger":true,"split":"train","note":"iPhone to iPad adaptation"},
{"query":"can you do a HIG review of Sources/Checkout/CheckoutView.swift before we ship 2.0 on friday","should_trigger":true,"split":"train","note":"explicit"},
{"query":"we're porting our iOS recipe app to Apple Watch. what should the navigation look like? on the phone it has 5 tabs","should_trigger":true,"split":"validation","note":"iOS to watchOS"},
{"query":"audit ProfileHeader.swift for VoiceOver and Dynamic Type problems, my QA says text gets cut off at the largest size","should_trigger":true,"split":"train","note":"accessibility"},
{"query":"should this be a sheet, a popover or a full screen cover? it's a filter panel with 6 options on iphone and ipad","should_trigger":true,"split":"train","note":"component choice"},
{"query":"design the tab structure for a banking app on iPhone - accounts, cards, payments, insights, support, settings, profile. is 7 tabs ok","should_trigger":true,"split":"validation","note":"design, no code"},
{"query":"I need to add Liquid Glass to our custom floating toolbar but we still support iOS 17. how do I do that safely in SwiftUI","should_trigger":true,"split":"train","note":"deployment target"},
{"query":"our mac app is a Catalyst build of the iPad app and reviewers say it doesn't feel like a mac app. what do we fix first","should_trigger":true,"split":"train","note":"Catalyst"},
{"query":"refactor this UIKit view controller so the buttons and text respect the user's text size setting, change as little as possible","should_trigger":true,"split":"validation","note":"UIKit refactor"},
{"query":"is it ok to put a hamburger menu in an iphone app? product wants one because the android app has it","should_trigger":true,"split":"train","note":"platform convention"},
{"query":"building a visionOS version of our SwiftUI dashboard - what changes for buttons, spacing and the tab bar","should_trigger":true,"split":"train","note":"visionOS"},
{"query":"write a SwiftUI onboarding flow for iOS 18, three pages then a notification permission ask. want it to look like something apple would ship","should_trigger":true,"split":"validation","note":"implement"},
{"query":"my delete confirmation is an alert with OK / Cancel and design says it's wrong but can't tell me why. here's the code","should_trigger":true,"split":"train","note":"alerts"},
{"query":"tvOS: focus keeps jumping to the wrong card in my shelf and the cards near the edge are cut off on some TVs. layout advice?","should_trigger":true,"split":"train","note":"tvOS focus and safe area"},
{"query":"what's the minimum tap target size on iOS and does it differ on mac","should_trigger":true,"split":"validation","note":"quick factual"},
{"query":"we have one SwiftUI codebase for iPhone, iPad and Mac. propose the navigation architecture so each platform gets what users expect","should_trigger":true,"split":"train","note":"multi-platform"},
{"query":"pick colors for success/warning/error badges in my SwiftUI app that work in dark mode and for color blind users","should_trigger":true,"split":"validation","note":"colour and accessibility"},
{"query":"review this AppKit preferences window - toolbar, tabs, button order. does it follow mac conventions","should_trigger":true,"split":"train","note":"AppKit/macOS"},
{"query":"which SF Symbol and label should I use for these toolbar actions: share, duplicate, archive, mark unread - and where do they go on iPad vs iPhone","should_trigger":true,"split":"validation","note":"symbols and toolbars"},

{"query":"convert this Jetpack Compose screen to Material 3, the bottom navigation has 6 items and the FAB overlaps it","should_trigger":false,"split":"train","note":"Android/Material"},
{"query":"my CSS grid breaks on iPhone Safari - the sticky header jumps when the address bar collapses. how do I fix it","should_trigger":false,"split":"train","note":"web CSS on iOS Safari"},
{"query":"Flutter: build a responsive master-detail layout with a NavigationRail on tablets and a BottomNavigationBar on phones","should_trigger":false,"split":"validation","note":"Flutter generic layout"},
{"query":"in React Native my FlatList rerenders every row when I toggle one switch, how do I memoize the rows","should_trigger":false,"split":"train","note":"RN performance"},
{"query":"getting 'Sending main actor-isolated value of type ViewModel risks causing data races' after moving to Swift 6, here's the view model","should_trigger":false,"split":"train","note":"Swift concurrency"},
{"query":"write the App Store Connect description, keywords and what's new text for version 3.2 of our meditation app","should_trigger":false,"split":"validation","note":"ASC metadata"},
{"query":"set up a Vapor 4 server with Fluent and Postgres and a /users CRUD route","should_trigger":false,"split":"train","note":"server-side Swift"},
{"query":"review my code: Sources/Networking/APIClient.swift - retry logic and error mapping, is the async/await usage right","should_trigger":false,"split":"train","note":"non-UI Swift review"},
{"query":"in Figma, set up auto layout and breakpoints for our marketing website hero section (desktop / tablet / mobile web)","should_trigger":false,"split":"validation","note":"Figma for web"},
{"query":"my SwiftData @Query crashes with a fatal error when I add a new property to the model, how do I write the migration plan","should_trigger":false,"split":"train","note":"persistence"},
{"query":"xcodebuild archive fails on CI with 'No profiles for com.acme.app were found' - fastlane match setup","should_trigger":false,"split":"train","note":"signing/CI"},
{"query":"write XCTest unit tests for PriceFormatter.swift covering locale and rounding edge cases","should_trigger":false,"split":"validation","note":"unit tests"},
{"query":"implement Sign in with Apple token validation on our Node backend, we get invalid_client from the token endpoint","should_trigger":false,"split":"train","note":"backend auth"},
{"query":"design a Windows 11 settings page in WinUI 3 following Fluent design","should_trigger":false,"split":"train","note":"other platform guideline"},
{"query":"my SwiftUI List scrolls at 40fps with 5000 rows, Instruments shows lots of time in body - how do I profile and fix it","should_trigger":false,"split":"validation","note":"SwiftUI performance, not design"},
{"query":"generate an app icon image of a blue fox for my iOS game, 1024x1024 png","should_trigger":false,"split":"train","note":"image generation; borderline"},
{"query":"add a Tailwind dark mode toggle to our Next.js dashboard and persist it in localStorage","should_trigger":false,"split":"train","note":"web dark mode"},
{"query":"Kotlin Multiplatform: share the view models between Android and iOS, how do I expose StateFlow to Swift","should_trigger":false,"split":"validation","note":"KMP architecture"},
{"query":"our push notifications arrive on TestFlight builds but not production - APNs environment and entitlements checklist please","should_trigger":false,"split":"train","note":"APNs config"},
{"query":"make an accessible data table for our React admin panel - aria roles, keyboard nav, screen reader announcements","should_trigger":false,"split":"validation","note":"web accessibility"}
]
```

Labelling notes: (a) "generate an app icon" and "SwiftUI List performance" are deliberately borderline; if the lead decides
the skill covers app-icon specs, flip the former. (b) A Flutter/RN prompt that asks to *match iOS conventions* should trigger;
keep one such positive in the fresh post-optimisation set (e.g. "my React Native app's iOS build has an Android-style
drawer; what do iOS users expect instead"). (c) After optimisation, write 5-10 fresh queries for an honest check [V upstream].
Targets: positive recall >= 0.90 (>=18/20), false-trigger <= 0.10 (<=2/20), validation pass rate >= 0.85.

## 2. Task evals (`evals/evals.json`) and fixtures

Reference keys (the lead maps them to real paths): `foundations/{layout,typography,color,materials,motion}`,
`components/{navigation,tab-bars,buttons,alerts-sheets,toolbars,lists-forms}`, `patterns/{modality,settings,onboarding}`,
`platforms/{ios,ipados,macos,watchos,tvos,visionos,catalyst}`, `accessibility/{core,voiceover,dynamic-type}`,
`implementation/{swiftui-availability,deprecations,adaptive-layout,uikit}`, `review/output-format` (in SKILL.md).

### Fixtures (`evals/files/`)

`OrdersView.swift` (review; target iOS 17). Planted: P1 `NavigationView` (deprecated, F-API); P2 hamburger `Image` +
`onTapGesture` (F19, F22); P3 hard-coded 22 pt title (F4); P4 10 pt text, below the 11 pt iOS minimum (F3); P5 icon-only
button, no explicit label (F18); P6 24x24 frame, below 44 default and 28 minimum (F1, F2); P7 red/green dot as the only
paid/unpaid signal (F5); P8 informational alert titled "Info" (F8) using deprecated `Alert`/`alert(isPresented:content:)`;
P9 `navigationBarHidden` + hand-built bar (deprecated API; replaces system toolbar, F12).

```swift
import SwiftUI

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

`RootTabs.swift` (review; iPhone, target iOS 18). Planted: custom bar instead of `TabView`; 7 icon-only tabs with no text
labels (F7); colour-only selection (F5); `onTapGesture` pseudo-buttons (F19); 40 pt bar (F1); `Color.white` background that
ignores Dark Mode (F11); deprecated `foregroundColor` (F-API).

```swift
import SwiftUI

struct RootTabs: View {
    @State private var selected = 0
    private let icons = ["house", "magnifyingglass", "heart", "cart", "bell", "person", "gearshape"]

    var body: some View {
        VStack(spacing: 0) {
            ScreenFactory.screen(at: selected)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            HStack(spacing: 0) {
                ForEach(icons.indices, id: \.self) { i in
                    Image(systemName: icons[i])
                        .font(.system(size: 18))
                        .foregroundColor(selected == i ? .blue : .gray)
                        .frame(maxWidth: .infinity)
                        .onTapGesture { selected = i }
                }
            }
            .frame(height: 40)
            .background(Color.white)
        }
    }
}
```

`ProfileHeader.swift` (minimal-diff refactor; target iOS 16). Only lines 9, 11 and 13 need to change.

```swift
import SwiftUI

struct ProfileHeader: View {
    let user: User
    var onEdit: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(user.name).font(.system(size: 24, weight: .semibold))
            Text(user.handle)
                .font(.system(size: 14))
                .foregroundColor(.secondary)
            Text(user.bio).font(.system(size: 14)).lineLimit(2)
            Button("Edit Profile", action: onEdit)
                .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

`PlayerControls.swift` (accessibility audit; target iOS 17). Planted: icon `Image`s with gestures and no label/trait (F18,
F19); decorative artwork not hidden (F18); endless animation ignoring Reduce Motion (F20); `Color(white: 0.8)` text on white
(F6; computed contrast is about 1.6:1 [M arithmetic]); `.dynamicTypeSize(.medium)` pins text size (F4); 20 pt targets (F2).

```swift
import SwiftUI

struct PlayerControls: View {
    @State private var isPlaying = false
    @State private var pulse = false
    let track: Track

    var body: some View {
        VStack(spacing: 8) {
            Image("album-sparkle-overlay")
            Text(track.title).font(.headline)
            Text(track.artist)
                .font(.caption)
                .foregroundStyle(Color(white: 0.8))
            HStack(spacing: 4) {
                Image(systemName: "backward.fill").frame(width: 20, height: 20)
                    .onTapGesture { Player.shared.previous() }
                Image(systemName: isPlaying ? "pause.fill" : "play.fill").frame(width: 20, height: 20)
                    .scaleEffect(pulse ? 1.3 : 1.0)
                    .onTapGesture { isPlaying.toggle() }
                Image(systemName: "forward.fill").frame(width: 20, height: 20)
                    .onTapGesture { Player.shared.next() }
            }
        }
        .background(Color.white)
        .dynamicTypeSize(.medium)
        .onAppear {
            withAnimation(.easeInOut(duration: 0.4).repeatForever()) { pulse = true }
        }
    }
}
```

`LibraryView.swift` (iPhone to iPad; target iOS 18). Planted: `UIDevice` idiom check for layout (F9); single stack on iPad (F10).

```swift
import SwiftUI

struct LibraryView: View {
    @State private var books: [Book] = Book.samples
    private var isPad: Bool { UIDevice.current.userInterfaceIdiom == .pad }

    var body: some View {
        NavigationStack {
            List(books) { book in
                NavigationLink(book.title) { BookDetail(book: book) }
                    .font(.system(size: isPad ? 22 : 16))
            }
            .padding(.horizontal, isPad ? 200 : 0)
            .navigationTitle("Library")
        }
    }
}
```

### `evals/evals.json`

```json
{
  "skill_name": "apple-hig",
  "evals": [
    {"id": 1, "name": "platform-ambiguous-settings", "category": "platform-selection",
     "prompt": "Build me a settings screen for my app. Needs notifications on/off, appearance, account, and about.",
     "expected_output": "Detects that platform and deployment target are unstated. Either inspects the project for them, asks one concise question, or proceeds on an explicitly stated assumption (e.g. iOS 17+, SwiftUI). Uses standard grouped form controls and does not present iOS chrome as universal.",
     "files": [],
     "references_expected": ["patterns/settings", "components/lists-forms"], "max_reference_files": 3,
     "assertions": [
       "The response either asks which Apple platform(s)/deployment target apply, or explicitly states the platform and minimum OS version it assumed",
       "Any SwiftUI code uses Form or List with sections and standard Toggle/Picker/NavigationLink controls rather than hand-drawn rows",
       "The code does not use NavigationView",
       "The response does not use fixed point sizes via .font(.system(size:)) for body text",
       "If macOS is mentioned, the response says a Mac app exposes settings through a Settings scene or app-menu Settings item rather than an in-content tab",
       "No API newer than the stated or assumed deployment target is used without an availability note or #available check"
     ]},
    {"id": 2, "name": "multiplatform-navigation", "category": "platform-selection",
     "prompt": "We have one SwiftUI codebase targeting iOS 18, iPadOS 18 and macOS 15. The app has three top-level areas (Notes, Tags, Archive) and each note opens a detail editor. Propose the navigation architecture and show the root view code so each platform gets what its users expect.",
     "expected_output": "One adaptive structure: TabView with Tab values and .tabViewStyle(.sidebarAdaptable), or NavigationSplitView; NavigationStack inside sections; macOS menu-bar commands and keyboard shortcuts. Layout decisions keyed on size class, not device idiom.",
     "files": [],
     "references_expected": ["components/navigation", "implementation/adaptive-layout", "platforms/macos"], "max_reference_files": 4,
     "assertions": [
       "The root structure uses either TabView with .tabViewStyle(.sidebarAdaptable) or NavigationSplitView",
       "The code does not use NavigationView or the tabItem modifier",
       "The response describes how the same structure presents on iPhone, iPad and Mac (e.g. bottom tab bar, top tab bar convertible to sidebar, sidebar)",
       "Layout branching, if any, uses size classes or the adaptive container rather than UIDevice.current.userInterfaceIdiom or #if os() around whole screens",
       "The response mentions macOS menu bar commands and/or keyboard shortcuts as a Mac expectation",
       "Every API used is available on iOS 18 / macOS 15, or the response marks it with an availability check"
     ]},
    {"id": 3, "name": "catalyst-or-native-mac", "category": "cross-platform",
     "prompt": "We ship an iPad app (UIKit with some SwiftUI screens). Management wants it on the Mac next quarter. Catalyst or a native macOS target? And if Catalyst, which idiom, and what will Mac users notice is wrong if we just tick the box?",
     "expected_output": "Explains the trade-off; names iPad idiom (scaled to 77%) vs Mac idiom (100%, needs layout audit); lists what Catalyst provides automatically and which Mac conventions still need work (menu bar commands, keyboard shortcuts, window resizing, fixed font sizes). Cites the Mac Catalyst HIG page. Gives a recommendation with its assumptions.",
     "files": [],
     "references_expected": ["platforms/catalyst", "platforms/macos"], "max_reference_files": 3,
     "assertions": [
       "The response distinguishes the 'Scale Interface to Match iPad' (iPad) idiom from the Mac idiom",
       "The response states that the iPad idiom scales the interface down to 77%",
       "The response says the Mac idiom requires auditing layout and recommends text styles over fixed font sizes",
       "The response names at least two things Catalyst provides automatically (e.g. menu bar, pointer and keyboard support, window management)",
       "The response names at least two Mac expectations that need explicit work (e.g. complete menu bar commands, keyboard shortcuts, resizable multi-window behaviour)",
       "The response cites the Mac Catalyst HIG page URL",
       "The response does not claim Catalyst apps are rejected by App Review or are unsupported"
     ]},
    {"id": 4, "name": "design-tab-bar-with-action-tab", "category": "design",
     "prompt": "No code yet. Design the top-level structure for an iPhone habit tracker: Today, Habits, Stats, Settings. Product wants a big + in the middle of the tab bar to add a habit, like some social apps have. Is that fine?",
     "expected_output": "Proposes a tab bar for the four sections with text labels and SF Symbols. Explains that the HIG says tab bars are for navigation, not actions, so the + tab conflicts with a recommendation (not a hard requirement); offers an alternative placement and says how to proceed if product insists.",
     "files": [],
     "references_expected": ["components/tab-bars"], "max_reference_files": 2,
     "assertions": [
       "The response proposes a tab bar for the top-level sections and gives each tab a text label",
       "The response states that the HIG says to use a tab bar for navigation rather than actions",
       "The + tab is classified as a departure from a recommendation or platform convention, not as a confirmed violation or App Review rejection",
       "At least one concrete alternative location for the add action is proposed (e.g. toolbar button on Today/Habits)",
       "The response cites the tab bars HIG page URL",
       "The response contains no Swift code longer than 5 lines"
     ]},
    {"id": 5, "name": "implement-native-settings-ios17", "category": "implementation",
     "prompt": "make this settings screen feel native. SwiftUI, min iOS 17. Right now it's a ScrollView of custom HStack rows with my own switch drawing, 15pt Helvetica everywhere and a #F2F2F2 background. Sections: Notifications (push, email digest), Appearance (text size preview), Account (email, sign out), About (version). Give me the full view.",
     "expected_output": "A NavigationStack + Form/List with sections, Toggle, LabeledContent, a destructive-role Sign Out button with confirmation, system text styles and semantic colours. All APIs available on iOS 17. Brief note of what changed and why, with sources.",
     "files": [],
     "references_expected": ["patterns/settings", "components/lists-forms", "implementation/swiftui-availability"], "max_reference_files": 3,
     "assertions": [
       "The code uses NavigationStack and a Form or List with Section headers",
       "The code uses Toggle for the on/off settings",
       "The code contains no .font(.system(size:)) and no custom font with a fixed size lacking relativeTo",
       "The code contains no hard-coded hex/RGB background colour; it relies on the default or a system background style",
       "Sign out is a Button with a destructive role and/or a confirmation step",
       "The code uses no API introduced after iOS 17 without an #available check",
       "The explanation ties at least two changes to a cited HIG or API documentation URL"
     ]},
    {"id": 6, "name": "review-orders-view", "category": "review",
     "prompt": "HIG review please: evals/files/OrdersView.swift. iPhone only, deployment target iOS 17. Tell me what actually matters before release.",
     "expected_output": "A structured review using the five classifications, each finding with severity, rationale, source URL and fix. Finds at least 7 of the 9 planted issues, separates deprecated-API and accessibility issues from convention and taste, and orders by severity.",
     "files": ["evals/files/OrdersView.swift"],
     "references_expected": ["components/navigation", "components/buttons", "components/alerts-sheets", "accessibility/core", "implementation/deprecations"], "max_reference_files": 5,
     "assertions": [
       "Every finding carries exactly one of the five classification labels, a severity, a concrete fix, and a developer.apple.com URL or an explicit note that no source exists",
       "NavigationView is flagged as deprecated with NavigationStack (or NavigationSplitView) named as the replacement, without asserting a specific deprecation version as fact",
       "The Image with onTapGesture is flagged and replaced with a Button (or Menu), citing accessibility and/or the SwiftUI guidance to use Button for button-like controls",
       "The 24x24 frame on the add button is flagged as below the 44x44 pt hit-target guidance, classified as an accessibility issue",
       "The hard-coded font sizes are flagged, with text styles / Dynamic Type as the fix, and the 10 pt text is identified as below the 11 pt iOS minimum",
       "The red/green dot is flagged as conveying status by colour alone, with a non-colour alternative (text, symbol) proposed",
       "The alert is flagged as an informational, non-actionable alert shown on appear (or for its deprecated Alert API), with an in-context alternative",
       "The hamburger menu is classified as a platform convention mismatch or recommended improvement, not as a confirmed guideline or API violation"
     ]},
    {"id": 7, "name": "review-custom-seven-tab-bar", "category": "review",
     "prompt": "Can you check evals/files/RootTabs.swift against Apple's guidelines? iPhone app, iOS 18 minimum. Our designer built the tab bar custom because 'the system one is ugly'.",
     "expected_output": "Recommends replacing the custom bar with TabView/Tab; flags missing labels, colour-only selection, small non-button targets, hard-coded white, deprecated foregroundColor. Treats the 7-tab count as a recommendation issue (overflow / More tab), without inventing a numeric HIG limit.",
     "files": ["evals/files/RootTabs.swift"],
     "references_expected": ["components/tab-bars", "accessibility/core", "foundations/color"], "max_reference_files": 4,
     "assertions": [
       "The review recommends the system TabView (with Tab on iOS 18) in place of the custom HStack bar",
       "Missing text labels on tabs are flagged, citing the HIG guidance to include tab labels",
       "The seven tabs are flagged with reference to overflow / the More tab or to fewer tabs being easier to navigate, and classified as a recommended improvement or convention mismatch",
       "The review does not assert that the HIG sets a hard numeric maximum of five tabs on iPhone",
       "Selection indicated only by blue vs gray is flagged as colour-only state or the icons are flagged as lacking accessibility labels/selected trait",
       "Color.white is flagged for Dark Mode and a system background colour/material is proposed",
       "foregroundColor is identified as deprecated with foregroundStyle as the replacement",
       "The custom bar itself is not labelled a 'Confirmed guideline or API violation' solely for being custom"
     ]},
    {"id": 8, "name": "refactor-minimal-diff-dynamic-type", "category": "refactor",
     "prompt": "evals/files/ProfileHeader.swift - make the text respect Dynamic Type. Minimal diff please, this file is in a release branch (min iOS 16). Don't restyle anything else.",
     "expected_output": "Replaces the three fixed-size fonts with text styles (or scaled equivalents), preserving weight. Leaves layout, button style, names and structure untouched. May mention foregroundColor deprecation and lineLimit truncation as optional follow-ups without applying them.",
     "files": ["evals/files/ProfileHeader.swift"],
     "references_expected": ["accessibility/dynamic-type"], "max_reference_files": 2,
     "assertions": [
       "All three .font(.system(size:)) calls are replaced with Dynamic Type-aware fonts (text styles, or a size tied to a text style)",
       "The semibold weight of the name is preserved",
       "No lines other than the three font lines are modified in the applied change (a diff shows at most 4 changed lines)",
       "View, property and parameter names are unchanged and no new files or types are added",
       "Any other observations (foregroundColor, lineLimit(2) truncation at large sizes) are reported as optional follow-ups, not applied",
       "No API newer than iOS 16 is introduced"
     ]},
    {"id": 9, "name": "accessibility-audit-player", "category": "accessibility",
     "prompt": "Accessibility audit of evals/files/PlayerControls.swift (iOS 17). We got a complaint from a VoiceOver user and another from someone who gets motion sick.",
     "expected_output": "Findings grouped by assistive need: VoiceOver (unlabelled gesture images, decorative image), motor (20 pt targets), vision (contrast, pinned Dynamic Type), motion (endless pulse ignoring Reduce Motion). Each with fix code and source. States what cannot be verified statically and recommends Accessibility Inspector/VoiceOver testing.",
     "files": ["evals/files/PlayerControls.swift"],
     "references_expected": ["accessibility/core", "accessibility/voiceover", "accessibility/dynamic-type"], "max_reference_files": 3,
     "assertions": [
       "The three control images are flagged as not being buttons/lacking accessibility labels, and the fix uses Button with an accessibility label (or Label)",
       "The repeating pulse animation is flagged and the fix reads the Reduce Motion setting (accessibilityReduceMotion)",
       "The .dynamicTypeSize(.medium) modifier is flagged as preventing text scaling",
       "The light-gray artist text on white is flagged for insufficient contrast, referencing the 4.5:1 guidance or recommending measurement",
       "The 20x20 pt targets and/or 4 pt spacing are flagged against the 44x44 pt guidance",
       "The decorative overlay image is recommended to be hidden from VoiceOver, or the response asks whether it is decorative",
       "The response states that a static review cannot confirm runtime behaviour and names at least one tool or manual test (Accessibility Inspector, VoiceOver)"
     ]},
    {"id": 10, "name": "adapt-iphone-to-ipad", "category": "cross-platform",
     "prompt": "why does my iPad app look like a stretched phone app? evals/files/LibraryView.swift is the root. iOS/iPadOS 18. Fix it without making the iPhone version worse.",
     "expected_output": "Explains the cause (single-column stack plus idiom-based magic numbers). Moves to NavigationSplitView or adaptive TabView, removes the UIDevice check in favour of size classes/adaptive containers and text styles; mentions pointer/keyboard and resizable windows. iPhone behaviour preserved through automatic collapse.",
     "files": ["evals/files/LibraryView.swift"],
     "references_expected": ["platforms/ipados", "implementation/adaptive-layout"], "max_reference_files": 3,
     "assertions": [
       "The fix introduces NavigationSplitView or a sidebar-adaptable TabView for regular width",
       "The UIDevice.current.userInterfaceIdiom check is removed, with the reason that layout should follow size class/available space rather than device type",
       "The fixed 200 pt horizontal padding is removed or replaced with an adaptive mechanism",
       "The idiom-dependent fixed font size is replaced with a text style",
       "The response explains how the result behaves in compact width (iPhone, narrow iPad window)",
       "The response mentions at least one further iPad expectation (keyboard shortcuts, pointer, multitasking/resizable windows)"
     ]},
    {"id": 11, "name": "adapt-ios-to-watchos", "category": "cross-platform",
     "prompt": "Porting our iOS interval-timer app to Apple Watch (watchOS 11+). On iPhone it has 4 tabs: Timer, Presets, History, Settings, and the timer screen has six buttons. Sketch the watch app structure and give me the SwiftUI root.",
     "expected_output": "A reduced, glanceable watch design: fewer destinations, shallow hierarchy, vertical pagination driven by the Digital Crown, primary action prominent, settings and history demoted or left on iPhone. Notes that the iOS tab bar is not a watchOS component and that complications/notifications matter.",
     "files": [],
     "references_expected": ["platforms/watchos"], "max_reference_files": 2,
     "assertions": [
       "The proposal reduces scope relative to the iPhone app (fewer top-level destinations and fewer than six controls on the timer screen)",
       "The response states that the iOS bottom tab bar is not used on watchOS and proposes vertical pages or a list instead",
       "The Digital Crown is named as the navigation/scroll input",
       "Any use of the verticalPage tab style or other watchOS-only API is consistent with the watchOS 11 target",
       "The response mentions at least one of complications, Smart Stack widgets, or notifications as part of the watch experience",
       "The code uses no iOS-only API (e.g. tabViewBottomAccessory, UIKit types)"
     ]},
    {"id": 12, "name": "adapt-to-visionos", "category": "cross-platform",
     "prompt": "We're adding a visionOS 26 target to our SwiftUI iOS 26 app. The main screen has a bottom tab bar, a row of 32pt icon buttons packed 8pt apart, and a custom card that uses .glassEffect(). What needs to change?",
     "expected_output": "Keeps a windowed UI; explains the vertical leading tab bar; enlarges and spaces targets to the 60 pt guidance; flags that glassEffect lists no visionOS availability and proposes a visionOS-appropriate alternative with a conditional; mentions hover effects and rounded shapes.",
     "files": [],
     "references_expected": ["platforms/visionos", "implementation/swiftui-availability"], "max_reference_files": 3,
     "assertions": [
       "The response states that on visionOS the tab bar is vertical on the leading side of the window (system-provided), not at the bottom",
       "The 32 pt buttons are flagged against the 60x60 pt visionOS target guidance",
       "The 8 pt spacing is flagged, with more space between interactive elements recommended",
       "glassEffect is identified as unavailable or unverified on visionOS, and the code is conditioned (#if os(visionOS) or availability) with an alternative such as glassBackgroundEffect",
       "The response recommends keeping standard windows for the UI rather than a fully immersive space",
       "The response cites at least one visionOS-specific HIG URL"
     ]},
    {"id": 13, "name": "adapt-to-tvos", "category": "cross-platform",
     "prompt": "Bringing our iOS video catalogue (SwiftUI) to Apple TV. The iOS home screen is a vertical feed with swipe actions, 12pt captions and content running edge to edge. What do we change for tvOS?",
     "expected_output": "Focus-driven navigation with system focus effects, no touch-only gestures, larger text, content inset to the tvOS safe area, top tab bar. Uses HIG numbers only where the HIG gives them.",
     "files": [],
     "references_expected": ["platforms/tvos"], "max_reference_files": 2,
     "assertions": [
       "The response says interaction is focus-based via remote and recommends system-provided focus effects",
       "Swipe actions are replaced with a focus/remote-appropriate alternative",
       "The 12 pt captions are flagged as below tvOS text guidance (23 pt minimum / 29 pt default)",
       "Primary content is inset from screen edges, citing the 60 pt top/bottom and 80 pt side safe-area guidance",
       "The response does not recommend a bottom tab bar on tvOS",
       "At least one tvOS HIG URL is cited"
     ]},
    {"id": 14, "name": "deployment-target-newer-api", "category": "deprecated-unsupported-api",
     "prompt": "Our minimum is iOS 16 and that is not changing this year. Add an empty state to SearchResultsView using ContentUnavailableView, switch our TabView to the new Tab { } syntax, and put a Liquid Glass background on the floating filter button.",
     "expected_output": "States that ContentUnavailableView is iOS 17+, Tab is iOS 18+, and glassEffect is iOS 26+. Provides #available-gated code with iOS 16 fallbacks (custom empty state, tabItem, a material background) and does not raise the deployment target.",
     "files": [],
     "references_expected": ["implementation/swiftui-availability", "implementation/deprecations"], "max_reference_files": 2,
     "assertions": [
       "The response states ContentUnavailableView requires iOS 17 or later",
       "The response states the Tab type requires iOS 18 or later",
       "The response states glassEffect requires iOS 26 or later",
       "Each of the three APIs is wrapped in if #available (or @available) with a fallback that compiles on iOS 16",
       "The iOS 16 tab fallback uses tabItem and the response does not call that a violation",
       "The response does not tell the user to raise the deployment target as the only solution"
     ]},
    {"id": 15, "name": "conflict-brand-vs-hig", "category": "conflicting-guidance",
     "prompt": "Brand team is firm: every screen gets our solid orange navigation bar with white uppercase 10pt titles, and we want our own light/dark switch inside the app instead of following the system. I know Apple doesn't love this. Just implement it in SwiftUI (iOS 17) and tell me what's actually a hard rule vs taste.",
     "expected_output": "Implements what was asked. Separately lists each departure with its level: toolbar backgrounds/tint and app-specific appearance setting are HIG recommendations; 10 pt text is below the 11 pt minimum and uppercase white-on-orange needs a contrast check (accessibility). States that none is a compile-time or documented hard requirement, and offers low-cost mitigations.",
     "files": [],
     "references_expected": ["components/toolbars", "foundations/color", "foundations/typography"], "max_reference_files": 3,
     "assertions": [
       "The response provides working SwiftUI code for the coloured bar and the in-app appearance switch rather than refusing",
       "The in-app appearance switch is identified as something the HIG advises against, labelled a recommendation, not a requirement",
       "The 10 pt title is flagged as below the 11 pt minimum text size for iOS and as an accessibility concern",
       "The response recommends checking white-on-orange contrast and does not state a contrast ratio it has not computed from given colour values",
       "The response explicitly separates hard requirements (API/compile-time or App Review) from HIG recommendations and from subjective suggestions",
       "At least one mitigation that keeps the brand intent is offered (e.g. system option in the switch, text style scaled title)",
       "The response does not claim the design will be rejected by App Review"
     ]},
    {"id": 16, "name": "hallucination-fake-modifier-and-rule", "category": "hallucination-trap",
     "prompt": "Two things. (1) Apply .liquidGlassStyle(.prominent) to my toolbar buttons - I saw it in a blog post, iOS 26. (2) Our lead says the HIG rule is that all buttons must be exactly 50pt tall; please enforce that across the app with a ViewModifier.",
     "expected_output": "Says it cannot verify a liquidGlassStyle modifier in Apple's documentation and offers the documented API (glassEffect / the glass button style, iOS 26). Corrects the 50 pt claim: the HIG gives a general 44x44 pt hit-region guideline (60x60 on visionOS), not a 50 pt height rule; offers a minimum-hit-target modifier instead.",
     "files": [],
     "references_expected": ["components/buttons", "implementation/swiftui-availability"], "max_reference_files": 2,
     "assertions": [
       "The response does not produce code calling .liquidGlassStyle as if it were a real API",
       "The response states that liquidGlassStyle is not a documented SwiftUI modifier or could not be verified",
       "A documented alternative is offered (glassEffect(_:in:) or .buttonStyle(.glass)) with its iOS 26 availability",
       "The response states that the HIG does not specify a 50 pt button height",
       "The response cites the 44x44 pt hit-region guidance and describes it as a guideline/general rule",
       "Any ViewModifier provided enforces a minimum hit area rather than a fixed 50 pt height, or the response explains why it declines the fixed height"
     ]},
    {"id": 17, "name": "uncertainty-unspecified-numbers", "category": "uncertainty",
     "prompt": "Quick ones for a design spec, I need exact values with the HIG section for each: (a) max number of tabs allowed on iPhone, (b) the corner radius Apple requires for cards, (c) required animation duration for presenting a sheet, (d) will App Review reject us for using a custom tab bar?",
     "expected_output": "For each, says what the HIG does and does not state: no numeric tab maximum (avoid overflow / More tab); no mandated card radius; no mandated sheet duration (system-provided); App Review outcome cannot be predicted from the HIG. Offers practical defaults clearly labelled as conventions or suggestions.",
     "files": [],
     "references_expected": ["components/tab-bars"], "max_reference_files": 2,
     "assertions": [
       "For (a) the response says the HIG gives no fixed maximum for iPhone and mentions avoiding overflow/the More tab",
       "For (b) the response does not present a specific corner-radius value as an Apple requirement",
       "For (c) the response does not present a specific duration as an Apple requirement and notes system presentations supply their own animation",
       "For (d) the response says it cannot guarantee an App Review outcome and does not answer with an unqualified yes or no",
       "Any number offered for (a)-(c) is explicitly labelled as a convention, default, or suggestion rather than an HIG rule",
       "The response contains no fabricated HIG section title or quotation for (b) or (c)"
     ]},
    {"id": 18, "name": "token-efficiency-simple-question", "category": "context-efficiency",
     "prompt": "what's the minimum tap target on iOS?",
     "expected_output": "A short answer: 44x44 pt recommended hit region (HIG buttons / accessibility), with 28x28 pt listed as the minimum control size in the accessibility table; one source link. Loads at most one reference file and no platform or implementation references.",
     "files": [],
     "references_expected": ["components/buttons"], "max_reference_files": 1,
     "assertions": [
       "The answer states 44x44 pt",
       "The answer includes one developer.apple.com HIG URL",
       "The answer is at most 120 words",
       "The transcript shows at most one reference file read after SKILL.md",
       "The answer does not include an unrequested review, code listing longer than 5 lines, or multi-platform survey"
     ]}
  ]
}
```

Coverage map: platform selection 1-3; design 4; implementation 5; review 6-7; refactor 8; accessibility 9; cross-platform
3, 10-13; deployment target 14; conflicting guidance 4, 15; hallucination 16; uncertainty 17; token efficiency 18.
Assertions that inspect code (no `NavigationView`, no `.font(.system(size:`, `#available` present, changed-line count,
word count, reference-read count) should be graded by script, the rest by an LLM grader with quoted evidence [V upstream advice].

Expected baseline behaviour (hypotheses to confirm, [M]): without the skill, models tend to pass 5, 8, 9 and 10 on
code-level assertions but fail classification labels, sourcing URLs, "no five-tab hard rule" (7, 17), visionOS `glassEffect`
availability (12), and tvOS/Catalyst numbers (3, 13). If an assertion passes in both configurations for 3 runs, remove it [V].

## 3. Grading rubric and comparison procedure

### 3.1 Dimensions (score 0-4 each per eval; N/A allowed)

| Dimension | Weight | 0 | 2 | 4 |
|---|---|---|---|---|
| Accuracy | 20 | invented API/number/HIG claim | correct but one imprecise claim | every factual claim matches Apple docs |
| Sourcing | 10 | no sources | some URLs, or URLs not matching claims | each substantive claim has a developer.apple.com URL that supports it |
| Classification correctness | 15 | labels missing or recommendations called violations | <=1 mislabel | all findings in the right one of five classes; HARD vs REC explicit |
| Severity calibration | 10 | taste ranked above broken accessibility | ordering mostly right | deprecated API/a11y blockers > convention > taste, with stated reason |
| Minimality of change | 10 | rewrites unrelated code | small unrelated edits | only requested lines change; extras listed as optional |
| Platform appropriateness | 10 | iOS idioms applied everywhere | right platform, one stray idiom | components, inputs and metrics match each target platform and OS version |
| Accessibility coverage | 10 | ignored | partial (labels only) | VoiceOver, Dynamic Type, contrast/colour, target size, motion considered where relevant |
| Honesty / uncertainty | 10 | confident fabrication | hedges generically | says exactly what is unverified, why, and how to verify |
| Context efficiency | 5 | loads most references | 1-2 files over budget | within `max_reference_files`; answer length fits the question |

Weighted score = sum(weight x score / 4), renormalised over applicable dimensions. Assertions give the objective layer;
the rubric is the holistic layer scored by a blind LLM judge plus human spot check of at least 5 evals per iteration.

### 3.2 Pass thresholds

| Gate | Threshold |
|---|---|
| Per eval | >= 80% of assertions pass AND no "critical" assertion fails (critical = any assertion beginning "does not" about invented APIs, numbers, rules or App Review claims; and all availability assertions in 12, 14, 16) |
| Suite, with skill | mean assertion pass rate >= 0.85 over 3 runs; every eval passes in >= 2 of 3 runs; stddev of pass rate <= 0.15 per eval |
| Skill value | with-skill minus baseline mean pass rate >= +0.20; no eval where baseline beats with-skill by > 0.10 |
| Hallucination | zero fabricated API or HIG number across all runs of 14, 16, 17 (hard gate) |
| Rubric | weighted score >= 75/100 mean; Accuracy and Honesty each >= 3.0 mean |
| Cost | with-skill median tokens <= 1.6x baseline on evals 1-17; eval 18 reads <= 1 reference and total tokens <= baseline + SKILL.md size + 1 reference |
| Triggering | section 1 targets |

The numeric thresholds are proposals [M]; upstream gives no pass marks, only "is the delta worth the cost" [V].

### 3.3 With-skill vs baseline procedure

1. Snapshot: `cp -r apple-hig apple-hig-workspace/skill-snapshot/` before edits (used as `old_skill` baseline from iteration 2) [V].
2. For each eval and each of 3 runs, spawn two fresh-context subagents in the same turn: one given the skill path, one given none
   (identical prompt, model, tools, fixture files copied into an empty temp project). Save to
   `apple-hig-workspace/iteration-N/eval-<name>/{with_skill,without_skill}/run-<k>/outputs/` [V layout; `run-<k>` is our addition].
3. Record `timing.json` (`total_tokens`, `duration_ms`) on completion [V]; also save the transcript and a `metrics.json` with
   tool-call counts and the list of files read (needed for context-efficiency assertions).
4. Grade: script-gradable assertions first (regex for banned APIs, `#available` presence, `git diff --numstat`, word count, reads of
   `references/`); remaining assertions by a grader subagent that must quote evidence; write `grading.json` with `text/passed/evidence`.
5. Blind comparison: shuffle the two outputs as A/B, judge with the 3.1 rubric without revealing which used the skill; record winner.
6. Aggregate `benchmark.json` (mean, stddev, delta for pass_rate, time, tokens) and a per-assertion table: passes-both (delete),
   fails-both (fix assertion or skill), skill-only (keep), baseline-only (regression: investigate).
7. Human review of outputs; `feedback.json` with one actionable line per eval; iterate; stop when feedback is empty or deltas flatten [V].
8. Run the suite on at least two model tiers; a skill that only helps the strongest model is under-specified [M].

## 4. Validation procedures

### 4.1 Static checks for `scripts/validate.py` (stdlib only, exit non-zero on error; `--online` optional)

| # | Check | Rule | Level |
|---|---|---|---|
| S1 | Frontmatter parses | starts with `---`, YAML mapping, only keys name, description, license, compatibility, metadata, allowed-tools | error [V spec + quick_validate] |
| S2 | `name` | 1-64 chars, `^[a-z0-9]+(-[a-z0-9]+)*$`, equals parent directory name | error [V] |
| S3 | `description` | non-empty, <= 1024 chars, no `<` `>`; contains a "use when" trigger clause; key use case within the first 200 chars (Claude Code truncates listings at 1,536) | error / warn [V limits; heuristic ours] |
| S4 | `compatibility` / `metadata` | <= 500 chars; string->string map | error [V] |
| S5 | SKILL.md budget | < 500 lines; estimated tokens (chars/4) < 5000; warn at 400 lines / 4000 tokens | error / warn [V limits; estimator M] |
| S6 | Reference budget | each `references/**/*.md` <= 300 lines and <= 3000 est. tokens; files > 100 lines start with a table of contents | warn [M numbers] |
| S7 | Links resolve | every relative Markdown link and backticked `references/...`, `scripts/...`, `examples/...` path in any .md exists; anchors exist | error |
| S8 | No orphans | every file under `references/` and `examples/` is reachable from SKILL.md in <= 1 hop (spec: one level deep) | error [V rule] |
| S9 | Routing table complete | each routing-table row points at an existing file; each reference file appears in the table | error |
| S10 | Provenance | each reference file has >= 1 `https://developer.apple.com/` URL and a `Last verified: YYYY-MM-DD` line; warn if older than 180 days | error / warn |
| S11 | Claim tags | every line containing a number followed by `pt`/`px`/`%`/`:1` in references has a source URL in the same section | warn |
| S12 | evals schema | `evals/evals.json`: `skill_name` == frontmatter name; `evals` non-empty; unique integer `id`; non-empty `prompt`, `expected_output`; `files` exist; 4-8 `assertions` (or `expectations`) strings; `max_reference_files` integer if present | error |
| S13 | trigger set schema | JSON array; each item has string `query` and boolean `should_trigger`; >= 8 of each; no duplicate queries; both splits contain both labels | error |
| S14 | Swift fences | every ```` ```swift ```` fence closed; braces, parentheses and brackets balanced per block after stripping strings and comments; no tab/space mix | error |
| S15 | Swift parse (if toolchain) | `swiftc -parse` (or `swift-format lint`) on each example file and fenced block marked compilable; skipped with a notice when `swiftc` is absent | error / skip |
| S16 | Deprecated deny-list | regex for `NavigationView`, `.foregroundColor(`, `.cornerRadius(`, `.tabItem`, `Alert(`, `ActionSheet(`, `.alert(isPresented:`, `.navigationBarHidden(`, `.navigationBarTitle(`, `.onChange(of:perform:`/single-parameter `onChange` closure, `NavigationLink(destination:isActive:`, `UIScreen.main`, `UIDevice.current.userInterfaceIdiom` in fenced Swift, unless the block or the 3 preceding lines carry a marker (`// Avoid`, `// Deprecated`, `// Before`, `// Fallback for iOS <N>`, "Don't") | error |
| S17 | Availability annotations | every fenced Swift block using a symbol from the availability table (iOS 17+/18+/26+ list) has `#available`/`@available` or a comment stating minimum OS | warn |
| S18 | Fake-API deny-list | the trap names in section 0 never appear outside `evals/` | error |
| S19 | Hygiene | no absolute local paths, no TODO/TBD in shipped files, no smart quotes inside code fences, no file > 1 MB, UTF-8, LF endings | warn |
| S20 | Online: URL liveness | each unique external URL returns 200 (HEAD then GET, 3 retries, rate-limited); for `developer.apple.com/design/human-interface-guidelines/<slug>` also fetch the `.json` endpoint because the HTML shell can return 200 for missing pages [M]; report 404s such as the removed `navigation-bars` [V] | warn |
| S21 | Online: availability drift | for each symbol in the availability table, fetch DocC JSON and compare `introducedAt`/`deprecated` with the recorded value | warn |
| S22 | Online: HIG change log | compare each cited HIG page's newest change-log date with the file's `Last verified` date | warn |

`deprecatedAt` handling in S21: treat a value equal to the newest OS version seen across the batch as "soft-deprecated, version
not meaningful" [V observation: 27.3 on eight symbols], not as a deprecation version.

### 4.2 Manual procedures

**Xcode build of examples.** New multiplatform SwiftUI app project; add each `examples/*.swift`; set deployment targets to the
minimum each example declares; build for iOS, iPadOS, macOS, watchOS, tvOS and visionOS destinations as applicable with
warnings as errors off, then note every deprecation warning; run on the oldest and newest simulators; confirm `#available`
fallback branches by running on the oldest. Record Xcode and SDK versions next to `Last verified`.

**Accessibility pass (per example screen).** Xcode Accessibility Inspector audit (contrast, hit region, missing label, clipped
text) with zero unexplained warnings; VoiceOver swipe-through in order with every control announced with role and state; largest
accessibility text size with no truncation of essential text; Increase Contrast, Reduce Motion, Differentiate Without Colour,
Bold Text toggled; Dark and Light; right-to-left pseudo-language; Full Keyboard Access on iPad/Mac; Voice Control "show names".

**Cross-agent smoke test** (same three prompts everywhere: trigger query 1, eval 6, eval 18):

| Client | Install | Confirm activation | Confirm reference loading |
|---|---|---|---|
| Claude Code | copy to `<proj>/.claude/skills/apple-hig/` [V]; new session; ask "What skills are available?" or type `/apple-hig` | `claude -p "<prompt>" --output-format stream-json --verbose` and look for a `Skill` tool_use naming `apple-hig`, or a `Read` of its SKILL.md [V detection logic] | in the same stream, list `Read` calls under `references/`; compare with `references_expected` and `max_reference_files` |
| Codex CLI | copy to `<proj>/.agents/skills/apple-hig/` (cross-client convention [V]; Codex-specific path [M]) | ask the agent to list available skills; run the prompt and inspect the tool/exec log for a read of `SKILL.md` [M] | inspect the log for reads of `references/*.md` [M] |
| Cursor | copy to `<proj>/.agents/skills/` or `.cursor/skills/` [M]; reload window | agent panel shows the skill/file read; ask "which skill did you use and which files did you open" as a weak fallback [M] | tool-call list in the agent panel [M] |

Pass: skill activates on prompts 1 and 6 in every client; eval 18 reads <= 1 reference; no client reads every reference file;
relative links resolve from the skill root regardless of working directory. Self-report by the agent is a fallback only; logs are
the evidence. Also test a negative (trigger query "Jetpack Compose ... Material 3") for non-activation.

## 5. Design recommendations for the skill text

### 5.1 Hallucination prevention

1. **Closed-world rule in SKILL.md:** "Use only APIs and numbers that appear in this skill's references or that you verify in
   Apple documentation during the task. If neither, say 'not verified' and give the lookup URL pattern." Include the two JSON URL
   patterns from the brief so agents with network access can self-verify.
2. **Availability table as the single source of truth** (`implementation/swiftui-availability`): symbol, introduced per
   platform, replacement, source URL. Rule: before emitting any symbol newer than the deployment target, add `#available` plus a
   fallback. Ask for the deployment target once if it is neither stated nor discoverable (`IPHONEOS_DEPLOYMENT_TARGET`,
   `Package.swift` `platforms:`).
3. **Three-level vocabulary used everywhere:** Requirement (API contract, platform limitation, documented "can't"), HIG
   recommendation, Convention/suggestion. Most HIG text is recommendation ("as a general rule", "strive", "prefer", "avoid") [V];
   the skill should say so and reserve "Confirmed guideline or API violation" for explicit HIG "don't/avoid/always" statements
   quoted with a URL, or for deprecated/unavailable API use.
4. **"Numbers the HIG does not give" list** in SKILL.md gotchas: iPhone tab count, card/button corner radius, sheet animation
   duration, a universal button height. Agents will otherwise supply lore (five tabs, 50 pt, 0.3 s) [V absence for the first three
   in fetched pages; the list should be extended by the other workstreams].
5. **Soft-deprecation note:** state "deprecated; use X" without a version for `NavigationView`, `foregroundColor`, `tabItem`,
   `cornerRadius`, `Alert`, `ActionSheet`; give versions only where metadata has a fixed one (`onChange(of:perform:)` 17.0).
   Deprecated is not "broken": in fallbacks below the replacement's minimum OS it is correct to use them.
6. **Every reference section ends with `Source:` URL(s) and the file carries `Last verified`.** The review format requires a
   source per finding; when no source exists the finding must drop to "Subjective design suggestion".
7. **Never predict App Review.** The HIG is not the App Review Guidelines; say outcomes cannot be guaranteed.
8. **Explain why, do not shout.** Upstream guidance: reasoning-based instructions beat "ALWAYS/NEVER" lists, and gotchas belong
   in SKILL.md where they are read before the mistake [V best-practices.mdx, evaluating-skills.mdx].
9. **Stale-lore callouts** (one line each, sourced): no `navigation-bars` HIG page; tab bars float on Liquid Glass and sit at the
   top on iPadOS; `glassEffect` has no visionOS availability; macOS has no Dynamic Type; HIG now mentions Macs with touch displays.
10. **Uncertainty template** for outputs: `Unverified: <claim>. Reason: <not in references / could not fetch>. Check: <URL>`.

### 5.2 Token efficiency

1. SKILL.md target <= 250 lines / ~3,000 tokens (limit 500 / 5,000 [V]): activation scope, platform + target detection, task
   router, routing table, review format, gotchas. No component guidance in SKILL.md.
2. **Routing table with load budgets:** columns task, platform, "read first" (one file), "read only if" (conditions). State the
   default: quick factual question = 0-1 references; single-screen implement/review = 2-3; cross-platform adaptation = source
   platform skipped, target platform file + adaptive-layout; never load all platform files.
3. **A 30-line "numbers card"** (F1-F3, F6 tables with URLs) either in SKILL.md or as the smallest reference, so the commonest
   questions need no further reads. This is what makes eval 18 pass.
4. Reference files <= 300 lines, one topic each, table of contents at top, tables over prose, do/don't pairs with 5-10 line Swift
   snippets, no restating of Apple prose. Split by component family, not one file per component (too many reads) and not one
   file per platform containing everything (too large).
5. One level deep: references never require another reference; cross-links are "see also", not prerequisites [V spec].
6. Put platform deltas in the platform file and keep component files platform-neutral with a compact "platform differences" table,
   so an iOS-only task never pays for tvOS text.
7. Review output format: fixed compact template (classification, severity, location, rationale in one sentence, source, fix);
   cap at the top N findings by severity unless asked for exhaustive; group duplicates.
8. Provide defaults, not menus [V best-practices]: one recommended structure per situation with a named escape hatch.
9. Measure: track tokens and files-read per eval in `benchmark.json`; treat a rise of > 20% between iterations without a pass-rate
   gain as a regression.

## 6. Not verified / open items

- Codex and Cursor skill directories, activation indicators and logs (hosts blocked) [M].
- Whether `deprecatedAt: "27.3"` implies no compiler warning; needs an Xcode build [M].
- App Review Guidelines were not fetched; no eval asserts anything about them beyond "do not predict".
- Whether an icon-only SwiftUI `Button` gets an adequate automatic VoiceOver label from its SF Symbol [M]; eval 6 asserts only that
  an explicit label is recommended, which H:voiceover and the `accessibilityLabel` doc support [V].
- Absence claims (F22, no numeric tab cap, no card radius, no sheet duration) cover the 35 HIG pages fetched, not the whole HIG.
- Thresholds in 3.2 and budgets in S6 are proposals to calibrate after the first benchmark run.
- Baseline-behaviour hypotheses in section 2 are untested.
