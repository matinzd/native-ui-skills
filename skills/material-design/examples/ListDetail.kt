// ListDetail.kt
//
// Purpose: a list-detail layout that shows one pane in compact windows and list plus detail
// side by side when the window is wide enough, with back navigation handled by the scaffold.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x for the ListItem(selected, onClick)
//   overload with a trailing content lambda (fallback on 1.4.x: ListItem(headlineContent = ...)
//   with Modifier.selectable); androidx.compose.material3.adaptive:adaptive,
//   adaptive-layout and adaptive-navigation 1.3.0 (the calls below exist since 1.1.0).
// Opt-ins: ExperimentalMaterial3AdaptiveApi. The pane scaffolds, AnimatedPane and the navigator
//   are experimental in every adaptive release to date, including "stable" 1.3.0. If the
//   project forbids experimental API, the stable alternative is your own Row of two panes
//   switched on currentWindowAdaptiveInfoV2().windowSizeClass.isWidthAtLeastBreakpoint(
//   WindowSizeClass.WIDTH_DP_EXPANDED_LOWER_BOUND), plus a BackHandler for the detail pane.
// Resources assumed: R.string.inbox, R.string.back, R.string.select_message,
//   R.drawable.ic_arrow_back (auto-mirrored vector).
//
// Pages applied:
//   https://developer.android.com/develop/ui/compose/layouts/adaptive/list-detail
//   https://developer.android.com/develop/ui/compose/layouts/adaptive/canonical-layouts
//   https://m3.material.io/foundations/layout/canonical-layouts
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.adaptive.ExperimentalMaterial3AdaptiveApi
import androidx.compose.material3.adaptive.layout.AnimatedPane
import androidx.compose.material3.adaptive.layout.ListDetailPaneScaffoldRole
import androidx.compose.material3.adaptive.navigation.NavigableListDetailPaneScaffold
import androidx.compose.material3.adaptive.navigation.rememberListDetailPaneScaffoldNavigator
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch

data class Message(val id: String, val sender: String, val subject: String, val body: String)

@OptIn(ExperimentalMaterial3AdaptiveApi::class)
@Composable
fun InboxScreen(messages: List<Message>) {
    // The content key (a message id) is saved with the navigator, so the open message survives
    // rotation and resizing. Use a small saveable key, not the whole object.
    val navigator = rememberListDetailPaneScaffoldNavigator<String>()
    val scope = rememberCoroutineScope()
    val selectedId = navigator.currentDestination?.contentKey
    val selected = messages.firstOrNull { it.id == selectedId }

    // The scaffold decides how many panes fit from the window size and posture, animates
    // between them, and handles system Back (including predictive back) from detail to list.
    NavigableListDetailPaneScaffold(
        navigator = navigator,
        listPane = {
            AnimatedPane {
                Scaffold(topBar = { TopAppBar(title = { Text(stringResource(R.string.inbox)) }) }) { innerPadding ->
                    LazyColumn(contentPadding = innerPadding) {
                        items(messages, key = { it.id }) { message ->
                            // Selectable overload: the open row stays marked as selected when
                            // both panes are visible, and the whole row is one touch target.
                            ListItem(
                                selected = message.id == selectedId,
                                onClick = {
                                    // navigateTo is a suspend function (adaptive 1.1+).
                                    scope.launch {
                                        navigator.navigateTo(ListDetailPaneScaffoldRole.Detail, message.id)
                                    }
                                },
                                supportingContent = { Text(message.subject, maxLines = 1) },
                            ) { Text(message.sender) }
                        }
                    }
                }
            }
        },
        detailPane = {
            AnimatedPane {
                Scaffold(
                    topBar = {
                        TopAppBar(
                            title = { Text(selected?.subject.orEmpty(), maxLines = 1) },
                            navigationIcon = {
                                // Show an Up arrow only when there is a list to go back to,
                                // that is when the detail pane covers the list.
                                if (navigator.canNavigateBack()) {
                                    IconButton(onClick = { scope.launch { navigator.navigateBack() } }) {
                                        Icon(
                                            painter = painterResource(R.drawable.ic_arrow_back),
                                            contentDescription = stringResource(R.string.back),
                                        )
                                    }
                                }
                            },
                        )
                    },
                ) { innerPadding ->
                    if (selected == null) {
                        // Two panes and nothing chosen yet: say what to do instead of leaving
                        // the pane blank.
                        Box(Modifier.fillMaxSize().padding(innerPadding), contentAlignment = Alignment.Center) {
                            Text(stringResource(R.string.select_message), style = MaterialTheme.typography.bodyLarge)
                        }
                    } else {
                        Text(
                            text = selected.body,
                            style = MaterialTheme.typography.bodyLarge,
                            // Scrolls: a long message or a large font size must stay readable.
                            modifier = Modifier
                                .padding(innerPadding)
                                .verticalScroll(rememberScrollState())
                                .padding(16.dp),
                        )
                    }
                }
            }
        },
    )
}
