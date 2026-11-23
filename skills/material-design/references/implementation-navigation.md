# Structure and navigation in Compose

Scope: Compose Material 3 code for app structure: `Scaffold` and its padding, top app bars and scroll behaviors, navigation bar, rail and drawers, `NavigationSuiteScaffold`, tabs, the search bar, window size classes and adaptive pane scaffolds, navigation libraries, Back and predictive back, edge-to-edge and window insets.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Scaffold and innerPadding
- Top app bars and scroll behaviors
- Navigation bar, rail and drawers
- NavigationSuiteScaffold
- Tabs
- Search bar
- Window size classes
- Adaptive pane scaffolds
- Navigation libraries
- Back and predictive back
- Edge-to-edge and window insets
- Common mistakes

## Scaffold and innerPadding

- [API] `Scaffold(modifier, topBar, bottomBar, snackbarHost, floatingActionButton, floatingActionButtonPosition, containerColor, contentColor, contentWindowInsets, content: (PaddingValues) -> Unit)` is stable. It has no drawer and no scaffold state (those were Material 2).
- [API] The `content` lambda receives `PaddingValues` that cover the bars and `contentWindowInsets`. Content that ignores them is drawn under the top bar, the bottom bar and the system bars.
- [Conv] Scrolling content: pass the padding as `contentPadding = innerPadding` to `LazyColumn` so items scroll behind the bars but rest clear of them. Non-scrolling content: `Modifier.padding(innerPadding)`.
- [API] Add `Modifier.consumeWindowInsets(innerPadding)` on the content so nested inset modifiers (`imePadding()`, `safeDrawingPadding()`) do not apply the same insets twice.
- [Conv] One `Scaffold` per screen. Snackbars go in `snackbarHost`, the FAB in `floatingActionButton`; do not overlay them with your own `Box`. Worked example: `examples/SettingsScreen.kt`.

```kotlin
// material3 1.4+; no opt-in. Not compiled.
Scaffold(
    topBar = { TopAppBar(title = { Text(stringResource(R.string.feed)) }) },
    snackbarHost = { SnackbarHost(snackbarHostState) },
) { innerPadding ->
    LazyColumn(
        modifier = Modifier.fillMaxSize().consumeWindowInsets(innerPadding),
        contentPadding = innerPadding,
    ) { items(posts, key = { it.id }) { post -> PostRow(post) } }
}
```

Source: https://developer.android.com/develop/ui/compose/components/scaffold , https://developer.android.com/develop/ui/compose/system/insets-ui

## Top app bars and scroll behaviors

| API | Notes | Status |
|---|---|---|
| `TopAppBar(title, modifier, navigationIcon, actions, expandedHeight, windowInsets, colors, scrollBehavior, contentPadding)` | small bar; `CenterAlignedTopAppBar` has the same parameters | stable (1.4+) |
| `TopAppBar(title, subtitle, ..., titleHorizontalAlignment, ...)` | small bar with subtitle | stable, 1.5+ |
| `MediumTopAppBar`, `LargeTopAppBar` | add `collapsedHeight`; no `contentPadding` | stable (1.4+) |
| `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar` | optional `subtitle`, `titleHorizontalAlignment` (Material 3 Expressive) | stable, 1.5+ |
| `BottomAppBar(actions, floatingActionButton, ...)`, `FlexibleBottomAppBar` | [MD] bottom app bar is no longer recommended in the Expressive update; toolbars replace it | stable; `FlexibleBottomAppBar` 1.5+ |
| `HorizontalFloatingToolbar(expanded, ...)`, `VerticalFloatingToolbar` | toolbars (Material 3 Expressive) | stable, 1.5+ |

| Scroll behavior (`TopAppBarDefaults`) | Effect | 1.4 | 1.5 |
|---|---|---|---|
| `pinnedScrollBehavior()` | bar stays; container color changes when content scrolls under it | needs `@OptIn(ExperimentalMaterial3Api::class)` | stable |
| `enterAlwaysScrollBehavior()` | bar leaves on scroll down, returns on any scroll up | opt-in | stable |
| `exitUntilCollapsedScrollBehavior()` | medium or large bar collapses to the small height | opt-in | stable |

- [API] A scroll behavior does nothing until its `nestedScrollConnection` is attached: `Scaffold(modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection))` and `scrollBehavior = scrollBehavior` on the bar.
- [API] On 1.5 the `enterAlwaysScrollBehavior` overloads with `reverseLayout` or `isScrollingContentAtStart` are deprecated.
- [MD] Navigation icon on the leading edge (Up arrow on lower-level screens), at most a few actions on the trailing edge as `IconButton`s, the rest in an overflow menu. Every icon action needs a `contentDescription`.
- [Conv] Pass text through the `title` slot only; the bar sets the text style and color. Long titles: use a flexible or large bar rather than shrinking text.
- [API] Bars apply the status bar inset through their `windowInsets` parameter; do not add `statusBarsPadding()` to a bar inside a `Scaffold`.

```kotlin
// material3 1.5+; no opt-in (on 1.4 add @OptIn(ExperimentalMaterial3Api::class)). Not compiled.
val scrollBehavior = TopAppBarDefaults.exitUntilCollapsedScrollBehavior()
Scaffold(
    modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
    topBar = {
        LargeTopAppBar(
            title = { Text(stringResource(R.string.article)) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(painterResource(R.drawable.ic_arrow_back), contentDescription = stringResource(R.string.back))
                }
            },
            scrollBehavior = scrollBehavior,
        )
    },
) { innerPadding -> ArticleBody(contentPadding = innerPadding) }
```

Source: https://developer.android.com/develop/ui/compose/components/app-bars , https://m3.material.io/components/app-bars/overview , https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary

## Navigation bar, rail and drawers

| API | Key parameters | Status |
|---|---|---|
| `NavigationBar { }` with `NavigationBarItem(selected, onClick, icon, label, alwaysShowLabel, ...)` | item is a `RowScope` extension | stable |
| `ShortNavigationBar(arrangement, ...) { }` with `ShortNavigationBarItem(selected, onClick, icon, label, iconPosition, ...)` | Expressive bar; `label` is a required (nullable) parameter | stable, 1.4+ |
| `NavigationRail(header, ...) { }` with `NavigationRailItem(selected, onClick, icon, label, ...)` | baseline rail | stable |
| `WideNavigationRail(state, header, ...)`, `ModalWideNavigationRail`, `WideNavigationRailItem(selected, onClick, icon, label, railExpanded, ...)` | Expressive collapsed and expanded rail | stable, 1.4+ |
| `ModalNavigationDrawer(drawerContent, drawerState, gesturesEnabled, ...) { }` with `ModalDrawerSheet { }` and `NavigationDrawerItem(label, selected, onClick, icon, badge, ...)` | also `DismissibleNavigationDrawer`, `PermanentNavigationDrawer` | stable |

- [MD] A navigation bar holds three to five top-level destinations of equal importance, in compact and medium windows; use a rail from expanded width up. Never show a bar and a rail together.
- [MD] Every destination has an icon and a visible text label; the active one shows the indicator and a filled icon.
- [MD] The navigation drawer is no longer recommended in the Material 3 Expressive update; an expanded navigation rail takes its role. Existing drawers remain valid API. (Material 3 Expressive)
- [API] `DrawerState.open()` and `close()` are `suspend`: call them from `rememberCoroutineScope().launch { }`. Pass the same `drawerState` to `ModalDrawerSheet(drawerState = ...)` to get predictive back on the drawer.
- [API] Since material3 1.4 the selected label color of `NavigationBarItem` and `NavigationRailItem` is `secondary` (it was `onSurface`).
- [Conv] Hold the selected destination in saveable state or derive it from the back stack; tapping the selected item again should not push a duplicate destination.
- [Conv] Prefer `NavigationSuiteScaffold` (next section) over choosing between bar and rail by hand.

Source: https://m3.material.io/components/navigation-bar/guidelines , https://m3.material.io/components/navigation-rail/guidelines , https://m3.material.io/components/navigation-drawer/overview , https://developer.android.com/jetpack/androidx/releases/compose-material3

## NavigationSuiteScaffold

- [API] Artifact `androidx.compose.material3:material3-adaptive-navigation-suite` (versioned with material3; no experimental annotation on its composables in 1.5), package `androidx.compose.material3.adaptive.navigationsuite`.
- [API] Scope form: `NavigationSuiteScaffold(navigationSuiteItems = { item(selected, onClick, icon, label = ..., badge = ...) }, layoutType = ..., ...) { content }`. A second form takes `navigationItems = { NavigationSuiteItem(selected, onClick, icon, label, ...) }` plus `navigationSuiteType` and a `primaryActionContent` slot (1.4+).
- [API] Default layout: navigation bar when the window width or height is compact or the device is in tabletop posture, navigation rail otherwise.
- [API] `NavigationSuiteType` values: `NavigationBar`, `NavigationRail`, `NavigationDrawer`, `None`, `ShortNavigationBarCompact`, `ShortNavigationBarMedium`, `WideNavigationRailCollapsed`, `WideNavigationRailExpanded`.
- [API] To customize, compute the type yourself: start from `NavigationSuiteScaffoldDefaults.calculateFromAdaptiveInfo(currentWindowAdaptiveInfoV2())` and override for the cases you want.
- [API] `rememberNavigationSuiteScaffoldState()` shows or hides the navigation component (for example on a full-screen detail). Complete example: `examples/AdaptiveNavigation.kt`.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation , https://developer.android.com/reference/kotlin/androidx/compose/material3/adaptive/navigationsuite/package-summary

## Tabs

- [API] `PrimaryTabRow(selectedTabIndex, modifier, containerColor, contentColor, indicator, divider, tabs)` and `SecondaryTabRow(...)` are stable from 1.4 (experimental in 1.3). Scrollable variants: `PrimaryScrollableTabRow`, `SecondaryScrollableTabRow`.
- [API] `Tab(selected, onClick, text = ..., icon = ...)`; `LeadingIconTab(selected, onClick, text, icon)` for icon beside text.
- [API] `TabRow` and `ScrollableTabRow` are deprecated from 1.4.
- [MD] Tabs group related content at the same level of hierarchy. Primary tabs sit at the top of the content pane under the app bar; secondary tabs sit inside a content area, below primary tabs, when a second level is needed.
- [MD] Fewer than three top-level destinations: use tabs, not a navigation bar.
- [Conv] Pair a tab row with a `HorizontalPager` when content should swipe; keep one source of truth for the selected index.

```kotlin
// material3 1.4+; no opt-in. Not compiled.
PrimaryTabRow(selectedTabIndex = selectedIndex) {
    titles.forEachIndexed { index, title ->
        Tab(selected = index == selectedIndex, onClick = { onSelect(index) }, text = { Text(title) })
    }
}
```

Source: https://m3.material.io/components/tabs/guidelines , https://developer.android.com/develop/ui/compose/components/tabs

## Search bar

| Call | 1.4 | 1.5 |
|---|---|---|
| `SearchBar(state: SearchBarState, inputField, ...)` + `ExpandedFullScreenSearchBar` or `ExpandedDockedSearchBar` + `rememberSearchBarState()` + `SearchBarDefaults.InputField(textFieldState, searchBarState, onSearch, ...)` | exists, needs `@OptIn(ExperimentalMaterial3Api::class)` | stable |
| `SearchBar(inputField, expanded, onExpandedChange, ...)`, `DockedSearchBar(inputField, expanded, ...)` | experimental | deprecated |
| `SearchBar(query, onQueryChange, onSearch, active, onActiveChange, ...)` | deprecated | deprecated |
| `AppBarWithSearch(state, inputField, navigationIcon, actions, ...)` | - | experimental |

- [API] The collapsed bar and the expanded container are separate composables that share one `SearchBarState` and one input field. `SearchBarState.animateToExpanded()` and `animateToCollapsed()` are `suspend`.
- [API] The search bar supports predictive back when expanded.
- [Conv] Full screen for compact windows, docked for medium and larger.

```kotlin
// material3 1.5+; no opt-in (on 1.4 add @OptIn(ExperimentalMaterial3Api::class)). Not compiled.
val searchBarState = rememberSearchBarState()
val query = rememberTextFieldState()
val scope = rememberCoroutineScope()
val inputField = @Composable {
    SearchBarDefaults.InputField(
        textFieldState = query,
        searchBarState = searchBarState,
        onSearch = { text -> onSearch(text); scope.launch { searchBarState.animateToCollapsed() } },
        placeholder = { Text(stringResource(R.string.search_hint)) },
        leadingIcon = { Icon(painterResource(R.drawable.ic_search), contentDescription = null) },
    )
}
SearchBar(state = searchBarState, inputField = inputField)
ExpandedFullScreenSearchBar(state = searchBarState, inputField = inputField) {
    SearchSuggestions(query = query.text.toString())
}
```

Source: https://m3.material.io/components/search/guidelines , https://developer.android.com/develop/ui/compose/components/search-bar , https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary

## Window size classes

| Width class | Window width | Breakpoint constant (`androidx.window.core.layout.WindowSizeClass`) |
|---|---|---|
| Compact | below 600dp | - |
| Medium | 600 to 839dp | `WIDTH_DP_MEDIUM_LOWER_BOUND` (600) |
| Expanded | 840 to 1199dp | `WIDTH_DP_EXPANDED_LOWER_BOUND` (840) |
| Large | 1200 to 1599dp | `WIDTH_DP_LARGE_LOWER_BOUND` (1200) |
| Extra-large | 1600dp and up | `WIDTH_DP_EXTRA_LARGE_LOWER_BOUND` (1600) |

Height: `HEIGHT_DP_MEDIUM_LOWER_BOUND` (480), `HEIGHT_DP_EXPANDED_LOWER_BOUND` (900).

| Library | Call |
|---|---|
| adaptive 1.3.0+ | `currentWindowAdaptiveInfoV2().windowSizeClass` |
| adaptive 1.2.x and older | `currentWindowAdaptiveInfo().windowSizeClass` (the only form there; deprecated in 1.3.0) |

- [API] Test with `isWidthAtLeastBreakpoint(...)` / `isHeightAtLeastBreakpoint(...)`. The `WindowWidthSizeClass` and `WindowHeightSizeClass` types, `windowWidthSizeClass` and `WindowSizeClass.compute(...)` are deprecated in window-core 1.5.
- [API] `calculateWindowSizeClass(activity)` from `material3-window-size-class` is a separate, older type hierarchy and still experimental; prefer the adaptive library.
- [MD] Most apps can adapt on width alone. Size classes describe the app's window, not the device: the same code must work in split screen, on foldables and in desktop windows.
- [Conv] Never branch on device type, orientation or `LocalConfiguration.current.screenWidthDp`.
- [API] The developer.android.com guide snippets still call `currentWindowAdaptiveInfo()`; on adaptive 1.3.0 that call compiles with a deprecation warning.

```kotlin
// adaptive 1.3.0+, window-core 1.5+; no opt-in. Not compiled.
val sizeClass = currentWindowAdaptiveInfoV2().windowSizeClass
val showTwoPanes = sizeClass.isWidthAtLeastBreakpoint(WindowSizeClass.WIDTH_DP_EXPANDED_LOWER_BOUND)
```

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes , https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive , https://developer.android.com/reference/kotlin/androidx/window/core/layout/WindowSizeClass

## Adaptive pane scaffolds

- [API] Artifacts `androidx.compose.material3.adaptive:adaptive`, `adaptive-layout`, `adaptive-navigation`. `ListDetailPaneScaffold`, `SupportingPaneScaffold`, `NavigableListDetailPaneScaffold`, `NavigableSupportingPaneScaffold`, `AnimatedPane` and `rememberListDetailPaneScaffoldNavigator` are annotated `@ExperimentalMaterial3AdaptiveApi` in every release from 1.0 to 1.4 alpha: they always need `@OptIn(ExperimentalMaterial3AdaptiveApi::class)`.
- [API] `NavigableListDetailPaneScaffold(navigator, listPane, detailPane, modifier, extraPane, defaultBackBehavior, ...)` handles Back itself. `navigator.navigateTo(ListDetailPaneScaffoldRole.Detail, contentKey)` and `navigateBack()` are `suspend` since adaptive 1.1; `navigator.currentDestination?.contentKey` is the selected item; `canNavigateBack()` tells whether to show an Up arrow.
- [API] Wrap each pane's content in `AnimatedPane { }`. Packages: scaffold roles and `AnimatedPane` in `androidx.compose.material3.adaptive.layout`, navigator and `Navigable...` scaffolds in `androidx.compose.material3.adaptive.navigation`.
- [MD] List-detail: one pane in compact width, list and detail side by side in expanded width; selecting in the list updates the detail without leaving the screen.
- [Conv] If the project forbids experimental API, build two panes in a `Row` switched on the width breakpoint (previous section) and handle Back with `BackHandler`; say that this trades away pane animation, hinge awareness and predictive back.
- [API] adaptive 1.3.0 adds `adaptive-navigation3` (`rememberListDetailSceneStrategy`) for apps on Navigation 3. Complete example: `examples/ListDetail.kt`.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/list-detail , https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts , https://m3.material.io/foundations/layout/canonical-layouts

## Navigation libraries

| Library | Artifact, stable version | Core API | Status |
|---|---|---|---|
| Navigation 3 | `androidx.navigation3:navigation3-runtime`, `navigation3-ui` 1.2.2 (1.0.0 on 2025-11-19) | `rememberNavBackStack(vararg NavKey)`, `NavDisplay(backStack, onBack, entryProvider = entryProvider { entry<Key> { } })` | stable; no experimental annotations in the 1.2 API files |
| Navigation 2 | `androidx.navigation:navigation-compose` 2.10.2 | `rememberNavController()`, `NavHost(navController, startDestination) { composable<Route> { } }` | stable, supported |

- [API] Navigation 3 is Compose-first: the back stack is a list of keys the app owns (`backStack.add(key)`, `backStack.removeLastOrNull()`); keys implement `NavKey` and are `@Serializable`.
- [Conv] Use Navigation 3 for new Compose apps and keep Navigation 2 where it already works. No official page deprecates Navigation 2; treat a migration as optional.
- [API] Both `NavHost` and `NavDisplay` have predictive-pop transition parameters; neither needs a manual `BackHandler` for ordinary back navigation.
- [Conv] Navigate with typed routes or keys carrying ids, not whole objects; top-level destination switches should restore each destination's state rather than stacking screens.

```kotlin
// navigation3 1.0+, kotlinx.serialization; no opt-in. Not compiled.
@Serializable data object Home : NavKey
@Serializable data class Detail(val id: String) : NavKey

val backStack = rememberNavBackStack(Home)
NavDisplay(
    backStack = backStack,
    onBack = { backStack.removeLastOrNull() },
    entryProvider = entryProvider {
        entry<Home> { HomeScreen(onOpen = { id -> backStack.add(Detail(id)) }) }
        entry<Detail> { key -> DetailScreen(key.id) }
    },
)
```

Source: https://developer.android.com/guide/navigation/navigation-3 , https://developer.android.com/jetpack/androidx/releases/navigation3 , https://developer.android.com/guide/navigation

## Back and predictive back

- [API] `BackHandler(enabled: Boolean = true, onBack: () -> Unit)` and `PredictiveBackHandler(enabled, onBack: suspend (progress: Flow<BackEventCompat>) -> Unit)` live in `androidx.activity.compose` (activity-compose 1.13; neither deprecated).
- [API] Predictive back previews the destination during the swipe. In-app animations arrived in Android 14; for apps targeting Android 16 (API 36) on Android 16+ devices the system animations are on by default. Opt out per app or activity with `android:enableOnBackInvokedCallback="false"`.
- [API] Overriding `onBackPressed()` or intercepting `KeyEvent.KEYCODE_BACK` is no longer supported for back interception; use the AndroidX callbacks.
- [Conv] Enable a `BackHandler` only while there is something to intercept (`enabled = hasUnsavedChanges`). An always-enabled handler disables the system preview and traps the user.
- [API] Material components with built-in predictive back: `ModalBottomSheet`, the search bar, `ModalDrawerSheet` and `DismissibleDrawerSheet` (via their `drawerState` overload), the navigable pane scaffolds.
- [MD] Back always returns to the previous destination or dismisses the top surface; do not use it for confirmation-only interstitials except to protect unsaved input.

```kotlin
// activity-compose; no opt-in. Not compiled.
BackHandler(enabled = hasUnsavedChanges) { showDiscardDialog = true }
```

Source: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture , https://developer.android.com/about/versions/16/behavior-changes-16 , https://developer.android.com/reference/kotlin/androidx/activity/compose/package-summary

## Edge-to-edge and window insets

- [Req] Edge-to-edge is enforced on Android 15+ devices for apps targeting SDK 35; apps targeting API 36 cannot opt out on Android 16. The app must handle insets.
- [MD] Enable edge-to-edge in `onCreate` so older Android versions behave the same. Bars become transparent, with a translucent scrim only for three-button navigation.
- [API] Two spellings: `ComponentActivity.enableEdgeToEdge(statusBarStyle, navigationBarStyle)` from `androidx.activity` (added in 1.8.0, not deprecated in stable 1.13, deprecated in 1.14.0-alpha03) and `WindowCompat.enableEdgeToEdge(window)` from `androidx.core`, which the 1.14 alpha notes and the Views guide name as the replacement. [Unverified] The androidx.core version that introduced the latter was not checked.
- [API] `window.statusBarColor` and `android:statusBarColor` are deprecated and have no effect on Android 15; draw your own background behind the bar instead.
- [API] Inside a `Scaffold`, `innerPadding` already includes the system bar insets (`contentWindowInsets`); Material bars, sheets and the navigation suite handle their own insets through `windowInsets` parameters.
- [API] Without a `Scaffold`: `Modifier.safeDrawingPadding()` (or `windowInsetsPadding(WindowInsets.safeDrawing)`) for content that must not sit under system UI; `WindowInsets.safeGestures` for gesture-sensitive content; `WindowInsets.systemBars` includes the caption bar of desktop windows.
- [API] Keyboard: set `android:windowSoftInputMode="adjustResize"` on the activity and apply `Modifier.imePadding()` to the scrolling container.
- [API] Inset padding modifiers consume what they apply, so nested ones do not add up; size modifiers (`windowInsetsBottomHeight`) do not consume. `Modifier.imeNestedScroll()` is `@ExperimentalLayoutApi`.
- [Conv] Backgrounds and lists extend edge to edge; text and controls stay inside the safe area. Do not pad the whole screen and leave blank bars.

```kotlin
// activity 1.8 to 1.13 (on 1.14 alpha use WindowCompat.enableEdgeToEdge(window)); no opt-in. Not compiled.
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent { AppTheme { AppShell() } }
    }
}
```

Source: https://developer.android.com/develop/ui/compose/system/setup-e2e , https://developer.android.com/develop/ui/compose/system/insets , https://developer.android.com/develop/ui/compose/system/insets-ui , https://developer.android.com/about/versions/15/behavior-changes-15 , https://developer.android.com/about/versions/16/behavior-changes-16

## Common mistakes

- Ignoring `innerPadding` -> `contentPadding = innerPadding` or `Modifier.padding(innerPadding)`.
- `statusBarsPadding()` added inside a `Scaffold` that already applies insets (double padding) -> rely on `innerPadding`, add `consumeWindowInsets(innerPadding)`.
- Scroll behavior created but `nestedScroll(scrollBehavior.nestedScrollConnection)` missing -> attach it to the `Scaffold`.
- Hand-built bottom bar from a `Row`, or a navigation bar at every window size -> `NavigationSuiteScaffold`.
- `TabRow`, `DockedSearchBar`, `currentWindowAdaptiveInfo()` in new code -> `PrimaryTabRow`, `SearchBar(state, inputField)`, `currentWindowAdaptiveInfoV2()`; see `references/implementation-availability.md`.
- `screenWidthDp > 600` or "isTablet" checks -> window size class breakpoints.
- `navigator.navigateTo(...)`, `drawerState.open()` or `searchBarState.animateToExpanded()` called outside a coroutine -> `scope.launch { }`.
- Pane scaffold used without the opt-in or described as stable -> `@OptIn(ExperimentalMaterial3AdaptiveApi::class)`, stated in the answer.
- Always-enabled `BackHandler`, or `onBackPressed()` override -> conditional `BackHandler`; let the system handle the rest.
- `window.statusBarColor = ...` or an Accompanist system UI controller -> `enableEdgeToEdge()` plus insets.
- Text field hidden by the keyboard -> `adjustResize` and `imePadding()`.
