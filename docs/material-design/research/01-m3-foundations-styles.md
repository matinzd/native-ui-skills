# M1 research: Material Design 3 foundations and styles

> Research agent M1, fetched 2026-11-23 from m3.material.io with the Chromium render helper.
> Tags: **[V]** = fetched this session and the page says this; **[M]** = from memory, not verified.
> `B` = `https://m3.material.io`. All guidance below is a Material *recommendation* unless marked otherwise;
> wording strength is quoted (must / should / don't / avoid / consider).
> Rendered page text (one file per slug) is kept in the scratch folder, see section 9.

## 0. What Material 3 is today

| Fact | Source | Tag |
|---|---|---|
| Material 3 is "the latest version"; it "enables personal, adaptive, and expressive experiences – from dynamic color and enhanced accessibility, to foundations for large screen layouts and design tokens". | B/get-started | [V] |
| **M3 Expressive** (announced 13 May 2025) is "an expansion of the Material 3 design system ... a set of new features, updated components, and design tactics". The launch post states: "M3 Expressive isn't a new version of the system. We're not deprecating M3, and this isn't 'M4.'" | B/get-started, B/blog/building-with-m3-expressive | [V] |
| Expressive contents: 15 new or updated components (launch post said 14), emphasized typography (15 extra type styles), motion physics (springs), 35-shape library with shape morph, vibrant colour schemes. | same | [V] |
| Launch component list: app bars, button groups (new), common buttons, extended FAB, FAB menu (new), FABs, icon buttons, loading indicator (new), navigation bar, navigation rail, progress indicators, sliders, split button (new), toolbars (new). | B/blog/building-with-m3-expressive | [V] |
| I/O 2026 (19 May 2026): "Expressive layout system" (layout scaffold of bars, rails, panes; spacing system on an 8dp scale; watch and XR guidance), expressive lists and menus, expressive search and search app bar. Naming change: window size classes -> **breakpoints**; responsive layout -> **adaptive design**. | B/blog/whats-new-at-io26, B/foundations/layout/layout-overview/overview | [V] |
| Compose Material 3 **1.5.0** stable (18 Nov 2026, with Jetpack Compose 1.13): "Material 3 core and Expressive APIs graduated to stable"; "promotes most M3 experimental APIs to stable". Expressive colour schemes, shapes and motion are stable. | B/blog/compose-material-3-is-stable | [V] |
| Compose Material 2 (`androidx.compose.material`) "is deprecated and no longer actively maintained". | same | [V] |
| Material Views (MDC-Android) **1.14.0** is the "final stable release"; the library is in "maintenance mode" (no new features, critical bug fixes only). 1.14.0 brought Expressive themes, expressive list, emphasized type scale and expressive styles for 11 components to Views. "Material Android is Compose-first." | B/blog/material-is-compose-first | [V] |
| Dynamic colour ("Material You" in the 2021 blog titles; the current guideline pages say "dynamic color") is "both a user setting and a developer choice"; apps need a custom/fallback scheme for users without it. | B/foundations/customization | [V] |
| Site structure: three parts, foundations, styles, components. Foundations nav: Accessibility (Overview, Designing, Writing and text), Building for all, Content design, Customizing Material, Desktop, Watches, XR, Design tokens, Interaction, Layout, Usability, Material A-Z. Styles nav: Color, Elevation, Icons, Motion, Shape, Spacing, Typography. | B/foundations, B/styles | [V] |

Deprecated or superseded relative to Material 2 / early M3 (all [V], details in section 5):
surface tint colour and elevation overlays, shadows at every level, the 3-step shape scale, easing-and-duration
for component motion ("no longer maintained", still used for transitions), Material Icons as default (now Material
Symbols), title-case/caps labels, Compose M2 library, new feature work in Views.

## 1. Slug map (rendered 2026-11-23)

Top-level slugs redirect to their first tab. Tab slugs are listed after the base path.

### Foundations (`B/foundations/...`)

| Nav item | Base path | Tabs (slugs) |
|---|---|---|
| Accessibility: Overview | `overview/` | `principles`, `assistive-technology` |
| Accessibility: Designing | `designing/` | `overview`, `color-contrast`, `structure`, `flow`, `elements` |
| Accessibility: Writing and text | `writing/` | `best-practices`, `text-truncation`, `text-resizing` |
| Building for all | `building-for-all/` | `user-needs`, `co-design` |
| Content design | `content-design/` | `overview`, `alt-text`, `notifications`, `global-writing/overview`, `global-writing/word-choice`, `style-guide/ux-writing-best-practices`, `style-guide/word-choice`, `style-guide/grammar-and-punctuation` |
| Customizing Material | `customization` | (single page) |
| Desktop | `desktop/` | `overview`, `layout`, `interaction`, `components` |
| Watches | `watches/` | `overview`, `foundations`, `layout`, `styles` |
| XR: design | `xr/design/` | `overview`, `interaction`, `layout`, `accessibility` |
| XR: components | `xr/components/` | `overview`, `app-bars`, `dialogs`, `nav-bar`, `nav-rail`, `toolbars` |
| Design tokens | `design-tokens/` | `overview`, `how-to-use-tokens` |
| Interaction | `interaction/` | `gestures`, `inputs`, `selection`, `states/overview`, `states/state-layers`, `states/applying-states` |
| Layout: overview | `layout/layout-overview/` | `overview`, `parts-of-layout`, `adaptive-design` (old `layout/understanding-layout/overview` redirects here) |
| Layout: scaffold | `layout/scaffold/` | `overview`, `bars`, `rails`, `panes` |
| Layout: grids and spacing | `layout/grids-spacing/` | `overview`, `grids`, `spacing`, `density` |
| Layout: breakpoints | `layout/breakpoints/` | `overview`, `compact`, `medium`, `expanded`, `large-extra-large` |
| Layout: bidirectionality | `layout/bidirectionality-rtl` | (single page) |
| Layout: canonical examples | `layout/canonical-examples/` | `overview`, `feed`, `list-detail`, `supporting-pane` |
| Usability | `usability/` | `overview`, `applying-m-3-expressive` |
| Material A-Z | `glossary` | (single page) |

### Styles (`B/styles/...`)

| Nav item | Base path | Tabs (slugs) |
|---|---|---|
| Color system | `color/system/` | `overview`, `how-the-system-works` |
| Color roles | `color/roles` | (single page) |
| Choosing a scheme | `color/choosing-a-scheme` | (single page) |
| Static schemes | `color/static/` | `baseline`, `custom-brand` |
| Dynamic schemes | `color/dynamic/` | `choosing-a-source`, `user-generated-source`, `content-based-source` |
| Advanced customizations | `color/advanced/` | `overview`, `apply-colors`, `define-new-colors`, `adjust-existing-colors` |
| Color resources | `color/resources` | (single page) |
| Elevation | `elevation/` | `overview`, `applying-elevation`, `tokens` |
| Icons | `icons/` | `overview`, `designing-icons`, `applying-icons` |
| Motion physics | `motion/overview/` | `how-it-works`, `specs` |
| Easing and duration (legacy) | `motion/easing-and-duration/` | `applying-easing-and-duration`, `tokens-specs` |
| Transitions | `motion/transitions/` | `transition-patterns`, `applying-transitions` |
| Shape | `shape/` | `overview-principles`, `corner-radius-scale`, `shape-morph` |
| Spacing (new, May 2026) | `spacing/` | `overview`, `applying-spacing`, `tokens` |
| Typography | `typography/` | `overview`, `fonts`, `type-scale-tokens`, `applying-type`, `editorial-treatments` |

Other: `B/get-started`, `B/blog` (key posts: `whats-new-at-io26`, `compose-material-3-is-stable`,
`material-is-compose-first`, `building-with-m3-expressive`, `m3-expressive-motion-theming`).

## 2. Foundations

### 2.1 Layout: breakpoints (formerly window size classes)

Source: B/foundations/layout/breakpoints/overview and the per-breakpoint tabs. All [V].

| Breakpoint | Width (dp) | Common devices | Panes (recommended) | Navigation | Margin | Pane spacer |
|---|---|---|---|---|---|---|
| Compact | under 600 | phone portrait | 1 | navigation bar, or modal expanded navigation rail | 16dp | n/a |
| Medium | 600-839 | tablet portrait, unfolded foldable portrait | 1 (recommended) or 2 | single pane: navigation rail; two panes: navigation bar | 24dp | 24dp |
| Expanded | 840-1199 | phone landscape, tablet landscape, unfolded foldable landscape, desktop | 1 or 2 (recommended) | navigation rail, collapsed or expanded | 24dp | 24dp |
| Large | 1200-1599 | desktop | 1 or 2 (recommended) | navigation rail, collapsed or expanded | 24dp | 24dp |
| Extra-large | 1600+ | desktop, ultra-wide | 1 to 3 (2 recommended on the panes page) | expanded rail suits XL | 24dp | 24dp |

- "A breakpoint (previously window size class) is the window size at which a layout needs to change"; "These apply
  to Android and web." Large and extra-large "are most useful for creating web experiences tailored to laptop and
  desktop devices. Some products may not need" them.
- Height breakpoints: "On Android, compact, medium, and expanded breakpoints are also available for height"; rarely
  needed because most layouts scroll vertically. (No dp values for height on this page; the Android docs hold them.)
- "Products should automatically adapt to any breakpoint." Design for breakpoints, not devices, because window size
  changes with multi-window, folding and rotation.
- Five adaptation questions: what to reveal, divide, resize, reposition, swap.
- "Across all breakpoints, adjust margins and type styles to keep text between 40–60 characters per line."
- "Don't use two panes in medium layouts with high information density."
- Swapping: navigation bar (compact) -> collapsed navigation rail (medium, expanded); modal expanded rail ->
  standard expanded rail (expanded); basic or full-screen dialog (compact) -> basic dialog; bottom sheet
  (compact) -> menu (medium and up). "Don't arbitrarily swap components that aren't functionally equivalent";
  "Don't swap a button for a chip."
- Fixed pane width in fixed-and-flexible layouts: "should have a width of 360dp by default" at expanded; "412dp by
  default" at large and extra-large. Side sheets "have a default maximum width of 400dp".
- Medium two-pane: "Each pane ... should take up 50% of the window width. Avoid setting custom widths."
- Reachability (medium): "limit the amount of interactions that are placed in the upper 25% of the screen"; "Avoid
  placing essential interactive elements too close to the bottom edge".
- Each breakpoint page lists the events that force a dynamic transition (fold/unfold, rotation, split-screen,
  multi-window, free-form resize).

### 2.2 Layout: scaffold, panes, grids, spacing, density

Sources: B/foundations/layout/scaffold/{bars,rails,panes}, .../layout-overview/{parts-of-layout,adaptive-design},
.../grids-spacing/{grids,spacing,density}, B/styles/spacing/{overview,applying-spacing,tokens}. All [V].

- Layout scaffold (new May 2026) = **bars** (app bar, navigation bar; adjacent to the safety regions),
  **rails** (perimeter around panes: navigation rail, toolbars, chat inputs, FABs; become orbiters in XR),
  **panes** (all content). "The safety region shouldn't contain primary content."
- "All content must be in a pane." "All layouts are made up of 1–3 panes." "Don't use more than three panes."
  "All layouts need at least one flexible pane." Panes are fixed or flexible, permanent or temporary.
- Two-pane types: **split-pane** (two flexible panes, spacer visually centred; with a rail, navigation plus first
  pane = 50% of window width) and **fixed-and-flexible**.
- Drag handles resize panes; "The drag handle should also toggle between layout sizes when selected." Recommended
  snap widths: 360dp, 412dp, or centred split. Persistent resizing for most layouts; temporary resizing for
  supporting-pane layouts.
- Multiple panes display as co-planar, floating or docked. Adaptive strategies: show and hide, levitate, reflow.
  "On large screens, consider changing docked panes into co-planar panes."
- Pane accessibility: "The focus order should match the visual arrangement of the panes"; modal floating pane moves
  focus to its first element and returns it to the trigger on close.
- Adaptive design: "Layouts must be versatile, designed to adapt fluidly across three primary experience types:
  mobile, desktop, and spatial"; "designs should be built with all inputs in mind—touch, pointer, and physical
  keyboard". Components adapt by resizing, showing and hiding, presentation changes (FAB <-> extended FAB).
- Rulers: global alignment lines (bar and safety rulers, title ruler, content rulers, margin rulers). Compose
  implementation is listed as "Available".
- Grouping: explicit (outlines, dividers, shadows) vs implicit (proximity and open space).
- **Spacing system** (Compose only: "The spacing system tokens are only used on Jetpack Compose"; Views
  "Unavailable"). Base unit `md.sys.measurement.space100` = 8dp. Tokens:

  | Token | dp | Token | dp | Token | dp |
  |---|---|---|---|---|---|
  | space0 | 0 | space150 | 12 | space450 | 36 |
  | space25 | 2 | space175 | 14 | space500 | 40 |
  | space50 | 4 | space200 | 16 | space600 | 48 |
  | space75 | 6 | space250 | 20 | space700 | 56 |
  | space100 | 8 | space300 | 24 | space800 | 64 |
  | space125 | 10 | space400 | 32 | space900 | 72 |

  Categories: padding (inside), gap (between), margin (outside). "Use padding & gaps before using margins";
  "Avoid defining margins on child elements". "When text is scaled up to 200%, the same spacing should be
  preserved by default." "Work is ongoing to hook up all Material components to spacing tokens."
- **Density**: "The default target size should be at least 48x48 CSS pixels"; "Don't apply component scaling by
  default if it would result in a target below 48x48"; "People should be able to opt in to dense layouts";
  "Density shouldn't automatically change across breakpoints or orientation unless a person changes it"; density
  scale 0, -1, -2, -3, each step typically -4dp of height; "Text size shouldn't change as the container size
  scales"; "Don't increase density in UIs that involve focused tasks, such as selecting from a menu" nor in
  "components that alert a person of changes, such as snackbars or dialogs". 1dp = 1px at 160 dpi.

### 2.3 Canonical layouts

Source: B/foundations/layout/canonical-examples/{overview,list-detail,supporting-pane,feed}. All [V].

| Layout | Use | Compact | Medium | Expanded and up |
|---|---|---|---|---|
| List-detail | parent-child content (inbox + message, settings + detail) | 1 pane, list or detail | 1 pane (recommended) or 2 | 2 panes |
| Supporting pane | secondary content only meaningful next to primary (about two-thirds / one-third) | supporting pane below, flexible; bottom sheet is an option | below, flexible | leading or trailing side, fixed 360dp |
| Feed | browsing cards/lists in a grid | single column, items fill pane width | multiple columns | more columns; "number of columns should usually increase" |

- List-detail: "Use a back button in single-pane layouts only"; "Use a selection state in two-pane layouts only".
  With no selection, two-pane shows placeholder content in the detail pane. Going from two panes to one with an
  item selected: "The detail pane should typically show". "Detail views should retain their scroll position when
  navigating to other items." At medium, two-pane layouts should use a bottom navigation bar or modal rail.
- "For content with a parent-child relationship, use a list-detail layout instead" of supporting pane.
- Feed items "should reflow when the amount of available space changes".
- Compose and Views canonical layout implementations are both listed "Available".

### 2.4 Interaction: states, gestures, selection, inputs

Sources: B/foundations/interaction/{states/overview,states/state-layers,states/applying-states,gestures,selection,inputs}. All [V].

| State layer | Opacity | Notes |
|---|---|---|
| Hover | 0.08 | one hover state at a time; low-emphasis animated fade |
| Focus | 0.10 | plus "a ring-like keyboard focus indicator"; one focus at a time |
| Pressed | 0.10 | ripple overlay; one pressed at a time; "should be high-emphasis" |
| Dragged | 0.16 | may also raise elevation; "should be low emphasis" |
| Disabled state layer opacity token | 0.38 | per-component disabled container/content opacities live in component specs |

- Six states: enabled, disabled, hover, focused, pressed, dragged. "States have two visual indicators to ensure
  accessibility."
- State layer colour = the content ("on") colour; "only one state layer can be applied at a given time".
- "The size of state layers is 40dp while the interactive target size is 48dp."
- "Disabled states don't need to meet Material's contrast requirements." Disabled components cannot be focused,
  dragged or pressed. "If the action represented in the FAB is unavailable, the FAB shouldn't appear."
- Gestures: tap, double tap, long press, scroll and pan, swipe, drag, pick up and move, pinch, compound.
  **Predictive back** (Android) compatible components: bottom sheet, navigation bar, navigation rail, search bar,
  side sheet. "UI elements should respond to gestures in real time."
- Selection: touch = long press (or shortcut such as tapping an avatar) to enter selection mode, then tap to add;
  long press and drag for batch selection, "Don't use this gesture combination if it is already in use to pick up
  and move items". Desktop: checkboxes always visible when selection is the primary activity, otherwise on hover.
  Navigation bar/drawer/rail and tabs use an active indicator and "only one item should be selected at a time".
- Inputs: show a cursor whenever a mouse is connected "regardless of the device type"; "A secondary click ...
  should activate a context menu"; hover should change component state and invoke tooltips; cursor shapes
  (pointer, hand for links, resize arrows, I-beam on text); mouse wheel scrolls lists vertically and horizontally;
  with a mouse, dragging in text selects (touch scrolls); "When a physical keyboard is attached, hide the virtual
  keyboard"; "focus on interactive items must follow a logical order"; Enter triggers the common action, Space
  plays/pauses media, "The Escape key should dismiss any visible modal elements like menus, dialogs, or bottom
  sheets".
- Desktop extras (B/foundations/desktop/interaction, /components): "All drag-and-drop actions should include a
  single-click alternative"; "Pointer dragging should be instantaneous"; "Don't use hover as the only way to
  access these actions"; "If using a bottom sheet on desktop, it must be detached from the bottom edge of the
  window"; prefer dialogs over modal bottom sheets and context menus over long-press sheets; single-pane desktop
  layouts: "cap and center the content width".

### 2.5 Accessibility

Sources: B/foundations/designing/{color-contrast,structure,flow,elements}, B/foundations/writing/{best-practices,text-truncation,text-resizing},
B/foundations/overview/{principles,assistive-technology}. All [V].

| Topic | Rule (wording) |
|---|---|
| Touch target | "consider making touch targets at least 48 x 48dp" (about 9mm; recommended 7-10mm). A 24dp icon keeps a 48dp target. Page notes "iOS recommends 44 x 44dp". |
| Pointer target | "Consider making pointer targets minimums 44 x 44dp." |
| Target spacing | "In most cases, targets separated by 8dp of space or more". |
| Dense desktop icon | "A 20dp size symbol can use a target size of 40dp" when mouse and keyboard are primary (B/styles/icons/applying-icons). |
| Text contrast | small text at least 4.5:1; large text (14pt bold / 18pt regular and up) and graphics at least 3:1 (W3C). |
| Non-text contrast | Clustered elements (button groups) "should meet a contrast ratio of 3:1" container vs background; standalone prominent elements such as a FAB "don't need to meet" it. Disabled states exempt. |
| Text scaling | "UIs should support a minimum text increase of 200%." Text and line height scale; padding and inter-element spacing stay 1x; "don't resize components without text". Fixes: grow containers, reflow (stack buttons), scroll (vertical preferred; one direction only), touch-and-hold tooltips for app bar, navigation bar, navigation rail, fixed tabs. |
| Truncation | "Content, understandability, and functionality must not be lost when users modify their type settings." "Don't cut off text without providing a way for users to view it." |
| Labels | Label icon-only buttons, meaningful icons/images, progress and error cues, generic links. Describe purpose, not appearance. "Don't include the element type (button, menu, etc.) in your label." Mark decorative images hidden. Assign roles to interactive elements. |
| Focus | Use default order unless needed; define initial focus; dialogs take focus and return it to the trigger on close; Tab between elements, arrows within components, Enter activates. |
| Keyboard shortcuts | "should use a combination of two or more keys by default"; single-key shortcuts need remap / focus-scoping / off switch. |
| Structure | Important actions at top or bottom of screen; headings by content hierarchy, never skip levels (web landmarks are web only). |
| Native controls | "Use native elements, such as the standard platform dialog"; non-standard elements need extra AT testing. |
| Assistive tech named | keyboard/D-pad, screen readers (TalkBack), Switch Access, braille displays, magnifiers, voice input. |
| Contrast levels | Colour roles support standard, medium and high user contrast (section 3.1). |
| Reduced motion | With the reduced animation setting on, transitions "should" use subtle fades instead of sliding/scaling and "Disable decorative effects like parallax or shape morphing" (B/styles/motion/transitions/applying-transitions). |

### 2.6 Content design and UX writing

Sources: B/foundations/content-design/style-guide/{ux-writing-best-practices,word-choice,grammar-and-punctuation},
.../global-writing/word-choice, .../alt-text, .../notifications. All [V]. The style guide "is specific to
English-language UX writing. Google generally follows Associated Press (AP) style."

- **Capitalization**: "use sentence-style capitalization ... All text, including titles, headings, labels, menu
  items, navigation components, app bars, and buttons". "Don't use title case capitalization." "Don't use caps
  block. Use sentence case for all product text."
- Tone: neutral, direct; "Tell users what will happen if they take an action and how they can undo it"; avoid
  alarming or condescending warnings.
- Pronouns: use "you"/"your"; "Don't combine first and second person"; caution with "I"/"we" (legal consent text
  excepted).
- Punctuation: no period on single sentences in labels, tooltips, bulleted lists, dialog body text; use
  contractions; serial comma; exclamation points sparingly; "Omit ellipses from menu items or buttons that open a
  dialog or start a process"; "&" allowed in headlines, column headers, navigation labels and buttons, not body
  text; avoid em dashes; en dash without spaces for ranges; bold rather than italics for emphasis.
- Abbreviations: spell out; avoid "e.g." and "etc.".
- Global writing: short simple sentences ("Other languages average at 1.5 times longer than English"); avoid
  idioms; avoid "Please", "Sorry", "Thank you" especially in error messages; repeat nouns instead of ambiguous
  pronouns.
- **Alt text**: describe meaning in context; "Don't start alt text with 'image of'"; do not repeat the caption;
  decorative images get none. Length: content-design page says "The recommended length for alt text is 140
  characters"; the accessibility writing page says "a short label (up to 125 characters)". **The two pages
  disagree**; cite both. Chart formula: "Summary of [data type] + [reason for showing the chart]".
- Notifications: do not repeat the app name; avoid dynamic text in titles; expanded body under 80 characters; "Use
  the days of the week. Don't use 'today,' 'tomorrow'"; emoji sparingly.
- Button-label specifics (verb-first, 1-2 words) are on the component pages, not in these sections [M].

### 2.7 Design tokens, customization, bidirectionality, building for all

- Tokens (B/foundations/design-tokens/overview) [V]: three classes, reference (`md.ref.*`, static values),
  system (`md.sys.*`, roles; theming happens here), component (`md.comp.*`, "in development"). "Use design tokens
  instead of hardcoded values." Contexts (dark theme, form factor, density, RTL) override values. Example names:
  `md.ref.palette.secondary90`, `md.comp.fab.primary.container.color`.
- Customization (B/foundations/customization) [V]: build a custom scheme with Material Theme Builder; a custom
  theme provides "a fallback color scheme available for users who don't enable dynamic color"; dynamic colour can
  be applied selectively.
- Bidirectionality (B/foundations/layout/bidirectionality-rtl) [V]:
  - Mirror layouts, navigation rail on the leading edge (right in RTL), badges, toolbars, app bars, chips, text
    field icons, swipe actions and predictive back.
  - Directional icons (back, forward, send) "should be mirrored". Do not mirror clocks, circular refresh and
    clockwise progress arrows; "Media controls for video or audio players are always LTR."
  - Linear progress runs right to left for most RTL languages, "except Hebrew where it should remain LTR";
    circular stays clockwise. Charts stay LTR for Persian and Urdu.
  - "Don't reverse the order of the email username and domain"; "Don't apply LTR directionality to RTL content".
  - Components use "leading"/"trailing" naming.
- Building for all (B/foundations/building-for-all/{user-needs,co-design}) [V]: this section is about inclusive
  research and co-design (dimensions such as age, culture, disability, literacy). It is **not** the large-screen
  or foldable guidance; that lives under Layout, Desktop, Watches and XR.
- Form-factor pages [V]: Desktop (above); Watches: "Design for small screens first, starting with a 192dp size
  watch", "Show more content on devices that are larger than 225dp", margins in percentages; XR: "icon buttons
  should have a 56dp target size and 4dp offset", rails become orbiters, panes need explicit containment.
- Foldables [V]: "Fold" and "Spacer" are layout terms; split-pane layouts are "best for foldable devices";
  unfolding must trigger a compact -> medium/expanded transition. Fold posture specifics (tabletop, book) are not
  on these pages; see Android docs [M].

### 2.8 Usability (Expressive tactics)

B/foundations/usability/overview and B/blog/building-with-m3-expressive [V]: emphasise the primary action with
size, colour, containment, placement; "The most important action ... should be the largest element"; one primary
task per page; "Don't overwhelm the user"; motion "sparingly"; "Stick to one or two hero moments in your product".

## 3. Styles

### 3.1 Color

Sources: B/styles/color/{system/overview,system/how-the-system-works,roles,choosing-a-scheme,static/baseline,dynamic/*}. All [V].

- "26 standard color roles organized into six groups: primary, secondary, tertiary, error, surface, and outline",
  plus add-ons. Same roles for light and dark.

| Group | Roles | Use |
|---|---|---|
| Primary | primary, on primary, primary container, on primary container | most prominent components: FAB, high-emphasis buttons, active states |
| Secondary | secondary, on secondary, secondary container, on secondary container | less prominent: filter chips, tonal buttons |
| Tertiary | tertiary, on tertiary, tertiary container, on tertiary container | contrasting accents; designer's discretion |
| Error | error, on error, error container, on error container | static by default even in dynamic schemes |
| Surface | surface, on surface, on surface variant; surface container lowest / low / (default) / high / highest; inverse surface, inverse on surface, inverse primary | backgrounds; containers for cards, sheets, dialogs; inverse for snackbars |
| Outline | outline (important boundaries such as text field border), outline variant (decorative: dividers) | |
| Add-ons | primary/secondary/tertiary fixed and fixed dim, on fixed, on fixed variant; surface dim, surface bright; scrim | "Most products won't need" them |

- "apply colors only in the intended pairs"; pairs give "an accessible minimum 3:1 contrast". Container roles
  "should not be used for text or icons".
- "Don't use the outline color for dividers ... Instead, use outline variant." "Don't use the outline variant
  color to create visual hierarchy or define the visual boundary of targets" (needs 3:1).
- Fixed colours "are likely to cause contrast issues. Avoid using them where contrast is necessary."
- Common mapping: surface for body, surface container for navigation area; keep role mappings identical across
  breakpoints ("should remain the same for layout regions across breakpoints").
- Pipeline: source colour -> five key colours (primary, secondary, tertiary, neutral, neutral variant) -> tonal
  palettes (tones 0-100; 0 black, 100 white) -> roles. Example: primary = primary40, on primary = primary100
  (light). HCT colour space; "Don't conflate color spaces".
- Schemes: **static** (baseline or custom brand) vs **dynamic** (user-generated from an Android wallpaper, or
  content-based from in-app imagery). Use static baseline when migrating from M2, for enterprise, or "Your product
  is built for iOS". Design with baseline first, then test across source colours.
- **Contrast levels** (May 2025): standard (default), medium ("minimum contrast ratio of 3:1"), high ("7:1
  contrast ratio" on essential elements). Applied automatically in light and dark; custom components get them by
  using roles. Static schemes do not get user-controlled contrast.
- Change log: Aug 2024 on-container roles more colourful in light theme; Feb 2023 tone-based surface containers
  "replaced the previous approach of surfaces at +1 to +5 elevation"; default light surface tone 99 -> 98.
- Scrim: "the scrim color role at an opacity of 32%" (B/styles/elevation/applying-elevation).
- Text colour default: on surface (alternative on surface variant); links use primary (or tertiary) and
  "Hyperlinked text must also be underlined" (B/styles/typography/applying-type).
- Baseline hex values sit in an interactive token module (surface tint/primary `#6750A4` seen) and were not
  expanded; take them from the Compose/MDC sources.

### 3.2 Typography

Sources: B/styles/typography/{overview,type-scale-tokens,fonts,applying-type,editorial-treatments}. Values read
from the expanded token module (scratch `tokens/typography_type-scale-tokens.txt`). All [V]. The module shows
units as "pt"; on Android the unit is sp (page: "Font size unit: sp", 1sp = 0.0625rem).

| Style | Size | Line height | Tracking | Weight (baseline) | Weight (emphasized) |
|---|---|---|---|---|---|
| Display large | 57 | 64 | -0.25 | 400 | 500 |
| Display medium | 45 | 52 | 0 | 400 | 500 |
| Display small | 36 | 44 | 0 | 400 | 500 |
| Headline large | 32 | 40 | 0 | 400 | 500 |
| Headline medium | 28 | 36 | 0 | 400 | 500 |
| Headline small | 24 | 32 | 0 | 400 | 500 |
| Title large | 22 | 28 | 0 | 400 | 500 |
| Title medium | 16 | 24 | 0.15 | 500 | 700 (variable `wght` 600) |
| Title small | 14 | 20 | 0.1 | 500 | 700 (variable `wght` 600) |
| Body large | 16 | 24 | 0.5 | 400 | 500 |
| Body medium | 14 | 20 | 0.25 | 400 | 500 |
| Body small | 12 | 16 | 0.4 | 400 | 500 |
| Label large | 14 | 20 | 0.1 | 500 | 700 (variable `wght` 600) |
| Label medium | 12 | 16 | 0.5 | 500 | 700 (variable `wght` 600) |
| Label small | 11 | 16 | 0.5 | 500 | 700 (variable `wght` 600) |

- "30 type styles: 15 baseline and 15 emphasized" (May 2025). Emphasized styles keep size, line height and
  tracking and raise weight. Tokens: `md.sys.typescale.display-large` / `md.sys.typescale.emphasized.display-large`.
- "Material components don't use emphasized type styles by default." Recommended for selection, primary-action
  buttons, badges, extended FAB, selected list and menu items, headlines, unread state.
- Fonts: Roboto is the default brand and plain typeface ("Static fonts like Roboto are currently applied by
  default"); Roboto Flex is variable but "not yet part of the M3 typescale"; Noto Sans is the fallback.
- Roles: display (short, large screens), headline, title, body ("Avoid expressive or decorative fonts for body
  text"), label ("Buttons ... use the label large style").
- Line height guidance: about 1.2x for title/headline/display, about 1.5x for body/label.
- Customizing: "Avoid changing the type size; this can affect how components render and reflow."
- Language script height (Aug 2026): small (Latin, Cyrillic, Greek, Hebrew), medium (about 7% taller: Arabic, CJK,
  Hindi, Thai, Vietnamese), large (about 30%: Burmese, Telugu), extra large (about 100%: Nastaliq); "recommended
  to default to medium"; "Components with fixed heights ... may not adapt by default."
- "Use tabular figures ... in tables or places where values may change often, such as clocks."
- Android uses baseline-relative measurement; web/iOS use bounding boxes.
- Editorial treatments: variable-axis showcase moments; "shouldn't be used in labels or just to give information".

### 3.3 Shape

Sources: B/styles/shape/{overview-principles,corner-radius-scale,shape-morph}. All [V].

| Token (corner value) | dp |
|---|---|
| None | 0 |
| Extra small | 4 |
| Small | 8 |
| Medium | 12 |
| Large | 16 |
| Large increased (new May 2025) | 20 |
| Extra large | 28 |
| Extra large increased (new) | 32 |
| Extra extra large (new) | 48 |
| Full | fully rounded ("Previously ... defined using 50% of the component size") |

- "ten styles"; M2 had a three-level scale. Asymmetric variants exist (extra small top, large top/start/end,
  extra large top) for inner corners in menus and split buttons.
- "Generally, products should consistently use the Material 3 shape styles"; customise per style or per component
  (buttons map to full by default; cards and small FABs to medium).
- Optical roundness for nested shapes: "Outer radius - padding = inner radius" (48 - 14 = 34dp). "Avoid using the
  same corner radius value for nested objects."
- "Be careful not to apply large or full corners to information-dense components, such as cards."
- Shape library: 35 shapes, for "mostly visual elements" (image crops, avatars). "Avoid applying unconventional
  shapes to text-heavy containers." "Avoid making shapes literal or assigning a specific function or meaning to a
  single shape."
- Shape morph: all library shapes morph into each other; used in the standard button group and loading
  indicator; uses the expressive motion scheme by default; Compose only ("Web is not currently available").

### 3.4 Elevation

Sources: B/styles/elevation/{overview,applying-elevation,tokens}. All [V].

| Level | dp | Resting components (examples) |
|---|---|---|
| 0 | 0 | app bar (not scrolled), filled/tonal/outlined buttons, filled/outlined cards, chips, full-screen dialog, icon buttons, list, navigation rail, docked side sheet, tabs, slider |
| 1 | 1 | banner, modal bottom sheet, elevated button/card/chips, modal navigation drawer, modal side sheet |
| 2 | 3 | app bar (scrolled), menu, navigation bar, rich tooltip, toolbar |
| 3 | 6 | date and time pickers, modal dialogs, FAB, extended FAB, FAB menu close button, search |
| 4 | 8 | not a resting level (interaction only) |
| 5 | 12 | not a resting level (interaction only) |

- "An element's resting state can be on levels 0 to +3, while levels +4 and +5 are reserved for user-interacted
  states such as hover and dragged." Hover usually raises one level (FAB 3 -> 4).
- "By default, Material 3's surfaces use tonal difference to indicate separation." Shadows only "when required to
  create additional protection against a background or to encourage interaction".
- "Surface tint color is deprecated. Use elevation level tokens (0–5) instead." Surface container roles "are not
  tied to elevation".
- "Avoid changing the default elevation of Material 3 components." "Stick to using a small amount of elevation
  levels."
- "Tokens have no shadows or color; each platform determines the specific shadows".

### 3.5 Motion

Sources: B/styles/motion/overview/{how-it-works,specs}, .../easing-and-duration/{applying-easing-and-duration,tokens-specs},
.../transitions/{transition-patterns,applying-transitions}. All [V] unless tagged.

- **Motion physics system** (May 2025) "is replacing the previous system based on easing and duration". Two preset
  schemes: **expressive** ("should be used for most situations"; overshoots) and **standard** ("for utilitarian
  products"; minimal bounce). Custom schemes are allowed.
- Six spring tokens per scheme: {fast, default, slow} x {spatial, effects}, for example
  `md.sys.motion.spring.fast.spatial`. Spatial = position, size, rotation, corner radius (may overshoot). Effects =
  colour and opacity ("there shouldn't be any overshoot"). Default speed for most; fast for small components
  (switches, buttons); slow for full-screen.
- Token values vary by device class (wearable, phone, tablet).

| Token | Standard scheme, Android: damping / stiffness [V] | Expressive scheme [M] | Web curve equivalent, expressive [V] |
|---|---|---|---|
| fast spatial | 0.9 / 1400 | 0.6 / 800 | cubic-bezier(0.42, 1.67, 0.21, 0.90), 350ms |
| default spatial | 0.9 / 700 | 0.8 / 380 | (0.38, 1.21, 0.22, 1.00), 500ms |
| slow spatial | 0.9 / 300 | 0.8 / 200 | (0.39, 1.29, 0.35, 0.98), 650ms |
| fast effects | 1 / 3800 | 1 / 3800 | (0.31, 0.94, 0.34, 1.00), 150ms |
| default effects | 1 / 1600 | 1 / 1600 | (0.34, 0.80, 0.34, 1.00), 200ms |
| slow effects | 1 / 800 | 1 / 800 | (0.34, 0.88, 0.34, 1.00), 300ms |

  Standard web curves: spatial (0.27, 1.06, 0.18, 1.00) at 350 / 500 / 750ms; effects same as expressive.
  The expressive damping/stiffness column was not readable in the module (context switch) and needs checking
  against Compose `MotionTokens`.
- Availability: Compose "Available" (21 components use it by default); Views "Available. Not added to
  components"; Flutter unavailable; Web "Compatible".
- **Legacy easing and duration**: "no longer maintained", "Products should migrate"; still used for transitions
  ("M3 transitions use the legacy easing and duration system").

| Easing | Android | Default duration | Use |
|---|---|---|---|
| Emphasized | path interpolator (two-segment) | 500ms | begin and end on screen |
| Emphasized decelerate | (0.05, 0.7, 0.1, 1) | 400ms | enter |
| Emphasized accelerate | (0.3, 0, 0.8, 0.15) | 200ms | exit permanently |
| Standard | (0.2, 0, 0, 1) | 300ms | small utility transitions |
| Standard decelerate | (0, 0, 0, 1) | 250ms | enter |
| Standard accelerate | (0.3, 0, 1, 1) | 200ms | exit |

  Duration tokens: short1-4 = 50/100/150/200ms; medium1-4 = 250/300/350/400; long1-4 = 450/500/550/600;
  extra-long1-4 = 700/800/900/1000.
- Transition patterns: container transform, forward and backward, lateral, top level (fade through), enter and
  exit, skeleton loaders.
  - "Both Android and iOS should use platform defaults for forward and backward navigation."
  - "Don't use a lateral transition to move between top level destinations."
  - "Don't use container transform in apps with deep hierarchies."
  - "Common transitions should not use overt style effects like bouncy springs."
  - "Fully fade out content before fading new content in." "Don't fade a bottom sheet as it enters and exits."
  - Android enter/exit expands along x or y; "Scale and z-axis motion is avoided".
  - Jump cuts "should generally be avoided".

### 3.6 Icons (Material Symbols)

Sources: B/styles/icons/{overview,designing-icons,applying-icons}. All [V].

- "Material Symbols are the new default"; three styles: outlined, rounded, sharp. Legacy Material Icons remain
  available without variable axes.
- Axes: **weight** 100-700 (regular 400 = 2dp stroke; "Don't use the lightest weight for standard-size (24dp)
  icons. The minimum weight for this size should be 200"; "Don't mix different weights"); **fill** 0-1 (state
  transitions, for example selected navigation items); **grade** (default 0 for dark-on-light, -25 for
  light-on-dark; positive for active emphasis); **optical size** 20-48dp.
- Sizes: 24dp standard; 20dp (desktop, dense), 40dp and 48dp (display/headline scale, larger screens, primary
  actions). Live area 20x20dp inside the 24dp frame with 2dp padding.
- "Symbols of 24dp should have a target size of 48dp by default."
- With text: same size and optical weight as the text; shift symbol baseline down about 11.5% of text size.
- "navigation items must have labels for clarity and accessibility"; complex or key-action symbols below 20dp
  need a text label; "Use caution if icons are displayed without labels."
- Localise icons (cart vs bag vs basket); mirror directional icons in RTL (section 2.7).

## 4. The 25 highest-value checkable rules

| # | Rule | Strength | Source |
|---|---|---|---|
| 1 | Interactive targets at least 48x48dp even when the visual is smaller (24dp icon in a 48dp target). | "consider" / "should" | B/foundations/designing/structure; B/styles/icons/applying-icons |
| 2 | Adjacent targets separated by 8dp or more. | "in most cases" | B/foundations/designing/structure |
| 3 | Text contrast 4.5:1 (small) and 3:1 (large: 18pt regular / 14pt bold and up). | W3C requirement adopted | B/foundations/designing/color-contrast |
| 4 | Clustered component containers and target boundaries reach 3:1 against the background. | "should" | same; B/styles/color/roles |
| 5 | UI survives 200% text scaling without clipped or lost content; padding stays constant. | "should support" / "must not be lost" | B/foundations/writing/text-resizing, /text-truncation |
| 6 | No truncation without a way to read the full text. | "Don't" | B/foundations/writing/text-truncation |
| 7 | Layout adapts at 600, 840, 1200 and 1600dp width; never keyed to device type or orientation. | "should" | B/foundations/layout/breakpoints/overview |
| 8 | Margins 16dp at compact, 24dp from medium up; 24dp spacer between panes. | spec | breakpoint tabs |
| 9 | Compact uses one pane with a navigation bar; medium and up swap to a navigation rail. | "Use" | breakpoints/compact, /overview |
| 10 | Never more than three panes; at least one flexible pane; fixed pane 360dp (expanded) or 412dp (large+). | "Don't" / "should" | B/foundations/layout/scaffold/panes |
| 11 | List-detail: back button only in single pane; selected state only in two-pane; detail keeps scroll position. | "Use ... only" | canonical-examples/list-detail |
| 12 | Line length 40-60 characters at every breakpoint; cap and centre single-pane content on desktop. | "keep" | breakpoints/overview; desktop/layout |
| 13 | Colours come from roles, used in their intended pairs (X with on X); no hard-coded hex. | "apply colors only in the intended pairs" | B/styles/color/roles; design-tokens/overview |
| 14 | Dividers use outline variant; boundaries of interactive targets use outline (3:1). | "Don't" | B/styles/color/roles |
| 15 | Separation by tonal surface containers; shadows only where needed; no surface tint overlays; component default elevations unchanged. | "Avoid" / deprecated | B/styles/elevation/* |
| 16 | State layers: hover 8%, focus 10%, pressed 10%, dragged 16% of the content colour; visible focus indicator for keyboard. | spec | interaction/states/state-layers |
| 17 | Text styles come from the 15 (+15 emphasized) type roles; sizes not altered; body text not in a decorative face. | "Avoid" | B/styles/typography/type-scale-tokens, /applying-type |
| 18 | Corner radii from the scale (0, 4, 8, 12, 16, 20, 28, 32, 48, full); nested radii follow outer - padding = inner. | "should consistently use" | B/styles/shape/corner-radius-scale |
| 19 | Component motion uses the theme motion scheme springs (spatial vs effects); effects never overshoot. | "should" | B/styles/motion/overview/how-it-works |
| 20 | Reduced-motion setting replaces slides/scales with fades and disables parallax and shape morph. | "should" | motion/transitions/applying-transitions |
| 21 | Hierarchical navigation uses the platform default forward/backward transition; no lateral slide between top-level destinations. | "should" / "Don't" | same |
| 22 | All UI text in sentence case; no title case, no all caps; no ellipsis on buttons/menu items; no trailing period on single-sentence labels. | "Don't" | content-design/style-guide/* |
| 23 | Icon-only controls have an accessibility label that states purpose without the control type; decorative images hidden; alt text has no "image of". | "Don't" | designing/elements; content-design/alt-text |
| 24 | Material Symbols at 20/24/40/48dp with one consistent weight (at least 200 at 24dp); navigation items labelled. | "Don't" / "must" | B/styles/icons/applying-icons |
| 25 | RTL: layout and directional icons mirrored; media controls, clocks and clockwise progress not mirrored; leading/trailing rather than left/right. | "should" | layout/bidirectionality-rtl |

Runner-up checks: pointer support (hover states, context menu on secondary click, Escape dismisses modals);
density never applied by default below 48dp targets; predictive back supported on sheets, navigation bar/rail and
search.

## 5. Stale lore vs current guidance (verified items only)

| Stale lore | Current guidance on m3.material.io | Source |
|---|---|---|
| "Window size classes: compact, medium, expanded" (three) | Renamed **breakpoints** (May 2026); five: compact <600, medium 600-839, expanded 840-1199, large 1200-1599, extra-large 1600+. | layout-overview/overview; breakpoints/overview |
| "Responsive layout" | Renamed "adaptive design". | layout-overview/overview |
| Use a navigation drawer on large screens | Breakpoint tables recommend a navigation rail, collapsed or expanded (modal or standard); the drawer does not appear in them. (Drawer status itself belongs to the components research.) | breakpoints/overview |
| M3 elevation = surface tint overlay (primary at 5/8/11/12/14%) | "Surface tint color is deprecated"; tone-based surface container roles replaced surfaces at +1 to +5 (Feb 2023). | elevation/tokens; color/system/overview |
| Shadows communicate every elevation (M2) | Tonal difference by default; shadows only for protection or interaction. Levels 0-5 = 0/1/3/6/8/12dp. | elevation/overview, /tokens |
| State layers: focus 12%, pressed 12% (early M3 numbers [M]) | Hover 8%, focus 10%, pressed 10%, dragged 16%. | interaction/states/state-layers |
| Motion = easing curves plus duration tokens | Springs (motion physics) for components; easing/duration is "legacy", "no longer maintained", still used for transitions. | motion/overview/how-it-works; easing-and-duration |
| Type scale has 15 styles | 30: 15 baseline + 15 emphasized. | typography/type-scale-tokens |
| Shape scale has 7 steps; "full" = 50% | 10 steps (added 20, 32, 48dp); full is its own fully rounded value. | shape/corner-radius-scale, /overview-principles |
| Material Icons (filled/outlined/round/sharp/two-tone icon fonts) | Material Symbols variable font is "the new default" (outlined, rounded, sharp; four axes). | icons/applying-icons |
| Title Case or ALL CAPS button labels (M2) | "Use sentence case for all product text"; "Avoid using caps blocks altogether". | style-guide/ux-writing-best-practices, /grammar-and-punctuation |
| "M3 Expressive is Material 4 / replaces M3" | "isn't a new version of the system ... this isn't 'M4'". | blog/building-with-m3-expressive |
| Expressive APIs are experimental/alpha | Stable in Compose Material 3 1.5.0 (Nov 2026); "most" experimental APIs promoted. | blog/compose-material-3-is-stable |
| Compose M2 and MDC Views are fine for new work | Compose M2 "deprecated"; Views 1.14.0 is the final feature release, maintenance mode. | same; blog/material-is-compose-first |
| On-container colours are near-black tone 10 | Since Aug 2024 on primary/secondary/tertiary/error container are "more colorful" in light theme. | color/system/overview |
| Dark theme needs a separate hand-made palette | Same roles for light and dark, generated together; three contrast levels on top. | color/system/how-the-system-works |
| Spacing is an informal 4/8dp grid | Tokenised spacing system (space0-space900, 8dp base), Compose only so far. | styles/spacing/tokens |

Not verified here, left out of the table: old M2 type names, 56dp bars, bottom app bar status, exact historical
state-layer values.

## 6. Licence and attribution statement

- B/get-started [V]: "All Material 3 content, guidelines, imagery, and resources are available under the Apache
  2.0 or CC BY 4.0 license." (No per-item split is given on that page.)
- Site footer [V]: links to Google "Privacy Policy" (policies.google.com/privacy) and "Terms of Service"
  (policies.google.com/terms); no copyright line or licence text in the rendered footer.
- B/styles/icons/designing-icons [V]: the icon keyline template "is available under Apache 2.0".
- Practical consequence: paraphrase and attribute to Google's Material Design with a link; short quotes for
  numbers are fine. Whether guideline prose is CC BY 4.0 and code Apache 2.0 is the usual reading [M]; the site
  sentence does not say which applies to what.

## 7. Recommended reference files for the material-design skill

| Proposed file | Contents | Apple analogue |
|---|---|---|
| `foundations-layout-adaptive.md` | breakpoints table, margins/spacers, scaffold (bars, rails, panes), pane rules, canonical layouts, navigation swap table, spacing tokens, density, desktop/foldable notes | foundations-layout.md |
| `foundations-color-elevation.md` | role table and pairing rules, dynamic vs static, contrast levels, surface containers, elevation levels, scrim, deprecated surface tint | foundations-color-materials.md |
| `foundations-typography.md` | 30-style table, emphasized usage, fonts and fallback, language height, text scaling behaviour | foundations-typography.md |
| `foundations-shape-icons.md` | corner scale, optical roundness, shape library and morph, Material Symbols axes/sizes/targets | foundations-icons-images.md |
| `foundations-motion.md` | motion schemes, spring tokens, legacy easing/duration tables, transition patterns, reduced motion | half of foundations-motion-writing.md |
| `foundations-writing.md` | sentence case, pronouns, punctuation, alt text, notifications, global writing | other half of foundations-motion-writing.md |
| `foundations-interaction-states.md` | state layers, focus, gestures, predictive back, selection, pointer/keyboard inputs | (Apple: inputs / focus content) |
| `foundations-accessibility.md` | targets, contrast, text scaling, labels and roles, focus order, shortcuts | accessibility reference |
| `foundations-rtl-global.md` (could fold into layout or writing) | mirroring rules and exceptions | right-to-left content |
| `platform-large-screens-desktop.md`, `platform-wear.md`, `platform-xr.md` | form-factor deltas; mostly from developer.android.com | platform files |

Motion and writing deserve separate files here: motion has two coexisting systems with token tables, and the
writing guide is long. Design tokens can be a short section inside the colour or a general "theming" file rather
than its own file.

## 8. Form-factor differences at a glance

| Topic | Phone (compact) | Tablet / foldable (medium, expanded) | Desktop (large, XL) | Watch | XR |
|---|---|---|---|---|---|
| Panes | 1 | 1-2 | 2, up to 3 at XL | single focused screens | spatial panels with explicit containment |
| Navigation | navigation bar | rail (bar if two panes at medium) | rail, expanded at XL | shallow, inline | rail/toolbars become orbiters |
| Margins | 16dp | 24dp | 24dp | percentages | n/a |
| Targets | 48dp | 48dp | 44dp pointer; 20dp icon in 40dp when dense | (Wear docs) | 56dp icon button, 4dp offset |
| Supplemental UI | bottom sheet, full-screen dialog | menu, basic dialog | menu, dialog, scrimless side sheet; detached bottom sheet only | tiles, notifications | elevation in depth |
| Input | touch | touch + keyboard/pointer | pointer + keyboard, context menus | touch, crown | gaze/hand/controller |
| Motion tokens | phone values | tablet values | duration scales with distance | wearable values | n/a |

## 9. Scratch material and gaps

Scratch folder: `<scratch>/m1/`
- `text/<slug with __ for />.txt`: cleaned visible text, 115 pages (all foundations and styles tabs, get-started,
  five blog posts). First line is the URL.
- `pages/`: same pages raw, with the link list of each page appended; `pages/_map.tsv` = requested path, final
  path, title, length.
- `tokens/`: pages re-rendered with token modules expanded (type scale, motion specs).
- `hub_*.txt`: hub pages with link lists (blog index includes all post slugs).
- `crawl.js`, `r.js`, `tok.js`: crawler, single-page renderer with links, token-module expander.

Not verified / gaps:
- Expressive-scheme spring damping and stiffness (module showed the standard Android context only) [M].
- Baseline colour hex values and per-role tone numbers (module not expanded).
- Height breakpoint dp values; fold postures; Android version requirement for dynamic colour (not on these pages).
- Component-level numbers (bar heights, button label rules) are out of scope for this file.
- Alt-text length conflict (125 vs 140 characters) is on the site itself.
- `foundations/content-design/overview`, `xr/*`, `watches/styles`, `color/advanced/*`, `glossary` were rendered and
  saved but only skimmed.
