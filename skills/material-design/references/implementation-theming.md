# Theming in Compose: color, type, shape, motion, icons

Scope: how to set up and read the Material 3 theme in Jetpack Compose: `MaterialTheme` and `MaterialExpressiveTheme`, color roles, dynamic color with a fallback, dark theme, contrast, typography in sp, shapes, motion, content color, icons, and tokens instead of hard-coded values.
Verified: 2026-11-23 against the sources linked in each section (Compose Material 3 1.5, BOM 2026.11.01).

## Contents

- Theme entry point
- Color roles in code
- Dynamic color with a fallback
- Dark theme
- Contrast
- Typography and sp
- Shapes
- Motion
- Content color and emphasis
- Elevation and surfaces
- Icons
- Tokens, not hard-coded values
- Common mistakes

## Theme entry point

| API | Parameters | Status |
|---|---|---|
| `MaterialTheme` | `colorScheme`, `shapes`, `typography`, `content` (all but `content` optional) | stable |
| `MaterialTheme` | `colorScheme`, `motionScheme`, `shapes`, `typography`, `content` | stable, material3 1.5+ |
| `MaterialExpressiveTheme` | `colorScheme: ColorScheme?`, `motionScheme: MotionScheme?`, `shapes: Shapes?`, `typography: Typography?`, `content` | stable, material3 1.5+; absent in 1.4 |
| `MaterialTheme.colorScheme`, `.typography`, `.shapes` | read-only composable properties | stable |
| `MaterialTheme.motionScheme` | read-only composable property | stable, material3 1.5+ |

- [Conv] Declare one app theme composable (`AppTheme { }`) and wrap the whole UI in it once, in `setContent`. Previews and tests wrap in the same function. A complete version is `examples/AppTheme.kt`.
- [API] `MaterialExpressiveTheme` applies the Material 3 Expressive defaults (expressive motion scheme and the expressive defaults for any parameter left `null`). Use it instead of `MaterialTheme`, not nested inside it. (Material 3 Expressive)
- [API] Parameters left out keep the Material baseline values, so a theme can start with only a color scheme.
- [Conv] A nested `MaterialTheme` is for a deliberately different subtree (for example an always-dark media player); do not nest themes to change one color.
- [MD] Do not mix a Material 2 `MaterialTheme` (`androidx.compose.material`) with Material 3 components: they read different theme objects.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary

## Color roles in code

- [API] `lightColorScheme(...)` and `darkColorScheme(...)` build a `ColorScheme`; every role is an optional named parameter. Roles: `primary`, `onPrimary`, `primaryContainer`, `onPrimaryContainer`, `inversePrimary`, the same four for `secondary` and `tertiary`, `background`, `onBackground`, `surface`, `onSurface`, `surfaceVariant`, `onSurfaceVariant`, `surfaceTint`, `inverseSurface`, `inverseOnSurface`, `error`, `onError`, `errorContainer`, `onErrorContainer`, `outline`, `outlineVariant`, `scrim`, `surfaceBright`, `surfaceDim`, `surfaceContainerLowest`, `surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`, `surfaceContainerHighest`, and the fixed roles (`primaryFixed`, `primaryFixedDim`, `onPrimaryFixed`, `onPrimaryFixedVariant`, same for secondary and tertiary).
- [MD] Read colors by role: `MaterialTheme.colorScheme.primary`. Never write a literal color in a composable.
- [MD] Pair every container role with its own "on" role: `primaryContainer` with `onPrimaryContainer`, `surface` with `onSurface`, `error` with `onError`. Pairs are designed to meet contrast; crossed pairs (for example `tertiaryContainer` with `primaryContainer` content) are not.
- [MD] Use `onSurfaceVariant` for lower-emphasis text and icons on surfaces, `outline` for important boundaries such as text field outlines, `outlineVariant` for decorative dividers.
- [API] `contentColorFor(backgroundColor)` returns the matching "on" color when the argument is a color of the current scheme; it cannot derive one for an arbitrary color.
- [Conv] A color the scheme lacks (for example "success") belongs in an extension of the theme (a `CompositionLocal` with light and dark values), not as a literal at the call site. [MD] Harmonize such custom colors with the primary color when dynamic color is on.
- [API] `expressiveLightColorScheme()` exists in 1.5; there is no dark counterpart. (Material 3 Expressive)

```kotlin
// material3 1.2+; no opt-in. Not compiled.
Surface(
    color = MaterialTheme.colorScheme.primaryContainer,   // container role
    contentColor = MaterialTheme.colorScheme.onPrimaryContainer, // its own "on" role
    shape = MaterialTheme.shapes.medium,
) {
    // Text and Icon inside pick up contentColor through LocalContentColor.
    Text(text = title, style = MaterialTheme.typography.titleMedium)
}
```

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/styles/color/roles

## Dynamic color with a fallback

- [API] `dynamicLightColorScheme(context)` and `dynamicDarkColorScheme(context)` are annotated `@RequiresApi(Build.VERSION_CODES.S)`: Android 12 (API 31) and later only.
- [MD] When dynamic color is unavailable, fall back to a custom light or dark `ColorScheme`. The fallback is the brand scheme, not the library baseline purple.
- [Conv] Expose a `dynamicColor: Boolean` parameter on the app theme so a product can turn it off; keep it on by default unless the brand requires fixed colors.
- [MD] With dynamic color the hues are the user's; never rely on a specific hue for meaning. Keep semantic colors (error, custom status colors) in dedicated roles.

```kotlin
// material3 1.2+; no opt-in. Not compiled.
val colorScheme = when {
    dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
        val context = LocalContext.current
        if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
    }
    darkTheme -> DarkColors      // darkColorScheme(...)
    else -> LightColors          // lightColorScheme(...)
}
```

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/styles/color/dynamic/choosing-a-source

## Dark theme

- [API] `isSystemInDarkTheme()` (`androidx.compose.foundation`) reports the system setting; use it as the default of the theme's `darkTheme` parameter.
- [MD] Provide a real dark `ColorScheme` (`darkColorScheme(...)`), chosen in the theme. Do not branch on dark mode inside composables.
- [Conv] If the app offers its own light/dark/system setting, feed the result into the theme parameter; "system" is the default.
- [Conv] Images and illustrations need dark variants or a neutral treatment; a `night` resource qualifier covers drawables the theme cannot recolor.
- [API] With `enableEdgeToEdge()` the system bar icon colors follow the system light or dark mode automatically; pass `SystemBarStyle` only when the app's theme differs from the system's.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://developer.android.com/develop/ui/compose/system/setup-e2e

## Contrast

- [API] The scheme builders (`lightColorScheme`, `dynamicLightColorScheme`, ...) take no contrast parameter in 1.5 or 1.6 alpha. A higher-contrast theme is another `ColorScheme` that the theme selects.
- [MD] Role pairs are built for accessible contrast; keeping to the pairs is the main contrast measure in code.
- [Conv] Material Theme Builder exports standard, medium-contrast and high-contrast schemes; ship them as separate `ColorScheme` values when the product supports a contrast setting.
- [Unverified] The user's system contrast level can be read with `UiModeManager.getContrast()` on API 34+ to pick one of those schemes; not re-checked in the reference for this file.
- [Conv] Check custom color pairs (charts, status colors, text on images) yourself: 4.5:1 for body text, 3:1 for large text and essential graphics.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/foundations/accessible-design/overview

## Typography and sp

- [API] `Typography(...)` has 15 styles: `displayLarge/Medium/Small`, `headlineLarge/Medium/Small`, `titleLarge/Medium/Small`, `bodyLarge/Medium/Small`, `labelLarge/Medium/Small`. material3 1.5 adds an overload with 15 `...Emphasized` counterparts and one that takes a `fontFamily` first. (Material 3 Expressive for the emphasized styles)
- [MD] Style text with a theme style: `Text(text, style = MaterialTheme.typography.bodyLarge)`. Change weight or color with `.copy(...)` on the style or with the `Text` parameters, not with a new ad-hoc size.
- [API] Font sizes and line heights are `TextUnit` values in `sp` (`16.sp`), which scale with the user's font size setting. `dp` does not scale; never convert a text size to dp to "protect" a layout.
- [API] Compose applies the platform's non-linear font scaling: at large settings small text grows proportionally more than large text. Android 14 and later scale up to 200%.
- [Conv] Let containers grow with text: `heightIn(min = 48.dp)` instead of `height(48.dp)`, `widthIn` instead of `width`, no fixed-height rows around text, and allow wrapping before truncating.
- [API] `Text` has `maxLines`, `overflow`, and (material3 1.4+) `autoSize: TextAutoSize?`. [Conv] Auto-size is for single-line display text in a fixed slot, not a substitute for layouts that reflow.
- [Conv] Custom fonts: build one `FontFamily` and pass it to each `TextStyle` (or to the 1.5 `Typography(fontFamily, ...)` overload); keep the Material sizes and line heights unless the design system defines its own scale.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/styles/typography/applying-type , https://developer.android.com/jetpack/androidx/releases/compose-ui

## Shapes

- [API] `Shapes(extraSmall, small, medium, large, extraLarge)`, each a `CornerBasedShape`. material3 1.5 adds an overload with `largeIncreased`, `extraLargeIncreased` and `extraExtraLarge`. (Material 3 Expressive)
- [MD] Read shapes from the theme: `MaterialTheme.shapes.medium`. Components already map to a shape token; override a component's `shape` parameter only for a deliberate exception.
- [API] `MaterialShapes` (the expressive polygon set used by `LoadingIndicator`) is `@ExperimentalMaterial3ExpressiveApi` in 1.5.
- [API] Shape morphing on press and selection is built into the 1.5 `shapes:` overloads (`Button(onClick, shapes = ...)`, `IconButton`, `ToggleButton`); it is not something to animate by hand.
- [Conv] Clip with the same shape the container draws: `Modifier.clip(MaterialTheme.shapes.medium)`.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/styles/shape/overview-principles

## Motion

- [API] `MotionScheme` (stable in 1.5, absent in 1.4) provides six specs: `defaultSpatialSpec()`, `fastSpatialSpec()`, `slowSpatialSpec()` for position, size and shape; `defaultEffectsSpec()`, `fastEffectsSpec()`, `slowEffectsSpec()` for color and opacity. Factories: `MotionScheme.standard()` and `MotionScheme.expressive()`.
- [MD] Spatial specs may overshoot (spring bounce); effects specs do not. Use a spatial spec for things that move or resize and an effects spec for fades and color changes. (Material 3 Expressive)
- [API] `MaterialExpressiveTheme` defaults to the expressive scheme; `MaterialTheme` defaults to the standard one unless `motionScheme` is passed.
- [Conv] On material3 1.4 there is no motion scheme: use the default specs of `animate*AsState` and `AnimatedVisibility`, and do not copy spring constants from 1.5 sources.
- [Conv] Do not add animation that conveys nothing, and never make logic depend on an animation finishing: users can shorten or remove animations in system settings.

```kotlin
// material3 1.5+; no opt-in. Not compiled.
val scale by animateFloatAsState(
    targetValue = if (selected) 1.1f else 1f,
    animationSpec = MaterialTheme.motionScheme.fastSpatialSpec(), // size change: spatial
    label = "selectedScale",
)
```

Source: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary , https://m3.material.io/styles/motion/overview/how-it-works

## Content color and emphasis

- [API] `LocalContentColor` carries the preferred color for text and icons; `Surface`, buttons, app bars, cards and list items set it from their `contentColor`. `Text` and `Icon` read it by default.
- [Conv] Put content on a `Surface` (or a Material container) instead of a `Box` with `Modifier.background(...)`: `background` paints a color but does not set the content color, so text keeps the outer color and can lose contrast.
- [API] `LocalTextStyle` and `ProvideTextStyle(value) { }` do the same for the text style; components such as `Button` and `TopAppBar` set it for their slots, so slot content usually needs no explicit style.
- [API] Material 3 has no `ContentAlpha` or `LocalContentAlpha`. [MD] Express emphasis with roles (`onSurface` for primary content, `onSurfaceVariant` for secondary) and font weight.
- [Conv] Disabled appearance comes from the component (`enabled = false`); do not fake it with `Modifier.alpha`.

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://developer.android.com/develop/ui/compose/designsystems/material2-material3

## Elevation and surfaces

- [MD] Distinguish surfaces with the tonal surface roles (`surfaceContainerLowest` to `surfaceContainerHighest`, `surfaceBright`, `surfaceDim`) rather than with shadows; reserve shadow elevation for elements that float above content (FAB, menus, dialogs).
- [API] `Surface(tonalElevation = ...)` and `ColorScheme.surfaceColorAtElevation(elevation)` still exist (the earlier tint-overlay approach); `LocalTonalElevationEnabled` can turn the overlay off. Prefer the container roles in new code.
- [Conv] Do not set `shadowElevation` on cards and bars to "make them pop"; pick the component variant (`ElevatedCard`, `Card`, `OutlinedCard`).

Source: https://developer.android.com/develop/ui/compose/designsystems/material3 , https://m3.material.io/styles/elevation/overview

## Icons

- [API] material3 no longer depends on `material-icons-core` (since 1.4.0): `Icons.Filled.*` does not resolve unless the project adds the icons artifact itself. The icons library is frozen and described as no longer maintained or recommended.
- [MD] Use Material Symbols: download the vector drawable (Android XML) from Google Fonts into `res/drawable` and load it with `painterResource(R.drawable.ic_name)`.
- [API] `Icon(painter, contentDescription, modifier, tint)`: `contentDescription` has no default. Pass a localized string for a meaningful or interactive icon, `null` for a decorative one or one whose label is visible next to it.
- [API] `Icon` tints with `LocalContentColor` by default; use `Image` (or `tint = Color.Unspecified`) for multi-color artwork.
- [Conv] Directional icons (back arrow, send, list bullets) must mirror in right-to-left layouts: set `android:autoMirrored="true"` in the vector XML. Do not mirror clocks, checkmarks or media playback icons.
- [MD] Use the outlined and filled versions of the same symbol for unselected and selected states (navigation items, toggles), so state is not signalled by color alone.
- [Conv] Standard icon size is 24dp inside a 48dp target; `IconButton` provides the target.

Source: https://developer.android.com/develop/ui/compose/graphics/images/material , https://m3.material.io/styles/icons/overview , https://developer.android.com/jetpack/androidx/releases/compose-material3

## Tokens, not hard-coded values

- [MD] Colors, type, shape and motion come from `MaterialTheme`; that is what makes dark theme, dynamic color, contrast variants and rebranding work without touching screens.
- [Conv] Component defaults already use the right tokens. Pass `colors = ButtonDefaults.buttonColors(...)` or a `shape` only to express a documented variant; a screen full of overrides is a custom design system in disguise.
- [Conv] Spacing has no theme object in Compose Material 3: keep a small set of `Dp` constants (4, 8, 12, 16, 24) in one place rather than scattering literals.
- [Conv] Literal `Color(0xFF...)` values are acceptable in exactly one place: the file that defines the color schemes.
- [API] `XxxDefaults` objects (`TopAppBarDefaults`, `CardDefaults`, `ListItemDefaults`, ...) expose each component's default colors, shapes, elevations and paddings; read them instead of copying numbers from the spec.

Source: https://m3.material.io/foundations/design-tokens/overview , https://developer.android.com/develop/ui/compose/designsystems/material3

## Common mistakes

- `Color(0xFF6200EE)` or `Color.White` inside a composable -> `MaterialTheme.colorScheme` role, paired with its "on" role.
- `if (isSystemInDarkTheme()) Color.Black else Color.White` at call sites -> choose the `ColorScheme` once in the theme.
- `dynamicLightColorScheme(context)` with no API 31 check, or with no static fallback -> gate on `Build.VERSION_CODES.S` and provide brand schemes.
- `fontSize = 14.sp` on every `Text`, or sizes in dp -> `style = MaterialTheme.typography.bodyMedium`.
- `Modifier.height(56.dp)` around text -> `heightIn(min = 56.dp)` so 200% font scale fits.
- `Box(Modifier.background(MaterialTheme.colorScheme.primary)) { Text(...) }` -> `Surface(color = ..., contentColor = ...)` or set the text color to `onPrimary`.
- `ContentAlpha.medium` or `Modifier.alpha(0.6f)` for secondary text -> `onSurfaceVariant`.
- `Icons.Default.Add` from `material-icons-extended` -> Material Symbols vector drawable and `painterResource`.
- `MaterialExpressiveTheme` or `MaterialTheme.motionScheme` on material3 1.4 -> they need 1.5; see `references/implementation-availability.md`.
- Shadows used to separate every card -> surface container roles and component variants.
