# Color, Dark Mode and materials

Scope: system colors, accent color, contrast figures, Dark Mode, materials, vibrancy and Liquid Glass rules.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Color basics
- System and semantic colors
- Accent color and tint
- Contrast figures
- Dark Mode
- Liquid Glass (OS 26+)
- Color on Liquid Glass
- Standard materials and vibrancy
- Platform notes
- Common mistakes

## Color basics

- [HIG] One color, one meaning. If the brand color marks interactive borderless buttons, do not use the same or a
  similar color for non-interactive text.
- [HIG] Never rely on color alone to differentiate objects, show interactivity or convey essential information;
  add text labels, glyph shapes or icons. Red-green and blue-orange pairings are named as hard to distinguish.
- [HIG] Every color has to work in light, dark and increased-contrast contexts. System colors already have all
  variants. For a custom color supply light and dark variants plus an increased-contrast option for each.
- [HIG] (OS 26+) Supply both light and dark colors even when the app ships a single appearance, because Liquid
  Glass adapts between light and dark on its own.
- [HIG] Test under varied lighting and on different devices (True Tone, several TV brands for tvOS, P3 and sRGB
  profiles on Mac). Colors near or behind translucent elements shift.
- [HIG] Check color meaning per culture (red is danger in some cultures and positive in others).
- [HIG] For color picking, prefer the system color controls (the page names `ColorPicker`).
- [HIG] Embed a color profile in images (sRGB by default). For wide color use Display P3 at 16 bits per channel,
  exported as PNG; add per-color-space asset variants only if P3 colors merge or gradients clip on sRGB displays.

Source: https://developer.apple.com/design/human-interface-guidelines/color

## System and semantic colors

- [HIG] Do not hard-code system color values. Published values are design-time reference and can change between
  releases and with environment; apply system colors through the color APIs.
- [HIG] Do not redefine what a dynamic system color means. Examples from the page: do not use the separator color
  for text, or the secondary label color as a background.
- [HIG] Named system colors (SwiftUI names): red, orange, yellow, green, mint, teal, cyan, blue, indigo, purple,
  pink, brown. Each has default and increased-contrast values for light and dark. visionOS uses the default dark
  values.
- [HIG] iOS and iPadOS grays: `systemGray` and `systemGray2` to `systemGray6` (UIKit); the SwiftUI equivalent of
  `systemGray` is `gray`.
- [HIG] iOS and iPadOS backgrounds come in two sets, each with primary, secondary and tertiary levels:

| Set | Use | UIKit names |
|-----|-----|-------------|
| System | Default for views | `systemBackground`, `secondarySystemBackground`, `tertiarySystemBackground` |
| Grouped | Grouped table views | `systemGroupedBackground`, `secondarySystemGroupedBackground`, `tertiarySystemGroupedBackground` |

- [HIG] Level meaning in both sets: primary for the overall view, secondary for groups inside it, tertiary for
  groups inside secondary elements.
- [HIG] iOS and iPadOS foreground colors: `label`, `secondaryLabel`, `tertiaryLabel`, `quaternaryLabel`,
  `placeholderText`, `separator` (lets content show through), `opaqueSeparator`, `link`.
- [HIG] macOS has its own semantic set (for example `labelColor`, `secondaryLabelColor`, `controlAccentColor`,
  `controlBackgroundColor`, `windowBackgroundColor`, `separatorColor`, `selectedContentBackgroundColor`,
  `unemphasizedSelectedContentBackgroundColor` for non-key windows, `keyboardFocusIndicatorColor`). See the page
  for the full list.

Source: https://developer.apple.com/design/human-interface-guidelines/color

## Accent color and tint

- [HIG] Use the accent (brand) color sparingly: primary actions and status indicators, not every control.
- [HIG] With colorful backgrounds or rich content, prefer monochrome toolbars and tab bars, or pick an accent with
  clear visual differentiation. With mostly monochrome content, a brand accent color works well.
- [HIG] macOS: an app accent color (macOS 11 and later) customizes buttons, selection highlighting and sidebar
  icons, but only while the user's Accent color setting is multicolor. Any other user choice replaces the app
  accent everywhere except sidebar icons that use a fixed color.
- [HIG] watchOS: people may prefer tinted mode over full color for graphic complications; design for both.

Source: https://developer.apple.com/design/human-interface-guidelines/color
Source: https://developer.apple.com/design/human-interface-guidelines/branding

## Contrast figures

The Accessibility page lists the WCAG Level AA values that Accessibility Inspector checks, and also names APCA as a
standard. It is worded "strive to meet".

| Text size | Weight | Minimum contrast |
|-----------|--------|------------------|
| Up to 17 pt | Any | 4.5:1 |
| 18 pt | Any | 3:1 |
| Any | Bold | 3:1 |

- [HIG] If default colors miss these values, at least provide a higher-contrast scheme when Increase Contrast is
  on. Check both light and dark appearances.
- [HIG] The Dark Mode page gives stricter numbers for all appearances: never below 4.5:1, and aim for 7:1 for
  custom foreground and background colors, especially small text.
- [Conv] The two pages differ (3:1 allowed for large or bold text vs. a flat 4.5:1 floor). Use 4.5:1 as the working
  floor, accept 3:1 only for bold text or text at 18 pt (the table row says only "18 pts"; read it as 18 pt and
  larger, as in WCAG), and target 7:1 for custom small text.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility
Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Dark Mode

Dark Mode is a setting in iOS, iPadOS, macOS and tvOS. It is not supported in visionOS or watchOS.

- [HIG] Do not add an app-specific appearance setting; follow the system choice.
- [HIG] Look right in both modes and when Auto switches appearance while the app is running.
- [HIG] A permanently dark UI is acceptable only in rare cases such as immersive media viewing.
- [HIG] Use semantic colors that adapt. For custom colors use a Color Set asset with both variants. Avoid
  hard-coded or non-adapting colors. Dark colors are not simple inversions of light ones.
- [HIG] Test with Increase Contrast and Reduce Transparency, each alone and together, in both modes.
- [HIG] Use the system label colors (primary to quaternary) for text and system views for text fields and text
  views so vibrancy is handled.
- [HIG] Prefer SF Symbols; provide separate light and dark interface icons or images only when one asset does not
  work in both. Slightly darken content images with white backgrounds so they do not glow.
- [HIG] iOS and iPadOS: dark backgrounds have base and elevated variants; the system switches to elevated for
  foreground layers (popovers, sheets, multitasking, multiple windows). Prefer the system background colors so this
  works; custom backgrounds hide the distinction.
- [HIG] macOS: with the graphite accent color, windows pick up desktop color (desktop tinting). Give custom
  component backgrounds some transparency only in neutral states, never in a state that uses color.

Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Liquid Glass (OS 26+)

Liquid Glass is the material of the functional layer: controls and navigation (tab bars, sidebars, toolbars) that
float above content. Standard components adopt it automatically.

- [HIG] Do not use Liquid Glass in the content layer (worded "Don't"). Use standard materials there, for example
  for app backgrounds. Exception: transient interactive parts of content-layer controls such as sliders and
  toggles take on glass while being operated.
- [HIG] Apply glass effects to custom controls sparingly: only the most important functional elements.
- [HIG] Two variants exist for custom components and some system components:

| Variant | Behaviour | Use for |
|---------|-----------|---------|
| Regular | Blurs and adjusts luminosity of what is behind; most system components use it | Any background that could hurt legibility; components with a lot of text (alerts, sidebars, popovers) |
| Clear | Highly translucent | Only components floating over visually rich media such as photos and video |

- [HIG] With clear glass over bright content, consider a dark dimming layer of 35% opacity behind the component.
  Skip it when the content is already dark or when standard AVKit playback controls supply their own dimming.
- [HIG] Appearance of both variants changes with user settings (preferred glass look, Reduce Transparency,
  Increase Contrast); do not assume a fixed translucency.
- [HIG] App icons on iOS, iPadOS, macOS and watchOS also take on glass attributes; see
  `references/foundations-icons-images.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/materials
Source: https://developer.apple.com/design/human-interface-guidelines/app-icons
Source: https://developer.apple.com/design/human-interface-guidelines/motion

## Color on Liquid Glass

- [HIG] Glass has no color of its own; it takes color from content behind it. Small elements (toolbars, tab bars)
  flip between light and dark with the underlying content, and their symbols and text are monochrome by default.
  Large elements (sidebars) are more opaque.
- [HIG] Tint sparingly, only where emphasis is earned: status indicators and primary actions.
- [HIG] To emphasize a primary action, color the control's background, not its symbol or text. This is what the
  system's prominent button style does with the accent color (the Done button is the page's example).
- [HIG] Do not color the backgrounds of several controls in the same area.
- [HIG] Avoid label colors similar to a colorful background behind the controls.
- [HIG] Check the resting state (for example the top of a scroll view): content directly under controls must leave
  them legible even if colorful content scrolls beneath later.
- [HIG] Do not paint a solid or semi-opaque background under glass controls; see the scroll edge effect rules in
  `references/foundations-layout.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/color
Source: https://developer.apple.com/design/human-interface-guidelines/layout

## Standard materials and vibrancy

Standard materials (blur, vibrancy, blending) structure the content layer beneath Liquid Glass.

- [HIG] Choose a material by its semantic purpose and recommended use, never by the color it appears to give;
  system settings change its look.
- [HIG] Put system vibrant colors on top of any material for legibility.
- [HIG] Thicker (more opaque) materials give better contrast for text and fine detail; thinner materials keep more
  background context visible.

| Platform | Materials and vibrancy |
|----------|------------------------|
| iOS, iPadOS | Four materials: ultra-thin, thin, regular (default), thick. Vibrancy: labels default, secondary, tertiary, quaternary; fills default, secondary, tertiary; one separator level. Avoid quaternary label on thin and ultra-thin (contrast too low). |
| macOS | Several purpose-named materials with vibrant versions of system colors; two blending modes, behind window and within window. Decide per custom view whether vibrancy helps. |
| tvOS | ultraThin: full-screen views needing a light scheme. thin: overlays needing a light scheme. regular: overlays. thick: overlays needing a dark scheme. |
| visionOS | Window background is a system "glass" material that apps cannot modify. For custom components: thin for interactive elements and selection, regular to separate sections (sidebar, grouped table), thick for a dark element on a regular background. Vibrancy levels: label (standard text), secondaryLabel (footnotes, subtitles), tertiaryLabel (inactive, low-legibility text only). |
| watchOS | Keep the default material background of full-screen modal sheets; do not remove or replace it. |

Source: https://developer.apple.com/design/human-interface-guidelines/materials

## Platform notes

| Platform | Dark Mode | Liquid Glass | Color specifics |
|----------|-----------|--------------|-----------------|
| iOS, iPadOS | Yes; base and elevated backgrounds | Yes | Two background sets, grouped vs. system |
| macOS | Yes; desktop tinting | Yes | User accent color can override the app accent |
| tvOS | Yes | Yes: navigation elements, Top Shelf, Control Center; image views and buttons adopt it on focus | Limited palette that matches the logo; never show focus by color alone (scale and motion are primary) |
| visionOS | No setting; glass adapts to luminance behind it | The Materials page describes only the visionOS glass window material, a different material | Use color sparingly on glass; put color in bold text and large areas; prefer translucency to opaque fills; in full immersion keep brightness balanced and avoid bright objects on black |
| watchOS | No | Not covered on the Materials page (its watchOS section is about modal-sheet materials) | Background color only when it communicates; no full-screen color on long-lived screens (workout, audio) |

- [HIG] Do not confuse visionOS "glass" with Liquid Glass: it is an always-present window material that limits
  background color range and brightens or darkens with the surroundings, and the clear/regular variant and tinting
  rules above are not described for it.

Source: https://developer.apple.com/design/human-interface-guidelines/materials
Source: https://developer.apple.com/design/human-interface-guidelines/color
Source: https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Common mistakes

- Hard-coded hex values for text and backgrounds -> semantic system colors or Color Set assets with variants.
- Using `separator` or a label color as a fill, or a gray fill as text -> use each semantic color for its purpose.
- In-app light/dark switch -> follow the system appearance.
- Custom dark backgrounds that flatten sheets and popovers -> system background colors (base and elevated).
- Assuming Dark Mode exists on watchOS or visionOS -> it does not; design the single appearance.
- Glass cards, glass list rows or glass content panels -> standard materials in the content layer; glass only for
  controls and navigation.
- Clear glass over text or plain UI -> regular variant; clear only over rich media, with 35% dimming if bright.
- Tinting toolbar symbols, or tinting every glass button -> one prominent background-tinted primary action.
- Opaque bar background added to "fix" legibility -> remove it; use the scroll edge effect.
- Picking a material because it "looks darker" -> pick by purpose; add vibrant colors on top.
- Status shown only by red or green -> add a symbol or text.
- Checking contrast in light mode only -> check light, dark and Increase Contrast.
