package com.example.trails

import android.app.Activity
import android.content.pm.ActivityInfo
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp

private val destinations = listOf("Explore", "Saved", "Record", "Stats", "Groups", "Profile")

@Composable
fun TrailShell(trails: List<Trail>, iconFor: (String) -> Int) {
    val activity = LocalContext.current as? Activity
    LaunchedEffect(Unit) { activity?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_PORTRAIT }
    var selected by rememberSaveable { mutableIntStateOf(0) }
    Scaffold(
        bottomBar = {
            NavigationBar {
                destinations.forEachIndexed { index, name ->
                    NavigationBarItem(
                        selected = selected == index,
                        onClick = { selected = index },
                        icon = { Icon(painterResource(iconFor(name)), contentDescription = null) },
                        label = { Text(name) },
                    )
                }
            }
        },
    ) { innerPadding ->
        LazyColumn(Modifier.padding(innerPadding).width(360.dp)) {
            items(trails) { trail -> TrailRow(trail) }
        }
    }
}
