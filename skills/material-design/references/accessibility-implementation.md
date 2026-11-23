# Accessibility implementation in Compose and Views

Scope: the code side of accessibility on Android: Compose semantics, labels and state, merging, traversal, custom actions and live regions, minimum interactive size, font scaling, short correct snippets, View equivalents, testing with TalkBack, Accessibility Scanner and Compose UI tests, and the most common implementation mistakes.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Semantics API at a glance
- Labels: contentDescription and visible text
- Merging and clearing
- Role, state and custom controls
- Headings, traversal order and panes
- Custom actions and live regions
- Minimum interactive size
- Font scaling and reflow
- Color is never the only signal
- Views equivalents
- Testing
- Common mistakes

## Semantics API at a glance

Everything below is in Compose UI and Foundation 1.13 (`androidx.compose.ui.semantics`, `androidx.compose.foundation`), stable, no opt-in.

| Need | API |
|---|---|
| Add or override semantics | `Modifier.semantics(mergeDescendants = false) { }` |
| Replace all descendant semantics | `Modifier.clearAndSetSemantics { }` |
| Label a graphic | `contentDescription` parameter of `Icon` and `Image`, or `contentDescription = "..."` in `semantics` |
| Decorative graphic | `contentDescription = null` |
| Hide from accessibility services | `hideFromAccessibility()`; `invisibleToUser()` is deprecated |
| State in words | `stateDescription = "..."` |
| Role | `role = Role.Button`, `Checkbox`, `Switch`, `RadioButton`, `Tab`, `Image`, `DropdownList`, `ValuePicker`, `Carousel` |
| Heading | `heading()` |
| Live region | `liveRegion = LiveRegionMode.Polite` or `Assertive` |
| Pane or window title | `paneTitle = "..."` |
| Custom actions | `customActions = listOf(CustomAccessibilityAction(label) { ...; true })` |
| Traversal order | `isTraversalGroup = true`, `traversalIndex = -1f`; `isContainer` is deprecated |
| Error | `error("description")` |
| Selection, toggle, range | `selected`, `toggleableState`, `progressBarRangeInfo`, `setProgress { }`, `selectableGroup()`, `collectionInfo`, `collectionItemInfo` |
| Click with label and role | `Modifier.clickable(enabled, onClickLabel, role, interactionSource, onClick)` |
| Whole-row toggle or selection | `Modifier.toggleable(value, enabled, role, interactionSource, onValueChange)`, `Modifier.selectable(selected, enabled, role, interactionSource, onClick)`, `Modifier.triStateToggleable(state, ...)` |
| Long press with label | `Modifier.combinedClickable(onClickLabel, role, onLongClickLabel, onLongClick, onDoubleClick, ..., onClick)` |

- [API] Material components (`Button`, `IconButton`, `Switch`, `Slider`, `ListItem(onClick = ...)`, text fields, navigation items) set role, state and actions themselves. Add semantics only for what they cannot know: the label of an icon, the meaning of a state.
- [Conv] Prefer a standard component over a custom one: every custom control has to re-create this table by hand.

Source: https://developer.android.com/develop/ui/compose/accessibility/semantics , https://developer.android.com/reference/kotlin/androidx/compose/ui/semantics/package-summary

## Labels: contentDescription and visible text

- [MD] `contentDescription` is mainly for graphic elements. Give every meaningful `Icon` and `Image` a localized description; pass `null` when the element is decorative or its meaning is already in adjacent text.
- [API] `Icon(painter, contentDescription, ...)` has no default for `contentDescription`: the choice is explicit at every call.
- [Conv] Describe purpose, not appearance, and leave out the role and state: "Delete", not "Trash can icon" or "Delete button". TalkBack appends the role and state from semantics.
- [Conv] Text is its own label: do not add a `contentDescription` that repeats or contradicts visible text. Use string resources so labels are translated.
- [API] `Modifier.clickable(onClickLabel = "open message")` makes TalkBack say "double tap to open message" instead of the generic "activate".

```kotlin
// material3 1.2+; no opt-in. Not compiled.
IconButton(onClick = onDelete) {                       // button role and 48dp target from IconButton
    Icon(
        painter = painterResource(R.drawable.ic_delete),
        contentDescription = stringResource(R.string.delete), // the button's only label
    )
}
Image(painter = painterResource(R.drawable.banner), contentDescription = null) // decorative
```

Source: https://developer.android.com/develop/ui/compose/accessibility/api-defaults , https://developer.android.com/develop/ui/compose/accessibility/semantics

## Merging and clearing

- [API] `clickable`, `toggleable` and `selectable` merge their descendants into one accessibility node: the row is read and activated as one element.
- [API] `Modifier.semantics(mergeDescendants = true) { }` groups a non-interactive block (avatar, name, date) so it is one swipe instead of three.
- [API] `Modifier.clearAndSetSemantics { }` drops all descendant semantics and replaces them; use it when the merged reading would be wrong or noisy and you supply a complete replacement.
- [MD] A row with a control and a label is one target: put the modifier on the row and pass `null` as the control's callback, as the guide's checkbox example does.
- [Conv] Do not nest clickable elements inside a merged clickable row unless they are real secondary actions; expose those as custom actions too.

```kotlin
// foundation and ui 1.13, material3 1.2+; no opt-in. Not compiled.
Row(
    modifier = Modifier
        .fillMaxWidth()
        .toggleable(value = checked, role = Role.Checkbox, onValueChange = onCheckedChange)
        .padding(horizontal = 16.dp)
        .heightIn(min = 56.dp),                        // row is the touch target; grows with text
    verticalAlignment = Alignment.CenterVertically,
) {
    Checkbox(checked = checked, onCheckedChange = null) // display only: no second target
    Text(text = label, modifier = Modifier.padding(start = 16.dp))
}

Row(Modifier.semantics(mergeDescendants = true) { }) {  // read as one item
    Image(painter = avatar, contentDescription = null)
    Column { Text(author); Text(postedAt) }
}
```

Source: https://developer.android.com/develop/ui/compose/accessibility/merging-clearing , https://developer.android.com/develop/ui/compose/accessibility/api-defaults

## Role, state and custom controls

- [API] A custom control needs four things: an action (`clickable`, `toggleable`, `selectable` or semantics actions), a `role`, a label, and its state (`toggleableState` or `selected` come from the modifiers; add `stateDescription` when "on/off" is not meaningful).
- [API] An adjustable custom control (rating, stepper, custom slider) exposes `progressBarRangeInfo = ProgressBarRangeInfo(current, range, steps)` and `setProgress { value -> ...; true }` so services can read and change the value.
- [Conv] Make custom controls focusable and operable from a keyboard: the foundation modifiers above do this; raw `pointerInput` gesture detectors do not.
- [Conv] Complete toggle and rating examples: `examples/AccessibleCustomControl.kt`.

```kotlin
// foundation and ui 1.13, material3 1.3+; no opt-in. Not compiled.
Box(
    modifier = Modifier
        .toggleable(value = subscribed, role = Role.Switch, onValueChange = onSubscribedChange)
        .minimumInteractiveComponentSize()             // reserve 48dp around the 24dp icon
        .semantics {
            contentDescription = subscribeLabel        // what it is
            stateDescription = if (subscribed) subscribedText else notSubscribedText // its state
        },
    contentAlignment = Alignment.Center,
) {
    Icon(
        painter = painterResource(if (subscribed) R.drawable.ic_bell_filled else R.drawable.ic_bell),
        contentDescription = null,                     // parent carries the label
    )
}

// Adjustable value exposed to accessibility services.
Modifier.semantics {
    contentDescription = ratingLabel
    progressBarRangeInfo = ProgressBarRangeInfo(current = rating.toFloat(), range = 0f..5f, steps = 4)
    setProgress { value -> onRatingChange(value.roundToInt()); true }
}
```

Source: https://developer.android.com/develop/ui/compose/accessibility/semantics , https://developer.android.com/guide/topics/ui/accessibility/principles

## Headings, traversal order and panes

- [API] Mark section titles with `Modifier.semantics { heading() }` so screen reader users can move between sections.
- [API] Default traversal follows layout order. Use `isTraversalGroup = true` to keep a group's elements together and `traversalIndex` (lower first) to reorder inside a group, only where the default order is wrong (for example a FAB that should be reached before a long list).
- [API] `paneTitle = "..."` announces a pane or window change; Material sheets, dialogs and drawers set it themselves.
- [API] `ModalBottomSheet` is first in traversal order, followed by its scrim; `Scaffold` orders top bar, bottom bar, FAB, content, snackbar.
- [Conv] Fix order by fixing layout order first; `traversalIndex` scattered across a screen is a maintenance trap.

```kotlin
// ui 1.13; no opt-in. Not compiled.
Text(
    text = stringResource(R.string.section_notifications),
    style = MaterialTheme.typography.titleSmall,
    modifier = Modifier.semantics { heading() },
)
```

Source: https://developer.android.com/develop/ui/compose/accessibility/traversal , https://developer.android.com/develop/ui/compose/accessibility/semantics , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Custom actions and live regions

- [API] Gestures such as swipe to dismiss, drag to reorder or long press are not available to every user. Add `customActions = listOf(CustomAccessibilityAction(label = "...") { doIt(); true })` on the item so the action appears in the TalkBack actions menu, and keep a visible alternative (menu or button).
- [API] For rows with several buttons, moving the secondary actions into custom actions on the row lets users swipe through items instead of through every button.
- [API] `liveRegion = LiveRegionMode.Polite` announces changes to a node without moving focus. [MD] Use `Polite` in most cases and `Assertive` sparingly, only for information that must interrupt.
- [Conv] Material's snackbar host and text field error state expose their own announcements; do not wrap them in another live region.
- [Conv] Do not move accessibility focus programmatically except to a newly opened dialog or pane (which the components already do).

```kotlin
// material3 1.4+, ui 1.13; no opt-in. Not compiled.
SwipeToDismissBox(
    state = dismissState,
    backgroundContent = { DeleteBackground() },
    onDismiss = { onDelete(item) },
    modifier = Modifier.semantics {
        customActions = listOf(CustomAccessibilityAction(deleteLabel) { onDelete(item); true })
    },
) { MessageRow(item) }

Text(
    text = statusText,                                  // "3 results", "Upload failed"
    modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
)
```

Source: https://developer.android.com/develop/ui/compose/accessibility/semantics

## Minimum interactive size

| API | Status |
|---|---|
| `Modifier.minimumInteractiveComponentSize()` (`androidx.compose.material3`) | stable; reserves at least 48dp x 48dp of layout space |
| `LocalMinimumInteractiveComponentSize: ProvidableCompositionLocal<Dp>` | stable (material3 1.3+); the size the modifier and components use |
| `LocalMinimumInteractiveComponentEnforcement` | deprecated (and experimental); replaced by the local above |
| `LocalMinimumTouchTargetEnforcement` | Material 2 only; does not exist in Material 3 |

- [MD] Give every interactive element a touch target of at least 48dp x 48dp; larger is better.
- [API] Material controls (`IconButton`, `Checkbox`, `RadioButton`, `Switch`, `Slider`, clickable `Surface`) reserve that size themselves, but only when they can receive input: a `Checkbox` with `onCheckedChange = null` reserves nothing.
- [API] For a small custom element put the click modifier first, then `minimumInteractiveComponentSize()`, then any size modifier: `Modifier.clickable { }.minimumInteractiveComponentSize().size(24.dp)`. A size modifier placed before it limits the space it can reserve.
- [Conv] Alternative without Material: `Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)` on the clickable element.
- [Conv] Do not provide a smaller `LocalMinimumInteractiveComponentSize` app-wide to tighten layouts. If a dense toolbar truly needs it, scope it to that subtree and keep 48dp spacing between target centers.
- [Conv] Targets must not overlap; check rows of icon buttons and chips at the largest font size.

Source: https://developer.android.com/develop/ui/compose/accessibility/api-defaults , https://developer.android.com/guide/topics/ui/accessibility/apps

## Font scaling and reflow

- [API] Text sized in `sp` follows the user's font size; Compose applies the platform's non-linear scaling, and Android 14+ scales up to 200%.
- [Conv] Use `MaterialTheme.typography` styles; never size text in `dp` and never cap scaling by dividing by `fontScale`.
- [Conv] Containers grow with text: `heightIn(min = ...)` instead of `height(...)`, wrapping `Text` instead of `maxLines = 1` on essential labels, `FlowRow` or a `Column` instead of a `Row` that cannot fit, and scrolling for any screen whose content can exceed the window.
- [Conv] Check every screen at the largest font size and display size, in both orientations and in a narrow split-screen window.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://developer.android.com/jetpack/androidx/releases/compose-ui

## Color is never the only signal

- [MD] Do not use color as the only way to convey state or meaning: pair it with text, an icon or a shape change.
- [MD] Text contrast: at least 4.5:1 for text smaller than 18sp (or bold and smaller than 14sp), at least 3:1 for larger text. Theme role pairs (`primary` / `onPrimary`, `surface` / `onSurface`) are designed to meet this.
- [API] Text fields: `isError = true` together with error text in `supportingText`; the color change alone is not enough.

```kotlin
// material3 1.2+; no opt-in. Not compiled.
Row(verticalAlignment = Alignment.CenterVertically) {
    Icon(                                               // shape differs per status
        painter = painterResource(if (failed) R.drawable.ic_error else R.drawable.ic_check_circle),
        contentDescription = null,                      // the text next to it says the same
        tint = if (failed) MaterialTheme.colorScheme.error else MaterialTheme.colorScheme.primary,
    )
    Text(
        text = stringResource(if (failed) R.string.sync_failed else R.string.synced), // words
        modifier = Modifier.padding(start = 8.dp),
    )
}
```

Source: https://developer.android.com/guide/topics/ui/accessibility/apps , https://m3.material.io/foundations/accessible-design/overview

## Views equivalents

| Need | Compose | Views |
|---|---|---|
| Label a graphic | `contentDescription` | `android:contentDescription` |
| Decorative graphic | `contentDescription = null` | `android:importantForAccessibility="no"` |
| Label for an input | `label = { Text(...) }` on the text field | `android:hint` on `TextInputLayout`, or `android:labelFor` on a `TextView` |
| Heading | `heading()` | `android:accessibilityHeading="true"` / `ViewCompat.setAccessibilityHeading` |
| State in words | `stateDescription` | `ViewCompat.setStateDescription` |
| Live region | `liveRegion` | `android:accessibilityLiveRegion` |
| Pane title | `paneTitle` | `android:accessibilityPaneTitle` / `ViewCompat.setAccessibilityPaneTitle` |
| Custom action | `customActions` | `ViewCompat.addAccessibilityAction` |
| Click label | `onClickLabel` | `ViewCompat.replaceAccessibilityAction` with a label |
| Group as one element | `semantics(mergeDescendants = true)` | focusable container; `android:screenReaderFocusable="true"` |
| Traversal order | `isTraversalGroup`, `traversalIndex` | `android:accessibilityTraversalBefore` / `After` |
| Minimum target | `minimumInteractiveComponentSize()` | `android:minWidth` / `android:minHeight` of 48dp, `TouchDelegate` |
| Error on a field | `isError` + `supportingText` | `TextInputLayout.setError`, `app:errorAccessibilityLiveRegion` |

- [Unverified] The framework and `ViewCompat` names in the Views column are long-standing platform API recalled from the Android accessibility guides; they were not re-fetched from the API reference in this pass. The `TextInputLayout` rows were checked against the MDC-Android documentation.
- [Conv] More on View widgets: `references/implementation-views.md`.

Source: https://developer.android.com/guide/topics/ui/accessibility/principles , https://developer.android.com/guide/topics/ui/accessibility/apps

## Testing

- [MD] Manual testing with accessibility services is essential: turn on TalkBack and complete each main flow by swiping and double-tapping, then try Switch Access and a hardware keyboard.
- [MD] Accessibility Scanner (an app built on the Accessibility Test Framework) scans a screen and suggests fixes for content labels, touch target size, contrast and clickable items. Run it on every new screen; it does not replace a screen reader pass.
- [API] Layout Inspector in Android Studio shows each composable's semantics; TalkBack developer settings can print the node tree.
- [API] Compose UI tests query the semantics tree (`androidx.compose.ui.test`): finders `onNodeWithText`, `onNodeWithContentDescription`, `onNodeWithTag`; matchers `hasContentDescription`, `hasStateDescription`, `hasClickAction`, `isHeading()`, `isToggleable()`, `isSelectable()`, `isOn()`, `isOff()`, `isSelected()`, `hasProgressBarRangeInfo`; assertions `assertIsOn()`, `assertIsOff()`, `assertIsSelected()`, `assertHasClickAction()`, `assertContentDescriptionEquals(...)`, `assertTouchWidthIsEqualTo(...)`, `assertTouchHeightIsEqualTo(...)`, `assertHeightIsAtLeast(...)`; action `performCustomAccessibilityActionWithLabel(label)` (`@ExperimentalTestApi`).
- [API] Automated accessibility checks (Compose 1.8+): add `androidx.compose.ui:ui-test-junit4-accessibility`, call `composeTestRule.enableAccessibilityChecks()`, then any action or `onRoot().tryPerformAccessibilityChecks()` runs the Accessibility Test Framework checks (missing labels, low contrast, small targets, traversal order). `enableAccessibilityChecks` is annotated `@RequiresApi(34)`.
- [API] In the Compose 1.14 alpha API file the `createComposeRule` and `createAndroidComposeRule` functions in `androidx.compose.ui.test.junit4` are deprecated in favor of the same names in `androidx.compose.ui.test.junit4.v2`; check which the project's version offers.
- [Conv] Assert semantics, not pixels: a test that finds the control by its accessible name and asserts its state doubles as an accessibility regression test.

```kotlin
// ui-test-junit4 1.13, ui-test-junit4-accessibility; test device API 34+ for the checks. Not compiled.
@get:Rule val composeTestRule = createAndroidComposeRule<ComponentActivity>()

@SdkSuppress(minSdkVersion = 34) @Test fun favoriteToggle_exposesNameStateAndSize() { // checks need API 34
    composeTestRule.setContent { AppTheme { FavoriteToggle(favorite = false, onFavoriteChange = {}) } }
    composeTestRule.enableAccessibilityChecks()
    composeTestRule.onNodeWithContentDescription("Favorite")
        .assertIsOff()
        .assertHasClickAction()
        .assertTouchHeightIsEqualTo(48.dp)
        .performClick()                                 // also runs the accessibility checks
}
```

Source: https://developer.android.com/develop/ui/compose/accessibility/testing , https://developer.android.com/develop/ui/compose/accessibility/inspect-debug , https://developer.android.com/guide/topics/ui/accessibility/testing , https://developer.android.com/reference/kotlin/androidx/compose/ui/test/package-summary

## Common mistakes

- `Icon(..., contentDescription = null)` inside an `IconButton` -> localized description; `null` only for decorative icons.
- `contentDescription = "Delete button"` or a description that repeats visible text -> name the purpose only; role and state come from semantics.
- `Modifier.clickable { }` on a custom control with no role or label -> `clickable(onClickLabel = ..., role = Role.Button)`, or use `Button`, `IconButton`, `Surface(onClick = ...)`.
- 24dp icon with a bare `clickable` -> `IconButton`, or `clickable { }.minimumInteractiveComponentSize().size(24.dp)`.
- `Checkbox(checked, onCheckedChange)` beside separately clickable text -> one `toggleable(role = Role.Checkbox)` row with `onCheckedChange = null`.
- List row whose children are announced one by one -> `clickable` or `toggleable` on the row, or `ListItem(onClick = ...)`.
- Section titles as plain `Text` -> `semantics { heading() }`.
- `semantics { invisibleToUser() }` or `isContainer = true` -> `hideFromAccessibility()`, `isTraversalGroup = true`.
- Swipe, drag or long press as the only way to act -> visible alternative plus `customActions`.
- Error or selection shown only by color -> text, icon or shape as well; `isError` plus `supportingText`.
- `Modifier.height(48.dp)` around text, text sized in dp -> `heightIn(min = 48.dp)`, sp through the type scale.
- `LocalMinimumInteractiveComponentEnforcement provides false` app-wide -> keep the 48dp reservation.
- Tested only by looking at it -> TalkBack pass, Accessibility Scanner, semantics assertions in UI tests.
