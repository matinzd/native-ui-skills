# 03 - Android platform conventions, form factors and quality guidance

> Research workstream M3 for the `material-design` skill. Fetched 2026-11-23. Primary source: developer.android.com
> (pages fetched as Markdown by appending `.md.txt` to the page URL, which works with plain curl).

## 0. Method, sources, licence

- **Source notation.** `(src: /path)` means `https://developer.android.com/path`. m3.material.io is cited in full.
- **Tags.** `[V]` fetched in this session and the page says this. `[M]` from memory, not verified. `[Syn]` my synthesis
  of verified facts (not a statement Google makes). Strength: **Req** (docs say must / enforced by platform, Play or
  API), **Rec** (should / recommend / do-don't), **Conv** (convention).
- **Scratch folder** (about 360 pages as `.md`, named by URL path with `/` replaced by `_`):
  `<scratch>/m3-agent/pages/`
  Helpers: `.../m3-agent/tools/get.sh /path ...` (batch fetch), `.../m3-agent/tools/v.py file` (strip links for reading).
  Navigation indexes: `_nav_*.txt`, `_llms_*.txt` (developer.android.com publishes `llms.txt` indexes per section, for
  example `/develop/ui/llms.txt`, `/design/llms.txt`, `/develop/xr/llms.txt`, `/training/wearables/llms.txt`).
- **Licence** [V] (src: /license): documentation and code on developer.android.com are Apache 2.0 unless noted; "all
  other content" is Creative Commons Attribution 2.5; Google trademarks and brand features are excluded. Page footer:
  "Content and code samples on this page are subject to the licenses described in the Content License."
  m3.material.io footer shows only "Privacy Policy / Terms of Service"; I did not find a licence statement there.
- **Discovery worth knowing** [V] (src: /tools/agents/android-skills): Google now ships official "Android skills"
  (agent-skills format, repository `github.com/android/skills`, installed with `android skills add <name>`). Pages
  advertise `edge-to-edge` (src: /develop/ui/compose/system/setup-e2e) and `wear-compose-m3`
  (src: /training/wearables/compose). Our skill should complement, not duplicate, these; github.com is blocked here so I
  could not read them.

## 1. Current platform state (as the docs state it on 2026-11-23)

| Item | Value | Tag and source |
|------|-------|----------------|
| Newest Android version documented | Android 17, API level 37, `CINNAMON_BUN` | [V] (src: /guide/topics/manifest/uses-sdk-element), (src: /about/versions/17) |
| Android 17 release status | `/about/versions/17/get` says supported Pixels "receive Android 17 over the air"; behaviour-change pages are written in final form. But `/tools/releases/platforms` and the `/about/versions` list still stop at Android 16 (API 36). Treat "17 is final" as likely, not confirmed by one unambiguous sentence | [V] both pages; conclusion [Syn] |
| Android 16 / 15 / 14 | API 36 `BAKLAVA` / 35 `VANILLA_ICE_CREAM` / 34 | [V] same |
| Google Play target API (from 31 Aug 2026) | New apps and updates: API 36+. Wear OS and Android Automotive OS: API 35+. Android TV and Android XR: API 34+. Existing apps must target 35+ to stay available to new users on newer OS versions. Extension available to 1 Nov 2026 | [V] Req (src: /google/play/requirements/target-sdk) |
| Compose BOM | Mapping page drop-down lists `2026.11.01` as newest; the BOM how-to page still shows `2026.09.00` in its snippet | [V] (src: /develop/ui/compose/bom/bom-mapping), (src: /develop/ui/compose/bom) |
| Compose Material 3 | `androidx.compose.material3:material3` **1.5.0 stable (18 Nov 2026)**, 1.6.0-alpha01 | [V] (src: /jetpack/androidx/releases/compose-material3) |
| Compose core (ui, foundation, runtime, animation, material) | 1.13.0 stable, 1.14.0-alpha01 | [V] (src: /jetpack/androidx/releases/compose) |
| Material 3 Expressive in Compose | Stable in material3 1.5.0: expressive buttons, button groups, split button, toggle buttons, FAB menu, floating toolbars, expressive list items, menus, text-field styling, wavy progress indicators, expressive theming. Still experimental in 1.5.0: `LoadingIndicator`/`ContainedLoadingIndicator`, `MaterialShapes`, `AppBarWithSearch`, carousel parallax, standalone static `BottomSheet`. A `Material3ExpressiveApi` annotation "that doesn't require OptIn" was added. In 1.4.0 all `ExperimentalMaterial3ExpressiveApi` APIs had been removed from the stable line ("switch to 1.5.0-alpha") | [V] same release notes |
| Docs' own framing | "M3 Expressive is an expansion of Material Design 3 ... complements the Android 16 visual style and system UI" | [V] (src: /develop/ui/compose/designsystems/material3) |
| Material 3 adaptive | `androidx.compose.material3.adaptive:adaptive*` 1.3.0 stable, 1.4.0-alpha03; `material3-adaptive-navigation-suite` ships in the material3 group | [V] (src: /jetpack/androidx/releases/compose-material3-adaptive) |
| Wear Compose | Group `androidx.wear.compose` 1.7.2 stable, 1.8.0-alpha04; M3 artifact `androidx.wear.compose:compose-material3` (migration guide uses 1.7.2). The separate "wear-compose-m3" release page still says stable 1.5.0, last updated Aug 2025 (stale) | [V] (src: /jetpack/androidx/releases/wear-compose), (src: /training/wearables/compose/migrate-to-material3) |
| Wear OS | Wear OS 6 is based on Android 16 (API 36); Wear OS 7 is referenced (one-handed gestures, Live Updates) | [V] (src: /training/wearables/versions/6), (src: /design/ui/wear/guides/patterns/gestures) |
| Compose for TV | `androidx.tv:tv-material` 1.1.0, `tv-foundation` 1.0.0 (updated 6 May 2026); package `androidx.tv.material3`. Leanback is "deprecated" | [V] (src: /jetpack/androidx/releases/tv), (src: /training/tv/playback/leanback) |
| Car App Library | `androidx.car.app:app` 1.7.0 stable, 1.8.0-rc01, 1.9.0-alpha03 | [V] (src: /jetpack/androidx/releases/car-app) |
| Jetpack Compose for XR | `androidx.xr.compose:compose` 1.0.0-rc01 (no stable yet); Glimmer `androidx.xr.glimmer:glimmer` 1.0.0-alpha22 | [V] (src: /jetpack/androidx/releases/xr-compose), (src: /jetpack/androidx/releases/xr-glimmer) |
| Glance / Window / Tiles | glance 1.2.0; window 1.5.1; wear tiles 1.6.2; protolayout 1.4.2 | [V] respective release pages |
| New device class | "Googlebook" (Android stack on ChromeOS desktop foundations) now appears next to tablets, foldables and Chromebooks in adaptive guidance | [V] (src: /develop/adaptive-apps/guides/googlebook/overview) |

## 2. Structure of the Android design and quality docs (discovered, not guessed)

| Hub | Real sections | Tag |
|-----|---------------|-----|
| `/design/ui/mobile` | `guides/foundations/{accessibility,system-bars,glossary,translate-designs}`; `guides/layout-and-content/{layout-basics,app-anatomy,content-structure,grids-and-units,edge-to-edge,adapt-layout,layout-and-nav-patterns,common-layouts,postures-and-orientation,immersive-content,images-graphics}`; `guides/styles/{themes,color}`; `guides/patterns/{predictive-back,settings,onboarding,help-content,passkeys}`; `guides/home-screen/{notifications,live-updates,picture-in-picture}`; `guides/widgets/{layouts,sizing,style,adapt,configuration,discovery-promotion}`; `guides/components/material-overview` | [V] |
| `/design/ui/desktop` (old `/design/ui/large-screens` redirects here) | `foundations/design-principles`, `interaction/pointer-interactions`, `system/{multi-task,system-bars}` | [V] |
| `/design/ui/wear` | M3 Expressive guides: `get-started/*`, `foundations/{adaptive-design,common-layouts,quality-tiers}`, `styles/{color,typography}`, `surfaces/{apps,tiles}`, `patterns/{gestures,media}`; older Material 2.5 guides kept under `guides/m2-5/*` | [V] |
| `/design/ui/tv` | `foundations/{design-for-tv,navigation-on-tv,color-on-tv}`, `styles/{layouts,typography,focus-system,color-system}`, `components/{buttons,cards,featured-carousel,immersive-list,lists,navigation-drawer,tabs}`, `system/tv-app-icon-guidelines` | [V] |
| `/design/ui/cars` | `foundations/{design-principles,design-process}`, `app-types/{media-apps,navigation-apps,communications,other-apps,parked-passenger-apps}`, `templates/overview`, `components/overview`, `flows/overview`, `ux-requirements/overview` | [V] |
| `/design/ui/xr` (immersive) and `/design/ui/ai-glasses` (augmented) | `foundations`, `spatial-ui`, `visual-design`, `environments`, `3d-content`, `motion`, `spatial-anchor`, `considerations`, `glimmer` | [V] |
| `/design/ui/widget` | hub for widget guides | [V] |
| Quality | `/docs/quality-guidelines/{core-app-quality,adaptive-app-quality,wear-app-quality,tv-app-quality,car-app-quality}`, mirrored under `/develop/adaptive-apps/quality-guidelines/` which adds `adaptive-app-quality/{tier-1,tier-2,tier-3,experiences/{desktop,foldables,camera-audio,stylus}}`, `android-xr`, `widget-quality` | [V] |
| Adaptive dev guides | `/develop/ui/compose/layouts/adaptive/*` and mirror `/develop/adaptive-apps/guides/*` (adds `chromeos/`, `googlebook/`, `tv/`) | [V] |

## 3. Mobile platform conventions

### 3.1 Layout basics, units, grid
- [V] Rec: design for portrait and landscape, several size classes and aspect ratios; honour "device safe areas" (cutouts,
  edge-to-edge insets, edge displays, software keyboard, system bars); keep primary navigation in a reachable area; do
  not hide inputs behind the keyboard. (src: /design/ui/mobile/guides/layout-and-content/layout-basics)
- [V] dp is relative to a 160 dpi screen (1 dp ~ 1 px there); `dp = (px * 160) / density`. "Always specify font sizes in sp."
  Android UI "utilizes an 8 dp grid"; icons, type and small elements align to 4 dp. Recommended aspect ratios: 16:9,
  3:2, 4:3, 1:1, 3:4, 2:3. (src: /design/ui/mobile/guides/layout-and-content/grids-and-units)
- [V] Window size classes (src: /develop/ui/compose/layouts/adaptive/use-window-size-classes):

| Class | Width | Height |
|-------|-------|--------|
| Compact | < 600dp | < 480dp |
| Medium | 600dp to < 840dp | 480dp to < 900dp |
| Expanded | 840dp to < 1200dp | >= 900dp |
| Large | 1200dp to < 1600dp | - |
| Extra-large | >= 1600dp | - |

  Computed from the **window**, not the device ("not intended for isTablet-type logic"); they change at runtime. API:
  `currentWindowAdaptiveInfo().windowSizeClass` in `androidx.compose.material3.adaptive`; pass
  `supportLargeAndXLargeWidth = true` to get Large and Extra-large. Note: the mobile design page still says "Android
  breaks window size classes into 3" (stale relative to the developer page).
- [V] Rec: compact = one pane; medium = one or two panes; large and extra-large = multiple panes. Set a max width on
  content and components; let components change presentation (bottom sheet to side sheet) instead of stretching; do not
  stretch inputs and buttons. (src: /design/ui/mobile/guides/layout-and-content/adapt-layout)
- [V] Core quality `Line_Length`: limit text lines to 45-75 characters including spaces. (src: /docs/quality-guidelines/core-app-quality)

### 3.2 System bars, edge-to-edge, insets, cutouts
| Fact | Strength | Tag and source |
|------|----------|----------------|
| System bars = status bar, caption bar (desktop windowing), navigation bar | fact | [V] (src: /design/ui/mobile/guides/foundations/system-bars) |
| Apps targeting API 35 are edge-to-edge by default on Android 15+ devices; "you must handle insets" | Req (platform) | [V] (src: /about/versions/15/behavior-changes-15) |
| With targetSdk 35 an app could opt out via `R.attr#windowOptOutEdgeToEdgeEnforcement`. With targetSdk 36 on an Android 16 device that attribute is "deprecated and disabled"; on an Android 15 device it still works | Req (platform) | [V] (src: /about/versions/16/behavior-changes-16) |
| On Android 15 with targetSdk 35: status bar transparent; `setStatusBarColor` / `R.attr#statusBarColor` deprecated with no effect; gesture nav bar transparent, `setNavigationBarColor` deprecated and without effect on gesture nav; 3-button nav gets an 80% opaque scrim (`setNavigationBarContrastEnforced` true by default) | fact | [V] same page |
| Non-floating windows are forced to `LAYOUT_IN_DISPLAY_CUTOUT_MODE_ALWAYS`; `SHORT_EDGES`, `NEVER`, `DEFAULT` are read as `ALWAYS` | Req (platform) | [V] same page |
| Call `enableEdgeToEdge()` (androidx.activity; `WindowCompat.enableEdgeToEdge(window)` for Views) for backward compatibility | Rec | [V] (src: /develop/ui/compose/system/setup-e2e), (src: /develop/ui/views/layout/edge-to-edge) |
| Inset types: system bars (tappable UI that must not be obscured), system gestures, display cutout. Compose: `WindowInsets.safeDrawing`, `safeGestures`, `safeContent`, `systemBars` (includes caption bar), `displayCutout` | fact | [V] (src: /develop/ui/compose/system/insets), (src: /design/ui/mobile/guides/layout-and-content/edge-to-edge) |
| "Transparent gesture navigation bars are always recommended"; do not add a background to the gesture bar; use a translucent 3-button bar over scrolling content | Rec | [V] system-bars page |
| Avoid tap gestures or drag targets under system gesture insets | Rec | [V] edge-to-edge design page |
| "Apps must handle display cutout insets so that important parts of the UI don't draw underneath the display cutout"; solid app-bar backgrounds and horizontal carousels should draw into the cutout | Rec worded "must" | [V] same |
| Backgrounds and dividers draw edge to edge; text and buttons are inset. Do not stack two status-bar protections. `NavigationBar` stays visible on scroll; `BottomAppBar` should collapse via `scrollBehavior` | Rec | [V] same |
| In desktop windowing the caption bar is always visible, even in immersive mode | fact | [V] (src: /develop/ui/views/layout/edge-to-edge) |
| Material 3 `Scaffold` and M3 components apply insets for you | fact | [V] behaviour-changes-15 |

Edge-to-edge is **platform behaviour tied to targetSdk**, not a named Google Play policy; it becomes unavoidable only
because Play requires targetSdk 36 (section 1). [Syn]

### 3.3 Gesture navigation, 3-button navigation, predictive back
- [V] Gesture navigation: swipe from left or right edge = back, up from bottom = home, up and hold = overview. Users can
  choose gesture or button navigation; design for both. (src: /design/ui/mobile/guides/foundations/system-bars)
- Predictive back timeline:

| Android / target | Behaviour | Tag and source |
|------------------|-----------|----------------|
| Android 13, 14 | System animations (back-to-home, cross-activity, cross-task) only behind a Developer option | [V] (src: /develop/ui/compose/system/predictive-back-setup) |
| Android 15+ | Developer option removed; system animations appear for apps that migrated to the supported back APIs (opt-in app-wide or per activity) | [V] (src: /guide/navigation/custom-back/predictive-back-gesture) |
| targetSdk 36 on Android 16+ | Enabled by default; `onBackPressed` is not called and `KeyEvent.KEYCODE_BACK` is not dispatched. Migrate, or temporarily set `android:enableOnBackInvokedCallback="false"` on `<application>` or `<activity>` | [V] Req (platform) (src: /about/versions/16/behavior-changes-16) |
| Android 16 (all apps) | Predictive back also works in 3-button navigation: long-press Back previews | [V] (src: /about/versions/16/behavior-changes-all) |

- [V] APIs: AndroidX Activity 1.6.0+ `OnBackPressedCallback` (backward compatible) or platform `OnBackInvokedCallback`;
  Compose `BackHandler` and `PredictiveBackHandler` (needs `androidx.activity:activity-compose` 1.8.0+); Navigation
  Compose 2.8.0+ cross-fades by default. Intercepting back at the root activity disables the back-to-home animation.
  Material Components for Android 1.10.0-alpha02+ animates bottom sheets, side sheets and search on back.
  (src: /guide/navigation/custom-back/predictive-back-gesture), (src: /design/ui/mobile/guides/patterns/predictive-back)
- [V] Rec motion specs for custom full-screen transitions: exit scale 100% to 90%, enter 110% to 100%, fade-through at
  35% progress; shared-element preview keeps an 8dp margin, x-shift `((screen width / 20) - 8) dp`, minimum scale 90%.
  (src: /design/ui/mobile/guides/patterns/predictive-back)

### 3.4 Navigation principles and patterns
- [V] Principles ("your app should follow these" even without the Navigation component): fixed start destination; state
  is a back stack; **Up and Back are identical within your app's task**; **the Up button never exits your app** (not
  shown on the start destination), Back does; deep links build a synthetic, realistic back stack.
  (src: /guide/navigation/principles)
- [V] Rec: navigation bar and modal navigation drawer are primary navigation; the navigation bar "can hold three to five
  navigation destinations"; it "translates to the navigation rail for large screens"; tabs and bottom app bar are
  secondary navigation; one FAB action at a time. "Don't use a bottom navigation bar on large screen sizes."
  (src: /design/ui/mobile/guides/layout-and-content/layout-and-nav-patterns)
- [V] `NavigationSuiteScaffold` default: navigation bar if width **or height** is compact or the device is in tabletop
  posture; navigation rail otherwise. (src: /develop/ui/compose/layouts/adaptive/build-adaptive-navigation)
- [V] Core quality `Back_Button_Nav`: "does not make use of any custom, onscreen back button prompts";
  `Back_Gesture_Nav`: supports gesture back and home. (src: /docs/quality-guidelines/core-app-quality)

### 3.5 App surfaces
| Surface | What the docs state | Tag and source |
|---------|--------------------|----------------|
| Notifications | Android 8.0 (API 26)+: every notification "must be assigned to a channel". Android 13 (API 33)+: runtime `POST_NOTIFICATIONS`; notifications off by default on new installs; apps targeting 33+ control when the dialog appears. Rec: explain benefit first, do not re-show after dismissal. Core `Notification_Quality`: no cross-promotion or ads ("strictly prohibited by the Play Store"), channels, groups, persistent only for ongoing events. `Conversation_Quality`: `MessagingStyle`, direct reply, conversation shortcuts, bubbles | [V] (src: /develop/ui/compose/notifications/channels), (src: /develop/ui/compose/notifications/notification-permission), (src: /design/ui/mobile/guides/home-screen/notifications), core quality |
| Widgets | Fill the grid bounds; resizable with min and max; `targetCellWidth`/`targetCellHeight`; widget quality tiers 3/2/1 with IDs `WL-*`, `WC-*`, `WD-*`, `WT-*`; `WL-4.2`: minimum size must "meet the 48x48 dp touch target requirement". Android 17: widget memory limit changes for targetSdk 37 | [V] (src: /design/ui/mobile/guides/widgets/sizing), (src: /develop/adaptive-apps/quality-guidelines/widget-quality), (src: /about/versions/17/behavior-changes-17) |
| Share sheet | Use `Intent.createChooser()`; core `System_Sharesheet`: "App should use the Android Sharesheet when sharing content" | [V] Rec (src: /develop/ui/compose/sharing/send), core quality |
| Photo picker | `ActivityResultContracts.PickVisualMedia` / `PickMultipleVisualMedia`; no storage permission needed. Built in on Android 11 (API 30)+ devices; a backported module via Google Play services covers Android 4.4 (API 19) to Android 10 | [V] (src: /training/data-storage/shared/photo-picker) |
| Permissions | Ask in context when the feature is used; do not block; show rationale UI when `shouldShowRequestPermissionRationale()` is true. Core IDs `Runtime_Permissions` (not at startup), `Permission_Rationale`, `Graceful_Degradation`, `Minimize_Permissions` | [V] (src: /training/permissions/requesting), core quality |
| Splash screen | Android 12+: system splash for every app; migrate custom splash to the `SplashScreen` compat library. Icon with background 240x240dp inside a 160dp circle; without background 288x288dp inside a 192dp circle; branded image 200x80dp; icon must be a vector drawable | [V] Req (API contract) (src: /develop/ui/views/launch/splash-screen) |
| App icon | Adaptive icon layers 108x108dp; logo at least 48x48dp and at most 66x66dp; outer 18dp per side reserved for masking. Themed icons from Android 13 (API 33) via a `<monochrome>` layer; from Android 16 QPR2 the system auto-themes icons that lack one | [V] (src: /develop/ui/views/launch/icon_design_adaptive), (src: /about/versions/16/behavior-changes-all) |
| Settings | Label it "Settings" (not "Options"/"Preferences"); place after all other items except Help & Feedback; usually not a top-level destination; do not replicate or override system settings; no account management or about-info inside settings | [V] Rec (src: /design/ui/mobile/guides/patterns/settings) |
| Picture-in-picture, Live Updates, shortcuts | Core `Video_PiP` "should support"; design pages exist. Not read in depth | [V] existence; details not verified |

### 3.6 Themes, colour, text, haptics
- [V] Dark theme: available from Android 10 (API 29) (src: /develop/ui/views/theming/darktheme). Core `Theme_Support`:
  app content and web content "support both light and dark themes". Locking to light is possible but "we don't
  recommend" it (src: /design/ui/mobile/guides/styles/themes).
- [V] Dynamic colour: Android 12 (API 31)+. Compose `dynamicLightColorScheme(context)` / `dynamicDarkColorScheme(context)`
  gated on `Build.VERSION_CODES.S`; Views `DynamicColors` API. "We strongly recommend creating a static scheme as a
  fallback"; otherwise the baseline purple scheme is used. (src: /develop/ui/compose/designsystems/material3),
  (src: /develop/ui/views/theming/dynamic-colors), (src: /design/ui/mobile/guides/styles/color)
- [V] Rec: adopt system preferences "including themes, like light or dark, dynamic, and contrast" (themes page). The
  API for the user contrast setting was **not verified** in this workstream.
- [V] Text: sp everywhere; body not smaller than 12sp (design accessibility page). Android 14+: font scaling up to 200%
  with a **non-linear** curve (large text grows less). "Don't use sp units for padding or define view heights assuming
  implicit padding ... 4sp + 20sp might not equal 24sp"; convert with `TypedValue.applyDimension()` /
  `deriveDimension()`; test at 200%. (src: /about/versions/14/features)
- [V] Android 15/16: `elegantTextHeight` defaults to true for targetSdk 35 and is ignored for targetSdk 36 (taller
  line metrics for Arabic, Thai, Tamil and others). (src: /about/versions/16/behavior-changes-16)
- [V] Haptics, Rec: "less is more"; use for attention, confirming a state change, or delight; prefer action-oriented
  `HapticFeedbackConstants` over raw `VibrationEffect` so the platform can provide fallbacks.
  (src: /develop/ui/views/haptics/haptics-principles)

## 4. Accessibility on Android

| Topic | Exact wording / number | Strength | Tag and source |
|-------|------------------------|----------|----------------|
| Touch target | "Ensure all touch targets are at least 48 dp, even if this extends past the UI element visual." | Rec | [V] (src: /design/ui/mobile/guides/foundations/accessibility) |
| Touch target | Core quality `Touch_Target_Size`: "Touch targets are at least 48 dp." Adaptive Tier 2 `Touch_Targets`: "at least 48dp" | quality guideline | [V] core and tier-2 pages |
| Touch target | "make sure to set the minimum size to 48dp to correctly follow the Material Design accessibility guidelines"; Material components add this padding only when interactive (for example `Checkbox` with non-null `onCheckedChange`) | Rec + API fact | [V] (src: /develop/ui/compose/accessibility/api-defaults) |
| Touch target | "touch target size, of at least 48dpx48dp. Larger is even better." | Rec | [V] (src: /guide/topics/ui/accessibility/apps) |
| Touch target (Material) | "For most platforms, consider making touch targets at least 48 x 48dp" (about 9mm; recommended 7-10mm). "Consider making pointer targets minimums 44 x 44dp." Targets separated by 8dp or more | Rec ("consider") | [V] https://m3.material.io/foundations/designing/structure |
| Contrast | Text smaller than 18sp, or bold and smaller than 14sp: at least 4.5:1; all other text at least 3:1 ("we recommend") | Rec | [V] (src: /guide/topics/ui/accessibility/apps) |
| Contrast | Core `Visual_Contrast`: 3:1 for large text and graphics; 4.5:1 for small text ("less than 18 pt or less than 14 pt if text is bold") - note pt here, sp elsewhere | quality guideline | [V] core page |
| Contrast | 4.5:1 text to background; 3:1 between surfaces and non-text elements | Rec | [V] design accessibility page |
| Labels | Core `Content_Description`: "Describe each UI element, except for TextView, using contentDescription." Set decorative items' description to null; group elements | quality guideline / Rec | [V] core page, design accessibility page |
| Semantics | Compose semantics tree; merging and clearing; traversal order; `paneTitle`, `liveRegion` | API | [V] (src: /develop/ui/compose/accessibility/semantics) and siblings |
| Announcements | Android 16 deprecates `announceForAccessibility` / `TYPE_ANNOUNCEMENT`; use pane titles, live regions, error state instead | API | [V] (src: /about/versions/16/behavior-changes-all) |
| Gestures | "Don't rely on gestures to complete all actions; create accessibility actions" (example: swipe-to-delete plus a delete button) | Rec | [V] design accessibility page |
| Scalable content | Offer pinch-to-zoom with reflow (density or font scaling) for reading layouts | Rec | [V] (src: /develop/ui/compose/accessibility/scalable-content) |
| Services to test with | TalkBack, Switch Access, Voice Access (manual); Accessibility Scanner; Compose UI Check in Android Studio | Rec | [V] (src: /guide/topics/ui/accessibility/testing) |
| Automated, Compose | From Compose 1.8.0: add `ui-test-junit4-accessibility`, call `composeTestRule.enableAccessibilityChecks()`, then any action or `onRoot().tryPerformAccessibilityChecks()`; checks labels, contrast, small touch targets, traversal order (Accessibility Test Framework) | API | [V] (src: /develop/ui/compose/accessibility/testing) |
| Automated, Views | Espresso `AccessibilityChecks.enable()` (optionally `.setRunChecksFromRootView(true)`); runs on `ViewActions` | API | [V] (src: /training/testing/espresso/accessibility-checking) |
| Keyboard focus | Adaptive Tier 2 `Drawable_Focus`: interactive custom drawables "must be focusable when the device is not in Touch Mode" with a visible focus state | quality guideline | [V] tier-2 page |

## 5. Quality guidelines

### 5.1 Core app quality (src: /docs/quality-guidelines/core-app-quality) [V]
Wording: "The guidelines define the minimum quality that all apps should meet." IDs are now **named** (the old coded
IDs such as `VD-1`, `FN-P1` are gone from this page). UI-relevant IDs:

| Area | IDs |
|------|-----|
| Usability | `Consistent_UX`, `App_Switcher`, `Sleep_Resume`, `Lock_Resume` |
| User interface | `Display_State_Parity`, `Fullscreen_Display` (not letterboxed, both orientations), `Orientation_Transitions` |
| Visual quality | `Graphic_Quality`, `Line_Length` (45-75 chars), `Theme_Support` (light and dark) |
| Navigation | `Back_Button_Nav`, `Back_Gesture_Nav`, `State_Preservation` |
| Notifications | `Notification_Quality`, `Conversation_Quality` |
| Accessibility | `Touch_Target_Size` (48 dp), `Visual_Contrast` (3:1 / 4.5:1), `Content_Description` |
| Functionality | `Audio_*` (several say "must": foreground service, `MediaStyle` notification), `Video_PiP`, `Video_Playback_Background`, `System_Sharesheet`, `Background_Service_Optimization` |
| Performance | `App_Startup_Time` (feedback if > 2 s), `Rendering_Performance` (16 ms frames), `Stability_ANR`, `Target_SDK_Version`, `Compile_SDK_Version` |
| Privacy / identity | `Minimize_Permissions`, `Runtime_Permissions`, `Permission_Rationale`, `Graceful_Degradation`, `Autofill_Hints`, `Credential_Manager`, `Biometric_Authentication` |
| Google Play | `Play_Content_Policies`, `App_Bundles` (app bundles "mandatory for all new apps" since Aug 2021) |

Each ID has a matching test `T-<ID>`. Also stated: "Use Material Design components ... in place of Android platform
components where possible."

### 5.2 Adaptive app quality (replaces "large screen app quality") [V]
- "The adaptive app quality guidelines replace and extend the guidance formerly provided in the large screen app
  quality guidelines" (archive entry dated 2026-01-21, with an ID map). The old page with `LS-*` IDs (`LS-C1` ...
  `LS-U4`) still resolves, and the car quality page still cites `LS-C1`/`LS-C2`. (src: /docs/quality-guidelines/adaptive-app-quality)
- "Tier 3 - Adaptive ready defines the baseline quality standard for apps on foldables and large screens on Google
  Play, while Tier 2 and Tier 1 help your app qualify for enhanced promotion and store badging." Tier 2 earns the
  "Google Play Large Screen Badge".

| Tier | Name | Guideline IDs |
|------|------|---------------|
| 3 | Adaptive ready | `Config_Changes` (fills window, not letterboxed, keeps scroll/text/playback state), `Config_Combinations`, `Multi-Window_Functionality`, `Multi-Resume`, `Camera_Preview`, `Media_Projection`, `Keyboard_Input`, `Mouse_Trackpad_Basic`, `Stylus_Basic`, `Stylus_Text_Input` |
| 2 | Adaptive optimized | `Responsive_adaptive_layouts` (window size classes, rails that expand, multi-pane via canonical layouts, `ListDetailPaneScaffold`), `UI_Secondary_Elements` (bottom sheets, buttons, text fields not full width; context menus next to the item; "Navigation rails replace navigation bars"; "Navigation drawers are updated to expanded navigation rails"), `Touch_Targets`, `Drawable_Focus`, `Keyboard_Navigation` (Tab and arrows), `Keyboard_Shortcuts`, `Keyboard_Media_Playback` (Spacebar), `Keyboard_Send` (Enter), `Keyboard_Exit` (Esc closes modals/menus/search), `Context_Menus` (right-click), `Content_Zoom` (Ctrl+wheel, pinch), `Hover_States` |
| 1 | Adaptive differentiated | Organised by experience: Desktop (`Scrollbar_Display`, `Hover_Parity`, `Desktop_Menus`, `UI_Config`, `Request_Fullscreen_Mode`, `Keyboard_Parity`, `Input_Combinations`, `Triple_Click`, `Multitasking_*`, `Multi-Instance`, `Drag_Drop_Support`, `Printing_Support`, `File_*`, `Custom_Cursors`, `Cursor_Target_Size`, `Cross_Device_Handoff`, `Offline_Support`, `Web_Transition`), Foldables (`Foldables_Postures`, `Foldables_Camera`, `Foldables_PiP`, `Foldables_Multi-Instance`), Camera/Audio, Stylus, Cars, TV, XR, Games, Widgets |

Test devices named: Googlebook (160 ppi), foldable 1:1 (802x802 dp), foldable 4:3 (1024x768 dp), 8-inch tablet
(1024x640 dp), 10.5-inch tablet (1280x800 dp), 13-inch Chromebook (1600x900 dp).

### 5.3 Orientation and resizability on large screens (platform, by targetSdk) [V]
| Target | Behaviour on displays with smallest width >= 600dp | Source |
|--------|-----------------------------------------------------|--------|
| API 36 | `screenOrientation`, `resizeableActivity`, `minAspectRatio`, `maxAspectRatio`, `setRequestedOrientation()` are ignored; app fills the window, no pillarboxing. Temporary opt-out: manifest `<property android:name="android.window.PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY" android:value="true"/>` per activity or application | (src: /about/versions/16/behavior-changes-16) |
| API 37 | Opt-out no longer available | (src: /about/versions/17/behavior-changes-17), (src: /about/versions/17/changes/ff-restrictions-ignored) |
| Exceptions | Games (`android:appCategory`), users opting in via aspect-ratio settings, screens smaller than sw600dp | behaviour-changes-16 |

Also: on Android 12 (API 31)+ large screens support multi-window regardless of `resizeableActivity`; "Don't set
`resizeableActivity="false"` for any API level"; "Letterboxed apps are subject to decreased discoverability on Google
Play". (src: /develop/ui/compose/layouts/adaptive/adaptive-dos-and-donts)

### 5.4 Wear OS quality (src: /docs/quality-guidelines/wear-app-quality) [V]
"To publish on the Play Store, your watch app must satisfy all the applicable requirements."
- Visual: `WO-V1` respect user font size without overlap or clipping; `WO-V2` 48x48dp touch targets; `WO-V3`
  swipe-to-close from almost all screens (exceptions: ongoing fitness, panning maps, with a clear close action);
  `WO-V4` ongoing activity uses `OngoingActivity` or a Live Update; `WO-V5` state preservation; `WO-V6` launcher icon
  and name; `WO-V8` show scroll bar on scrollable views; `WO-V9` tile signed-out state; `WO-V10` tile preview;
  `WO-V13` black background for apps and tiles; `WO-V14` minimum 12sp essential text, 10sp non-essential; `WO-V15`
  splash: 48x48dp app icon on black; `WO-V16` content fits the display, no overlap or clipping, at least a 192dp
  circle. (`WO-V7`, `WO-V11` retired.)
- Functional: `WO-P1` target API; `WO-P6` "must not ask the user to input a username or password directly on the Wear
  OS device"; `WO-P7` always-on watch faces light at most 15% of pixels; `WO-P10` at most 8 complication slots;
  `WO-G7` same package name and signing key as the phone app.
- Dated requirements: Watch Face Format required since Jan 2026; 64-bit support since 15 Sep 2026. Its "target API 34
  as of 31 Aug 2025" paragraph is older than the target-sdk page (API 35 for Wear from 31 Aug 2026).

### 5.5 Android TV quality (src: /docs/quality-guidelines/tv-app-quality) [V]
Tiers: 3 "TV Ready" (fundamental requirements), 2 "TV Optimized", 1 "TV Differentiated". Tier 3 UI items:
`TV-LM` launcher icon; `TV-LB` 320x180 px banner and 160x160 px icon; `TV-BN` banner contains app name; `TV-LO`
landscape without letterboxing or pillarboxing; `TV-OV` nothing cut off by screen edges (overscan); `TV-TR`
full-screen, non-transparent background; `TV-DP` fully navigable with a five-way D-pad; `TV-DM` no dependence on a
Menu button; `TV-DB` Back leads back to the Android TV home screen; `TV-PS` `minSdkVersion` 31 or lower; `TV-ML`
`CATEGORY_LEANBACK_LAUNCHER`; `TV-MT` touchscreen declared not required; `TV-WB` web content only in `WebView`, never
launch a browser; `TV-PC` D-pad centre toggles play/pause, left/right seek; `TV-I*` PiP rules; `TV-G1` app bundles;
`TV-G6` 32/64-bit and 16 KB page size from 1 Aug 2026. Tier 2 adds `TV-4K`, `TV-VS` voice search, `TV-LI` phone or
Google sign-in. Tier 1 adds `TV-TO` touch and pointer support with hover states, `TV-AX` enhanced accessibility.

### 5.6 Cars quality (src: /docs/quality-guidelines/car-app-quality) [V]
Tiers: 3 "Car ready" (parked categories: video, games, browsers - required for Play acceptance), 2 "Car optimized"
(driving categories "must meet all of the applicable requirements in this tier to be accepted"), 1 "Car
differentiated". Selected IDs: `PC-1` only permitted categories; `AR-1` nothing obstructed by system bars or cutouts;
`DD-2`/`DD-3` parked apps not launchable or visible while driving; `SA-1` no animated elements; `IU-1` no images
(except one static content image, icons); `ST-1` no auto-scrolling text; `AC-1` tasks in five screens or fewer;
`VC-1` voice commands (media, navigation); `DR-1` button response within 2 s; `DR-2`/`DR-3` launch and load within
10 s; `VD-1..3` contrast; `TH-1` custom theming with Car App Library 1.9+ must support light and dark; `MA-1` no
autoplay; `IN-1`, `NA-1` notification limits; `PA-1` simple purchase flows only.

### 5.7 XR and widgets [V]
- XR quality is split into immersive (headsets, wired XR glasses) and augmented (audio and display glasses) guideline
  sets; the hub page only links to them (not fetched). (src: /develop/adaptive-apps/quality-guidelines/android-xr)
- Widget quality tiers: section 3.5.

## 6. Form factors

### 6.1 Phone
Inputs: touch, system gestures, IME. Navigation: navigation bar (3-5) or drawer, top app bar with Up, system Back.
Numbers: 48dp targets, 8dp grid, compact width < 600dp. Everything in section 3 applies. [V] as cited above.

### 6.2 Foldables and tablets
- [V] States: `FLAT`, `HALF_OPENED`; half-opened with horizontal fold = tabletop posture, vertical fold = book posture.
  `FoldingFeature` exposes `state`, `orientation`, `occlusionType` (`FULL` on dual-screen hinges), `isSeparating`,
  `bounds`; the hinge angle is **not** exposed. Compose: `collectFoldingFeaturesAsState()` (Jetpack WindowManager).
  Extra modes: rear display mode, dual-screen mode. (src: /develop/ui/compose/layouts/adaptive/foldables/learn-about-foldables), (src: .../make-your-app-fold-aware)
- [V] Rec: do not place dialogs, menus or controls over the fold; split content top/bottom (tabletop) or left/right
  (book); widen the gutter of a two-pane layout for the hinge; trifolds have several hinges; cover screens are compact
  and may be square - keep them focused, edge-to-edge and clear of cutouts. "Your app doesn't have to specifically
  account for every posture." (src: /design/ui/mobile/guides/layout-and-content/postures-and-orientation)
- [V] Inner displays: square 1:1 (medium or expanded) and wide 4:3 (expanded in landscape). Emulators "Foldable (1:1
  inner display)" and "Foldable (4:3 inner display)".
- [V] Rec: "Don't lock apps to portrait. Doing so can look like a bug"; landscape phones are medium width with compact
  height, so two panes are not practical there. If content did not scroll in portrait, do not make it scroll in
  landscape.
- Biggest mistakes [Syn from Tier 2/3]: orientation lock and letterboxing; stretched single column, full-width buttons,
  sheets and text fields; bottom navigation bar at expanded width; state lost on fold/unfold or resize; camera preview
  stretched; `isTablet` logic instead of window size classes.

### 6.3 Desktop windowing, ChromeOS, Googlebook, connected displays
- [V] Free-form windows; each has a system header (caption) bar with minimize/maximize/close, customisable in the
  middle (`APPEARANCE_TRANSPARENT_CAPTION_BAR_BACKGROUND`, `WindowInsets.captionBar`, `WindowInsets.isCaptionBarVisible`);
  a taskbar shows app icons and App Shortcuts. (src: /design/ui/desktop/guides/system/system-bars), (src: /develop/ui/compose/layouts/adaptive/support-desktop-windowing)
- [V] Rec principles: adaptive from the start; denser layout instead of scaled-up elements; shorter/faster small
  transitions, slower large ones; multitasking and multi-instance (Alt+Tab switches windows); touch, pointer and
  keyboard "are equally important". (src: /design/ui/desktop/guides/foundations/design-principles)
- [V] Rec pointer: everything reachable by primary click; context menus on secondary click instead of long-press;
  hover states and tooltips; drag starts immediately (no long-press); "Targets should have more precise sizing".
  (src: /design/ui/desktop/guides/interaction/pointer-interactions)
- Quality: Tier 2 keyboard/mouse items and Tier 1 Desktop items in section 5.2.
- Biggest mistakes [Syn]: long-press-only actions; no hover or focus states; Esc and Enter doing nothing; content under
  the caption bar; assuming a fixed window size; one window only for document-style apps.

### 6.4 Wear OS
- [V] Principles: design for critical tasks done "within seconds"; do not port the whole phone app; choose the right
  surface (complication, notification, tile, widget, app). Navigation "should be shallow - avoid a design deeper than
  two levels - and linear". Dark theme only. Swipe to dismiss goes up the back stack. `android.webkit` is not
  supported. (src: /training/wearables/principles), (src: /training/wearables/wear-v-mobile)
- [V] Inputs: touch, rotary (crown/bezel), at least one hardware button (power), optional multifunction buttons, voice
  and IME via Remote Input (dictation, emoji, canned responses), Wear OS 7 one-handed gestures (primary action =
  double pinch, dismiss = wrist turn on Pixel Watch; "isn't designed to enable full watch navigation").
- [V] Design system: "Material 3 Expressive is the latest design system for ... the watch"; Roboto Flex; dynamic colour
  theming from seed colours for apps that opt in; "Wear OS uses only the dark theme"; build from a black background.
  (src: /design/ui/wear/guides/get-started), (src: /design/ui/wear/guides/styles/color/system)
- [V] Layout numbers: design small first (204-216dp emulator, check dense layouts at 192dp and with large fonts);
  breakpoint at 225dp (192-224dp vs 225-240+dp); outer margins in **percentages**, spacing between elements in fixed
  dp; a larger screen must never show less than a smaller one. (src: /design/ui/wear/guides/foundations/adaptive-design)
- [V] Typography: user font size steps of +/-6%; styles of 20sp and up do not scale; min 12sp essential, 10sp
  non-essential (`WO-V14`). (src: /design/ui/wear/guides/styles/typography/type-scale-tokens)
- [V] Compose: `androidx.wear.compose:compose-material3`, `compose-foundation`, `compose-navigation` (use instead of
  `navigation-compose`); `AppScaffold`, `ScreenScaffold` (computes percentage padding), `TransformingLazyColumn`,
  `SwipeDismissableNavHost`, `EdgeButton`, `TimeText`. Do not mix M2.5 and M3 long-term; Horologist composables are no
  longer recommended. Tiles use ProtoLayout (not Compose) and cannot scroll; newer "Wear Widgets" use Glance and Remote
  Compose (small 2x1, large 2x2). (src: /training/wearables/compose/migrate-to-material3), (src: /training/wearables/tiles), (src: /training/wearables/widgets)
- [V] Rec app practices: vertical scrolling only; show the time at the top; inline entry points with icon and label;
  primary action near the top; show the scroll indicator only on scrolling screens.
  (src: /design/ui/wear/guides/surfaces/apps/best-practices)
- Does not apply [V/Syn]: light theme, navigation bar/rail/drawer, multi-window, sign-in by typing credentials.
- Biggest mistakes [Syn]: porting phone screens and deep hierarchies; fixed-dp outer margins that clip on round
  screens; no swipe-to-dismiss; no rotary support; coloured or light backgrounds.

### 6.5 Android TV / Google TV
- [V] Inputs: D-pad (up/down/left/right), select, Home, Back, microphone; game controllers. No touchscreen assumed
  (Tier 1 optionally adds pointer remotes). Focus is "the key state definition for TV design"; exactly one focused
  element; indicators: scale (defaults 1.025, 1.05, 1.1x), border, glow (2-32dp), colour.
  (src: /design/ui/tv/guides/foundations/navigation-on-tv), (src: /design/ui/tv/guides/styles/focus-system)
- [V] Back: goes to the previous destination and ultimately to the launcher; with top navigation, Back returns focus to
  the top menu; with left navigation, it opens the side menu. "Don't display a back button." No exit confirmation
  ("avoid exit gating").
- [V] Layout: 16:9; design at 960x540 dp (MDPI, 1px = 1dp), assets for 1080p; 12-column grid, 52dp columns, 20dp
  gutters, 58dp side margins; overscan about 5%. The page gives both 48dp/27dp and 58dp/28dp for the safe margin
  (internal inconsistency) and notes "Most modern TVs no longer have overscan issues". Backgrounds fill the full
  screen. (src: /design/ui/tv/guides/styles/layouts)
- [V] Colour/type: "Build from dark themes"; no user-generated dynamic colour - use content-based schemes instead;
  design in sRGB for Standard picture mode; watch for gradient banding; larger type, Roboto default, 15-style type
  scale. (src: /design/ui/tv/guides/styles/color-system), (src: /design/ui/tv/guides/styles/typography)
- [V] Text input: Gboard on-screen keyboard with speech-to-text; limited input types. Multitasking: PiP only
  (Android 14 APIs). (src: /training/tv/get-started/onscreen-keyboard), (src: /training/tv/get-started/multitasking)
- [V] Compose for TV (`androidx.tv.material3`) is the recommended toolkit, works from API 21; Leanback "is deprecated"
  and based on "Material 1". Components in the design docs: buttons, cards, featured carousel, immersive list, lists,
  navigation drawer, tabs.
- Does not apply [Syn]: touch targets, bottom navigation bar, FAB, swipe gestures, portrait, on-screen Up/Back.
- Biggest mistakes [Syn from Tier 3]: unreachable or invisible focus; touch-only widgets; portrait or letterboxed
  layout; small text; launching a browser; on-screen back button.

### 6.6 Android Auto and Android Automotive OS
- [V] Android Auto projects from a phone (Android 9+); Android Automotive OS is built into the car. Only supported
  categories: media, messaging/calling, navigation, POI, IoT, weather (driving); video, games, browsers (parked).
  (src: /training/cars)
- [V] Driving apps are **templated**: the app supplies models, the host renders. Templates: List, Grid, Sectioned
  Item, Pane, Message, Long Message, Search, Sign-in, Tab; Navigation, Place List (map), Map + Content, Media
  Playback. `CarAppService` -> `Session` -> `Screen` stack; "the app can only push up to five templates to the screen
  stack". (src: /design/ui/cars/guides/templates/overview), (src: /training/cars/apps)
- [V] UX requirements use MUST / SHOULD / MAY ("MUST = required, enforced either in the API or in Android app quality
  for cars"). MUST keep task flows to 5 steps or fewer; SHOULD keep them to 2-3; SHOULD provide a back/exit where no
  other action exists; MUST NOT let users set up payment methods; SHOULD NOT use stateful buttons outside list rows;
  images, icons and map markers SHOULD be at least 36x36dp; map text SHOULD be 24dp or larger.
  (src: /design/ui/cars/guides/ux-requirements/overview)
- [V] Principles: driving first; robust voice; pause and resume; tasks as short as possible (common tasks in three taps
  or less); text while driving 1-3 lines and 120 characters. (src: /design/ui/cars/guides/foundations/design-principles)
- [V] Parked apps (video, games, browsers) are ordinary large-screen activities ("Car ready mobile apps" programme on
  AAOS) and must not be usable while driving.
- Does not apply [Syn]: custom Compose/Views UI while driving, Material theming beyond what templates expose, free
  navigation depth, animation, arbitrary images.
- Biggest mistakes [Syn]: assuming you can draw your own driving UI; flows longer than five screens; relying on the
  phone screen; ads or irrelevant notifications.

### 6.7 Android XR
- [V] Two modes. **Home Space**: apps side by side; any compatible mobile or large-screen app runs unmodified; default
  window 1024x720dp, min 385x595dp, max 2560x1800dp, launched 1.75 m away; no spatial panels or 3D. **Full Space**:
  one app, spatial panels, orbiters, 3D models, environments, spatial audio. Rec: give clear controls to switch.
  (src: /design/ui/xr/guides/foundations)
- [V] Inputs: hand tracking (pinch = tap, pinch-and-hold = scroll/move/resize), eye tracking, voice, Bluetooth
  keyboard and mouse, controllers. System gesture menu offers Go back and Launcher. Hover states matter; with eye
  tracking the system draws the highlight and the app cannot read hover.
- [V] Spatial UI (marked "Preview", Full Space only): spatial panels (no minimum, max 2560x1800dp, 32dp corners by
  default); panel depth 0.75 m to 5 m; spawn 1.75 m away, centre 5 degrees below eye level, keep content within the
  central 41 degrees; 0.868 dp-to-dmm. Orbiters: use sparingly, 20dp offset, do not overlap more than 50%. Spatial
  elevation levels: Orbiter 16dp, SpatialPopup 32dp, SpatialDialog 56dp (the orbiter text says 15dp; inconsistent).
  (src: /design/ui/xr/guides/spatial-ui)
- [V] Targets: "your target sizes meet the minimum, though 56dp is optimal"; recommended target 56x56dp, visual 48x48dp.
  Text: 14dp or larger (the page writes dp, not sp), weight normal or heavier. Dark and light themes both supported;
  on see-through glasses dark pixels look transparent. (src: /design/ui/xr/guides/visual-design)
- [V] APIs: `androidx.xr.compose` (`Subspace`, `SpatialPanel`, `Orbiter`, `SpatialDialog`, `SpatialPopup`,
  `SpatialRow`, `SpatialBox`); Material 3 for XR (`androidx.xr.compose.material3`: `SpatialNavigationRail`,
  `SpaceToggleButton`, ...) is experimental behind `@OptIn(ExperimentalMaterial3XrApi::class)`; check
  `LocalSpatialCapabilities.current.isSpatialUiEnabled` and fall back to normal M3. Glasses use Jetpack Compose
  Glimmer (alpha). (src: /develop/xr/jetpack-xr-sdk/material-design)
- Biggest mistakes [Syn]: ignoring Home Space resizing; small targets and thin text; overusing orbiters; assuming
  spatial capabilities are always present; motion that causes discomfort.

## 7. Deliverable 1: universal versus form-factor matrix

Cells are [V] where the fact appears above with a source; "n/s" = not stated in the pages I read; [Syn] = inference.

| Concern | Phone | Foldable / tablet | Desktop / ChromeOS / Googlebook | Wear OS | TV | Auto / AAOS (driving) | XR |
|---------|-------|-------------------|---------------------------------|---------|----|-----------------------|----|
| Primary navigation | Navigation bar (3-5) or modal drawer | Navigation rail from medium/expanded width; `NavigationSuiteScaffold` switches | Rail expanding to a full navigation panel; app content may enter the window header bar | Shallow (max two levels), linear, inline; no bar/rail [Syn] | Tabs (top) or navigation drawer (left) | `Tab` template; screen stack max 5 | Home Space: as large screen. Full Space: rail/bar in an `Orbiter` |
| Back | System gesture or 3-button; predictive back; Up = Back within the task | Same | Same plus Esc (`Keyboard_Exit`) | Swipe to dismiss (`WO-V3`); hardware/wrist-turn dismiss | Remote Back; no on-screen back; must reach launcher (`TV-DB`) | Host header back; pop `Screen` | System gesture menu "Go back" |
| Modality | Dialogs, bottom sheets | Sheets with max width or side sheet; small modals keep context | Desktop-style menus, context menus on right-click, small modals | Full-screen dialogs/confirmations [n/s in detail] | n/s (focus-trapped overlays [Syn]) | Message / Long Message templates | `SpatialDialog`, `SpatialPopup` (elevated) |
| Text input | Soft keyboard; handle IME insets | Plus hardware keyboard and stylus handwriting (Android 14+) | Hardware keyboard first; shortcuts | Remote Input: voice, emoji, canned, small IME; no credential entry (`WO-P6`) | Gboard with voice; voice search (Tier 2) | Search template; voice | Voice dictation, Bluetooth keyboard |
| Minimum target | 48dp (touch) | 48dp | 48dp touch; pointer 44dp (M3 "consider"); precise cursor targets | 48x48dp (`WO-V2`) | Focus based; no touch target | Host-rendered; images/icons >= 36x36dp (SHOULD) | 56dp recommended, 48dp visual |
| Typography units | sp; test 200% non-linear scaling | sp | sp | sp; styles >= 20sp do not scale; min 12sp / 10sp | dp/sp at 960x540 design size; large type | Host-rendered; 1-3 lines, 120 chars | dp-to-dmm 0.868; text >= 14dp |
| Dark theme | Light and dark (`Theme_Support`) | Same | Same | Dark only, black background (`WO-V13`) | Dark recommended ("build from dark themes") | Light and dark required for custom theming, library 1.9+ (`TH-1`) | Light and dark, user switch |
| Dynamic colour | Android 12+ with static fallback | Same | Same [Syn] | Seed-based dynamic theming for opted-in apps | Not user-generated; content-based schemes | n/a (host) | n/s |
| Multi-window | Split screen (Android 7+), PiP | Standard on large screens (Android 12+); multi-resume | Free-form windows, multi-instance, drag and drop | n/a | PiP only | n/a | Home Space side by side; Full Space single app |
| Orientation | Both recommended; lock still honoured below sw600dp | Locks ignored at targetSdk 36+ (sw >= 600dp) | Arbitrary window sizes | Round/square, fixed | Landscape only (`TV-LO`) | Car display, host | n/a |
| Edge-to-edge / safe area | Enforced at targetSdk 35/36 | Same, plus hinge | Plus caption bar inset | Round-screen percentage margins | Overscan about 5% | `AR-1` for own activities | Panel bounds |
| Universal across all | dp/sp units, state preservation, contrast, labels for assistive tech, Material-first components, target API rules | | | | | | |

## 8. Deliverable 2: detection procedure for a codebase

Run from the repository root. All artifact, manifest and theme names below were confirmed in the cited pages [V].

```bash
# 1. Modules and SDK levels (Gradle Kotlin/Groovy DSL and version catalog)
rg -n --glob '*.gradle*' -e 'compileSdk(Version)?\b' -e 'minSdk(Version)?\b' -e 'targetSdk(Version)?\b' -e 'compileSdkPreview'
rg -n -e 'compileSdk|minSdk|targetSdk' gradle/libs.versions.toml build-logic buildSrc 2>/dev/null   # convention plugins
rg -n 'android:(min|target)SdkVersion' --glob 'AndroidManifest.xml'                                 # legacy

# 2. Compose versus Views
rg -n --glob '*.gradle*' -e 'org\.jetbrains\.kotlin\.plugin\.compose' -e 'buildFeatures' -e 'compose\s*=?\s*true' -e 'viewBinding|dataBinding'
rg -l '@Composable' --glob '*.kt' | wc -l ; fd -e xml . --full-path -g '**/res/layout*/*.xml' | wc -l
rg -n 'ComposeView|AndroidView\(|setContent\s*\{' --glob '*.kt' | head       # interop

# 3. Design system and versions (also check libs.versions.toml aliases)
rg -n -e 'androidx\.compose:compose-bom' -e 'androidx\.compose\.material3:material3' \
      -e 'androidx\.compose\.material:material\b' -e 'com\.google\.android\.material:material' \
      -e 'androidx\.compose\.material3\.adaptive' -e 'material3-adaptive-navigation-suite' \
      -e 'material3-window-size-class' -e 'androidx\.window:window' --glob '*.gradle*' --glob '*.toml'
rg -n 'parent="Theme\.(Material3Expressive|Material3|MaterialComponents|AppCompat)[A-Za-z.]*"' --glob '*.xml'
rg -n -e 'import androidx\.compose\.material3\.' -e 'import androidx\.compose\.material\.[A-Z]' --glob '*.kt' | cut -d: -f3 | sort | uniq -c | sort -rn | head
rg -n -e 'materialExpressTheme|MaterialExpressiveTheme|expressiveLightColorScheme|MotionScheme\.expressive|ExperimentalMaterial3ExpressiveApi|Material3ExpressiveApi' \
      -e 'ButtonGroup|SplitButton|FloatingToolbar|LoadingIndicator|MaterialShapes|WavyLinearProgressIndicator' --glob '*.kt'

# 4. Form factors
rg -n -e 'android\.hardware\.type\.watch' -e 'com\.google\.android\.wearable\.standalone' \
      -e 'android\.intent\.category\.LEANBACK_LAUNCHER' -e 'android\.software\.leanback' -e 'android:banner' \
      -e 'android\.hardware\.touchscreen' -e 'android\.hardware\.type\.automotive' \
      -e 'com\.google\.android\.gms\.car\.application' -e 'androidx\.car\.app\.(CarAppService|category\.[A-Z]+|minCarApiLevel)' \
      -e 'android\.software\.xr\.api\.(spatial|openxr)' -e 'PROPERTY_XR_ACTIVITY_START_MODE' --glob 'AndroidManifest.xml'
rg -n '<automotiveApp|<uses name=' --glob '*automotive_app_desc*.xml'
rg -n -e 'androidx\.wear\.compose:compose-(material3|material|foundation|navigation)' -e 'androidx\.wear\.tiles' \
      -e 'androidx\.wear\.protolayout' -e 'androidx\.tv:tv-(material|foundation)' -e 'androidx\.leanback' \
      -e 'androidx\.car\.app:app(-projected|-automotive)?' -e 'androidx\.xr\.(compose|scenecore|glimmer)' \
      -e 'androidx\.glance:glance' --glob '*.gradle*' --glob '*.toml'

# 5. Behaviours tied to targetSdk
rg -n -e 'windowOptOutEdgeToEdgeEnforcement' -e 'enableEdgeToEdge' -e 'statusBarColor|navigationBarColor' \
      -e 'enableOnBackInvokedCallback' -e 'onBackPressed\(' -e 'KEYCODE_BACK' \
      -e 'screenOrientation|resizeableActivity|(min|max)AspectRatio|setRequestedOrientation' \
      -e 'PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY' -e 'layoutInDisplayCutoutMode' .
```

Interpretation table:

| Signal | Conclusion | Source of the name |
|--------|------------|--------------------|
| `<uses-feature android:name="android.hardware.type.watch"/>` | Wear OS module; `com.google.android.wearable.standalone` meta-data tells standalone or not | [V] (src: /training/wearables/packaging) |
| `category android:name="android.intent.category.LEANBACK_LAUNCHER"`, `android.software.leanback`, `android.hardware.touchscreen` `required="false"`, `android:banner` | TV app (leanback `required="false"` = shared phone+TV APK) | [V] (src: /training/tv/get-started/create) |
| service with action `androidx.car.app.CarAppService` and `androidx.car.app.category.{NAVIGATION,POI,IOT,WEATHER,MEDIA,MESSAGING,CALLING}` | Car App Library (templated) app | [V] (src: /training/cars/apps) |
| meta-data `com.google.android.gms.car.application` -> `@xml/automotive_app_desc` with `<uses name="template"/>` (or media/notification) | Android Auto | [V] (src: /training/cars/apps/auto) |
| `<uses-feature android:name="android.hardware.type.automotive"/>`; artifact `app-automotive` | Android Automotive OS (the docs say not to include the gms.car meta-data there; `app-automotive` provides `CarAppActivity`). `app-projected` = Android Auto is my reading of the artifact name | [V] (src: /training/cars/apps/automotive-os); mapping of `app-projected` [M] |
| `android.software.xr.api.spatial` / `.openxr`; property `android.window.PROPERTY_XR_ACTIVITY_START_MODE` | Android XR (Jetpack XR SDK / OpenXR engines) | [V] (src: /develop/xr/package-and-distribute), (src: /develop/xr/jetpack-xr-sdk/transition-home-space-to-full-space) |
| No form-factor feature, `material3-adaptive*` or `androidx.window` present | Phone app with adaptive (tablet/foldable/desktop) support | [Syn] |
| `androidx.compose.material3:material3` | Compose Material 3; version from BOM mapping if no explicit version; >= 1.5.0 means stable Expressive components available | [V] section 1 |
| `androidx.compose.material:material` without material3 | Compose Material 2 (migration guide: /develop/ui/compose/designsystems/material2-material3) | [V] |
| `com.google.android.material:material` + `Theme.Material3.*` / `Theme.Material3.DynamicColors.*` | Views Material 3 | [V] raw.githubusercontent.com/material-components/material-components-android/master/docs/getting-started.md, theming/Color.md |
| `Theme.Material3Expressive.*` | Views M3 Expressive themes | [V] same docs |
| `Theme.MaterialComponents.*` | Views Material 2; `Theme.AppCompat.*` = pre-Material-Components | [V] same docs, (src: /develop/ui/views/theming/darktheme) |
| `androidx.wear.compose:compose-material3` vs `compose-material` | Wear M3 (Expressive) vs Wear M2.5 | [V] migrate-to-material3 |
| `androidx.tv:tv-material` vs `androidx.leanback` | Compose for TV vs deprecated Leanback | [V] |
| targetSdk >= 35 | Edge-to-edge enforced (35: opt-out possible; 36: opt-out disabled on Android 16) | [V] |
| targetSdk >= 36 | Predictive back on by default; orientation/resizability locks ignored at sw >= 600dp (opt-out property until 37) | [V] |
| targetSdk below the Play floor for its form factor | Flag as a publishing blocker (36 phone; 35 Wear/AAOS; 34 TV/XR) | [V] |

Caveats [Syn]: SDK levels often live in convention plugins (`build-logic/`, `buildSrc/`) or `gradle.properties`;
BOM-managed artifacts have no version in the build file (look up the BOM mapping page); multi-module apps can mix
Material 2 and 3; KMP projects put Android config under `androidMain`.

## 9. Deliverable 3: cross-form-factor adaptation checklists

Each item is backed by a cited rule above; the grouping is mine [Syn].

**Phone -> tablet / foldable**
1. Remove orientation, aspect-ratio and resizability restrictions; confirm no letterboxing (`Config_Changes`).
2. Drive layout from `WindowSizeClass` (width first, then height), never from device type.
3. Swap navigation bar for rail at medium/expanded (`NavigationSuiteScaffold`); keep bar when height is compact.
4. Move to canonical layouts (list-detail, supporting pane, feed) with `ListDetailPaneScaffold` and friends.
5. Cap widths: sheets, buttons, text fields, dialogs; convert bottom sheet to side sheet where suitable.
6. Preserve scroll position, typed text and playback across rotate, fold/unfold, resize; test combinations.
7. Keep content and controls off the hinge; consider tabletop/book layouts for media and reading.
8. Per-pane status-bar protection; insets for cutouts in landscape.
9. Basic keyboard, mouse, trackpad and stylus support (Tier 3); 48dp targets remain.

**-> Desktop windowing / ChromeOS / Googlebook**
1. Everything above, plus arbitrary window sizes including very small and extra-large (opt in to Large/XL classes).
2. Handle `captionBar` insets; optionally draw into the header bar.
3. Keyboard: Tab/arrow traversal, visible focus, shortcuts (copy/paste/undo), Esc exits, Enter sends, Space plays.
4. Pointer: hover states, right-click context menus, scroll-wheel/Ctrl-zoom, immediate drag, scrollbars, cursors.
5. Density: show more information instead of scaling up; shorter flows.
6. Multi-instance, drag and drop between windows, file picker and file handlers, printing (Tier 1).

**-> Wear OS**
1. Pick 1-3 critical tasks; decide surface (complication, tile/widget, notification, app).
2. Rebuild with Wear Compose Material 3: `AppScaffold`/`ScreenScaffold`, `TransformingLazyColumn`, `EdgeButton`, `TimeText`.
3. Vertical-only scrolling, two levels deep at most, swipe-to-dismiss everywhere, rotary scrolling, scroll indicator.
4. Black background, dark only, percentage outer margins, 225dp breakpoint, test at 192dp and largest font.
5. 48dp targets; min 12sp; no typed credentials - use phone/Google sign-in; ongoing activity for long tasks.
6. Same package name and signing key as the phone app; declare `android.hardware.type.watch`.

**-> Android TV**
1. Add the leanback launcher activity, banner, touchscreen not required; landscape only.
2. Rebuild navigation for D-pad: every element focusable, one focus at a time, predictable directions, strong focus
   indicator; top tabs or left drawer; Back to launcher without confirmation; no on-screen back.
3. 10-foot layout: 960x540dp canvas, 12-column grid, about 5% overscan margin, large type, dark-first palette.
4. Media keys and D-pad centre play/pause; voice search; sign-in via phone or Google account.
5. Use Compose for TV (`androidx.tv.material3`); do not start new work on Leanback; never open a browser.

**-> Android Auto / Automotive OS**
1. Confirm the app fits a supported category; otherwise only parked (video, games, browser) distribution applies.
2. Driving UI: Car App Library templates only; flows of 5 steps or fewer (aim for 2-3); voice entry points.
3. No animation, auto-scrolling text or decorative images; short text; light and dark variants; contrast rules.
4. Notifications only when relevant to driving; no ads; no payment set-up.
5. Parked apps: meet adaptive Tier 3, block use while driving, avoid system-bar/cutout obstruction (`AR-1`).

**-> Android XR**
1. First make the app a good large-screen adaptive app; it then runs in Home Space unchanged (385x595 to 2560x1800dp).
2. Add a Home Space / Full Space toggle; check `isSpatialUiEnabled` and keep the 2D fallback.
3. Split into spatial panels; move navigation and toolbars to orbiters (few, 20dp offset); use spatial dialogs.
4. Targets 56dp, hover and focus states, text >= 14dp at normal weight or heavier, test contrast on passthrough.
5. Keep panels 0.75-5 m, default 1.75 m, slightly below eye level; avoid motion that causes discomfort.

## 10. Deliverable 4: requirements versus recommendations

| # | Statement | Class | Source |
|---|-----------|-------|--------|
| 1 | Target API level floors for Play submission (section 1) | **Req - Google Play** | /google/play/requirements/target-sdk |
| 2 | Android App Bundles for new apps (all), and for all TV apps | Req - Google Play | core `App_Bundles`, `TV-G1` |
| 3 | No notifications for cross-promotion/advertising | Req - Play policy as quoted by core quality | core `Notification_Quality` |
| 4 | Edge-to-edge at targetSdk 35 (opt-out) and 36 (no opt-out on Android 16) | **Req - platform behaviour** | behaviour-changes-15/16 |
| 5 | Predictive back default, `onBackPressed`/`KEYCODE_BACK` not delivered at targetSdk 36 | Req - platform behaviour | behaviour-changes-16 |
| 6 | Orientation/aspect/resizability ignored at sw >= 600dp for targetSdk 36; no opt-out at 37 | Req - platform behaviour | behaviour-changes-16/17 |
| 7 | Cutout mode forced to ALWAYS for non-floating windows (targetSdk 35) | Req - platform behaviour | behaviour-changes-15 |
| 8 | Notification channel required (API 26+); `POST_NOTIFICATIONS` runtime permission (API 33+) | Req - API contract | notifications pages |
| 9 | Runtime permission request for dangerous permissions (API 23+) | Req - API contract | /training/permissions/requesting |
| 10 | Splash icon sizes and formats; adaptive icon layer sizes | Req - API/asset contract ("must") | splash-screen, icon_design_adaptive |
| 11 | Wear OS quality `WO-*` items | **Req for Play publishing of watch apps** ("must satisfy all the applicable requirements") | wear-app-quality |
| 12 | TV Tier 3 "TV Ready" items | Req to qualify as a TV app ("fundamental requirements") | tv-app-quality |
| 13 | Car Tier 3 (parked) and Tier 2 (driving) items; templated MUST items | Req for acceptance on Play for cars | car-app-quality, cars ux-requirements |
| 14 | Adaptive Tier 3 "Adaptive ready" | "Baseline quality standard for apps on foldables and large screens on Google Play"; consequence stated is reduced discoverability, not rejection | adaptive-app-quality, dos-and-donts |
| 15 | Adaptive Tier 2 / Tier 1 | Optional; qualifies for badging and promotion | adaptive-app-quality |
| 16 | Core app quality items (48dp targets, contrast, light and dark, back navigation, content descriptions ...) | Quality guideline: "minimum quality that all apps should meet"; the page does not say Play rejects apps for them | core-app-quality |
| 17 | 48dp touch target | Rec in design and Material docs ("ensure", "consider"); listed in core quality; a hard "requirement" only on Wear (`WO-V2`) and widgets (`WL-4.2`) | section 4 |
| 18 | Contrast 4.5:1 / 3:1 | Rec ("we recommend") plus core quality item | section 4 |
| 19 | Navigation bar 3-5 destinations; rail on large screens; no bottom bar at large sizes | Rec | layout-and-nav-patterns |
| 20 | Up never exits the app; Up = Back in task | Principle ("should follow") | /guide/navigation/principles |
| 21 | Transparent gesture bar; no touch targets under gesture insets; draw behind system bars | Rec | system-bars, edge-to-edge |
| 22 | Do not lock to portrait | Rec on phones; platform-enforced on sw >= 600dp (row 6) | postures-and-orientation |
| 23 | Dynamic colour with static fallback; respect system dark/contrast settings | Rec | themes, color |
| 24 | sp for text, test at 200% | Rec ("always") | grids-and-units, Android 14 features |
| 25 | XR numbers (56dp, 1.75 m, 41 degrees, 20dp orbiter offset) | Rec | xr spatial-ui, visual-design |
| 26 | 8dp grid, margins, TV 12-column grid, Wear 225dp breakpoint | Rec / convention | cited pages |

## 11. Deliverable 5: Android-side column for an "Android versus Apple" porting table

Only the Android/Material side is filled, from the sources above. Apple column to be completed from the apple-hig skill.

| Topic | Android / Material (verified) | Apple |
|-------|-------------------------------|-------|
| Top-level navigation | Navigation bar at the bottom for 3-5 destinations (compact); navigation rail at medium/expanded; modal drawer for more destinations | (apple-hig) |
| Back | System-wide Back (edge swipe from either side, or 3-button) handled by the OS; predictive back previews the destination; app bar Up arrow behaves like Back inside the task and never exits the app; no custom on-screen back prompts (`Back_Button_Nav`) | |
| Exit | Back from the start destination leaves the app | |
| Primary action | FAB (one per screen) or prominent button; secondary actions in the top app bar, rest in overflow menu | |
| Buttons | Material button hierarchy; do not stretch full width on large screens | |
| Sheets | Bottom sheet on compact; max width or side sheet on larger windows; dismissible with Back (predictive animation in MDC 1.10+/Compose M3) | |
| Dialogs / menus | Dialogs; context menu by long-press on touch and right-click with a pointer; menus anchored next to the item | |
| Tabs | Secondary navigation inside a destination, not app-level | |
| Search | Material search bar / `AppBarWithSearch` (experimental in 1.5.0) | |
| Typography units | sp for text, dp for layout; user font scale up to 200%, non-linear from Android 14 | |
| Minimum target | 48dp touch (Material notes "iOS recommends 44 x 44"), 44dp pointer | |
| System UI | Status bar and navigation bar drawn over the app (edge-to-edge enforced); handle insets, cutouts, gesture areas; caption bar in desktop windowing | |
| Colour | Dynamic colour from wallpaper (Android 12+) with static fallback; light and dark schemes; tonal surfaces | |
| App icon | Adaptive icon (foreground, background, monochrome) masked by the launcher; themed icons | |
| Launch | System splash screen from the app icon (Android 12+) | |
| Settings | In-app "Settings" screen reached from overflow/top bar; do not duplicate system settings | |
| Notifications | Channels (user-controllable categories), runtime permission from Android 13 | |
| Sharing / photos | System Sharesheet; system photo picker without storage permission | |
| Large screens | Window size classes (600/840/1200/1600dp), canonical layouts, no orientation lock | |
| Watch | Wear OS: black background, swipe-to-dismiss, tiles and complications, rotary input | |
| TV | D-pad focus, no on-screen back, Compose for TV | |
| Car | Templates rendered by the host; category-restricted | |
| Headset | Home Space / Full Space, spatial panels, orbiters | |

## 12. Deliverable 6: proposed reference files (mirrors `apple-hig/references/platforms-*.md`)

| File | Outline |
|------|---------|
| `platforms-detection.md` | Section 8 commands and interpretation table; version table from section 1 with "verify online" note; universal-versus-form-factor matrix (section 7); targetSdk behaviour table |
| `platforms-phone.md` | Navigation and back; system bars, edge-to-edge and insets; cutouts; predictive back; app surfaces (notifications, share, photo picker, permissions, splash, icons, settings); numbers table |
| `platforms-large-screens.md` | Window size classes; canonical layouts and panes; navigation suite; foldable postures and hinge; orientation/resizability rules by targetSdk; adaptive quality tiers 3/2/1 with IDs |
| `platforms-desktop.md` | Desktop windowing, caption bar, taskbar; keyboard, pointer, hover, context menus; multi-instance, drag and drop, files; ChromeOS and Googlebook notes; Tier 1 desktop IDs |
| `platforms-wear.md` | Principles and surfaces; Wear Compose M3 components; round-screen layout numbers; typography scaling; inputs (rotary, buttons, gestures); `WO-*` requirements |
| `platforms-tv.md` | Focus system; D-pad and Back rules; 960x540 grid and overscan; colour and type; Compose for TV versus Leanback; `TV-*` tiers |
| `platforms-auto.md` | Android Auto versus AAOS; categories; templates and 5-step rule; MUST/SHOULD table; parked apps; `car-app-quality` IDs |
| `platforms-xr.md` | Home versus Full Space; panels, orbiters, elevation; targets and type; APIs and experimental status; glasses and Glimmer pointer |
| `platforms-adaptation.md` | Section 9 checklists; "what does not carry over" lists; biggest mistakes per target; Android-versus-Apple table (section 11) |
| `quality-requirements.md` (or inside review guide) | Section 10 table; core quality ID list; how to phrase findings ("Play requirement", "platform behaviour at targetSdk N", "quality guideline", "recommendation") |

## 13. Stale lore, contradictions, and what I could not verify

**Lore that is now wrong or outdated** (all [V]):
- "Large screen app quality, LS-* IDs" -> replaced in 2026 by **Adaptive app quality** with named IDs; tiers are now
  "Adaptive ready / optimized / differentiated".
- Core quality coded IDs (`VD-1`, `FN-*`, `UX-*`) -> replaced by named IDs (`Touch_Target_Size`, ...).
- "Three window size classes" -> five width classes (Large >= 1200dp, Extra-large >= 1600dp are opt-in).
- "Set status bar / navigation bar colour" -> deprecated, no effect at targetSdk 35 on Android 15+.
- "Override `onBackPressed`" -> not called at targetSdk 36 on Android 16+.
- "Lock the app to portrait" -> ignored on sw >= 600dp at targetSdk 36; opt-out removed at 37.
- "M3 Expressive is experimental/alpha-only" -> most of it is stable in material3 1.5.0 (Nov 2026).
- "Use Leanback for TV" -> deprecated; "Horologist/Wear Material 2.5 for watches" -> Wear Compose Material 3.
- "Wear tiles are the only glanceable surface" -> Wear Widgets (Glance + Remote Compose) are being introduced.
- "Navigation drawer on tablets" -> Tier 2 says drawers "are updated to expanded navigation rails".

**Contradictions inside Google's own pages**:
- Wear quality page target API (34, Aug 2025) versus target-sdk page (35 for Wear from Aug 2026).
- BOM how-to snippet (2026.09.00) versus mapping page (2026.11.01); "wear-compose-m3" release page (1.5.0) versus
  wear-compose group (1.7.2).
- TV overscan margin 48dp/27dp versus 58dp/28dp on the same page; XR orbiter elevation 15dp (text) versus 16dp (table).
- Contrast thresholds in sp (accessibility guide) versus pt (core quality); XR text size given in dp.
- Android 16 page says sw ">= 600dp"; Android 17 change page says "greater than 600dp".
- Mobile design page says 3 size classes; developer page says 5.

**Not verified in this workstream** (do not state as fact without checking):
- Whether Android 17 is formally final (see section 1); API for the system contrast setting; the exact name of the Compose expressive theme function (release notes
  write `materialExpressTheme` and `expressiveLightColorScheme`; check the API file); exact TV type-scale sizes; Wear dialog/modality rules; XR quality guideline contents;
  the Android Auto `app-projected` mapping; contents of the `github.com/android/skills` repository; Google Play Console
  help pages (support.google.com was not fetched); Material Web/Flutter.
