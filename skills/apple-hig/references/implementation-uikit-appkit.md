# UIKit and AppKit implementation

Scope: when to stay in or drop to UIKit or AppKit, how to bridge to SwiftUI, and which UIKit and AppKit APIs carry HIG behavior (navigation, tabs, sheets, menus, text size, color, toolbars, windows), with a SwiftUI to UIKit to AppKit map.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- When to use UIKit or AppKit
- Bridging SwiftUI with UIKit and AppKit
- UIKit: navigation, titles, search
- UIKit: tabs and split views
- UIKit: sheets, alerts, menus
- UIKit: lists, cells, buttons
- UIKit: text size, color, traits, layout guides
- UIKit: keyboard, pointer, focus
- UIKit: Liquid Glass (OS 26+)
- AppKit: windows, toolbars, split views
- AppKit: menus and validation
- AppKit: appearance, color, materials, settings
- SwiftUI, UIKit, AppKit map
- Deprecated UIKit to avoid
- Common mistakes

Availability is `introducedAt` from the documentation data. UIKit entries are iOS and iPadOS unless a platform is named; AppKit entries are macOS.

## When to use UIKit or AppKit

- [Conv] Match the project. In a UIKit or AppKit codebase, fix and extend the existing framework code; do not rewrite a screen in SwiftUI unless asked.
- [Conv] In a SwiftUI codebase, drop down only when SwiftUI has no API for the need at the deployment target, and wrap the smallest piece (one view or one controller), not the screen.
- [Conv] Typical reasons to drop down: a collection layout SwiftUI cannot express, text-system customisation, an OS-version gap (for example sheet detents below iOS 16 through `UISheetPresentationController`, iOS 15), AppKit window, toolbar or menu behavior beyond the SwiftUI scene API.
- [HIG] The same HIG rules apply in every framework: system components first, semantic colors, text styles, safe areas, accessibility labels. Standard UIKit and AppKit components also adopt the current system appearance when built with the current SDK.
- [Conv] A wrapped UIKit or AppKit view keeps its own accessibility. Check labels, traits and Dynamic Type on the wrapped view itself.

Source: https://developer.apple.com/documentation/swiftui/uikit-integration , https://developer.apple.com/documentation/swiftui/appkit-integration , https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass

## Bridging SwiftUI with UIKit and AppKit

| Direction | API | Minimum OS |
|---|---|---|
| SwiftUI inside UIKit | `UIHostingController` (set `sizingOptions`, iOS 16, when the host must track content size) | iOS 13, tvOS 13 |
| SwiftUI inside a table or collection cell | `UIHostingConfiguration` assigned to `contentConfiguration` | iOS 16, tvOS 16 |
| SwiftUI inside AppKit | `NSHostingView`, `NSHostingController`; `NSHostingMenu` (macOS 14.4) | macOS 10.15 |
| UIKit inside SwiftUI | `UIViewRepresentable`, `UIViewControllerRepresentable` | iOS 13, tvOS 13 |
| AppKit inside SwiftUI | `NSViewRepresentable`, `NSViewControllerRepresentable` | macOS 10.15 |

- [Conv] When embedding a hosting controller, add it as a child view controller (`addChild(_:)`, add its view, `didMove(toParent:)`) so appearance, traits and safe areas propagate.
- [Conv] In a representable, create the view in `makeUIView(context:)` and push SwiftUI state into it in `updateUIView(_:context:)`; send changes back through a coordinator and a binding. Do not recreate the view on update.
- [Conv] Guard platform-only bridges with `#if canImport(UIKit)` or `#if os(macOS)` in multiplatform targets.

Source: https://developer.apple.com/documentation/swiftui/uihostingcontroller , https://developer.apple.com/documentation/swiftui/uihostingconfiguration , https://developer.apple.com/documentation/swiftui/nshostingview , https://developer.apple.com/documentation/swiftui/uiviewrepresentable

## UIKit: navigation, titles, search

- [API] Large titles: `UINavigationBar.prefersLargeTitles` and per-screen `UINavigationItem.largeTitleDisplayMode` (iOS 11). Set a `title` on every pushed controller.
- [API] `UINavigationItem.subtitle` is iOS 26; `UINavigationItem.style` and `titleMenuProvider` are iOS 16.
- [API] Search: assign a `UISearchController` to `navigationItem.searchController` (iOS 11); `hidesSearchBarWhenScrolling` (iOS 11) and `preferredSearchBarPlacement` (iOS 16) control where it sits.
- [HIG] Use the standard Back button and standard bar; avoid custom bar backgrounds and tinted bar items, which fight the system appearance (OS 26+).
- [API] Bar items: `UIBarButtonItem(systemItem:primaryAction:menu:)` (iOS 14) takes an action and a menu. `UIBarButtonItem.Style.done` is deprecated in iOS 26; use `.prominent` (iOS 26) for the one emphasised item.
- [HIG] Give every icon-only bar item an `accessibilityLabel` that names its action, and confirm it with VoiceOver.

Source: https://developer.apple.com/documentation/uikit/uinavigationitem , https://developer.apple.com/documentation/uikit/uisearchcontroller , https://developer.apple.com/design/human-interface-guidelines/toolbars , https://developer.apple.com/design/human-interface-guidelines/search-fields

## UIKit: tabs and split views

- [API] `UITab`, `UITabGroup` and `UISearchTab` (iOS 18, tvOS 18, visionOS 2): create each tab with `UITab(title:image:identifier:viewControllerProvider:)` and assign the array to `UITabBarController.tabs`.
- [API] `UITabBarController.mode` (iOS 18) decides whether iPad may show the tab bar as a sidebar (`.tabSidebar`); `UITabBarController.sidebar` (iOS 18) configures that sidebar.
- [API] `tabBarMinimizeBehavior` (iOS 26, tvOS 26, visionOS 26) and `bottomAccessory` (iOS 26) are the UIKit forms of the SwiftUI tab bar minimise and bottom accessory APIs.
- [HIG] Tabs navigate between sections; they do not run actions, and they are not hidden or disabled. On iPad the tab bar sits at the top and can become a sidebar.
- [API] `UISplitViewController(style:)` with `.doubleColumn` or `.tripleColumn` (iOS 14): set children with `setViewController(_:for:)`; the `.compact` column supplies what is shown when the split view collapses. An `.inspector` column exists from iOS 26.
- [API] A column-style split view wraps each child in a navigation controller, and a split view controller cannot be pushed onto a navigation stack. Make it the window's root.

Source: https://developer.apple.com/documentation/uikit/uitab , https://developer.apple.com/documentation/uikit/uitabbarcontroller , https://developer.apple.com/documentation/uikit/uisplitviewcontroller , https://developer.apple.com/design/human-interface-guidelines/tab-bars

## UIKit: sheets, alerts, menus

```swift
// iOS 15+. A resizable sheet with a visible grabber.
let filters = FilterViewController()
if let sheet = filters.sheetPresentationController {
    sheet.detents = [.medium(), .large()]
    sheet.prefersGrabberVisible = true
}
present(filters, animated: true)
```

- [API] `UISheetPresentationController` (iOS 15): `detents`, `prefersGrabberVisible`, `selectedDetentIdentifier`; custom heights with `Detent.custom(identifier:resolver:)` (iOS 16).
- [API] `isModalInPresentation` (iOS 13) blocks swipe-to-dismiss while there are unsaved changes.
- [HIG] Give the sheet's navigation item a Cancel item on the leading side and a Done or Save item on the trailing side; keep the grabber on resizable sheets.
- [API] `UIAlertController` (iOS 8) covers alerts (`.alert`) and action sheets (`.actionSheet`). Use `UIAlertAction` styles `.cancel` and `.destructive`; `preferredAction` (iOS 9) marks the default button.
- [HIG] Never make the destructive button the default; always include Cancel when an action can destroy data.
- [API] Menus: `UIMenu` and `UIAction` (iOS 13); attach with `UIButton.menu` and `showsMenuAsPrimaryAction` (iOS 14, tvOS 17) or `UIBarButtonItem.menu` (iOS 14). Mark destructive items with `UIMenuElement.Attributes.destructive`.
- [API] Context menus: `UIContextMenuInteraction` with `UIContextMenuConfiguration` (iOS 13, tvOS 17). Edit menus: `UIEditMenuInteraction` (iOS 16), replacing `UIMenuController`.
- [HIG] Everything in a context menu must also be reachable in the main interface; hide unavailable context-menu items instead of dimming them.

Source: https://developer.apple.com/documentation/uikit/uisheetpresentationcontroller , https://developer.apple.com/documentation/uikit/uialertcontroller , https://developer.apple.com/documentation/uikit/uimenu , https://developer.apple.com/design/human-interface-guidelines/sheets , https://developer.apple.com/design/human-interface-guidelines/context-menus

## UIKit: lists, cells, buttons

- [API] Lists: `UICollectionViewCompositionalLayout` (iOS 13) with `UICollectionLayoutListConfiguration` (iOS 14) and `UICollectionViewListCell`; `UITableView.Style.insetGrouped` (iOS 13) for grouped settings-style tables.
- [API] Cell content: get `defaultContentConfiguration()` (a `UIListContentConfiguration`, iOS 14), set `text`, `secondaryText` and `image`, and assign it to `contentConfiguration`. `UITableViewCell.textLabel` is deprecated. `UIBackgroundConfiguration` (iOS 14) styles the background.
- [API] Empty states: `UIContentUnavailableConfiguration` assigned to a view controller's `contentUnavailableConfiguration` (iOS 17).
- [API] Buttons: `UIButton(configuration:primaryAction:)` with `UIButton.Configuration` (iOS 15): `.filled()` for the single most likely action, `.bordered()` or plain styles for the rest. `contentEdgeInsets` is deprecated since iOS 15.
- [HIG] Keep the hit region at 44x44 pt or more on iPhone and iPad even when the visible button is smaller.

Source: https://developer.apple.com/documentation/uikit/uilistcontentconfiguration-swift.struct , https://developer.apple.com/documentation/uikit/uicollectionlayoutlistconfiguration-swift.struct , https://developer.apple.com/documentation/uikit/uibutton/configuration-swift.struct , https://developer.apple.com/design/human-interface-guidelines/buttons

## UIKit: text size, color, traits, layout guides

```swift
// System text style that follows Dynamic Type live.
label.font = UIFont.preferredFont(forTextStyle: .body)
label.adjustsFontForContentSizeCategory = true
label.numberOfLines = 0          // wrap instead of truncating
label.textColor = .label         // semantic color: adapts to Dark Mode and contrast

// Custom font scaled like a text style (iOS 11+).
let brand = UIFont(name: "Avenir-Medium", size: 17) ?? .systemFont(ofSize: 17)
label.font = UIFontMetrics(forTextStyle: .body).scaledFont(for: brand)

// iOS 17+: react to size-class or text-size changes without overriding a method.
registerForTraitChanges([UITraitHorizontalSizeClass.self, UITraitPreferredContentSizeCategory.self]) {
    (self: Self, previousTraitCollection: UITraitCollection) in
    self.updateLayout()
}
```

- [API] `adjustsFontForContentSizeCategory` (iOS 10) must be true for a label to update while the app is running. `UIFontMetrics.scaledValue(for:)` scales spacing and icon sizes.
- [API] `UIContentSizeCategory.isAccessibilityCategory` (iOS 11) is the cue to restack a row vertically. `minimumContentSizeCategory` and `maximumContentSizeCategory` (iOS 15) limit a subtree; use them only for bar-like chrome and add the Large Content Viewer (`showsLargeContentViewer`, `largeContentTitle`, iOS 13).
- [API] Semantic colors: `UIColor.label`, `.secondaryLabel`, `.separator`, `.link` (iOS 13, tvOS 13); `.systemBackground`, `.secondarySystemBackground`, `.systemGroupedBackground`, `.systemFill` (iOS 13; no tvOS entry). Custom adaptive colors: an asset-catalog color or `UIColor(dynamicProvider:)` (iOS 13).
- [API] Traits: `horizontalSizeClass`, `userInterfaceStyle`, `preferredContentSizeCategory`, `accessibilityContrast`, `legibilityWeight` on `UITraitCollection`. `traitCollectionDidChange(_:)` is deprecated since iOS 17; use `registerForTraitChanges(_:handler:)`.
- [HIG] Do not force an appearance with `overrideUserInterfaceStyle` app-wide; follow the system setting.
- [API] Layout guides: `safeAreaLayoutGuide` (iOS 11), `layoutMarginsGuide` and `readableContentGuide` (iOS 9), `keyboardLayoutGuide` (iOS 15). Pin content to these instead of to the screen edges or to fixed insets.
- [API] Do not size layout from `UIScreen.main` (deprecated in iOS 26); use the view's bounds, traits, or `UIWindowScene.effectiveGeometry` (iOS 16).

Source: https://developer.apple.com/documentation/uikit/uifontmetrics , https://developer.apple.com/documentation/uikit/uicontentsizecategoryadjusting/adjustsfontforcontentsizecategory , https://developer.apple.com/documentation/uikit/uitraitchangeobservable-67e94 , https://developer.apple.com/documentation/uikit/uicolor , https://developer.apple.com/documentation/uikit/uiview/safearealayoutguide , https://developer.apple.com/design/human-interface-guidelines/typography

## UIKit: keyboard, pointer, focus

- [API] Keyboard shortcuts: return `UIKeyCommand` objects from `keyCommands` (iOS 7), or build menu bar items in `buildMenu(with:)` using `UIMenuBuilder` (iOS 13), which fills the app's menu bar (including in Mac Catalyst apps).
- [HIG] Do not repurpose standard shortcuts; prefer Command as the main modifier for custom ones.
- [API] Pointer: `UIPointerInteraction` and `UIPointerStyle` (iOS 13.4); for `UIButton` prefer its built-in pointer support. `UIHoverStyle` (iOS 17) and `UIHoverGestureRecognizer` (iOS 13) cover hover.
- [API] Focus (tvOS, iPad keyboard): `UIFocusGuide` (iOS 9, tvOS 9) bridges gaps between focusable items.
- [HIG] Standard controls already respond to pointer, keyboard focus and Full Keyboard Access; add custom handling only for custom views.

Source: https://developer.apple.com/documentation/uikit/uikeycommand , https://developer.apple.com/documentation/uikit/uiresponder/buildmenu(with:) , https://developer.apple.com/documentation/uikit/uipointerinteraction , https://developer.apple.com/design/human-interface-guidelines/keyboards , https://developer.apple.com/design/human-interface-guidelines/pointing-devices

## UIKit: Liquid Glass (OS 26+)

- [API] `UIGlassEffect` and `UIGlassContainerEffect` (iOS 26, tvOS 26) are effects for `UIVisualEffectView`. `UIButton.Configuration.glass()` and `.prominentGlass()` (iOS 26, tvOS 26) are the glass button styles.
- [API] `UIScrollEdgeEffect` and `UIBackgroundExtensionView` (iOS 26, tvOS 26, visionOS 26); `UIBarButtonItem.sharesBackground` (iOS 26) controls grouping of bar items on a shared glass background.
- [HIG] Standard bars, tab bars and controls adopt the material automatically. Use the glass APIs only for a few custom controls in the navigation and control layer, never for content, and remove custom bar backgrounds.
- [Conv] Gate every glass API with `if #available(iOS 26, *)` and fall back to `UIBlurEffect` in a `UIVisualEffectView` or to a standard button configuration.

Source: https://developer.apple.com/documentation/uikit/uiglasseffect , https://developer.apple.com/documentation/uikit/uibutton/configuration-swift.struct/glass() , https://developer.apple.com/design/human-interface-guidelines/materials

## AppKit: windows, toolbars, split views

- [API] Toolbar: `NSToolbar` with `NSToolbarItem`; `NSSearchToolbarItem`, `NSTrackingSeparatorToolbarItem` and `NSWindow.toolbarStyle` are macOS 11. Standard identifiers include `.toggleSidebar`, `.sidebarTrackingSeparator` (macOS 11), `.toggleInspector` and `.inspectorTrackingSeparator` (macOS 14).
- [HIG] Make every toolbar item available as a menu bar command too, because people can hide or customise the toolbar; consider allowing customisation (`allowsUserCustomization`), but not in a settings window.
- [API] Sidebar and inspector: `NSSplitViewController` with `NSSplitViewItem(sidebarWithViewController:)`, `(contentListWithViewController:)` (macOS 10.11) and `(inspectorWithViewController:)` (macOS 11). `toggleSidebar(_:)` (macOS 10.11) and `toggleInspector(_:)` (macOS 14) are the standard actions to wire to menu items.
- [API] Window tabs: `NSWindow.tabbingMode`, `tabbingIdentifier` and the class property `allowsAutomaticWindowTabbing` (macOS 10.12). The default mode follows the person's system tabbing preference; leave it unless tabs make no sense for the window.
- [API] Title bar: `NSWindow.subtitle` (macOS 11), `titlebarAppearsTransparent`, `NSTitlebarAccessoryViewController` (macOS 10.10).
- [API] Sheets and alerts: `NSWindow.beginSheet(_:completionHandler:)` and `NSAlert.beginSheetModal(for:completionHandler:)` (macOS 10.9) attach a dialog to its window instead of blocking the whole app. `NSPopover` (macOS 10.7) for transient detail.
- [Conv] Let document and browser windows resize, set sensible minimum sizes, and restore size and position between launches (`setFrameAutosaveName(_:)`).

Source: https://developer.apple.com/documentation/appkit/nstoolbar , https://developer.apple.com/documentation/appkit/nssplitviewitem , https://developer.apple.com/documentation/appkit/nswindow , https://developer.apple.com/design/human-interface-guidelines/toolbars , https://developer.apple.com/design/human-interface-guidelines/windows

## AppKit: menus and validation

- [API] The menu bar is `NSApplication.mainMenu`, built from `NSMenu` and `NSMenuItem`; set `keyEquivalent` and `keyEquivalentModifierMask` for shortcuts.
- [API] Enable and disable items through validation rather than by hand: implement `validateMenuItem(_:)` (`NSMenuItemValidation`) or `validateUserInterfaceItem(_:)` (`NSUserInterfaceValidations`, which also covers toolbar items) on the object that handles the action. `NSMenu.autoenablesItems` drives this.
- [HIG] Keep unavailable menu bar items visible and dimmed so people can still discover them; keep a menu openable even when all its items are unavailable. Context menus are the exception: hide unavailable items there.
- [HIG] Put app-specific commands in the menu bar even when they exist elsewhere, follow the standard menu order (app menu, File, Edit, Format, View, app-specific, Window, Help), and keep standard shortcuts for standard commands.
- [API] Context menus: assign an `NSMenu` to the `menu` property a view inherits from `NSResponder`.

Source: https://developer.apple.com/documentation/appkit/nsmenu , https://developer.apple.com/documentation/appkit/nsmenuitemvalidation , https://developer.apple.com/documentation/appkit/nsuserinterfacevalidations , https://developer.apple.com/design/human-interface-guidelines/the-menu-bar , https://developer.apple.com/design/human-interface-guidelines/menus

## AppKit: appearance, color, materials, settings

- [API] Semantic colors: `NSColor.labelColor`, `.secondaryLabelColor`, `.tertiaryLabelColor`, `.linkColor` (macOS 10.10); `.textColor`, `.textBackgroundColor`, `.windowBackgroundColor`, `.controlBackgroundColor`; `.separatorColor`, `.controlAccentColor`, `.selectedContentBackgroundColor` (macOS 10.14). Custom adaptive colors: asset catalog or `NSColor(name:dynamicProvider:)` (macOS 10.15).
- [API] Appearance: `NSAppearance`; `NSApplication.appearance` (macOS 10.14) overrides the app's appearance. Leave it nil to follow the system.
- [API] Text: `NSFont.preferredFont(forTextStyle:options:)` (macOS 11) gives text styles. [HIG] macOS has no Dynamic Type; the default text size is 13 pt and the minimum 10 pt.
- [API] Symbols: `NSImage(systemSymbolName:accessibilityDescription:)` (macOS 11); the description is what VoiceOver reads for a meaningful image.
- [API] Materials: `NSVisualEffectView` (macOS 10.10) with a semantic `material` such as `.sidebar`; choose by purpose, not by apparent color.
- [API] Liquid Glass (macOS 26): `NSGlassEffectView`, `NSGlassEffectContainerView`, `NSBackgroundExtensionView`, and `NSButton.BezelStyle.glass`. Gate with `if #available(macOS 26, *)`.
- [HIG] Settings: open a dedicated settings window from the app menu's Settings item (Command-Comma). Use a noncustomisable toolbar whose buttons switch panes, show the active pane, and dim the minimise and zoom buttons. Do not put a settings button in a main window's toolbar.
- [Conv] An AppKit settings window is commonly an `NSTabViewController` with `tabStyle = .toolbar` (macOS 10.10) as the window's content view controller. In SwiftUI use the `Settings` scene (macOS 11).

Source: https://developer.apple.com/documentation/appkit/nscolor , https://developer.apple.com/documentation/appkit/nsvisualeffectview , https://developer.apple.com/documentation/appkit/nsglasseffectview , https://developer.apple.com/documentation/appkit/nstabviewcontroller , https://developer.apple.com/design/human-interface-guidelines/settings , https://developer.apple.com/design/human-interface-guidelines/typography

## SwiftUI, UIKit, AppKit map

| Need | SwiftUI | UIKit | AppKit |
|---|---|---|---|
| Push navigation | `NavigationStack` | `UINavigationController` | Usually a split view or window per task |
| Sidebar plus detail | `NavigationSplitView` | `UISplitViewController(style:)` | `NSSplitViewController` with sidebar item |
| Tabs | `TabView` + `Tab` | `UITabBarController` + `UITab` | `NSTabViewController` (panes), not top-level navigation |
| Toolbar items | `toolbar` + `ToolbarItem` | `UIBarButtonItem` on `navigationItem` | `NSToolbar` + `NSToolbarItem` |
| Search | `searchable` | `UISearchController` | `NSSearchToolbarItem`, `NSSearchField` |
| Sheet | `sheet` + `presentationDetents` | `UISheetPresentationController` | `beginSheet(_:completionHandler:)` |
| Alert, confirmation | `alert`, `confirmationDialog` | `UIAlertController` | `NSAlert` |
| Popover | `popover` | `UIPopoverPresentationController` | `NSPopover` |
| Inspector | `inspector` | `UISplitViewController` inspector column (iOS 26) | `NSSplitViewItem(inspectorWithViewController:)` |
| Menu on a control | `Menu` | `UIButton.menu` + `UIMenu` | `NSPopUpButton`, `NSMenuToolbarItem` |
| Context menu | `contextMenu` | `UIContextMenuInteraction` | `menu` property |
| Menu bar commands | `commands`, `CommandMenu` | `buildMenu(with:)` | `NSApplication.mainMenu` |
| List | `List` | `UICollectionView` list layout, `UITableView` | `NSTableView`, `NSOutlineView` |
| Empty state | `ContentUnavailableView` | `UIContentUnavailableConfiguration` | Custom view; no dedicated class found |
| Toggle, slider, stepper | `Toggle`, `Slider`, `Stepper` | `UISwitch`, `UISlider`, `UIStepper` | `NSSwitch` or checkbox `NSButton`, `NSSlider`, `NSStepper` |
| Text style font | `Font.body` | `UIFont.preferredFont(forTextStyle:)` | `NSFont.preferredFont(forTextStyle:options:)` |
| Label color | `.primary`, `.secondary` | `UIColor.label`, `.secondaryLabel` | `NSColor.labelColor`, `.secondaryLabelColor` |
| Size class | `\.horizontalSizeClass` | `traitCollection.horizontalSizeClass` | Window size; no size classes |
| Glass on a custom control (OS 26) | `glassEffect(_:in:)` | `UIGlassEffect` | `NSGlassEffectView` |
| Settings | `Settings` scene (macOS) | Settings bundle or in-app screen | Settings window |

Source: https://developer.apple.com/documentation/swiftui , https://developer.apple.com/documentation/uikit , https://developer.apple.com/documentation/appkit

## Deprecated UIKit to avoid

- [API] `UIScreen.main` (iOS 26), `UIApplication.keyWindow` (iOS 13) and `.windows` (iOS 15), `statusBarOrientation` (iOS 13), `traitCollectionDidChange(_:)` (iOS 17), `UIButton.contentEdgeInsets` (iOS 15), `UIBarButtonItem.Style.done` (iOS 26), `UIMenuController` (iOS 16), `topLayoutGuide` and `automaticallyAdjustsScrollViewInsets` (iOS 11), `UIAlertView`, `UIActionSheet`, `UIPopoverController`, `UISearchDisplayController`, `UIWebView`.
- [API] `UITableViewCell.textLabel` and `UIAccessibility.buttonShapesEnabled` are deprecated in the OS 26 to 27 cycle. Replacements for all of these are in `references/implementation-availability.md`.

Source: https://developer.apple.com/documentation/uikit/uiscreen/main , https://developer.apple.com/documentation/uikit/uitableviewcell/textlabel

## Common mistakes

- Rewriting a UIKit screen in SwiftUI to fix one HIG issue -> fix it in UIKit.
- `UIFont.systemFont(ofSize:)` for body text -> `preferredFont(forTextStyle:)` plus `adjustsFontForContentSizeCategory = true`.
- Custom font with a fixed size -> `UIFontMetrics.scaledFont(for:)`.
- `UIColor.black`, `.white` or hex values for text and backgrounds -> semantic colors or asset colors with dark and high-contrast variants.
- Constraints pinned to the superview edges -> `safeAreaLayoutGuide`, `layoutMarginsGuide`, `readableContentGuide`.
- Layout from `UIScreen.main.bounds` or device idiom -> traits and the view's own bounds.
- `cell.textLabel?.text = ...` -> `defaultContentConfiguration()`.
- Custom tab bar or custom modal view -> `UITabBarController`, `UISheetPresentationController`, `UIAlertController`.
- Icon-only `UIButton` or bar item with no `accessibilityLabel` -> set one.
- Mac window with a toolbar but no matching menu bar commands, or menu items enabled by hand -> add menu items and implement validation.
- An iOS-style settings screen inside the main Mac window -> a settings window opened from the app menu.
- Glass effect views behind content or lists -> standard materials for content; glass only for custom controls, gated to OS 26.
