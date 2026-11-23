# 05 - Evaluation assets and ecosystem check for `material-design`

Research agent M5, 2026-11-23. Every row of the facts table is [V]: fetched in this session (m3.material.io through the
render helper, developer.android.com and raw.githubusercontent.com through curl). Anything from memory is marked [M].

## Summary

- Part A holds 40 trigger queries, 16 task scenarios and 5 fixtures. All JSON blocks parse, and the fixtures are bracket-balanced (the XML is well-formed).
- Every assertion that states a number or an API fact rests on a row of the facts table. Nothing was compiled; there is no Android toolchain here.
- Fixture paths assume `tests/evals/material-design/files/`. Change the prefix in `files` and in the prompts if the lead picks another layout.
- Part B: Google publishes official Android skills (`android/skills`, Apache-2.0), but none covers component choice, review or general Material guidance. The name `material-design` is already used by many third-party skills.

Findings that contradict common lore, and should shape the skill:

| Lore | What the sources say today | Fact |
|---|---|---|
| "Rail from 600dp up" | M3 allows a bar or a rail at medium width; `NavigationSuiteScaffold` defaults to a rail for everything that is not compact | F3, F5 |
| "A small clickable is untappable" | Compose expands the touch target by itself; the defect is that the layout does not reserve the space, so targets overlap | F7 |
| "`Divider` and `TabRow` are the M3 names" | Both are deprecated in material3; the official migration guide still maps M2 `Divider` to M3 `Divider` | F20 |
| "ModalBottomSheet is stable by now" | Still `@ExperimentalMaterial3Api` in 1.4.0-beta03, 1.5.0-beta01 and androidx-main | F22 |
| "Expressive components are experimental" | ToggleButton, SplitButton, ButtonGroup, FloatingToolbar and the wavy indicators are stable in 1.5.0; LoadingIndicator and MaterialShapes are not | F21, F22 |
| "Lock to portrait and tablets will letterbox" | Ignored on smallest width 600dp and up for apps targeting API 36; the opt-out goes away at API 37 | F29 |
| "Snackbars last 4 seconds" | Guidance is a 4 to 10 second range, depending on platform, for snackbars without actions | F14 |
| "Material Icons ship with material3" | Since 1.4.0 the library no longer depends on `material-icons-core`; Material Symbols as vector drawables are recommended (release notes) | F21 URL |
| "`value` / `onValueChange` text fields are the norm" | Deprecated in 1.6.0-alpha01 in favour of the `TextFieldState` overloads; still fine in 1.5.0 | F21 URL |

Could not verify: repository dates and stars for the third-party skills (the GitHub repository API is blocked here; only
code search and raw files work), skills.sh (blocked), and exact API annotations in the final 1.5.0 artifact (the closest
published API file is `1.5.0-beta01.txt`; the 1.5.0 release notes agree with it for every API used here).

## Part A - eval assets

### A1. Facts the assertions rely on

| ID | Fact | Strength | URL | Quoted phrase or signature |
|---|---|---|---|---|
| F1 | Navigation bar holds three to five destinations | M3 rec. | https://m3.material.io/components/navigation-bar/guidelines | "Navigation bars provide access to three to five destinations." / "Avoid putting more than five navigation items in a navigation bar" |
| F2 | Navigation bar items keep their labels; labels are short. No character limit is published | M3 rec. | https://m3.material.io/components/navigation-bar/guidelines | "Don't remove the labels from navigation items" / "All navigation items require a label text. It should be 1-2 words." The string "charact" occurs 0 times on the guidelines, specs and accessibility tabs |
| F3 | Bar at compact, bar or rail at medium, rail at expanded and larger | M3 rec. | https://m3.material.io/components/navigation-bar/guidelines | "Only use navigation bars for compact and medium breakpoints." / "Medium: Use a navigation bar or navigation rail." / "Expanded and extra-large: Use a navigation rail instead." |
| F4 | Width breakpoints 600 / 840 / 1200 / 1600 dp; classes describe the window, not the device | API doc | https://developer.android.com/develop/ui/compose/layouts/adaptive/use-window-size-classes | "width < 600dp", "600dp ≤ width < 840dp", "840dp ≤ width < 1200dp"; "Window size classes categorize the display area available to your app". M3 page: "Under 600dp", "600-839dp", "840-1199dp" |
| F5 | NavigationSuiteScaffold switches bar and rail by window size class; separate artifact | API doc | https://developer.android.com/develop/ui/compose/layouts/adaptive/build-adaptive-navigation | "Navigation bar if the width or height is compact or if the device is in tabletop posture. Navigation rail for everything else"; `androidx.compose.material3:material3-adaptive-navigation-suite` |
| F6 | Touch target 48 x 48 dp | M3 rec.; Android quality guideline | https://m3.material.io/foundations/designing/structure | "For most platforms, consider making touch targets at least 48 x 48dp." Core app quality (https://developer.android.com/docs/quality-guidelines/core-app-quality): "Touch targets are at least 48 dp." |
| F7 | Compose expands small touch targets, but layout must still reserve the space | API doc | https://developer.android.com/develop/ui/compose/accessibility/api-defaults | "set the minimum size to 48dp" / "To prevent possible overlap between touch areas of different composables, always use a large enough minimum size" / minimumInteractiveComponentSize "reserves at least 48 dp of layout space in each dimension" |
| F8 | Text contrast 4.5:1 (small) and 3:1 (large text, graphics) | Android quality guideline; M3 | https://developer.android.com/docs/quality-guidelines/core-app-quality | "3:1 for large text and graphics" / "4.5:1 for small text (less than 18 pt or less than 14 pt if text is bold)" |
| F9 | contentDescription: text for meaningful graphics, null only for decorative ones | API doc | https://developer.android.com/develop/ui/compose/accessibility/api-defaults | "When you set the contentDescription parameter to null, you indicate to the Android framework that this element does not have associated actions or state." Quality test: "Verify that all UI elements other than TextView have content descriptions." |
| F10 | clickable takes an optional role and click label | API | https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/foundation/foundation/api/current.txt | `Modifier clickable(Modifier, optional boolean enabled, optional String? onClickLabel, optional Role? role, ...)`; semantics page: "The Role indicates the type of element." |
| F11 | Text sizes use sp, which follows the user's text size preference | Android rec. | https://developer.android.com/training/multiscreen/screendensities | "The sp unit is the same size as a dp, by default, but it resizes based on the user's preferred text size." / "When specifying text size, use sp" |
| F12 | Scaffold passes PaddingValues that the content should apply | API doc | https://developer.android.com/develop/ui/compose/components/scaffold | "It passes PaddingValues to the content lambda that you should apply to your content's root composable" |
| F13 | Dialogs for critical, blocking decisions; snackbars for low-priority messages | M3 rec. | https://m3.material.io/components/dialogs/guidelines | "Don't use dialogs for low- or medium-priority information. Instead use a snackbar, which can be dismissed or disappear automatically." |
| F14 | Snackbar: one optional action, Undo is the example; no single duration | M3 rec. | https://m3.material.io/components/snackbar/guidelines | "To allow users to amend choices, display an 'Undo' action" / "Snackbars without actions can auto-dismiss after 4-10 seconds, depending on platform." |
| F15 | Modal bottom sheet suits long lists of actions on mobile | M3 rec. | https://m3.material.io/components/bottom-sheets/guidelines | "Use a modal bottom sheet as an alternative to inline menus or simple dialogs on mobile, especially when offering a long list of action items" |
| F16 | Text fields need a label; error text replaces supporting text | M3 rec. | https://m3.material.io/components/text-fields/guidelines | "Every text field should have a label." / "replace supporting text with error text" |
| F17 | material3 text fields expose isError and supportingText; secure fields exist since 1.4.0 | API | https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/1.5.0-beta01.txt | `OutlinedTextField(String value, ..., boolean isError, ..., supportingText, ...)`; 1.4.0 notes list SecureTextField and OutlinedSecureTextField; validate-input guide uses `isError` with `supportingText` |
| F18 | Do not keep Material 2 and Material 3 in one app long-term; phased migration is the advice | Android rec. | https://developer.android.com/develop/ui/compose/designsystems/material2-material3 | "In general, you should not use both M2 and M3 in a single app long-term." / "Take a phased approach to migration." |
| F19 | M2 to M3 mappings | API doc | https://developer.android.com/develop/ui/compose/designsystems/material2-material3 | BottomNavigation -> NavigationBar, BottomNavigationItem -> NavigationBarItem; "The M2 ScaffoldState class no longer exists in M3"; "ContentAlpha and LocalContentAlpha don't exist in M3"; medium emphasis -> onSurfaceVariant; backgroundColor "is now named to containerColor" |
| F20 | material3 Divider, TabRow and ScrollableTabRow are deprecated | API | https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/current.txt | `@Deprecated ... void Divider(`; `void HorizontalDivider(`; `@Deprecated ... void TabRow(`; `void PrimaryTabRow(` (same in 1.4.0-beta03.txt and 1.5.0-beta01.txt) |
| F21 | Current releases: 1.5.0 stable and 1.6.0-alpha01, both 18 November 2026 | Release notes | https://developer.android.com/jetpack/androidx/releases/compose-material3 | "Version 1.5.0 Nov 18 2026"; top app bar variants, BottomAppBar, slot-based SearchBar "now stable" |
| F22 | ModalBottomSheet is experimental; LoadingIndicator is expressive-experimental; FadeThroughNavigationTransitions is 1.6.0-alpha01 only | API; release notes | https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/1.5.0-beta01.txt | `@ExperimentalMaterial3Api ... void ModalBottomSheet(` (also in 1.4.0-beta03 and current); `@ExperimentalMaterial3ExpressiveApi ... void LoadingIndicator(`; FadeThrough: 0 matches in 1.5.0-beta01, 2 in current; notes for 1.6.0-alpha01: "Added HorizontalSharedAxisNavigationTransitions and FadeThroughNavigationTransitions"; 1.5.0 "Remaining experimental APIs" lists LoadingIndicator |
| F23 | Made-up names are absent | API | https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/current.txt | `accessibleTouchTarget` and `AdaptiveNavigationBar`: 0 matches in material3, adaptive-navigation-suite, ui, foundation and foundation-layout current.txt. Real: `Modifier minimumInteractiveComponentSize(Modifier)` |
| F24 | M3 typography pages publish no minimum text size | Absence | https://m3.material.io/styles/typography/applying-type | "minimum" and "smallest" occur 0 times on applying-type and type-scale-tokens. Smallest style in the Views type table: `textAppearanceLabelSmall \| Medium 11sp` (https://raw.githubusercontent.com/material-components/material-components-android/master/docs/theming/Typography.md) |
| F25 | Views: hint goes on TextInputLayout | MDC doc | https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/TextField.md | "The android:hint should always be set on the TextInputLayout instead of on the EditText in order to avoid unintended behaviors." |
| F26 | Views: avoid hard-coded colours, use theme attributes | Android rec. | https://developer.android.com/develop/ui/views/theming/darktheme | "Avoid using hardcoded colors or icons intended for use under a light theme. Use theme attributes or night-qualified resources instead." |
| F27 | Compose: theme colours come from MaterialTheme.colorScheme; dynamic colour is optional | API doc | https://developer.android.com/develop/ui/compose/designsystems/material3 | "You can access Material theme colors in your app via MaterialTheme.colorScheme" / "If dynamic color is available, you can set up a dynamic ColorScheme. If not, you should fall back to using a custom light or dark ColorScheme." |
| F28 | Do not signal state by colour alone | Android rec. | https://developer.android.com/guide/topics/ui/accessibility/principles | "One version uses only color to distinguish between two possible actions in a workflow. The other version uses the best practice of including shapes and text in addition to color" |
| F29 | Orientation locks are ignored on large screens for apps targeting API 36 | Platform behaviour | https://developer.android.com/develop/ui/compose/layouts/adaptive/app-orientation-aspect-ratio-resizability | "The following manifest attributes and APIs are ignored for apps targeting Android 16 (API level 36) on large screens": screenOrientation, setRequestedOrientation() ... ; "devices with smallest width >= 600dp" |
| F30 | Single pane at compact and medium, two panes possible above | M3 rec. | https://m3.material.io/foundations/layout/applying-layout/window-size-classes | "Compact and medium breakpoints should use a single pane, while larger breakpoints can use two" |
| F31 | Wear OS has its own Material, foundation and navigation libraries | Android rec. | https://developer.android.com/training/wearables/compose | "Wear OS has its own versions of material and material3, foundation, and navigation libraries" / "mixing Compose Material with Compose Material for Wear OS can result in unexpected behavior" |
| F32 | Wear OS navigation and lists | API doc | https://developer.android.com/training/wearables/compose/navigation | "declare SwipeDismissableNavHost as a content of the AppScaffold"; lists page: "a version of the LazyColumn class called TransformingLazyColumn" |
| F33 | TV has its own Material library | Android rec. | https://developer.android.com/training/tv/playback/compose | "Use the TV version of APIs wherever possible"; `androidx.tv:tv-material`; "mixing Compose Material with Compose Material from Compose for TV can result in unexpected behavior" |
| F34 | TV input is D-pad focus; keep content overscan-safe | Android rec. | https://developer.android.com/training/tv/get-started/navigation | "Ensure that a user with a D-pad controller can navigate to all visible controls on the screen." Layout page (https://developer.android.com/design/ui/tv/guides/styles/layouts): "Ensure important elements are always visible ... within the overscan." |
| F35 | FAB is for the most important action on a screen | M3 rec. | https://m3.material.io/components/floating-action-button/guidelines | "Use a FAB for the most important action on a screen" |
| F36 | Back is a system gesture apps opt in to | Platform behaviour | https://developer.android.com/guide/navigation/custom-back/predictive-back-gesture | "Predictive Back, a gesture navigation feature, lets users preview where the back swipe takes them." |
| F37 | Views BottomNavigationView takes at most five items (not used in an assertion) | MDC doc | https://raw.githubusercontent.com/material-components/material-components-android/master/docs/components/BottomNavigation.md | "BottomNavigationView does not support more than 5 menu items." |

Quotes replace typographic dashes and apostrophes with ASCII ones; wording is otherwise verbatim.

Contrast values were computed with the WCAG relative-luminance formula: `#BDBDBD` on `#FFFFFF` is 1.88:1 and `#C6FF00` on
`#FFFFFF` is 1.19:1. The assertions accept a band around each value.

### A2. Trigger queries

Format matches `tests/evals/apple-hig/trigger-queries.json`. 20 positives and 20 negatives, 13 train and 7 validation of each.
Six positives never say "Material". The negatives cover Apple UI (three, for the sibling `apple-hig` skill), MUI,
Angular Material, Material Web, Flutter, React Native Paper, Compose Multiplatform for desktop and iOS, generic CSS,
Play metadata, and non-design Android work that mentions Compose or material3.

```json
[
  {"query": "my Compose bottom bar has 7 items and looks cramped on small phones, labels get cut off. what should I do with it", "should_trigger": true, "split": "train", "note": "never says Material; destination count"},
  {"query": "make this Android settings screen feel native - right now it's a Column of custom rows with a toggle I drew myself and it looks like a web page", "should_trigger": true, "split": "validation", "note": "never says Material; native feel"},
  {"query": "why does my app look wrong on a foldable? when I unfold the Pixel Fold it's just the phone layout stretched, with a giant bottom bar and one huge list", "should_trigger": true, "split": "train", "note": "never says Material; phone to foldable"},
  {"query": "can you do a Material 3 review of app/src/main/java/com/acme/checkout/CheckoutScreen.kt before we ship 3.0 on friday", "should_trigger": true, "split": "train", "note": "explicit review"},
  {"query": "should this be a dialog, a bottom sheet or a snackbar? it's a filters panel with 6 options in our Android app, phone and tablet", "should_trigger": true, "split": "train", "note": "component choice"},
  {"query": "audit RatingBar.kt for TalkBack and font scale problems, QA says the labels get clipped at 200% font size", "should_trigger": true, "split": "validation", "note": "accessibility; never says Material"},
  {"query": "we're migrating from androidx.compose.material to material3. what replaces BottomNavigation and ScaffoldState, and is ModalBottomSheet still experimental", "should_trigger": true, "split": "train", "note": "M2 to M3 migration; API status"},
  {"query": "bringing our Compose phone app to Wear OS. it has 4 bottom tabs and long lists - what should navigation and lists look like on the watch", "should_trigger": true, "split": "validation", "note": "phone to Wear OS"},
  {"query": "Android TV version of our streaming app in Compose: focus jumps around the rows and the cards near the edge are cut off on some TVs. what are the layout rules", "should_trigger": true, "split": "train", "note": "TV focus and overscan"},
  {"query": "res/layout/activity_login.xml - the fields have no visible labels and the button style doesn't match the rest of the app. fix it to follow the guidelines. Views with MaterialComponents, not Compose", "should_trigger": true, "split": "train", "note": "Views/XML"},
  {"query": "what's the minimum touch target size on android", "should_trigger": true, "split": "validation", "note": "quick fact"},
  {"query": "pick colour roles for success / warning / error banners in my Compose app that still work with dynamic color and dark theme", "should_trigger": true, "split": "train", "note": "colour roles"},
  {"query": "the FAB covers the last list item and my snackbar shows up behind the navigation bar. I'm using Scaffold, what am I doing wrong", "should_trigger": true, "split": "train", "note": "Scaffold slots and padding; never says Material"},
  {"query": "is it ok to have a hamburger drawer and a bottom bar in the same Android app? product wants both", "should_trigger": true, "split": "validation", "note": "navigation pattern conflict"},
  {"query": "navigation rail or bottom bar for our tablet layout? 4 destinations, Compose, landscape supported", "should_trigger": true, "split": "train", "note": "window size classes"},
  {"query": "we want the M3 Expressive look - button groups, a floating toolbar, the wavy progress bar. we're pinned to material3 1.4.0. which of those exist there and which need an opt-in", "should_trigger": true, "split": "train", "note": "Expressive; API availability by version"},
  {"query": "refactor this Compose screen so sizes and colours come from the theme instead of hard-coded sp and hex values, change as little as possible", "should_trigger": true, "split": "validation", "note": "minimal-diff refactor"},
  {"query": "we have an iOS app with a tab bar and large titles and are designing the Android version now. what should change so it doesn't feel like an iPhone port", "should_trigger": true, "split": "validation", "note": "cross-skill: Android is the target"},
  {"query": "after targeting Android 15 my top app bar draws under the status bar and the list is hidden behind the gesture bar. how should insets work with a Scaffold", "should_trigger": true, "split": "train", "note": "edge-to-edge UI"},
  {"query": "write a Compose sign-up form with inline validation errors, should look like a proper Google-style form", "should_trigger": true, "split": "train", "note": "form implementation; never says Material"},
  {"query": "make this SwiftUI settings screen feel native - right now it's a ScrollView with custom toggle rows and my designer says it looks like a web page", "should_trigger": false, "split": "train", "note": "Apple UI: belongs to apple-hig"},
  {"query": "my UITabBarController has 7 tabs and the More tab looks ugly. what does the HIG say about tab count", "should_trigger": false, "split": "validation", "note": "Apple UI: UIKit / HIG"},
  {"query": "what's the minimum tap target on iOS per the Human Interface Guidelines", "should_trigger": false, "split": "train", "note": "Apple UI quick fact"},
  {"query": "MUI v6: how do I override the theme palette and set AppBar elevation to 0 in dark mode in our React dashboard", "should_trigger": false, "split": "train", "note": "Material UI for React (web)"},
  {"query": "Angular Material mat-form-field shows the error under the input but the layout jumps. how do I reserve space with subscriptSizing", "should_trigger": false, "split": "validation", "note": "Angular Material (web)"},
  {"query": "Flutter: switch between NavigationRail on tablets and NavigationBar on phones with useMaterial3: true, and keep the selected index", "should_trigger": false, "split": "train", "note": "Flutter Material widgets"},
  {"query": "my StateFlow collection in a Compose screen restarts every time I rotate. collectAsStateWithLifecycle or repeatOnLifecycle?", "should_trigger": false, "split": "train", "note": "coroutines / lifecycle, not design"},
  {"query": "Room migration from version 3 to 4 fails with 'expected column not found' after I added a nullable field", "should_trigger": false, "split": "train", "note": "Room"},
  {"query": "Gradle sync fails after bumping the Compose BOM: Duplicate class androidx.compose.material3.internal... how do I align the versions", "should_trigger": false, "split": "validation", "note": "build problem that mentions material3"},
  {"query": "write the Play Store listing for version 4.1 of our hiking app: short description, full description, what's new", "should_trigger": false, "split": "train", "note": "Play Console metadata"},
  {"query": "Compose Multiplatform desktop app (JVM, Windows and macOS): how do I add a native menu bar and a tray icon", "should_trigger": false, "split": "validation", "note": "Compose Multiplatform desktop target"},
  {"query": "Compose Multiplatform on iOS: my UIKitView map doesn't receive touches inside a LazyColumn", "should_trigger": false, "split": "train", "note": "Compose Multiplatform iOS target"},
  {"query": "CSS only: card with a material-like shadow and a ripple on click, no library", "should_trigger": false, "split": "train", "note": "generic web CSS that says material"},
  {"query": "LazyColumn with 5000 items janks and Layout Inspector shows recomposition on every scroll frame. how do I profile and fix it", "should_trigger": false, "split": "validation", "note": "Compose performance, not design"},
  {"query": "WorkManager periodic job stops running after reboot on some Xiaomi devices", "should_trigger": false, "split": "train", "note": "background work"},
  {"query": "Navigation Compose with type-safe routes: how do I pass a Parcelable argument with kotlinx.serialization", "should_trigger": false, "split": "train", "note": "navigation plumbing, not navigation design"},
  {"query": "@material/web md-filled-button: change the container shape with CSS custom properties in a Lit component", "should_trigger": false, "split": "validation", "note": "Material Web components"},
  {"query": "generate an adaptive launcher icon foreground for my Android app, a green fox, 432x432 png", "should_trigger": false, "split": "train", "note": "image generation"},
  {"query": "write Compose UI tests with createComposeRule for LoginScreen - button disabled until both fields are filled", "should_trigger": false, "split": "validation", "note": "UI testing, not design"},
  {"query": "React Native Paper BottomNavigation: the badge doesn't update when my redux state changes", "should_trigger": false, "split": "train", "note": "React Native Paper"}
]
```

### A3. Task scenarios

Same schema as `tests/evals/apple-hig/evals.json`. `references_expected` is empty for the lead to fill once the reference files
exist. The merges needed to fit 20 requested topics into 16 scenarios: detection with the settings screen (1); adaptive
navigation code with the tablet adaptation (9); Wear OS with TV (10); the two hallucination traps with unspecified
numbers (14). Scenario 15 carries a reference-count assertion, as the first round recommended.

```json
{
 "skill_name": "material-design",
 "evals": [
  {
   "id": 1,
   "name": "formfactor-ambiguous-settings",
   "category": "form-factor-detection",
   "prompt": "Build me a settings screen for my app. Needs notifications on/off, theme (system / light / dark), account, and about.",
   "expected_output": "Notices that toolkit (Compose or Views), form factor and Material library version are unstated. Inspects the project, asks one concise question, or proceeds on an explicit assumption (for example phone and tablet, Jetpack Compose, material3 1.5.0). Builds the screen from Material 3 components with theme colours and typography.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "The response either asks about, or explicitly states the assumption it made for, the UI toolkit (Jetpack Compose or Views) and the form factor or device class",
    "Any Compose code uses components from androidx.compose.material3 and imports nothing from androidx.compose.material other than the icons package",
    "On/off settings use the Material Switch component (or SwitchPreference / MaterialSwitch in Views), not a hand-drawn toggle",
    "The code contains no hard-coded Color(0x...) or hex colour literals; colours come from MaterialTheme.colorScheme, theme attributes, or component defaults",
    "If the code uses Scaffold, the PaddingValues passed to the content lambda are applied to the content",
    "The code does not call the deprecated material3 Divider composable (HorizontalDivider is fine)"
   ]
  },
  {
   "id": 2,
   "name": "design-navigation-window-size-classes",
   "category": "design",
   "prompt": "No code yet. Android app for a local news outlet with five top-level sections: Top stories, Local, Sport, Saved, Podcasts. It has to work on phones, foldables and tablets. Which navigation component should show at each window size, and where are the breakpoints?",
   "expected_output": "Navigation bar at compact width, bar or rail at medium, navigation rail at expanded and larger; breakpoints at 600dp and 840dp; five destinations is inside the three-to-five range; keyed on window size class, not device type. Cites sources.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "The response recommends a navigation bar for compact-width windows",
    "The response recommends a navigation rail for expanded-width windows and does not recommend a navigation bar there",
    "The response gives 600dp and 840dp as the width breakpoints between compact, medium and expanded",
    "The response treats five destinations as acceptable for a navigation bar (for example by citing the three-to-five guidance) and does not say five is too many",
    "The response bases the choice on the window size class or available window width, not on device model or an isTablet check",
    "The response cites at least one m3.material.io or developer.android.com URL",
    "The response contains no code block longer than 5 lines"
   ]
  },
  {
   "id": 3,
   "name": "design-dialog-sheet-snackbar",
   "category": "design",
   "prompt": "Three moments in my Android notes app. Which component for each, and why? (1) 'Note moved to trash', with a way to undo. (2) 'Delete all 42 notes forever?'. (3) A list of actions for one note on a phone: Share, Duplicate, Move to folder, Export as PDF, Add label, Print. No code.",
   "expected_output": "(1) Snackbar with an Undo action. (2) Basic dialog with explicit confirm and dismiss actions. (3) Modal bottom sheet (a menu is an acceptable alternative). Reasons tied to message priority and how interruptive each component is, with sources.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 2,
   "assertions": [
    "For (1) the response recommends a snackbar with an Undo action and does not recommend a dialog",
    "For (2) the response recommends a dialog that requires an explicit confirm or cancel choice",
    "For (3) the response recommends a modal bottom sheet (it may mention a menu as an alternative)",
    "The reasoning distinguishes low-priority, non-blocking messages (snackbar) from critical, blocking decisions (dialog)",
    "The response cites at least one m3.material.io or developer.android.com URL",
    "The response contains no code block longer than 5 lines"
   ]
  },
  {
   "id": 4,
   "name": "implement-form-validation",
   "category": "implementation",
   "prompt": "Compose, material3 1.5.0, minSdk 26, phones. Write a sign-up form: email, password, confirm password and a Create account button. Validate inline and show errors the Material way. Full composable please.",
   "expected_output": "OutlinedTextField or TextField (or the secure variants) with labels, isError plus supportingText for error messages, obscured password input, theme colours only, and nothing that needs an alpha release. Brief notes with sources.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "Every input is a material3 TextField, OutlinedTextField, SecureTextField or OutlinedSecureTextField with a label",
    "Invalid input sets isError on the field and puts the error message in the field's supportingText (not in a Toast, dialog, or a separate Text placed outside the field)",
    "Password inputs are obscured, using SecureTextField / OutlinedSecureTextField or a password visual transformation",
    "The code contains no hard-coded Color(0x...) literal for the error state; it relies on component defaults or MaterialTheme.colorScheme.error",
    "Any API the code uses that is marked experimental carries a matching @OptIn, and the response does not tell the user to move to an alpha or beta release",
    "The explanation cites at least one m3.material.io or developer.android.com URL"
   ]
  },
  {
   "id": 5,
   "name": "review-compose-inbox",
   "category": "review",
   "prompt": "Material review please: tests/evals/material-design/files/InboxScreen.kt. Phone app, Compose, material3 1.5.0, minSdk 26. Tell me what actually matters before release.",
   "expected_output": "A structured review in the skill's format: each finding has one of the five classes, a severity, a rationale, a source URL and a fix. Finds at least 5 of the 6 planted issues, separates the deprecated API and the accessibility problem from recommendations, and orders by severity.",
   "files": [
    "tests/evals/material-design/files/InboxScreen.kt"
   ],
   "references_expected": [],
   "max_reference_files": 4,
   "assertions": [
    "Every finding carries exactly one of the skill's five classification labels, a severity, a concrete fix, and a source URL or an explicit note that no source exists",
    "The androidx.compose.material imports (FloatingActionButton, Text) are flagged as Material 2 components mixed into a Material 3 screen, with the material3 equivalents as the fix",
    "The ignored Scaffold content padding is flagged, and the fix applies the PaddingValues to the list (padding modifier or contentPadding)",
    "Divider is flagged as deprecated with HorizontalDivider as the replacement, and the response does not state the library version in which it was deprecated",
    "contentDescription = null on the search icon button is flagged as an accessibility issue, with a text description as the fix",
    "The AlertDialog that only confirms 'Conversation archived.' is flagged, a snackbar is proposed instead, and the finding is not classified as a confirmed guideline or API violation",
    "The hard-coded top app bar colours are flagged with theme colour roles as the fix, and the finding is not classified as a confirmed guideline or API violation"
   ]
  },
  {
   "id": 6,
   "name": "review-views-xml-appointment",
   "category": "review",
   "prompt": "Review tests/evals/material-design/files/fragment_appointment.xml against Material and Android accessibility guidance. This is a Views app on Material Components for Android with a Theme.Material3 DayNight theme; we are not moving to Compose.",
   "expected_output": "A structured review that stays in XML. Finds the dp text size, the unlabelled 32dp ImageButton, the hint on the wrong element, the hard-coded colours that break the night theme, and the colour-only status dot, each with a source and an XML fix.",
   "files": [
    "tests/evals/material-design/files/fragment_appointment.xml"
   ],
   "references_expected": [],
   "max_reference_files": 4,
   "assertions": [
    "All fixes are given as XML or View-system changes; the response does not rewrite the layout in Jetpack Compose",
    "android:textSize=\"20dp\" is flagged because dp text does not follow the user's font size setting, with sp or a textAppearance attribute as the fix",
    "The ImageButton is flagged for having no contentDescription, classified as an accessibility issue",
    "The 32dp ImageButton is flagged as smaller than the 48dp touch target guidance",
    "The android:hint on the TextInputEditText is flagged, with moving it to the TextInputLayout as the fix",
    "The hard-coded #FFFFFF background and/or #212121 text colour is flagged as breaking the dark (night) theme, with theme attributes such as ?attr/colorSurface and ?attr/colorOnSurface as the fix",
    "The status dot is flagged as conveying availability by colour alone, with a text, icon or shape cue (or a content description) proposed"
   ]
  },
  {
   "id": 7,
   "name": "refactor-minimal-diff-dark-theme",
   "category": "refactor",
   "prompt": "In tests/evals/material-design/files/ForecastCard.kt the card stays white with dark grey text when the phone is in dark theme. Fix that. Don't restyle or restructure anything else - the diff has to be tiny.",
   "expected_output": "Replaces the five colour literals with MaterialTheme.colorScheme roles (or removes them so component defaults apply). No other pre-existing line changes. The 28.sp size and everything else are at most listed as optional follow-ups.",
   "files": [
    "tests/evals/material-design/files/ForecastCard.kt"
   ],
   "references_expected": [],
   "max_reference_files": 2,
   "assertions": [
    "No Color(0xFF...) literal remains in the edited composable",
    "Each replaced colour is a MaterialTheme.colorScheme role, or the argument is removed so the component default or content colour applies",
    "Text and icon colours are roles meant for content on the chosen container (for example onSurface / onSurfaceVariant on a surface role), not unrelated roles such as primary for body text",
    "No pre-existing line that lacks a colour literal is modified in the applied change (import lines may be added or removed)",
    "The composable's name, parameters and layout structure (Card > Row > Icon, Column, Text) are unchanged",
    "Any other observation (for example the 28.sp font size) is presented as optional and is not applied"
   ]
  },
  {
   "id": 8,
   "name": "accessibility-audit-quantity-stepper",
   "category": "accessibility",
   "prompt": "Accessibility audit of tests/evals/material-design/files/QuantityStepper.kt please. A TalkBack user told us they can't tell what the two buttons do, and someone else says the number is unreadable. Compose, material3 1.5.0.",
   "expected_output": "Finds the unlabelled icons, the clickable Boxes with no button role, the 32dp targets, the dp-derived font size that ignores font scale, and the low-contrast number. Gives corrected code that keeps the composable's signature, with sources.",
   "files": [
    "tests/evals/material-design/files/QuantityStepper.kt"
   ],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "The two controls are flagged as having no accessible name (contentDescription = null and no click label), with a description or onClickLabel as the fix",
    "The clickable Boxes are flagged as not exposing a button role, and the fix uses IconButton (or another Material button) or passes role = Role.Button",
    "The 32dp controls are flagged against the 48dp minimum touch target guidance, with a fix such as IconButton, minimumInteractiveComponentSize, or a 48dp minimum size",
    "The 14.dp.toSp() font size is flagged because it does not scale with the user's font size setting, with sp or a MaterialTheme.typography style as the fix",
    "The #BDBDBD text on white is flagged as failing the 4.5:1 contrast guidance; if a ratio is stated it is between 1.7:1 and 2.1:1",
    "The corrected code keeps the QuantityStepper(quantity, onChange, modifier) signature"
   ]
  },
  {
   "id": 9,
   "name": "adapt-phone-to-tablet-foldable",
   "category": "adaptation",
   "prompt": "Tablet and foldable users say our app looks like a blown-up phone: tests/evals/material-design/files/TrailShell.kt. We target API 36. Make the shell adaptive and show the new root composable.",
   "expected_output": "Switches navigation by window size class (NavigationSuiteScaffold, or NavigationBar at compact and NavigationRail at wider sizes), deals with six destinations, removes the fixed 360dp column in favour of a layout that uses the width, and removes the portrait lock, explaining that large screens ignore it for apps targeting API 36.",
   "files": [
    "tests/evals/material-design/files/TrailShell.kt"
   ],
   "references_expected": [],
   "max_reference_files": 4,
   "assertions": [
    "The new code uses NavigationSuiteScaffold, or chooses between NavigationBar and NavigationRail from the window size class (for example currentWindowAdaptiveInfo().windowSizeClass)",
    "The navigation choice is not based on device model, an isTablet flag, or screen orientation",
    "Six destinations are flagged against the three-to-five navigation bar guidance, with a concrete proposal (reduce to five, or move the rest into a rail or drawer)",
    "The fixed width(360.dp) is removed, and the response says how wide windows use the extra space (for example list-detail panes, a grid, or a maximum content width)",
    "The portrait lock is removed or flagged, and the response says that orientation restrictions are ignored on large screens (smallest width 600dp and up) for apps targeting API level 36, or that they conflict with large-screen quality guidance",
    "The response cites at least one developer.android.com or m3.material.io URL"
   ]
  },
  {
   "id": 10,
   "name": "adapt-phone-to-wear-and-tv",
   "category": "adaptation",
   "prompt": "Our Compose phone app is a workout timer: a list of routines, a routine detail screen with start / pause, and a bottom navigation bar with Routines, History, Settings. We now need a Wear OS version and an Android TV version. What changes in navigation, components and input on each? Outline first; short code only where the API differs.",
   "expected_output": "Wear OS: the Wear Compose Material 3 library, no bottom bar, swipe-to-dismiss navigation, a watch list component inside the Wear scaffolds. TV: the TV Material library, D-pad focus navigation with every control reachable, overscan-safe margins. Does not carry the phone navigation bar to either.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 4,
   "assertions": [
    "For Wear OS the response says to use the Wear Compose Material 3 library (androidx.wear.compose) rather than the phone androidx.compose.material3 components",
    "For Wear OS the response replaces the bottom navigation bar and describes swipe-to-dismiss back navigation (for example SwipeDismissableNavHost)",
    "For Wear OS the response uses a watch list component such as TransformingLazyColumn or ScalingLazyColumn for the routine list",
    "For TV the response says to use the TV Material library (androidx.tv.material3 / tv-material) rather than the phone components",
    "For TV the response says navigation is by D-pad focus and that every control must be reachable and show focus",
    "For TV the response says to keep important content inside overscan-safe margins",
    "The response does not propose reusing the phone NavigationBar on the watch or on TV"
   ]
  },
  {
   "id": 11,
   "name": "migrate-m2-to-m3",
   "category": "migration",
   "prompt": "We're still on androidx.compose.material and planning the move to material3 1.5.0. What do BottomNavigation, scaffoldState.snackbarHostState, ContentAlpha.medium and Scaffold's backgroundColor become? And can we migrate screen by screen, or is it all at once?",
   "expected_output": "BottomNavigation and BottomNavigationItem become NavigationBar and NavigationBarItem; ScaffoldState is gone, use SnackbarHostState with the snackbarHost slot; ContentAlpha does not exist, use colour roles such as onSurfaceVariant; backgroundColor is containerColor. A phased migration is possible, but the two libraries should not coexist long-term. Cites the migration guide.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 2,
   "assertions": [
    "The response maps BottomNavigation / BottomNavigationItem to NavigationBar / NavigationBarItem",
    "The response says ScaffoldState does not exist in material3 and shows SnackbarHostState passed through the Scaffold's snackbarHost slot",
    "The response says ContentAlpha / LocalContentAlpha do not exist in material3 and maps medium emphasis to a colour role such as onSurfaceVariant",
    "The response maps Scaffold's backgroundColor to containerColor",
    "The response says a phased, screen-by-screen migration is possible while both libraries are present, and that using both long-term is discouraged",
    "The response cites the Material 2 to Material 3 migration guide on developer.android.com"
   ]
  },
  {
   "id": 12,
   "name": "experimental-or-unavailable-api",
   "category": "deprecated-unsupported-api",
   "prompt": "We're pinned to androidx.compose.material3:material3:1.5.0. Stable releases only, and every @OptIn needs tech-lead sign-off. I want (a) the morphing LoadingIndicator for pull-to-refresh, (b) a ModalBottomSheet for filters, (c) FadeThroughNavigationTransitions with predictive back. Which can I use as is, which need an opt-in, and which aren't there?",
   "expected_output": "(a) LoadingIndicator exists in 1.5.0 but is experimental: needs @OptIn(ExperimentalMaterial3ExpressiveApi::class). (b) ModalBottomSheet exists but is annotated @ExperimentalMaterial3Api. (c) FadeThroughNavigationTransitions is not in 1.5.0; it first appears in 1.6.0-alpha01. Offers an alternative for (a) that needs no opt-in and does not push an alpha upgrade against the stated policy.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 2,
   "assertions": [
    "The response says LoadingIndicator is experimental in 1.5.0 and needs an opt-in to ExperimentalMaterial3ExpressiveApi",
    "The response says ModalBottomSheet is available in 1.5.0 but needs an opt-in to ExperimentalMaterial3Api",
    "The response says FadeThroughNavigationTransitions is not available in 1.5.0 (it was added in 1.6.0-alpha01)",
    "The response does not present upgrading to an alpha release as the solution without noting that it conflicts with the stable-only policy",
    "The response offers at least one alternative for (a) that needs no opt-in (for example the default PullToRefreshBox indicator or CircularProgressIndicator)",
    "The response cites the Compose Material 3 release notes or API reference on developer.android.com"
   ]
  },
  {
   "id": 13,
   "name": "conflict-brand-vs-material",
   "category": "conflicting-guidance",
   "prompt": "Brand rules for our Android app, non-negotiable according to the brand team: (1) the bottom navigation bar shows icons only, no labels; (2) links are brand lime #C6FF00 on our white background; (3) every icon button is 36dp and they sit edge to edge in a row; (4) dynamic colour off, our palette only. Implement it in Compose with material3 1.5.0 and tell me which of these are real problems and which are just 'not Material'.",
   "expected_output": "Separates accessibility problems (lime links at about 1.2:1 on white; 36dp touch targets packed together) from departures from Material recommendations (no labels) and non-issues (dynamic colour is optional). Pushes back on the accessibility items with a concrete alternative, then implements what the user decides, with content descriptions on label-less navigation icons.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "The response says Material guidance asks for labels on navigation bar items, and presents removing them as a departure from a recommendation rather than a hard requirement",
    "If the code implements icon-only navigation items, each icon has a non-null contentDescription",
    "The response says #C6FF00 on white fails the 4.5:1 text contrast guidance and proposes an alternative (for example a darker brand variant); if it states the ratio, the value is between 1.0:1 and 1.4:1",
    "The response flags 36dp edge-to-edge icon buttons against the 48dp touch target guidance and offers a way to keep the 36dp visual size with a 48dp target or spacing",
    "The response says turning dynamic colour off is acceptable and not a guideline violation",
    "The response explicitly separates accessibility problems from brand or style preferences",
    "The response does not claim that Google Play will reject the app for any of the four rules"
   ]
  },
  {
   "id": 14,
   "name": "hallucination-and-unspecified-numbers",
   "category": "hallucination-trap",
   "prompt": "My lead left review comments on our Compose code (material3 1.5.0): wrap the small icons in Modifier.accessibleTouchTarget() from material3, swap our bar-plus-rail switching for the new AdaptiveNavigationBar composable, and shorten the tab labels because Material 3 caps navigation bar labels at 12 characters. Can you tell me how to apply all three? Also, what is Material's official minimum font size in sp, and exactly how many seconds does a snackbar have to stay on screen?",
   "expected_output": "Says Modifier.accessibleTouchTarget and AdaptiveNavigationBar do not exist in material3 and offers the real APIs (minimumInteractiveComponentSize; NavigationSuiteScaffold or NavigationBar / NavigationRail). Does not confirm a 12-character rule; gives the actual label guidance. Says Material publishes no minimum font size, and no single required snackbar duration (guidance is a 4 to 10 second range for snackbars without actions).",
   "files": [],
   "references_expected": [],
   "max_reference_files": 2,
   "assertions": [
    "The response says Modifier.accessibleTouchTarget() is not a material3 API and offers minimumInteractiveComponentSize or a 48dp minimum size instead",
    "The response says AdaptiveNavigationBar is not a material3 composable and offers NavigationSuiteScaffold or NavigationBar / NavigationRail switching instead",
    "The response does not confirm a 12-character limit; it says the guidance is short labels (one or two words, not truncated) or that no character limit is published",
    "The response does not state a minimum font size in sp as a Material rule; it says none is published (it may mention the smallest type scale style)",
    "The response does not give a single required snackbar duration as a Material rule; it says none is fixed, or gives the 4 to 10 second guidance for snackbars without actions",
    "The response contains no code that calls accessibleTouchTarget or AdaptiveNavigationBar"
   ]
  },
  {
   "id": 15,
   "name": "token-efficiency-simple-question",
   "category": "context-efficiency",
   "prompt": "what's the minimum touch target size on android?",
   "expected_output": "A short answer: 48 x 48 dp, a Material accessibility recommendation that Android's core app quality guidelines also list; the visible element can be smaller than the target. One source link. No review, no long code, at most one reference file read.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 1,
   "assertions": [
    "The answer states 48 x 48 dp (or 48dp)",
    "The answer does not say that Android or Google Play enforces the size or rejects apps below it",
    "The answer includes one m3.material.io or developer.android.com URL",
    "The answer is at most 120 words, excluding URLs and table syntax",
    "The answer contains no code block longer than 5 lines and mentions platforms other than Android in at most one clause",
    "At most one skill reference file was read to produce the answer"
   ]
  },
  {
   "id": 16,
   "name": "cross-skill-port-ios-tab-bar",
   "category": "cross-skill",
   "prompt": "We're porting our iOS app to Android in Compose (material3 1.5.0). On iPhone it has a UITabBar with five tabs - Home, Search, a centre + that opens the composer, Inbox, Me - a large title that collapses on scroll, and swipe from the left edge to go back. The designer wants the Android app to look identical. What should I build?",
   "expected_output": "Applies Android conventions instead of copying iOS chrome: a Material navigation bar with labelled destinations (rail on wider windows), the composer action moved out of the destinations (for example a FAB), a collapsing Material top app bar, and the system back gesture instead of a custom edge swipe. Explains the trade-off of an identical look once and leaves the decision to the user.",
   "files": [],
   "references_expected": [],
   "max_reference_files": 3,
   "assertions": [
    "The response recommends the Material 3 NavigationBar with labelled destinations rather than a custom replica of the iOS tab bar",
    "The response proposes a FloatingActionButton or another placement outside the navigation destinations for the composer action, or explicitly explains the trade-off of keeping an action among the destinations",
    "The response says back navigation should use the Android system back gesture (predictive back) and does not implement a custom left-edge swipe",
    "The response maps the collapsing large title to a Material top app bar with a scroll behaviour (for example LargeTopAppBar or a flexible top app bar)",
    "The response explains that copying iOS chrome departs from Android conventions, and leaves the final choice to the user instead of refusing",
    "The response gives no SwiftUI or UIKit code and does not cite Apple's Human Interface Guidelines as the rule for the Android app"
   ]
  }
 ]
}
```

Grading notes:

- Scenarios 5 and 6 name "the skill's five classification labels". This assumes the new skill keeps the Apple skill's review format.
- Scenario 7 is graded from a diff against the fixture. Its line rule is the rewritten form from iteration 1 (no pre-existing line without a colour literal changes), with no line-count cap.
- Scenario 9: `contentDescription = null` on the labelled navigation icons is deliberately not graded. The accessibility page says to pass null for an icon that is part of another element, while Android's own `NavigationSuiteScaffold` sample sets a description.
- Scenario 12 depends on release state as of 2026-11-18. Re-check F21 and F22 when a new material3 version ships.
- Scenario 16 should load `material-design`, not `apple-hig`. A trigger query covers the same case.

### A4. Fixtures

Five files with different subjects (mail inbox, clinic appointment, weather card, cart quantity stepper, hiking app
shell); none shares a subject with the Swift fixtures (orders, tabs, profile, player, library). Types such as
`MailThread`, `DayForecast`, `Trail` and `TrailRow` are assumed to exist elsewhere, as in the Swift fixtures. Not compiled.

`InboxScreen.kt` (45 lines; scenario 5)

```kotlin
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
```

`fragment_appointment.xml` (45 lines; scenario 6)

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#FFFFFF"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="@string/appointment_title"
        android:textColor="#212121"
        android:textSize="20dp" />
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">
        <!-- AppointmentFragment tints this green when the slot is free, red when it is taken -->
        <View
            android:id="@+id/slot_status"
            android:layout_width="12dp"
            android:layout_height="12dp"
            android:background="#D32F2F" />
        <TextView
            android:id="@+id/slot_time"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:textAppearance="?attr/textAppearanceBodyLarge" />
        <ImageButton
            android:id="@+id/change_slot"
            android:layout_width="32dp"
            android:layout_height="32dp"
            android:background="?attr/selectableItemBackgroundBorderless"
            android:src="@drawable/ic_calendar" />
    </LinearLayout>
    <com.google.android.material.textfield.TextInputLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content">
        <com.google.android.material.textfield.TextInputEditText
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="@string/reason_for_visit" />
    </com.google.android.material.textfield.TextInputLayout>
</LinearLayout>
```

`ForecastCard.kt` (33 lines; scenario 7)

```kotlin
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
```

`QuantityStepper.kt` (31 lines; scenario 8)

```kotlin
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
```

`TrailShell.kt` (42 lines; scenario 9)

```kotlin
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
```

### A5. Planted problems and evidence

Evidence is the facts-table row, which carries the URL and the quote.

| Fixture | Planted problem | Evidence |
|---|---|---|
| InboxScreen.kt | Material 2 FloatingActionButton and Text imported into a Material 3 screen | F18 |
| InboxScreen.kt | Scaffold content padding ignored (`{ _ ->`) | F12 |
| InboxScreen.kt | Deprecated `Divider()` | F20 |
| InboxScreen.kt | `contentDescription = null` on the search IconButton | F9 |
| InboxScreen.kt | Hard-coded `Color(0xFF1A73E8)` / `Color.White` app bar colours | F27, F26 |
| InboxScreen.kt | AlertDialog for the low-priority 'Conversation archived.' message | F13, F14 |
| fragment_appointment.xml | `android:textSize="20dp"` | F11 |
| fragment_appointment.xml | ImageButton without contentDescription | F9 |
| fragment_appointment.xml | ImageButton 32dp x 32dp | F6 |
| fragment_appointment.xml | `android:hint` on the TextInputEditText | F25 |
| fragment_appointment.xml | Hard-coded `#FFFFFF` background and `#212121` text | F26 |
| fragment_appointment.xml | Slot availability shown by a colour-only dot | F28 |
| ForecastCard.kt | Five `Color(0xFF...)` literals that ignore dark theme (the only intended change) | F27 |
| ForecastCard.kt | Distractor, not a defect to fix: `fontSize = 28.sp` | none; sp scales (F11) |
| QuantityStepper.kt | Icons with `contentDescription = null` inside the only clickable element | F9 |
| QuantityStepper.kt | `clickable` Box with no role | F10 |
| QuantityStepper.kt | 32dp clickable Boxes | F6, F7 |
| QuantityStepper.kt | `14.dp.toSp()` font size that ignores font scale | F11 |
| QuantityStepper.kt | `#BDBDBD` on white: computed 1.88:1 | F8 |
| TrailShell.kt | Six destinations in a NavigationBar | F1 |
| TrailShell.kt | NavigationBar at every window size | F3, F5 |
| TrailShell.kt | `width(360.dp)` single column | F30 |
| TrailShell.kt | Portrait lock through `requestedOrientation` | F29 |

Not planted on purpose, so a review that reports them should not gain or lose marks: hard-coded strings ("Inbox",
"Archive"), the missing `key` in `items`, the `@OptIn` question for `TopAppBar` (stable in 1.5.0, F21), and the status
dot's own hex colour.

A shipped example in the skill must not reuse any of these five screens or their fixes (the mistake found in the Apple
skill's first round).

## Part B - ecosystem check

### B1. Existing public skills (10 opened)

Found with `gh api search/code` (`filename:SKILL.md` plus "material design", "jetpack compose material3",
"name: material-design", "Material 3 Expressive"), then read from raw.githubusercontent.com. Sizes are for `SKILL.md`;
file counts come from code search and may undercount.

| Skill | URL | Licence | Size and structure | Bundles Google's text | Staleness | Patterns to learn from |
|---|---|---|---|---|---|---|
| android/skills (Google LLC), 42 skills | https://raw.githubusercontent.com/android/skills/main/README.md | Apache-2.0 (LICENSE.txt) | Opened 6. `jetpack-compose/adaptive` 497 lines + 16 references; `wear/wear-compose-m3` 370 lines + 52 references; `system/edge-to-edge` 426 lines, single file; `migration/ios-to-android` 429 lines + 22 references; `tv/leanback-to-compose-tv-migration` 739 lines + 3 references | Yes: references mirror developer.android.com pages (Google's own text) | Current: `last-updated` between 2026-08 and 2026-11 | Descriptions end with explicit "Don't use for ..." exclusions; `last-updated` metadata; one workflow per skill. README says they skip areas "where LLMs are already proficient, such as basic Jetpack Compose best practices". No component-choice, review or general Material skill |
| gdlbo/material-skill (`material-design-3`) | https://raw.githubusercontent.com/gdlbo/material-skill/main/SKILL.md | No licence file | 143 lines / 12 KB + 6 references (android, web, expressive, foundations, adaptive-accessibility, sources) | No (paraphrase plus a 156-line link index) | Current; covers Expressive | "Resolve the context first" checklist that asks whether an API is stable, experimental or unavailable; forbids incidental dependency upgrades; one reference per target |
| skydashnet/material-design-3-ui-skill | https://raw.githubusercontent.com/skydashnet/material-design-3-ui-skill/main/SKILL.md | MIT | 241 lines / 12 KB + 13 references + 6 markdown test cases; version 1.1.1 | No | Updated 2026-10-01; Expressive optional | Anti-patterns reference; a 'fake Material' audit test case; the destinations-versus-actions rule stated plainly. Design-spec oriented, little Compose code, few source links |
| asimawdah/material-expressive-skill | https://raw.githubusercontent.com/asimawdah/material-expressive-skill/main/SKILL.md | MIT | 121 lines / 8 KB + 9 references, 1 example, 2 templates | No | Reference review date 2026-11-16 | `official-sources.md` with a review date; review checklist; handoff templates. Trigger needs the word Material |
| macsystems/m3-agent-skill (`material-design-3-expert`) | https://raw.githubusercontent.com/macsystems/m3-agent-skill/main/SKILL.md | Apache-2.0 | 38 lines + 9 short references, one per foundation | No | Undated; token-level M3, one Expressive mention | Very small core. Weak points to avoid: numbers with no source links, no API status |
| david-saint/m3-skill (`material-design-3`) | https://raw.githubusercontent.com/david-saint/m3-skill/main/skill-v2/SKILL.md | No licence file | 38 lines + 4 files (foundations, styles, components, resources) | Not checked beyond SKILL.md | Claims "2025/2026 standards" | Mirrors the site's own section structure, which makes routing obvious |
| aldefy/compose-skill (`compose-expert`) | https://raw.githubusercontent.com/aldefy/compose-skill/master/skills/compose-expert/SKILL.md | MIT | 360 lines / 25 KB + about 45 references (accessibility, adaptive layout, deprecated patterns, TV, multiplatform ...) | No | Current | A deprecated-patterns reference written as old -> new. Its description triggers on any Compose API name, so it will compete with ours for Compose prompts |
| vinnie357/claude-skills (`material-design`) | https://raw.githubusercontent.com/vinnie357/claude-skills/main/plugins/design/skills/material-design/SKILL.md | MIT (2025) | 184 lines, single file | No | Material You era; 3 Expressive mentions | Same name as ours. Short overview with five m3.material.io links |
| sickn33/agentic-awesome-skills (`material-design`) | https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/main/skills/design-it/material-design/SKILL.md | MIT | 275 lines, single file; a sub-style of a `design-it` skill | No | Stale: Material 2 aesthetics (elevation shadows, uppercase 36px buttons, 4px radius) as CSS, plus a SwiftUI section; added 2026-06-17 | Same name as ours and mirrored into at least six other collections. Shows what to avoid: Material as a visual style rather than platform behaviour |
| SangkuOh/build-androidos-apps (`material3-adaptive-ui`) | https://raw.githubusercontent.com/SangkuOh/build-androidos-apps/main/plugins/build-androidos-apps/skills/material3-adaptive-ui/SKILL.md | MIT | 61 lines + 1 checklist reference | No | Current (names NavigationSuiteScaffold); no Expressive | Tight scope and a checklist reference |

Seen in search but not opened: `flutter/packages` `.agents/skills/material-3-expressive-migration` (Flutter), and many
per-project `.agents/skills/material-3` copies.

What this means for our skill:

- Google's own skills are narrow workflows with bundled documentation. Ours should not duplicate them: point to `wear-compose-m3`, `edge-to-edge`, `adaptive` and the TV migration skill where a task goes deep into those areas, and keep our Wear OS and TV files at the level of "what changes and why".
- No skill opened tags rule strength, records API status per library version, ships objective evals with fixtures, or gives a review output format. Those are the gaps the Apple skill's structure already fills.
- Useful patterns: exclusions written into the description; a dated sources file; an old -> new deprecated-patterns table; a context checklist that asks for toolkit, library version and API status first.

### B2. Name collisions

- `gh api search/code` for `filename:SKILL.md "name: material-design"` returns 182 hits (154 when hits mentioning Expressive are excluded). Distinct originals opened: `sickn33/agentic-awesome-skills` and `vinnie357/claude-skills`; others seen in the results: `anubhavg-icpl/vibe`, `alisonaquinas/llm-web-design-skills`, `Dev-Toolbelt/dev-team-agents`, `JantonioFC/skillsbank`, plus registry mirrors.
- No `material-design` skill exists in `android/skills`, `anthropics/skills` (4 hits for "material", none a Material Design skill), or the `material-components` organisation (0 `SKILL.md` files).
- Skill names are scoped to the directory or plugin they are installed from, so the collision is a discoverability and install-path concern, not a technical conflict. If both ours and a same-named skill are installed in one agent, the later copy can shadow the earlier one. Options for the lead: keep `material-design` (matches the brief and the sibling's naming), or use a more specific name such as `android-material-design`. The description must say Android, Compose and Views early, because most same-named skills are web or visual-style skills.

### B3. Licence terms of the sources

| Source | Statement as published | URL |
|---|---|---|
| Material Design 3 site | "All Material 3 content, guidelines, imagery, and resources are available under the Apache 2.0 or CC BY 4.0 license." The site footer itself has only Privacy Policy and Terms of Service links | https://m3.material.io/get-started |
| Android Developers, page footer | "Content and code samples on this page are subject to the licenses described in the Content License." | any page, for example https://developer.android.com/develop/ui/compose/components/scaffold |
| Android Developers, Content License | "the documentation on this site, including any code shown in it, is made available to you under the Apache 2.0 license" / "All other content on this site, except the license documents themselves and as otherwise noted, is licensed under the Creative Commons Attribution 2.5 license." / "Google's trademarks and other brand features ... are not included in the license." | https://developer.android.com/license |
| AndroidX API files, Material Components for Android docs | Apache-2.0 repositories [M]; licence files not opened in this session | - |

The older footer wording that names CC BY 4.0 for page content did not appear on the pages fetched today; the footer now
points to the Content License page, which names Apache 2.0 for documentation and CC BY 2.5 for other site content.

For a skill that paraphrases and links:

- Paraphrase with links needs no licence at all, and short quotations of numbers and wording are low risk. Both licences would also permit reuse of longer text, on conditions: attribution for CC BY; for Apache 2.0, keeping the licence and notices and stating changes.
- The Material statement does not say which of the two licences covers which item. If the skill ever copies a passage, table or image, treat it as CC BY 4.0 content: credit Google, link the page and the licence, and say it was adapted.
- Code adapted from Android documentation samples is Apache 2.0. Our repository is MIT, so add a notice for any such snippet, or write examples from scratch, which is simpler and is what the Apple skill did.
- Trademarks are excluded. Use "Material Design", "Android" and "Google" only to describe; no logos, and keep the same kind of disclaimer the Apple skill carries (independent, not Google documentation, Google's pages win).
- This is a reading of the published terms, not legal advice.
