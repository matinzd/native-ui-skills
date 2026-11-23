# API availability, library versions and deprecated APIs

Scope: how to find the Compose Material 3 version a project uses, what is stable, experimental or deprecated in material3 1.3 to 1.6 alpha, how to opt in, what replaces stale and Material 2 spellings, names that do not exist, how to check a signature yourself, and API-level gating for platform features.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Find the library versions first
- Current versions
- Stable, experimental, deprecated
- Status by material3 version: structure and navigation
- Status by material3 version: controls and presentation
- Deprecated or stale spelling and its replacement
- Material 2 names and their Material 3 replacements
- Names that do not exist
- Verify a signature yourself
- Platform gating by API level
- Common mistakes

## Find the library versions first

- [Conv] Read the versions before choosing any API. Look in `gradle/libs.versions.toml` (version catalog) and the module `build.gradle.kts` for `androidx.compose:compose-bom`, `androidx.compose.material3:material3`, `androidx.compose.material3.adaptive:adaptive*`, `androidx.activity:activity-compose`, plus `compileSdk`, `targetSdk` and `minSdk`.
- [API] With the Compose BOM (`implementation(platform("androidx.compose:compose-bom:<version>"))`) the Compose artifacts carry no version of their own; the BOM mapping page gives the library versions for each BOM. BOM 2026.11.01 maps to material3 1.5.0 and Compose UI and Foundation 1.13.0.
- [API] The `androidx.compose.material3.adaptive:*` artifacts (pane scaffolds, `currentWindowAdaptiveInfoV2`) version separately (1.3.0) from `material3` and `material3-adaptive-navigation-suite` (1.5.0).
- [Conv] An explicit version on an artifact overrides the BOM, and a transitive dependency can raise it. When it matters, resolve it: `./gradlew :app:dependencies --configuration releaseRuntimeClasspath` and search for `material3`.
- [Conv] Existing code is evidence: `rememberBottomSheetState` or `ListItem { }` with a trailing lambda means 1.5+; `@OptIn(ExperimentalMaterial3Api::class)` on a plain `TopAppBar` means 1.3 or older.
- [Conv] If the version is unknown and cannot be asked for, write for material3 1.5.x, say so in one line, and name what changes on 1.4 (the tables below).
- [Conv] State the result with every snippet: "material3 1.5.x; opt-in: ExperimentalMaterial3Api for ModalBottomSheet".

Source: https://developer.android.com/develop/ui/compose/bom , https://developer.android.com/develop/ui/compose/bom/bom-mapping , https://developer.android.com/build/migrate-to-catalogs

## Current versions

| Library | Stable on 2026-11-23 | Pre-release |
|---|---|---|
| Compose BOM | 2026.11.01 | - |
| `androidx.compose.material3:material3`, `material3-adaptive-navigation-suite` | 1.5.0 (2026-11-18) | 1.6.0-alpha01 |
| `androidx.compose.material3.adaptive:adaptive`, `adaptive-layout`, `adaptive-navigation` | 1.3.0 | 1.4.0-alpha03 |
| Compose UI, Foundation | 1.13.0 | 1.14.0-alpha01 |
| `androidx.activity:activity-compose` | 1.13.0 | 1.14.0-alpha03 |
| `androidx.navigation:navigation-compose` (Navigation 2) | 2.10.2 | 2.11.0-alpha01 |
| `androidx.navigation3:navigation3-runtime`, `navigation3-ui` | 1.2.2 | 1.3.0-alpha05 |
| `androidx.window:window-core` | 1.5.1 | 1.6.0-alpha05 |

- [API] material3 1.5.0 is the first stable release that contains the Material 3 Expressive components and `MaterialExpressiveTheme`; material3 1.4.x has none of them.

Source: https://developer.android.com/jetpack/androidx/releases/compose-material3 , https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive , https://developer.android.com/develop/ui/compose/bom/bom-mapping

## Stable, experimental, deprecated

- [API] Experimental API is marked with a `@RequiresOptIn` annotation; calling it without opting in is a compile error. The markers: `ExperimentalMaterial3Api`, `ExperimentalMaterial3ExpressiveApi` (both in `androidx.compose.material3`), `ExperimentalMaterial3AdaptiveApi` (`androidx.compose.material3.adaptive`), `ExperimentalLayoutApi`, `ExperimentalFoundationApi`.
- [Conv] Opt in at the smallest scope, on the one function that needs it: `@OptIn(ExperimentalMaterial3Api::class)`. Do not put `@file:OptIn` or a module-wide `-opt-in` compiler flag on code that no longer needs it; on 1.5 most former opt-ins are obsolete.
- [API] Experimental API may change or be removed in any release, including patch releases of a "stable" artifact. Say so when you use one.
- [Conv] Prefer a stable alternative when it gives the same result (for example `AlertDialog` instead of a custom experimental surface). When the guideline-correct component is experimental (`ModalBottomSheet`, tooltips, pane scaffolds), use it and state the opt-in.
- [API] Deprecated API still compiles with a warning. Do not write it in new code; use it only as a marked fallback for an older library version.
- [Conv] A stable artifact version does not imply every API in it is stable: adaptive 1.3.0 is stable, yet all its pane scaffolds are experimental.

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Status by material3 version: structure and navigation

`exp` = needs `@OptIn(ExperimentalMaterial3Api::class)`; `-` = does not exist in that version.

| API | 1.3 | 1.4 | 1.5 | 1.6 alpha |
|---|---|---|---|---|
| `Scaffold`, `NavigationBar`, `NavigationRail`, drawers, `Surface` | stable | stable | stable | stable |
| `TopAppBar`, `CenterAlignedTopAppBar`, `MediumTopAppBar`, `LargeTopAppBar` | exp | stable | stable | stable |
| `TopAppBarDefaults.pinnedScrollBehavior()` and the other scroll behaviors | exp | exp | stable | stable |
| `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar`, `TopAppBar(title, subtitle)` | - | - | stable | stable |
| `BottomAppBar` with `scrollBehavior` | exp | exp | stable | stable |
| `ShortNavigationBar`, `WideNavigationRail`, `ModalWideNavigationRail` | - | stable | stable | stable |
| `HorizontalFloatingToolbar`, `FlexibleBottomAppBar` | - | - | stable | stable |
| `PrimaryTabRow`, `SecondaryTabRow`, scrollable variants | exp | stable | stable | stable |
| `TabRow`, `ScrollableTabRow` | stable | deprecated | deprecated | deprecated |
| `SearchBar(state, inputField)`, `ExpandedFullScreenSearchBar`, `rememberSearchBarState` | - | exp | stable | stable |
| `SearchBar(inputField, expanded, ...)`, `DockedSearchBar(inputField, ...)` | exp | exp | deprecated | deprecated |
| `AppBarWithSearch` | - | - | exp | exp |
| `MaterialExpressiveTheme`, `MotionScheme`, `MaterialTheme.motionScheme` | - | - | stable | stable |
| `NavigationSuiteScaffold` (separate artifact, same version) | not checked | not checked | stable | stable |

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Status by material3 version: controls and presentation

| API | 1.3 | 1.4 | 1.5 | 1.6 alpha |
|---|---|---|---|---|
| `ListItem(headlineContent = ...)` | stable | stable | deprecated | deprecated |
| `ListItem(...) { content }`, clickable, selectable and toggleable overloads, `SegmentedListItem` | - | - | stable | stable |
| `Slider(value, onValueChange)`, `RangeSlider(value, ...)` | stable | stable | deprecated | deprecated |
| `Slider(state: SliderState, ...)` (`rememberSliderState` from 1.4) | exp | exp | stable | stable |
| `TextField(state: TextFieldState)`, `OutlinedTextField(state)`, `SecureTextField` | - | stable | stable | stable |
| `TextField(value, onValueChange)`, `OutlinedTextField(value, onValueChange)` | stable | stable | stable | deprecated |
| `ModalBottomSheet`, `BottomSheetScaffold`, `SheetState` | exp | exp | exp | exp |
| `rememberModalBottomSheetState`, `rememberStandardBottomSheetState` | exp | exp | deprecated | deprecated |
| `rememberBottomSheetState` | - | - | exp | exp |
| `BasicAlertDialog` | exp | exp | stable | stable |
| `DatePicker`, `DatePickerDialog`, `rememberDatePickerState`, `DateRangePicker` | exp | stable | stable | stable |
| `TimePicker`, `TimeInput`, `rememberTimePickerState` | exp | exp | stable | stable |
| `TimePickerDialog` | - | stable | stable | stable |
| `ExposedDropdownMenuBox`, `menuAnchor(type)` | exp | exp | stable | stable |
| `TooltipBox`, `PlainTooltip`, `RichTooltip`, `rememberTooltipState` | exp | exp | exp | exp |
| `PullToRefreshBox` | exp | stable | stable | stable |
| `HorizontalMultiBrowseCarousel`, `rememberCarouselState` | exp | exp | stable | stable |
| `ButtonGroup`, `ToggleButton`, `FloatingActionButtonMenu`, `SplitButtonLayout`, `MediumFloatingActionButton` | - | - | stable | stable |
| `LinearWavyProgressIndicator`, `CircularWavyProgressIndicator` | - | - | stable | stable |
| `LoadingIndicator`, `ContainedLoadingIndicator` | - | - | expressive exp | expressive exp |
| `SegmentedButton`, `SwipeToDismissBox`, `HorizontalDivider`, chips, `Card`, `Badge` | stable | stable | stable | stable |

- [API] "expressive exp" needs `@OptIn(ExperimentalMaterial3ExpressiveApi::class)`.
- [API] The 1.3, 1.4 and 1.5 columns were read from the `1.3.0-beta01`, `1.4.0-beta03` and `1.5.0-beta01` API snapshots, the closest files to each stable release that are published; a late change between beta and stable is possible.
- [Unverified] The 1.5.0 release notes mention a `SplitButton` composable replacing `SplitButtonLayout`; no `SplitButton(` function is in the 1.5.0-beta01 or current API file. Use `SplitButtonLayout` and check the project's version.

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Deprecated or stale spelling and its replacement

| Stale spelling | Status | Use instead |
|---|---|---|
| `Divider()` | deprecated | `HorizontalDivider()`, `VerticalDivider()` |
| `TabRow`, `ScrollableTabRow` | deprecated (1.4+) | `PrimaryTabRow`, `SecondaryTabRow`, `PrimaryScrollableTabRow`, `SecondaryScrollableTabRow` |
| `ListItem(headlineContent = { })` | deprecated (1.5+) | `ListItem(...) { headline }` |
| `Slider(value = v, onValueChange = { })` | deprecated (1.5+) | `Slider(state = rememberSliderState(...), onValueChange = { })` |
| `rememberModalBottomSheetState(skipPartiallyExpanded = true)` | deprecated (1.5+) | `rememberBottomSheetState(initialValue = ..., enabledValues = ...)`, or the sheet's default state |
| `DockedSearchBar`, `SearchBar(query, onQueryChange, ...)`, `SearchBar(inputField, expanded, ...)` | deprecated | `SearchBar(state, inputField)` with `ExpandedFullScreenSearchBar` or `ExpandedDockedSearchBar` |
| `LinearProgressIndicator(progress = 0.5f)` | deprecated | `progress = { 0.5f }` (lambda) |
| `AlertDialog(onDismissRequest) { content }` | deprecated | `BasicAlertDialog` |
| `Modifier.menuAnchor()` without arguments | deprecated in 1.4, gone in 1.5 | `Modifier.menuAnchor(ExposedDropdownMenuAnchorType.PrimaryNotEditable)` |
| `rememberSwipeToDismissBoxState(confirmValueChange = ...)` | deprecated | `SwipeToDismissBox(onDismiss = ...)` |
| `rememberPlainTooltipPositionProvider()`, `rememberRichTooltipPositionProvider()` | deprecated | `TooltipDefaults.rememberTooltipPositionProvider(TooltipAnchorPosition.Above)` |
| `LocalMinimumInteractiveComponentEnforcement` | deprecated | `LocalMinimumInteractiveComponentSize` |
| `TextFieldLabelPosition.Attached` | deprecated | `TextFieldLabelPosition.Inside` or `Cutout` |
| `rememberRipple()`, `RippleTheme`, `LocalRippleTheme` | deprecated, ignored by Material 3 components | `ripple()`, `LocalRippleConfiguration` |
| `currentWindowAdaptiveInfo()` | deprecated in adaptive 1.3.0 | `currentWindowAdaptiveInfoV2()` |
| `WindowWidthSizeClass`, `windowSizeClass.windowWidthSizeClass`, `WindowSizeClass.compute(...)` | deprecated (window-core) | `windowSizeClass.isWidthAtLeastBreakpoint(WindowSizeClass.WIDTH_DP_MEDIUM_LOWER_BOUND)` |
| `calculateWindowSizeClass(activity)` (`material3-window-size-class`) | still experimental | `currentWindowAdaptiveInfoV2().windowSizeClass` |
| `Icons.Filled.*`, `Icons.Default.*` (`material-icons-core`, `-extended`) | library frozen, no longer recommended, not a material3 dependency since 1.4 | Material Symbols vector drawables with `painterResource` |
| `BasicTextField(value, onValueChange)` | deprecated in Foundation 1.13 | `BasicTextField(state: TextFieldState)` |
| `semantics { invisibleToUser() }`, `isContainer = true` | deprecated | `hideFromAccessibility()`, `isTraversalGroup = true` |
| Accompanist `rememberSystemUiController()`, `window.statusBarColor = ...` | [Unverified] Accompanist status not re-checked; status bar color has no effect on Android 15+ | `enableEdgeToEdge()` and window insets |
| `ComponentActivity.enableEdgeToEdge()` (`androidx.activity`) | fine through activity 1.13; deprecated in 1.14.0-alpha03 | `WindowCompat.enableEdgeToEdge(window)` (`androidx.core`) once the project is on activity 1.14 |
| `onBackPressed()` override, intercepting `KEYCODE_BACK` | not supported with predictive back | `BackHandler`, `PredictiveBackHandler`, `OnBackPressedCallback` |

- [Conv] When 1.4 must be supported, the deprecated-in-1.5 form is the correct fallback there; mark it: `// Fallback for material3 1.4: ListItem(headlineContent = ...)`.

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://developer.android.com/develop/ui/compose/touch-input/user-interactions/migrate-indication-ripple , https://developer.android.com/develop/ui/compose/graphics/images/material , https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes

## Material 2 names and their Material 3 replacements

Material 2 (`androidx.compose.material.*`) is still published but has its own theme. These names are absent from every material3 API file.

| Material 2 | Material 3 |
|---|---|
| `BottomNavigation`, `BottomNavigationItem` | `NavigationBar`, `NavigationBarItem` |
| `MaterialTheme.colors`, `Colors`, `lightColors()` | `MaterialTheme.colorScheme`, `ColorScheme`, `lightColorScheme()` |
| `ContentAlpha`, `LocalContentAlpha` | color roles such as `onSurfaceVariant` |
| `Scaffold(scaffoldState = ..., drawerContent = ..., backgroundColor = ...)` | `SnackbarHostState` with `snackbarHost = { }`, `ModalNavigationDrawer`, `containerColor` |
| `ModalBottomSheetLayout`, `ModalBottomSheetValue` | `ModalBottomSheet` |
| `SwipeToDismiss`, `rememberDismissState`, `DismissValue` | `SwipeToDismissBox`, `rememberSwipeToDismissBoxState`, `SwipeToDismissBoxValue` |
| `Modifier.pullRefresh`, `rememberPullRefreshState`, `PullRefreshIndicator` | `PullToRefreshBox` |
| `LocalMinimumTouchTargetEnforcement` | `LocalMinimumInteractiveComponentSize` |
| `TopAppBar(title, backgroundColor, elevation)` | `TopAppBar(title, colors = TopAppBarDefaults.topAppBarColors(...))` |

- [MD] Do not use Material 2 and Material 3 in one app long-term; migrate imports to `androidx.compose.material3`.

Source: https://developer.android.com/develop/ui/compose/designsystems/material2-material3

## Names that do not exist

- `SmallTopAppBar` does not exist in material3 1.3 or later (it was deprecated in the 1.0 betas); use `TopAppBar`.
- `PlainTooltipBox` and `RichTooltipBox` do not exist; use `TooltipBox` with `PlainTooltip` or `RichTooltip`.
- `PullToRefreshContainer` does not exist since 1.3; use `PullToRefreshBox`.
- `expressiveDarkColorScheme()` does not exist; only `expressiveLightColorScheme()` is in the API file.
- `LocalMotionScheme` does not exist in 1.5; read `MaterialTheme.motionScheme`.
- `MenuAnchorType` does not exist in 1.4 or later (it was the 1.3 name); the type is `ExposedDropdownMenuAnchorType`.
- `BottomNavigation` does not exist in Material 3 (it is the Material 2 name of `NavigationBar`).
- `MaterialTheme.colors` does not exist in Material 3; the property is `MaterialTheme.colorScheme`.
- `ButtonGroup { Button(...) }` with plain composable content does not exist in 1.5.0; the content is a `ButtonGroupScope` with `clickableItem`, `toggleableItem` and `customItem`, and `overflowIndicator` is required.
- A `contrast` parameter on `lightColorScheme()` or `dynamicLightColorScheme()` does not exist.
- A `Modifier.minimumTouchTargetSize()` modifier does not exist; the modifier is `Modifier.minimumInteractiveComponentSize()`.

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary

## Verify a signature yourself

- [API] The public API of every androidx library is a text file in the `androidx/androidx` repository. Pattern: `https://raw.githubusercontent.com/androidx/androidx/androidx-main/<module path>/api/<file>` where `<file>` is `current.txt` (the next, unreleased version) or a frozen snapshot such as `1.5.0-beta01.txt`.
- [API] Module paths: `compose/material3/material3`, `compose/material3/material3-adaptive-navigation-suite`, `compose/material3/adaptive/adaptive` (also `adaptive-layout`, `adaptive-navigation`), `compose/foundation/foundation`, `compose/foundation/foundation-layout`, `compose/ui/ui`, `activity/activity-compose`, `navigation3/navigation3-ui`, `window/window-core`.
- [Conv] Search the file for the function name and read the whole line: parameters marked `optional` have defaults; `@ExperimentalMaterial3Api`, `@ExperimentalMaterial3ExpressiveApi` and `@Deprecated` are printed on the function or on its enclosing class. Ignore lines marked `@BytecodeOnly`.
- [Conv] `current.txt` describes the alpha in development, not the stable release: an API that appears only there is not available to a project on the stable BOM.
- [Conv] The release notes list additions, graduations ("Graduate ... to non-experimental") and deprecations per version; use them to find the version that introduced an API. When notes and API file disagree, trust the API file of the version in use.
- [Conv] The reference page on developer.android.com documents the latest stable release; it marks experimental and deprecated members too.

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Platform gating by API level

| Feature | Gate | Fallback |
|---|---|---|
| Dynamic color (`dynamicLightColorScheme`, `dynamicDarkColorScheme`) | `@RequiresApi(31)`: `Build.VERSION.SDK_INT >= Build.VERSION_CODES.S` | static `lightColorScheme()` / `darkColorScheme()` |
| `rememberDatePickerState(initialSelectedDate: LocalDate?, ...)` | `@RequiresApi(26)` | the `initialSelectedDateMillis` overload |
| Edge-to-edge | enforced on Android 15+ devices once `targetSdk` is 35; the opt-out attribute is disabled for `targetSdk` 36 on Android 16 | call `enableEdgeToEdge()` in `onCreate` so older versions match |
| Predictive back system animations | in-app animations from Android 14; on by default for `targetSdk` 36 on Android 16+ | none needed: use `BackHandler` or `OnBackPressedCallback` on every version |
| Compose accessibility checks in tests (`enableAccessibilityChecks`) | `@RequiresApi(34)` test device | TalkBack and Accessibility Scanner |

```kotlin
// material3 1.2+; no opt-in. Not compiled.
val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
        if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
    darkTheme -> DarkColors
    else -> LightColors
}
```

- [API] Library version and API level are independent gates: a material3 1.5 composable runs on every `minSdk` the library supports, while a platform feature needs the `Build.VERSION.SDK_INT` check whatever the library version.
- [API] `targetSdk` changes behavior on new devices only (edge-to-edge enforcement, predictive back default); `minSdk` decides which checks need a fallback branch.
- [Conv] Always write the fallback branch as working UI. An API-level check without an `else` is a regression on older devices.
- [API] `android:enableOnBackInvokedCallback="false"` on the application or an activity opts out of the predictive back system animations when Back is still intercepted the old way.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://developer.android.com/about/versions/15/behavior-changes-15 , https://developer.android.com/about/versions/16/behavior-changes-16 , https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture

## Common mistakes

- Assuming the newest API without reading the BOM or catalog -> read the versions, state them with the snippet.
- `@file:OptIn(ExperimentalMaterial3Api::class)` copied into every file on 1.5 -> remove; opt in on the single function that still needs it.
- Calling `ListItem(headlineContent = ...)` or `Slider(value = ...)` in new 1.5 code -> use the content-lambda and state-based overloads; keep the old form only as a marked 1.4 fallback.
- Taking an API from `current.txt` or an alpha blog post for a project on the stable BOM -> check the snapshot of the version in use.
- Treating adaptive 1.3.0 pane scaffolds as stable -> add `@OptIn(ExperimentalMaterial3AdaptiveApi::class)` and say so.
- `dynamicLightColorScheme(context)` without a `Build.VERSION_CODES.S` check -> gate it and fall back to a static scheme.
- Mixing `androidx.compose.material.*` imports into a Material 3 screen -> use the Material 3 replacement from the table.
- Adding `material-icons-extended` to get one icon -> add the Material Symbols vector drawable instead.
