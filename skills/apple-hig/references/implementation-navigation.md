# SwiftUI navigation, tabs, toolbars, search and presentations

Scope: which SwiftUI container and presentation API to use, with verified minimum OS versions, platform gaps and short patterns. Design guidance is in `references/components-navigation.md` and `references/components-presentation.md`.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Reading availability
- Choosing a container
- NavigationStack
- NavigationSplitView
- TabView and Tab
- Toolbars and titles
- Search
- Presentations: API minimums and platform gaps
- Sheets, covers, popovers, inspectors
- Alerts and confirmation dialogs
- Common mistakes

## Reading availability

- [API] Availability below is `metadata.platforms[].introducedAt` from the documentation JSON. A platform that is not listed has no availability entry; treat the API as unavailable there and guard with `#if os(...)`.
- [API] Apple's documentation merges overloads onto one page and the landing page often shows the newest overload. Example: `alert(_:isPresented:actions:message:)` shows iOS 16 (the `LocalizedStringResource` overload) although the `LocalizedStringKey` and `StringProtocol` overloads are iOS 15. Minimums here are for the oldest overload; do not conclude a newer minimum from the landing page.
- [API] Many long-standing spellings (`NavigationView`, `tabItem(_:)`, `.navigationBarLeading`, `Alert`, `ActionSheet`, `toolbar(_:for:)` visibility) are now marked deprecated. They remain correct inside an `#available` fallback branch for older systems. See `references/implementation-availability.md`.
- [Conv] Nothing in this file was compiled. Build before claiming it works. `HomeView`, `Recipe` and similar names are placeholders.

Source: https://developer.apple.com/documentation/swiftui/navigation, https://developer.apple.com/documentation/swiftui/view

## Choosing a container

| App structure | Use | Minimum |
|---|---|---|
| One column, drill down and back | `NavigationStack` | iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+ |
| Sidebar or list plus detail (2 or 3 columns) | `NavigationSplitView` | same as `NavigationStack` |
| A few peer top-level sections | `TabView` with `Tab` | `Tab`: iOS 18+, macOS 15+, tvOS 18+, watchOS 11+, visionOS 2+ |
| Peer sections plus groups or collections, mainly iPad | `TabView` + `.tabViewStyle(.sidebarAdaptable)` + `TabSection` | iOS 18+, macOS 15+, tvOS 18+, visionOS 2+ (style not on watchOS) |
| Supplementary properties of the current selection | `inspector(isPresented:content:)` | iOS 17+, macOS 14+ only |

- [API] `NavigationSplitView` collapses all columns into one stack on watchOS, tvOS and at narrow sizes (iPhone, iPad in Slide Over). One split view therefore covers "stack when compact, columns when regular" without a size-class branch.
- [API] A `NavigationStack` can be embedded in a split-view column; links in an earlier column then replace that stack's root.
- [Conv] Give each tab its own `NavigationStack` so every tab keeps its own navigation state.
- [HIG] Tabs navigate between sections and toolbars act on the current view; do not put actions in tabs.

Source: https://developer.apple.com/documentation/swiftui/navigationsplitview, https://developer.apple.com/documentation/swiftui/navigationstack, https://developer.apple.com/documentation/swiftui/tabview, https://developer.apple.com/design/human-interface-guidelines/tab-bars

## NavigationStack

```swift
// iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+
struct RecipeList: View {
    let recipes: [Recipe]                      // Recipe: Identifiable, Hashable
    @State private var path = NavigationPath()
    var body: some View {
        NavigationStack(path: $path) {
            List(recipes) { recipe in
                NavigationLink(recipe.name, value: recipe)
            }
            .navigationTitle("Recipes")
            .navigationDestination(for: Recipe.self) { recipe in
                RecipeDetail(recipe: recipe)
            }
        }
    }
}
```

- [API] Push programmatically with `path.append(value)`; pop with `path.removeLast()`. `NavigationPath` is type-erased; a typed array of `Hashable` values also works as the path.
- [API] `navigationDestination(for:destination:)` and `navigationDestination(isPresented:destination:)` are iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+. `navigationDestination(item:destination:)` is newer: iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+.
- [API] `NavigationLink(destination:isActive:label:)` and the `tag:selection:` form are deprecated since iOS 16. Use value links with `navigationDestination`.
- [API] Dismiss from inside a pushed or presented view with `@Environment(\.dismiss)` (iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+).

Source: https://developer.apple.com/documentation/swiftui/navigationstack, https://developer.apple.com/documentation/swiftui/navigationpath, https://developer.apple.com/documentation/swiftui/navigationlink

## NavigationSplitView

```swift
// iOS 16+, macOS 13+, visionOS 1+ (also tvOS 16+ and watchOS 9+, where it shows as a stack)
struct LibraryView: View {
    let folders: [Folder]                      // Folder: Identifiable, Hashable
    @State private var selectedID: Folder.ID?
    var body: some View {
        NavigationSplitView {
            List(folders, selection: $selectedID) { folder in
                Label(folder.name, systemImage: "folder")
            }
            .navigationTitle("Library")
        } detail: {
            if let folder = folders.first(where: { $0.id == selectedID }) {
                FolderDetail(folder: folder)
            } else {
                Text("Select a folder").foregroundStyle(.secondary)
            }
        }
    }
}
```

- [API] Three columns: `NavigationSplitView { sidebar } content: { list } detail: { detail }`. Control visibility with `init(columnVisibility:...)` and `NavigationSplitViewVisibility`; the split view ignores that control while collapsed.
- [API] When collapsed, choose the column shown on top with `init(preferredCompactColumn:sidebar:detail:)`.
- [API] `navigationSplitViewColumnWidth(_:)` and `navigationSplitViewStyle(_:)` are iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+.
- [API] `List` selection initializers list no watchOS availability; on watchOS use `NavigationLink` rows instead.
- [HIG] Always show a placeholder in an empty detail column rather than a blank pane.

Source: https://developer.apple.com/documentation/swiftui/navigationsplitview, https://developer.apple.com/design/human-interface-guidelines/split-views

## TabView and Tab

```swift
// Tab: iOS 18+, macOS 15+, tvOS 18+, watchOS 11+, visionOS 2+. Older systems take the else branch.
struct RootView: View {
    var body: some View {
        if #available(iOS 18, macOS 15, tvOS 18, watchOS 11, visionOS 2, *) {
            TabView {
                Tab("Home", systemImage: "house") { HomeView() }
                Tab("Library", systemImage: "books.vertical") { LibraryView() }
                Tab("Search", systemImage: "magnifyingglass", role: .search) { SearchView() }
            }
        } else {
            TabView {
                // Fallback for iOS 17 and earlier: tabItem is deprecated but correct here.
                HomeView().tabItem { Label("Home", systemImage: "house") }
                LibraryView().tabItem { Label("Library", systemImage: "books.vertical") }
                SearchView().tabItem { Label("Search", systemImage: "magnifyingglass") }
            }
        }
    }
}
```

| API | Availability | Notes |
|---|---|---|
| `Tab`, `TabSection`, `TabView(selection:content:)` with `Tab(_:systemImage:value:content:)` | iOS 18+, macOS 15+, tvOS 18+, watchOS 11+, visionOS 2+ | The older `TabView(selection:)` + `.tag` form is deprecated. |
| `TabRole.search` | same as `Tab` | [API] A searchable tab view prefers the first tab with this role to implement search. |
| `TabRole.prominent` | OS 27+ on all platforms | One tab gets a prominent treatment; without it a search tab may get it. |
| `.tabViewStyle(.sidebarAdaptable)`, `.tabBarOnly` | iOS 18+, macOS 15+, tvOS 18+, visionOS 2+; not on watchOS | iPadOS: top tab bar that can become a sidebar. iOS: bottom tab bar. macOS and tvOS: sidebar. visionOS: ornament, plus a sidebar for `TabSection` tabs. |
| `tabViewCustomization(_:)` | iOS 18+, macOS 15+, visionOS 2+ | People can reorder and hide sidebar tabs. |
| `.tabViewStyle(.page)` / `.verticalPage` | page: iOS 14+, tvOS 14+, watchOS 7+, visionOS 1+ (not macOS); verticalPage: watchOS 10+ only | Paged content, not top-level navigation. |
| `tabBarMinimizeBehavior(_:)` | modifier: OS 26+ on all platforms; `.onScrollDown` value: iOS 26+ only | Tab bar shrinks while scrolling down. |
| `tabViewBottomAccessory(content:)` | iOS 26+ only; `isEnabled:` variant iOS 26.1+ | Accessory above the tab bar; inline when the bar is minimized. Read `\.tabViewBottomAccessoryPlacement` to adapt. |
| `badge(_:)` on a tab | iOS 18+, macOS 15+, visionOS 2+ | |

```swift
// iOS 26+ only: wrap in #if os(iOS) and #available(iOS 26, *) in multiplatform code.
TabView {
    Tab("Feed", systemImage: "list.bullet") { FeedView() }
    Tab("Saved", systemImage: "bookmark") { SavedView() }
}
.tabBarMinimizeBehavior(.onScrollDown)
.tabViewBottomAccessory { NowPlayingBar() }
```

- [HIG] Do not hide or disable tabs, and avoid overflowing into a More tab. The HIG gives no fixed tab count.
- [Conv] Do not build a tab bar from an `HStack` of buttons: `TabView` supplies the OS 26 glass appearance, sidebar adaptation, the search role and accessibility traits.

Source: https://developer.apple.com/documentation/swiftui/tabview, https://developer.apple.com/documentation/swiftui/tab, https://developer.apple.com/documentation/swiftui/tabrole, https://developer.apple.com/documentation/swiftui/tabbarminimizebehavior, https://developer.apple.com/design/human-interface-guidelines/tab-bars

## Toolbars and titles

| Placement | Availability | Where the system puts it |
|---|---|---|
| `.automatic`, `.primaryAction` | iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+ | primaryAction: trailing edge of the bar on iOS, iPadOS, tvOS; leading edge of the toolbar on macOS; beneath the bar (revealed by scrolling) on watchOS. |
| `.confirmationAction` | same | Modal confirm button. iOS, iPadOS, tvOS: same spot as primaryAction. macOS: trailing-most in the sheet. watchOS: trailing edge. |
| `.cancellationAction` | same | iOS, iPadOS, tvOS, watchOS: leading edge. macOS: trailing edge, before confirmation items. |
| `.destructiveAction` | same | |
| `.principal`, `.navigation` | iOS 14+, macOS 11+, tvOS 14+, visionOS 1+; not on watchOS | |
| `.secondaryAction` | iOS 16+, macOS 13+, visionOS 1+ | Overflow-eligible actions. |
| `.topBarLeading`, `.topBarTrailing` | iOS 14+ (back-deployed), tvOS 14+, watchOS 10+, visionOS 1+; not on macOS | Replace the deprecated `.navigationBarLeading` / `.navigationBarTrailing`. |
| `.bottomBar` | iOS 14+, tvOS 18+, watchOS 10+, visionOS 1+; not on macOS | |
| `.keyboard` | iOS 15+, macOS 12+ | Bar above the software keyboard. |
| `.topBarPinnedTrailing` | iOS 27+, visionOS 27+ | Stays visible while other items overflow. |

```swift
// iOS 14+, macOS 11+, tvOS 14+, watchOS 7+, visionOS 1+
List(messages) { MessageRow(message: $0) }
    .navigationTitle("Inbox")
    .toolbar {
        ToolbarItem(placement: .primaryAction) {
            Button { isComposing = true } label: {
                Label("Compose", systemImage: "square.and.pencil")
            }
        }
        ToolbarItemGroup(placement: .secondaryAction) {   // iOS 16+, macOS 13+
            Button("Select", systemImage: "checkmark.circle") { isSelecting = true }
            Button("Filter", systemImage: "line.3.horizontal.decrease") { showsFilter = true }
        }
    }
```

- [API] Prefer semantic placements; the system positions them per platform. Use `.topBar...` only for an explicit side, inside `#if !os(macOS)`.
- [API] Use `Label` (or `Button(_:systemImage:action:)`) for bar items: the toolbar shows the icon and assistive technologies get the title.
- [API] `ToolbarSpacer(_:placement:)` with `.fixed` or `.flexible` sizing is iOS 26+, macOS 26+ only; it separates groups of bar items. `DefaultToolbarItem(kind:placement:)` is OS 26+ on all platforms.
- [API] Titles: `navigationTitle(_:)` is iOS 14+, macOS 11+, tvOS 14+, watchOS 7+. `navigationBarTitleDisplayMode(_:)` is iOS 14+, watchOS 8+, visionOS 1+ and does not exist on macOS or tvOS. `toolbarTitleDisplayMode(_:)` is iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+; its `.large` value is not on macOS or tvOS and `.inlineLarge` is not on tvOS or watchOS. `navigationSubtitle(_:)` is macOS 13+ and iOS 26+.
- [API] Hide a bar with `toolbarVisibility(_:for:)` (iOS 18+, macOS 15+, tvOS 18+, watchOS 11+, visionOS 2+). Below that, the deprecated `toolbar(_:for:)` visibility form (iOS 16+) is the fallback.
- [HIG] Reduce custom toolbar backgrounds and tinted bar items (OS 26+, Liquid Glass); keep the title short and use standard Back and Close buttons.

Source: https://developer.apple.com/documentation/swiftui/toolbaritemplacement, https://developer.apple.com/documentation/swiftui/toolbaritem, https://developer.apple.com/documentation/swiftui/toolbarspacer, https://developer.apple.com/documentation/swiftui/toolbartitledisplaymode, https://developer.apple.com/design/human-interface-guidelines/toolbars

## Search

```swift
// searchable: iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+
// searchScopes and searchSuggestions: iOS 16+, macOS 13+ (scopes not on watchOS; tvOS 16.4+)
// ContentUnavailableView: iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+
List(results) { Text($0.name) }
    .navigationTitle("Contacts")
    .searchable(text: $query, prompt: "Search contacts")
    .searchScopes($scope) {
        Text("All").tag(Scope.all)
        Text("Favorites").tag(Scope.favorites)
    }
    .searchSuggestions {
        ForEach(recentQueries, id: \.self) { Text($0).searchCompletion($0) }
    }
    .overlay {
        if results.isEmpty && !query.isEmpty { ContentUnavailableView.search(text: query) }
    }
```

- [API] `SearchFieldPlacement`: `.automatic`; `.toolbar` (iOS 15+, macOS 12+, watchOS 8+, visionOS 1+, not tvOS); `.sidebar` (iOS 15+, macOS 12+, visionOS 1+); `.navigationBarDrawer` (iOS 15+, watchOS 8+, visionOS 1+, not macOS).
- [API] `searchable(text:isPresented:placement:prompt:)` is iOS 17+, macOS 14+, visionOS 1+. `\.isSearching` and `\.dismissSearch` are iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+.
- [API] Search tab: give one tab `role: .search` and make the tab view searchable; the tab view prefers the first search-role tab to implement search. `searchToolbarBehavior(_:)` (OS 26+) adjusts a toolbar search field, for example `.minimized` on iPhone.
- [Unverified] Whether `searchable` should sit on the `TabView` or inside the search tab's `NavigationStack` for a given layout; the documentation wording implies the tab view. Build and check both placements on the target OS.
- [HIG] Use the standard search field rather than a `TextField` with a magnifier icon, and show a clear "no results" state.

Source: https://developer.apple.com/documentation/swiftui/searchfieldplacement, https://developer.apple.com/documentation/swiftui/tabrole, https://developer.apple.com/documentation/swiftui/contentunavailableview, https://developer.apple.com/design/human-interface-guidelines/search-fields

## Presentations: API minimums and platform gaps

A dash means the documentation lists no availability for that platform.

| API | iOS | macOS | tvOS | watchOS | visionOS |
|---|---|---|---|---|---|
| `sheet(isPresented:onDismiss:content:)`, `sheet(item:...)` | 13 | 10.15 | 13 | 6 | 1 |
| `presentationDetents(_:)`, `presentationDragIndicator(_:)` | 16 | 13 | 16 | 9 | 1 |
| `presentationBackgroundInteraction(_:)`, `presentationCompactAdaptation(_:)`, `presentationBackground(_:)` | 16.4 | 13.3 | 16.4 | 9.4 | 1 |
| `presentationSizing(_:)` | 18 | 15 | 18 | 11 | 2 |
| `interactiveDismissDisabled(_:)` | 15 | 12 | 15 | 8 | 1 |
| `fullScreenCover(isPresented:onDismiss:content:)`, `fullScreenCover(item:...)` | 14 | - | 14 | 7 | 1 |
| `popover(isPresented:attachmentAnchor:arrowEdge:content:)`, `popover(item:...)` | 13 | 10.15 | - | - | 1 |
| `inspector(isPresented:content:)`, `inspectorColumnWidth(_:)` | 17 | 14 | - | - | - |
| `alert(_:isPresented:actions:message:)`, `alert(_:isPresented:presenting:actions:message:)` | 15 | 12 | 15 | 8 | 1 |
| `confirmationDialog(_:isPresented:titleVisibility:actions:message:)` | 15 | 12 | 15 | 8 | 1 |
| `dismissalConfirmationDialog(_:shouldPresent:actions:)` | 27 | 15 | - | - | - |

- [API] `Alert`, `alert(isPresented:content:)`, `ActionSheet` and `actionSheet(isPresented:content:)` are deprecated; use the rows above.
- [API] Being listed for a platform does not mean the modifier changes anything there. [Unverified] Detents are documented without a per-platform behaviour note; test on each platform you ship.

Source: https://developer.apple.com/documentation/swiftui/modal-presentations, https://developer.apple.com/documentation/swiftui/presentationdetent, https://developer.apple.com/documentation/swiftui/presentationadaptation

## Sheets, covers, popovers, inspectors

```swift
// iOS 16+, macOS 13+, tvOS 16+, watchOS 9+, visionOS 1+
struct FilterSheet: View {
    @Environment(\.dismiss) private var dismiss
    @State private var onlyUnread = false
    var body: some View {
        NavigationStack {
            Form { Toggle("Unread Only", isOn: $onlyUnread) }
                .navigationTitle("Filters")
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) { Button("Cancel") { dismiss() } }
                    ToolbarItem(placement: .confirmationAction) { Button("Done") { dismiss() } }
                }
        }
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
    }
}
// Present with: .sheet(isPresented: $showsFilters) { FilterSheet() }
```

- [API] `presentationDetents(_:)` takes a `Set<PresentationDetent>`: `.medium`, `.large`, `.fraction(_:)`, `.height(_:)`. Apply it to the sheet's content, not to the presenting view.
- [API] A sheet over a vertically compact view uses a full-screen appearance by default. On iPhone a popover adapts into a sheet, and into a full-screen cover when vertically compact; override with `presentationCompactAdaptation(_:)` (for example `.popover` or `.none`).
- [API] An inspector presents as a trailing column in a horizontally regular size class and can adapt to a sheet when compact.
- [API] `fullScreenCover` has no macOS availability; on macOS use a sheet or a separate window.
- [API] Block swipe-to-dismiss while there are unsaved edits with `interactiveDismissDisabled(_:)`.
- [HIG] In iOS and iPadOS put Cancel on the leading edge and Done on the trailing edge of the sheet's top toolbar; pair Done with Cancel or Back, and never show Cancel, Done and Back together.
- [HIG] Reserve full-screen covers for immersive or multistep tasks and always give a visible way out.

Source: https://developer.apple.com/documentation/swiftui/presentationdetent, https://developer.apple.com/documentation/swiftui/presentationadaptation, https://developer.apple.com/design/human-interface-guidelines/sheets, https://developer.apple.com/design/human-interface-guidelines/popovers, https://developer.apple.com/design/human-interface-guidelines/modality

## Alerts and confirmation dialogs

```swift
// iOS 15+, macOS 12+, tvOS 15+, watchOS 8+, visionOS 1+
Button("Delete Draft", role: .destructive) { isConfirmingDelete = true }
    .confirmationDialog("Delete this draft?", isPresented: $isConfirmingDelete, titleVisibility: .visible) {
        Button("Delete Draft", role: .destructive) { deleteDraft() }
        Button("Cancel", role: .cancel) { }
    } message: {
        Text("This action can't be undone.")
    }
    .alert("Couldn't Save", isPresented: $showsSaveError, presenting: saveError) { _ in
        Button("Try Again") { save() }
        Button("Cancel", role: .cancel) { }
    } message: { error in
        Text(error.localizedDescription)
    }
```

- [API] Every action dismisses the dialog after it runs. A button with `role: .cancel` replaces the default dismiss action. The system may reorder buttons by role.
- [API] In regular size classes on iOS a confirmation dialog renders as a popover anchored to the view it is attached to, so attach it to the control that triggered it.
- [API] On iOS, tvOS and watchOS, confirmation dialogs support only controls whose labels are `Text`; other content is omitted.
- [HIG] Use alerts sparingly; do not alert for common, undoable actions even when destructive. Never give a destructive button the default (primary) role, and include Cancel when a choice is destructive.
- [HIG] Use a confirmation dialog (action sheet) for choices related to an action the person just started, not for general menus; use `Menu` for those.

Source: https://developer.apple.com/documentation/swiftui/buttonrole, https://developer.apple.com/documentation/swiftui/modal-presentations, https://developer.apple.com/design/human-interface-guidelines/alerts, https://developer.apple.com/design/human-interface-guidelines/action-sheets

## Common mistakes

| Mistake | Fix |
|---|---|
| `NavigationView` or `NavigationLink(destination:isActive:)` in new code | `NavigationStack` / `NavigationSplitView` with value links (iOS 16+); keep the old form only in a fallback branch. |
| Branching on device idiom to choose stack or split view | Use `NavigationSplitView`; it collapses by itself at narrow widths. |
| Assuming `navigationDestination(item:)` is iOS 16 | It is iOS 17+; on 16 use `navigationDestination(isPresented:)` or a path. |
| `Tab` used with an iOS 17 deployment target and no guard | `#available(iOS 18, *)` with a `tabItem` fallback. |
| `.navigationBarLeading` / `.navigationBarTrailing` | `.topBarLeading` / `.topBarTrailing`, or semantic placements. |
| `navigationBarTitleDisplayMode` in shared macOS or tvOS code | Wrap in `#if os(iOS)` or use `toolbarTitleDisplayMode` (iOS 17+, macOS 14+). |
| Icon-only toolbar button built from a bare `Image` | `Label("Compose", systemImage: ...)` so VoiceOver and tooltips get a name. |
| Custom dimmed `ZStack` overlay as an alert or sheet | `alert`, `confirmationDialog`, `sheet`, `popover`. |
| Sheet with Done but no Cancel, or no way out | `.cancellationAction` and `.confirmationAction` toolbar items. |
| `fullScreenCover` or `popover` in code shared with macOS, tvOS or watchOS | Check the gap table; guard with `#if os(...)` and present a sheet instead. |
| Custom search bar | `searchable`, a search-role tab, `ContentUnavailableView.search`. |
