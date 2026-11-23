# Platform detection and the cross-platform matrix

Scope: how to work out which Apple platform(s), which Mac/Vision flavour and which minimum OS version a request or codebase targets before giving any design or API advice, plus a matrix of what is universal and what differs across the six platforms.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Order of evidence
- Xcode project settings
- Swift packages
- Conditional compilation and imports
- Info.plist keys
- Classify the Mac and Apple Vision flavour
- Minimum OS version and why it gates advice
- When the target is ambiguous
- Universal versus platform-specific matrix
- Common mistakes

## Order of evidence

Work down this list; later evidence refines earlier evidence, but an explicit user statement always wins.

1. [Conv] Explicit statement in the prompt ("iPad app", "watchOS 11", "Mac Catalyst"). Take it literally, including the version.
2. [API] Xcode project: per-target build settings in `*.xcodeproj/project.pbxproj` and any `.xcconfig` files.
3. [API] `Package.swift` `platforms:` list.
4. [API] Conditional compilation in the file being edited (`#if os(...)`, `#if targetEnvironment(macCatalyst)`, `#if canImport(...)`).
5. [Conv] Imports and platform-only APIs in the file (`import AppKit`, `ImmersiveSpace`, `.digitalCrownRotation`).
6. [API] Info.plist keys (`UIApplicationSceneManifest`, `WKApplication`, `LSUIElement`, ...).
7. [Conv] Target layout: a project usually has one target per design surface (app, Watch app, widget extension, Top Shelf extension). Treat each target as its own platform decision.
8. [Conv] Cross-check: if a file compiles for several platforms, give guidance for every platform that compiles it, not only the one named in the prompt.

- [API] A single multiplatform target can cover iOS, iPadOS, macOS, tvOS and visionOS; watchOS apps stay in a separate target. So "one target" does not mean "one platform", and a Watch app is never hidden inside the main target.
- [HIG] Platform is not the same as layout class: decide layout from size classes and available space, not from device type or orientation. Detection tells you which conventions, inputs and APIs apply; it does not tell you the layout.

Source: https://developer.apple.com/documentation/xcode/configuring-a-multiplatform-app-target, https://developer.apple.com/design/human-interface-guidelines/layout

## Xcode project settings

| Setting | What it tells you | Tag |
|---|---|---|
| `SDKROOT` | Name or path of the base SDK the target builds against | [API] |
| `SUPPORTED_PLATFORMS` | List of platforms whose SDKs the target can build with; several entries means a multiplatform target | [API] |
| `TARGETED_DEVICE_FAMILY` | Comma-separated integers: `1` iPhone/iPod touch, `2` iPad (and Mac Catalyst scaled to match iPad), `3` Apple TV, `4` Apple Watch, `6` Mac Catalyst optimized for Mac, `7` Apple Vision. The build system derives the Info.plist `UIDeviceFamily` key from it | [API] |
| `SUPPORTS_MACCATALYST` | Target also builds for Mac Catalyst | [API] |
| `SUPPORTS_MAC_DESIGNED_FOR_IPHONE_IPAD` | Shows the "Mac (Designed for iPhone/iPad)" destinations: the unmodified iOS binary runs on Apple silicon Macs | [API] |
| `SUPPORTS_XR_DESIGNED_FOR_IPHONE_IPAD` | Same for Apple Vision: the iOS binary runs as a compatible app | [API] |
| `IS_MACCATALYST` | Read-only, true while building the Catalyst variant; for scripts | [API] |
| `MACOSX_DEPLOYMENT_TARGET` | Minimum macOS version (shown in Apple's xcconfig example) | [API] |
| `DEPLOYMENT_TARGET_SETTING_NAME` | Name of the deployment-target setting for the platform being built; use it instead of hard-coding a name in scripts | [API] |
| `IPHONEOS_DEPLOYMENT_TARGET`, `TVOS_DEPLOYMENT_TARGET`, `WATCHOS_DEPLOYMENT_TARGET`, `XROS_DEPLOYMENT_TARGET` | Minimum iOS/iPadOS, tvOS, watchOS, visionOS version. Names are not listed in the build settings reference; they appear in Apple's open-source build system (github.com/swiftlang/swift-build) | [Conv] |
| SDK and platform names `iphoneos`, `macosx` | Named as SDKs in Apple's xcconfig documentation (`[sdk=macosx*]` conditions) | [API] |
| SDK and platform names `appletvos`, `watchos`, `xros`, and simulator names `iphonesimulator`, `appletvsimulator`, `watchsimulator`, `xrsimulator` | Present in swift-build sources, not enumerated in the documentation | [Conv] |
| `SDKROOT = auto` for multiplatform targets | Commonly seen in generated projects; not confirmed in any Apple source checked | [Unverified] |

Run from the repository root (read-only):

```bash
# Platforms, device families, deployment targets and Mac/Vision flavours, de-duplicated with counts
grep -hoE '(SDKROOT|SUPPORTED_PLATFORMS|TARGETED_DEVICE_FAMILY|SUPPORTS_MACCATALYST|SUPPORTS_(MAC|XR)_DESIGNED_FOR_IPHONE_IPAD|[A-Z]+_DEPLOYMENT_TARGET) = [^;]+' \
  $(find . -name project.pbxproj -not -path '*/Pods/*' -not -path '*/.build/*') | sort | uniq -c

# The same settings in xcconfig files (these override or feed the project)
grep -rnE '^(SDKROOT|SUPPORTED_PLATFORMS|TARGETED_DEVICE_FAMILY|SUPPORTS_MACCATALYST|[A-Z]+_DEPLOYMENT_TARGET)' --include='*.xcconfig' .

# Target names and product types (app, app extension, watch app)
grep -hE 'productType = |^\s+name = ' $(find . -name project.pbxproj -not -path '*/Pods/*') | sort | uniq -c
```

- [Conv] Settings appear once per build configuration and once at project level; target-level values override project-level ones. If targets disagree, report per target.
- [API] Build settings can be conditional on SDK (`SETTING[sdk=macosx*] = value`); a grep that ignores the bracket part can mislead, so print the whole line.
- [Conv] Projects generated by XcodeGen or Tuist keep the truth in `project.yml` / `Project.swift`; grep those for `deploymentTarget`, `platform` and `destinations` as well.

Source: https://developer.apple.com/documentation/xcode/build-settings-reference, https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project

## Swift packages

- [API] `Package.swift` declares supported platforms and minimum versions in `platforms:` using `SupportedPlatform` values (iOS, macOS, tvOS, watchOS, visionOS, Mac Catalyst and others).
- [API] If `platforms:` is absent, SwiftPM assigns a predefined minimum version for every platform (the oldest the installed SDK supports). Read that as "unspecified", not as "supports everything deliberately".
- [API] A dependency's deployment target must be lower than or equal to the top-level package's; the app target that consumes the package still decides what actually ships.
- [Conv] A UI package with only `.iOS(...)` listed is still compiled for iPadOS (same SDK) and for Mac Catalyst and visionOS compatible-app runs when the host app enables them.

```bash
grep -nE 'platforms:|\.(iOS|macOS|macCatalyst|tvOS|watchOS|visionOS)\(' $(find . -name Package.swift -not -path '*/.build/*')
grep -n 'swift-tools-version' $(find . -name Package.swift -not -path '*/.build/*')
```

Source: https://developer.apple.com/documentation/packagedescription/supportedplatform

## Conditional compilation and imports

| Signal in source | Indicates | Tag |
|---|---|---|
| `#if os(iOS)`, `os(macOS)`, `os(watchOS)`, `os(tvOS)`, `os(visionOS)` | The valid Apple arguments to `os()`. There is no `os(iPadOS)`: iPad code compiles under `os(iOS)` | [API] |
| `#if targetEnvironment(macCatalyst)` | Code specific to the Mac Catalyst build (`simulator` is the other valid argument) | [API] |
| `#if canImport(UIKit)` / `canImport(AppKit)` | Framework-availability branching in multiplatform code; Apple recommends it for unavailable frameworks and `#if os` for unavailable symbols | [API] |
| `UIDevice.current.userInterfaceIdiom` / trait `userInterfaceIdiom` compared with `.phone`, `.pad`, `.tv`, `.carPlay`, `.mac`, `.vision` (also `.unspecified`) | Runtime idiom branching; `.mac` means a Catalyst app in the Mac idiom | [API] |
| `ProcessInfo.processInfo.isiOSAppOnMac` | iOS app running unmodified on a Mac (iOS 14.0+); Apple calls checking it a last resort | [API] |
| `ProcessInfo.processInfo.isMacCatalystApp` | Mac Catalyst build (iOS 13.0+) | [API] |
| `import AppKit`, `NSWindow`, `NSViewController`, `NSMenu` | Native macOS (AppKit) | [Conv] |
| SwiftUI `Settings` scene (macOS 11.0+ only), `MenuBarExtra` (macOS 13.0+ only) | macOS target | [API] |
| `.commands`, `CommandMenu` (iOS 14.0+, macOS 11.0+, visionOS 1.0+) | Menu bar commands: macOS, iPadOS menu bar, visionOS shortcut list | [API] |
| `import WatchKit`, `TabView` with `.verticalPage` (watchOS 10.0+ only), `.digitalCrownRotation` (watchOS 6.0+ only) | watchOS | [API] |
| `import TVServices` (tvOS 9.0+), heavy use of `UIFocusGuide` | tvOS (focus guides also exist on iOS/visionOS) | [API] |
| `ImmersiveSpace`, `.ornament(...)`, `.windowStyle(.volumetric)` (all visionOS 1.0+ only) | Native visionOS. `import RealityKit` alone is not decisive | [API] |
| `ArrangementView`, `ReservedRegion`, `UIArrangementViewController` (27.1+) | iPhone Duo-aware code and a 27.1 deployment target or availability guard | [API] |

```bash
grep -rnoE '#(if|elseif) +!?(os|targetEnvironment|canImport)\([A-Za-z]+\)' --include='*.swift' . | awk -F: '{print $NF}' | sort | uniq -c | sort -rn
grep -rhoE '^import +(UIKit|AppKit|SwiftUI|WatchKit|TVUIKit|TVServices|RealityKit|ARKit|WidgetKit|ActivityKit)' --include='*.swift' . | sort | uniq -c
grep -rnE 'userInterfaceIdiom|isiOSAppOnMac|isMacCatalystApp' --include='*.swift' . | head -20
```

- [HIG] Finding idiom checks used for layout is itself a review finding: layout should follow size classes, not device type.

Source: https://docs.swift.org/swift-book/documentation/the-swift-programming-language/statements/ (conditional compilation block; checked in the book's source), https://developer.apple.com/documentation/uikit/uiuserinterfaceidiom, https://developer.apple.com/documentation/foundation/processinfo/isiosapponmac, https://developer.apple.com/documentation/xcode/configuring-a-multiplatform-app-target

## Info.plist keys

Modern projects generate much of Info.plist from build settings (`INFOPLIST_KEY_...`), so grep both the plist files and `project.pbxproj`.

| Key | Meaning | Tag |
|---|---|---|
| `UIDeviceFamily` | Written by the build system from `TARGETED_DEVICE_FAMILY` (the key has no documentation page of its own) | [API] |
| `MinimumOSVersion` | Minimum iOS, iPadOS, tvOS, watchOS version; Xcode writes it from the deployment target, do not set it by hand | [API] |
| `LSMinimumSystemVersion` | Minimum macOS version | [API] |
| `LSRequiresIPhoneOS` | App must run in iOS | [API] |
| `UIApplicationSceneManifest` > `UIApplicationSupportsMultipleScenes` | `true` means the app can have two or more scenes (multiple windows on iPad, Catalyst, visionOS); iOS 13.0+ | [API] |
| `UIRequiresFullScreen` | iPad opt-out of multitasking and resizing; deprecated in iOS/iPadOS 26.0. On iPadOS 26+ the system keeps the scene size and scales the app rather than presenting it full screen | [API] |
| `UIDesignRequiresCompatibility` | Temporary opt-out of the OS 26 design (iOS, iPadOS, macOS, tvOS 26.0+); ignored when building for OS 27 or later | [API] |
| `WKApplication` (watchOS 7.0+), `WKWatchOnly`, `WKRunsIndependentlyOfCompanionApp` (watchOS 6.0+) | watchOS app; watch-only; runs without the iPhone app | [API] |
| `UIApplicationPreferredDefaultSceneSessionRole` (visionOS 1.0+) | visionOS app choosing its default scene role | [API] |
| `LSUIElement` | macOS agent app with no Dock icon (often a menu bar extra) | [API] |
| `UILaunchToFullScreenByDefaultOnMac` (macOS 12.1+) | iPad app tuned for running full screen on a Mac | [API] |

```bash
grep -rlE 'UIApplicationSceneManifest|WKApplication|LSUIElement|UIRequiresFullScreen|UIDesignRequiresCompatibility' --include='*.plist' --include='project.pbxproj' .
```

Source: https://developer.apple.com/documentation/bundleresources/information-property-list/minimumosversion, https://developer.apple.com/documentation/bundleresources/information-property-list/uirequiresfullscreen, https://developer.apple.com/documentation/bundleresources/information-property-list/uidesignrequirescompatibility, https://developer.apple.com/documentation/bundleresources/information-property-list/uiapplicationscenemanifest

## Classify the Mac and Apple Vision flavour

A "Mac app" or "Vision app" can be four different things with different design latitude. Decide which before advising.

| Flavour | How to recognise | What guidance applies |
|---|---|---|
| Native macOS (AppKit or SwiftUI, "Mac" destination) | macOS SDK/destination, `import AppKit`, `MACOSX_DEPLOYMENT_TARGET`, no `SUPPORTS_MACCATALYST` | Full macOS conventions: `references/platforms-macos.md` |
| Mac Catalyst, iPad idiom | `SUPPORTS_MACCATALYST = YES`, device family includes `2` but not `6` | UIKit app in the `.pad` idiom, scaled to the Mac display; must still add Mac menus, shortcuts, toolbar, context menus |
| Mac Catalyst, Mac idiom | `SUPPORTS_MACCATALYST = YES`, device family includes `6` | `.mac` idiom, unscaled points, AppKit-like controls; audit layout, fonts and images |
| iPad/iPhone app on Mac ("Designed for iPad") | `SUPPORTS_MAC_DESIGNED_FOR_IPHONE_IPAD = YES`, no Catalyst, no macOS target | Unmodified iOS binary on Apple silicon: design it as an iPad app (resizing, keyboard, pointer); no Mac-only UI is possible |
| Native visionOS | Apple Vision destination, device family `7`, visionOS-only APIs | `references/platforms-visionos.md` |
| Compatible iPad/iPhone app on Vision ("Designed for iPad") | `SUPPORTS_XR_DESIGNED_FOR_IPHONE_IPAD = YES`, no visionOS destination | Links the iOS SDK, keeps its iPadOS/iOS appearance in a window; apply iPad guidance and handle missing features |

- [API] Xcode's destination picker names these choices Mac, Mac Catalyst, Apple Vision and Designed for iPad; "Designed for iPad" is the default Mac/Vision destination type for iPad apps.
- [API] iPhone apps running on a Mac always get a fixed-size window; iPad apps that have not adopted multitasking do too.

Source: https://developer.apple.com/documentation/xcode/configuring-a-multiplatform-app-target, https://developer.apple.com/documentation/uikit/choosing-a-user-interface-idiom-for-your-mac-app, https://developer.apple.com/documentation/apple-silicon/running-your-ios-apps-in-macos, https://developer.apple.com/documentation/visionos/making-your-app-compatible-with-visionos

## Minimum OS version and why it gates advice

- [Conv] Find the deployment target per target (snippets above). When several targets or configurations disagree, use the lowest value that applies to the code being changed.
- [Conv] Anything introduced after the deployment target must be wrapped in an availability check with a working fallback, or not recommended at all. State the version next to each such API.
- [API] OS versions are year-aligned since 26: the release after iOS 18 / macOS 15 / watchOS 11 / tvOS 18 / visionOS 2 is version 26 on every platform; the current cycle is 27.

Availability anchors worth remembering (all read from documentation metadata on 2026-11-23):

| API or behaviour | Introduced |
|---|---|
| `NavigationSplitView` | iOS 16.0, macOS 13.0, tvOS 16.0, watchOS 9.0, visionOS 1.0 |
| `TabView` `.sidebarAdaptable` | iOS/iPadOS 18.0, macOS 15.0, tvOS 18.0, visionOS 2.0 |
| `TabView` `.verticalPage` | watchOS 10.0 |
| `handGestureShortcut(_:isEnabled:)` (double tap primary action) | watchOS 11.0, iOS 18.0, macOS 15.0, tvOS 18.0 |
| `glassEffect(_:in:)`, `GlassEffectContainer`, `buttonStyle(.glass)` (glass effect and glass button style) | 26.0 on iOS, iPadOS, macOS, tvOS, watchOS; no visionOS availability listed. Other OS 26 APIs do list visionOS 26: see `references/implementation-availability.md` |
| `TabBarMinimizeBehavior` | 26.0 |
| `UIRequiresFullScreen` | deprecated 26.0 |
| `ToolbarOverflowMenu` | iOS/iPadOS 27.0, visionOS 27.0 |
| `ToolbarItemVisibilityPriority` | iOS/iPadOS 27.0, macOS 26.1, tvOS 27.0, watchOS 27.0, visionOS 27.0 |
| `ArrangementView`, `ReservedRegion`, `ToolbarVerticalCompressionBehavior`, `UIArrangementViewController` | 27.1 |

- [API] Standard components pick up the OS 26 look when the app is built with the current SDK and run on OS 26 or later; on older OS versions the same code shows the older appearance. Do not promise Liquid Glass to a user whose deployment target and test device are below 26.
- [Conv] Design guidance is also era-dependent: describe floating glass bars for OS 26+, and say plainly when the project's minimum OS means some users will see the previous design.

Source: https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass, https://developer.apple.com/documentation/swiftui/arrangementview, https://developer.apple.com/documentation/swiftui/tabviewstyle/sidebaradaptable

## When the target is ambiguous

- [Conv] No codebase and no platform named: assume iPhone with the default minimum OS below (iOS 17), say so in one sentence, and continue. Ask a question only when the answer changes the deliverable materially (for example "Mac or iPad?" for a document editor).
- [Conv] Ask at most one question, and make it closed: "Is this for iPhone only, or iPhone and iPad?"
- [Conv] "Mac app" with UIKit code: check Catalyst settings before assuming AppKit conventions are reachable.
- [Conv] "Universal" or "multiplatform": enumerate the destinations found and treat iPhone and iPad as two layouts of one iOS target, not one layout.
- [Conv] Minimum OS neither stated nor discoverable (snippet, single file) and asking is not worthwhile: write for iOS 17 / macOS 14 / tvOS 17 / watchOS 10 / visionOS 1, state the assumption, and gate anything newer. Details: `references/implementation-availability.md`.
- [Conv] Always report: platforms detected, flavour (native, Catalyst idiom, Designed for iPad), minimum OS per platform, and which evidence produced each conclusion.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Universal versus platform-specific matrix

Universal on every platform [HIG]: use system components first; modality only when it helps and always with an obvious exit; one consistent search location; SF Symbols and semantic colors; never rely on color alone; every gesture has a visible alternative; verb-led, plain writing. Cells marked (syn) are synthesized from several pages or from the absence of platform notes, not stated in one place by Apple.

| Concern | iOS | iPadOS | macOS | watchOS | tvOS | visionOS |
|---|---|---|---|---|---|---|
| Primary navigation | Tab bar floating at the bottom; or a stack | Tab bar near the top, optionally sidebar-adaptable; or split view | Sidebar and split view; all commands in the menu bar | Vertical lists and vertical tab pages on the Digital Crown | Tab bar at the top, driven by focus | Vertical tab bar on the window's leading side |
| Secondary navigation | Push in a stack; segmented control | Split-view columns; segmented control | Split panes, tab views, outline views | Short detail pages (syn) | Split view for filtering; content rows (syn) | Sidebar inside a tab; split view |
| Action bar | Top toolbar (the former navigation bar) plus bottom toolbar | Top toolbar, can share the row with the tab bar | Window toolbar, customizable; subset of menu commands | Toolbar buttons in top corners or bottom | No tvOS-specific toolbar guidance (syn) | Toolbar ornament along the window's bottom edge |
| Modality | Sheets with detents, alerts, action sheets | Page/form sheets, popovers, alerts | Window-attached sheets, alerts, panels, detachable popovers | Full-screen sheet, alert, action sheet (4 buttons max) | Alerts, action sheets, full-screen views (syn) | Sheet centered in front of the window; no action sheets |
| Menus | Pull-down, pop-up, context, edit menus | Same plus menu bar and secondary click | Menu bar, context menus, Dock menu | No context or edit menus | Context menus; no edit menu, pop-up or pull-down buttons | Context menus; no menu bar (Command-key shortcut list) |
| Search | Search tab, bottom or top toolbar, or inline | Toolbar trailing side, sidebar top, or dedicated tab | Toolbar trailing side or sidebar top | Field opens full-screen text input | Dedicated search screen with keyboard and suggestions | General guidance only (syn) |
| Settings | In-app, minimal (syn) | In-app; App menu Settings opens the app's page in system Settings | Settings window from the App menu, Command-Comma | No custom entries in the Settings app; a few inline options | In-app (syn) | In-app (syn) |
| Focus and selection | Touch; no focus system | Touch, pointer effects, keyboard focus groups | Pointer, key window, keyboard | Touch and Crown; no focus system | Focus engine reaches every element | Eyes show hover effect, pinch selects; focus only with keyboard/controller |
| Text entry | Virtual keyboard | Virtual or hardware keyboard, Scribble | Hardware keyboard; no virtual keyboard | Dictation, Scribble, small keyboard; minimize | Linear remote keyboard; minimize | Virtual keyboard in its own window; hardware keyboard |
| Control size, default / minimum | 44 / 28 pt | 44 / 28 pt | 28 / 20 pt | 44 / 28 pt | 66 / 56 pt | 60 / 28 pt |
| Text size, default / minimum | 17 / 11 pt | 17 / 11 pt | 13 / 10 pt | 16 / 12 pt | 29 / 23 pt | 17 / 12 pt |
| Dynamic Type | Yes | Yes | No | Yes | Yes | Yes |
| Dark Mode | Yes | Yes | Yes | No | Yes | No (glass adapts to surroundings) |
| Windows | No | Yes, resizable, multiple | Yes, core model | No | No | Windows, volumes, immersive spaces |
| Multitasking | App switching, Picture in Picture; Split View on iPhone Duo inner display | Full screen or windowed, Picture in Picture | Always | Not supported | Picture in Picture | Shared Space |
| Liquid Glass (OS 26+) | Yes | Yes | Yes | Minimal, automatic | Yes, mostly on focus; Apple TV 4K (2nd generation) and newer | No glass effect or glass button style APIs (`glassEffect`, `buttonStyle(.glass)`); system glass material |
| Glanceable surfaces | Widgets (Home, Lock Screen, StandBy), Live Activities | Widgets, Live Activities | Widgets; iPhone Live Activities in the menu bar | Complications, Smart Stack widgets, Live Activities | Top Shelf; no widgets, no Live Activities | Widgets placed on surfaces; no Live Activities |

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility, https://developer.apple.com/design/human-interface-guidelines/typography, https://developer.apple.com/design/human-interface-guidelines/dark-mode, https://developer.apple.com/design/human-interface-guidelines/tab-bars, https://developer.apple.com/design/human-interface-guidelines/toolbars, https://developer.apple.com/design/human-interface-guidelines/windows, https://developer.apple.com/design/human-interface-guidelines/multitasking, https://developer.apple.com/design/human-interface-guidelines/widgets, https://developer.apple.com/design/human-interface-guidelines/settings

## Common mistakes

| Mistake | Fix |
|---|---|
| Assuming iPhone because the code says `os(iOS)` or `import UIKit` | Check `TARGETED_DEVICE_FAMILY`, Catalyst and "Designed for iPad" settings; `os(iOS)` covers iPad too |
| Treating "runs on Mac" as "Mac app" | Classify the flavour first; a Designed-for-iPad app cannot gain a Mac menu structure beyond what the iPad app defines |
| Recommending 26+ or 27.1 APIs without checking the deployment target | Read the deployment target, then guard with availability checks and give a fallback |
| Reading a missing `platforms:` in Package.swift as "all platforms, any version" | Treat as unspecified; look at the consuming app target |
| Looking for a Watch app inside the multiplatform target | watchOS is always a separate target; inspect it separately |
| Using the detected idiom to pick a layout | Platform decides conventions; size classes and available space decide layout |
| Silently guessing the platform | State the assumption and the evidence in one line |
| Asking several clarifying questions | Ask one closed question, or proceed on a stated assumption |
