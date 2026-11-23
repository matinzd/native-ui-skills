// SettingsScreen.kt
//
// Purpose: a settings screen: Scaffold with a pinned top app bar, sections with real headings,
// ListItem rows that toggle a Switch as one target, and a navigation row. Insets come from the
// Scaffold's innerPadding.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x; foundation and ui 1.13.
//   On material3 1.4.x two things differ: ListItem has only the (deprecated in 1.5)
//   headlineContent overload, and TopAppBarDefaults.pinnedScrollBehavior() needs
//   @OptIn(ExperimentalMaterial3Api::class).
// Opt-ins: none on material3 1.5.x.
// Resources assumed: R.string.settings, back, section_notifications, section_data,
//   push_title, push_summary, wifi_only_title, wifi_only_summary, storage_title,
//   storage_summary; R.drawable.ic_arrow_back (auto-mirrored vector).
//
// Pages applied:
//   https://m3.material.io/components/lists/guidelines
//   https://m3.material.io/components/switch/guidelines
//   https://developer.android.com/develop/ui/compose/components/scaffold
//   https://developer.android.com/develop/ui/compose/accessibility/merging-clearing
//   https://developer.android.com/develop/ui/compose/system/insets-ui
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import androidx.compose.foundation.layout.consumeWindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.selection.toggleable
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp

data class SettingsState(val pushEnabled: Boolean = true, val wifiOnly: Boolean = false)

@Composable
fun SettingsScreen(
    state: SettingsState,
    onStateChange: (SettingsState) -> Unit,
    onOpenStorage: () -> Unit,
    onBack: () -> Unit,
) {
    // Pinned: the bar stays put and only changes container color once content scrolls under it.
    val scrollBehavior = TopAppBarDefaults.pinnedScrollBehavior()
    Scaffold(
        // Without this connection the bar never learns that the list scrolled.
        modifier = Modifier.nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.settings)) },
                navigationIcon = {
                    // IconButton supplies the 48dp target and the button role; the icon's
                    // description is its only label, so it must not be null.
                    IconButton(onClick = onBack) {
                        Icon(
                            painter = painterResource(R.drawable.ic_arrow_back),
                            contentDescription = stringResource(R.string.back),
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
            )
        },
    ) { innerPadding ->
        LazyColumn(
            // innerPadding carries the bar height and the system bar insets. As contentPadding
            // the list still draws edge to edge behind the navigation bar while its first and
            // last rows rest clear of the bars. consumeWindowInsets stops children from
            // applying the same insets again.
            modifier = Modifier.fillMaxSize().consumeWindowInsets(innerPadding),
            contentPadding = innerPadding,
        ) {
            item { SectionHeader(stringResource(R.string.section_notifications)) }
            item {
                SwitchRow(
                    title = stringResource(R.string.push_title),
                    summary = stringResource(R.string.push_summary),
                    checked = state.pushEnabled,
                    onCheckedChange = { onStateChange(state.copy(pushEnabled = it)) },
                )
            }
            item { HorizontalDivider() } // dividers separate groups, not every row
            item { SectionHeader(stringResource(R.string.section_data)) }
            item {
                SwitchRow(
                    title = stringResource(R.string.wifi_only_title),
                    summary = stringResource(R.string.wifi_only_summary),
                    checked = state.wifiOnly,
                    onCheckedChange = { onStateChange(state.copy(wifiOnly = it)) },
                )
            }
            item {
                // Clickable overload: one merged, focusable row with the button role.
                ListItem(
                    onClick = onOpenStorage,
                    supportingContent = { Text(stringResource(R.string.storage_summary)) },
                ) { Text(stringResource(R.string.storage_title)) }
            }
        }
    }
}

@Composable
private fun SectionHeader(title: String) {
    Text(
        text = title,
        style = MaterialTheme.typography.titleSmall,
        color = MaterialTheme.colorScheme.primary,
        // heading(): screen reader users can jump between sections.
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp).semantics { heading() },
    )
}

@Composable
private fun SwitchRow(title: String, summary: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    ListItem(
        // The whole row is the control: toggleable merges title, summary and switch into one
        // node announced as "title, summary, switch, on/off", with a row-sized touch target.
        modifier = Modifier.toggleable(value = checked, role = Role.Switch, onValueChange = onCheckedChange),
        supportingContent = { Text(summary) },
        // onCheckedChange = null: the switch only displays state, so there is one target, not two.
        trailingContent = { Switch(checked = checked, onCheckedChange = null) },
    ) { Text(title) }
}
