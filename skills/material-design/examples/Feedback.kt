// Feedback.kt
//
// Purpose: choosing the right feedback surface. A dialog for a decision that must be made
// before continuing (destructive confirmation), a modal bottom sheet for a short list of
// secondary actions, and a snackbar for low-priority, non-blocking confirmation with Undo.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x. Only the two ListItem(onClick)
//   rows need 1.5 (fallback on 1.4.x: ListItem(headlineContent = ...) with Modifier.clickable).
//   The rest is identical on 1.4.x: the sheet uses its default state, so neither
//   rememberBottomSheetState (1.5+) nor the 1.4 state factory that 1.5 deprecates is called.
// Opt-ins: ExperimentalMaterial3Api for ModalBottomSheet only (experimental in 1.4, 1.5 and
//   1.6 alpha). AlertDialog, Snackbar and Scaffold are stable.
// Resources assumed: R.string.more_actions, archive, delete, cancel, undo, archived_message,
//   delete_title, delete_body; R.drawable.ic_more_vert.
//
// Pages applied:
//   https://m3.material.io/components/dialogs/guidelines
//   https://m3.material.io/components/bottom-sheets/guidelines
//   https://m3.material.io/components/snackbar/guidelines
//   https://developer.android.com/develop/ui/compose/components/snackbar
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarDuration
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.SnackbarResult
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import kotlinx.coroutines.launch

@Composable
fun DocumentScreen(onArchive: () -> Unit, onUndoArchive: () -> Unit, onDelete: () -> Unit) {
    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    // Presentation state is plain saveable booleans owned by the screen.
    var showActions by rememberSaveable { mutableStateOf(false) }
    var confirmDelete by rememberSaveable { mutableStateOf(false) }
    val archivedMessage = stringResource(R.string.archived_message)
    val undoLabel = stringResource(R.string.undo)

    // Snackbars go through the Scaffold's host so they are placed above bars and FABs.
    Scaffold(snackbarHost = { SnackbarHost(snackbarHostState) }) { innerPadding ->
        Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.TopEnd) {
            IconButton(onClick = { showActions = true }) {
                Icon(painterResource(R.drawable.ic_more_vert), contentDescription = stringResource(R.string.more_actions))
            }
        }
    }

    if (showActions) {
        ActionsSheet(
            onDismiss = { showActions = false },
            onArchive = {
                showActions = false
                onArchive()
                // Snackbar: the action already happened and is reversible, so confirm it without
                // blocking and offer Undo. showSnackbar suspends until the snackbar is gone,
                // hence the coroutine.
                scope.launch {
                    val result = snackbarHostState.showSnackbar(
                        message = archivedMessage,
                        actionLabel = undoLabel, // a single text action
                        // Material: a snackbar with an action stays until the user acts on it
                        // or dismisses it, so give it a dismiss affordance.
                        duration = SnackbarDuration.Indefinite,
                        withDismissAction = true,
                    )
                    if (result == SnackbarResult.ActionPerformed) onUndoArchive()
                }
            },
            onDelete = { showActions = false; confirmDelete = true },
        )
    }

    if (confirmDelete) {
        // Dialog: deletion cannot be undone, so interrupt and require an explicit choice.
        AlertDialog(
            // Back and outside taps mean "cancel", never "confirm".
            onDismissRequest = { confirmDelete = false },
            // Title and text state the consequence; no "Are you sure?".
            title = { Text(stringResource(R.string.delete_title)) },
            text = { Text(stringResource(R.string.delete_body)) },
            confirmButton = {
                // The button names the action ("Delete"), not "OK". Error color on the
                // destructive action is this skill's convention, not a Material rule.
                TextButton(
                    onClick = { confirmDelete = false; onDelete() },
                    colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error),
                ) { Text(stringResource(R.string.delete)) }
            },
            dismissButton = {
                TextButton(onClick = { confirmDelete = false }) { Text(stringResource(R.string.cancel)) }
            },
        )
    }
}

// Bottom sheet: a few secondary actions related to the current content, easy to reach and
// easy to dismiss (swipe down, scrim tap, Back). Not for critical decisions.
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ActionsSheet(onDismiss: () -> Unit, onArchive: () -> Unit, onDelete: () -> Unit) {
    // Default sheetState and contentWindowInsets: the sheet keeps its content clear of the
    // navigation bar. Removing the sheet from composition (as the callers do) closes it
    // without the hide animation; to animate, hold the state and call its suspend hide().
    ModalBottomSheet(onDismissRequest = onDismiss) {
        ListItem(onClick = onArchive) { Text(stringResource(R.string.archive)) }
        ListItem(onClick = onDelete) { Text(stringResource(R.string.delete)) }
    }
}
