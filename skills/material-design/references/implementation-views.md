# Views: Material Components for Android

Scope: Material 3 in View-based (XML) apps with the Material Components for Android library (MDC-Android): setup and theme parents, dynamic color, the key widgets and their attributes, edge-to-edge and Back in Views, a Compose-to-Views mapping, and when to host Compose in Views or Views in Compose.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Setup and requirements
- Theme parents
- Color, type and shape attributes
- Dynamic color
- Key widgets and attributes
- Text fields, dialogs, sheets and snackbars
- Edge-to-edge and Back in Views
- Compose to Views mapping
- Mixing Compose and Views
- Common mistakes

## Setup and requirements

- [API] Dependency: `com.google.android.material:material:<version>`. `Theme.Material3.*` themes and `Widget.Material3.*` styles need library 1.5.0 or later; `Theme.Material3Expressive.*` themes and `Widget.Material3Expressive.*` styles need 1.14.0 or later (first available in 1.14.0-alpha01).
- [API] The getting-started guide asks for `compileSdk` 36.1 or later and `minSdk` 23 or later for the latest library versions.
- [API] Activities extend `AppCompatActivity` (or use `AppCompatDelegate`) so that the Material versions of framework widgets are inflated.
- [API] Since 1.13.0-alpha12 the library is built with non-transitive R classes: refer to AppCompat attributes as `androidx.appcompat.R.attr.colorPrimary` and to Material ones as `com.google.android.material.R.attr.colorOnPrimary` in code.
- [API] Material's blog states that Material Views 1.14.0 is the final stable feature release of the Views library, which is now in maintenance mode (no new features, critical bug fixes only), because Material Android is Compose-first. Existing Views apps stay supported; do not promise new Views components.
- [Unverified] The current MDC-Android release number was not checked (the Maven index was unreachable); read the version from the project's build files.
- [Conv] Find the library version and the app theme parent (in `res/values/themes.xml` and its `values-night` variant) before recommending a widget style.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/getting-started.md , https://m3.material.io/develop/android/mdc-android , https://m3.material.io/blog/material-is-compose-first

## Theme parents

| Material 3 Expressive (1.14.0+) | Material 3 (1.5.0+) | Legacy Material 2 |
|---|---|---|
| `Theme.Material3Expressive.DayNight` (`.NoActionBar`) | `Theme.Material3.DayNight` (`.NoActionBar`) | `Theme.MaterialComponents.DayNight` (`.NoActionBar`) |
| `Theme.Material3Expressive.Light` (`.NoActionBar`) | `Theme.Material3.Light` (`.NoActionBar`) | `Theme.MaterialComponents.Light` (`.NoActionBar`) |
| `Theme.Material3Expressive.Dark` (`.NoActionBar`) | `Theme.Material3.Dark` (`.NoActionBar`) | `Theme.MaterialComponents` (`.NoActionBar`) |
| `Theme.Material3Expressive.DynamicColors.DayNight` / `.Light` / `.Dark` (`.NoActionBar`) | `Theme.Material3.DynamicColors.DayNight` / `.Light` / `.Dark` (`.NoActionBar`) | none |

- [MD] Migrate app-wide by changing the app theme parent to a `Material3` theme, then test: default styles of existing widgets change.
- [Conv] Use a `DayNight` parent so the theme follows the system dark setting; put dark-only overrides in `values-night`. Use a `.NoActionBar` parent when the layout has its own `MaterialToolbar`.
- [API] `Widget.Material3Expressive.*` component styles require a `Theme.Material3Expressive.*` theme. (Material 3 Expressive)
- [API] A `Theme.AppCompat` or `Theme.MaterialComponents` parent does not define the Material 3 attributes; Material 3 widget styles then fail to inflate or look wrong.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/getting-started.md , https://developer.android.com/develop/ui/views/theming/darktheme

## Color, type and shape attributes

- [API] Color roles are theme attributes with the same names as in Compose: `?attr/colorPrimary`, `colorOnPrimary`, `colorPrimaryContainer`, `colorOnPrimaryContainer`, `colorSecondary`, `colorTertiary`, `colorSurface`, `colorOnSurface`, `colorOnSurfaceVariant`, `colorSurfaceContainer` (`Low`, `High`, `Highest`), `colorOutline`, `colorError`.
- [MD] Reference roles in layouts and styles (`android:textColor="?attr/colorOnSurface"`), never literal colors or `@color/...` values that bypass the theme.
- [API] Type scale: `?attr/textAppearanceDisplayLarge` to `?attr/textAppearanceLabelSmall` (for example `textAppearanceTitleLarge`, `textAppearanceBodyLarge`, `textAppearanceBodyMedium`). Apply with `android:textAppearance`.
- [API] Shape: `?attr/shapeAppearanceCornerMedium` and the other `shapeAppearanceCorner*` attributes; components take `app:shapeAppearance` or `app:shapeAppearanceOverlay`.
- [Conv] Text sizes in `sp`, everything else in `dp`; prefer `wrap_content` with `android:minHeight` over fixed heights around text.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Color.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Typography.md , https://m3.material.io/styles/color/roles

## Dynamic color

- [API] Dynamic color needs Android 12 (API 31). `DynamicColors.applyToActivitiesIfAvailable(application)` in `Application.onCreate()` applies it to every activity and does nothing on older versions, so the static theme colors are the fallback.
- [API] Variants: `applyToActivitiesIfAvailable(application, R.style.ThemeOverlay_...)` with a custom overlay, a precondition callback, or a `DynamicColorsOptions`; `DynamicColors.applyToActivityIfAvailable(activity)` for one activity; `DynamicColors.wrapContextIfAvailable(context)` for a context.
- [API] Overlays: `ThemeOverlay.Material3.DynamicColors.Light`, `.Dark`, `.DayNight`; the `Theme.Material3.DynamicColors.*` parents bake them into the theme.
- [API] `MaterialColors.harmonizeWithPrimary(context, color)` shifts a custom color toward the dynamic primary; `HarmonizedColors` does it for color resources.
- [MD] Keep semantic colors (error, brand-critical status colors) readable under any wallpaper: harmonize them instead of leaving raw brand values next to dynamic ones.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Color.md , https://developer.android.com/develop/ui/views/theming/dynamic-colors

## Key widgets and attributes

| Component | View class and style | Useful attributes and API |
|---|---|---|
| Buttons | `MaterialButton` (a plain `Button` tag inflates as one under a Material theme); styles `Widget.Material3.Button` (filled), `.Button.TonalButton`, `.Button.ElevatedButton`, `.Button.OutlinedButton`, `.Button.TextButton`; theme attrs `?attr/materialButtonStyle`, `materialButtonTonalStyle`, `materialButtonElevatedStyle`, `materialButtonOutlinedStyle` | `app:icon`, `android:text`, `android:enabled` |
| Icon button | `MaterialButton` with `?attr/materialIconButtonStyle`, `materialIconButtonFilledStyle`, `materialIconButtonFilledTonalStyle`, `materialIconButtonOutlinedStyle` | `app:icon`, `android:contentDescription` (required) |
| Button group, split button | `MaterialButtonGroup`, `MaterialSplitButton` | Material 3 Expressive |
| FAB | `FloatingActionButton`, `ExtendedFloatingActionButton` | `app:srcCompat`, `android:contentDescription`; FAB menu has no View class (host the Compose one) |
| Top app bar | `AppBarLayout` + `MaterialToolbar` (+ `CollapsingToolbarLayout`) in a `CoordinatorLayout` | `app:title`, `app:subtitle`, `app:navigationIcon`, `app:navigationContentDescription`, `app:menu`, `app:titleCentered`, `app:layout_scrollFlags`, `app:liftOnScroll` |
| Navigation bar | `BottomNavigationView` (base class `NavigationBarView`) | `app:menu`, `app:labelVisibilityMode`, `setOnItemSelectedListener`, `getOrCreateBadge(itemId)` |
| Navigation rail | `NavigationRailView` | `app:menu`, `app:headerLayout`, `app:labelVisibilityMode` |
| Navigation drawer | `DrawerLayout` + `NavigationView` | `app:menu`, `app:headerLayout`, `android:layout_gravity="start"` |
| Tabs | `TabLayout`; styles `Widget.Material3.TabLayout`, `.TabLayout.Secondary` | `app:tabMode` |
| Search | `SearchBar` + `SearchView`; styles `Widget.Material3.SearchBar`, `Widget.Material3.SearchView` | `app:layout_anchor` on the `SearchView` pointing at the `SearchBar`, `app:navigationIcon`, `app:menu` |
| Checkbox, radio, switch | `MaterialCheckBox`, `MaterialRadioButton`, `MaterialSwitch` | `app:checkedState`, `app:errorShown` (checkbox); `?attr/minTouchTargetSize` |
| Chips | `Chip` in a `ChipGroup`; styles `Widget.Material3.Chip.Assist`, `.Filter`, `.Input`, `.Suggestion` | `app:singleSelection`, `app:selectionRequired`, `app:chipMinTouchTargetSize`, `app:ensureMinTouchTargetSize` |
| Slider | `Slider`, `RangeSlider` | `android:valueFrom`, `android:valueTo`, `android:stepSize`, `app:labelBehavior`, `addOnChangeListener` |
| Card | `MaterialCardView`; `?attr/materialCardViewElevatedStyle`, `materialCardViewFilledStyle`, `materialCardViewOutlinedStyle` | `android:clickable`, `android:focusable`, `app:strokeWidth` |
| List item | `ListItemLayout`, `ListItemCardView` in a `RecyclerView` | - |
| Divider | `MaterialDivider`, `MaterialDividerItemDecoration` | `app:dividerInsetStart` |
| Progress, loading | `LinearProgressIndicator`, `CircularProgressIndicator`, `LoadingIndicator` | `android:indeterminate`, `app:trackThickness`, `app:indicatorColor` |
| Toolbars | `FloatingToolbarLayout`, `DockedToolbarLayout` | Material 3 Expressive |
| Carousel | `RecyclerView` + `CarouselLayoutManager` + `MaskableFrameLayout` items | `CarouselSnapHelper`, strategies such as `MultiBrowseCarouselStrategy` |
| Badge | `BadgeDrawable` | `bottomNavigation.getOrCreateBadge(itemId)` |

- [API] `MaterialSwitch` is the Material 3 switch; `SwitchMaterial` is the deprecated one. `MaterialSwitch` is not auto-inflated from a `Switch` tag: write the full class name `com.google.android.material.materialswitch.MaterialSwitch` in XML.
- [API] `BottomNavigationView#setOnNavigationItemSelectedListener` and `setOnNavigationItemReselectedListener` are deprecated in favor of `setOnItemSelectedListener` and `setOnItemReselectedListener` from `NavigationBarView`.
- [MD] In MDC-Android the non-flexible medium and large top app bars are being deprecated and are no longer recommended; the small bar and the flexible variants remain. (Material 3 Expressive)
- [API] Chips and checkboxes extend their touch target to 48dp by default (`app:ensureMinTouchTargetSize`, `?attr/minTouchTargetSize`); do not switch that off to tighten a layout.
- [API] The Tooltip page of MDC-Android says the component is not yet implemented; use `TooltipCompat.setTooltipText(view, text)` from AppCompat. [Unverified] `TooltipCompat` was not re-checked in this pass.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/CommonButton.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/TopAppBar.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomNavigation.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/Switch.md , https://m3.material.io/components

## Text fields, dialogs, sheets and snackbars

- [API] Text field: `TextInputLayout` wrapping a `TextInputEditText`; styles `Widget.Material3.TextInputLayout.FilledBox` and `.OutlinedBox` (plus `.Dense` and `.ExposedDropdownMenu` variants). Set `android:hint` on the `TextInputLayout`, not on the edit text: it is the floating label.
- [API] Supporting and error text: `app:helperText`, `app:errorEnabled`, `textInputLayout.error = "..."` (pass `null` to clear), `app:counterEnabled` with `app:counterMaxLength`, `app:startIconDrawable`, `app:endIconMode` (`clear_text`, `password_toggle`, `custom`), `app:endIconContentDescription`, `app:errorAccessibilityLiveRegion`.
- [API] Exposed dropdown: `TextInputLayout` with an `.ExposedDropdownMenu` style around a `MaterialAutoCompleteTextView` (`app:simpleItems`).
- [API] Dialog: `MaterialAlertDialogBuilder(context).setTitle(...).setMessage(...).setPositiveButton(...) { dialog, which -> }.setNegativeButton(...).show()`. Do not use the framework or AppCompat `AlertDialog.Builder` directly: it does not get the Material 3 dialog theme.
- [API] Bottom sheet: `BottomSheetDialogFragment` (modal) or a view with `app:layout_behavior="com.google.android.material.bottomsheet.BottomSheetBehavior"` (standard); `app:behavior_peekHeight`, `app:behavior_hideable`; `BottomSheetDragHandleView` gives an accessible drag handle. Side sheets: `SideSheetDialog`, `SideSheetBehavior`.
- [API] Snackbar: `Snackbar.make(view, text, Snackbar.LENGTH_SHORT).setAction(label) { }.show()`; `setAnchorView(fab)` places it above a FAB or bottom bar. Durations `LENGTH_SHORT`, `LENGTH_LONG`, `LENGTH_INDEFINITE`.
- [API] Pickers: `MaterialDatePicker.Builder.datePicker().build()` and `.dateRangePicker()`; `MaterialTimePicker.Builder().setTimeFormat(...).setHour(...).setMinute(...).build()`; show with `show(supportFragmentManager, tag)`.

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/TextField.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/Dialog.md , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomSheet.md , https://m3.material.io/components/text-fields/guidelines , https://m3.material.io/components/dialogs/guidelines

## Edge-to-edge and Back in Views

- [API] Edge-to-edge is enforced on Android 15+ once the app targets SDK 35, and the opt-out is disabled for apps targeting API 36 on Android 16; View apps must handle insets too.
- [API] Enable it on older versions in `onCreate`: the Views guide calls `WindowCompat.enableEdgeToEdge(window)`; `ComponentActivity.enableEdgeToEdge()` from `androidx.activity` does the same through activity 1.13 (deprecated in 1.14.0-alpha03).
- [API] Apply insets with `ViewCompat.setOnApplyWindowInsetsListener(view) { v, windowInsets -> val insets = windowInsets.getInsets(WindowInsetsCompat.Type.systemBars()); ...; WindowInsetsCompat.CONSUMED }`: margins for floating controls such as a FAB, padding plus `android:clipToPadding="false"` for a `RecyclerView` so content scrolls behind the bars. Combine `Type.systemBars()` with `Type.displayCutout()` for lists; use `Type.systemGestures()` for gesture conflicts.
- [API] Material widgets help: set `android:fitsSystemWindows="true"` on `AppBarLayout` (or on the `MaterialToolbar` when there is no `AppBarLayout`) so the bar pads itself below the status bar; `BottomSheetBehavior` handles insets with `app:paddingBottomSystemWindowInsets` and its siblings; `NavigationView` and `NavigationRailView` fit system windows by default.
- [API] `android:statusBarColor` and `window.statusBarColor` have no effect on Android 15; let the app bar's background show through a transparent status bar.
- [API] Back: migrate to `OnBackPressedCallback` (AndroidX Activity 1.6.0+) through `onBackPressedDispatcher.addCallback(owner, callback)`, enabled only while there is something to intercept. Overriding `onBackPressed()` or intercepting `KEYCODE_BACK` is not supported with predictive back.
- [API] With library 1.10.0 or later and the app migrated to back callbacks, these components animate predictive back: `SearchView` set up with a `SearchBar`, modal bottom sheet, modal side sheet, `NavigationView` in a `DrawerLayout`.

Source: https://developer.android.com/develop/ui/views/layout/edge-to-edge , https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture , https://developer.android.com/about/versions/15/behavior-changes-15 , https://raw.githubusercontent.com/material-components/material-components-android/master/docs/foundations/PredictiveBack.md

## Compose to Views mapping

| Component | Compose (material3 1.5) | Views (MDC-Android) |
|---|---|---|
| Theme | `MaterialTheme`, `MaterialExpressiveTheme` | `Theme.Material3.*`, `Theme.Material3Expressive.*` |
| Color role | `MaterialTheme.colorScheme.primary` | `?attr/colorPrimary` |
| Type style | `MaterialTheme.typography.bodyLarge` | `?attr/textAppearanceBodyLarge` |
| Dynamic color | `dynamicLightColorScheme(context)` behind an API 31 check | `DynamicColors.applyToActivitiesIfAvailable(application)` |
| Screen structure | `Scaffold` | `CoordinatorLayout` + `AppBarLayout` |
| Top app bar | `TopAppBar`, `MediumFlexibleTopAppBar`, `LargeFlexibleTopAppBar` | `MaterialToolbar`, `CollapsingToolbarLayout` |
| Navigation bar / rail / drawer | `NavigationBar` / `NavigationRail`, `WideNavigationRail` / `ModalNavigationDrawer` | `BottomNavigationView` / `NavigationRailView` / `DrawerLayout` + `NavigationView` |
| Tabs | `PrimaryTabRow` + `Tab` | `TabLayout` |
| Search | `SearchBar` + `ExpandedFullScreenSearchBar` | `SearchBar` + `SearchView` |
| Buttons | `Button`, `FilledTonalButton`, `OutlinedButton`, `TextButton`, `IconButton` | `MaterialButton` with a style |
| FAB | `FloatingActionButton`, `ExtendedFloatingActionButton` | same class names in `com.google.android.material.floatingactionbutton` |
| Text field | `OutlinedTextField`, `TextField` | `TextInputLayout` + `TextInputEditText` |
| Dialog | `AlertDialog` | `MaterialAlertDialogBuilder` |
| Bottom sheet | `ModalBottomSheet`, `BottomSheetScaffold` | `BottomSheetDialogFragment`, `BottomSheetBehavior` |
| Snackbar | `SnackbarHost` + `SnackbarHostState` | `Snackbar.make(...)` |
| Checkbox / radio / switch | `Checkbox` / `RadioButton` / `Switch` | `MaterialCheckBox` / `MaterialRadioButton` / `MaterialSwitch` |
| Chips | `AssistChip`, `FilterChip`, `InputChip`, `SuggestionChip` | `Chip` + `ChipGroup` |
| Slider | `Slider`, `RangeSlider` | `Slider`, `RangeSlider` |
| Card / list item / divider | `Card` / `ListItem` / `HorizontalDivider` | `MaterialCardView` / `ListItemLayout` / `MaterialDivider` |
| Progress / loading | `LinearProgressIndicator`, `CircularProgressIndicator`, `LoadingIndicator` | same class names in `com.google.android.material` |
| Date / time picker | `DatePickerDialog` + `DatePicker`, `TimePickerDialog` + `TimePicker` | `MaterialDatePicker`, `MaterialTimePicker` |
| Side sheet | none | `SideSheetDialog`, `SideSheetBehavior` |
| FAB menu | `FloatingActionButtonMenu` | none (Compose interop) |
| Insets | `Scaffold` padding, `WindowInsets.safeDrawing`, `imePadding()` | `ViewCompat.setOnApplyWindowInsetsListener`, `fitsSystemWindows` |
| Back | `BackHandler` | `OnBackPressedCallback` |
| Accessibility label | `contentDescription` in `semantics` or on `Icon` | `android:contentDescription` |

Source: https://raw.githubusercontent.com/material-components/material-components-android/master/docs/getting-started.md , https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://m3.material.io/develop/android/mdc-android

## Mixing Compose and Views

- [API] Compose inside Views: put a `ComposeView` in the layout (or create one in code) and call `setContent { AppTheme { ... } }`. In a Fragment set `setViewCompositionStrategy(ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed)` so the composition follows the view lifecycle.
- [API] Views inside Compose: `AndroidView(factory = { context -> MyView(context) }, modifier = ..., update = { view -> ... })` from `androidx.compose.ui.viewinterop`; an overload adds `onReset` and `onRelease` for reuse in lazy lists.
- [Conv] Match the code base: in a View screen write View code with MDC-Android; in a Compose screen write Compose. Do not introduce the other toolkit for a single widget unless the component exists only there.
- [Conv] Reasons to host Compose in a View screen: a component MDC-Android does not ship (the FAB menu documentation itself points to the Compose component), or incremental migration screen by screen or component by component.
- [Conv] Reasons to host a View in Compose: views without a Compose equivalent (maps, web content, ads, camera previews, custom legacy views).
- [Conv] Keep one source of truth for the theme: the XML theme and the Compose `MaterialTheme` must define the same roles, or mixed screens show two palettes. With dynamic color both sides read the same system palette.
- [Conv] Interop boundaries are where insets, focus order and TalkBack traversal break; test them with a keyboard and a screen reader.

Source: https://developer.android.com/develop/ui/compose/migrate/interoperability-apis/compose-in-views , https://developer.android.com/develop/ui/compose/migrate/interoperability-apis/views-in-compose , https://developer.android.com/develop/ui/compose/migrate/strategy

## Common mistakes

- `Theme.AppCompat` or `Theme.MaterialComponents` parent with `Widget.Material3` styles -> `Theme.Material3.DayNight.NoActionBar` (or a `Material3Expressive` parent on 1.14+).
- `Widget.Material3Expressive.*` styles on library versions below 1.14.0 or under a non-Expressive theme -> upgrade and change the parent, or use `Widget.Material3.*`.
- `SwitchMaterial`, or a `Switch` tag expected to become a Material 3 switch -> `com.google.android.material.materialswitch.MaterialSwitch`.
- `setOnNavigationItemSelectedListener` -> `setOnItemSelectedListener`.
- `android:hint` on the `TextInputEditText`, or error shown by tinting the field red -> hint on the `TextInputLayout`, `error` text on the layout.
- `AlertDialog.Builder` -> `MaterialAlertDialogBuilder`.
- Hard-coded `#RRGGBB` or `@color/purple_500` in layouts -> `?attr/color...` roles.
- `android:statusBarColor` and no inset handling when targeting SDK 35+ -> edge-to-edge with `fitsSystemWindows` on the app bar and inset listeners on content.
- `onBackPressed()` override -> `OnBackPressedCallback`.
- A `ComposeView` in a Fragment without a view composition strategy -> `DisposeOnViewTreeLifecycleDestroyed`.
