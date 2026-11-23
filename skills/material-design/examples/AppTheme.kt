// AppTheme.kt
//
// Purpose: the app's single theme entry point: dynamic color on Android 12+ with a static
// brand fallback, light and dark schemes, and a type scale defined in sp.
//
// Library versions: Compose BOM 2026.11.01; material3 1.5.x. Everything here also compiles on
//   material3 1.2+ (dynamic*ColorScheme, lightColorScheme, Typography are long stable).
//   For the Material 3 Expressive defaults (material3 1.5+ only) replace the MaterialTheme
//   call with MaterialExpressiveTheme(colorScheme = ..., typography = ..., content = content).
// Opt-ins: none.
//
// Pages applied:
//   https://developer.android.com/develop/ui/compose/designsystems/material3
//   https://m3.material.io/styles/color/roles
//   https://m3.material.io/styles/color/dynamic/choosing-a-source
//   https://m3.material.io/styles/typography/applying-type
//
// Checked against the androidx API signature files on 2026-11-23; not compiled.

package com.example.app

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

// Static fallback schemes. Literal colors live only here; composables read roles from
// MaterialTheme.colorScheme. The values are illustrative: generate a complete, contrast-checked
// set (all roles, both modes) with Material Theme Builder instead of picking them by hand.
// Roles you do not set keep the library's baseline values.
private val LightColors = lightColorScheme(
    primary = Color(0xFF005FAF),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFD4E3FF),
    onPrimaryContainer = Color(0xFF001C3A),
)

// Dark is its own scheme (lighter primary, dark surfaces), not an inverted light scheme.
private val DarkColors = darkColorScheme(
    primary = Color(0xFFA5C8FF),
    onPrimary = Color(0xFF00315F),
    primaryContainer = Color(0xFF004787),
    onPrimaryContainer = Color(0xFFD4E3FF),
)

// Text sizes and line heights are in sp so they follow the user's font size setting.
// Override only the styles the brand changes; the other styles keep the Material defaults.
private val AppTypography = Typography(
    titleLarge = TextStyle(
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp,
    ),
    bodyLarge = TextStyle(
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp,
    ),
)

@Composable
fun AppTheme(
    // Follow the system setting by default; do not add an in-app "dark mode" flag that ignores it.
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Lets a brand-critical app (or a user preference) turn wallpaper-based color off.
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit,
) {
    val colorScheme = when {
        // dynamicLightColorScheme / dynamicDarkColorScheme are @RequiresApi(31): the version
        // check is mandatory, and the static branches are the real fallback on Android 11
        // and lower.
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColors
        else -> LightColors
    }

    // One MaterialTheme at the root. Shapes are left at the Material defaults.
    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        content = content,
    )
}
