# Icons, SF Symbols, app icons and images

Scope: SF Symbols configuration and animation, interface icons and the standard-action symbol table, the layered
app icon model, and image assets.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- SF Symbols: rendering and color
- SF Symbols: weights, scales and variants
- SF Symbols: animations
- Custom symbols and licence limits
- Interface icons
- Standard symbols for common actions
- App icons: layers and format
- App icons: design, appearances and specifications
- Images
- Common mistakes

## SF Symbols: rendering and color

- [HIG] Symbol and feature availability depends on the OS version targeted; features introduced in a given year
  are not available on earlier systems. Check before using a new symbol or effect.
- [HIG] Four rendering modes:

| Mode | What it does | Typical use |
|------|--------------|-------------|
| Monochrome | One color on all layers | Default look, toolbars, text-adjacent symbols |
| Hierarchical | One color, opacity varies by layer level | Depth and emphasis with a single tint |
| Palette | Two or more colors, one per layer (with two colors, secondary and tertiary layers share one) | Matching a custom color scheme |
| Multicolor | Intrinsic colors that carry meaning (green `leaf`, red in `trash.slash`) | When the real-world color aids recognition |

- [HIG] The automatic setting picks a symbol's preferred mode; still check legibility at the actual size and
  against the actual background.
- [HIG] Use system colors so symbols adapt to vibrancy, Dark Mode and accessibility settings.
- [HIG] Gradients (SF Symbols 7 and later): a linear gradient generated from one source color, available in every
  rendering mode and for custom symbols; looks best at larger sizes.
- [HIG] Variable color shows a value that changes over time (signal strength, volume) by coloring layers at
  thresholds. Use it for change, never for depth; use Hierarchical for depth.

Source: https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## SF Symbols: weights, scales and variants

- [HIG] Nine weights, ultralight to black, each matching a San Francisco font weight. Match symbol weight to
  adjacent text unless emphasis is intended.
- [HIG] Three scales: small, medium (default), large, defined relative to the font's cap height. Scale changes
  emphasis without breaking weight matching.
- [HIG] Design variants: outline (most common), fill, slash, and enclosed (circle, square, rectangle); many
  combine. Slash can show unavailability; fill can show selection.
- [HIG] Outline suits toolbars, lists and symbols next to text. Fill gives more emphasis and suits iOS tab bars,
  swipe actions and accent-colored selection. Enclosed shapes help legibility at small sizes.
- [HIG] The hosting view usually chooses outline or fill itself (an iOS tab bar prefers fill, a toolbar outline),
  so do not hard-code the variant there.
- [HIG] Language- and script-specific variants (Latin, Arabic, Hebrew, Hindi, Thai, Chinese, Japanese, Korean,
  Cyrillic, Devanagari and several Indic numeral systems) switch automatically with the device language. RTL
  variants are included.

Source: https://developer.apple.com/design/human-interface-guidelines/sf-symbols
Source: https://developer.apple.com/design/human-interface-guidelines/right-to-left

## SF Symbols: animations

Animations work on every symbol, rendering mode, weight and scale, and on custom symbols. Playback can run once or
repeat until a condition is met.

| Animation | Meaning to use it for |
|-----------|-----------------------|
| Appear / Disappear | Symbol entering or leaving view |
| Bounce | One-shot: an action occurred or is needed |
| Scale | Persistent size change: selection, press feedback |
| Pulse | Opacity cycling: ongoing activity |
| Variable color | Cumulative or iterative layer coloring: progress, connecting, broadcasting |
| Replace | Swap symbols: down-up (state change), up-up (forward progression), off-up (emphasize next state) |
| Magic Replace | Default replace between related shapes (slash drawn on or off, badge added or removed); falls back to down-up for unrelated symbols |
| Wiggle | Draw attention to a change or call to action; reinforce direction |
| Breathe | Opacity and size cycling: ongoing status such as recording |
| Rotate | Whole symbol or by layer: task in progress, real-world behaviour |
| Draw On / Draw Off | SF Symbols 7 and later: draws along a path; progress or reinforcing meaning |

- [HIG] Animate sparingly and only when the motion communicates the symbol's intent; too many animated symbols
  distract.
- [HIG] Prefer a symbol animation to a larger custom animation for compact feedback, and match the app's tone.

Source: https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## Custom symbols and licence limits

- [Req] The SF Symbols terms prohibit using symbols, or confusingly similar images, in app icons, logos or any
  other trademarked use.
- [Req] Symbols that depict Apple products and features are copyrighted: they may be displayed but not customized
  (the SF Symbols app marks them with an Info badge and lists restrictions). Do not design replicas of Apple
  products as custom symbols.
- [HIG] Build a custom symbol from the exported template of a similar system symbol; match level of detail,
  optical weight, alignment, position and perspective. Aim for simple, recognizable, inclusive and directly related
  to the action or content.
- [HIG] Annotate layers (color or hierarchical level) so the symbol supports the rendering modes and by-layer
  animation; draw whole shapes and use erase layers instead of cut-outs; test every animation preset.
- [HIG] Do not draw common variants (enclosures, badges) by hand; generate them from the SF Symbols app's
  component library.
- [HIG] Use negative side margins for optical alignment of badged symbols, with the page's naming pattern (for
  example "left-margin-Regular-M").
- [HIG] Give every custom symbol and custom interface icon an alternative text label for VoiceOver.

Source: https://developer.apple.com/design/human-interface-guidelines/sf-symbols

## Interface icons

- [HIG] An interface icon (glyph) expresses one concept with a simplified, familiar shape; black and clear define
  the shape and the system applies color.
- [HIG] Keep all icons in an app consistent in size, detail, stroke weight and perspective, whether custom,
  system or mixed.
- [HIG] Add padding inside the asset to center asymmetric icons optically.
- [HIG] Do not supply selected-state versions for icons in standard components (toolbars, tab bars, buttons); the
  system draws selection.
- [HIG] Include text in an icon only when essential; localize characters; for a passage of text use an abstract
  representation and provide a flipped version for RTL.
- [HIG] Use a vector format (PDF or SVG) for custom icons; PNG needs one file per scale factor. A custom SF Symbol
  is the alternative when the icon should match text.
- [HIG] Do not depict Apple hardware; if unavoidable use only Apple Design Resources images or the matching
  SF Symbols.
- [HIG] macOS document icons: supply any of a background fill, a center image and short text; the system
  composites the folded-corner shape. Background sizes 16, 32, 128, 256 and 512 px at @1x and @2x; the center image
  is half the canvas with about a 10% margin; keep the top-right corner of the fill free; without a custom icon
  macOS composites the app icon and file extension.

Source: https://developer.apple.com/design/human-interface-guidelines/icons

## Standard symbols for common actions

Use these symbol names for these actions in menus, toolbars and buttons on all platforms (table added 2025-06-09).
Actions listed together share one symbol.

| Action | Symbol | Action | Symbol |
|--------|--------|--------|--------|
| Cut | `scissors` | Search | `magnifyingglass` |
| Copy | `document.on.document` | Find, Find and Replace, Find Next, Find Previous, Use Selection for Find | `text.page.badge.magnifyingglass` |
| Paste | `document.on.clipboard` | Filter | `line.3.horizontal.decrease` |
| Done, Save | `checkmark` | Share, Export | `square.and.arrow.up` |
| Cancel, Close, Deselect | `xmark` | Print | `printer` |
| Delete | `trash` | Account, User, Profile | `person.crop.circle` |
| Undo | `arrow.uturn.backward` | Like | `hand.thumbsup` |
| Redo | `arrow.uturn.forward` | Dislike | `hand.thumbsdown` |
| Compose | `square.and.pencil` | Select | `checkmark.circle` |
| Duplicate | `plus.square.on.square` | Bold, Italic, Underline | `bold`, `italic`, `underline` |
| Rename | `pencil` | Superscript, Subscript | `textformat.superscript`, `textformat.subscript` |
| Move to, Folder | `folder` | Align Left, Center, Right, Justified | `text.alignleft`, `text.aligncenter`, `text.alignright`, `text.justify` |
| Attach | `paperclip` | Bring to Front, Send to Back | `square.3.layers.3d.top.filled`, `square.3.layers.3d.bottom.filled` |
| Add | `plus` | Bring Forward, Send Backward | `square.2.layers.3d.top.filled`, `square.2.layers.3d.bottom.filled` |
| More | `ellipsis` | Alarm, Archive, Calendar | `alarm`, `archivebox`, `calendar` |

- [HIG] Do not invent a different glyph for these actions, and do not reuse these symbols for other meanings (on
  iPhone Duo the ellipsis is reserved for the system overflow menu).

Source: https://developer.apple.com/design/human-interface-guidelines/icons
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo

## App icons: layers and format

Current model (layered icons since 2025-06-09; format guidance added 2026-10-28). The old "one flattened PNG per
size" workflow is stale lore.

- [HIG] iOS, iPadOS, macOS and watchOS icons have a background layer plus one or more foreground layers and take
  on Liquid Glass attributes (specular highlights, refraction, translucency) applied by the system.
- [HIG] Two accepted formats on those platforms: a layered Icon Composer file (preferred, full control over glass
  and appearance variants) or a nonlayered bitmap such as PNG. With a bitmap the system tries to segment the icon
  into two layers and applies glass only to large simple foreground shapes, not to text or thin lines.
- [HIG] Icon Composer (ships with Xcode) is where the background is defined, layers placed, effects set, and
  default, dark and mono variants annotated and previewed.
- [HIG] tvOS icons use two to five layers (parallax on focus). visionOS icons use a background plus one or two
  layers (3D, expands when looked at). Both are built as image stacks in Xcode, not in Icon Composer.
- [Req] The tvOS app icon must be a layered image, and a layered image's background layer must be opaque (the
  Images page says a non-opaque background produces an error).
- [HIG] Provide unmasked layers in the platform's layout shape; the system masks. Pre-masked layers break
  highlights and produce jagged edges.
- [HIG] Foreground layers: clearly defined edges (no soft or feathered edges), varied opacity for depth, vector
  artwork (SVG or PDF) with text outlined; PNG for mesh gradients and raster art. An imported background must be
  full-bleed and opaque; solid colors and gradients can be set in Icon Composer directly.
- [HIG] Do not bake in highlights, drop shadows, bevels, blurs or glows; the system adds dynamic effects.

Source: https://developer.apple.com/design/human-interface-guidelines/app-icons
Source: https://developer.apple.com/design/human-interface-guidelines/images

## App icons: design, appearances and specifications

- [HIG] One simple core idea, few shapes, simple background (solid or gradient); no need to fill the canvas.
- [HIG] Keep the design consistent across every platform the app supports.
- [HIG] Text only when essential to the brand; never instructions ("Watch", "Play") or context terms ("New").
- [HIG] Prefer illustration to photos; no screenshots or replicas of UI components; avoid very thin lines and
  sharp corners.
- [Req] Do not use replicas of Apple hardware (the page says they are copyrighted and cannot be reproduced).
- [HIG] Keep primary content centered, especially for the circular visionOS and watchOS masks.
- [HIG] Appearances (iOS, iPadOS, macOS): people choose default, dark, clear or tinted. Provide the variants or
  let the system generate missing ones. Keep the same core features in every variant; base the dark icon on the
  light one; avoid very bright imagery.
- [HIG] Alternate app icons (iOS, iPadOS, tvOS, compatible apps in visionOS) must stay clearly related to the app.
- [Req] Alternate icons in iOS and iPadOS need their own dark, clear and tinted variants, and all alternate and
  variant icons are subject to App Review.
- [HIG] tvOS: keep a safe zone, because focus scaling crops edges and foreground layers crop more. visionOS: no
  hole or concave shapes on the background layer. watchOS: no black background; lighten it.

| Platform | Layout | Masked shape | Layout size | Appearances |
|----------|--------|--------------|-------------|-------------|
| iOS, iPadOS, macOS | Square | Rounded rectangle | 1024x1024 px | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | Landscape rectangle | Rounded rectangle | 800x480 px | n/a |
| visionOS | Square | Circle | 1024x1024 px | n/a |
| watchOS | Square | Circle | 1088x1088 px | n/a |

- [HIG] The system scales the icon for smaller placements (Settings, notifications). Color spaces: sRGB, Gray
  Gamma 2.2, and Display P3 on all platforms except visionOS.

Source: https://developer.apple.com/design/human-interface-guidelines/app-icons

## Images

| Platform | Bitmap scale factors |
|----------|----------------------|
| iOS | @2x and @3x |
| iPadOS, watchOS | @2x |
| macOS, tvOS | @1x and @2x |
| visionOS | @2x or higher |

- [HIG] Supply every bitmap at each scale factor of the devices supported. A point maps to pixels on 2D displays
  and is an angular unit in visionOS.
- [HIG] Formats: de-interlaced PNG for bitmap art (8-bit palette when full 24-bit color is not needed); JPEG or
  HEIC for photos; stereo HEIC for spatial photos; PDF or SVG for flat icons and artwork that must scale.
- [HIG] Embed a color profile; test on real devices.
- [HIG] tvOS: layered images (two to five layers) are required for the parallax effect and strongly encouraged for
  focusable images including Top Shelf; keep text in the foreground, keep a safe zone, preview on a real TV.
- [HIG] visionOS: prefer vector art for 2D images; raster above @2x costs performance, particularly beyond @6x;
  show spatial photos and scenes in standalone views, not inline.
- [HIG] watchOS: avoid transparency except in template images (complications, menu icons); an autoscaling PDF
  designed at @2x for 40mm and 42mm scales per screen size (38mm 90%, 41mm 106%, 44mm 110%, 45mm and 49mm 119%).

Source: https://developer.apple.com/design/human-interface-guidelines/images

## Common mistakes

- Custom glyph for Share, Delete, Search and similar -> the standard symbol from the table.
- An SF Symbol used as, or inside, the app icon or logo -> prohibited by the SF Symbols terms; draw original art.
- Forcing `.fill` on tab bar symbols or outline in toolbars -> let the container choose the variant.
- Variable color or multicolor used as decoration -> variable color for changing values; Hierarchical for depth.
- Symbol weight or scale that does not match adjacent text -> match weight; adjust scale for emphasis.
- Looping symbol animations everywhere -> one purposeful animation tied to a state change.
- PNG interface icons at one scale -> PDF, SVG or a custom symbol.
- Custom icon with no accessibility label -> add alternative text.
- Flattened, pre-rounded app icon with baked shadows and gloss -> unmasked square layers, system effects only.
- App icon variants that swap elements between default, dark and tinted -> same features in every appearance.
- Black watchOS icon background, or a non-opaque tvOS background layer -> lighten; make it opaque.
- Supplying iOS images at @1x only, or macOS at @3x -> use the platform's scale factors.
