package com.example.mail.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.material.FloatingActionButton
import androidx.compose.material.Text
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.mail.R

@Composable
fun InboxScreen(threads: List<MailThread>, onSearch: () -> Unit, onCompose: () -> Unit, onArchive: (MailThread) -> Unit) {
    var showArchived by remember { mutableStateOf(false) }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Inbox") },
                actions = { IconButton(onClick = onSearch) { Icon(painterResource(R.drawable.ic_search), contentDescription = null) } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = Color(0xFF1A73E8), titleContentColor = Color.White),
            )
        },
        floatingActionButton = { FloatingActionButton(onClick = onCompose) { Icon(painterResource(R.drawable.ic_edit), "Compose") } },
    ) { _ ->
        LazyColumn(Modifier.fillMaxSize()) {
            items(threads) { thread ->
                Row(Modifier.fillMaxWidth().padding(16.dp)) {
                    Text(thread.subject, Modifier.weight(1f))
                    TextButton(onClick = { onArchive(thread); showArchived = true }) { Text("Archive") }
                }
                Divider()
            }
        }
    }
    if (showArchived) {
        AlertDialog(
            onDismissRequest = { showArchived = false },
            confirmButton = { TextButton(onClick = { showArchived = false }) { Text("OK") } },
            text = { Text("Conversation archived.") },
        )
    }
}
