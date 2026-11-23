# Platform detection and the form-factor matrix

Scope: how to work out which Android form factor(s), SDK levels, UI toolkit (Compose or Views), Material generation (Material 2, Material 3, Material 3 Expressive) and library versions a request or codebase targets before giving design or API advice; the default when nothing is known; the current version facts; and a matrix of what is universal and what differs by form factor.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Order of evidence
- SDK levels
- Compose or Views
- Material generation and library versions
- Form factor signals
- Behaviour switches tied to targetSdk
- When the target is ambiguous, and the default
- Current version facts
- Universal versus form-factor matrix
- Common mistakes

## Order of evidence

Work down the list; later evidence refines earlier evidence, and an explicit user statement always wins.

1. [Conv] Explicit statement in the prompt ("Wear OS tile", "targetSdk 35", "we are still on Views"). Take it literally, including versions.
2. [API] Module build files: `build.gradle(.kts)` of each module, `gradle/libs.versions.toml`, convention plugins under `build-logic/` or `buildSrc/`, and `gradle.properties`.
3. [API] `AndroidManifest.xml` of each module: `uses-feature`, launcher categories, `meta-data`, activity attributes.
4. [API] Dependencies and imports in the file being edited (`androidx.compose.material3.*`, `androidx.wear.compose.material3.*`, `androidx.tv.material3.*`, `androidx.car.app.*`, `androidx.xr.compose.*`).
5. [API] Theme parents in `res/values*/themes.xml` or `styles.xml` (Views) and the theme composable in Compose.
6. [Conv] Module layout: Android projects usually keep one module per form factor (`app`, `wear`, `tv`, `automotive`). Decide per module, and report per module when they disagree.

- [API] Form factor is not layout. Window size classes come from the window the app currently has, change at runtime, and are explicitly not meant for "is this a tablet" logic. Detection tells you which conventions, inputs and libraries apply; it does not pick the layout. See `references/platforms-large-screens.md`.

Source: https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes

## SDK levels

- [API] `minSdk` is the oldest API level the app installs on; `targetSdk` is the level whose behaviour changes the app has opted into; `compileSdk` is the SDK the code is built against. Android 15 = API 35, Android 16 = API 36 (`BAKLAVA`), Android 17 = API 37 (`CINNAMON_BUN`).
- [API] `targetSdk`, not the device OS alone, switches edge-to-edge enforcement, predictive back and the large-screen orientation rules: see the table further down.
- [Conv] If `targetSdk` is absent from the module, look in convention plugins and the version catalog before assuming a value; legacy projects may still set `android:targetSdkVersion` in the manifest.

```bash
grep -rnE '(compileSdk|minSdk|targetSdk)(Version|Preview)?[ =(]' --include='*.gradle' --include='*.gradle.kts' --include='*.toml' --include='gradle.properties' .
grep -rnE 'android:(min|target)SdkVersion' --include='AndroidManifest.xml' .
```

Source: https://developer.android.com/guide/topics/manifest/uses-sdk-element

## Compose or Views

| Signal | Conclusion | Tag |
|---|---|---|
| Plugin `org.jetbrains.kotlin.plugin.compose`, or `buildFeatures { compose = true }`; `@Composable` functions; `setContent { }` | Compose UI | [Conv] |
| `res/layout*/*.xml`, `viewBinding` / `dataBinding`, `Fragment` subclasses inflating layouts | Views UI | [Conv] |
| `ComposeView` in XML or code, `AndroidView(` in composables | Interop: both toolkits; answer in the toolkit of the file being edited | [Conv] |
| Kotlin Multiplatform project | Android configuration lives under `androidMain` | [Conv] |

```bash
grep -rnE 'kotlin\.plugin\.compose|compose *= *true|viewBinding|dataBinding' --include='*.gradle*' --include='*.toml' .
grep -rlE '@Composable' --include='*.kt' . | wc -l
find . -path '*/res/layout*' -name '*.xml' -not -path '*/build/*' | wc -l
grep -rnE 'ComposeView|AndroidView\(|setContent *\{' --include='*.kt' . | head
```

- [MD] Core app quality asks for Material Design components in place of platform components where possible, in either toolkit.

Source: https://developer.android.com/docs/quality-guidelines/core-app-quality

## Material generation and library versions

| Signal | Conclusion | Tag |
|---|---|---|
| `androidx.compose.material3:material3` | Compose Material 3. With no explicit version, the Compose BOM decides it: read the BOM version and look it up on the BOM mapping page | [API] |
| material3 at 1.5.0 or later; `MaterialExpressiveTheme`, `MotionScheme.expressive()`, `ButtonGroup`, `SplitButtonLayout`, `HorizontalFloatingToolbar` in code | Material 3 Expressive available as stable API | [API] |
| material3 1.4.x | Only a small part of Expressive: `ShortNavigationBar`, `WideNavigationRail` and `ModalWideNavigationRail` are stable there. Everything else (expressive theme, motion scheme, button groups, FAB menu, toolbars) starts at 1.5.0; the 1.4.0 notes say the experimental Expressive APIs were removed and point to the 1.5.0 alphas | [API] |
| `@OptIn(ExperimentalMaterial3ExpressiveApi::class)` | Still-experimental Expressive API in use (in 1.5.0 for example `LoadingIndicator`, `MaterialShapes`), or a 1.5.0 pre-release | [API] |
| `androidx.compose.material:material` without material3 | Compose Material 2; a migration guide exists | [API] |
| Both `material` and `material3` | Mid-migration or mixed modules; check imports of the file being edited | [Conv] |
| `com.google.android.material:material` with theme parent `Theme.Material3.*` (including `Theme.Material3.DynamicColors.*`) | Views, Material 3 | [API] |
| Theme parent `Theme.Material3Expressive.*` | Views, Material 3 Expressive themes (naming taken from the Material Components for Android docs, not from developer.android.com) | [Unverified] |
| Theme parent `Theme.MaterialComponents.*` | Views, Material 2 | [API] |
| Theme parent `Theme.AppCompat.*` | Views without Material Components theming | [API] |
| `androidx.compose.material3.adaptive:adaptive*`, `material3-adaptive-navigation-suite`, `androidx.window:window` | App already uses the adaptive libraries | [API] |
| `androidx.wear.compose:compose-material3` versus `compose-material` | Wear Material 3 (Expressive) versus Wear Material 2.5 | [API] |
| `androidx.tv:tv-material` versus `androidx.leanback:*` | Compose for TV versus the deprecated Leanback toolkit | [API] |

```bash
grep -rnE 'compose-bom|compose\.material3|compose\.material:material|com\.google\.android\.material:material|material3-adaptive|androidx\.window' --include='*.gradle*' --include='*.toml' .
grep -rnE 'parent="Theme\.(Material3Expressive|Material3|MaterialComponents|AppCompat)[A-Za-z.]*"' --include='*.xml' .
grep -rhoE 'import androidx\.compose\.(material3|material)\.[A-Za-z]+' --include='*.kt' . | sort | uniq -c | sort -rn | head -20
grep -rnE 'MaterialExpressiveTheme|MotionScheme\.expressive|ExperimentalMaterial3ExpressiveApi|ExperimentalMaterial3Api' --include='*.kt' . | head
```

- [Conv] State the version you assumed. Before using an API marked experimental, say which opt-in it needs and offer the stable alternative.

Source: https://developer.android.com/jetpack/androidx/releases/compose-material3, https://developer.android.com/develop/ui/compose/bom/bom-mapping, https://developer.android.com/develop/ui/compose/designsystems/material2-material3, https://developer.android.com/develop/ui/views/theming/dynamic-colors, https://developer.android.com/develop/ui/views/theming/darktheme

## Form factor signals

| Signal (manifest unless noted) | Conclusion | Tag |
|---|---|---|
| `<uses-feature android:name="android.hardware.type.watch"/>` | Wear OS module. `meta-data` `com.google.android.wearable.standalone` says whether it works without a phone app | [API] |
| Intent filter category `android.intent.category.LEANBACK_LAUNCHER`; `android:banner`; `android.hardware.touchscreen` with `required="false"` | TV app. `android.software.leanback` with `required="false"` means one app for mobile and TV | [API] |
| Service with intent action `androidx.car.app.CarAppService` and a category `androidx.car.app.category.*` | Templated car app (Car App Library) | [API] |
| `meta-data` `com.google.android.gms.car.application`; dependency `androidx.car.app:app-projected` | Android Auto (projected from the phone) | [API] |
| `<uses-feature android:name="android.hardware.type.automotive"/>`; dependency `androidx.car.app:app-automotive` | Android Automotive OS (built into the car) | [API] |
| `<uses-feature>` `android.software.xr.api.spatial` or `android.software.xr.api.openxr`; property `android.window.PROPERTY_XR_ACTIVITY_START_MODE` | Android XR (Jetpack XR SDK, or an OpenXR engine) | [API] |
| Dependencies `androidx.wear.tiles`, `androidx.wear.protolayout`, `androidx.glance:glance*` | Tiles (Wear) or widgets (Glance) in scope | [API] |
| None of the above | Phone app that also runs on tablets, foldables, desktop windows, ChromeOS and Android XR Home Space unless it opts out | [Conv] |

```bash
grep -rnE 'hardware\.type\.(watch|automotive)|wearable\.standalone|LEANBACK_LAUNCHER|software\.leanback|android:banner|hardware\.touchscreen|gms\.car\.application|car\.app\.(CarAppService|category)|software\.xr\.api|XR_ACTIVITY_START_MODE' --include='AndroidManifest.xml' .
grep -rnE 'wear\.compose|wear\.tiles|wear\.protolayout|androidx\.tv:|androidx\.leanback|car\.app:app|androidx\.xr\.|glance' --include='*.gradle*' --include='*.toml' .
```

Source: https://developer.android.com/training/wearables/packaging, https://developer.android.com/training/tv/get-started/create, https://developer.android.com/training/cars/apps, https://developer.android.com/training/cars/apps/automotive-os, https://developer.android.com/develop/xr/package-and-distribute

## Behaviour switches tied to targetSdk

| targetSdk | Switch to look for (on a device of that Android version or newer) |
|---|---|
| 33 | Notification runtime permission under app control |
| 35 | Edge-to-edge enforced; status-bar colour APIs have no effect; opt-out attribute still honoured |
| 36 | Edge-to-edge opt-out disabled; predictive back on by default (`onBackPressed`, `KEYCODE_BACK` not delivered); orientation and resizability restrictions ignored at smallest width 600dp and up |
| 37 | Large-screen opt-out gone |

```bash
grep -rnE 'windowOptOutEdgeToEdgeEnforcement|enableEdgeToEdge|statusBarColor|navigationBarColor|enableOnBackInvokedCallback|onBackPressed\(|KEYCODE_BACK|screenOrientation|resizeableActivity|(min|max)AspectRatio|setRequestedOrientation|PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY' --include='*.kt' --include='*.java' --include='*.xml' .
```

- [API] This is a summary. Full table with every change, device-version effects and opt-outs: `references/platforms-system.md`; orientation rules: `references/platforms-large-screens.md`.

Source: https://developer.android.com/about/versions/15/behavior-changes-15, https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/about/versions/17/behavior-changes-17

## When the target is ambiguous, and the default

- [Conv] Prompt and code disagree (prompt says "Material 3", code imports `androidx.compose.material`): say so, answer for what the code uses, and name the migration as a separate step.
- [Conv] Several modules: answer for the module that owns the file; mention the other form factors only where the change affects shared code.
- [Conv] No version visible: do not guess silently. Use the default below and state it in one line.
- [Conv] A question about a behaviour that depends on `targetSdk` (bar colours, Back handling, orientation locks) cannot be answered without the level: find it or give both branches.
- [Conv] Default when nothing is known: a phone app that must also behave in resizable windows; Jetpack Compose; Material 3 on the current stable `androidx.compose.material3:material3` line (1.5.x, where Expressive components are stable); `targetSdk` 36 behaviours (edge-to-edge, predictive back); light and dark themes; dynamic colour with a static fallback. Gate anything annotated `@ExperimentalMaterial3Api`, `@ExperimentalMaterial3ExpressiveApi` or `@ExperimentalMaterial3AdaptiveApi` behind a stated opt-in and prefer a stable equivalent when one exists.

Source: https://developer.android.com/jetpack/androidx/releases/compose-material3, https://developer.android.com/google/play/requirements/target-sdk

## Current version facts

As the documentation states them on 2026-11-23. Re-check release pages before quoting a version in code.

| Item | Value | Tag |
|---|---|---|
| Android versions | Android 16 = API 36; Android 17 = API 37. The Android 17 pages describe behaviour changes and delivery to Pixel devices, while the SDK platform release notes and the versions overview still end at Android 16 | [API] |
| `androidx.compose.material3:material3` | 1.5.0 stable (2026-11-18) in BOM `2026.11.01`; Material 3 Expressive mostly stable there. Still experimental in 1.5.0: loading indicators, `MaterialShapes`, app bar with search. All other Compose library versions: `references/implementation-availability.md` | [API] |
| Form-factor libraries | Wear Compose (`androidx.wear.compose:*`) 1.7.2 stable, 1.8.0-alpha04 (Wear OS 6 is based on Android 16); `androidx.tv:tv-material` 1.1.0, `tv-foundation` 1.0.0 (Leanback deprecated); Car App Library `androidx.car.app:app` 1.7.0 stable, 1.8.0-rc01; `androidx.xr.compose:compose` 1.0.0-rc01, no stable release yet; Glimmer (glasses) 1.0.0-alpha22; Glance (widgets) 1.2.0 stable | [API] |
| Google Play target API from 2026-08-31 | New apps and updates: 36. Wear OS and Android Automotive OS: 35. Android TV and Android XR: 34. See `references/platforms-quality.md` | [Req] |

Source: https://developer.android.com/jetpack/androidx/releases/compose-material3, https://developer.android.com/develop/ui/compose/bom/bom-mapping, https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive, https://developer.android.com/jetpack/androidx/releases/wear-compose, https://developer.android.com/jetpack/androidx/releases/tv, https://developer.android.com/jetpack/androidx/releases/car-app, https://developer.android.com/jetpack/androidx/releases/xr-compose, https://developer.android.com/google/play/requirements/target-sdk, https://developer.android.com/about/versions/17

## Universal versus form-factor matrix

Universal on every form factor: dp for layout and sp for text, state preserved across configuration changes, contrast and labels for assistive technology, Material components first, and a target API level that meets Google Play's floor.

| Concern | Phone | Tablet, foldable | Desktop window, ChromeOS | Wear OS | TV | Car (driving) | XR |
|---|---|---|---|---|---|---|---|
| Primary navigation | Navigation bar (3 to 5) or modal expanded rail | Navigation rail | Rail that expands; content may enter the window header | Shallow and linear, inline entries | Top tabs or left navigation drawer | Tab template; screen stack of at most 5 | Rail or bar, optionally in an orbiter |
| Back | System gesture or 3-button Back; Up equals Back in the task | Same | Same, plus Esc | Swipe to dismiss | Remote Back; no on-screen back | Host back button pops the screen | System gesture menu "Go back" |
| Text input | Software keyboard, IME insets | Plus hardware keyboard, stylus handwriting | Hardware keyboard first | Voice, emoji, canned replies, small keyboard; no password entry | On-screen Gboard with voice | Search template, voice | Voice, Bluetooth keyboard |
| Target size | 48dp touch | 48dp touch | 48dp touch; pointer targets may be smaller | 48dp, stated as required | Focus based | Host rendered | 56dp recommended |
| Theme | Light and dark | Light and dark | Light and dark | Dark only, black background | Dark first | Host decides; light and dark variants | Light and dark |
| Dynamic colour | Android 12+ with static fallback | Same | Same | Seed based, opt-in | Content based, not from the user | Not applicable | Not stated |
| Windowing | Split screen, picture-in-picture | Multi-window is standard | Free-form windows, multi-instance | None | Picture-in-picture only | None | Home Space side by side; Full Space single app |
| Orientation | Both recommended; locks still honoured below sw600dp | Locks ignored at targetSdk 36 | Any window shape | Fixed, round or square | Landscape only | Host | Not applicable |
| Reference | `references/platforms-system.md` | `references/platforms-large-screens.md` | `references/platforms-large-screens.md` | `references/platforms-wear.md` | `references/platforms-tv.md` | `references/platforms-auto-xr.md` | `references/platforms-auto-xr.md` |

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns, https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/design/ui/tv/guides/foundations/navigation-on-tv, https://developer.android.com/design/ui/cars/guides/templates/overview, https://developer.android.com/design/ui/xr/guides/foundations

## Common mistakes

| Mistake | Fix |
|---|---|
| Reading `compileSdk` as the behaviour level | Behaviour changes follow `targetSdk`; report both |
| Assuming the material3 version from the import alone | Resolve it from the explicit version or the Compose BOM mapping |
| Treating Expressive as "all experimental" or "all stable" | On 1.5.x most is stable, a few APIs still need `ExperimentalMaterial3ExpressiveApi`; on 1.4.x only `ShortNavigationBar` and the wide navigation rail exist |
| Calling a `LEANBACK_LAUNCHER` app a "Leanback library" app | The launcher category marks a TV app; the toolkit is decided by `androidx.tv:tv-material` versus `androidx.leanback` |
| Giving phone Material 3 advice to a module that declares `android.hardware.type.watch` | Wear has its own Material 3 library and rules: `references/platforms-wear.md` |
| Deciding tablet versus phone from device model or `smallestScreenWidthDp` and fixing the layout to it | Use window size classes at runtime |
| Looking only at the `app` module | Check every module and the convention plugins |
