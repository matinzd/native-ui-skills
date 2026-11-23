# Cars and Android XR

Scope: the essentials for two form factors where the app does not own the screen in the usual way: Android Auto and Android Automotive OS (categories, templates, driver-distraction rules stated as MUST, parked versus driving tiers) and Android XR (Home Space and Full Space, spatial panels, orbiters, targets, library status), with pointers to the official pages for depth.
Verified: 2026-11-23 against the sources linked in each section (Android 16/17, Compose Material 3 1.5).

## Contents

- Cars: two platforms and the permitted categories
- Cars: templates, not custom UI
- Cars: UX requirements (MUST, SHOULD, MAY)
- Cars: quality tiers and distraction rules
- Cars: parked apps
- Cars: what does not apply
- XR: Home Space and Full Space
- XR: inputs
- XR: spatial panels, orbiters and elevation
- XR: targets, type, colour and comfort
- XR: libraries and their status
- XR: what does not apply
- Common mistakes

## Cars: two platforms and the permitted categories

- [API] Android Auto projects a driver-optimised experience from the phone (Android 9, API 28, or higher) to a compatible car display. Android Automotive OS (AAOS) is an Android system built into the vehicle; the app is installed on the car.
- [Req] Only certain app types are supported, and the app must not include features outside them (`PC-1`).

| Category | Built with | Platforms | Use |
|---|---|---|---|
| Media (audio) | `MediaBrowserService` and `MediaSession` | Both | Driving or parked |
| Messaging notifications | `MessagingStyle` notifications with reply and mark-as-read | Android Auto | Driving or parked |
| Templated messaging, calling | Car App Library | Android Auto | Driving or parked; limited to testing tracks at the time of writing |
| Navigation, point of interest, IoT, weather | Car App Library | Both | Driving or parked |
| Video | Views or Compose | AAOS | Primarily while parked |
| Games | Views or Compose | Both | Only while parked |
| Browsers | Views or Compose | AAOS | Only while parked; internal testing track |

- [API] Design is shared between the two platforms, but development produces two APKs: `androidx.car.app:app-projected` for Android Auto and `androidx.car.app:app-automotive` for AAOS, on top of `androidx.car.app:app` (1.7.0 stable).

Source: https://developer.android.com/training/cars, https://developer.android.com/training/cars/apps, https://developer.android.com/docs/quality-guidelines/car-app-quality

## Cars: templates, not custom UI

- [API] A driving app supplies models; the host (Android Auto or AAOS) renders them with vehicle-optimised templates and handles screen sizing. The app does not draw its own widgets, choose fonts, or control layout. Only navigation, POI and weather maps and the parked categories draw their own surface.
- [API] Structure: a `CarAppService` creates a `Session`, which manages a stack of `Screen` objects; each screen returns a template. The host's back button or the hardware back button pops the stack.
- [Req] The screen stack can have a maximum depth of five screens.

| Template | Shows |
|---|---|
| List, Grid | Items in a list or grid |
| Sectioned Item | Mixed browsing structure of lists and grids |
| Pane | Detail information and prominent actions, optional image |
| Message, Long Message | Brief or longer full-screen message with actions |
| Search | Search bar and results |
| Sign-in | Sign-in options |
| Tab | Tabs at the top switching between embedded templates |
| Navigation | Full-screen map with action strip and optional routing card (navigation apps) |
| Place List (map) | Locations next to a map drawn by the library (POI apps) |
| Map + Content | Map plus another template (navigation, POI, weather) |
| Media Playback | Now-playing view (media apps) |

- [API] Templates restrict their content (for example list item counts) and how they chain into a task flow; the limits vary by vehicle and are read through the constraints API.

Source: https://developer.android.com/design/ui/cars/guides/templates/overview, https://developer.android.com/training/cars/apps

## Cars: UX requirements (MUST, SHOULD, MAY)

Google's page defines MUST as required and enforced either in the API or in the car quality guidelines; SHOULD as recommended; MAY as optional. Selected rules for templated apps:

- [Req] MUST keep task flows to 5 steps or fewer.
- [Req] MUST NOT end a 5-step flow with a list-based template unless adaptive task limits are enabled; the fifth step is a Navigation, Message or Pane template.
- [Req] MUST get permission to access the car microphone before recording audio for voice input.
- [Req] MUST use the documented method to send Android Auto users to the phone for actions not allowed while driving, telling them to look only when it is safe.
- [Req] Purchase flows MUST NOT let users set up payment methods, commit to recurring payments, or select multiple items in one flow.
- [Req] Navigation and weather apps MUST meet contrast requirements for everything drawn on the map, draw only map and drive-related (or weather-related) content on the surface, and draw a light or dark map when instructed. Weather apps MUST NOT animate weather on the surface while driving or show more than 5 unique map annotations.
- [MD] SHOULD keep flows to 2 or 3 steps and offer shortcuts to earlier steps when a flow exceeds 3 screens.
- [MD] SHOULD provide a back button or other exit where no other action exists (loading screens, actionless Message and Pane templates).
- [MD] SHOULD show content for at least 8 seconds before an automatic transition removes it; SHOULD NOT chain automatic transitions.
- [MD] SHOULD NOT create stateful buttons such as toggles outside list rows.
- [MD] SHOULD provide two accent colours for dark and light backgrounds; SHOULD show useful content instead of an empty state on open.
- [MD] SHOULD keep images, icons and map markers at 36 x 36dp or larger and map text at 24dp or larger.
- [MD] Design principles: driving comes first; robust voice control; tasks easy to pause and resume; common tasks in three taps or fewer; text while driving limited to 1 to 3 lines and 120 characters.

Source: https://developer.android.com/design/ui/cars/guides/ux-requirements/overview, https://developer.android.com/design/ui/cars/guides/foundations/design-principles

## Cars: quality tiers and distraction rules

| Tier | Meaning | What the page says about acceptance |
|---|---|---|
| 3, Car ready | Large-screen compatible app usable while parked | Parked categories must meet all requirements in this tier to be accepted on Google Play |
| 2, Car optimized | Car-specific capabilities on the centre display | Apps in categories built for use while driving must meet all applicable requirements in this tier to be accepted |
| 1, Car differentiated | Adapts across driving and parked modes and across the car's screens | Optional |

Selected IDs (all worded with "must" on the quality page, so tagged as requirements for their categories):

| ID | Applies to | Rule |
|---|---|---|
| `PC-1` | All | No features outside the supported app types |
| `DD-3` | Video, games, browsers | Not launchable or usable while driving; no audio |
| `AR-1` | App-implemented activities on AAOS | Interactive elements not obstructed by system bars or display cutouts |
| `SA-1` | Driving categories | No animated elements such as animated graphics or video (canvas animation while parked is excepted when relevant to driving) |
| `IU-1` | Driving categories | No images, except one static context image (album art, logo), icons, and images that aid driving decisions |
| `ST-1` | Driving categories | No automatically scrolling text |
| `AC-1` | Templated categories | Tasks completable in five screens or fewer |
| `VC-1` | Media, navigation | Supports Gemini and Google Assistant voice commands |
| `DR-1`, `DR-2`, `DR-3` | Driving categories | Buttons respond within 2 seconds; app launches and loads content within 10 seconds |
| `VD-1` | Driving categories | Icons and colours meet Android Auto contrast requirements |
| `TH-1` | Templated categories | Custom theming with Car App Library 1.9+ supports light and dark |
| `MA-1` | Media | No autoplay without a user action |
| `IN-1`, `NA-1` | Driving categories | Notifications only when relevant to the driver; no advertisements in notifications |
| `PA-1` | Navigation, POI, IoT, weather | Simple purchase flows only |

- [API] The car page still cites large-screen IDs in the old `LS-*` form (for example `LS-U3` for touch targets) although the large-screen guidelines were replaced by the adaptive app quality guidelines in 2026.
- [Conv] Report car findings with the ID and category; do not predict review outcomes.

Source: https://developer.android.com/docs/quality-guidelines/car-app-quality

## Cars: parked apps

- [API] Video, game and browser apps are ordinary activities built with Views or Compose, shown on a large landscape display while the car is parked. The "Car ready mobile apps" programme can distribute eligible mobile apps that meet Tier 3 to cars with Google built in.
- [MD] Treat a parked app as a large-screen adaptive app (`references/platforms-large-screens.md`): no letterboxing, insets and cutouts handled (`AR-1`), touch targets per the large-screen guidance.
- [Req] It must not be launchable or usable while driving (`DD-3`); audio while driving is a separate, optional capability for video apps on capable devices.
- [Conv] If Google's Android skill for parked car apps (`android-for-cars-parked-apps` in android/skills) is installed, prefer it for the adaptation steps.

Source: https://developer.android.com/training/cars/parked, https://developer.android.com/training/cars/car-ready-mobile-apps, https://developer.android.com/docs/quality-guidelines/car-app-quality

## Cars: what does not apply

- [Conv] While driving: custom Compose or Views UI, Material theming beyond accent colours and what templates expose, your own navigation containers, free navigation depth, decorative images, animation, long text, dense lists.
- [Conv] Phone patterns such as bottom sheets, FABs, snackbars and gestures: the host decides presentation.
- [Conv] Assumptions about one screen size or theme: the host adapts templates per vehicle and switches light and dark.

Source: https://developer.android.com/design/ui/cars/guides/templates/overview

## XR: Home Space and Full Space

| | Home Space | Full Space |
|---|---|---|
| Apps visible | Several, side by side | One; others hidden |
| What runs | Any compatible mobile or large-screen app, unmodified | Spatialised app: spatial panels, 3D models, environments, spatial audio |
| Bounds | Default 1024 x 720dp; minimum 385 x 595dp; maximum 2560 x 1800dp | No space boundaries; panel maximum 2560 x 1800dp, no minimum |
| Launch | 1.75 metres from the user | App may set position; can open directly into Full Space |

- [MD] Apps that follow large-screen guidance adapt best in Home Space, so the first step toward XR is a good adaptive app.
- [MD] Give users a clear control to switch between the two spaces (collapse and expand icons are suggested).
- [API] Spatial capabilities can change while the app runs: check them before showing spatial UI and keep a 2D fallback. The start mode is declared with the manifest property `android.window.PROPERTY_XR_ACTIVITY_START_MODE`.
- [API] Environments: passthrough shows the real room with digital elements; a spatial environment replaces it (Full Space only). On wired XR glasses users still see their surroundings.

Source: https://developer.android.com/design/ui/xr/guides/foundations, https://developer.android.com/develop/xr/jetpack-xr-sdk/transition-home-space-to-full-space

## XR: inputs

- [API] Hand tracking: pinching index finger and thumb is the equivalent of a tap; a held pinch scrolls, moves and resizes. Also eye tracking, voice (dictation and commands through Gemini), Bluetooth keyboard, mouse and trackpad, and 6DoF controllers.
- [API] The system gesture menu offers Go back (same back stack behaviour as on mobile), Launcher and Recents.
- [MD] Do not rely on a single input method; confirm every action with visual or audio feedback; keep custom gestures comfortable and distinct from system gestures.
- [API] With eye tracking the system draws the hover highlight itself and the app does not receive hover or raw gaze data.

Source: https://developer.android.com/design/ui/xr/guides/foundations, https://developer.android.com/design/ui/xr/guides/visual-design

## XR: spatial panels, orbiters and elevation

- [API] Spatial UI is marked Preview and is available only in Full Space.
- [MD] Spatial panels are the containers for UI. Panels have 32dp rounded corners by default. Keep panels between 0.75 metres and 5 metres from the user; spawn the panel centre 1.75 metres away with its vertical centre 5 degrees below eye level; keep content within the central 41 degrees of the field of view. The system uses 0.868 dp-to-dmm, so UI appears larger than on a phone.
- [MD] An app may be decomposed into several panels in rows (flat or curved) or free positions; do not let panels overlap critical information.
- [MD] Orbiters are floating elements attached to a panel that hold controls such as a navigation rail, navigation bar or playback controls. Use them sparingly; recommended visual offset 20dp; do not overlap a panel by more than 50% of the orbiter's size; no absolute coordinates; not too far from the panel.
- [MD] Spatial elevation levels in the table: orbiter 16dp, `SpatialPopup` 32dp, `SpatialDialog` 56dp. The orbiter guidelines on the same page say orbiters are elevated 15dp by default: Google's page is inconsistent (15dp in text, 16dp in the table), and it warns the levels may change.
- [MD] Do not spatialise or elevate large planes such as bottom sheets and side sheets, or elements with scrolling content.

Source: https://developer.android.com/design/ui/xr/guides/spatial-ui, https://developer.android.com/design/ui/xr/guides/visual-design

## XR: targets, type, colour and comfort

- [MD] Targets: recommended 56 x 56dp or larger with a visual affordance of 48 x 48dp or larger; an app that already follows Material target sizes meets the minimum, though 56dp is optimal. Keep at least 8dp between targets; pointer targets must not overlap.
- [MD] Add hover and focus states to every interactive component.
- [MD] Text: 14dp or larger (the page writes dp, not sp) at normal weight or heavier.
- [MD] Support dark and light themes as on mobile. On see-through glasses dark colours emit less light and look transparent, brighter colours look more solid.
- [MD] Comfort: motion is more comfortable when the user controls it; avoid moving UI or environments quickly or unexpectedly; provide moments of rest; consider making motion optional; avoid continuous joystick locomotion.
- [API] XR quality guidelines are published as two sets, for immersive experiences (headsets, wired XR glasses) and for augmented experiences (audio and display glasses). Their contents were not read for this file. [Unverified]

Source: https://developer.android.com/design/ui/xr/guides/visual-design, https://developer.android.com/design/ui/xr/guides/motion, https://developer.android.com/design/ui/xr/guides/considerations, https://developer.android.com/develop/adaptive-apps/quality-guidelines/android-xr

## XR: libraries and their status

| Library | Provides | Status on 2026-11-23 | Tag |
|---|---|---|---|
| `androidx.xr.compose:compose` | `Subspace`, `SpatialPanel`, `Orbiter`, `SpatialRow`, `SpatialColumn`, `SpatialBox`, `SpatialDialog`, `SpatialPopup` | 1.0.0-rc01; no stable release yet | [API] |
| `androidx.xr.compose.material3` | Material 3 for XR: `SpatialNavigationRail`, `SpatialWideNavigationRail`, `SpatialNavigationBar`, `SpatialShortNavigationBar`, `SpatialTopAppBar`, `SpatialBasicAlertDialog`, `SpatialListDetailPaneScaffold` | Experimental; needs `@OptIn(ExperimentalMaterial3XrApi::class)` | [API] |
| `androidx.xr.glimmer:glimmer` | Jetpack Compose Glimmer, the design system for transparent-display glasses | 1.0.0-alpha22 | [API] |

- [API] Check `LocalSpatialCapabilities.current.isSpatialUiEnabled` and render the ordinary Material 3 component when it is false.
- [API] Manifest features: `android.software.xr.api.spatial` (Jetpack XR SDK) or `android.software.xr.api.openxr` (Unity, Godot, Unreal, OpenXR). Google Play's target API floor for Android XR is 34.
- [MD] Unity, OpenXR and WebXR apps may use any design language; the target, type and comfort guidance still applies.

Source: https://developer.android.com/develop/xr/jetpack-xr-sdk/material-design, https://developer.android.com/jetpack/androidx/releases/xr-compose, https://developer.android.com/jetpack/androidx/releases/xr-glimmer, https://developer.android.com/develop/xr/package-and-distribute

## XR: what does not apply

- [Conv] Edge-to-edge and system-bar insets as on a phone: a panel has its own bounds.
- [Conv] Orientation: a panel is a resizable window, not a rotating screen.
- [Conv] Touch-first assumptions: no long-press-only actions, no tiny targets, no reliance on hover data.
- [Conv] Phone-style bottom sheets as spatialised surfaces: keep them flat inside the panel.

Source: https://developer.android.com/design/ui/xr/guides/spatial-ui

## Common mistakes

| Mistake | Fix |
|---|---|
| Designing custom screens for a driving app | Choose templates; supply data, icons and accent colours |
| Flow of six or more screens in the car | 5 steps maximum (MUST), aim for 2 or 3 |
| Media app built on Car App Library templates from scratch | Media uses `MediaBrowserService` and `MediaSession`; the host shows playback UI |
| App type outside the supported categories | Not permitted (`PC-1`); only a parked category may fit |
| Video or game reachable while driving | Block while driving (`DD-3`) |
| Animated lists, marquee text, decorative images in driving UI | Remove (`SA-1`, `ST-1`, `IU-1`) |
| One hard-coded map theme | Draw light or dark when instructed |
| XR app that only works in Full Space | Start from an adaptive app that works in Home Space; add a space toggle |
| Spatial UI shown without a capability check | Check `isSpatialUiEnabled`, fall back to 2D |
| Many orbiters around every panel | A few key navigation or control orbiters |
| Thin 12dp text and 40dp targets on a panel | 14dp or larger text, 56dp targets |
| Treating XR Material 3 as stable | It is experimental; Compose for XR is at release candidate |
| Quoting one orbiter elevation | The page says 15dp in text and 16dp in its table |
