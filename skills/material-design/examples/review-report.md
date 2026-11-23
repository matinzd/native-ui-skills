# Example: a complete Material review

An illustration of the review format from `SKILL.md`, applied to one Jetpack Compose file. The code under review
is shown first so the findings can be followed. Sources were checked on 2026-11-23.

## Input

Request: "Review CreatePlaylistScreen.kt. Phone app, minSdk 26, targetSdk 36, Compose Material 3 1.5.0. The
screen opens from the library tab; `coverUpload` is null until a cover image is uploading."

```kotlin
// Before: the code under review (deliberately flawed; do not copy). Imports omitted.
@Composable
fun CreatePlaylistScreen(coverUpload: Float?, onClose: () -> Unit, onPickCover: () -> Unit,
                         onAddSongs: () -> Unit, onCreate: (String, Boolean) -> Unit) {
    var name by rememberSaveable { mutableStateOf("") }
    var isPrivate by rememberSaveable { mutableStateOf(false) }
    var showDiscard by rememberSaveable { mutableStateOf(false) }
    BackHandler { showDiscard = true }
    Scaffold(
        topBar = {
            SmallTopAppBar(title = { Text("New playlist") }, navigationIcon = {
                IconButton({ showDiscard = true }) { Icon(painterResource(R.drawable.ic_close), "Close") }
            })
        },
        floatingActionButton = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                FloatingActionButton(onPickCover) { Icon(painterResource(R.drawable.ic_image), "Choose cover") }
                FloatingActionButton(onAddSongs) { Icon(painterResource(R.drawable.ic_add), "Add songs") }
            }
        },
    ) { innerPadding ->
        Column(Modifier.padding(innerPadding).padding(16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            OutlinedTextField(name, { name = it }, Modifier.fillMaxWidth(), placeholder = { Text("Playlist name") })
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Private", Modifier.weight(1f))
                Switch(checked = isPrivate, onCheckedChange = { isPrivate = it })
            }
            if (coverUpload != null) LinearProgressIndicator(progress = coverUpload, Modifier.fillMaxWidth())
            Button({ onCreate(name, isPrivate) }, Modifier.fillMaxWidth()) { Text("CREATE PLAYLIST") }
        }
    }
    if (showDiscard) AlertDialog(
        onDismissRequest = { showDiscard = false }, title = { Text("Discard this playlist?") },
        confirmButton = { TextButton(onClick = onClose) { Text("Discard") } },
        dismissButton = { Row {
            TextButton({ showDiscard = false; onAddSongs() }) { Text("Add songs first") }
            TextButton({ showDiscard = false }) { Text("Keep editing") }
        } },
    )
}
```

## Output

## Material review: CreatePlaylistScreen.kt
Target: phone, minSdk 26 / targetSdk 36, Compose Material 3 1.5.0 (all stated). Evidence: source code only, so
rendered sizes, contrast, and TalkBack output were not measured.

### 1. `SmallTopAppBar` does not exist in Material 3 1.5
- Class: Confirmed guideline or API violation
- Severity: High
- Where: `topBar = { SmallTopAppBar(...) }`
- Why: The function was deprecated in 1.0.0-beta02 in favour of `TopAppBar` and is absent from the 1.5.0 API,
  so the file does not compile and nobody gets the screen.
- Source: https://developer.android.com/jetpack/androidx/releases/compose-material3 (API documentation)
- Fix: Rename it to `TopAppBar`; the `title` and `navigationIcon` arguments stay as they are. `TopAppBar` is
  stable in 1.5.0 and needs no opt-in.

### 2. The "Private" label and its switch are two separate elements
- Class: Accessibility issue
- Severity: Medium
- Where: the `Row` holding `Text("Private")` and `Switch`
- Why: The switch carries no label of its own, so a screen reader reaches the text and an unnamed switch as
  separate stops, and tapping the word "Private" does nothing. Android's guidance is to lift the toggle to the
  parent so label and control act as one.
- Source: https://developer.android.com/develop/ui/compose/accessibility/api-defaults (recommendation)
- Fix: `Row(Modifier.toggleable(value = isPrivate, role = Role.Switch, onValueChange = { isPrivate = it }),`
  `verticalAlignment = Alignment.CenterVertically) { ...; Switch(checked = isPrivate, onCheckedChange = null) }`

### 3. Back always opens the discard dialog
- Class: Platform convention mismatch
- Severity: Medium
- Where: `BackHandler { showDiscard = true }`
- Why: The handler is always enabled, so someone who opened the screen and typed nothing still has to answer
  a dialog to leave, and the system's predictive back animation never runs here. People expect Back to
  simply go back when there is nothing to lose.
- Source: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture (recommendation)
- Fix: `BackHandler(enabled = name.isNotBlank() && !showDiscard) { showDiscard = true }`. Apply the same
  condition to the close icon: call `onClose()` directly when `name` is blank.

### 4. Two FABs, neither for the screen's main action
- Class: Recommended improvement
- Severity: Medium
- Where: the `Column` of two `FloatingActionButton`s in `floatingActionButton`
- Why: Material reserves the FAB for the most important action on a screen and says not to show several.
  Here two secondary actions float above the content while the main action, creating the playlist, is the
  filled button below them, so the visual emphasis points the wrong way.
- Source: https://m3.material.io/components/floating-action-button/guidelines (recommendation)
- Fix: Remove the `floatingActionButton` slot and add both actions to the content column above the filled
  button: `OutlinedButton(onClick = onPickCover) { Text("Choose cover") }` and
  `OutlinedButton(onClick = onAddSongs) { Text("Add songs") }`.

### 5. The name field has a placeholder but no label
- Class: Recommended improvement
- Severity: Medium
- Where: `OutlinedTextField(..., placeholder = { Text("Playlist name") })`
- Why: Material says every text field should have a label that is always visible. The placeholder vanishes
  with the first character, after which nothing on screen says what the field is for.
- Source: https://m3.material.io/components/text-fields/guidelines (recommendation)
- Fix: Replace `placeholder = { Text("Playlist name") }` with `label = { Text("Playlist name") }`.

### 6. The discard dialog offers three actions
- Class: Recommended improvement
- Severity: Low
- Where: `dismissButton = { Row { ... } }` in the `AlertDialog`
- Why: Material limits a dialog to two actions, one confirming and one dismissing, and advises against a third
  that leads away from the decision. "Add songs first" does exactly that, and three text buttons in a row are
  likely to be cramped on a narrow phone.
- Source: https://m3.material.io/components/dialogs/guidelines (recommendation)
- Fix: `dismissButton = { TextButton(onClick = { showDiscard = false }) { Text("Keep editing") } }`. Adding
  songs stays available on the screen itself (finding 4).

### 7. Button label in capitals
- Class: Recommended improvement
- Severity: Low
- Where: `Text("CREATE PLAYLIST")`
- Why: Material asks for sentence case on button labels: capitalize only the first word and proper nouns.
- Source: https://m3.material.io/components/buttons/guidelines (recommendation)
- Fix: `Text("Create playlist")`.

### 8. Deprecated `LinearProgressIndicator(progress: Float)`
- Class: Confirmed guideline or API violation
- Severity: Low
- Where: `LinearProgressIndicator(progress = coverUpload, ...)`
- Why: The overload that takes a `Float` is deprecated in 1.5.0, and its replacement, which takes the progress
  as a lambda, has been in the library since 1.2.0-alpha10. It still compiles, with a warning.
- Source: https://developer.android.com/jetpack/androidx/releases/compose-material3 (API documentation)
- Fix: `LinearProgressIndicator(progress = { coverUpload }, modifier = Modifier.fillMaxWidth())`.

### 9. Create is enabled while the name is empty
- Class: Subjective design suggestion
- Severity: Low
- Where: `Button({ onCreate(name, isPrivate) }, ...)`
- Why: Opinion, no source. A tap with an empty field creates an unnamed playlist or fails somewhere the
  person cannot see.
- Fix: `enabled = name.isNotBlank()`, or keep it enabled and fall back to a default name such as "My playlist".

### Not verified
- What TalkBack announces for the "Private" row before and after finding 2: run the screen with TalkBack.
- Whether the predictive back animation plays once finding 3 is applied: that depends on how the host
  activity and navigation handle Back, which were not provided.
  Check: https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture
- Whether the column fits at the largest font size or with the keyboard open: it does not scroll, and no
  device run was available. Test at 200% font size and with the field focused.
- Contrast: every color comes from the theme, so it depends on the app's color scheme, which was not provided.

### What already works
- The content applies the `innerPadding` from `Scaffold`, so the app bar and system bars do not cover it.
- No hard-coded colors or font sizes: text, buttons, and the field take their styles from the theme.
- All three icons have content descriptions, and the dialog title is a specific question, not "Are you sure?".
