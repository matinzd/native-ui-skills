# M4: Jetpack Compose and Views implementation of Material 3

Research agent M4, 2026-11-23. Nothing here was compiled (no Android SDK on the machine). Every Compose signature below
was read from the androidx public API signature files; every status (stable / experimental / deprecated) is the
annotation printed in that file.

Tags: **[V]** fetched in this session and the source says this; **[M]** from memory, not verified.
Strength: **[API]** API contract or fixed platform behaviour, **[Rec]** Google recommendation, **[Conv]** community convention.

## 0. Sources, versions and how to read the signatures

### 0.1 Current versions (all [V])

| Library | Latest stable | Latest pre-release | Source |
|---|---|---|---|
| Compose BOM | `2026.11.01` | - | https://developer.android.com/develop/ui/compose/bom/bom-mapping |
| `androidx.compose.material3:material3` | **1.5.0** (2026-11-18) | 1.6.0-alpha01 (2026-11-18) | https://developer.android.com/jetpack/androidx/releases/compose-material3 |
| `material3-adaptive-navigation-suite`, `material3-window-size-class` | 1.5.0 (same group as material3 since material3 1.3) | 1.6.0-alpha01 | same page |
| `androidx.compose.material3.adaptive:adaptive*` | **1.3.0** (2026-08-12) | 1.4.0-alpha03 | https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive |
| Compose UI / Foundation / Material (M2) | **1.13.0** (2026-11-18) | 1.14.0-alpha01 | .../releases/compose-ui , compose-foundation , compose-material |
| `androidx.compose.material:material-icons-core` / `-extended` | frozen at **1.7.8** in the BOM | none | BOM mapping page |
| `androidx.activity:activity(-compose)` | **1.13.0** (2026-09-23) | 1.14.0-alpha03 | https://developer.android.com/jetpack/androidx/releases/activity |
| `androidx.navigation:navigation-compose` (Navigation 2) | **2.10.2** (2026-09-23) | 2.11.0-alpha01 | https://developer.android.com/jetpack/androidx/releases/navigation |
| `androidx.navigation3:navigation3-*` | **1.2.2** (2026-11-18); 1.0.0 was 2025-11-19 | 1.3.0-alpha05 | https://developer.android.com/jetpack/androidx/releases/navigation3 |
| `androidx.window:window(-core)` | **1.5.1** (2026-06-17) | 1.6.0-alpha05 | https://developer.android.com/jetpack/androidx/releases/window |
| `androidx.wear.compose:compose-material3` | **1.7.2** (2026-11-18) | 1.8.0-alpha04/05 | https://developer.android.com/jetpack/androidx/releases/wear-compose |
| `androidx.tv:tv-material` | **1.1.0** (2026-05-06) | - | https://developer.android.com/jetpack/androidx/releases/tv |
| Material Components for Android (Views) | version number not verified (maven host blocked); docs say Material3 themes need >= 1.5.0, `Material3Expressive` themes need >= **1.14.0**, compileSdk 36.1+, minSdk 23+ | - | https://raw.githubusercontent.com/material-components/material-components-android/master/docs/getting-started.md |

### 0.2 API files used as ground truth (cached)

Cache folder: `/tmp/claude-0/-home-user-apple-hig-skill/4b8f6fc4-b934-5d7d-9f48-9d6e78d71918/scratchpad/m4/api/`
(release notes and guides as text in `.../m4/web/`, MDC-Android docs in `.../m4/mdc/`).
All files come from `https://raw.githubusercontent.com/androidx/androidx/androidx-main/<module>/api/<file>`.

| Cached file | Module path | Corresponds to |
|---|---|---|
| `m3-1.5.0-beta01.txt` | `compose/material3/material3/api/1.5.0-beta01.txt` | API frozen at material3 1.5.0-beta01; **used as the stable 1.5.0 surface** |
| `m3-main.txt` | `.../api/current.txt` | androidx-main = material3 **1.6.0-alpha01** (`libraryversions.toml`: `COMPOSE_MATERIAL3 = "1.6.0-alpha01"`) |
| `m3-1.4.0-beta03.txt`, `m3-1.4.0-beta01.txt`, `m3-1.3.0-beta01.txt` | same folder | material3 1.4.x and 1.3.x surfaces |
| `navsuite-1.5.0-beta01.txt` / `navsuite-main.txt` | `compose/material3/material3-adaptive-navigation-suite/api/` | 1.5.0 / 1.6.0-alpha01 (identical apart from header) |
| `wsc-1.5.0-beta01.txt` | `compose/material3/material3-window-size-class/api/` | 1.5.0 |
| `adaptive-1.3.0-beta01.txt`, `adaptive-layout-*.txt`, `adaptive-navigation-*.txt` (1.0, 1.1, 1.2, 1.3 betas and main) | `compose/material3/adaptive/<artifact>/api/` | adaptive 1.3.0 (stable) and 1.4.0-alpha03 (main) |
| `window-core-1.5.0-beta01.txt` | `window/window-core/api/` | window 1.5.x |
| `foundation-layout-1.13.0-beta01.txt`, `foundation-1.13.0-beta01.txt`, `ui-1.13.0-beta01.txt`, `ui-test-1.13.0-beta01.txt` | `compose/foundation/...`, `compose/ui/...` | Compose 1.13.0 |
| `ui-test-junit4-main.txt`, `a11y-test-main.txt` | `compose/ui/ui-test-junit4`, `compose/ui/ui-test-accessibility` | Compose 1.14.0-alpha02 (main) |
| `activity-1.13.0-beta01.txt`, `activity-compose-1.13.0-beta01.txt` | `activity/...` | activity 1.13.0 |
| `nav-compose-2.10.0-beta01.txt`, `nav3-runtime-1.2.0-beta01.txt`, `nav3-ui-1.2.0-beta01.txt` | `navigation/navigation-compose`, `navigation3/...` | navigation 2.10.x, navigation3 1.2.x |
| `wear-m3-1.7.0-beta01.txt`, `tv-m3-1.1.0-beta01.txt` | `wear/compose/compose-material3`, `tv/tv-material` | Wear Compose M3 1.7.x, TV Material 1.1.0 |
| `m2-main.txt`, `ripple-main.txt`, `ripple3-main.txt` | `compose/material/material`, `material-ripple`, `compose/material3/material3-ripple` | main |

Caveats:
- **No release branch or tag was reachable** on raw.githubusercontent.com (tried `androidx-compose-material3-release` and
  variants: 404). The stable surface is therefore approximated by the `<version>-beta01.txt` snapshot that androidx keeps
  in `androidx-main`; API changes between beta01 and the final release are possible but rare. The 1.5.0 release notes were
  used as a cross-check; one mismatch was found (SplitButton, section 4).
- `material-icons-core/api/current.txt` is 404 in androidx-main (the module's API file is no longer there).
- Signature notation used below: parameters in declaration order; `~name` means the parameter has a default; a trailing
  `content`/lambda is the trailing lambda. `[exp]` = `@ExperimentalMaterial3Api`, `[exp-expressive]` =
  `@ExperimentalMaterial3ExpressiveApi`, `[exp-adaptive]` = `@ExperimentalMaterial3AdaptiveApi`.

### 0.3 Headline findings that contradict common lore (all [V] in the API files)

1. **material3 1.5.0 is the first stable release with M3 Expressive.** `MaterialExpressiveTheme`, `MotionScheme`,
   `ButtonGroup`, `ToggleButton`, `FloatingActionButtonMenu`, `HorizontalFloatingToolbar`, wavy progress indicators,
   `ShortNavigationBar`, `WideNavigationRail`, `SegmentedListItem` carry **no** experimental annotation in 1.5.0. Only 27
   `@ExperimentalMaterial3ExpressiveApi` uses remain (loading indicators, `MaterialShapes`, carousel parallax). The 1.4.0
   file contains zero expressive APIs.
2. `ExperimentalMaterial3Api` uses dropped from 200 (1.4) to 74 (1.5). Still `[exp]` in 1.5.0: `ModalBottomSheet`,
   `BottomSheetScaffold`, `SheetState`, `TooltipBox`/`PlainTooltip`/`RichTooltip`, `AppBarWithSearch`, standalone `BottomSheet`.
3. Deprecated in 1.5.0 (still compile, with warnings): `ListItem(headlineContent = ...)`, `Slider(value = ...)` and
   `RangeSlider(value = ...)`, `rememberModalBottomSheetState`, `rememberStandardBottomSheetState`, `DockedSearchBar`,
   `SearchBar(inputField, expanded, ...)`, `TopSearchBar`, `TabRow`/`ScrollableTabRow` (already in 1.4), `Divider`.
4. In **1.6.0-alpha01 only**: `TextField`/`OutlinedTextField(value, onValueChange)` are deprecated in favour of the
   `TextFieldState` overloads. In 1.5.0 both forms are non-deprecated. Foundation 1.13 already deprecates
   `BasicTextField(value, onValueChange)`.
5. `currentWindowAdaptiveInfo()` is **deprecated** in adaptive 1.3.0; replacement `currentWindowAdaptiveInfoV2()`. The
   developer.android.com guides still show the old call.
6. `ListDetailPaneScaffold`, `SupportingPaneScaffold`, `NavigableListDetailPaneScaffold`, `AnimatedPane`,
   `rememberListDetailPaneScaffoldNavigator` are `[exp-adaptive]` in **every** cached version (1.0 to main), although the
   artifact is "stable" 1.3.0. They always need `@OptIn(ExperimentalMaterial3AdaptiveApi::class)`.
7. `androidx.window.core.layout.WindowWidthSizeClass`/`WindowHeightSizeClass` and `WindowSizeClass.compute` are deprecated;
   use `isWidthAtLeastBreakpoint(...)`. Breakpoint constants now include Large (1200) and Extra-large (1600).
8. material3 no longer depends on `material-icons-core` (since 1.4.0); `Icons.*` is not on the classpath by default and the
   icons library is "no longer maintained or recommended".

## 1. Theming

Source for all signatures: `m3-1.5.0-beta01.txt` [V]. Guide: https://developer.android.com/develop/ui/compose/designsystems/material3

| API | Signature (1.5.0) | Status |
|---|---|---|
| `MaterialTheme` | `(~colorScheme: ColorScheme, ~shapes: Shapes, ~typography: Typography, content)` | stable |
| `MaterialTheme` | `(~colorScheme, ~motionScheme: MotionScheme, ~shapes, ~typography, content)` | stable in 1.5.0; absent in 1.4 |
| `MaterialExpressiveTheme` | `(~colorScheme: ColorScheme?, ~motionScheme: MotionScheme?, ~shapes: Shapes?, ~typography: Typography?, content)` | stable in 1.5.0; absent in 1.4 |
| `MaterialTheme.colorScheme / typography / shapes / motionScheme` | `@Composable @ReadOnlyComposable` properties | stable (`motionScheme` new in 1.5) |
| `MotionScheme` | interface with `defaultSpatialSpec() fastSpatialSpec() slowSpatialSpec() defaultEffectsSpec() fastEffectsSpec() slowEffectsSpec()`; `MotionScheme.standard()`, `MotionScheme.expressive()` | stable in 1.5.0 |
| `lightColorScheme(...)` / `darkColorScheme(...)` | all roles optional: primary, onPrimary, primaryContainer, onPrimaryContainer, inversePrimary, secondary..., tertiary..., background, onBackground, surface, onSurface, surfaceVariant, onSurfaceVariant, surfaceTint, inverseSurface, inverseOnSurface, error, onError, errorContainer, onErrorContainer, outline, outlineVariant, scrim, surfaceBright, surfaceContainer, surfaceContainerHigh, surfaceContainerHighest, surfaceContainerLow, surfaceContainerLowest, surfaceDim, primaryFixed, primaryFixedDim, onPrimaryFixed, onPrimaryFixedVariant, (same for secondary, tertiary) | stable |
| `expressiveLightColorScheme()` | no parameters; there is **no** `expressiveDarkColorScheme` in 1.5.0 or main | stable in 1.5.0 |
| `dynamicLightColorScheme(context: Context)` / `dynamicDarkColorScheme(context)` | `@RequiresApi(Build.VERSION_CODES.S)` (API 31) | stable |
| `Typography` | `(~displayLarge ... ~labelSmall: TextStyle)` 15 styles; 1.5 adds an overload with 15 more `*Emphasized` styles and one taking `fontFamily: FontFamily` first | stable |
| `Shapes` | `(~extraSmall, ~small, ~medium, ~large, ~extraLarge)`; 1.5 overload adds `~largeIncreased, ~extraLargeIncreased, ~extraExtraLarge` (all `CornerBasedShape`) | stable |
| `LocalContentColor`, `LocalTextStyle`, `ProvideTextStyle(value, content)` | composition locals | stable |
| `contentColorFor(backgroundColor: Color): Color`; `ColorScheme.contentColorFor(backgroundColor)` | | stable |
| `ColorScheme.surfaceColorAtElevation(elevation: Dp)` | tonal-elevation overlay colour | stable (legacy approach) |
| `LocalAbsoluteTonalElevation`, `LocalTonalElevationEnabled` | | stable (`LocalTonalElevationEnabled` since 1.2.0-alpha03) |
| `Surface` | `(~modifier, ~shape, ~color, ~contentColor, ~tonalElevation, ~shadowElevation, ~border, content)` plus clickable `(onClick, ...)`, selectable `(selected, onClick, ...)`, toggleable `(checked, onCheckedChange, ...)` overloads | stable |
| `isSystemInDarkTheme()` | `androidx.compose.foundation`, `@Composable @ReadOnlyComposable` | stable |
| `LocalMotionScheme` | not in the 1.5.0-beta01 file; release notes say deprecated in favour of `MaterialTheme.motionScheme` | [V] release notes |

Rules:
- [API] Dynamic colour needs API 31+: gate with `Build.VERSION.SDK_INT >= Build.VERSION_CODES.S` and fall back to a static
  scheme. Guide: "If not, you should fall back to using a custom light or dark ColorScheme". [V]
- [Rec] Read colours from `MaterialTheme.colorScheme` roles and pair container with its `on` role. The guide's contrast
  example pairs `primary`/`onPrimary` and marks `tertiaryContainer` with `primaryContainer` content as poor contrast. [V]
- [Rec] M3 has no `ContentAlpha`/`LocalContentAlpha`; emphasis comes from colour roles (`onSurface` vs `onSurfaceVariant`)
  and font weight. [V] guide "Emphasis" section; neither symbol exists in the M3 API file.
- [V] `dynamicLightColorScheme`/`dynamicDarkColorScheme` return higher-chroma surface and surfaceContainer roles since 1.2.
- [V] 1.4.0 behaviour change: selected label colour of `NavigationBarItem`/`NavigationRailItem` is `secondary` (was `onSurface`).
- Contrast: the colour-scheme builders take no contrast parameter in 1.5.0 or main [V]. User contrast level
  (`UiModeManager.getContrast()`, API 34) and Material Theme Builder medium/high contrast schemes are [M]; not verified here.

## 2. Structure and navigation

### 2.1 Scaffold and app bars (`m3-1.5.0-beta01.txt` [V])

| API | Signature | Status |
|---|---|---|
| `Scaffold` | `(~modifier, ~topBar, ~bottomBar, ~snackbarHost, ~floatingActionButton, ~floatingActionButtonPosition: FabPosition, ~containerColor, ~contentColor, ~contentWindowInsets: WindowInsets, content: (PaddingValues) -> Unit)` | stable. `FabPosition`: Start, Center, End, EndOverlay |
| `TopAppBar` | `(title, ~modifier, ~navigationIcon, ~actions: RowScope.() -> Unit, ~expandedHeight, ~windowInsets, ~colors: TopAppBarColors, ~scrollBehavior: TopAppBarScrollBehavior?, ~contentPadding)` | stable (1.4 and 1.5) |
| `TopAppBar` with subtitle | `(title, subtitle, ~modifier, ~navigationIcon, ~actions, ~titleHorizontalAlignment, ~expandedHeight, ~windowInsets, ~colors, ~scrollBehavior, ~contentPadding)` | stable in 1.5.0 |
| `CenterAlignedTopAppBar` | same as `TopAppBar` | stable |
| `MediumTopAppBar`, `LargeTopAppBar` | `(title, ~modifier, ~navigationIcon, ~actions, ~collapsedHeight, ~expandedHeight, ~windowInsets, ~colors, ~scrollBehavior)` | stable |
| `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar` | `(title, ~modifier, ~subtitle, ~navigationIcon, ~actions, ~titleHorizontalAlignment, ~collapsedHeight, ~expandedHeight, ~windowInsets, ~colors, ~scrollBehavior)` | stable in 1.5.0; absent in 1.4 |
| `TwoRowsTopAppBar` | `(title: (expanded: Boolean) -> Unit, ~modifier, ~subtitle, ...)` | stable in 1.5.0 |
| `TopAppBarDefaults.pinnedScrollBehavior` | `(~state: TopAppBarState, ~canScroll: () -> Boolean)`; new overload `(scrollableState: ScrollableState, ~state, ~canScroll)` | stable in 1.5.0; `[exp]` in 1.4 |
| `TopAppBarDefaults.enterAlwaysScrollBehavior` | `(~state, ~canScroll, ~snapAnimationSpec, ~flingAnimationSpec)`; overload with leading `scrollableState`; overloads with `reverseLayout` / `isScrollingContentAtStart` are deprecated | stable in 1.5.0; `[exp]` in 1.4 |
| `TopAppBarDefaults.exitUntilCollapsedScrollBehavior` | `(~state, ~canScroll, ~snapAnimationSpec, ~flingAnimationSpec)` | stable in 1.5.0; `[exp]` in 1.4 |
| `TopAppBarScrollBehavior.nestedScrollConnection` | pass to `Modifier.nestedScroll(...)` on the Scaffold | stable in 1.5.0 |
| `BottomAppBar` | `(actions: RowScope.() -> Unit, ~modifier, ~floatingActionButton, ~containerColor, ~contentColor, ~tonalElevation, ~contentPadding, ~windowInsets, ~scrollBehavior: BottomAppBarScrollBehavior?)` and a `content: RowScope.() -> Unit` form | stable in 1.5.0; `[exp]` in 1.4 |
| `FlexibleBottomAppBar` | `(~modifier, ~containerColor, ~contentColor, ~contentPadding, ~horizontalArrangement, ~expandedHeight, ~windowInsets, ~scrollBehavior, content)` | stable in 1.5.0 |
| `HorizontalFloatingToolbar` | `(expanded: Boolean, ~modifier, ~colors, ~contentPadding, ~scrollBehavior, ~shape, ~leadingContent, ~trailingContent, ~expandedShadowElevation, ~collapsedShadowElevation, content: RowScope.() -> Unit)`; FAB overload `(expanded, floatingActionButton, ...)`; `VerticalFloatingToolbar` mirrors it | stable in 1.5.0; absent in 1.4 |
| `AppBarWithSearch` | `(state: SearchBarState, inputField, ~modifier, ~navigationIcon, ~actions, ...)` | `[exp]` |

- [API] `SmallTopAppBar` does not exist in any cached M3 file. It was deprecated in 1.0.0-beta02 in favour of `TopAppBar`. [V]
- [API] The Scaffold `content` lambda receives `PaddingValues`; apply it (`Modifier.padding(innerPadding)` or
  `contentPadding = innerPadding`) or content draws under the bars. Lint check name `UnusedMaterial3ScaffoldPaddingParameter` is [M].

### 2.2 Navigation components

| API | Signature | Status |
|---|---|---|
| `NavigationBar` | `(~modifier, ~containerColor, ~contentColor, ~tonalElevation, ~windowInsets, content: RowScope.() -> Unit)` | stable |
| `RowScope.NavigationBarItem` | `(selected, onClick, icon, ~modifier, ~enabled, ~label, ~alwaysShowLabel, ~colors: NavigationBarItemColors, ~interactionSource)` | stable |
| `ShortNavigationBar` | `(~modifier, ~containerColor, ~contentColor, ~windowInsets, ~arrangement: ShortNavigationBarArrangement, content)` | stable (no annotation in 1.4.0-beta03 or 1.5.0) |
| `ShortNavigationBarItem` | `(selected, onClick, icon, label: (() -> Unit)?, ~modifier, ~enabled, ~iconPosition: NavigationItemIconPosition, ~colors: NavigationItemColors, ~interactionSource)` | stable |
| `NavigationRail` | `(~modifier, ~containerColor, ~contentColor, ~header: (ColumnScope.() -> Unit)?, ~windowInsets, content: ColumnScope.() -> Unit)` | stable |
| `NavigationRailItem` | `(selected, onClick, icon, ~modifier, ~enabled, ~label, ~alwaysShowLabel, ~colors, ~interactionSource)` | stable |
| `WideNavigationRail` | `(~modifier, ~state: WideNavigationRailState, ~shape, ~colors, ~header, ~windowInsets, ~arrangement, ~contentPadding, content)` | stable |
| `ModalWideNavigationRail` | `(~modifier, ~state, ~hideOnCollapse, ~collapsedShape, ~expandedShape, ~colors, ~header, ~expandedHeaderTopPadding, ~windowInsets, ~arrangement, ~expandedProperties, ~contentPadding, content)` | stable |
| `WideNavigationRailItem` | `(selected, onClick, icon, label, railExpanded: Boolean, ~modifier, ~enabled, ~iconPosition, ~colors, ~interactionSource, ~indicatorPadding)` | stable |
| `ModalNavigationDrawer` | `(drawerContent, ~modifier, ~drawerState: DrawerState, ~gesturesEnabled, ~scrimColor, content)` | stable |
| `DismissibleNavigationDrawer` | `(drawerContent, ~modifier, ~drawerState, ~gesturesEnabled, content)` | stable |
| `PermanentNavigationDrawer` | `(drawerContent, ~modifier, content)` | stable |
| `ModalDrawerSheet` / `DismissibleDrawerSheet` | `(~modifier, ~drawerShape, ~drawerContainerColor, ~drawerContentColor, ~drawerTonalElevation, ~windowInsets, content: ColumnScope.() -> Unit)`; overload with leading `drawerState` (predictive back) | stable |
| `PermanentDrawerSheet` | same without `drawerState` | stable |
| `NavigationDrawerItem` | `(label, selected, onClick, ~modifier, ~icon, ~badge, ~shape, ~colors, ~interactionSource)` | stable |
| `rememberDrawerState` | `(initialValue: DrawerValue, ~confirmStateChange)`; `DrawerState.open()`, `close()` are `suspend`; `isOpen`, `isClosed` | stable |

Tabs:

| API | Signature | Status |
|---|---|---|
| `PrimaryTabRow`, `SecondaryTabRow` | `(selectedTabIndex: Int, ~modifier, ~containerColor, ~contentColor, ~indicator: TabIndicatorScope.() -> Unit, ~divider, tabs)` | stable (1.4 and 1.5) |
| `PrimaryScrollableTabRow`, `SecondaryScrollableTabRow` | `(selectedTabIndex, ~modifier, ~scrollState, ~containerColor, ~contentColor, ~edgePadding, ~indicator, ~divider, ~minTabWidth, tabs)` | stable |
| `Tab` | `(selected, onClick, ~modifier, ~enabled, ~text, ~icon, ~selectedContentColor, ~unselectedContentColor, ~interactionSource)`; custom-content overload | stable |
| `LeadingIconTab` | `(selected, onClick, text, icon, ~modifier, ~enabled, ...)` | stable |
| `TabRow`, `ScrollableTabRow` | `indicator: (List<TabPosition>) -> Unit` | **@Deprecated** in 1.4.0-beta03, 1.5.0 and main |

Search (1.5.0):

| API | Signature | Status |
|---|---|---|
| `SearchBar` (collapsed bar) | `(state: SearchBarState, inputField, ~modifier, ~shape, ~colors, ~tonalElevation, ~shadowElevation)` | stable in 1.5.0; `[exp]` in 1.4 |
| `SearchBarDefaults.InputField` | `(textFieldState: TextFieldState, searchBarState: SearchBarState, onSearch: (String) -> Unit, ~modifier, ~enabled, ~readOnly, ~textStyle, ~placeholder, ~leadingIcon, ~trailingIcon, ~prefix, ~suffix, ~inputTransformation, ~outputTransformation, ~scrollState, ~shape, ~colors, ~interactionSource, ~keyboardOptions, ~lineLimits)` | stable in 1.5.0 |
| `ExpandedFullScreenSearchBar` | `(state, inputField, ~modifier, ~collapsedShape, ~colors, ~tonalElevation, ~shadowElevation, ~windowInsets: () -> WindowInsets, ~properties: DialogProperties, content: ColumnScope.() -> Unit)` | stable in 1.5.0 |
| `ExpandedDockedSearchBar` | `(state, inputField, ~modifier, ~shape, ~colors, ~tonalElevation, ~shadowElevation, ~properties: PopupProperties, content)` | stable in 1.5.0 |
| `ExpandedDockedSearchBarWithGap`, `ExpandedFullScreenContainedSearchBar` | same family | stable in 1.5.0 |
| `rememberSearchBarState` | `(~initialValue: SearchBarValue, ~animationSpecForExpand, ~animationSpecForCollapse)`; `SearchBarValue`: Collapsed, Expanded | stable in 1.5.0 |
| `SearchBar(query, onQueryChange, onSearch, active, onActiveChange, ...)`, `SearchBar(inputField, expanded, onExpandedChange, ...)`, `DockedSearchBar(...)` (both), `TopSearchBar`, `InputField(query, ...)`, `InputField(state, onSearch, expanded, ...)` | | all **@Deprecated** `[exp]` in 1.5.0 |

### 2.3 Adaptive navigation and panes

`NavigationSuiteScaffold` (`navsuite-1.5.0-beta01.txt` [V]; artifact `androidx.compose.material3:material3-adaptive-navigation-suite`; no experimental annotation on any composable):

| API | Signature |
|---|---|
| `NavigationSuiteScaffold` (scope DSL) | `(navigationSuiteItems: NavigationSuiteScope.() -> Unit, ~modifier, ~layoutType: NavigationSuiteType, ~navigationSuiteColors, ~containerColor, ~contentColor, ~state: NavigationSuiteScaffoldState, ~content)` |
| `NavigationSuiteScope.item` | `(selected, onClick, icon, ~modifier, ~enabled, ~label, ~alwaysShowLabel, ~badge, ~colors: NavigationSuiteItemColors?, ~interactionSource)` |
| `NavigationSuiteScaffold` (composable items) | `(navigationItems: @Composable () -> Unit, ~modifier, ~navigationSuiteType, ~navigationSuiteColors, ~containerColor, ~contentColor, ~state, ~navigationItemVerticalArrangement, ~primaryActionContent, ~primaryActionContentHorizontalAlignment, content)` |
| `NavigationSuiteItem` | `(selected, onClick, icon, label: (() -> Unit)?, ~modifier, ~navigationSuiteType, ~enabled, ~badge, ~colors: NavigationItemColors?, ~interactionSource)` |
| `NavigationSuiteScaffoldDefaults.calculateFromAdaptiveInfo(adaptiveInfo: WindowAdaptiveInfo)`, `.navigationSuiteType(adaptiveInfo)` | return `NavigationSuiteType` |
| `NavigationSuiteType` values | `NavigationBar`, `NavigationRail`, `NavigationDrawer`, `None`, `ShortNavigationBarCompact`, `ShortNavigationBarMedium`, `WideNavigationRailCollapsed`, `WideNavigationRailExpanded` |
| `rememberNavigationSuiteScaffoldState(~initialValue)` | show/hide the navigation component |

- [V] Default behaviour per the guide: navigation bar "if the width or height is compact or if the device is in tabletop
  posture", navigation rail "for everything else". https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation
- The second overload with `NavigationSuiteItem` was added in 1.4.0-alpha12 (release notes) [V].

Window size (`adaptive-1.3.0-beta01.txt`, `window-core-1.5.0-beta01.txt` [V]):

| API | Status |
|---|---|
| `currentWindowAdaptiveInfoV2(): WindowAdaptiveInfo` (`androidx.compose.material3.adaptive`) | stable, added 1.3.0-alpha10 |
| `currentWindowAdaptiveInfo(~supportLargeAndXLargeWidth: Boolean)` | **@Deprecated** in 1.3.0 (release note 1.3.0-alpha10: "Deprecate currentWindowAdaptiveInfo and introduce V2 of it"); still the only form in adaptive 1.2.x |
| `currentWindowSize()`, `currentWindowDpSize()` | **@Deprecated** in 1.3.0 |
| `WindowAdaptiveInfo(windowSizeClass: WindowSizeClass, windowPosture: Posture)` | stable |
| `androidx.window.core.layout.WindowSizeClass`: `minWidthDp`, `minHeightDp`, `isWidthAtLeastBreakpoint(widthDpBreakpoint: Int)`, `isHeightAtLeastBreakpoint(heightDpBreakpoint: Int)`, `isAtLeastBreakpoint(width, height)` | stable |
| Constants on `WindowSizeClass`: `WIDTH_DP_MEDIUM_LOWER_BOUND = 600`, `WIDTH_DP_EXPANDED_LOWER_BOUND = 840`, `WIDTH_DP_LARGE_LOWER_BOUND = 1200`, `WIDTH_DP_EXTRA_LARGE_LOWER_BOUND = 1600`, `HEIGHT_DP_MEDIUM_LOWER_BOUND = 480`, `HEIGHT_DP_EXPANDED_LOWER_BOUND = 900`; `BREAKPOINTS_V1`, `BREAKPOINTS_V2` | stable |
| `WindowWidthSizeClass`, `WindowHeightSizeClass`, `windowWidthSizeClass`, `windowHeightSizeClass`, `WindowSizeClass.compute(dpWidth, dpHeight)` | **@Deprecated** |
| `androidx.compose.material3.windowsizeclass.calculateWindowSizeClass(activity: Activity)` (artifact `material3-window-size-class`) | still `@ExperimentalMaterial3WindowSizeClassApi` in 1.5.0; a separate, older type hierarchy. Prefer the adaptive library. |

- [V] Width classes per the guide: compact < 600dp, medium 600 to 839, expanded 840 to 1199, large 1200 to 1599,
  extra-large >= 1600. "Most apps can build an adaptive UI by considering only the width". https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes
- [V] Contradiction: that guide's snippets call `currentWindowAdaptiveInfo()` and `currentWindowAdaptiveInfo(supportLargeAndXLargeWidth = true)`, both deprecated in adaptive 1.3.0.

Pane scaffolds (`adaptive-layout-1.3.0-beta01.txt`, `adaptive-navigation-1.3.0-beta01.txt` [V]); all `[exp-adaptive]`:

| API | Signature |
|---|---|
| `ListDetailPaneScaffold` | `(directive: PaneScaffoldDirective, scaffoldState: ThreePaneScaffoldState, listPane: ThreePaneScaffoldPaneScope.() -> Unit, detailPane, ~modifier, ~extraPane, ~paneExpansionDragHandle, ~paneExpansionState)`; overload with `value: ThreePaneScaffoldValue` |
| `SupportingPaneScaffold` | `(directive, scaffoldState or value, mainPane, supportingPane, ~modifier, ~extraPane, ~paneExpansionDragHandle, ~paneExpansionState)` |
| `NavigableListDetailPaneScaffold<T>` | `(navigator: ThreePaneScaffoldNavigator<T>, listPane, detailPane, ~modifier, ~extraPane, ~defaultBackBehavior: BackNavigationBehavior, ~paneExpansionDragHandle, ~paneExpansionState)` |
| `NavigableSupportingPaneScaffold<T>` | `(navigator, mainPane, supportingPane, ~modifier, ~extraPane, ~defaultBackBehavior, ...)` |
| `rememberListDetailPaneScaffoldNavigator<T>` | `(~scaffoldDirective, ~adaptStrategies, ~isDestinationHistoryAware, ~initialDestinationHistory)`; non-generic overload returns `ThreePaneScaffoldNavigator<Any>` |
| `ThreePaneScaffoldNavigator<T>` | `suspend navigateTo(pane: ThreePaneScaffoldRole, ~contentKey: T?)`, `suspend navigateBack(~backNavigationBehavior): Boolean`, `canNavigateBack(~backNavigationBehavior)`, `currentDestination: ThreePaneScaffoldDestinationItem<T>?` (has `pane`, `contentKey`), `scaffoldValue`, `scaffoldDirective` |
| `AnimatedPane` | extension on the pane scope: `(~modifier, ~enterTransition, ~exitTransition, ~boundsAnimationSpec, ~dragToResizeHandle, content: AnimatedPaneScope.() -> Unit)` |
| `ListDetailPaneScaffoldRole.List / Detail / Extra`; `SupportingPaneScaffoldRole.Main / Supporting / Extra` | roles |
| `calculatePaneScaffoldDirective(windowAdaptiveInfo, ~verticalHingePolicy)` | |

- [V] Artifacts: `androidx.compose.material3.adaptive:adaptive`, `:adaptive-layout`, `:adaptive-navigation`; 1.3.0 adds
  `adaptive-navigation3` (`ListDetailSceneStrategy`, `rememberListDetailSceneStrategy`, `SupportingPaneSceneStrategy`).
  `navigateTo`/`navigateBack` have been `suspend` since 1.1 (guide requires 1.1.0-beta01+). https://developer.android.com/develop/ui/compose/layouts/adaptive/list-detail

### 2.4 Navigation library

- [V] **Navigation 3** (`androidx.navigation3:navigation3-runtime`, `navigation3-ui`) is stable since 1.0.0 (2025-11-19), now
  1.2.2. Release notes call it "the AndroidX Compose first approach to navigation". The back stack is a list you own.
  https://developer.android.com/guide/navigation/navigation-3
  - `rememberNavBackStack(vararg elements: NavKey): NavBackStack<NavKey>`; keys implement `NavKey` (serializable).
  - `NavDisplay(backStack: List<T>, ~modifier, ~contentAlignment, ~onBack: () -> Unit, ~entryDecorators, ~sceneStrategies: List<SceneStrategy<T>>, ~sceneDecoratorStrategies, ~sharedTransitionScope, ~sizeTransform, ~transitionSpec, ~popTransitionSpec, ~predictivePopTransitionSpec, entryProvider: (T) -> NavEntry<T>)`.
  - `entryProvider { entry<Key> { key -> ... } }`; `NavEntry(key, ~contentKey, ~metadata, content)`.
- [V] **Navigation 2** (`navigation-compose` 2.10.2) remains supported: `NavHost(navController, startDestination..., ~modifier, ~contentAlignment, ~enterTransition, ~exitTransition, ~popEnterTransition, ~popExitTransition, ~predictivePopEnterTransition..., builder)`,
  `rememberNavController()`, type-safe `composable<T>()`, `dialog<T>()`, `navigation<T>(startDestination)`.
- I did not find a sentence on developer.android.com that deprecates Navigation 2; treat "Navigation 3 for new Compose
  apps, keep Navigation 2 in existing apps" as [Conv], not a stated requirement.

## 3. Presentation

| API | Signature (1.5.0) | Status |
|---|---|---|
| `AlertDialog` | `(onDismissRequest, confirmButton, ~modifier, ~dismissButton, ~icon, ~title, ~text, ~shape, ~containerColor, ~iconContentColor, ~titleContentColor, ~textContentColor, ~tonalElevation, ~properties: DialogProperties)` | stable |
| `BasicAlertDialog` | `(onDismissRequest, ~modifier, ~properties, content)` | stable in 1.5.0; `[exp]` in 1.4 |
| `AlertDialog(onDismissRequest, ~modifier, ~properties, content)` | | **@Deprecated**, use `BasicAlertDialog` |
| `ModalBottomSheet` | `(onDismissRequest, ~modifier, ~sheetState: SheetState, ~sheetMaxWidth, ~sheetGesturesEnabled, ~shape, ~containerColor, ~contentColor, ~tonalElevation, ~scrimColor, ~dragHandle, ~contentWindowInsets: () -> WindowInsets, ~properties: ModalBottomSheetProperties, content: ColumnScope.() -> Unit)` | `[exp]` in 1.4, 1.5 and main |
| `rememberBottomSheetState` | `(initialValue: SheetValue, ~enabledValues: Set<SheetValue>, ~confirmValueChange)` | `[exp]`, new in 1.5.0 (1.5.0-alpha20) |
| `rememberModalBottomSheetState(~skipPartiallyExpanded, ~confirmValueChange)`, `rememberStandardBottomSheetState(...)` | | **@Deprecated** `[exp]` in 1.5.0; the only forms in 1.4 |
| `SheetState` | `suspend show() / hide() / expand() / partialExpand()`, `isVisible`, `currentValue`, `targetValue`; `SheetValue`: Hidden, PartiallyExpanded, Expanded | `[exp]` |
| `BottomSheetScaffold` | `(sheetContent, ~modifier, ~scaffoldState, ~sheetPeekHeight, ~sheetMaxWidth, ~sheetShape, ~sheetContainerColor, ~sheetContentColor, ~sheetTonalElevation, ~sheetShadowElevation, ~sheetDragHandle, ~sheetSwipeEnabled, ~topBar, ~snackbarHost, ~containerColor, ~contentColor, content: (PaddingValues) -> Unit)` | `[exp]` |
| `SnackbarHost` | `(hostState: SnackbarHostState, ~modifier, ~snackbar: (SnackbarData) -> Unit)` | stable |
| `SnackbarHostState.showSnackbar` | `suspend (message: String, ~actionLabel: String?, ~withDismissAction: Boolean, ~duration: SnackbarDuration): SnackbarResult`; overload `(visuals: SnackbarVisuals)`. `SnackbarDuration`: Short, Long, Indefinite. `SnackbarResult`: Dismissed, ActionPerformed | stable |
| `Snackbar` | `(~modifier, ~action, ~dismissAction, ~actionOnNewLine, ~shape, ~containerColor, ~contentColor, ~actionContentColor, ~dismissActionContentColor, content)`; overload `(snackbarData, ...)` | stable |
| `DropdownMenu` | `(expanded, onDismissRequest, ~modifier, ~offset: DpOffset, ~scrollState, ~properties: PopupProperties, ~shape, ~containerColor, ~tonalElevation, ~shadowElevation, ~border, content: ColumnScope.() -> Unit)` | stable |
| `DropdownMenuItem` | `(text, onClick, ~modifier, ~leadingIcon, ~trailingIcon, ~enabled, ~colors, ~contentPadding, ~interactionSource)` | stable |
| `DropdownMenuPopup`, `DropdownMenuGroup`, `DropdownMenuItem(onClick, text, shape, ..., ~supportingText)` | expressive menus | stable in 1.5.0; absent in 1.4 |
| `ExposedDropdownMenuBox` | `(expanded, onExpandedChange: (Boolean) -> Unit, ~modifier, content: ExposedDropdownMenuBoxScope.() -> Unit)` | stable in 1.5.0; `[exp]` in 1.4 |
| `Modifier.menuAnchor` (scope member) | `(type: ExposedDropdownMenuAnchorType, ~enabled: Boolean)`; types `PrimaryNotEditable`, `PrimaryEditable`, `SecondaryEditable` | stable in 1.5.0. The no-argument `menuAnchor()` is not in the 1.5.0 file |
| `ExposedDropdownMenu` (scope member) | `(expanded, onDismissRequest, ~modifier, ~scrollState, ~matchAnchorWidth, ~shape, ~containerColor, ~tonalElevation, ~shadowElevation, ~border, content)` | stable in 1.5.0 |
| `ExposedDropdownMenuDefaults.TrailingIcon` | `(expanded: Boolean, ~modifier)` | stable |
| `TooltipBox` | `(positionProvider: PopupPositionProvider, tooltip: TooltipScope.() -> Unit, state: TooltipState, ~modifier, ~onDismissRequest, ~focusable, ~enableUserInput, ~hasAction, content)` | `[exp]` |
| `TooltipScope.PlainTooltip` / `RichTooltip` | `(~modifier, ~caretShape, ~maxWidth, ~shape, ~contentColor, ~containerColor, ...)` / `(~modifier, ~title, ~action, ~caretShape, ..., text)` | `[exp]` |
| `rememberTooltipState` | `(~initialIsVisible, ~isPersistent, ~mutatorMutex)` | `[exp]` |
| `TooltipDefaults.rememberTooltipPositionProvider` | `(positioning: TooltipAnchorPosition, ~spacingBetweenTooltipAndAnchor)` | current; `rememberPlainTooltipPositionProvider`, `rememberRichTooltipPositionProvider` and the overload without `positioning` are **@Deprecated** |
| `DatePickerDialog` | `(onDismissRequest, confirmButton, ~modifier, ~dismissButton, ~shape, ~tonalElevation, ~colors, ~properties, content: ColumnScope.() -> Unit)` | stable |
| `DatePicker` | `(state: DatePickerState, ~modifier, ~dateFormatter, ~colors, ~title, ~headline, ~showModeToggle, ~focusRequester)` | stable |
| `rememberDatePickerState` | `(~initialSelectedDateMillis: Long?, ~initialDisplayedMonthMillis: Long?, ~yearRange: IntRange, ~initialDisplayMode: DisplayMode, ~selectableDates: SelectableDates)`; API 26+ overload taking `LocalDate`/`YearMonth` | stable |
| `DatePickerState` | `selectedDateMillis: Long?` (UTC millis), `displayedMonthMillis`, `displayMode`, `selectableDates`, `yearRange` | stable |
| `DateRangePicker`, `rememberDateRangePickerState` | `(state, ...)`; `(~initialSelectedStartDateMillis, ~initialSelectedEndDateMillis, ...)` | stable |
| `TimePicker` / `TimeInput` | `(state: TimePickerState, ~modifier, ~colors, ~layoutType)` / `(state, ~modifier, ~colors)` | stable in 1.5.0; `[exp]` in 1.4 |
| `rememberTimePickerState` | `(~initialHour: Int, ~initialMinute: Int, ~is24Hour: Boolean)`; state has `hour`, `minute`, `is24hour` | stable in 1.5.0 |
| `TimePickerDialog` | `(onDismissRequest, confirmButton, title, ~modifier, ~properties, ~modeToggleButton, ~dismissButton, ~shape, ~containerColor, content)` | stable (added 1.4.0) |
| `Scrim` | `(contentDescription: String?, ~modifier, ~onClick, ~alpha: () -> Float, ~color)` | stable in 1.5.0 |

- [V] 1.5.0 behaviour change: sheets "no longer automatically remove the PartiallyExpanded anchor based on layout height
  heuristics"; control anchors through `rememberBottomSheetState(enabledValues = ...)`.
- [V] `ModalBottomSheet` supports predictive back on Android 14+ since 1.3.0; `contentWindowInsets` replaced `windowInsets` in 1.3.

## 4. Controls

| API | Signature (1.5.0) | Status |
|---|---|---|
| `Button`, `FilledTonalButton`, `ElevatedButton`, `OutlinedButton`, `TextButton` | `(onClick, ~modifier, ~enabled, ~shape, ~colors: ButtonColors, ~elevation, ~border, ~contentPadding, ~interactionSource, content: RowScope.() -> Unit)`; 1.5 overload `(onClick, shapes: ButtonShapes, ~modifier, ...)` for shape morphing | stable |
| `IconButton` | `(onClick, ~modifier, ~enabled, ~colors, ~interactionSource, ~shape, content)`; overload `(onClick, shapes: IconButtonShapes, ...)` | stable |
| `FilledIconButton`, `FilledTonalIconButton`, `OutlinedIconButton` | `(onClick, ~modifier, ~enabled, ~shape, ~colors, [~border,] ~interactionSource, content)` | stable |
| `IconToggleButton`, `FilledIconToggleButton`, `FilledTonalIconToggleButton`, `OutlinedIconToggleButton` | `(checked, onCheckedChange, ~modifier, ~enabled, ...)` | stable |
| `FloatingActionButton`, `SmallFloatingActionButton`, `MediumFloatingActionButton`, `LargeFloatingActionButton` | `(onClick, ~modifier, ~shape, ~containerColor, ~contentColor, ~elevation, ~interactionSource, content)` | stable (`Medium...` new in 1.5) |
| `ExtendedFloatingActionButton` (also `Small/Medium/LargeExtended...`) | `(text, icon, onClick, ~modifier, ~expanded, ~shape, ~containerColor, ~contentColor, ~elevation, ~interactionSource)`; content overload `(onClick, ..., content: RowScope.() -> Unit)` | stable |
| `FloatingActionButtonMenu` | `(expanded: Boolean, button, ~modifier, ~horizontalAlignment, content: FloatingActionButtonMenuScope.() -> Unit)` | stable in 1.5.0 |
| `FloatingActionButtonMenuItem` (scope ext.) | `(onClick, text, icon, ~modifier, ~containerColor, ~contentColor)` | stable in 1.5.0 |
| `ToggleFloatingActionButton` | `(checked, onCheckedChange, ~modifier, ~containerColor: (Float) -> Color, ~contentAlignment, ~containerSize, ~containerCornerRadius, content)` | stable in 1.5.0 |
| `SplitButtonLayout` | `(leadingButton, trailingButton, ~modifier, ~spacing)` with `SplitButtonDefaults.LeadingButton(onClick, ...)`, `.TrailingButton(checked, onCheckedChange, ...)`, `Tonal*/Outlined*/Elevated*` variants | stable in the 1.5.0-beta01 **and** main files. The 1.5.0 release notes speak of "`SplitButton` ... replacing `SplitButtonLayout`", but no `SplitButton(` function exists in either API file: treat `SplitButton` as unverified |
| `ButtonGroup` | `(overflowIndicator: (ButtonGroupMenuState) -> Unit, ~modifier, ~expandedRatio, ~horizontalArrangement, ~verticalAlignment, content: ButtonGroupScope.() -> Unit)` | stable in 1.5.0 |
| `ToggleButton` (+ `Elevated/Tonal/Outlined`) | `(checked, onCheckedChange, ~modifier, ~buttonSize, ~enabled, ~icon, ~shapes, ~colors, ~elevation, ~border, ~contentPadding, ~interactionSource, content)` | stable in 1.5.0 |
| `SingleChoiceSegmentedButtonRow` / `MultiChoiceSegmentedButtonRow` | `(~modifier, ~space, content)` | stable |
| `SegmentedButton` (single) | `(selected, onClick, shape: Shape, ~modifier, ~enabled, ~colors, ~border, ~contentPadding, ~interactionSource, ~icon, label)`; multi: `(checked, onCheckedChange, shape, ...)`; `SegmentedButtonDefaults.itemShape(index, count)` | stable |
| `Checkbox` | `(checked, onCheckedChange: ((Boolean) -> Unit)?, ~modifier, ~enabled, ~colors, ~interactionSource)` | stable |
| `TriStateCheckbox` | `(state: ToggleableState, onClick: (() -> Unit)?, ~modifier, ~enabled, ~colors, ~interactionSource)` | stable |
| `RadioButton` | `(selected, onClick: (() -> Unit)?, ~modifier, ~enabled, ~colors, ~interactionSource)` | stable |
| `Switch` | `(checked, onCheckedChange: ((Boolean) -> Unit)?, ~modifier, ~thumbContent, ~enabled, ~colors, ~interactionSource)` | stable |
| `Slider` (1.5) | `(state: SliderState, onValueChange: (Float) -> Unit, ~modifier, ~enabled, ~onValueChangeFinished, ~colors, ~interactionSource, ~thumb, ~track)`; `rememberSliderState(~value, ~steps, ~trackRange)` | stable in 1.5.0 |
| `Slider(value: Float, onValueChange, ~modifier, ~enabled, ~valueRange, ~steps, ~onValueChangeFinished, ~colors, ~interactionSource)` | | **@Deprecated** in 1.5.0; the stable form in 1.4 |
| `RangeSlider` (1.5) | `(state: RangeSliderState, onValueChange: (ClosedFloatingPointRange<Float>) -> Unit, ...)`; `rememberRangeSliderState(~startValue, ~endValue, ~steps, ~trackRange)` | stable in 1.5.0; value-based overload deprecated |
| `AssistChip`, `ElevatedAssistChip` | `(onClick, label, ~modifier, ~enabled, ~leadingIcon, ~trailingIcon, ~shape, ~colors, ~elevation, ~border, ~horizontalArrangement, ~contentPadding, ~interactionSource)` | stable |
| `FilterChip`, `ElevatedFilterChip` | `(selected, onClick, label, ~modifier, ~enabled, ~leadingIcon, ~trailingIcon, ~shape, ~colors, ~elevation, ~border, ...)` | stable |
| `InputChip` | `(selected, onClick, label, ~modifier, ~enabled, ~leadingIcon, ~avatar, ~trailingIcon, ...)` | stable |
| `SuggestionChip`, `ElevatedSuggestionChip` | `(onClick, label, ~modifier, ~enabled, ~icon, ...)` | stable |
| `TextField`, `OutlinedTextField` (state) | `(state: TextFieldState, ~modifier, ~enabled, ~readOnly, ~textStyle, ~labelPosition: TextFieldLabelPosition, ~label: (TextFieldLabelScope.() -> Unit)?, ~placeholder, ~leadingIcon, ~trailingIcon, ~prefix, ~suffix, ~supportingText, ~isError, ~inputTransformation, ~outputTransformation, ~keyboardOptions, ~onKeyboardAction: KeyboardActionHandler?, ~lineLimits: TextFieldLineLimits, ~onTextLayout, ~scrollState, ~shape, ~colors, ~contentPadding, ~interactionSource)` | stable (added 1.4.0-alpha01) |
| `TextField`, `OutlinedTextField` (value) | `(value: String or TextFieldValue, onValueChange, ~modifier, ~enabled, ~readOnly, ~textStyle, ~label, ~placeholder, ~leadingIcon, ~trailingIcon, ~prefix, ~suffix, ~supportingText, ~isError, ~visualTransformation, ~keyboardOptions, ~keyboardActions, ~singleLine, ~maxLines, ~minLines, ~interactionSource, ~shape, ~colors)` | stable in 1.5.0; **deprecated in 1.6.0-alpha01** |
| `SecureTextField`, `OutlinedSecureTextField` | `(state: TextFieldState, ..., ~textObfuscationMode, ~textObfuscationCharacter, ...)` | stable (added 1.4.0); default obfuscation is `TextObfuscationMode.System` since 1.5 |
| `TextFieldLabelPosition` | `Above(~alignment)`, `Inside(~isAlwaysMinimized, ...)`, `Cutout(...)`; `Attached` is **@Deprecated** | 1.5.0 |
| `LinearProgressIndicator` | `(~modifier, ~color, ~trackColor, ~strokeCap, ~gapSize)`; determinate `(progress: () -> Float, ~modifier, ~color, ~trackColor, ~strokeCap, ~gapSize, ~drawStopIndicator)` | stable; `progress: Float` overloads **@Deprecated** |
| `CircularProgressIndicator` | `(~modifier, ~color, ~strokeWidth, ~trackColor, ~strokeCap, ~gapSize)`; determinate `(progress: () -> Float, ...)` | stable |
| `LinearWavyProgressIndicator`, `CircularWavyProgressIndicator` | `(~modifier, ~color, ~trackColor, ~stroke, ~trackStroke, ~gapSize, ~amplitude, ~wavelength, ~waveSpeed)`; determinate `(progress: () -> Float, ...)` | stable in 1.5.0 |
| `LoadingIndicator`, `ContainedLoadingIndicator` | `(~modifier, ~color, ~polygons)`; `(progress: () -> Float, ...)` | **`[exp-expressive]`** |
| `Card`, `ElevatedCard`, `OutlinedCard` | `(~modifier, ~shape, ~colors, ~elevation, [~border,] content: ColumnScope.() -> Unit)`; clickable `(onClick, ~modifier, ~enabled, ..., ~interactionSource, content)` | stable |
| `ListItem` (1.5) | `(~modifier, ~enabled, ~leadingContent, ~trailingContent, ~overlineContent, ~supportingContent, ~verticalAlignment, ~shapes, ~colors, ~elevation, ~contentPadding, content)`; clickable `(onClick, ...)`; selectable `(selected, onClick, ...)`; toggleable `(checked, onCheckedChange, ...)`; interactive forms add `~onLongClick, ~onLongClickLabel, ~interactionSource` | stable in 1.5.0; absent in 1.4 |
| `SegmentedListItem` | same four forms with `shapes: ListItemShapes` required; `ListItemDefaults.segmentedShapes(index, count)` | stable in 1.5.0 |
| `ListItem(headlineContent, ~modifier, ~overlineContent, ~supportingContent, ~leadingContent, ~trailingContent, ~colors, ~tonalElevation, ~shadowElevation)` | | **@Deprecated** in 1.5.0; the only form in 1.4 |
| `HorizontalDivider`, `VerticalDivider` | `(~modifier, ~thickness, ~color)` | stable (since 1.2.0-alpha04) |
| `Divider` | | **@Deprecated** |
| `Badge` / `BadgedBox` | `(~modifier, ~containerColor, ~contentColor, ~content)` / `(badge: BoxScope.() -> Unit, ~modifier, content)` | stable |
| `HorizontalMultiBrowseCarousel` | `(state: CarouselState, preferredItemWidth: Dp, ~modifier, ~itemSpacing, ~flingBehavior, ~userScrollEnabled, ~minSmallItemWidth, ~maxSmallItemWidth, ~contentPadding, content: CarouselItemScope.(Int) -> Unit)` | stable in 1.5.0; `[exp]` in 1.4 |
| `HorizontalUncontainedCarousel` | `(state, itemWidth: Dp, ...)`; `HorizontalCenteredHeroCarousel(state, ~modifier, ~preferredItemWidth, ...)`; `rememberCarouselState(~initialItem, itemCount: () -> Int)` | stable in 1.5.0 |
| `PullToRefreshBox` | `(isRefreshing, onRefresh, ~modifier, ~state: PullToRefreshState, ~contentAlignment, ~indicator: BoxScope.() -> Unit, ~enabled, ~threshold, content: BoxScope.() -> Unit)`; `rememberPullToRefreshState()`; `Modifier.pullToRefresh(isRefreshing, state, ~enabled, ~threshold, onRefresh)` | stable (since 1.3.0; `enabled`/`threshold` new in 1.5) |
| `PullToRefreshDefaults.LoadingIndicator(state, isRefreshing, ...)` | | `[exp-expressive]` |
| `SwipeToDismissBox` | `(state: SwipeToDismissBoxState, backgroundContent: RowScope.() -> Unit, ~modifier, ~enableDismissFromStartToEnd, ~enableDismissFromEndToStart, ~gesturesEnabled, ~onDismiss: (SwipeToDismissBoxValue) -> Unit, content: RowScope.() -> Unit)` | stable |
| `rememberSwipeToDismissBoxState` | `(~initialValue, ~positionalThreshold)`; the overload with `confirmValueChange` is **@Deprecated**. Values: `Settled`, `StartToEnd`, `EndToStart` | stable |
| `Icon` | `(imageVector or painter or bitmap, contentDescription: String?, ~modifier, ~tint)` | stable; `contentDescription` has no default |
| `Text` | `(text, ~modifier, ~color, ~autoSize: TextAutoSize?, ~fontSize, ..., ~maxLines, ~minLines, ~onTextLayout, ~style)` | stable (`autoSize` since 1.4.0) |

## 5. System integration

### 5.1 Edge-to-edge and insets

- [API][V] Edge-to-edge is enforced for apps targeting SDK 35 on Android 15+. On an Android 16 device, apps targeting API 36
  cannot opt out: `R.attr#windowOptOutEdgeToEdgeEnforcement` is "deprecated and disabled".
  https://developer.android.com/about/versions/15/behavior-changes-15 , https://developer.android.com/about/versions/16/behavior-changes-16
- [API][V] `setStatusBarColor` and `R.attr#statusBarColor` are deprecated and have no effect on Android 15.
- [V] `ComponentActivity.enableEdgeToEdge(~statusBarStyle: SystemBarStyle, ~navigationBarStyle: SystemBarStyle)` (activity 1.13).
  `SystemBarStyle.auto(lightScrim, darkScrim, ~detectDarkMode)`, `.light(scrim, darkScrim)`, `.dark(scrim)`.
  [Rec] Call it in `onCreate` for backward compatibility; default is transparent bars with a translucent scrim only in
  3-button mode. https://developer.android.com/develop/ui/compose/system/setup-e2e
- [Rec][V] Set `android:windowSoftInputMode="adjustResize"` so the app receives IME insets (same page).
- Insets API (`foundation-layout-1.13.0-beta01.txt` [V]), all stable unless noted:
  - `WindowInsets.safeDrawing`, `.safeGestures`, `.safeContent`, `.systemBars`, `.statusBars`, `.navigationBars`, `.ime`,
    `.displayCutout`, `.captionBar`, `.waterfall`, `.systemGestures`, `.mandatorySystemGestures`, `.tappableElement`,
    `*IgnoringVisibility`, `.imeAnimationSource/Target`, `WindowInsets.isImeVisible`.
  - `Modifier.windowInsetsPadding(insets)`, `.safeDrawingPadding()`, `.safeContentPadding()`, `.safeGesturesPadding()`,
    `.systemBarsPadding()`, `.statusBarsPadding()`, `.navigationBarsPadding()`, `.imePadding()`, `.displayCutoutPadding()`,
    `.captionBarPadding()`, `.waterfallPadding()`.
  - `Modifier.consumeWindowInsets(insets: WindowInsets)` and `(paddingValues: PaddingValues)`,
    `.onConsumedWindowInsetsChanged(block)`, `.windowInsetsTopHeight(insets)`, `.windowInsetsBottomHeight(insets)`,
    `.recalculateWindowInsets()`, `.fitInside(rulers: RectRulers)`, `.fitOutside(rulers)`.
  - `WindowInsets.only(sides)`, `.union`, `.exclude`, `.add`, `.asPaddingValues()`.
  - `Modifier.imeNestedScroll()` is `@ExperimentalLayoutApi`.
- [V] Padding modifiers consume the insets they apply, so nested inset paddings do not double up; size modifiers do not
  consume. https://developer.android.com/develop/ui/compose/system/insets-ui
- [Rec][V] Use `safeDrawing` for content that must not be drawn under any system UI, `safeGestures` for gesture content.
  "The Material 3 Scaffold component can reduce the work required". https://developer.android.com/develop/ui/compose/system/insets
- [V] In desktop windowing every app has a caption bar: use `WindowInsets.systemBars` (includes it) or `WindowInsets.captionBar`.
- [API] `Scaffold(contentWindowInsets = ...)`, bars' `windowInsets` parameters and `ModalBottomSheet(contentWindowInsets = { ... })`
  are how Material components take insets (signatures above).
- Accompanist `systemuicontroller`: not checked in this session (github.com HTML is blocked). [M] it is deprecated in
  favour of `enableEdgeToEdge`.

### 5.2 Back and predictive back

- [V] `BackHandler(~enabled: Boolean, onBack: () -> Unit)` and
  `PredictiveBackHandler(~enabled: Boolean, onBack: suspend (progress: Flow<BackEventCompat>) -> Unit)` in
  `androidx.activity.compose` (activity 1.13 and main; neither deprecated).
- [API][V] Predictive back-to-home arrived in Android 13 (developer option), in-app predictive back in Android 14. For apps
  targeting Android 16 on an Android 16+ device the predictive system animations are on by default; opt out with
  `android:enableOnBackInvokedCallback="false"` (application or activity). Intercepting `KeyEvent.KEYCODE_BACK` or
  `onBackPressed` is "no longer supported". https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture
- [V] Material Compose components with predictive back: `ModalBottomSheet`, `SearchBar` (1.3.0), `ModalDrawerSheet` /
  `DismissibleDrawerSheet` via the `drawerState` overload (1.3.0). `NavHost` and `NavDisplay` have `predictivePop*` transition parameters.
- [V] Views: MDC-Android 1.10.0+ gives predictive back for search bar, modal bottom sheet, side sheet and navigation
  drawer once the app migrates to back callbacks. https://raw.githubusercontent.com/material-components/material-components-android/master/docs/foundations/PredictiveBack.md

### 5.3 Touch target, ripple, haptics

- [V] `Modifier.minimumInteractiveComponentSize()` is stable. `LocalMinimumInteractiveComponentSize:
  ProvidableCompositionLocal<Dp>` is stable (introduced 1.3.0-alpha04) and replaces
  `LocalMinimumInteractiveComponentEnforcement` (**@Deprecated** `[exp]` in 1.5.0). `LocalMinimumTouchTargetEnforcement` exists
  only in M2 (`androidx.compose.material`); it is not in any M3 file since it was deprecated in 1.1.0-alpha06.
- [Rec][V] "set the minimum size to 48dp"; Material components such as `Checkbox`, `RadioButton`, `Switch`, `Slider`,
  `Surface` set it internally "but only when the component can receive user actions" (a `Checkbox` with
  `onCheckedChange = null` gets no padding). `minimumInteractiveComponentSize` "reserves at least 48 dp of layout space in
  each dimension"; "Put it before any size modifier". https://developer.android.com/develop/ui/compose/accessibility/api-defaults
- [V] Ripple: `ripple(~bounded, ~radius, ~color, ...)` in `androidx.compose.material3` is a non-composable factory returning
  `IndicationNodeFactory` (added 1.3.0-alpha01). `rememberRipple` (in `material-ripple`) is **@Deprecated**; `RippleTheme`
  and `LocalRippleTheme` are no longer queried by Material components.
  `LocalRippleConfiguration: ProvidableCompositionLocal<RippleConfiguration?>`: provide `null` to disable a ripple
  (1.3.0-alpha06). 1.5.0 adds `LocalRippleThemeConfiguration` / `RippleThemeConfiguration` (inset focus rings) and the
  `material3-ripple` artifact. https://developer.android.com/develop/ui/compose/touch-input/user-interactions/migrate-indication-ripple
- [V] Haptics in Compose: `LocalHapticFeedback.current.performHapticFeedback(type)`; `HapticFeedbackType` in ui 1.13:
  `Confirm`, `ContextClick`, `GestureEnd`, `GestureThresholdActivate`, `KeyboardTap`, `LongPress`, `Reject`,
  `SegmentFrequentTick`, `SegmentTick`, `TextHandleMove`, `ToggleOff`, `ToggleOn`, `VirtualKey`.
  `Modifier.combinedClickable(..., ~hapticFeedbackEnabled, ...)`.
- [V] Views: `View.performHapticFeedback(HapticFeedbackConstants.X)` needs no `VIBRATE` permission and honours the system
  setting. https://developer.android.com/develop/ui/views/haptics/haptic-feedback

## 6. Accessibility in Compose

Sources: `ui-1.13.0-beta01.txt`, `foundation-1.13.0-beta01.txt` [V]; guides under https://developer.android.com/develop/ui/compose/accessibility

| Need | API (verified) |
|---|---|
| Add or override semantics | `Modifier.semantics(~mergeDescendants: Boolean = false, properties: SemanticsPropertyReceiver.() -> Unit)` |
| Replace all descendant semantics | `Modifier.clearAndSetSemantics(properties)` |
| Label a graphic | `Icon(..., contentDescription = ...)`, `Image(..., contentDescription = ...)`, or `contentDescription = "..."` in `semantics {}` |
| Decorative graphic | `contentDescription = null` |
| Hide from accessibility services | `hideFromAccessibility()`; `invisibleToUser()` is **@Deprecated** |
| State text | `stateDescription = "..."` |
| Role | `role = Role.X`; `Role`: `Button`, `Checkbox`, `Switch`, `RadioButton`, `Tab`, `Image`, `DropdownList`, `ValuePicker`, `Carousel` |
| Heading | `heading()` |
| Live region | `liveRegion = LiveRegionMode.Polite` or `.Assertive` |
| Pane or window title | `paneTitle = "..."` |
| Custom actions | `customActions = listOf(CustomAccessibilityAction(label: String, action: () -> Boolean))` |
| Traversal order | `isTraversalGroup = true`, `traversalIndex = -1f`; `isContainer` is **@Deprecated** |
| Error | `error(description: String)` |
| Selection, toggle, progress | `selected`, `toggleableState`, `progressBarRangeInfo`, `selectableGroup()`, `collectionInfo`, `collectionItemInfo` |
| Click with label and role | `Modifier.clickable(~enabled, ~onClickLabel: String?, ~role: Role?, ~interactionSource, onClick)` |
| Toggle or select a whole row | `Modifier.toggleable(value, ~enabled, ~role, ~interactionSource, onValueChange)`, `Modifier.selectable(selected, ~enabled, ~role, ~interactionSource, onClick)`, `Modifier.triStateToggleable(state, ...)` |
| Long press with label | `Modifier.combinedClickable(~enabled, ~onClickLabel, ~role, ~onLongClickLabel, ~onLongClick, ~onDoubleClick, ~hapticFeedbackEnabled, ~interactionSource, onClick)` |
| UI Automator ids | `testTagsAsResourceId = true` |

Guidance:
- [Rec][V] `contentDescription` is "mainly meant to be used for graphic elements"; give a localized description, or `null`
  when the element is decorative. The guide's row example nulls the child control's callback (`Checkbox(checked,
  onCheckedChange = null)`) and puts `toggleable(role = Role.Checkbox)` on the parent row.
- [Rec][V] Use `LiveRegionMode.Polite` in most cases, `Assertive` "sparingly".
- [V] `clickable`, `toggleable` and `selectable` merge descendants; use `semantics(mergeDescendants = true)` to group a
  non-interactive block; `clearAndSetSemantics` drops children's semantics. https://developer.android.com/develop/ui/compose/accessibility/merging-clearing
- [V] `ModalBottomSheet` is first in traversal order, followed by the scrim (1.3.0).
- [Rec] Font scaling: text sizes in `sp` through `MaterialTheme.typography`; do not fix heights around text
  (`heightIn(min = ...)` instead of `height(...)`). The `sp` vs `dp` behaviour is [M] here (not re-fetched); non-linear font
  scaling up to 200% on Android 14 is [M].

Testing (`ui-test-1.13.0-beta01.txt`, `a11y-test-main.txt` [V]):
- Finders and matchers: `onNodeWithText`, `onNodeWithContentDescription`, `onNodeWithTag`, `hasText`, `hasContentDescription`,
  `hasStateDescription`, `hasClickAction`, `isHeading()`, `isToggleable()`, `isSelectable()`, `isOn()`, `isOff()`,
  `isSelected()`, `isFocused()`, `isDialog()`, `isPopup()`, `isHiddenFromAccessibility()`, `hasProgressBarRangeInfo`.
- Assertions: `assertIsDisplayed`, `assertIsEnabled`, `assertIsOn/Off`, `assertIsSelected`, `assertContentDescriptionEquals`,
  `assertTextEquals`, `assertHasClickAction`, `assertTouchWidthIsEqualTo`, `assertTouchHeightIsEqualTo`,
  `assertWidthIsAtLeast`, `assertHeightIsAtLeast`.
- Actions: `performClick`, `performTextInput`, `performScrollTo`, `performSemanticsAction`,
  `performCustomAccessibilityActionWithLabel(label)` (`@ExperimentalTestApi`).
- Accessibility checks: `ComposeUiTest.enableAccessibilityChecks(~accessibilityValidator)` and `disableAccessibilityChecks()`
  (`@RequiresApi(34)`, artifact `androidx.compose.ui:ui-test-accessibility`; rule variant in
  `ui-test-junit4-accessibility`), then any action or `tryPerformAccessibilityChecks()` on a node. Available "starting with
  Compose 1.8.0"; checks cover missing labels, colour contrast, small touch targets, traversal order.
  https://developer.android.com/develop/ui/compose/accessibility/testing . The older `GlobalAssertions` API was removed.
- [Rec][V] Manual testing with TalkBack and Switch Access is called "essential" by the same page.

## 7. Deprecated, renamed and commonly hallucinated API

"Absent" means zero occurrences in `m3-1.4.0-beta03.txt`, `m3-1.5.0-beta01.txt` and `m3-main.txt` [V].

| Stale or wrong | Reality | Use instead |
|---|---|---|
| `import androidx.compose.material.*` (M2) mixed with M3 | M2 is still published (1.13.0) but has a separate theme. Guide: "you should not use both M2 and M3 in a single app long-term" | `androidx.compose.material3.*` only |
| `BottomNavigation`, `BottomNavigationItem` | M2 only; absent from M3 | `NavigationBar`, `NavigationBarItem` (or `ShortNavigationBar`, `NavigationSuiteScaffold`) |
| `Scaffold(scaffoldState = rememberScaffoldState())`, `drawerContent =`, `backgroundColor =` | M2 only; M3 Scaffold has no `scaffoldState` or drawer parameters | `SnackbarHostState` + `snackbarHost = { SnackbarHost(it) }`; `ModalNavigationDrawer`; `containerColor` |
| `MaterialTheme.colors`, `Colors`, `lightColors()` | M2 | `MaterialTheme.colorScheme`, `lightColorScheme()` |
| `ContentAlpha`, `LocalContentAlpha` | M2 only | colour roles such as `onSurfaceVariant` |
| `SmallTopAppBar`, `TopAppBarDefaults.smallTopAppBarColors` | absent (deprecated 1.0.0-beta02) | `TopAppBar`, `TopAppBarDefaults.topAppBarColors()` |
| `Divider` | deprecated (renamed 1.2.0-alpha04) | `HorizontalDivider`, `VerticalDivider` |
| `TabRow`, `ScrollableTabRow`, `Modifier.tabIndicatorOffset` | deprecated | `PrimaryTabRow`, `SecondaryTabRow`, `Primary/SecondaryScrollableTabRow` |
| `SwipeToDismiss`, `rememberDismissState`, `DismissValue`, `DismissDirection` | M2 only now; renamed in M3 1.2.0 | `SwipeToDismissBox`, `rememberSwipeToDismissBoxState`, `SwipeToDismissBoxValue` |
| `rememberSwipeToDismissBoxState(confirmValueChange = ...)` | deprecated in 1.5.0 | `SwipeToDismissBox(onDismiss = ...)` |
| `ModalBottomSheetLayout`, `rememberModalBottomSheetState(ModalBottomSheetValue.Hidden)` | M2 only | `ModalBottomSheet` + `rememberBottomSheetState` (1.5) or `rememberModalBottomSheetState()` (<= 1.4) |
| `rememberModalBottomSheetState(skipPartiallyExpanded = true)` | deprecated in 1.5.0 | `rememberBottomSheetState(initialValue = SheetValue.Hidden, enabledValues = ...)` |
| `Modifier.pullRefresh`, `rememberPullRefreshState`, `PullRefreshIndicator` | M2 experimental (`androidx.compose.material.pullrefresh`) | `PullToRefreshBox(isRefreshing, onRefresh)` |
| `PullToRefreshContainer`, `state.nestedScrollConnection` | absent (1.2.0 API, replaced in 1.3.0) | `PullToRefreshBox` or `Modifier.pullToRefresh` |
| `LocalMinimumTouchTargetEnforcement` | M2 only | `LocalMinimumInteractiveComponentSize` |
| `LocalMinimumInteractiveComponentEnforcement` | deprecated since 1.3.0-alpha04 | `LocalMinimumInteractiveComponentSize provides Dp.Unspecified` to opt out ([M] for the exact opt-out value) |
| `rememberRipple()`, `RippleTheme`, `LocalRippleTheme` | deprecated; not used by Material | `ripple()`, `LocalRippleConfiguration` |
| `SearchBar(query, onQueryChange, onSearch, active, onActiveChange)`, `DockedSearchBar` | deprecated | `SearchBar(state, inputField)` + `ExpandedFullScreenSearchBar` / `ExpandedDockedSearchBar` |
| `PlainTooltipBox`, `RichTooltipBox` | absent | `TooltipBox` + `PlainTooltip` / `RichTooltip` |
| `Modifier.menuAnchor()` with no argument, `MenuAnchorType` | not in 1.5.0 | `Modifier.menuAnchor(ExposedDropdownMenuAnchorType.PrimaryNotEditable)` |
| `ExposedDropdownMenuBox` needs opt-in | only up to 1.4 | stable in 1.5.0 |
| `ListItem(headlineContent = { ... })` | deprecated in 1.5.0 | `ListItem(...) { headline }` (trailing `content`) |
| `Slider(value = v, onValueChange = ...)` | deprecated in 1.5.0 | `Slider(state = rememberSliderState(...), onValueChange = ...)` |
| `LinearProgressIndicator(progress = 0.5f)` | deprecated | `progress = { 0.5f }` |
| `AlertDialog(onDismissRequest) { content }` | deprecated | `BasicAlertDialog` |
| `TextFieldLabelPosition.Attached` | deprecated | `Inside` or `Cutout` |
| `Icons.Filled.*`, `Icons.Default.*`, `material-icons-extended` | library frozen at 1.7.8; "no longer maintained or recommended"; not a transitive dependency since material3 1.4.0 | vector drawable XML from https://fonts.google.com/icons + `painterResource(R.drawable.x)` |
| `Icons.Filled.ArrowBack` in RTL | auto-mirrored variants exist as `Icons.AutoMirrored.Filled.*` (compose-material notes) | a Material Symbols drawable with `android:autoMirrored="true"` ([M] for the attribute) |
| `calculateWindowSizeClass(activity)`, `WindowWidthSizeClass.Compact` | first is still experimental; second (window-core) deprecated | `currentWindowAdaptiveInfoV2().windowSizeClass.isWidthAtLeastBreakpoint(WindowSizeClass.WIDTH_DP_MEDIUM_LOWER_BOUND)` |
| `currentWindowAdaptiveInfo()` | deprecated in adaptive 1.3.0 | `currentWindowAdaptiveInfoV2()` |
| `navigator.navigateTo(...)` called outside a coroutine | `suspend` since adaptive 1.1 | `scope.launch { navigator.navigateTo(...) }` |
| Accompanist `rememberSystemUiController().setStatusBarColor` | [M] deprecated; status bar colour has no effect on Android 15 [V] | `enableEdgeToEdge()` + insets |
| `window.statusBarColor = ...`, `android:statusBarColor` | deprecated, no effect on Android 15 | draw your own background behind the bar |
| `onBackPressed()` override, `KEYCODE_BACK` interception | not supported with predictive back | `BackHandler`, `PredictiveBackHandler`, `OnBackPressedCallback` |
| `FlowRow` needs `@OptIn(ExperimentalLayoutApi::class)` | stable overload exists in foundation-layout 1.13; the overload with `overflow` is deprecated | `FlowRow(...)` |
| `BasicTextField(value, onValueChange)` | deprecated in foundation 1.13 | `BasicTextField(state: TextFieldState, ...)` |
| `Modifier.semantics { invisibleToUser() }`, `isContainer = true` | deprecated | `hideFromAccessibility()`, `isTraversalGroup = true` |
| `expressiveDarkColorScheme()`, `SplitButton(...)`, `LocalMotionScheme` | none exist in the 1.5.0 or main files | `expressiveLightColorScheme()` only; `SplitButtonLayout`; `MaterialTheme.motionScheme` |
| "Surface tints with elevation" as the M3 look | `surfaceColorAtElevation` still exists, but `surfaceContainer*` roles are in `ColorScheme` | `surfaceContainerLowest ... surfaceContainerHighest` |

## 8. Views (Material Components for Android)

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/ (all [V] unless tagged).

Setup:
- Dependency `com.google.android.material:material:<version>`; Material3 themes need 1.5.0+; `Theme.Material3Expressive.*`
  and `Widget.Material3Expressive.*` need 1.14.0+ (`getting-started.md`). compileSdk 36.1+, minSdk 23+, AGP 8.13+.
- Since 1.13.0-alpha12 R classes are non-transitive: AppCompat attributes are `androidx.appcompat.R.attr.colorPrimary`,
  Material ones `com.google.android.material.R.attr.colorOnPrimary`.
- Use `AppCompatActivity` (or `AppCompatDelegate`) so Material widgets are inflated.

Theme parents:

| Material3 Expressive | Material3 | Legacy `MaterialComponents` |
|---|---|---|
| `Theme.Material3Expressive.DayNight(.NoActionBar)` | `Theme.Material3.DayNight(.NoActionBar)` | `Theme.MaterialComponents.DayNight(.NoActionBar)` |
| `Theme.Material3Expressive.Light(.NoActionBar)` | `Theme.Material3.Light(.NoActionBar)` | `Theme.MaterialComponents.Light(.NoActionBar)` |
| `Theme.Material3Expressive.Dark(.NoActionBar)` | `Theme.Material3.Dark(.NoActionBar)` | `Theme.MaterialComponents(.NoActionBar)` |
| `Theme.Material3Expressive.DynamicColors.DayNight / Light / Dark (.NoActionBar)` | `Theme.Material3.DynamicColors.DayNight / Light / Dark (.NoActionBar)` | N/A |

Dynamic colour (`docs/theming/Color.md`): `DynamicColors.applyToActivitiesIfAvailable(application)` in
`Application.onCreate` (overloads with a theme overlay, a precondition, or `DynamicColorsOptions`);
`DynamicColors.applyToActivityIfAvailable(activity)`; `DynamicColors.wrapContextIfAvailable(context)`; overlays
`ThemeOverlay.Material3.DynamicColors.Light / Dark / DayNight`; `MaterialColors.harmonizeWithPrimary(context, color)`.

Compose to Views mapping (class names from the component docs):

| Component | Compose (material3 1.5.0) | Views (MDC-Android) | Doc |
|---|---|---|---|
| Navigation bar | `NavigationBar` / `NavigationBarItem` | `BottomNavigationView` (base `NavigationBarView`; `setOnItemSelectedListener`; expressive style `Widget.Material3Expressive.BottomNavigationView`) | `components/BottomNavigation.md` |
| Navigation rail | `NavigationRail`, `WideNavigationRail` | `NavigationRailView` | `components/NavigationRail.md` |
| Navigation drawer | `ModalNavigationDrawer` + `ModalDrawerSheet` | `DrawerLayout` + `NavigationView` | `components/NavigationDrawer.md` |
| Top app bar | `TopAppBar`, `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar` | `AppBarLayout` + `MaterialToolbar` (+ `CollapsingToolbarLayout`) in a `CoordinatorLayout`; the non-flexible Medium and Large variants are "being deprecated" | `components/TopAppBar.md` |
| Tabs | `PrimaryTabRow` + `Tab` | `TabLayout` | `components/Tabs.md` |
| Search | `SearchBar` + `ExpandedFullScreenSearchBar` | `SearchBar` + `SearchView` | `components/Search.md` |
| Buttons | `Button`, `FilledTonalButton`, `OutlinedButton`, `TextButton`, `ElevatedButton` | `MaterialButton` with a `Widget.Material3.Button.*` style | `components/CommonButton.md` |
| Icon button | `IconButton` family | `MaterialButton` with an icon-button style | `components/IconButton.md` |
| Button group, split button | `ButtonGroup`, `SplitButtonLayout` | `MaterialButtonGroup`, `MaterialSplitButton` | `components/ButtonGroup.md`, `SplitButton.md` |
| FAB | `FloatingActionButton`, `ExtendedFloatingActionButton` | `FloatingActionButton`, `ExtendedFloatingActionButton` | `components/FloatingActionButton.md` |
| FAB menu | `FloatingActionButtonMenu` | no View class: the doc tells you to host the Compose component in a `ComposeView` | `components/FloatingActionButtonMenu.md` |
| Text field | `TextField`, `OutlinedTextField` | `TextInputLayout` + `TextInputEditText` (`app:helperText`, `setError`, `app:endIconMode`, `app:errorAccessibilityLiveRegion`) | `components/TextField.md` |
| Exposed dropdown | `ExposedDropdownMenuBox` | `TextInputLayout` + `MaterialAutoCompleteTextView` | `components/Menu.md` |
| Dialog | `AlertDialog` | `MaterialAlertDialogBuilder` | `components/Dialog.md` |
| Bottom sheet | `ModalBottomSheet`, `BottomSheetScaffold` | `BottomSheetDialogFragment` / `BottomSheetDialog`, `BottomSheetBehavior`, `BottomSheetDragHandleView` (48dp minimum) | `components/BottomSheet.md` |
| Side sheet | (none in material3 1.5.0 stable) | `SideSheetDialog`, `SideSheetBehavior` | `components/SideSheet.md` |
| Snackbar | `SnackbarHost` + `SnackbarHostState` | `Snackbar.make(view, text, duration)` | `components/Snackbar.md` |
| Checkbox, radio, switch | `Checkbox`, `RadioButton`, `Switch` | `MaterialCheckBox`, `MaterialRadioButton`, `MaterialSwitch` (`SwitchMaterial` is the deprecated one; `MaterialSwitch` does not auto-inflate) | `components/Checkbox.md`, `RadioButton.md`, `Switch.md` |
| Slider | `Slider`, `RangeSlider` | `Slider`, `RangeSlider` | `components/Slider.md` |
| Chips | `AssistChip`, `FilterChip`, `InputChip`, `SuggestionChip` | `Chip`, `ChipGroup` (`app:ensureMinTouchTargetSize`, default 48dp) | `components/Chip.md` |
| Card | `Card`, `ElevatedCard`, `OutlinedCard` | `MaterialCardView` | `components/Card.md` |
| List item | `ListItem`, `SegmentedListItem` | `ListItemLayout`, `ListItemCardView` in a `RecyclerView` | `components/List.md` |
| Divider | `HorizontalDivider` | `MaterialDivider`, `MaterialDividerItemDecoration` | `components/Divider.md` |
| Progress, loading | `LinearProgressIndicator`, `CircularProgressIndicator`, `LoadingIndicator` | `LinearProgressIndicator`, `CircularProgressIndicator`, `LoadingIndicator` | `components/ProgressIndicator.md`, `LoadingIndicator.md` |
| Date, time picker | `DatePickerDialog` + `DatePicker`, `TimePickerDialog` + `TimePicker` | `MaterialDatePicker.Builder`, `MaterialTimePicker.Builder` | `components/DatePicker.md`, `TimePicker.md` |
| Toolbars | `HorizontalFloatingToolbar`, `FlexibleBottomAppBar` | `FloatingToolbarLayout`, `DockedToolbarLayout` | `components/FloatingToolbar.md`, `DockedToolbar.md` |
| Carousel | `HorizontalMultiBrowseCarousel` | `RecyclerView` + `CarouselLayoutManager` ([M] for the manager name) + `MaskableFrameLayout` | `components/Carousel.md` |
| Badge | `BadgedBox` + `Badge` | `BadgeDrawable` | `components/BottomNavigation.md` |

Views notes:
- [V] Edge-to-edge: set `android:fitsSystemWindows="true"` on `AppBarLayout` (or `MaterialToolbar`); `BottomSheetBehavior`
  can handle insets itself. General guidance: https://developer.android.com/develop/ui/views/layout/edge-to-edge
- [V] `BottomNavigationView#setOnNavigationItemSelectedListener` is deprecated in favour of the `NavigationBarView` listeners.
- [V] Touch target: `?attr/minTouchTargetSize` (checkbox), `app:chipMinTouchTargetSize`.
- Not verified here: `BottomAppBar` View class docs, `MaterialToolbar` menu APIs, the exact `Widget.Material3.Button.*` style names.

## 9. Implementation anti-patterns

Fix column uses APIs verified above. Source keys: G-M3 = .../compose/designsystems/material3 ; G-M2M3 =
.../designsystems/material2-material3 ; G-A11Y = .../compose/accessibility/api-defaults ; G-INS = .../compose/system/insets ;
G-E2E = .../compose/system/setup-e2e ; G-WSC = .../layouts/adaptive/use-window-size-classes ; G-NAV =
.../layouts/adaptive/build-adaptive-navigation ; RN = material3 release notes ; API = cached API files (all under
https://developer.android.com/develop/ui except RN and API).

| # | Anti-pattern | Fix | Source |
|---|---|---|---|
| 1 | `Color(0xFF6200EE)` or `Color.White` in composables | `MaterialTheme.colorScheme.primary` etc.; pair `x` with `onX` | G-M3 [V] |
| 2 | Custom dark-mode `if` around hard-coded colours | one `ColorScheme` per mode chosen in the theme with `isSystemInDarkTheme()` | G-M3 [V] |
| 3 | `dynamicLightColorScheme(context)` without an API check | gate on `Build.VERSION_CODES.S`, fall back to a static scheme | API `@RequiresApi(S)` [V] |
| 4 | `fontSize = 14.dp`-style fixed sizes or ad-hoc `fontSize = 13.sp` everywhere | `style = MaterialTheme.typography.bodyMedium` | G-M3 [V]; sp scaling [M] |
| 5 | `Modifier.height(48.dp)` on a row or button containing text | `heightIn(min = 48.dp)` and let text wrap | [Conv]; RN fixes for clipping at large font scale [V] |
| 6 | `Modifier.clickable { }` without `role` or `onClickLabel` on a custom control | `clickable(onClickLabel = ..., role = Role.Button)` or use `Button`/`IconButton`/`Surface(onClick)` | API, G-A11Y [V] |
| 7 | 24dp icon with `clickable` only | `IconButton`, or `.clickable{}.minimumInteractiveComponentSize().size(24.dp)` | G-A11Y [V] |
| 8 | `Icon(..., contentDescription = null)` inside an `IconButton` without a label | localized `contentDescription`; `null` only for decorative icons | G-A11Y [V] |
| 9 | `Checkbox(checked, onCheckedChange)` next to a separately clickable `Text` | row with `toggleable(value, role = Role.Checkbox)` and child `onCheckedChange = null` | G-A11Y [V] |
| 10 | Custom `Row` bottom bar | `NavigationBar` + `NavigationBarItem` or `NavigationSuiteScaffold` | G-NAV [V] |
| 11 | Bottom bar on every window size | `NavigationSuiteScaffold` (bar when compact, rail otherwise) | G-NAV [V] |
| 12 | `LocalConfiguration.current.screenWidthDp > 600` or device-type checks | `currentWindowAdaptiveInfoV2().windowSizeClass.isWidthAtLeastBreakpoint(...)` | G-WSC, API [V] |
| 13 | Locking orientation or `resizeableActivity=false` | adaptive layouts; restrictions are ignored on displays >= 600dp for apps targeting API 36 | behavior-changes-16 [V] |
| 14 | Ignoring `innerPadding` from `Scaffold` | `Modifier.padding(innerPadding)` or `contentPadding = innerPadding` | API [V]; lint name [M] |
| 15 | Adding `statusBarsPadding()` inside a Scaffold that already applies insets | rely on Scaffold; `consumeWindowInsets(innerPadding)` for children | insets-ui guide [V] |
| 16 | No inset handling when targeting SDK 35+ | `enableEdgeToEdge()` + Scaffold or `safeDrawingPadding()` | G-INS, G-E2E [V] |
| 17 | `window.statusBarColor = ...` or Accompanist system UI controller | `enableEdgeToEdge(statusBarStyle = ...)`; draw backgrounds yourself | behavior-changes-15 [V] |
| 18 | Form field hidden by the keyboard | `adjustResize` + `imePadding()` (or Scaffold/sheet `contentWindowInsets`) | G-E2E [V] |
| 19 | Mixing `androidx.compose.material.*` and `material3.*` | migrate imports; one `MaterialTheme` | G-M2M3 [V] |
| 20 | `Divider()`, `TabRow`, `SmallTopAppBar`, `SwipeToDismiss` | see section 7 | API [V] |
| 21 | `rememberRipple()` or custom `RippleTheme` | `ripple()`, `LocalRippleConfiguration` | migrate-indication-ripple [V] |
| 22 | `Icons.Filled.X` from `material-icons-extended` | Material Symbols vector drawable + `painterResource` | images/material guide, RN 1.4.0 [V] |
| 23 | Error shown only by red colour | `isError = true` + `supportingText = { Text(message) }` | API [V]; [Conv] |
| 24 | Placeholder used as the only label | `label = { Text(...) }` | API [V]; [Conv] |
| 25 | Password in a plain `TextField` with `PasswordVisualTransformation` | `SecureTextField` / `OutlinedSecureTextField` (material3 1.4.0+) | RN 1.4.0 [V] |
| 26 | Snackbar shown with a custom `Box` overlay | `Scaffold(snackbarHost = { SnackbarHost(state) })` + `showSnackbar` | API [V] |
| 27 | `showSnackbar` or `sheetState.hide()` called outside a coroutine | `scope.launch { ... }` (both are `suspend`) | API [V] |
| 28 | Dialog built from `Dialog { Surface { ... } }` for a simple confirm | `AlertDialog(onDismissRequest, confirmButton, dismissButton, title, text)` | API [V] |
| 29 | Hand-rolled date field with three text inputs | `DatePickerDialog` + `DatePicker` | API [V] |
| 30 | Custom pull-to-refresh or M2 `pullRefresh` | `PullToRefreshBox` | API, RN 1.3.0 [V] |
| 31 | Overriding `onBackPressed` or swallowing back with an always-enabled `BackHandler` | `BackHandler(enabled = condition)`; let the system handle the rest | predictive-back guide [V] |
| 32 | `LocalMinimumInteractiveComponentEnforcement provides false` app-wide to tighten layouts | keep the 48dp reservation; use it only for a justified dense subtree via `LocalMinimumInteractiveComponentSize` | API, G-A11Y [V] |
| 33 | `Modifier.semantics { contentDescription = "Button" }` duplicating role or state | set `role`, `stateDescription`; let the node's text be the label | semantics guide [V] |
| 34 | Clickable list row whose children are announced separately | `clickable`/`toggleable` on the row (merges descendants) or `ListItem(onClick = ...)` | merging-clearing guide, API [V] |
| 35 | Section titles as plain `Text` | `Modifier.semantics { heading() }` | semantics guide [V] |
| 36 | Opt-in sprayed file-wide (`@file:OptIn(ExperimentalMaterial3Api::class)`) on material3 1.5 | remove; opt in only where an API is still `[exp]` (sheets, tooltips) | API [V] |
| 37 | `ModalBottomSheet` shown with `if (state.isVisible)` and no `onDismissRequest` state update | own a `showSheet` boolean; hide with `scope.launch { state.hide() }.invokeOnCompletion { showSheet = false }` | [Conv]; API [V] |
| 38 | `TextField` hoisted through `value`/`onValueChange` in new code on 1.6 alphas | `rememberTextFieldState()` + state overload | RN 1.6.0-alpha01 [V] |
| 39 | Views: `Theme.AppCompat` or `Theme.MaterialComponents` parent with M3 widgets | `Theme.Material3.DayNight.NoActionBar` (or `Material3Expressive`) | getting-started.md [V] |
| 40 | Views: `SwitchMaterial`, `setOnNavigationItemSelectedListener` | `MaterialSwitch`, `setOnItemSelectedListener` | Switch.md, BottomNavigation.md [V] |

## 10. Conservative Compose examples

Not compiled. Assumptions for all: Compose BOM 2026.11.01, material3 **1.5.0**, activity-compose 1.13.0. Each call was
checked against the cached API files. Notes say what changes on material3 1.4.x. Imports are omitted except where the
package is easy to get wrong.

### 10.1 Adaptive navigation (stable; artifact `material3-adaptive-navigation-suite` 1.5.0)

```kotlin
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold

enum class TopLevel(@StringRes val label: Int, @DrawableRes val icon: Int) {
    Home(R.string.home, R.drawable.ic_home), Search(R.string.search, R.drawable.ic_search),
    Profile(R.string.profile, R.drawable.ic_person)
}

@Composable
fun AppShell() {
    var current by rememberSaveable { mutableStateOf(TopLevel.Home) }
    NavigationSuiteScaffold(
        navigationSuiteItems = {
            TopLevel.entries.forEach { dest ->
                item(
                    selected = dest == current,
                    onClick = { current = dest },
                    icon = { Icon(painterResource(dest.icon), contentDescription = null) }, // label names it
                    label = { Text(stringResource(dest.label)) },
                )
            }
        },
    ) {
        when (current) { TopLevel.Home -> HomeScreen(); TopLevel.Search -> SearchScreen(); TopLevel.Profile -> ProfileScreen() }
    }
}
```

### 10.2 List-detail (experimental: `ExperimentalMaterial3AdaptiveApi`; adaptive 1.3.0, also valid on 1.1+)

```kotlin
@OptIn(ExperimentalMaterial3AdaptiveApi::class)
@Composable
fun MailScreen(mails: List<Mail>) {
    val navigator = rememberListDetailPaneScaffoldNavigator<String>()
    val scope = rememberCoroutineScope()
    NavigableListDetailPaneScaffold(
        navigator = navigator,
        listPane = {
            AnimatedPane {
                MailList(mails, onOpen = { id ->
                    scope.launch { navigator.navigateTo(ListDetailPaneScaffoldRole.Detail, id) }
                })
            }
        },
        detailPane = {
            AnimatedPane {
                val id = navigator.currentDestination?.contentKey
                if (id != null) MailDetail(id) else EmptyDetail()
            }
        },
    )
}
```
Back handling is built in (`defaultBackBehavior`). One pane shows in compact width, two when the directive allows.

### 10.3 Theme with dynamic colour fallback (stable)

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> AppDarkColors   // darkColorScheme(primary = ..., ...)
        else -> AppLightColors       // lightColorScheme(primary = ..., ...)
    }
    MaterialTheme(colorScheme = colorScheme, typography = AppTypography, content = content)
}
```
For the expressive defaults on 1.5.0 swap in `MaterialExpressiveTheme(colorScheme = colorScheme, typography = AppTypography, content = content)`.

### 10.4 Settings row with ListItem and Switch (stable on 1.5.0)

```kotlin
@Composable
fun SettingSwitchRow(title: String, summary: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    ListItem(
        modifier = Modifier.toggleable(value = checked, role = Role.Switch, onValueChange = onCheckedChange),
        supportingContent = { Text(summary) },
        trailingContent = { Switch(checked = checked, onCheckedChange = null) }, // row owns the action
    ) { Text(title) }
}
```
material3 1.4.x: the trailing-`content` overload does not exist; write `ListItem(headlineContent = { Text(title) }, modifier = ..., supportingContent = ..., trailingContent = ...)`.

### 10.5 Form field with validation and supporting text (stable; `TextFieldState` overload since 1.4.0)

```kotlin
@Composable
fun EmailField(onSubmit: (String) -> Unit) {
    val email = rememberTextFieldState()
    var submitted by rememberSaveable { mutableStateOf(false) }
    val invalid = submitted && !Patterns.EMAIL_ADDRESS.matcher(email.text).matches()
    OutlinedTextField(
        state = email,
        modifier = Modifier.fillMaxWidth(),
        label = { Text(stringResource(R.string.email)) },
        supportingText = { if (invalid) Text(stringResource(R.string.email_error)) },
        isError = invalid,
        lineLimits = TextFieldLineLimits.SingleLine,
        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email, imeAction = ImeAction.Done),
        onKeyboardAction = { submitted = true; if (!invalid) onSubmit(email.text.toString()) },
    )
}
```
`rememberTextFieldState`, `TextFieldLineLimits` are in `androidx.compose.foundation.text.input`. Passwords: `OutlinedSecureTextField(state = ...)`.

### 10.6 Dialog vs bottom sheet vs snackbar

```kotlin
// Blocking decision: AlertDialog (stable)
AlertDialog(
    onDismissRequest = onDismiss,
    title = { Text(stringResource(R.string.delete_title)) },
    text = { Text(stringResource(R.string.delete_body)) },
    confirmButton = { TextButton(onClick = onConfirm) { Text(stringResource(R.string.delete)) } },
    dismissButton = { TextButton(onClick = onDismiss) { Text(stringResource(R.string.cancel)) } },
)

// Secondary content or a set of actions: ModalBottomSheet (experimental in 1.4, 1.5 and 1.6 alpha)
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ShareSheet(onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss) {
        ShareTargets(Modifier.padding(bottom = 16.dp))
    }
}

// Brief, non-blocking feedback with an optional action: snackbar (stable)
val snackbarHostState = remember { SnackbarHostState() }
val scope = rememberCoroutineScope()
Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { innerPadding ->
    Content(Modifier.padding(innerPadding), onArchived = {
        scope.launch {
            val result = snackbarHostState.showSnackbar(message = archivedText, actionLabel = undoText)
            if (result == SnackbarResult.ActionPerformed) undoArchive()
        }
    })
}
```

### 10.7 Accessible custom control (stable; foundation and ui 1.13)

```kotlin
@Composable
fun FavoriteToggle(favorite: Boolean, onFavoriteChange: (Boolean) -> Unit, modifier: Modifier = Modifier) {
    val label = stringResource(R.string.favorite)
    val state = stringResource(if (favorite) R.string.state_on_favorites else R.string.state_not_on_favorites)
    Box(
        modifier
            .toggleable(value = favorite, role = Role.Switch, onValueChange = onFavoriteChange)
            .minimumInteractiveComponentSize()          // reserves 48dp; keep before size()
            .semantics { contentDescription = label; stateDescription = state },
        contentAlignment = Alignment.Center,
    ) {
        Icon(
            painterResource(if (favorite) R.drawable.ic_star_filled else R.drawable.ic_star),
            contentDescription = null,                   // described by the parent
            tint = if (favorite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
```
Prefer `IconToggleButton(checked, onCheckedChange) { Icon(...) }` when the standard look is acceptable.

### 10.8 Edge-to-edge scaffold with insets (stable)

```kotlin
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent { AppTheme { FeedScreen() } }
    }
}

@Composable
fun FeedScreen(items: List<String> = emptyList()) {
    Scaffold(topBar = { TopAppBar(title = { Text(stringResource(R.string.feed)) }) }) { innerPadding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().consumeWindowInsets(innerPadding),
            contentPadding = innerPadding,               // content scrolls under the bars, starts clear of them
        ) { items(items) { ListItem { Text(it) } } }
    }
}
```
Manifest: `android:windowSoftInputMode="adjustResize"`. The guide's snippet calls `enableEdgeToEdge()` after `super.onCreate`; both orders appear in Google samples ([M] for the second).

### 10.9 Top app bar with scroll behaviour (stable on 1.5.0)

```kotlin
@Composable
fun ArticleScreen(onBack: () -> Unit) {
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
}
```
material3 1.4.x: add `@OptIn(ExperimentalMaterial3Api::class)` (the `*ScrollBehavior()` factories are experimental there).

### 10.10 Date picker dialog (stable in 1.4 and 1.5)

```kotlin
@Composable
fun BirthdayPickerDialog(initialMillis: Long?, onDismiss: () -> Unit, onDateSelected: (Long?) -> Unit) {
    val state = rememberDatePickerState(initialSelectedDateMillis = initialMillis)
    DatePickerDialog(
        onDismissRequest = onDismiss,
        confirmButton = {
            TextButton(onClick = { onDateSelected(state.selectedDateMillis); onDismiss() }) {
                Text(stringResource(R.string.ok))
            }
        },
        dismissButton = { TextButton(onClick = onDismiss) { Text(stringResource(R.string.cancel)) } },
    ) { DatePicker(state = state) }
}
```
`selectedDateMillis` is UTC milliseconds at the start of the day; convert with `Instant.ofEpochMilli(...).atZone(ZoneOffset.UTC).toLocalDate()` ([M] for the conversion detail).

## 11. Wear OS and TV (brief)

- [V] Wear: `androidx.wear.compose:compose-material3` 1.7.2 stable, package `androidx.wear.compose.material3`: `AppScaffold`,
  `ScreenScaffold`, `MaterialTheme`, `Button`, `FilledTonalButton`, `CompactButton`, `EdgeButton`, `IconButton`, `TitleCard`,
  `ListHeader`, `SwitchButton`, `AlertDialog`, `ConfirmationDialog`, `TimeText`, `ScrollIndicator`, `Stepper`, `Slider`,
  `Picker`, `HorizontalPagerScaffold`, `dynamicColorScheme(context): ColorScheme?`. (`TransformingLazyColumn` is not in
  this artifact's API file; [M] it lives in `androidx.wear.compose:compose-foundation`.)
  It is a separate library: do not use `androidx.compose.material3` on Wear. Guide lists Material "2.5" and "3" variants.
  https://developer.android.com/training/wearables/compose
- [V] TV: `androidx.tv:tv-material` 1.1.0 stable, package `androidx.tv.material3`: `MaterialTheme`, `Surface`, `Button`,
  `WideButton`, `IconButton`, `Card`, `ClassicCard`, `StandardCardContainer`, `ListItem`, `DenseListItem`, `NavigationDrawer`,
  `ModalNavigationDrawer`, `TabRow`, `Tab`, `Carousel`, `Checkbox`, `Switch`, `RadioButton`, `AssistChip`, `FilterChip`.
  33 `@ExperimentalTvMaterial3Api` uses remain in 1.1.0-beta01. https://developer.android.com/training/tv/playback/compose

## 12. Not verified / open items

- Exact published 1.5.0 surface: taken from the 1.5.0-beta01 snapshot; no release branch reachable. `SplitButton` (release
  notes) vs `SplitButtonLayout` (API files) is unresolved.
- MDC-Android current version number and Maven coordinates beyond the docs' minimums.
- Accompanist deprecation status, the Scaffold-padding lint id, `sp` non-linear scaling details, contrast-level APIs.
- Whether the BOM maps `material3-adaptive-navigation-suite` (the lookup on the BOM page did not return a row; release notes
  list it under `material3-*:1.5.0`).
- Android 17 behaviour changes were not read by this workstream; statements stop at API 36.
- Licence: developer.android.com pages state "Content and code samples on this page are subject to the licenses described
  in the Content License" [V]; the licence text itself was not opened here.
