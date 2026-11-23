# 01 — Apple HIG: foundations, accessibility, navigation, components, inputs

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Research date: 2026-11-23. Source: DocC render JSON for every HIG page (171 pages fetched, all HTTP 200), from
`https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`; TOC from
`https://developer.apple.com/tutorials/data/index/design--human-interface-guidelines`.

Conventions
- Canonical human URL for any page: `https://developer.apple.com/design/human-interface-guidelines/<slug>` (written below as `/<slug>`).
- **[V]** = read in the fetched page this session. **[M]** = memory / not verified. Everything below is [V] unless tagged [M].
- Strength tags: **REQ** = HIG uses must/always/never/"don't" or it is an App Review / platform contract; **REC** = HIG
  recommendation ("prefer", "consider", "avoid", "in general", "aim", "strive"). The HIG is overwhelmingly REC; even the
  hit-target and contrast numbers are phrased "as a general rule" / "strive to meet". Treat REC numbers as review warnings, not hard failures.
- "Changelog" dates are the latest entry on that page; use them to judge freshness.

---

## 0. What changed vs. common lore (read this first)

| Common lore | What the current HIG says [V] | Page |
|---|---|---|
| HIG has no principles page / principles are "Clarity, Deference, Depth" | A **Design principles** page was reintroduced June 8, 2026 with eight principles: Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight | `/design-principles` |
| "Navigation bars" is a component page | No `navigation-bars` page exists. Navigation bar guidance lives in **Toolbars** ("In iOS, a navigation-specific toolbar is sometimes called a navigation bar") | `/toolbars` |
| iPhone tab bar: "3 to 5 tabs, max 5" | No numeric tab limit on the page. Guidance is "use the appropriate number", "avoid overflow tabs" (the More tab), and for customizable iPad tab bars "a default list of five or fewer" | `/tab-bars` |
| iOS tab bar is an opaque bar pinned to the bottom edge | Tab bar "floats above content at the bottom of the screen" on a Liquid Glass background; can minimize on scroll; can host a trailing search tab. iPadOS tab bar sits near the top and can convert to a sidebar | `/tab-bars` |
| Layout page lists device screen sizes / margins | No device-dimension table is in the current Layout page (updated Sept 9, 2026). It defers to Apple Design Resources for margins and safe areas. Do not quote point sizes of devices from the HIG | `/layout` |
| Use translucent/custom bar backgrounds and tinted bar buttons for brand | "Reduce the use of toolbar backgrounds and tinted controls"; use scroll edge effects instead of a solid or semi-opaque background under controls | `/toolbars`, `/layout` |
| Contrast: just "4.5:1" | Accessibility page gives the WCAG AA table (4.5:1 up to 17 pt; 3:1 at 18 pt+ or bold) and names APCA as an alternative. Dark Mode page separately says minimum 4.5:1 and "strive for 7:1" for custom colors, especially small text | `/accessibility`, `/dark-mode` |
| Minimum hit target is 44x44 pt, full stop | Accessibility page has a per-platform table with a **default** and a smaller **minimum** control size (iOS 44 default / 28 minimum; macOS 28 / 20; tvOS 66 / 56; visionOS 60 / 28; watchOS 44 / 28). Buttons page still says hit region "at least 44x44 pt — in visionOS, 60x60 pt" | `/accessibility`, `/buttons` |
| Mac is pointer/keyboard only | As of Oct 28, 2026 the Gestures, Pointing devices and Designing for macOS pages cover **Mac with a touch display** (enlarge tap targets, not controls; reveal hidden controls on tap) | `/gestures`, `/pointing-devices` |
| iPhone is one display | New page **Designing for iPhone Duo** (Sept 9, 2026): two displays, hinge, vertical side bars, reserved regions, arrangement views | `/designing-for-iphone-duo` |
| App icons are flattened PNG sets per size | Layered icons, Icon Composer format, appearances: default, dark, clear light/dark, tinted light/dark; 1024x1024 px layout for iOS/iPadOS/macOS | `/app-icons` |
| Switches anywhere on iOS | "Use the switch toggle style only in a list row"; outside a list use a button that behaves like a toggle | `/toggles` |
| Dynamic Type guidance is on Accessibility | Moved to Typography (March 7, 2025); VoiceOver moved to its own page | `/typography`, `/voiceover` |

---

## 1. Foundations

### 1.1 Design principles — `/design-principles` (reintroduced June 8, 2026)
All REC ("no one right way to apply these"). Use as the skill's rationale vocabulary.

| Principle | One-line | Sub-rules worth encoding |
|---|---|---|
| Purpose | Make something meaningful | Keep focused on most important features; avoid re-creating existing solutions |
| Agency | Let people do things their own way | Stay out of the way; guided flows must be easy to skip or escape; make recovery from mistakes easy |
| Responsibility | Act in people's best interest | Clear rationale when asking permission; collect only what is needed |
| Familiarity | Build on what people know | Consistent visuals and interactions; clear feedback using system patterns for alerts and choices |
| Flexibility | Adapt to diverse contexts and needs | Accessibility from the start; keep content and controls in predictable positions across configurations; many input methods; each platform gets equal care |
| Simplicity | Be clear and direct | "Simplicity isn't minimalism"; concise wording; recognizable controls and consistent structure |
| Craft | Care about every detail | Prototype and iterate; keep current with platform capabilities after shipping |
| Delight | Make it human | "Don't mistake delight for decoration" |

### 1.2 Layout — `/layout` (changelog Sept 9, 2026)
- Visual hierarchy (REC): most important items near top and leading side; align to aid scanning, indent to show subordination;
  group with negative space, container shapes, or separators; use progressive disclosure.
- Differentiate controls from content (REC): use Liquid Glass for controls; do not put a solid or semi-opaque background under
  controls, use a scroll edge effect; extend full-screen background content under sidebars, toolbars, and tab bars; background
  extension effect (`backgroundExtensionEffect()`, `UIBackgroundExtensionView`) mirrors and blurs imagery under sidebars and inspectors.
- Adaptability: handle size classes, screen sizes, orientations and aspect ratios, Dynamic Island, external displays, Display Zoom,
  resizable windows, text-size changes, RTL and locale formatting. Respect system safe areas, margins, and guides.
- Text-size changes (REC, strongly worded: apps that ignore it "can be difficult or impossible to use"): stack horizontally adjacent
  views vertically; let rows grow in height; allow multi-line.
- Artwork (REQ wording "don't"): do not change the aspect ratio of background artwork; scale to fill.
- Size classes (iOS, iPadOS): "Determine layout based on size classes, not device type or orientation." Consider all four
  combinations. "Don't change your app's functionality based on the space it occupies" (you may change how much is visible, for example tab bar to sidebar).
- Safe area: "Respecting the safe area is essential" so hardware features and system UI do not obstruct content.

| Platform | Layout specifics on the page |
|---|---|
| iOS, iPadOS | No additional considerations |
| macOS | Avoid controls or critical info at the bottom of a window; avoid content behind the camera housing |
| tvOS | Safe area: inset primary content **60 pt top and bottom, 80 pt sides**. Grids: horizontal spacing 40 pt, minimum vertical spacing 100 pt; unfocused content width by column count: 2=860, 3=560, 4=410, 5=320, 6=260, 7=217, 8=184, 9=160 pt. Leave room for focus scaling |
| visionOS | Support resizing; do not use min/max size to prevent resizing; keep content centered at large sizes; button centers **at least 60 pt apart**; supplemental content goes in an adjacent window, not an ornament; 3D content sparingly in windows |
| watchOS | No more than three glyph buttons or two text buttons side by side; prefer full-width text buttons |

iPhone Duo (`/designing-for-iphone-duo`): compact width on outer display, regular width on inner display; avoid fixed widths
and display-specific dependencies; system moves toolbars, tab bars, and navigation controls to the side (vertical axis), and
they do not flip in RTL; "In general, don't override the default bar placement"; provide both title and symbol for each
non-text toolbar item; keep text-based buttons to a minimum; use the system overflow menu and reserve the ellipsis for it;
prefer an even number of grid columns so content divides at the fold; reserved regions (outer camera, inner camera, folding region).

### 1.3 Typography — `/typography` (changelog Dec 16, 2025)

Default and minimum sizes (REC, same table also on `/accessibility`):

| Platform | Default | Minimum |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

iOS/iPadOS text styles at the default Dynamic Type size (Large): size / leading in pt, weight, emphasized weight.

| Style | Size/leading | Weight | Emphasized | | Style | Size/leading | Weight | Emphasized |
|---|---|---|---|---|---|---|---|---|
| Large Title | 34/41 | Regular | Bold | | Callout | 16/21 | Regular | Semibold |
| Title 1 | 28/34 | Regular | Bold | | Subhead | 15/20 | Regular | Semibold |
| Title 2 | 22/28 | Regular | Bold | | Footnote | 13/18 | Regular | Semibold |
| Title 3 | 20/25 | Regular | Semibold | | Caption 1 | 12/16 | Regular | Semibold |
| Headline | 17/22 | Semibold | Semibold | | Caption 2 | 11/13 | Regular | Semibold |
| Body | 17/22 | Regular | Semibold | | | | | |

- Body across sizes: xSmall 14, Small 15, Medium 16, Large 17, xLarge to xxxLarge up to 23; accessibility sizes AX1 to AX5 with Body 53/62 and Large Title 60/70 at AX5.
- macOS built-in styles (no Dynamic Type on macOS): Large Title 26/32, Title 1 22/26, Title 2 17/22, Title 3 15/20, Headline 13/16 Bold, Body 13/16, Callout 12/15, Subheadline 11/14, Footnote 10/13, Caption 1 10/13, Caption 2 10/13 Medium.
- tvOS built-in styles: Title 1 76/96, Title 2 57/66, Title 3 48/56, Headline 38/46, Subtitle 1 38/46, Callout 31/38, Body 29/36, Caption 1 25/32, Caption 2 23/30 (Medium weight except Subtitle 1).
- watchOS (Large, default for 40/41/42 mm): Large Title 36, Title 1 34, Title 2 28, Title 3 19, Headline 16 Semibold, Body 16, Caption 1 15, Caption 2 14, Footnote 1 13, Footnote 2 12.
- visionOS: bolder Body and Title styles; adds Extra Large Title 1 and 2; prefer 2D text; billboard text attached to points in space.
- Rules (REC): avoid Ultralight, Thin, Light weights; minimize number of typefaces; use built-in text styles for Dynamic Type
  support; if three or more lines, avoid tight leading; custom fonts must implement Dynamic Type and Bold Text behavior
  ("make sure it implements the same behaviors"); do not embed system fonts (developer note, "don't"); scale meaningful
  icons with text (SF Symbols do this automatically); keep truncation minimal at large sizes; at large sizes switch to
  stacked layouts and reduce column count; keep hierarchy consistent at all sizes; not every element must grow (tab titles are an example).
- System fonts: SF Pro (iOS, iPadOS, macOS, tvOS, visionOS), SF Compact (watchOS; SF Compact Rounded in complications), New York serif. Dynamic Type exists on iOS, iPadOS, tvOS, visionOS, watchOS.
- Tracking tables exist per platform (for mockups only; the system applies tracking at runtime).

### 1.4 Color — `/color` (changelog Dec 16, 2025)
- REC: do not use the same color for different meanings (for example brand color on both interactive and non-interactive text).
- REC: every custom color needs light and dark variants plus an increased-contrast option for each; provide both even if the app ships one appearance, "to support Liquid Glass adaptivity".
- "Avoid hard-coding system color values"; values in the docs are reference only and can change per release.
- "Avoid redefining the semantic meanings of dynamic system colors" (example: do not use separator as a text color).
- Inclusive color: never rely on color alone to differentiate, indicate interactivity, or convey essential information.
- Liquid Glass color: glass has no inherent color; apply color sparingly; to emphasize a primary action, color the
  **background** (prominent style), not the symbol or text; do not color the backgrounds of multiple controls; with colorful
  content prefer monochromatic toolbars and tab bars; check resting-state legibility of content under controls.
- System colors (SwiftUI names): red, orange, yellow, green, mint, teal, cyan, blue, indigo, purple, pink, brown; iOS grays systemGray to systemGray6. visionOS uses the dark values.
- iOS backgrounds: system set (`systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground`) versus grouped set (`systemGroupedBackground` and its secondary and tertiary) for grouped tables. Foreground: `label`, `secondaryLabel`, `tertiaryLabel`, `quaternaryLabel`, `placeholderText`, `separator`, `opaqueSeparator`, `link`.
- macOS: long list of `NSColor` semantic colors; app accent color applies only when the user's accent setting is multicolor.
- tvOS: do not indicate focus with color alone. visionOS: use color sparingly on glass, prefer it in bold text and large areas. watchOS: avoid full-screen background color on long-lived screens.
- Color management: sRGB default; Display P3 at 16 bits per channel for wide color; PNG export.

### 1.5 Dark Mode — `/dark-mode` (changelog Aug 6, 2024)
- "Avoid offering an app-specific appearance setting" (REC). Must look good in both modes and when Auto switches mid-session.
- Contrast: "At a minimum ... no lower than 4.5:1"; custom foreground/background "strive for a contrast ratio of 7:1, especially in small text".
- Use semantic colors and Color Set assets; "avoid using hard-coded color values or colors that don't adapt".
- Test with Increase Contrast and Reduce Transparency, separately and together.
- iOS/iPadOS: base versus elevated background sets; prefer system background colors so elevation works.
- Soften white backgrounds in content images. Dark-only UI is acceptable "in rare cases" (immersive media).
- Dark Mode is not supported in visionOS or watchOS.

### 1.6 Materials and Liquid Glass — `/materials` (changelog Sept 9, 2025)
- Two material families: **Liquid Glass** (functional layer for controls and navigation, floats above content) and **standard materials** (structure within the content layer).
- "Don't use Liquid Glass in the content layer" (REQ wording). Exception: transient interactive parts of controls such as sliders and toggles.
- "Use Liquid Glass effects sparingly" on custom controls; standard components get it automatically.
- Variants: **regular** (blurs and adjusts luminosity; use for text-heavy components such as alerts, sidebars, popovers) and
  **clear** (only over visually rich media backgrounds). With clear over bright content, add a dark dimming layer of **35% opacity**.
- Standard materials: choose by semantic purpose, not apparent color; use vibrant colors on top. iOS/iPadOS: ultra-thin, thin,
  regular (default), thick; avoid quaternary vibrancy on thin and ultra-thin. tvOS table: ultraThin (full-screen, light scheme), thin
  (overlay, light), regular (overlay), thick (overlay, dark). visionOS: glass is system-defined; prefer translucency to opaque
  colors; thin for interactive elements, regular for sections, thick for dark elements on regular. watchOS: do not remove default material backgrounds on modal sheets.

### 1.7 Icons, SF Symbols, app icons, images
- `/icons` (June 9, 2025): simplified, consistent weight with adjacent text; vector formats (PDF, SVG) for custom icons;
  alt text for custom icons; no replicas of Apple hardware; a table of standard SF Symbols for common actions (for example
  Cut `scissors`, Copy `document.on.document`, Paste `document.on.clipboard`, Done `checkmark`, Cancel `xmark`, Delete `trash`).
  macOS document icon sizes from 16x16 px to 512x512 px at 1x and 2x.
- `/sf-symbols` (July 28, 2025; SF Symbols 7): rendering modes monochrome, hierarchical, palette, multicolor; gradients; variable
  color is for change, not depth; animations appear, disappear, bounce, scale, pulse, variable color, replace, magic replace,
  wiggle, breathe, rotate, draw on/off; apply animations judiciously; custom symbols need alt text and must not replicate Apple products.
- `/app-icons` (Oct 28, 2026): layered design, Icon Composer; keep primary content centered; text only when essential; prefer
  illustration over photos; no UI replicas, no Apple hardware; keep features consistent across appearances. Alternate icons are subject to App Review (REQ).

| Platform | Layout size | Shape after masking | Appearances |
|---|---|---|---|
| iOS, iPadOS, macOS | 1024x1024 px | Rounded rectangle | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | 800x480 px | Rounded rectangle (landscape), parallax layers | n/a |
| visionOS | 1024x1024 px | Circular, 3D layers | n/a |
| watchOS | 1088x1088 px | Circular | n/a |

- `/images`: scale factors — iOS @2x and @3x; iPadOS and watchOS @2x; macOS and tvOS @1x and @2x; visionOS @2x or higher.

### 1.8 Motion — `/motion` (changelog Sept 9, 2025)
- REC: purposeful motion only; "Make motion optional" and never the only way to convey important information; brief, precise
  feedback animations; avoid motion on frequent interactions; let people cancel motion (do not block input on animation).
- Games: 30 to 60 fps. visionOS: avoid motion at the edge of the field of view; avoid sustained oscillation, particularly around **0.2 Hz**; prefer fades for relocating objects.
- Reduce Motion behavior is specified on `/accessibility` (see section 2).

### 1.9 Writing, inclusion, privacy, branding, right to left
- `/writing` (Dec 16, 2025): verb-led button and link labels; no "Click here"; avoid "we"; consistent capitalization; error
  messages next to the problem, no blame, say how to fix; empty states give next steps; text field hints say what to do
  ("Use only letters for your name") instead of what not to do.
- `/inclusion`: plain language, define technical terms, avoid unnecessary gender references; if gender is required offer nonbinary, self-identify, and decline to state; avoid stereotypes; people-first language.
- `/privacy` (June 21, 2023) — contains real requirements:
  - REQ: provide privacy details on submission; request permission via system alerts; show the App Tracking Transparency alert before collecting tracking data; "Never precede the system-provided alert with a custom screen or window that could confuse or mislead people".
  - REC: request only needed data; avoid requesting at launch unless required to function; purpose strings in sentence case, active voice, ending with a period, stating how and why.
  - Pre-alert screen: only one button, which opens the system alert; no cancel or close path (REQ wording "don't").
  - Data protection: "Never store passwords or other secure content in plain-text files"; use keychain; avoid custom authentication schemes; prefer passkeys.
- `/branding` (Sept 9, 2026): branding defers to content; do not put the logo everywhere; "Avoid using a launch screen as a branding opportunity"; Apple trademarks must not appear in app name or images (REQ).
- `/right-to-left`: flip navigation and progress controls (back button points right in RTL); do not flip numerals within a
  number, logos, checkmarks, photos, or real-world-object icons; align paragraphs by their language; increase Arabic or Hebrew font size by about 2 pt next to all-caps Latin.

---

## 2. Accessibility — `/accessibility` (changelog June 9, 2025), `/voiceover` (March 7, 2025)

Concrete numbers (all REC: "strive to meet", "ideally"):

| Item | Value |
|---|---|
| Text enlargement | Support at least 200% (140% on watchOS) |
| Contrast, text up to 17 pt, any weight | 4.5:1 |
| Contrast, text 18 pt and larger | 3:1 |
| Contrast, bold text any size | 3:1 |
| Standards named | WCAG (Level AA values used by Accessibility Inspector) and APCA |
| Padding around bezeled elements | about 12 pt |
| Padding around elements without a bezel | about 24 pt (from visible edges) |

| Platform | Default control size | Minimum control size |
|---|---|---|
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

- If the default palette misses the contrast minimum, at least provide a higher-contrast scheme when Increase Contrast is on; check both light and dark.
- Color independence: convey information with shape, icon, or text in addition to color; red-green and blue-orange pairs are called out.
- Hearing: captions, subtitles, audio descriptions, transcripts; pair audio cues with haptics and visual cues.
- Mobility: simplest gestures for frequent actions; avoid custom multifinger and multihand gestures; every gesture needs an
  on-screen alternative (swipe-to-dismiss also needs a button); label elements for Voice Control; test VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control, Switch Control.
- Keyboard: do not override system keyboard shortcuts; work with Full Keyboard Access.
- Cognitive: minimize time-boxed, auto-dismissing UI; prefer explicit dismissal; no autoplaying audio or video without controls; respect Dim Flashing Lights.
- **Reduce Motion**: reduce automatic and repetitive animation including zooming, scaling, peripheral motion; tighten springs to
  reduce bounce; track animation to the gesture; avoid animating z-axis depth changes; replace x/y/z transitions with fades; avoid animating into and out of blurs.
- Assistive Access (iOS, iPadOS): strip to core functionality; one interaction per screen; "Always ask for confirmation twice" for hard-to-recover actions.
- visionOS: keep UI in field of view, prefer horizontal layouts, do not head-anchor content, minimize large or repetitive gestures.
- VoiceOver (`/voiceover`): alternative labels for all key elements; describe meaningful images; exclude decorative images;
  make charts accessible; use titles and headings; specify grouping and order; announce layout and content changes; support the rotor.
- Accessibility Nutrition Labels on the App Store are referenced as the way to declare support.

---

## 3. Navigation and information architecture

### 3.1 Tab bars — `/tab-bars` (June 8, 2026)
- Navigation only, never actions (use a toolbar for actions). Keep the tab bar visible across sections except under modals.
- "Don't disable or hide tab bar buttons, even when their content is unavailable"; explain empty sections.
- Avoid overflow (More tab). Labels: single words where possible. Prefer filled SF Symbols. Badges only for critical information.
- Avoid similar color for tab labels and content backgrounds.
- iOS: floating glass bar at bottom; optional minimize-on-scroll with accessory (`TabBarMinimizeBehavior`); optional trailing search tab.
- iPadOS: tab bar near top; `tabBarOnly` or `sidebarAdaptable`; "Prefer a tab bar for navigation"; let people customize; default list of five or fewer.
- tvOS: height 68 pt, top edge 46 pt from top of screen, not changeable. visionOS: always vertical on the leading side; symbol plus short label required. macOS: none. watchOS: not supported.

### 3.2 Sidebars — `/sidebars` (June 8, 2026)
- No more than two levels of hierarchy; deeper needs a split view with a content list column.
- Let people hide the sidebar but do not hide it by default; allow customization; extend rich content beneath it.
- iOS/iPadOS: "Consider using a tab bar first". macOS: avoid critical info or actions at the bottom; auto-hide on window resize. visionOS: sidebar within a tab for deep hierarchy.

### 3.3 Toolbars (including navigation bars and titles) — `/toolbars` (Dec 16, 2025)
- Avoid overcrowding; the system adds the overflow menu on iPadOS and macOS — "Don't add an overflow menu manually" and avoid layouts that overflow by default.
- Reduce custom backgrounds and tinted controls; avoid label colors similar to content.
- Titles: useful per-window title; "Don't title windows with your app name"; keep the title **under 15 characters**.
- Navigation: use standard Back and Close buttons with standard symbols; do not use text labels "Back" or "Close".
- Actions: prefer borderless system symbols; `.prominent` style for key actions such as Done or Submit.
- Grouping: by function and frequency; **maximum of about three groups**; keep text-labeled actions separate; consistent placement across platforms.
- iOS: only the most important items in the main bar; large title for orientation. iPadOS: toolbar can share the row with the tab bar.
  macOS: every toolbar item must also be a menu bar command (REC "make"). visionOS: avoid vertical toolbars and pull-down menus in toolbars. watchOS: toolbar buttons in corners.

### 3.4 Split views — `/split-views` (June 9, 2025)
- Persistently highlight the current selection in each pane leading to the detail. iOS: prefer split views in regular, not compact, environments.
  macOS: sensible min and max pane sizes; thin divider (1 pt). visionOS: prefer a split view to a new window for supplementary info. watchOS: show most relevant detail automatically.

### 3.5 Search — `/searching`, `/search-fields` (June 8, 2026)
- Single search location; show the current scope; suggestions; consider privacy before showing history.
- Placeholder text describing what is searchable; search as people type when possible; scope bars default to the broader scope; tokens for common filters.
- iOS placements: search as a tab; search in a toolbar (bottom if there is room, top otherwise); inline field above the list it searches.
- iPadOS/macOS: trailing side of the toolbar; top of sidebar when filtering it; dedicated search area in sidebar or tab bar for discovery.

### 3.6 Modality and presentations
- `/modality` (Dec 5, 2023): modal only for clear benefit; keep tasks short; avoid an "app within your app"; "Always give
  people an obvious way to dismiss a modal view"; confirm before closing if work would be lost; title the modal task; one modal at a time (alerts are the exception).
- `/sheets` (March 24, 2026): one sheet at a time; "always pair [Done] with a Cancel button" or a Back button; "Avoid showing
  all three buttons — Cancel, Done, and Back — together". iOS/iPadOS: Cancel on the leading edge of the top toolbar, Done on
  the trailing edge; detents large and medium (about half); include a grabber for resizable sheets; support swipe to dismiss,
  with an action sheet if unsaved changes; iPad prefers page or form sheet styles. macOS: do not block other app windows; use a
  panel for repeated input. visionOS: center the sheet, do not emerge from the bottom edge, do not cover most of the window. watchOS: brief and occasional.
- `/alerts` (Feb 2, 2024): use sparingly; not for mere information; not for common undoable actions even if destructive; not
  at app start. Up to three buttons. Title specific (not "Error"), no more than two lines. Button titles one or two words,
  verbs; "OK" only for purely informational alerts; avoid Yes/No; "Always use 'Cancel'" for the cancel button. Default button on
  the trailing side or top of stack; Cancel leading or bottom; never make Cancel the default; destructive style only for
  destructive actions the person did not deliberately choose; destructive alerts include Cancel. Support Esc and Command-Period.
  iOS: avoid scrolling alerts. visionOS accessory view: max height 154 pt, 16 pt corner radius.
- `/action-sheets` (confirmation dialogs in SwiftUI): for choices related to an intentional action; title fits one line;
  destructive choices at the top with destructive style; Cancel at the bottom; avoid scrolling; watchOS no more than four
  buttons including Cancel. Not supported in visionOS. iOS: use an action sheet, not a menu, for choices following an action.
- `/popovers`: small amount of content; arrow points at the source; one popover at a time, "Never show a cascade or hierarchy
  of popovers"; nothing on top except an alert; "Always save work when automatically closing a nonmodal popover"; animate size changes.

### 3.7 Menus — `/menus` (June 8, 2026), `/context-menus`, `/pull-down-buttons`, `/pop-up-buttons`
- Menus: title-style capitalization; drop articles; show unavailable items as unavailable (dimmed); ellipsis when more input is
  needed; icons sparingly and uniformly within a group; important items first; submenus sparingly and shallow.
- Context menus: every item must also be available in the main interface ("Always"); small number of items; submenus one level;
  **hide** unavailable items instead of dimming (macOS exception: Cut, Copy, Paste); about three groups at most; no keyboard
  shortcuts shown; warn on destructive items (iOS, iPadOS, visionOS); iOS: context menu or edit menu for an item, not both.
- Pull-down buttons: for commands related to the button; do not hide all primary actions in one; at least three items;
  confirm destructive items with an action sheet.
- Pop-up buttons: flat list of mutually exclusive options; useful default; label predicts options.

### 3.8 Flow patterns
- `/onboarding` (June 10, 2024): teach by interactivity; brief; optional tutorial that is not re-shown but remains findable; do
  not teach system features; avoid licensing details in onboarding; postpone nonessential setup; let people try before rating or purchase prompts.
- `/launching` (June 10, 2024): launch instantly; launch screen (required on iOS, iPadOS, tvOS; not on macOS, visionOS,
  watchOS) should look nearly identical to the first screen; no text; "Don't advertise", no logos unless part of the first screen; restore previous state.
- `/loading` (June 9, 2025): show something immediately; allow other work while loading; determinate indicator when duration is known; watchOS avoid loading indicators.
- `/settings` (June 10, 2024): good defaults; minimize settings; do not duplicate systemwide settings; task-specific options in
  context; macOS: Settings item in the App menu (Command-Comma), not a toolbar button.
- `/entering-data`: get data from the system instead of asking; "Never prepopulate a password field"; offer choices over typing; validate dynamically; mark required fields.
- `/feedback`: integrate status into the interface; alerts only for critical, ideally actionable information; warn only for
  unexpected and irreversible data loss; watchOS avoid indeterminate indicators.
- `/undo-and-redo`: multiple undo levels; show the result; iOS/iPadOS do not redefine three-finger swipe and shake; macOS Edit menu plus standard shortcuts.
- `/drag-and-drop`: support widely, always with a non-drag alternative; between apps it is always a copy; drag image appears after about 3 pt of movement; show valid and invalid destinations; prefer undoable drops.
- `/managing-accounts`: delay sign-in as long as possible; prefer passkeys if not using Sign in with Apple; name the
  authentication method and only ones available on the device; **REQ: apps that create accounts must offer account deletion in-app or a direct link**.
- `/going-full-screen` (June 9, 2025): do not programmatically resize windows; keep essential controls reachable; let people
  choose when to enter and exit; temporarily hide toolbars to prioritize content; macOS use the system full-screen experience.

---

## 4. Controls and components

| Component | Key rules (strength) | Platform notes | Slug |
|---|---|---|---|
| Buttons | Hit region "at least 44x44 pt — in visionOS, 60x60 pt" (REC, "general rule"); always a press state for custom buttons; one prominent style for the most likely action; distinguish by style, not size; "Don't assign the primary role to a button that performs a destructive action" | iOS: activity indicator inside button for slow actions. macOS: ellipsis when opening another window; one help button per window; about 10 px padding in image buttons. visionOS sizes: mini 28, small 32, regular 44, large 52, extra large 64 pt; centers 60 pt apart; 4 pt padding if 60 pt or larger; avoid white fill with black text. watchOS: full-width primary buttons | `buttons` |
| Toggles | Two opposing states only; state must not rely on color alone | iOS: switch only in list rows; elsewhere a toggle-behaving button. macOS: switches, checkboxes, radios in window body, not toolbar; do not replace a checkbox with a switch | `toggles` |
| Pickers | Medium-to-long lists; predictable order; avoid switching views to show a picker; minute interval must divide 60 | iOS compact date picker when space is tight | `pickers` |
| Sliders | Minimum on leading side or bottom; consider paired text field and stepper | iOS: "Don't use a slider to adjust audio volume". visionOS: prefer horizontal | `sliders` |
| Steppers | Make the affected value obvious; pair with a text field for large ranges | macOS Shift-click for 10x | `steppers` |
| Segmented controls | No more than about five to seven segments on wide layouts, about five on iPhone; text or images, not mixed; do not mix actions and selection; equal segment size | macOS: tab view, not segmented control, for view switching in the main window | `segmented-controls` |
| Text fields | Small amounts of text; show a hint; "Always use a secure text field" for sensitive data; correct keyboard type; validate when sensible | iOS Clear button at trailing end. tvOS and watchOS minimize text entry | `text-fields` |
| Lists and tables | Prefer text in lists; succinct rows; selection feedback | iOS: edit mode before selection; info button only for more info; no index with trailing controls. macOS: sortable, resizable columns; outline view for hierarchy | `lists-and-tables` |
| Collections | Standard row or grid layouts; tables for text; avoid layout changes mid-interaction | | `collections` |
| Progress indicators | Prefer determinate; be accurate; keep moving; never switch circular to bar; avoid vague labels such as "loading"; let people halt | iOS refresh control: update automatically too; do not explain how to refresh. macOS: do not label spinners | `progress-indicators` |
| Page controls | Ordered peer pages only; centered at the bottom; more than about 10 dots is too many; at most two indicator images; do not color indicator images | visionOS: not interactive | `page-controls` |
| Labels | Uneditable short text; system fonts; system label colors for importance; make useful text selectable | | `labels` |
| Disclosure controls | Most-used controls visible at the top; no more than one disclosure button per view | | `disclosure-controls` |
| Scroll views | No nested same-axis scroll views; make scrollability apparent; scroll edge effect only behind floating elements, automatic style, one per view; no page control plus scroll indicator on the same axis | visionOS Look to Scroll for reading views. watchOS vertical scrolling | `scroll-views` |
| Tab views | Closely related content; no more than six tabs; not a pop-up button as a tab switcher | macOS mostly | `tab-views` |

---

## 5. Inputs and gestures

- `/gestures` (Oct 28, 2026): more than one way to do anything; do not repurpose standard gestures or invent gestures for
  standard actions; custom gestures only when necessary and never replacing standard ones; avoid conflicts with system-UI
  edge gestures. Standard set: tap, swipe, drag, touch (or pinch) and hold, double tap, zoom, rotate. iOS/iPadOS system
  gestures: three-finger swipe undo/redo, three-finger pinch copy/paste, four-finger swipe app switching (iPadOS), shake to
  undo. macOS touch display: keep layout and control size, "Make tap targets bigger, not the controls themselves"; never
  touch-only access. visionOS: support indirect and direct; do not require specific body positions or a specific hand; keep
  the area around the hand for system overlays. watchOS double tap: one primary action per view, none in lists or scroll views.
- `/keyboards` (June 9, 2025): support Full Keyboard Access; do not repurpose standard shortcuts (full table on the page);
  custom shortcuts only for the most frequent commands; Command is the main modifier, Shift secondary, Option sparingly,
  avoid Control; list modifiers in the order Control, Option, Shift, Command. iPadOS: do not add keyboard navigation for
  buttons, segmented controls, and switches; leave that to Full Keyboard Access.
- `/pointing-devices` (Oct 28, 2026): do not redefine systemwide trackpad gestures; iPadOS hit-region padding about 12 pt
  (bezeled) and about 24 pt (no bezel); contiguous hit regions for bar buttons; prefer system pointer effects; no
  instructional text attached to the pointer. macOS pointer catalog and touch reveal rules for hidden controls.
- `/apple-pencil-and-scribble`: marks the instant Pencil touches, no mode switch; controls respond to Pencil too; left- and right-handed layouts; hover previews, never hover-initiated actions.
- `/digital-crown`: watchOS 10 and later, the Crown is the primary navigation input; always give visual feedback; match update rate to rotation speed.
- `/remotes` (tvOS): focus moves in the gesture direction; distinguish press from tap; Back opens the parent (games: pause menu); honor Play/Pause.
- `/focus-and-selection`: rely on system focus effects; do not move focus without interaction; focus ring for text and search fields, highlight for lists and collections; tvOS supply assets for the larger focused size.
- `/eyes` (visionOS): place content at least one meter away for sustained viewing; at least 16 pt margin around interactive
  items or centers at least 60 pt apart; rounded shapes for interactive items; standard components preferred; avoid field-filling repeating patterns.
- `/playing-haptics`: system patterns only for their documented meanings; complement, do not replace, other feedback; avoid overuse; make haptics optional.
- `/virtual-keyboards`: match keyboard type to content; use the keyboard layout guide; custom keyboards must offer an obvious way to switch keyboards.

---

## 6. Common mistakes the HIG explicitly warns against

| # | Mistake | Source |
|---|---|---|
| 1 | Putting actions in a tab bar, or hiding/disabling tabs | `/tab-bars` |
| 2 | Deciding layout from device idiom or orientation instead of size classes; fixed widths | `/layout`, `/designing-for-iphone-duo` |
| 3 | Changing functionality (not just visible amount) when size class changes | `/layout` |
| 4 | Solid or semi-opaque backgrounds under bars; custom bar backgrounds and tinted bar items; manual overflow menu | `/layout`, `/toolbars` |
| 5 | Liquid Glass in the content layer, or on many custom controls; color on multiple glass controls | `/materials`, `/color` |
| 6 | Hard-coded colors or system color values; misusing semantic colors; one appearance only | `/color`, `/dark-mode` |
| 7 | App-specific light/dark setting | `/dark-mode` |
| 8 | Color as the only signal for state, interactivity, or focus | `/color`, `/accessibility`, `/toggles` |
| 9 | Light font weights; many typefaces; fixed font sizes that ignore Dynamic Type; truncation at large sizes | `/typography` |
| 10 | Alerts for information only, at launch, or for common undoable actions; "OK"/"Yes"/"No" on action alerts; "Error" as a title; Cancel as default | `/alerts` |
| 11 | Destructive action given the primary role or default styling | `/buttons`, `/alerts` |
| 12 | Stacked sheets, cascaded popovers, modal "app within an app", no obvious dismiss | `/sheets`, `/popovers`, `/modality` |
| 13 | Done button with no Cancel or Back; Cancel, Done, and Back all together | `/sheets` |
| 14 | Context-menu-only features; dimmed rather than hidden context items; all actions buried in one pull-down button | `/context-menus`, `/pull-down-buttons` |
| 15 | Gesture-only features; custom gestures replacing standard ones; overriding system gestures or shortcuts | `/gestures`, `/accessibility`, `/keyboards` |
| 16 | Auto-dismissing timed UI; autoplay without controls; ignoring Reduce Motion | `/accessibility` |
| 17 | Motion as the sole carrier of information; blocking input during animation | `/motion` |
| 18 | Permission request at launch without need; custom screen that preempts or mimics the tracking alert; pre-alert screen with a cancel path | `/privacy` |
| 19 | Launch screen used for branding, with text or logos; splash-style advertising | `/launching`, `/branding` |
| 20 | Forcing sign-in before showing value; no account deletion | `/managing-accounts` |
| 21 | Prepopulated password fields; plain-text secrets; custom authentication schemes | `/entering-data`, `/privacy` |
| 22 | Switch outside a list row on iOS; slider for volume on iOS; segmented control mixing actions and selection | `/toggles`, `/sliders`, `/segmented-controls` |
| 23 | Nested same-axis scroll views; progress indicator that stalls or says only "Loading" | `/scroll-views`, `/progress-indicators` |
| 24 | Text labels "Back"/"Close" in toolbars; window titled with the app name | `/toolbars` |
| 25 | Flipping logos, numerals, or checkmarks in RTL; not flipping back and progress controls | `/right-to-left` |
| 26 | Controls or critical info at the bottom of a Mac window or sidebar | `/layout`, `/sidebars` |
| 27 | Replicas of Apple hardware in icons; Apple trademarks in name or images | `/icons`, `/app-icons`, `/branding` |

---

## 7. Thirty highest-value checkable rules for an agentic UI review

Each is detectable from code or a screenshot. Severity: E = likely defect, W = warning. All sourced above.

| # | Check | Sev | Source |
|---|---|---|---|
| 1 | Interactive elements have a hit region of at least 44x44 pt (60x60 pt visionOS, 66x66 tvOS default); never below the platform minimum (28x28 iOS, watchOS, visionOS; 20x20 macOS; 56x56 tvOS) | E below minimum, W below default | `/accessibility`, `/buttons` |
| 2 | Text contrast at least 4.5:1 (3:1 for 18 pt and larger or bold), in light and dark | E | `/accessibility`, `/dark-mode` |
| 3 | No text below the platform minimum size (11 pt iOS/iPadOS, 10 macOS, 23 tvOS, 12 visionOS, 12 watchOS) | E | `/typography` |
| 4 | Text uses text styles or scaled metrics, not fixed point sizes; custom fonts scale with Dynamic Type | E | `/typography` |
| 5 | Layout survives the largest accessibility text size without clipping or overlap (rows grow, HStacks restack) | E | `/layout`, `/typography` |
| 6 | No Ultralight, Thin, or Light weights for body-size text | W | `/typography` |
| 7 | Colors are semantic or asset-catalog colors with light, dark, and high-contrast variants; no hex literals for UI chrome | W | `/color`, `/dark-mode` |
| 8 | No in-app appearance (light/dark) switch | W | `/dark-mode` |
| 9 | State, validity, and interactivity are never conveyed by color alone | E | `/accessibility`, `/color` |
| 10 | Layout branches on size class or available space, not device idiom or orientation; no hard-coded screen widths | W | `/layout` |
| 11 | Content respects safe areas; backgrounds extend under bars while controls and text do not sit under hardware features | E | `/layout` |
| 12 | Tab bar contains only navigation destinations; no tab is hidden or disabled; no More overflow in the default configuration | E | `/tab-bars` |
| 13 | Each tab has an icon and a short label | W | `/tab-bars` |
| 14 | Bars have no custom opaque background or tint that defeats system glass and scroll edge effects | W | `/toolbars`, `/layout` |
| 15 | Glass effects are only on controls and navigation, not content-layer cards or backgrounds; at most one tinted glass control per view | W | `/materials`, `/color` |
| 16 | Toolbar: at most about three groups; title under 15 characters and not the app name; standard Back/Close symbols with no "Back" text | W | `/toolbars` |
| 17 | One prominent button per view; destructive actions never use the primary or prominent role | E | `/buttons` |
| 18 | Alerts: at most three buttons; specific title; verb button titles; cancel is titled "Cancel" and is not the default; destructive alerts include Cancel | E | `/alerts` |
| 19 | No alert at launch, and no alert that is purely informational or for an undoable action | W | `/alerts` |
| 20 | Choices following a user-initiated action use a confirmation dialog or action sheet with the destructive item first and styled destructive | W | `/action-sheets` |
| 21 | Every modal has a visible dismiss control; sheets with Done also have Cancel or Back; never all three | E | `/modality`, `/sheets` |
| 22 | No sheet presented from a sheet, and no popover from a popover | W | `/sheets`, `/popovers` |
| 23 | Resizable sheets show a grabber and support swipe to dismiss, with confirmation when there are unsaved changes | W | `/sheets` |
| 24 | Every gesture-driven action (swipe actions, long press, drag) has a visible control alternative; context menu items also exist in the main UI | E | `/accessibility`, `/context-menus` |
| 25 | All controls and meaningful images have accessibility labels; decorative images are hidden from VoiceOver | E | `/voiceover` |
| 26 | Animations honor Reduce Motion (fades instead of slides, zooms, or depth changes); no information conveyed only by motion | E | `/accessibility`, `/motion` |
| 27 | No timed auto-dismissing UI for essential information; no autoplay media without controls | W | `/accessibility` |
| 28 | iOS switches appear only in list rows; segmented controls have no more than about five segments on iPhone and do not mix text and images | W | `/toggles`, `/segmented-controls` |
| 29 | Permission prompts are requested in context (not at launch unless essential) with purpose strings that are active sentences ending in a period | E | `/privacy` |
| 30 | Sign-in is deferred until needed; password fields are secure and never prefilled; account deletion is reachable in-app | E | `/managing-accounts`, `/entering-data` |

---

## 8. Recommended reference files for the skill

| Reference file | Contents | Why separate |
|---|---|---|
| `principles-and-review-checklist.md` | Eight principles, section 0 lore corrections, the 30 checks, mistakes table | Loaded on every review task; must be short |
| `layout-and-adaptivity.md` | Size classes, safe areas, per-platform layout numbers, tvOS grids, iPhone Duo, scroll edge effects | Most frequent source of implementation bugs |
| `typography-dynamic-type.md` | Size tables per platform, text styles, Dynamic Type adaptation rules | Table-heavy; needed only when setting type |
| `color-materials-liquid-glass.md` | Semantic colors, Dark Mode, contrast, Liquid Glass rules and variants, standard materials | Fast-changing area; isolate for easy updates |
| `accessibility.md` | Control sizes, contrast, Reduce Motion, VoiceOver, Assistive Access, captions | Hard numbers; cross-cutting |
| `navigation.md` | Tab bars, sidebars, toolbars and titles, split views, search placement | Core IA decisions per platform |
| `modality-and-menus.md` | Sheets, alerts, action sheets, popovers, menus, context menus, pull-down and pop-up buttons | Decision tree "which presentation do I use" |
| `controls.md` | Section 4 table expanded | Lookup while building forms and screens |
| `patterns.md` | Onboarding, launching, loading, settings, entering data, feedback, undo, drag and drop, accounts, full screen, privacy prompts, writing | Flow-level guidance |
| `inputs.md` | Gestures, keyboards and shortcuts, pointer, Pencil, Crown, remotes, eyes, focus, haptics | Platform-dependent; load on demand |
| `icons-and-assets.md` | SF Symbols, standard action symbols, app icon specs, image scale factors, RTL flipping | Asset work only |
| `hig-index.md` | Section 9 slug list | Lets the agent link or fetch any page |

Per-platform files (iOS, iPadOS, macOS, tvOS, visionOS, watchOS, iPhone Duo) belong to the platform-architecture workstream; the platform rows above should be cross-linked from them.

---

## 9. Complete HIG slug list (171 pages, fetched 2026-11-23)

URL pattern: `https://developer.apple.com/design/human-interface-guidelines/<slug>`. Section landing pages are marked (L).

**Getting started** — `getting-started` (L): `design-principles`, `designing-for-ios`, `designing-for-ipados`, `designing-for-macos`,
`designing-for-tvos`, `designing-for-visionos`, `designing-for-watchos`, `designing-for-games`, `designing-for-iphone-duo`

**Foundations** — `foundations` (L): `accessibility`, `app-icons`, `branding`, `color`, `dark-mode`, `icons`, `images`,
`immersive-experiences`, `inclusion`, `layout`, `materials`, `motion`, `privacy`, `right-to-left`, `sf-symbols`, `spatial-layout`,
`typography`, `writing`

**Patterns** — `patterns` (L): `charting-data`, `collaboration-and-sharing`, `drag-and-drop`, `entering-data`, `feedback`,
`file-management`, `going-full-screen`, `launching`, `live-viewing-apps`, `loading`, `managing-accounts`, `managing-notifications`,
`modality`, `multitasking`, `offering-help`, `onboarding`, `playing-audio`, `playing-haptics`, `playing-video`, `printing`,
`ratings-and-reviews`, `searching`, `settings`, `undo-and-redo`, `workouts`

**Components** — `components` (L)
- Content — `content` (L): `charts`, `image-views`, `text-views`, `web-views`
- Layout and organization — `layout-and-organization` (L): `boxes`, `collections`, `column-views`, `disclosure-controls`, `labels`,
  `lists-and-tables`, `lockups`, `outline-views`, `split-views`, `tab-views`
- Menus and actions — `menus-and-actions` (L): `activity-views`, `buttons`, `context-menus`, `dock-menus`, `edit-menus`,
  `home-screen-quick-actions`, `menus`, `ornaments`, `pop-up-buttons`, `pull-down-buttons`, `the-menu-bar`, `toolbars`
- Navigation and search — `navigation-and-search` (L): `path-controls`, `search-fields`, `sidebars`, `tab-bars`, `token-fields`
- Presentation — `presentation` (L): `action-sheets`, `alerts`, `page-controls`, `panels`, `popovers`, `scroll-views`, `sheets`, `windows`
- Selection and input — `selection-and-input` (L): `color-wells`, `combo-boxes`, `digit-entry-views`, `image-wells`, `pickers`,
  `segmented-controls`, `sliders`, `steppers`, `text-fields`, `toggles`, `virtual-keyboards`
- Status — `status` (L): `activity-rings`, `gauges`, `progress-indicators`, `rating-indicators`
- System experiences — `system-experiences` (L): `app-shortcuts`, `complications`, `controls`, `live-activities`, `notifications`,
  `snippets`, `status-bars`, `top-shelf`, `watch-faces`, `widgets`

**Inputs** — `inputs` (L): `action-button`, `apple-pencil-and-scribble`, `camera-control`, `digital-crown`, `eyes`,
`focus-and-selection`, `game-controls`, `gestures`, `gyro-and-accelerometer`, `keyboards`, `nearby-interactions`,
`pointing-devices`, `remotes`

**Technologies** — `technologies` (L): `airplay`, `always-on`, `app-clips`, `apple-in-app-purchase`, `apple-pay`,
`augmented-reality`, `carekit`, `carplay`, `game-center`, `generative-ai`, `healthkit`, `homekit`, `icloud`, `id-verifier`,
`imessage-apps-and-stickers`, `live-photos`, `mac-catalyst`, `machine-learning`, `maps`, `nfc`, `photo-editing`, `researchkit`,
`shareplay`, `shazamkit`, `sign-in-with-apple`, `siri`, `tap-to-pay-on-iphone`, `voiceover`, `wallet`

Absent from the TOC: `navigation-bars` (guidance is in `toolbars`). The root index JSON is
`.../tutorials/data/design/human-interface-guidelines.json` (not under the per-page path).

---

## 10. Not verified / caveats

- Pages read only as rule headlines plus numeric sentences (not full prose): most components in section 4, patterns in 3.8, inputs
  in section 5. Headline wording and all quoted numbers are [V]; nuance in the surrounding paragraphs may be missing.
- Not read in this workstream: Technologies pages (except titles), `windows`, `panels`, `boxes`, `charts`, `widgets`,
  `live-activities`, `notifications`, `multitasking`, `spatial-layout`, `immersive-experiences`, `designing-for-*` bodies other than iPhone Duo.
- System color numeric values are images in the HIG JSON, not text; no RGB values were extracted. The HIG says not to hard-code them anyway.
- Tab bar icon dimensions and iOS margin values are not in the HIG text; the HIG defers to Apple Design Resources. Any number
  for these (for example 16 pt or 20 pt margins) is [M] and should not be stated as HIG guidance.
- The 28x28 pt "minimum control size" for iOS sits beside the Buttons page's "at least 44x44 pt" hit region. They are compatible
  if read as visual control size versus hit region, but the HIG does not state that explicitly; the skill should recommend 44 pt and treat 28 pt as an absolute floor.
- SwiftUI/UIKit symbol names mentioned (`backgroundExtensionEffect()`, `TabBarMinimizeBehavior`, `sidebarAdaptable`,
  `ReservedRegion`, `ArrangementView`, `ToolbarItemVisibilityPriority`, `ScrollEdgeEffectStyle`) are names as referenced by HIG
  pages; availability versions were not checked here (SwiftUI API workstream).
