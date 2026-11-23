package com.example.weather.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

@Composable
fun ForecastCard(day: DayForecast, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFFFFF)),
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(
                painter = painterResource(day.iconRes),
                contentDescription = day.conditionLabel,
                tint = Color(0xFF5F6368),
            )
            Spacer(Modifier.width(16.dp))
            Column(Modifier.weight(1f)) {
                Text(day.weekday, color = Color(0xFF202124), style = MaterialTheme.typography.titleMedium)
                Text(day.conditionLabel, color = Color(0xFF5F6368), style = MaterialTheme.typography.bodyMedium)
            }
            Text("${day.highCelsius}°", color = Color(0xFF202124), fontSize = 28.sp)
        }
    }
}
