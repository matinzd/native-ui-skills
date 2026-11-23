# Required versus recommended: Google Play and Android quality guidelines

Scope: what Google actually states as required and what is recommendation: Google Play target API levels by form factor, platform behaviour tied to `targetSdk`, core app quality IDs most relevant to UI, the adaptive app quality tiers, the Wear OS, TV, car and widget quality guidelines, how to word a finding, and a table of common claims against what the docs say. This file never predicts a Google Play review outcome.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Classes of obligation
- Google Play target API levels
- Platform behaviour tied to targetSdk
- Core app quality
- Adaptive app quality tiers
- Form-factor quality guidelines
- Accessibility numbers and their strength
- Claims versus what the docs say
- How to word a finding
- Common mistakes

## Classes of obligation

| Class | Meaning | Tag to use | Examples |
|---|---|---|---|
| Google Play requirement | A stated condition for submitting or staying available on Google Play | [Req] | Target API level; app bundles; no advertising in notifications |
| Form-factor publishing requirement | The form factor's quality page says apps must meet it to be published or accepted | [Req] | Wear OS `WO-*`; car Tier 3 (parked) and Tier 2 (driving); TV manifest declarations |
| API or asset contract | The platform will not work otherwise | [Req] or [API] | Notification channel; runtime permission; splash and adaptive icon sizes |
| Platform behaviour by `targetSdk` | The OS does this once the app targets the level; nothing to "comply" with, only to handle | [API] | Edge-to-edge; predictive back; ignored orientation locks |
| Quality guideline | "Minimum quality that all apps should meet", graded tiers, badging | [MD] | Core app quality; adaptive Tier 3/2/1 |
| Design recommendation | Material and Android design guidance | [MD] | 48dp targets on phones; navigation bar with 3 to 5 destinations |

- [Conv] When a page mixes "must" wording into a recommendation context (for example a design page saying apps "must handle display cutout insets"), report the wording but keep the class of the page it is on.

Source: https://developer.android.com/docs/quality-guidelines/core-app-quality, https://developer.android.com/google/play/requirements/target-sdk

## Google Play target API levels

Starting 2026-08-31, per the target API level page:

| App type | New apps and updates must target | Tag |
|---|---|---|
| Phone, tablet and other apps not listed below | Android 16 (API 36) or higher | [Req] |
| Wear OS, Android Automotive OS | Android 15 (API 35) or higher | [Req] |
| Android TV, Android XR | Android 14 (API 34) or higher | [Req] |

- [Req] Existing apps must target Android 15 (API 35) or higher to stay available to new users on devices running an Android version newer than the app's target. Apps below that (API 33 or lower for Wear OS, TV and XR; API 31 or lower for Automotive OS) remain available only on devices at or below their target level.
- [API] An extension to 2026-11-01 could be requested.
- [API] Contradiction: the Wear OS quality page still says new apps must target API 34 (from 2025-08-31). Its `WO-P1` item defers to Google Play's requirement, so the target-API page governs.
- [MD] Core app quality lists `Target_SDK_Version` (target the SDK needed for Google Play) and `Compile_SDK_Version` (build with the latest SDK).
- [Req] App bundles: mandatory for all new apps since August 2021 (`App_Bundles`), and for all new and existing TV apps (`TV-G1`).

Source: https://developer.android.com/google/play/requirements/target-sdk, https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Platform behaviour tied to targetSdk

These are facts about what the OS does, not policies. They matter because the target API floor above forces apps onto them.

| Behaviour | Level | Opt-out | Tag |
|---|---|---|---|
| Edge-to-edge enforced on Android 15+ | targetSdk 35 | `windowOptOutEdgeToEdgeEnforcement` at 35; disabled at targetSdk 36 on Android 16 devices | [API] |
| Cutout mode treated as always for non-floating windows | targetSdk 35 | None | [API] |
| Predictive back on by default; `onBackPressed` and `KEYCODE_BACK` not delivered | targetSdk 36 on Android 16+ | `android:enableOnBackInvokedCallback="false"` (described as temporary) | [API] |
| Orientation, resizability and aspect-ratio restrictions ignored at smallest width 600dp and up | targetSdk 36 | `PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`; removed at targetSdk 37 | [API] |
| Notification runtime permission under app control | targetSdk 33 | None | [API] |

Details: `references/platforms-system.md`, `references/platforms-large-screens.md`.

Source: https://developer.android.com/about/versions/15/behavior-changes-15, https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/about/versions/17/behavior-changes-17

## Core app quality

- [MD] The page describes itself as "the minimum quality that all apps should meet". It does not state that Google Play rejects apps for these items, except where an item quotes a Play rule. IDs are now names (older coded IDs such as `VD-1` or `FN-P1` are gone); each has a test `T-<ID>`.

| Area | ID | What it asks |
|---|---|---|
| Usability | `Consistent_UX` | Consistent experience for all use cases on all form factors |
| User interface | `Display_State_Parity` | Orientations and fold states expose essentially the same features |
| User interface | `Fullscreen_Display` | Fills the window in both orientations; not letterboxed after configuration changes |
| User interface | `Orientation_Transitions` | Rapid rotation and folding without rendering problems or lost state |
| Visual quality | `Graphic_Quality` | No distortion, blurring or pixelation; vector drawables where possible |
| Visual quality | `Line_Length` | Text lines limited to 45 to 75 characters including spaces |
| Visual quality | `Theme_Support` | App content and web content support light and dark themes |
| Navigation | `Back_Button_Nav` | Standard Back button; no custom on-screen back button prompts |
| Navigation | `Back_Gesture_Nav` | Gesture navigation for Back and Home |
| Navigation | `State_Preservation` | State kept when leaving the foreground; no accidental data loss on Back |
| Notifications | `Notification_Quality` | Relevant notifications; channels; no cross-promotion or advertising (quoted as strictly prohibited by the Play Store) |
| Notifications | `Conversation_Quality` | `MessagingStyle`, direct reply, conversation shortcuts for messaging apps |
| Accessibility | `Touch_Target_Size` | Touch targets at least 48dp |
| Accessibility | `Visual_Contrast` | 3:1 for large text and graphics; 4.5:1 for small text (under 18pt, or under 14pt bold) |
| Accessibility | `Content_Description` | Every UI element except `TextView` described with `contentDescription` |
| Functionality | `Video_PiP`, `System_Sharesheet` | Picture-in-picture for video; Android Sharesheet for sharing |
| Functionality | `Audio_Playback_Background`, `Audio_Notification_Style` | Worded with "must": foreground service and a `MediaStyle` notification for background audio |
| Performance | `App_Startup_Time`, `Rendering_Performance` | Feedback if loading exceeds two seconds; frames within 16 ms |
| Privacy | `Runtime_Permissions`, `Permission_Rationale`, `Graceful_Degradation`, `Minimize_Permissions` | Ask when the feature is used, explain why, keep working when denied, ask for the minimum |
| Identity | `Autofill_Hints`, `Credential_Manager`, `Biometric_Authentication` | Autofill hints; Credential Manager sign-in; biometrics for sensitive actions |

- [MD] The page also asks for Material Design components in place of platform components where possible.

Source: https://developer.android.com/docs/quality-guidelines/core-app-quality

## Adaptive app quality tiers

- [API] The adaptive app quality guidelines replace and extend the former large screen app quality guidelines (archived 2026-01-21, with an ID map). The old `LS-*` IDs are superseded, although the car quality page still cites some.
- [MD] The page calls Tier 3 "the baseline quality standard for apps on foldables and large screens on Google Play"; Tier 2 and Tier 1 qualify an app for enhanced promotion and store badging (Tier 2 for the Google Play large screen badge). Elsewhere Google states letterboxed apps are subject to decreased discoverability on Google Play for tablets, foldables and ChromeOS. No page read here says an app is rejected for missing a tier.
- [MD] Tier 3 apps must first fulfil the core app quality requirements.

| Tier | Name | Representative IDs |
|---|---|---|
| 3 | Adaptive ready | `Config_Changes` (fills the window, not letterboxed, not in compatibility mode, state kept across configuration changes), `Config_Combinations`, `Multi-Window_Functionality`, `Multi-Resume`, `Camera_Preview`, `Media_Projection`, `Keyboard_Input`, `Mouse_Trackpad_Basic` (click, select, scroll), `Stylus_Basic`, `Stylus_Text_Input` |
| 2 | Adaptive optimized | `Responsive_adaptive_layouts` (window size classes, rails that expand, grids that change column count, multi-pane canonical layouts), `UI_Secondary_Elements` (sheets, buttons, text fields not full width; context menus next to the item; rails replace navigation bars; drawers become expanded rails), `Touch_Targets` (48dp), `Drawable_Focus`, `Keyboard_Navigation` (Tab and arrows), `Keyboard_Shortcuts`, `Keyboard_Media_Playback` (Spacebar), `Keyboard_Send` (Enter), `Keyboard_Exit` (Esc), `Context_Menus` (right-click), `Content_Zoom` (Ctrl plus wheel, pinch), `Hover_States` |
| 1 | Adaptive differentiated | By experience. Desktop: `Scrollbar_Display`, `Hover_Parity`, `Desktop_Menus`, `UI_Config`, `Request_Fullscreen_Mode`, `Keyboard_Parity`, `Input_Combinations`, `Triple_Click`, `Multi-Instance`, `Drag_Drop_Support`, `Printing_Support`, `File_Picker`, `File_Handlers`, `Custom_Cursors`, `Cursor_Target_Size`, `Cross_Device_Handoff`, `Offline_Support`. Foldables: `Foldables_Postures` (tabletop for calls and playback, book for reading), `Foldables_Camera`, `Foldables_PiP`, `Foldables_Multi-Instance`. Stylus: `Stylus_Draw_Write`, `Stylus_Drag_Drop`, `Stylus_Enhanced`. Further experiences: camera and audio, cars, TV, XR, games, widgets |

- [MD] Test devices named by the page: Googlebook (160 ppi), foldable 1:1 inner display (802 x 802dp), foldable 4:3 inner display (1024 x 768dp), 8-inch tablet (1024 x 640dp), 10.5-inch tablet (1280 x 800dp), 13-inch Chromebook (1600 x 900dp).

Source: https://developer.android.com/docs/quality-guidelines/adaptive-app-quality, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-3, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/experiences/desktop, https://developer.android.com/develop/ui/compose/layouts/adaptive/adaptive-dos-and-donts

## Form-factor quality guidelines

| Form factor | What the page says about obligation | Tag | Details |
|---|---|---|---|
| Wear OS | "To publish on the Play Store, your watch app must satisfy all the applicable requirements"; failing them might lead to rejection | [Req] | `references/platforms-wear.md` |
| Android TV | Tier 3 "TV Ready" is the fundamental requirements to run on Android TV OS devices; Tiers 2 and 1 are graded improvements. Declaring the touchscreen as not required is stated as required to be considered a TV app on Google Play | [Req] for the manifest items and items worded "must"; [MD] for the rest | `references/platforms-tv.md` |
| Cars | Tier 3 must be met by parked categories, Tier 2 by driving categories, "to be accepted on the Google Play Store". Templated UX rules labelled MUST are enforced by the API or the quality guidelines | [Req] | `references/platforms-auto-xr.md` |
| Android XR | Separate guideline sets for immersive and augmented experiences; not read for this skill | [Unverified] | `references/platforms-auto-xr.md` |
| Widgets | Tiers: 3 low quality, 2 standard, 1 differentiated. `WL-4.2` states the minimum size must meet the 48 x 48dp touch target requirement | [MD], with `WL-4.2` worded as a requirement | `references/platforms-system.md` |

Source: https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/docs/quality-guidelines/tv-app-quality, https://developer.android.com/docs/quality-guidelines/car-app-quality, https://developer.android.com/develop/adaptive-apps/quality-guidelines/android-xr, https://developer.android.com/develop/adaptive-apps/quality-guidelines/widget-quality

## Accessibility numbers and their strength

| Number | Where and how it is worded | Strength |
|---|---|---|
| 48dp touch target | Android design accessibility page: ensure all touch targets are at least 48dp. Material layout guidance: "consider" 48 x 48dp for most platforms. Compose accessibility docs: set a 48dp minimum to follow Material guidance. Core `Touch_Target_Size` and adaptive `Touch_Targets`: at least 48dp | Recommendation and quality guideline on phones and large screens |
| 48 x 48dp | Wear OS `WO-V2`; widget `WL-4.2` | Stated as a requirement there |
| 44 x 44dp pointer target | Material layout guidance: "consider" for pointer targets | Recommendation |
| 56dp | Android XR recommended target | Recommendation |
| 8dp between targets | Material layout guidance; repeated for XR | Recommendation |
| Contrast 4.5:1 and 3:1 | Accessibility guide: recommended, thresholds in sp (text under 18sp, or bold under 14sp, needs 4.5:1). Core `Visual_Contrast`: same ratios with thresholds in pt. Design page: 4.5:1 for text, 3:1 for non-text against surfaces | Recommendation and quality guideline; the unit differs between pages |
| 12sp minimum body text | Android design accessibility page | Recommendation; on Wear OS 12sp essential and 10sp non-essential is `WO-V14` |
| 200% font scale | Android 14+ system capability; test at it | Platform fact plus recommendation |

Source: https://developer.android.com/design/ui/mobile/guides/foundations/accessibility, https://developer.android.com/guide/topics/ui/accessibility/apps, https://developer.android.com/develop/ui/compose/accessibility/api-defaults, https://m3.material.io/foundations/designing/structure, https://developer.android.com/docs/quality-guidelines/core-app-quality

## Claims versus what the docs say

| Claim people make | What the docs say |
|---|---|
| "48dp touch targets are mandatory" | Recommended in design and Material guidance and listed in core and adaptive quality guidelines. Worded as a requirement only for Wear OS (`WO-V2`) and widgets (`WL-4.2`) |
| "Portrait lock is fine on tablets" | At targetSdk 36 the lock is ignored on displays of sw600dp and up, with a temporary opt-out that ends at targetSdk 37. Guidance says not to lock orientation at all. On phones the lock is still honoured |
| "Edge-to-edge is a Play policy" | It is platform behaviour for apps targeting API 35+ on Android 15+. Play requires a target API level, which brings the behaviour with it |
| "You can still opt out of edge-to-edge" | Only at targetSdk 35, or at 36 when running on an Android 15 device |
| "Set the status bar colour to brand colour" | Deprecated and without effect at targetSdk 35 on Android 15+ |
| "Override onBackPressed for Back" | Not called at targetSdk 36 on Android 16+ unless the app opts out |
| "Large screen quality uses LS-C1, LS-U4 and so on" | Replaced in 2026 by adaptive app quality with named IDs |
| "Core app quality items are Play rejection reasons" | The page calls them the minimum quality all apps should meet; it does not describe enforcement, apart from items that quote Play rules |
| "Tablets need a navigation drawer" | Tier 2: navigation rails replace bars, and drawers are updated to expanded navigation rails |
| "There are three window size classes" | Five width classes (large from 1200dp, extra-large from 1600dp) and three height classes |
| "Material 3 Expressive is experimental" | Most of it is stable in material3 1.5.0; a few APIs still need an opt-in |
| "Leanback is the TV toolkit" | Deprecated; Compose for TV is recommended |
| "Wear apps must support rotary input" | `WO-V7` was retired in 2024; rotary support is recommended |
| "Wear OS apps must target API 34" | The Play target API page says 35 for Wear OS from 2026-08-31; the Wear quality page is out of date |
| "Dark theme is optional" | Core `Theme_Support` asks for light and dark; it is a quality guideline, not a publishing rule. On Wear OS the black background is `WO-V13` |
| "Car apps can use any UI if it is simple" | Driving categories use host-rendered templates; MUST rules are enforced by the API or car quality |

Source: https://developer.android.com/docs/quality-guidelines/core-app-quality, https://developer.android.com/about/versions/16/behavior-changes-16, https://developer.android.com/develop/adaptive-apps/quality-guidelines/adaptive-app-quality/tier-2, https://developer.android.com/docs/quality-guidelines/wear-app-quality, https://developer.android.com/google/play/requirements/target-sdk

## How to word a finding

- [Conv] Name the class first: "Google Play requirement", "Wear OS quality requirement WO-V13", "platform behaviour at targetSdk 36", "core app quality guideline Touch_Target_Size", "Material recommendation".
- [Conv] Quote the ID and the page; give the number with its unit exactly as the page does.
- [Conv] Never write that an app "will be rejected" or "will pass review". Say what the documentation states and, where it states a consequence (rejection possible for Wear, acceptance conditions for cars, reduced discoverability for letterboxed apps), repeat that consequence in the page's own strength.
- [Conv] Where two Google pages disagree, give both and say which is newer or more specific.
- [Conv] Google Play Console help and policy pages were not part of the sources for this skill; send policy questions there rather than answering from these guidelines.

Source: https://developer.android.com/docs/quality-guidelines/adaptive-app-quality, https://developer.android.com/docs/quality-guidelines/car-app-quality

## Common mistakes

| Mistake | Fix |
|---|---|
| Labelling every "should" as a Play requirement | Use the classes above; most UI guidance is recommendation or quality guideline |
| Labelling `targetSdk` behaviour as policy | It is platform behaviour, tagged [API] |
| Citing retired IDs (`LS-*`, `VD-1`, `WO-V7`) | Use the current named IDs; note retirements |
| One target API level for all form factors | 36 general; 35 Wear OS and Automotive OS; 34 TV and XR |
| Stating contrast thresholds without the unit caveat | Pages use sp in one place and pt in another |
| Predicting review outcomes | Report what the page states |
| Treating Tier 2 or Tier 1 as mandatory | They qualify for badging and promotion |
| Ignoring form-factor pages that do use "must" | Wear OS and car requirements are stated as conditions for publishing or acceptance |
