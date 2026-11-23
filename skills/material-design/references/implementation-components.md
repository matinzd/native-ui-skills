# Components in Compose: API, status and correct calls

Scope: the Compose Material 3 call for each Material component: buttons and FABs, selection controls, chips, sliders, text fields, dialogs, sheets, snackbars, menus, tooltips, pickers, cards, lists, dividers, progress, badges, carousel, pull to refresh and swipe to dismiss, with stability per library version and a component-to-API table.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Material component to Compose API
- Buttons, icon buttons and FABs
- Button groups, toggle buttons, split buttons, FAB menu
- Selection controls and chips
- Sliders
- Text fields
- Dialogs
- Bottom sheets
- Snackbars
- Menus and tooltips
- Date and time pickers
- Cards, list items and dividers
- Progress, loading and badges
- Carousel, pull to refresh, swipe to dismiss
- Common mistakes

## Material component to Compose API

Status is for material3 1.5.0; "1.5+" means absent in 1.4. `exp` = `@OptIn(ExperimentalMaterial3Api::class)`. Per-version detail: `references/implementation-availability.md`.

| Material component | Compose API | Status |
|---|---|---|
| Button (filled, tonal, elevated, outlined, text) | `Button`, `FilledTonalButton`, `ElevatedButton`, `OutlinedButton`, `TextButton` | stable |
| Icon button | `IconButton`, `FilledIconButton`, `FilledTonalIconButton`, `OutlinedIconButton`; toggles `IconToggleButton`, `FilledIconToggleButton`, ... | stable |
| FAB, extended FAB | `FloatingActionButton`, `SmallFloatingActionButton`, `MediumFloatingActionButton` (1.5+), `LargeFloatingActionButton`, `ExtendedFloatingActionButton` | stable |
| FAB menu | `FloatingActionButtonMenu` + `FloatingActionButtonMenuItem` + `ToggleFloatingActionButton` | stable, 1.5+ |
| Button group | `ButtonGroup` | stable, 1.5+ |
| Toggle button | `ToggleButton`, `ElevatedToggleButton`, `FilledTonalToggleButton`, `OutlinedToggleButton` | stable, 1.5+ |
| Split button | `SplitButtonLayout` + `SplitButtonDefaults.LeadingButton` / `TrailingButton` | stable, 1.5+ |
| Segmented button | `SingleChoiceSegmentedButtonRow` / `MultiChoiceSegmentedButtonRow` + `SegmentedButton` | stable |
| Checkbox, radio button, switch | `Checkbox`, `TriStateCheckbox`, `RadioButton`, `Switch` | stable |
| Chips | `AssistChip`, `FilterChip`, `InputChip`, `SuggestionChip` (+ `Elevated...`) | stable |
| Slider | `Slider(state, ...)`, `RangeSlider(state, ...)` | stable, 1.5 (experimental in 1.4) |
| Text field | `TextField`, `OutlinedTextField`, `SecureTextField`, `OutlinedSecureTextField` | stable |
| Dialog | `AlertDialog`, `BasicAlertDialog` (stable 1.5, exp 1.4) | stable |
| Bottom sheet | `ModalBottomSheet`, `BottomSheetScaffold` | exp |
| Snackbar | `SnackbarHost` + `SnackbarHostState.showSnackbar` | stable |
| Menu | `DropdownMenu` + `DropdownMenuItem`; `ExposedDropdownMenuBox` (stable 1.5, exp 1.4) | stable |
| Tooltip | `TooltipBox` + `PlainTooltip` / `RichTooltip` | exp |
| Date picker | `DatePickerDialog` + `DatePicker`, `DateRangePicker` | stable (1.4+) |
| Time picker | `TimePickerDialog` + `TimePicker` / `TimeInput` | dialog stable 1.4+; pickers stable 1.5, exp 1.4 |
| Card | `Card`, `ElevatedCard`, `OutlinedCard` | stable |
| List item | `ListItem`, `SegmentedListItem` (1.5+) | stable |
| Divider | `HorizontalDivider`, `VerticalDivider` | stable |
| Progress indicator | `LinearProgressIndicator`, `CircularProgressIndicator`; wavy variants 1.5+ | stable |
| Loading indicator | `LoadingIndicator`, `ContainedLoadingIndicator` | `ExperimentalMaterial3ExpressiveApi`, 1.5+ |
| Badge | `BadgedBox` + `Badge` | stable |
| Carousel | `HorizontalMultiBrowseCarousel`, `HorizontalUncontainedCarousel`, `HorizontalCenteredHeroCarousel` | stable 1.5, exp 1.4 |
| Pull to refresh | `PullToRefreshBox` | stable (1.4+) |
| Swipe to dismiss | `SwipeToDismissBox` | stable |
| Side sheet | none in material3 1.5 | - |

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://m3.material.io/components

## Buttons, icon buttons and FABs

- [API] All five buttons share `(onClick, modifier, enabled, shape, colors, elevation, border, contentPadding, interactionSource, content: RowScope.() -> Unit)`. 1.5 adds overloads taking `shapes: ButtonShapes` for press shape morphing. (Material 3 Expressive)
- [MD] Emphasis order: FAB, filled, tonal, elevated, outlined, text. Use one filled button per screen for the main action and lower-emphasis buttons for the rest.
- [API] `IconButton(onClick, modifier, enabled, colors, interactionSource, shape) { Icon(...) }` reserves the 48dp minimum interactive size and sets the button role. The `Icon` inside must have a `contentDescription`.
- [API] `FloatingActionButton(onClick, modifier, shape, containerColor, contentColor, elevation, interactionSource) { }`; `ExtendedFloatingActionButton(text, icon, onClick, modifier, expanded, ...)`. Place it with `Scaffold(floatingActionButton = { })`.
- [MD] At most one FAB per screen, for the primary constructive action. Small and surface-colored FABs are no longer recommended in the Expressive update. (Material 3 Expressive)
- [Conv] Disable with `enabled = false`; do not swap in a grey look-alike. Do not set a fixed `height` on buttons: the label must be able to grow with font scale.

Source: https://m3.material.io/components/buttons/overview , https://m3.material.io/components/floating-action-button/overview , https://developer.android.com/develop/ui/compose/components/button

## Button groups, toggle buttons, split buttons, FAB menu

All material3 1.5+, stable there, absent in 1.4. (Material 3 Expressive)

- [API] `ButtonGroup(overflowIndicator: (ButtonGroupMenuState) -> Unit, modifier, expandedRatio, horizontalArrangement, verticalAlignment, content: ButtonGroupScope.() -> Unit)`. The scope offers `clickableItem(onClick, label, icon, weight, enabled)`, `toggleableItem(checked, label, onCheckedChange, icon, weight, enabled)` and `customItem(buttonGroupContent, menuContent)`. Items that do not fit move into the overflow menu, which is why every item needs a text `label`.
- [API] `ToggleButton(checked, onCheckedChange, modifier, buttonSize, enabled, icon, shapes, colors, ...) { }`.
- [API] `SplitButtonLayout(leadingButton, trailingButton, modifier, spacing)` with `SplitButtonDefaults.LeadingButton(onClick) { }` and `SplitButtonDefaults.TrailingButton(checked, onCheckedChange) { }`; the trailing button opens a menu. There is no `SplitButton(...)` function in the 1.5.0-beta01 or 1.6 alpha API file although the 1.5.0 release notes name one; see the note in `references/implementation-availability.md`.
- [API] `FloatingActionButtonMenu(expanded, button = { ToggleFloatingActionButton(checked, onCheckedChange) { } }, modifier, horizontalAlignment) { FloatingActionButtonMenuItem(onClick, text, icon) }`.
- [MD] Segmented buttons are no longer recommended in the Expressive update; a connected button group of toggle buttons takes their role. `SegmentedButton` remains the only option on material3 1.4.
- [Conv] On 1.4, the fallback for a button group is a `Row` of standard buttons, and for a FAB menu a FAB that opens a `DropdownMenu` or a bottom sheet.

```kotlin
// material3 1.5+; no opt-in. Not compiled.
ButtonGroup(overflowIndicator = { menuState -> ButtonGroupDefaults.OverflowIndicator(menuState) }) {
    clickableItem(onClick = onReply, label = replyLabel)
    toggleableItem(checked = starred, label = starLabel, onCheckedChange = onStarredChange)
}
```

Source: https://m3.material.io/components/button-groups/overview , https://m3.material.io/components/fab-menu/overview , https://m3.material.io/components/split-button/overview , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Selection controls and chips

- [API] `Checkbox(checked, onCheckedChange: ((Boolean) -> Unit)?, ...)`, `RadioButton(selected, onClick: (() -> Unit)?, ...)`, `Switch(checked, onCheckedChange: ((Boolean) -> Unit)?, modifier, thumbContent, enabled, ...)`, `TriStateCheckbox(state: ToggleableState, onClick, ...)`.
- [MD] Checkbox: independent choices in a list. Radio buttons: exactly one of a small visible set. Switch: a setting that takes effect immediately.
- [API] A control with a non-null callback reserves the 48dp minimum interactive size; with `null` it reserves nothing and is display-only.
- [Conv] A labelled control is one target: put `Modifier.toggleable(value, role = Role.Checkbox or Role.Switch, onValueChange)` or `Modifier.selectable(selected, role = Role.RadioButton, onClick)` on the row and pass `null` to the control. Put `Modifier.selectableGroup()` on the column of radio rows. See `references/accessibility-implementation.md`.
- [API] Chips: `AssistChip(onClick, label, leadingIcon, trailingIcon, ...)`, `FilterChip(selected, onClick, label, ...)`, `InputChip(selected, onClick, label, avatar, trailingIcon, ...)`, `SuggestionChip(onClick, label, icon, ...)`.
- [MD] Assist chips start an action, filter chips toggle a filter, input chips represent an entered item (removable), suggestion chips offer generated responses. Chips are not navigation.
- [Conv] Show the selected state of a filter chip with a leading check icon as well as color; lay chips out with `FlowRow` (stable in Foundation 1.13) or a horizontal list so they wrap or scroll at large text sizes.

Source: https://developer.android.com/develop/ui/compose/accessibility/api-defaults , https://m3.material.io/components/chips/overview , https://m3.material.io/components/switch/guidelines

## Sliders

| Call | 1.4 | 1.5 | 1.6 alpha |
|---|---|---|---|
| `Slider(value, onValueChange, modifier, enabled, valueRange, steps, onValueChangeFinished, ...)` | stable | deprecated | deprecated |
| `Slider(state: SliderState, onValueChange, modifier, enabled, onValueChangeFinished, colors, interactionSource, thumb, track)` with `rememberSliderState(value, steps, trackRange)` | experimental, and a different shape (callbacks lived in the state) | stable | stable |
| `RangeSlider(state: RangeSliderState, onValueChange, ...)` with `rememberRangeSliderState(startValue, endValue, steps, trackRange)` | experimental | stable | stable |

- [API] In 1.5 the state holds the value; `onValueChange` is required and reports changes for side effects. `SliderState.value` can be read or set.
- [MD] Sliders are for picking from a range where the precise value matters less than the relative position; show the current value in text nearby when the number matters.
- [Conv] Use `steps` for discrete values; give the slider an accessible label through a visible label that is merged with it or `Modifier.semantics { contentDescription = ... }`.

```kotlin
// material3 1.5+; no opt-in. Not compiled.
val sliderState = rememberSliderState(value = volume, steps = 9, trackRange = 0f..100f)
Slider(state = sliderState, onValueChange = onVolumeChange)
// Fallback for material3 1.4 (deprecated in 1.5):
// Slider(value = volume, onValueChange = onVolumeChange, valueRange = 0f..100f, steps = 9)
```

Source: https://m3.material.io/components/sliders/overview , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Text fields

| Form | 1.3 | 1.4 | 1.5 | 1.6 alpha |
|---|---|---|---|---|
| `TextField(value, onValueChange, ..., visualTransformation, keyboardOptions, keyboardActions, singleLine, maxLines, minLines, ...)` (also `OutlinedTextField`) | stable | stable | stable | deprecated |
| `TextField(state: TextFieldState, ..., labelPosition, inputTransformation, outputTransformation, keyboardOptions, onKeyboardAction, lineLimits, ...)` (also `OutlinedTextField`) | - | stable | stable | stable |
| `SecureTextField(state, ...)`, `OutlinedSecureTextField(state, ...)` | - | stable | stable | stable |

- [Conv] New code on 1.4+ uses the state form: `val state = rememberTextFieldState()` (`androidx.compose.foundation.text.input`), read `state.text`. Keep the value form in existing code on 1.5; do not mix forms within one screen.
- [API] Both forms take `label`, `placeholder`, `leadingIcon`, `trailingIcon`, `prefix`, `suffix`, `supportingText`, `isError`, `keyboardOptions`. Single line: `singleLine = true` (value form) or `lineLimits = TextFieldLineLimits.SingleLine` (state form). IME action: `keyboardActions = KeyboardActions(onDone = { })` (value form) or `onKeyboardAction = KeyboardActionHandler { }` (state form).
- [MD] Every text field has a visible label; a placeholder is not a label. Show an error with `isError = true`, an error icon, and error text in `supportingText` that replaces the helper text and says how to fix the problem.
- [API] `KeyboardOptions(capitalization, autoCorrectEnabled, keyboardType, imeAction, ...)`: set `KeyboardType.Email`, `Number`, `Phone`, `Password`, `Uri` to match the content and `ImeAction.Next` / `Done` / `Search` to match the flow. The `autoCorrect: Boolean` constructor is deprecated.
- [API] Passwords: `SecureTextField` or `OutlinedSecureTextField` (1.4+), not a plain field with `PasswordVisualTransformation`. Default obfuscation is `TextObfuscationMode.System` since 1.5.
- [API] `TextFieldLabelPosition.Attached` is deprecated in 1.5; use `Inside`, `Cutout` or `Above`.
- [Conv] Complete form with validation and keyboard handling: `examples/FormScreen.kt`.

Source: https://m3.material.io/components/text-fields/guidelines , https://developer.android.com/develop/ui/compose/text/user-input , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Dialogs

- [API] `AlertDialog(onDismissRequest, confirmButton, modifier, dismissButton, icon, title, text, shape, containerColor, ..., properties: DialogProperties)` is stable. `BasicAlertDialog(onDismissRequest, modifier, properties) { }` is the custom-content form (stable in 1.5, experimental in 1.4); the old `AlertDialog(onDismissRequest) { content }` overload is deprecated.
- [MD] Use a dialog for critical information or a decision that must be taken before continuing, sparingly. Low-priority feedback belongs in a snackbar.
- [MD] Buttons are text buttons; the confirming action is labelled with a verb that names the outcome ("Delete"), the dismissing one with "Cancel".
- [API] `onDismissRequest` runs on Back and on outside taps; treat it as cancel. Block dismissal only with `DialogProperties(dismissOnBackPress = false, dismissOnClickOutside = false)` and only when losing the dialog would lose work.
- [Conv] Show a dialog from state (`if (showDialog) AlertDialog(...)`) and keep that state saveable. Complete example: `examples/Feedback.kt`.

Source: https://m3.material.io/components/dialogs/guidelines , https://developer.android.com/develop/ui/compose/components/dialog

## Bottom sheets

| Need | 1.4 | 1.5 |
|---|---|---|
| Show a modal sheet | `ModalBottomSheet(onDismissRequest) { }` | same |
| Hold the state | `rememberModalBottomSheetState(skipPartiallyExpanded = ...)` | `rememberBottomSheetState(initialValue, enabledValues, confirmValueChange)`; the 1.4 factory is deprecated |
| Skip the half-expanded stop | `skipPartiallyExpanded = true` | `enabledValues` without `SheetValue.PartiallyExpanded` |
| Opt-in | `ExperimentalMaterial3Api` | `ExperimentalMaterial3Api` |

- [API] `ModalBottomSheet`, `BottomSheetScaffold` and `SheetState` are experimental in 1.4, 1.5 and 1.6 alpha. `SheetState.show()`, `hide()`, `expand()`, `partialExpand()` are `suspend`.
- [API] In 1.5 the sheet no longer drops the partially expanded stop by itself for short content; control the stops through `enabledValues`.
- [API] Insets go through `contentWindowInsets: () -> WindowInsets`; the default keeps content clear of the navigation bar. The sheet supports predictive back on Android 14+ and is first in accessibility traversal, before the scrim.
- [MD] Modal sheets hold secondary content or a short list of actions tied to the current screen; they are not for critical decisions. They are dismissed by swiping down, tapping the scrim or Back.
- [Conv] Own a `showSheet` boolean; do not render the sheet from `sheetState.isVisible`. To close with the animation after an item tap: `scope.launch { sheetState.hide() }.invokeOnCompletion { if (!sheetState.isVisible) showSheet = false }`.
- [Conv] If the code does not need the state, omit `sheetState`: the call is then identical on 1.4 and 1.5 (as in `examples/Feedback.kt`).

Source: https://m3.material.io/components/bottom-sheets/guidelines , https://developer.android.com/develop/ui/compose/components/bottom-sheets , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Snackbars

- [API] `val hostState = remember { SnackbarHostState() }`, `Scaffold(snackbarHost = { SnackbarHost(hostState) })`, then `hostState.showSnackbar(message, actionLabel, withDismissAction, duration): SnackbarResult` from a coroutine. It suspends until the snackbar is dismissed or its action is tapped (`SnackbarResult.ActionPerformed` or `Dismissed`).
- [API] `SnackbarDuration` is `Short`, `Long` or `Indefinite`. Calls are queued: only one snackbar shows at a time.
- [MD] Snackbars give low-priority feedback about a process, with at most one text action. One without an action may leave by itself; one with an action should stay until the user acts or dismisses it. A snackbar must not be the only way to reach a core function.
- [Conv] Launch from a scope that outlives the click handler (`rememberCoroutineScope()` or a view-model event), resolve strings before launching.

Source: https://m3.material.io/components/snackbar/guidelines , https://developer.android.com/develop/ui/compose/components/snackbar

## Menus and tooltips

- [API] `DropdownMenu(expanded, onDismissRequest, modifier, offset, scrollState, properties, shape, containerColor, ...) { DropdownMenuItem(text, onClick, leadingIcon, trailingIcon, enabled) }`. Anchor it by placing it in the same `Box` as the button that opens it.
- [API] 1.5 adds expressive menus: `DropdownMenuPopup`, `DropdownMenuGroup`, and a `DropdownMenuItem(onClick, text, shape, ..., supportingText)` overload. (Material 3 Expressive)
- [API] Exposed dropdown: `ExposedDropdownMenuBox(expanded, onExpandedChange) { TextField(..., modifier = Modifier.menuAnchor(ExposedDropdownMenuAnchorType.PrimaryNotEditable)); ExposedDropdownMenu(expanded, onDismissRequest) { } }`. Stable in 1.5, opt-in in 1.4; the argument-less `menuAnchor()` is deprecated in 1.4 and gone in 1.5.
- [API] Tooltips: `TooltipBox(positionProvider = TooltipDefaults.rememberTooltipPositionProvider(TooltipAnchorPosition.Above), tooltip = { PlainTooltip { Text(label) } }, state = rememberTooltipState()) { IconButton(...) }`. All tooltip API is experimental in 1.4, 1.5 and 1.6 alpha; `TooltipAnchorPosition` exists from 1.4.
- [MD] A plain tooltip labels an icon-only control on long press or hover; it supplements the `contentDescription`, it does not replace it. Never put essential information only in a tooltip.

Source: https://m3.material.io/components/menus/overview , https://m3.material.io/components/tooltips/overview , https://developer.android.com/develop/ui/compose/components/menu

## Date and time pickers

- [API] `DatePickerDialog(onDismissRequest, confirmButton, modifier, dismissButton, ...) { DatePicker(state = rememberDatePickerState(initialSelectedDateMillis = ...)) }`. Read `state.selectedDateMillis` (a `Long?` in UTC milliseconds) in the confirm button. Stable from 1.4.
- [API] `rememberDatePickerState` also takes `initialDisplayedMonthMillis`, `yearRange`, `initialDisplayMode` and `selectableDates`; a `LocalDate` overload is `@RequiresApi(26)`. Ranges: `DateRangePicker` with `rememberDateRangePickerState`.
- [API] `TimePickerDialog(onDismissRequest, confirmButton, title, modifier, properties, modeToggleButton, dismissButton, ...) { TimePicker(state) }` with `rememberTimePickerState(initialHour, initialMinute, is24Hour)`; read `state.hour` and `state.minute`. The dialog is stable from 1.4; `TimePicker`, `TimeInput` and the state factory need the opt-in on 1.4 and are stable in 1.5.
- [Conv] Use the pickers instead of hand-built date fields; convert UTC milliseconds with `Instant.ofEpochMilli(millis).atZone(ZoneOffset.UTC).toLocalDate()`, not the device zone.

Source: https://m3.material.io/components/date-pickers/overview , https://m3.material.io/components/time-pickers/overview , https://developer.android.com/develop/ui/compose/components/datepickers

## Cards, list items and dividers

| ListItem call | 1.4 | 1.5 |
|---|---|---|
| `ListItem(headlineContent, modifier, overlineContent, supportingContent, leadingContent, trailingContent, colors, tonalElevation, shadowElevation)` | the only form | deprecated |
| `ListItem(modifier, enabled, leadingContent, trailingContent, overlineContent, supportingContent, verticalAlignment, shapes, colors, elevation, contentPadding) { headline }` | - | stable |
| `ListItem(onClick, ...) { }`, `ListItem(selected, onClick, ...) { }`, `ListItem(checked, onCheckedChange, ...) { }` (add `onLongClick`, `onLongClickLabel`, `interactionSource`) | - | stable |
| `SegmentedListItem(..., shapes = ListItemDefaults.segmentedShapes(index, count)) { }` | - | stable (Material 3 Expressive) |

- [Conv] On 1.4 make a row interactive with `Modifier.clickable` or `Modifier.toggleable` on the `ListItem`; on 1.5 prefer the interactive overloads. `examples/SettingsScreen.kt` shows both ideas.
- [API] `Card`, `ElevatedCard`, `OutlinedCard`: `(modifier, shape, colors, elevation, border) { }` and a clickable overload `(onClick, modifier, enabled, ...) { }`. Use the clickable overload instead of `Modifier.clickable` on a card so shape, ripple and semantics match.
- [API] `HorizontalDivider(modifier, thickness, color)` and `VerticalDivider`. `Divider` is deprecated.
- [MD] Dividers separate groups of content; do not put one between every row when spacing already separates them.

Source: https://m3.material.io/components/lists/guidelines , https://m3.material.io/components/cards/overview , https://m3.material.io/components/divider/overview

## Progress, loading and badges

- [API] Indeterminate: `LinearProgressIndicator()` or `CircularProgressIndicator()`. Determinate: `progress = { fraction }` (a lambda); the `progress: Float` overloads are deprecated.
- [API] `LinearWavyProgressIndicator` and `CircularWavyProgressIndicator` are stable in 1.5. `LoadingIndicator` and `ContainedLoadingIndicator` need `@OptIn(ExperimentalMaterial3ExpressiveApi::class)`. (Material 3 Expressive)
- [Conv] Progress components expose progress semantics themselves; add a `contentDescription` saying what is loading when the surrounding text does not.
- [API] `BadgedBox(badge = { Badge { Text("3") } }) { Icon(...) }`; navigation items take a `badge` slot. [Conv] Include the count in the item's accessible text ("Inbox, 3 new").

Source: https://m3.material.io/components/progress-indicators/overview , https://m3.material.io/components/loading-indicator/overview , https://m3.material.io/components/badges/overview

## Carousel, pull to refresh, swipe to dismiss

- [API] `HorizontalMultiBrowseCarousel(state = rememberCarouselState { items.size }, preferredItemWidth = 186.dp, itemSpacing = 8.dp) { index -> ... }` (package `androidx.compose.material3.carousel`); clip items with `Modifier.maskClip(shape)` from `CarouselItemScope`. Stable in 1.5, opt-in in 1.4.
- [API] `PullToRefreshBox(isRefreshing, onRefresh, modifier, state, contentAlignment, indicator) { scrollable content }` (package `androidx.compose.material3.pulltorefresh`), stable from 1.4; `enabled` and `threshold` are new in 1.5.
- [API] `SwipeToDismissBox(state = rememberSwipeToDismissBoxState(), backgroundContent = { }, enableDismissFromStartToEnd, enableDismissFromEndToStart, onDismiss = { value -> }) { row }`; values `Settled`, `StartToEnd`, `EndToStart`. The `confirmValueChange` state parameter is deprecated.
- [Conv] A swipe or pull gesture is never the only way to do something: offer the same action in a menu or button, and expose it to accessibility services with `customActions` (see `references/accessibility-implementation.md`).

Source: https://m3.material.io/components/carousel/overview , https://developer.android.com/develop/ui/compose/components/pull-to-refresh , https://developer.android.com/develop/ui/compose/touch-input/user-interactions/swipe-to-dismiss

## Common mistakes

- `Divider()`, `ListItem(headlineContent = ...)`, `Slider(value = ...)`, `LinearProgressIndicator(progress = 0.5f)` in new 1.5 code -> the replacements above.
- Placeholder as the only label, or error shown only by red color -> `label`, `isError`, error text in `supportingText`.
- Password in a plain `TextField` -> `SecureTextField`.
- `showSnackbar` or `sheetState.hide()` called outside a coroutine -> `scope.launch { }`.
- Custom `Dialog { Surface { } }` for a simple confirmation -> `AlertDialog`.
- Snackbar drawn in a custom `Box` overlay -> `Scaffold(snackbarHost = ...)`.
- `ModalBottomSheet` or `TooltipBox` used without stating the opt-in -> `@OptIn(ExperimentalMaterial3Api::class)` on that function, and say it.
- `ButtonGroup`, `ToggleButton` or `FloatingActionButtonMenu` on material3 1.4 -> they need 1.5; use the fallbacks.
- `Checkbox` with its own callback next to separately clickable text -> one `toggleable` row, `onCheckedChange = null`.
- Three text fields for a date -> `DatePickerDialog`.
- Fixed `Modifier.height` on buttons, chips or list rows -> `heightIn(min = ...)`.
