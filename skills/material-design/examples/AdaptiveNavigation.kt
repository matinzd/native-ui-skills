// AdaptiveNavigation.kt
//
// Purpose: an app shell with three top-level destinations whose navigation component follows the
// window size: a navigation bar in compact windows, a navigation rail in larger ones.
//
// Library versions: Compose BOM 2026.11.01; androidx.compose.material3:material3 1.5.x and
//   androidx.compose.material3:material3-adaptive-navigation-suite 1.5.x (no opt-in: nothing
//   used here is experimental); androidx.compose.material3.adaptive:adaptive 1.3.0+ for
//   currentWindowAdaptiveInfoV2(). On adaptive 1.2.x delete the layoutType argument: the
//   default does the same calculation.
// Opt-ins: none.
// Resources assumed: R.string.nav_home / nav_search / nav_profile and outlined plus filled
//   Material Symbols vector drawables (R.drawable.ic_home, ic_home_filled, ...).
//
// Pages applied:
//   https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation
//   https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes
//   https://m3.material.io/components/navigation-bar/guidelines
//   https://m3.material.io/components/navigation-rail/guidelines
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import androidx.annotation.DrawableRes
import androidx.annotation.StringRes
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.adaptive.currentWindowAdaptiveInfoV2
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffold
import androidx.compose.material3.adaptive.navigationsuite.NavigationSuiteScaffoldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource

// Three to five top-level destinations of equal importance: the range a navigation bar is
// meant for. Each has a short text label and an icon pair (outlined, filled when selected).
enum class TopLevelDestination(
    @StringRes val label: Int,
    @DrawableRes val icon: Int,
    @DrawableRes val selectedIcon: Int,
) {
    Home(R.string.nav_home, R.drawable.ic_home, R.drawable.ic_home_filled),
    Search(R.string.nav_search, R.drawable.ic_search, R.drawable.ic_search_filled),
    Profile(R.string.nav_profile, R.drawable.ic_person, R.drawable.ic_person_filled),
}

@Composable
fun AppShell() {
    // rememberSaveable: the selected destination survives rotation, resizing and process death.
    var current by rememberSaveable { mutableStateOf(TopLevelDestination.Home) }

    // Window size class and posture of the app's window (not the device). The default rule:
    // navigation bar when the width or height is compact or the device is in tabletop posture,
    // navigation rail otherwise. Never branch on "is this a tablet".
    val layoutType = NavigationSuiteScaffoldDefaults.calculateFromAdaptiveInfo(
        currentWindowAdaptiveInfoV2(),
    )

    NavigationSuiteScaffold(
        layoutType = layoutType,
        navigationSuiteItems = {
            TopLevelDestination.entries.forEach { destination ->
                val selected = destination == current
                item(
                    selected = selected,
                    onClick = { current = destination },
                    icon = {
                        Icon(
                            // Selection is shown by the indicator and a filled icon, not by
                            // color alone.
                            painter = painterResource(
                                if (selected) destination.selectedIcon else destination.icon,
                            ),
                            // null: the visible label already names the item, so a description
                            // would make TalkBack read it twice.
                            contentDescription = null,
                        )
                    },
                    // Always label destinations; icon-only navigation is hard to learn.
                    label = { Text(stringResource(destination.label)) },
                )
            }
        },
    ) {
        // The scaffold places this content beside the rail or above the bar and handles the
        // window insets of the navigation component itself.
        DestinationScreen(current)
    }
}

@Composable
private fun DestinationScreen(destination: TopLevelDestination, modifier: Modifier = Modifier) {
    // Placeholder content. A real destination hosts its own Scaffold and back stack.
    Box(modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(
            text = stringResource(destination.label),
            style = MaterialTheme.typography.headlineMedium,
        )
    }
}
