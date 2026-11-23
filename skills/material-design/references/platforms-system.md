# Phone and system conventions

Scope: the system-level conventions every Android app meets on a phone (and inherits on other form factors): edge-to-edge and insets, system bars, cutouts, gesture and 3-button navigation, Back, predictive back and Up, splash screen, app icons, notifications, permissions, sharing, photo picker, widgets, settings, haptics, themes, dynamic colour and text scaling, with what each `targetSdk` level changes.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- What each targetSdk level changes
- Edge-to-edge and window insets
- System bars
- Display cutouts
- Gesture and 3-button navigation
- Back, Up and predictive back
- App structure on a phone
- Splash screen and app icon
- Notifications
- Permissions
- Sharing and the photo picker
- Widgets
- Settings
- Haptics
- Dark theme, dynamic colour and text scaling
- Common mistakes

## What each targetSdk level changes

| Level | Change relevant to UI | Tag |
|---|---|---|
| targetSdk 33 (Android 13) | Notifications need the `POST_NOTIFICATIONS` runtime permission; the app decides when to ask. (Android 13 devices, any target: themed icons use the `monochrome` layer) | [API] |
| Android 14 device | Font scale up to 200% with a non-linear curve (all apps) | [API] |
| targetSdk 35 (Android 15) | Edge-to-edge enforced; status bar and gesture navigation bar transparent; `setStatusBarColor` and `R.attr#statusBarColor` have no effect; non-floating windows always lay out into the cutout; `Configuration` screen size no longer excludes system bars; opt-out `R.attr#windowOptOutEdgeToEdgeEnforcement` available | [API] |
| Android 15 device | Predictive back system animations no longer sit behind a developer option; they show for apps that opted in | [API] |
| targetSdk 36 (Android 16) | Edge-to-edge opt-out disabled on Android 16 devices (still works on an Android 15 device); predictive back system animations on by default, `onBackPressed` not called, `KEYCODE_BACK` not dispatched; large-screen orientation and resizability restrictions ignored; `elegantTextHeight` ignored | [API] |
| Android 16 device | Predictive back in 3-button navigation (long-press Back); `announceForAccessibility` deprecated; from Android 16 QPR2 icons without a monochrome layer are themed automatically | [API] |
| targetSdk 37 (Android 17) | No opt-out from the large-screen rules; oversized widget bitmap updates throw; password characters hidden when a physical keyboard is used | [API] |
| Android 17 device | IME visibility is not restored after an unhandled configuration change such as rotation | [API] |

- [API] These are platform behaviours selected by `targetSdk`, not Google Play policies. They become unavoidable in practice because Google Play sets a minimum target API level: see `references/platforms-quality.md`.

Source: https://developer.android.com/about/versions/15/behavior-changes-15, https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/about/versions/16/behavior-changes-all, https://developer.android.com/about/versions/17/behavior-changes-17, https://developer.android.com/about/versions/17/behavior-changes-all

## Edge-to-edge and window insets

- [API] An edge-to-edge app draws behind the status bar, caption bar and navigation bar. Enforcement applies on Android 15+ devices once the app targets API 35; the docs state that the app then must handle insets or parts of the UI are hidden.
- [MD] Call `enableEdgeToEdge()` (androidx.activity; deprecated in activity 1.14 alpha in favour of `WindowCompat.enableEdgeToEdge(window)`, which is also the Views spelling) so older Android versions behave the same way, and set `android:windowSoftInputMode="adjustResize"` so the app receives IME insets.
- [API] Inset kinds to design for: system bars (tappable UI must not be obscured), system gestures (the OS takes priority), display cutout, and the software keyboard. In Compose: `WindowInsets.safeDrawing` (nothing drawn under system UI), `safeGestures` (no gesture clash), `safeContent` (both); `systemBars` includes the caption bar.
- [API] Material 3 Compose components (`Scaffold`, `TopAppBar`, `BottomAppBar`, `NavigationBar`) apply insets themselves. Compose Material 2 components do not (use their `windowInsets` parameters, material 1.6.0+). Most Views Material components handle insets; `AppBarLayout` needs `android:fitsSystemWindows="true"`.
- [MD] Draw backgrounds, dividers and scrolling content edge to edge; inset text, buttons and other controls.
- [MD] Do not put tap targets or drag handles under system gesture insets.
- [API] Do not compute layout from `Configuration.screenWidthDp` / `screenHeightDp` at targetSdk 35+: they include the system bars. Use insets and window metrics.
- [Conv] If Google's Android skill for edge-to-edge (`edge-to-edge` in android/skills) is installed, prefer it for the migration steps; use this file for the design rules.

Source: https://developer.android.com/develop/ui/compose/system/setup-e2e, https://developer.android.com/develop/ui/compose/system/insets, https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge, https://developer.android.com/about/versions/15/behavior-changes-15

## System bars

- [API] The system bars are the status bar, the caption bar (desktop windowing) and the navigation bar.
- [MD] Keep the status bar transparent when nothing scrolls under it or an image sits under it; make it translucent (a gradient protection matching the surface) when content scrolls underneath.
- [API] Material 3 `TopAppBar` provides that protection when scrolling. [MD] Do not stack a second custom protection on top of it.
- [MD] In multi-pane layouts and navigation drawers give each pane its own protection matching that pane's background.
- [MD] Top app bars should collapse on scroll; a sticky small app bar collapses to status-bar height.
- [MD] Gesture navigation bar: always transparent, no added background or scrim.
- [API] 3-button navigation bar: the system adds a translucent scrim (80% opaque at targetSdk 35) because `setNavigationBarContrastEnforced` defaults to true. [MD] Keep it translucent over scrolling content; make it transparent (contrast enforcement off) when a bottom app bar or navigation bar sits there or nothing scrolls under it.
- [MD] `BottomAppBar` should collapse on scroll through its `scrollBehavior`; `NavigationBar` stays visible.
- [API] `setStatusBarColor`, `setNavigationBarColor` (gesture mode) and the divider-colour APIs are deprecated and disabled at targetSdk 35 on Android 15+; `setNavigationBarColor` still affects 3-button navigation.
- [MD] Immersive mode may hide the bars for video and similar content; the user should still be able to reveal them. In desktop windowing the caption bar stays visible even in immersive mode.

Source: https://developer.android.com/design/ui/mobile/guides/foundations/system-bars, https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge, https://developer.android.com/develop/ui/compose/system/system-bars

## Display cutouts

- [API] Supported from Android 9 (API 28). At targetSdk 35 on Android 15+, or after `enableEdgeToEdge`, non-floating windows draw into the cutout area: `DEFAULT`, `SHORT_EDGES` and `NEVER` are read as `LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS`.
- [MD] Keep important text, controls and fine-touch elements out of the cutout using `WindowInsets.displayCutout`, `safeDrawing` or `safeContent`. The design page words this as something apps "must" do; it is guidance, not an enforced rule.
- [MD] Solid app-bar backgrounds and horizontal carousels should extend into the cutout; only their content is inset.
- [MD] Do not hard-code the status bar height.

Source: https://developer.android.com/develop/ui/compose/system/cutouts, https://developer.android.com/design/ui/mobile/guides/layout-and-content/edge-to-edge

## Gesture and 3-button navigation

- [API] Users choose the navigation mode. Gesture navigation: swipe in from the left or right edge for Back, up from the bottom for Home, up and hold for Overview. Button mode shows Back, Home and Overview.
- [MD] Design for both modes; do not rely on horizontal edge swipes for app features that the Back gesture would intercept.
- [MD] Use `WindowInsetsAnimationCompat` (or the Compose IME insets) so content moves in step with the keyboard.

Source: https://developer.android.com/design/ui/mobile/guides/foundations/system-bars

## Back, Up and predictive back

- [MD] Navigation principles the docs say every app should follow: a fixed start destination; navigation state is a back stack with the start destination at the bottom; Up and Back behave identically inside the app's task; the Up button never exits the app and is not shown on the start destination; Back from the start destination leaves the app; a deep link builds a realistic synthetic back stack.
- [MD] Core app quality: support the standard Back button and the Back gesture, and do not add custom on-screen "back" prompts (`Back_Button_Nav`, `Back_Gesture_Nav`). An Up arrow in the top app bar is the standard affordance, not a custom prompt.
- [API] Predictive back previews the destination while the user swipes. Timeline:

| Device and target | Behaviour |
|---|---|
| Android 13 and 14 | System animations only behind a developer option |
| Android 15+ | Shown for apps that opted in (per app or per activity) |
| Android 16+ with targetSdk 36 | On by default; `onBackPressed` is not called and `KEYCODE_BACK` is not dispatched. Temporary opt-out: `android:enableOnBackInvokedCallback="false"` on the application or activity |

- [API] Supported APIs: AndroidX `OnBackPressedCallback` (Activity 1.6.0+, backward compatible), platform `OnBackInvokedCallback`, Compose `BackHandler` and `PredictiveBackHandler` (activity-compose 1.8.0+).
- [API] An enabled callback at default priority suppresses the system animation, so enable callbacks only while the UI state needs them (unsaved form, open sheet) and never for logging. Intercepting Back at the root removes the back-to-home preview.
- [API] Material Components for Android 1.10.0-alpha02+ animate bottom sheets, side sheets and search with the gesture.
- [MD] Custom full-screen transitions: outgoing surface scales from 100% to 90%, incoming from 110% to 100%, with a fade-through at 35% progress. Shared-element previews keep an 8dp margin from the screen edge and scale to no less than 90%.

Source: https://developer.android.com/guide/navigation/principles, https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture, https://developer.android.com/design/ui/mobile/guides/patterns/predictive-back, https://developer.android.com/docs/quality-guidelines/core-app-quality

## App structure on a phone

- [MD] Primary navigation: a navigation bar for three to five destinations at the same level, or a modal navigation drawer when there are more (the drawer is less ideal because the top bar is a long reach).
- [MD] Tabs and the bottom app bar are secondary navigation inside a destination.
- [MD] One floating action button for the most important action at that level; secondary actions in the top app bar or next to their content; infrequent actions in an overflow menu.
- [MD] Do not keep the bottom navigation bar at large window sizes: `references/platforms-large-screens.md`.
- [MD] Units: dp for layout (1dp is about 1px at 160dpi), sp for text, an 8dp grid with 4dp for small elements.

Source: https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns, https://developer.android.com/design/ui/mobile/guides/layout-and-content/grids-and-units

## Splash screen and app icon

- [API] From Android 12 every app launches with a system splash screen built from the app icon. Migrate a custom splash activity to the `SplashScreen` compat library (`androidx.core:core-splashscreen`).
- [Req] Splash element sizes (asset contract): icon with background 240x240dp inside a 160dp circle; icon without background 288x288dp inside a 192dp circle; branded image 200x80dp. The icon must be a vector drawable; an animated icon must be an `AnimatedVectorDrawable`.
- [MD] Keep an animated splash at or under 1,000 ms.
- [Req] Adaptive icon (asset contract): foreground and background layers of 108x108dp each; the logo at least 48x48dp and at most 66x66dp; the outer 18dp on each side is reserved for masking and motion.
- [API] Themed icons: add a `monochrome` layer (Android 13+). From Android 16 QPR2 the system themes icons that lack one, so supplying the layer is how you control the result.

Source: https://developer.android.com/develop/ui/views/launch/splash-screen, https://developer.android.com/develop/ui/views/launch/icon_design_adaptive, https://developer.android.com/about/versions/16/behavior-changes-all

## Notifications

- [Req] From Android 8.0 (API 26) every notification must belong to a channel; without one it is not shown.
- [API] On Android 13+ notifications from newly installed apps are off until the user grants `POST_NOTIFICATIONS`. With targetSdk 33+ the app chooses the moment; with a lower target the system asks when the first channel is created.
- [MD] Ask in context after explaining the benefit, with dismissible UI; if the user dismisses that UI, do not show the system dialog.
- [MD] Choose channel importance by urgency (high for messages and alarms, default for reminders, low for subscribed content).
- [Req] Do not use notifications for cross-promotion or advertising: the docs describe this as strictly prohibited by the Play Store.
- [MD] Also avoid notifications for rating requests, "come back" nudges, greetings, or background work that needs no user involvement. Messaging apps use `MessagingStyle`, direct reply and conversation shortcuts.

Source: https://developer.android.com/develop/ui/compose/notifications/channels, https://developer.android.com/develop/ui/compose/notifications/notification-permission, https://developer.android.com/design/ui/mobile/guides/home-screen/notifications

## Permissions

- [API] Dangerous permissions are requested at runtime; the user can deny, and the app must keep working.
- [MD] Ask in context, when the user starts the feature that needs the permission, not at startup (`Runtime_Permissions`).
- [MD] Show a rationale UI when `shouldShowRequestPermissionRationale()` returns true, and always let the user cancel it (`Permission_Rationale`).
- [MD] On denial, explain which feature is unavailable and degrade gracefully; never block the whole UI (`Graceful_Degradation`). Request the minimum set (`Minimize_Permissions`).

Source: https://developer.android.com/training/permissions/requesting, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Sharing and the photo picker

- [MD] Share through the Android Sharesheet (`Intent.createChooser()`), not a custom target list (`System_Sharesheet`). It offers ranked targets and, from Android 10, rich previews.
- [API] Pick images and video with the system photo picker (`PickVisualMedia`, `PickMultipleVisualMedia`; androidx.activity 1.7.0+): no storage permission, access only to what the user selects. Available on Android 11 (API 30)+ devices; a backported version reaches Android 4.4 to 10 through Google Play services; otherwise the library falls back to the document picker.

Source: https://developer.android.com/develop/ui/compose/sharing/send, https://developer.android.com/training/data-storage/shared/photo-picker, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Widgets

- [MD] Fill the allotted grid cells, make widgets resizable with a minimum and maximum size, set `targetCellWidth` and `targetCellHeight`, and show more content as the widget grows instead of scaling text.
- [Req] Widget quality guideline `WL-4.2`: the minimum widget size must show a clear use case and meet the 48x48dp touch target requirement.
- [API] targetSdk 37: a `RemoteViews` update whose bitmaps exceed the system memory ceiling throws `IllegalArgumentException` (logged only for lower targets).

Source: https://developer.android.com/design/ui/mobile/guides/widgets/sizing, https://developer.android.com/develop/adaptive-apps/quality-guidelines/widget-quality, https://developer.android.com/about/versions/17/behavior-changes-17

## Settings

- [MD] Call it "Settings" (not "Options" or "Preferences"). Usually not a top-level destination: place it after all other items except Help and feedback in a drawer or top-app-bar menu.
- [MD] Include infrequently changed preferences only. Keep frequent actions next to the feature; keep account management and app information (version, licences) out of settings.
- [MD] Do not replicate or override system settings (theme, accessibility); extend them only when the app adds something.
- [MD] Build it as a list or list-detail layout; group with headings; move a group to a subscreen at about 15 or more settings; the row label matches the subscreen title; keep settings reachable when signed out.
- [MD] Controls: switch or checkbox for on/off; radio buttons in a dialog or child screen for one-of-many (never for a single option); slider for ranges. Do not let single-pane settings stretch full width on large windows.

Source: https://developer.android.com/design/ui/mobile/guides/patterns/settings

## Haptics

- [MD] Less is more: use haptics to confirm a discrete action or state change, never constantly. Subtle for frequent events, stronger for important ones; design them together with visuals and sound.
- [MD] Prefer the action-oriented `HapticFeedbackConstants` so effect and meaning stay consistent across devices; avoid legacy one-shot vibrations for feedback.

Source: https://developer.android.com/develop/ui/views/haptics/haptics-principles

## Dark theme, dynamic colour and text scaling

- [API] Dark theme exists from Android 10 (API 29). [MD] Support light and dark and follow the system setting (`Theme_Support` also covers web content); locking to light is possible but not recommended.
- [API] Dynamic colour (wallpaper-derived schemes) exists from Android 12 (API 31). [MD] Always supply a static scheme as fallback, otherwise the baseline purple scheme appears. Adopt system preferences including contrast; the API for reading the user's contrast setting was not checked for this file. [Unverified]
- [MD] Text in sp; body text not smaller than 12sp.
- [API] Android 14+: the user can scale fonts to 200%, non-linearly (large text grows less). Do not use sp for padding or heights and do not assume sp values add up (4sp + 20sp may not equal 24sp). [MD] Test at 200%.
- [MD] Contrast: at least 4.5:1 for text and 3:1 for non-text elements against their background. Touch targets at least 48dp, a recommendation here (strength by form factor: `references/platforms-quality.md`).

Source: https://developer.android.com/develop/ui/views/theming/darktheme, https://developer.android.com/design/ui/mobile/guides/styles/themes, https://developer.android.com/design/ui/mobile/guides/styles/color, https://developer.android.com/about/versions/14/features, https://developer.android.com/design/ui/mobile/guides/foundations/accessibility

## Common mistakes

| Mistake | Fix |
|---|---|
| Setting a status bar colour to match the app bar | No effect at targetSdk 35 on Android 15+; draw the app bar background behind the transparent bar |
| Opaque or tinted gesture navigation bar | Keep it transparent; pad content with insets |
| Padding the whole screen by the system bar insets | Only content and controls are inset; backgrounds and lists draw edge to edge |
| Overriding `onBackPressed` or listening for `KEYCODE_BACK` | Not delivered at targetSdk 36 on Android 16+; use `OnBackPressedCallback`, `BackHandler` or `PredictiveBackHandler` |
| An always-enabled back callback | Enable it only while the state needs interception, or the system preview never plays |
| Up arrow on the start destination, or Up that leaves the app | Up is hidden on the start destination and stays inside the app |
| Asking for notification or other permissions on first launch | Ask in context with a dismissible explanation |
| Custom share dialog or storage permission just to pick a photo | Sharesheet; system photo picker |
| No dark theme, or dynamic colour without a fallback scheme | Provide light, dark and a static fallback |
| Fixed-height text containers, sp used for spacing | Let text containers grow; spacing in dp; test at 200% font scale |
| Custom splash activity | System splash through the `SplashScreen` library |
