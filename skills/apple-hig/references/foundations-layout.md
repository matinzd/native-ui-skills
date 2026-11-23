# Layout

Scope: visual hierarchy, adaptivity, size classes, safe areas and guides, spacing numbers, scroll edge effects,
per-platform layout rules and right-to-left layout.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- What the Layout page no longer contains
- Visual hierarchy and grouping
- Controls vs. content (OS 26+, Liquid Glass)
- Scroll edge effects
- Adaptivity and text-size changes
- Size classes (iOS, iPadOS)
- Safe areas, margins and layout guides
- Spacing and control-size numbers
- Platform notes
- Right-to-left
- Common mistakes

## What the Layout page no longer contains

- [HIG] The current Layout page (last changed 2026-09-09) has no device-dimension table and no numeric margins for
  iOS, iPadOS or macOS. It defers to Apple Design Resources for margins and safe areas. Do not quote device point
  sizes, a "16 pt" or "20 pt" margin, or a readable-width number as HIG facts.
- [Conv] Numbers such as 16/20 pt screen margins and an 8 pt spacing grid are community convention. Take real values
  from system layout margins and safe-area insets at runtime.
- [HIG] The only hard layout numbers on the page are for tvOS (safe insets, grids) and visionOS (60 pt centers).

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Visual hierarchy and grouping

- [HIG] Order by importance in reading order: most important content near the top and the leading side.
- [HIG] Align elements so they scan easily; aligned items read as related. Use indentation only to show that an item
  is subordinate to the one above it.
- [HIG] Group related items with negative space, container shapes or separator lines.
- [HIG] Use progressive disclosure (disclosure controls, menus, nested views, scrollable sections) instead of
  showing every choice at once.
- [HIG] Prefer standard system components so reading-order placement adapts to right-to-left automatically.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Controls vs. content (OS 26+, Liquid Glass)

- [HIG] Let controls be distinguished by the Liquid Glass material on platforms that support it.
- [HIG] Do not put a solid or semi-opaque background color beneath controls (bars, floating buttons). Use a scroll
  edge effect to lift controls above content.
- [HIG] Extend full-screen background content underneath sidebars, toolbars and tab bars so it fills the whole
  screen or window (full bleed). Layout content still respects safe areas; only the background extends.
- [HIG] If a sidebar or inspector would cover an important part of a full-bleed image, use a background extension
  effect, which mirrors and blurs the image under the adjacent component. The page names `backgroundExtensionEffect()`
  (SwiftUI) and `UIBackgroundExtensionView` (UIKit).
- [HIG] When display aspect ratio changes, never change background artwork's aspect ratio; scale it to fill.
  Windows can be very wide or very tall, so artwork needs bleed beyond a standard aspect ratio.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Scroll edge effects

Applies to iOS, iPadOS and macOS. System bars get the effect automatically.

- [HIG] Prefer the automatic style. It becomes more opaque for top toolbars with many controls, for text outside
  glass controls and for pinned table headers. If the soft style is chosen instead, test control legibility widely.
- [HIG] Add the effect manually only for custom bars that need extra clarity, and only where a scroll view sits
  behind floating interface elements. It is not decoration and does not dim like an overlay.
- [HIG] One scroll edge effect per view. In split views on iPad and Mac each pane may have its own; keep their
  heights consistent so they align.
- [HIG] Under the status bar, prefer a scroll edge effect (blurred view) so the status bar stays readable and
  content behind it does not look interactive.

Source: https://developer.apple.com/design/human-interface-guidelines/scroll-views
Source: https://developer.apple.com/design/human-interface-guidelines/status-bars

## Adaptivity and text-size changes

- [HIG] Handle all of: both size classes in both dimensions, different screen sizes, orientations and aspect
  ratios, the Dynamic Island, external displays, Display Zoom, resizable windows on iPad and Mac, text-size changes,
  and locale effects (layout direction, formats, font variation, text length).
- [HIG] Keep the experience recognizable across rotation, window resizing, added displays and device changes.
- [HIG] An orientation-locked app (for example a landscape-only game) still needs to resize well across devices and
  window sizes.
- [HIG] Support larger text by changing layout: stack horizontally adjacent views vertically, let rows and
  containers grow in height, allow single-line rows to wrap to several lines. The page warns that apps ignoring
  text size can be difficult or impossible to use.
- [HIG] Test the largest and the smallest layouts first, across size classes, localizations and text sizes. The page
  names Device Hub (simulated devices) for this, including iPad resizing and iPhone Mirroring on Mac.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Size classes (iOS, iPadOS)

- [HIG] Two dimensions, two values each: horizontal compact (narrow) or regular (wide); vertical compact (short) or
  regular (tall). The system derives them from device type, window configuration and multitasking state.
- [HIG] An iOS or iPadOS app can appear in every combination, for example when resized on iPad, run on Mac, or
  shown through iPhone Mirroring (where width and height are freely resizable).
- [HIG] Decide layout from size classes, never from device type (idiom) or orientation; those say nothing about
  available space.
- [HIG] Design for all combinations. A regular-width, compact-height landscape iPhone layout must not waste vertical
  space when the same size class pair gains regular height on iPad.
- [HIG] Do not change functionality with available space. Changing how much is visible is fine: switch a tab bar to
  a sidebar, or surface items that were in an overflow menu.
- [HIG] The idiom stays the same while size classes change; keep the layout recognizable for that platform.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Safe areas, margins and layout guides

- [HIG] A safe area is the part of a window not covered at its edges by a hardware feature or by another view such
  as a toolbar, tab bar or status bar. The page calls respecting it essential (Dynamic Island is its example).
- [HIG] Layout guides are rectangular regions for positioning and spacing. The system provides predefined guides
  for standard margins and for restricting text width for readability; use them instead of hard-coded insets. The
  page names `UILayoutGuide` and `NSLayoutGuide` and gives no numeric readable width.
- [HIG] Respect system safe areas, margins and guides where available, then fine-tune with layout modifiers.

Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Spacing and control-size numbers

These numbers come from the Accessibility and Buttons pages, not the Layout page. All are worded as general rules.

| Platform | Default control size | Minimum control size |
|----------|----------------------|----------------------|
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

- [HIG] Padding of about 12 pt around elements that have a bezel; about 24 pt around the visible edges of elements
  without a bezel.
- [HIG] HIG inconsistency to flag: common lore and the Buttons page say a button needs a hit region of at least
  44x44 pt (60x60 pt in visionOS), while the Accessibility table lists 44x44 as the iOS default and 28x28 as the
  minimum. Use 44x44 pt (60x60 in visionOS) as the target for buttons; treat 28x28 as the floor for dense secondary
  controls, and report anything below 44 as a warning, not a hard failure.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility
Source: https://developer.apple.com/design/human-interface-guidelines/buttons

## Platform notes

| Platform | Layout rules stated in the HIG |
|----------|--------------------------------|
| iOS, iPadOS | No additional considerations on the Layout page. Use size classes, layout margins, safe areas. |
| iPhone Duo | Outer display = compact width, inner display = regular width. Bars move to the side except on the inner display in portrait. Reserved regions (outer camera, inner camera when active, folding region). Avoid fixed widths. Full rules: `references/platforms-ios.md`. |
| macOS | Do not put controls or critical information at the bottom of a window (people park windows partly off-screen). Do not show content behind the camera housing at the top edge. |
| tvOS | Inset primary content 60 pt from top and bottom and 80 pt from each side (overscan safety). Leave padding between focusable elements because focused items grow. Grid specs below. |
| visionOS | Support resizing of windows and volumes; keep content horizontally centered at very large sizes; min and max sizes are for preventing overlap and unwieldy layouts, not for blocking resizing. Button centers at least 60 pt apart. Supplemental content goes in an adjacent window, not an ornament. Use 3D content in windows sparingly and inset. |
| watchOS | No more than three glyph buttons or two text buttons in a row; prefer full-width text buttons; two short text buttons side by side only when the screen does not scroll. Autorotate only views people show to others (image, QR code). |

tvOS grids: horizontal spacing 40 pt and minimum vertical spacing 100 pt in every case.

| Columns | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---------|---|---|---|---|---|---|---|---|
| Unfocused content width (pt) | 860 | 560 | 410 | 320 | 260 | 217 | 184 | 160 |

- [HIG] tvOS: add extra vertical space for titled rows; keep spacing consistent; make partially hidden off-screen
  items the same width on both sides.
- [HIG] visionOS: the Eyes and Spatial layout pages add that interactive items need a margin of at least 16 pt
  around their bounds or centers at least 60 pt apart.
- [HIG] iPhone Duo: side-placed controls stay on the same physical side in right-to-left languages, and content
  space is asymmetric, so rely on safe areas on both edges (Split View multitasking puts another app's controls on
  the opposite edge).

Source: https://developer.apple.com/design/human-interface-guidelines/layout
Source: https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo
Source: https://developer.apple.com/design/human-interface-guidelines/spatial-layout
Source: https://developer.apple.com/design/human-interface-guidelines/eyes

## Right-to-left

System frameworks flip standard components and layouts automatically; the rules below matter for custom layout.

- [HIG] Mirror text alignment with the interface direction when the system does not.
- [HIG] Align a paragraph (three or more lines) by its own language; align one- and two-line blocks by the
  interface direction. Use one alignment for every item in a list, including items in another script.
- [HIG] Never reverse the digits inside a number (phone, card, "541"). Do reverse the order of numerals that show
  progress or sequence, without flipping the glyphs.
- [HIG] Flip controls that show progress (sliders, progress indicators) and swap their start and end glyphs. Flip
  ordered navigation: back points right in RTL (the page words this as "must"), as do next and previous.
- [HIG] Do not flip a control that refers to a real direction or points at an on-screen area.
- [HIG] Do not flip photos, illustrations, logos, universal marks such as the checkmark, or icons of real-world
  objects (clocks, right-handed tools). Reverse the positions of images whose order is meaningful.
- [HIG] Flip icons that depict text, reading direction, or forward and backward motion (speaker sound waves).
  SF Symbols supplies RTL and localized variants; custom symbols can declare directionality.
- [HIG] When Arabic or Hebrew sits next to all-caps Latin text, increasing the RTL font size by about 2 pt balances it.

Source: https://developer.apple.com/design/human-interface-guidelines/right-to-left

## Common mistakes

- Branching layout on device model, idiom or orientation -> branch on size classes and available space.
- Hard-coding screen sizes, margins or notch/Dynamic Island insets -> use safe areas, layout margins and guides.
- Opaque or tinted background painted under a toolbar or tab bar (OS 26+) -> remove it; rely on the scroll edge
  effect and let content extend under the bar.
- Background image stopping at the bar or sidebar edge -> extend it full bleed; use the background extension effect.
- Stretching artwork to a new aspect ratio -> scale to fill and provide bleed.
- Truncating or clipping at large text sizes -> stack, wrap and let rows grow.
- Removing features in compact width -> same functionality, less of it visible (overflow menu, tab bar).
- tvOS content flush to the screen edge -> 60 pt top and bottom, 80 pt side insets.
- macOS primary button at the very bottom of a resizable window -> move it out of the bottom edge.
- visionOS window with min == max size to stop resizing -> allow resizing; adapt and center content.
- Using left/right instead of leading/trailing, or mirroring logos and numbers in RTL -> follow the flip rules above.
- Citing "44 pt minimum" as an absolute HIG requirement -> it is a general rule; the table minimum is 28x28 pt.
