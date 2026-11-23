package com.example.shop.cart

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.shop.R

@Composable
fun QuantityStepper(quantity: Int, onChange: (Int) -> Unit, modifier: Modifier = Modifier) {
    val labelSize = with(LocalDensity.current) { 14.dp.toSp() }
    Row(modifier.background(Color.White), verticalAlignment = Alignment.CenterVertically) {
        Box(Modifier.size(32.dp).clickable { onChange(quantity - 1) }, contentAlignment = Alignment.Center) {
            Icon(painterResource(R.drawable.ic_remove), contentDescription = null)
        }
        Text(quantity.toString(), fontSize = labelSize, color = Color(0xFFBDBDBD))
        Box(Modifier.size(32.dp).clickable { onChange(quantity + 1) }, contentAlignment = Alignment.Center) {
            Icon(painterResource(R.drawable.ic_add), contentDescription = null)
        }
    }
}
