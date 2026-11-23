# Color foundations

Scope: Material 3 color roles and how to pair them, static and dynamic schemes, dark theme, user contrast levels, contrast ratios, state layers, scrim, and what replaced surface tint; code for color schemes is in `references/implementation-theming.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- How the system is built
- Vocabulary in role names
- Accent roles: primary, secondary, tertiary
- Error roles
- Surface roles and surface containers
- Inverse roles
- Outline roles
- Add-on roles
- Pairing and layering rules
- Static versus dynamic schemes
- Dynamic color sources
- Custom, static and content-based colors
- Dark theme
- Contrast levels and contrast ratios
- State layers
- Scrim
- Surface tint and elevation overlays (deprecated)
- Common mistakes

## How the system is built

- [API] A color role is a semantic slot (primary, on primary, surface container, and so on) that components read through tokens. Material describes 26 standard roles in six groups (primary, secondary, tertiary, error, surface, outline) plus optional add-on roles; elsewhere the site writes "26+".
- [API] The same roles are used in light and dark theme and at every contrast level; only the values behind them change.
- [API] Generation pipeline: one source color -> five key colors (primary, secondary, tertiary, neutral, neutral variant) -> a tonal palette per key color -> tones assigned to roles for light and dark. Accent roles come from their own palette; surface roles come from the neutral palette.
- [API] Tones run from 0 (black) to 100 (white); palettes carry tones in steps of 10 plus 95, 98 and 99. Example given for light theme: primary = primary40, on primary = primary100.
- [API] Colors are defined in HCT (hue 0-360, chroma from 0 up to roughly 120, tone 0-100). Tone determines contrast. HCT values do not map onto HSL or RGB; do not mix color spaces when inspecting or adjusting colors.
- [MD] Always apply color roles, never fixed hex values or raw tonal-palette values: fixed values break light and dark theme, contrast control and dynamic color.
- [API] Changes Material lists: tone-based surface containers replaced elevation-based surfaces (Feb 2023, when the default light surface also moved from tone 99 to 98); fixed accent roles added (Feb 2023); on-container roles made more colorful in light theme (Aug 2024); three contrast levels (May 2025).

Source: https://m3.material.io/styles/color/system/overview , https://m3.material.io/styles/color/system/how-the-system-works , https://m3.material.io/styles/color/roles , https://m3.material.io/styles/color/advanced/apply-colors

## Vocabulary in role names

| Word | Meaning |
|------|---------|
| Surface | backgrounds and large, low-emphasis areas |
| Primary, secondary, tertiary | accent roles that raise or lower the emphasis of foreground elements |
| Container | a fill color for foreground elements such as buttons; should not be used for text or icons |
| On | the color for text and icons placed on the paired parent color |
| Variant | a lower-emphasis alternative to the non-variant role |

Source: https://m3.material.io/styles/color/roles

## Accent roles: primary, secondary, tertiary

| Role | Use |
|------|-----|
| Primary | high-emphasis fills, text and icons against surface |
| On primary | text and icons on primary |
| Primary container | standout fill against surface for key components such as the FAB |
| On primary container | text and icons on primary container |
| Secondary | less prominent fills, text and icons against surface |
| On secondary | text and icons on secondary |
| Secondary container | less prominent fill for recessive components such as tonal buttons |
| On secondary container | text and icons on secondary container |
| Tertiary | complementary fills, text and icons against surface |
| On tertiary | text and icons on tertiary |
| Tertiary container | complementary container color, for components such as input fields |
| On tertiary container | text and icons on tertiary container |

- [MD] Primary: the most prominent components across the UI, such as the FAB, high-emphasis buttons and active states.
- [MD] Secondary: less prominent components, such as filter chips; also elements that need no immediate attention, such as a selected navigation icon's state or a dismissive button.
- [MD] Tertiary: contrasting accents that balance primary and secondary or draw heightened attention to a small element, such as a badge. Applied at the designer's discretion.
- [MD] Assign accent roles by importance and needed emphasis; be cautious about changing roles only for visual effect.

Source: https://m3.material.io/styles/color/roles

## Error roles

- [MD] Error, on error, error container and on error container communicate error states, for example a wrong password in a text field.
- [API] Error roles are static by default: they do not change with a dynamic scheme, but they still adapt to light and dark theme.
- [MD] Do not define another semantic red; Material's error color already serves as the static semantic red.

Source: https://m3.material.io/styles/color/roles , https://m3.material.io/styles/color/advanced/define-new-colors

## Surface roles and surface containers

| Role | Use |
|------|-----|
| Surface | default background color |
| On surface | text and icons on any surface or surface container color |
| On surface variant | lower-emphasis text and icons on any surface or surface container color |
| Surface container lowest | lowest-emphasis container |
| Surface container low | low-emphasis container |
| Surface container | default container color |
| Surface container high | high-emphasis container |
| Surface container highest | highest-emphasis container |

- [MD] Use surface for neutral backgrounds and the container roles for components such as cards, sheets and dialogs. The most common combination is surface for the body area and surface container for the navigation area.
- [MD] Keep role mappings, surface roles above all, the same for a layout region across breakpoints (body = surface and navigation = surface container on both phone and tablet). Larger windows may add other container roles for hierarchy and nesting as long as they are applied consistently.
- [API] Neutral components such as navigation bars, menus and dialogs map by default to specific surface container roles (low, default, high, highest). The mapping may be changed.
- [API] Surface container roles are not tied to elevation.
- [MD] Give overlapping containment areas or components different color roles so separation is visible.
- [MD] Default text color is on surface; on surface variant is the lower-emphasis alternative. Links on a surface use primary (tertiary for less prominence).
- [Req] Stated as a must: hyperlinked text is also underlined.

Source: https://m3.material.io/styles/color/roles , https://m3.material.io/styles/elevation/applying-elevation , https://m3.material.io/styles/typography/applying-type

## Inverse roles

- [MD] Inverse surface, inverse on surface and inverse primary are applied selectively to make a component contrast with the surrounding UI. The snackbar is the example: inverse surface for the container, inverse on surface for the text, inverse primary for the text button.

Source: https://m3.material.io/styles/color/roles

## Outline roles

- [MD] Outline: important boundaries, such as a text field border. Outline variant: decorative elements, such as dividers.
- [MD] Do not use outline for dividers, or for components that contain several elements such as cards; use outline variant for those.
- [MD] Do not use outline variant to create visual hierarchy or to define the boundary of a target; use outline or another color with 3:1 contrast against the surface.
- [MD] Exception (stated as a caution): outline variant may border targets such as chips and buttons when the elements inside them provide the contrast; the example cites icons and text at 4.5:1.

Source: https://m3.material.io/styles/color/roles

## Add-on roles

Material says most products will not need these, and that a team unsure whether it needs them probably does not.

| Role | Behaviour |
|------|-----------|
| Primary, secondary, tertiary fixed | fill colors that keep the same tone in light and dark theme |
| Primary, secondary, tertiary fixed dim | a stronger tone with the same fixed behaviour |
| On fixed, on fixed variant (per accent) | text and icons on the fixed color; variant is lower emphasis |
| Surface dim | the dimmest surface in both themes |
| Surface bright | the brightest surface in both themes |

- [MD] Fixed colors do not change between themes, so they are likely to cause contrast problems; avoid them where contrast is necessary and use the regular accent roles there.
- [API] Surface inverts between themes (brightest area in light, dimmest in dark); surface bright and surface dim keep their relative brightness in both.

Source: https://m3.material.io/styles/color/roles

## Pairing and layering rules

- [MD] Apply colors only in the intended pairs and layering orders: X with on X, X container with on X container, on surface or on surface variant on any surface role.
- [API] The designed pairs provide an accessible minimum of 3:1; roles starting with "on" are guaranteed sufficient contrast with their partner. Other combinations may miss the 4.5:1 (small text) and 3:1 (large text) targets.
- [MD] Wrong pairs break when the user changes the contrast level. The documented failing example puts primary container on primary and on surface on secondary container.
- [MD] Do not use container roles for text or icons.
- [MD] When remapping a component or coloring a custom one, choose roles by function, and test a dynamic scheme across themes (light and dark, and several source hues).

Source: https://m3.material.io/styles/color/roles , https://m3.material.io/styles/color/advanced/apply-colors

## Static versus dynamic schemes

| | Static (baseline or custom brand) | Dynamic |
|--|-----------------------------------|---------|
| Colors change with wallpaper or content | no | yes |
| Accessible pairings, light and dark | yes | yes |
| User-controlled contrast | listed as not included | yes |
| Same colors on every device | yes | no |

- [MD] Choose static baseline when the product is not ready for dynamic color, is migrating from Material 2, serves enterprise users who would not benefit from personalization, or is built for iOS.
- [MD] Choose dynamic color to showcase personalization, to follow wallpaper or content, or to offer user-controlled contrast.
- [MD] Even for dynamic color, design first with the baseline scheme so the role mapping is right, then test the mocks across a range of source colors. Role mappings stay the same across dynamic schemes; only values change.
- [MD] A brand scheme is hand-picked and maintained by the team (primary first; secondary, tertiary, error, neutral and neutral variant inputs are optional) and costs more effort.
- [MD] Dynamic color is both a user setting and a developer choice. Ship a custom theme so the app has a fallback scheme for people who do not enable dynamic color; dynamic color can also be applied selectively, for example to a profile screen.
- [Unverified] The Material pages read for this file do not state which Android version provides wallpaper-based color. See `references/implementation-theming.md`.

Source: https://m3.material.io/styles/color/choosing-a-scheme , https://m3.material.io/styles/color/static/baseline , https://m3.material.io/styles/color/static/custom-brand , https://m3.material.io/foundations/customization

## Dynamic color sources

- [API] User-generated color comes from the Android user's wallpaper; content-based color comes from in-app content such as album art, a logo or a video preview. In both, the image is quantized to one source color.
- [MD] Pick user-generated color for a personalized experience; pick content-based color when content is front and center and the team can do some customization.
- [MD] Content-based color works best on contained elements next to the source image. Keep the source visible, and avoid content-based color where the content itself is not shown.
- [MD] Limit a screen to two color schemes from different source types (for example user-generated plus one kind of content).
- [MD] Do not let content-based color replace colors with semantic meaning, such as a red error or a green positive action.

Source: https://m3.material.io/styles/color/dynamic/choosing-a-source , https://m3.material.io/styles/color/dynamic/user-generated-source , https://m3.material.io/styles/color/dynamic/content-based-source , https://m3.material.io/styles/color/advanced/apply-colors

## Custom, static and content-based colors

- [MD] Static colors (formerly "custom colors") are extra colors that stay fixed inside a dynamic scheme, for brand or semantic meaning such as success. Define them through the Material system: one input returns four roles (color, on color, container, on container) that follow the accent conventions and support dark theme and contrast levels.
- [MD] Static colors in a dynamic scheme may be harmonized, which shifts their hue slightly toward the scheme's primary. Skip harmonization when the value is tied to a literal source such as a brand color or real-world signage.
- [MD] Define a custom color role only when existing roles and static colors cannot do the job. A custom role needs a palette and reference tone for light and dark, its pairings, and contrast that meets Material's minimums.
- [API] Color fidelity adjusts tones so scheme colors match the input color more closely; Material Theme Builder enables it by default for custom baseline schemes and static colors.

Source: https://m3.material.io/styles/color/advanced/define-new-colors , https://m3.material.io/styles/color/advanced/adjust-existing-colors

## Dark theme

- [API] Dark theme is built in: the algorithm assigns dark values to the same roles, so one set of roles yields both themes. The baseline scheme ships light and dark values.
- [API] Contrast levels apply automatically in both themes.
- [MD] Do not hand-build a second palette or switch on theme in component code; read roles. Fixed add-on roles are the only roles that deliberately ignore the theme.
- [MD] Text can look heavier when switching between dark and light with identical settings; a negative font grade can offset this. Material Symbols default to grade 0 for dark-on-light and -25 for light-on-dark.
- [Conv] Material has no separate dark theme page in the current foundations and styles sections; everything it says about dark theme is in the color system pages cited here. Do not import dark theme rules from other Material versions.

Source: https://m3.material.io/styles/color/system/how-the-system-works , https://m3.material.io/styles/color/static/baseline , https://m3.material.io/styles/typography/editorial-treatments , https://m3.material.io/styles/icons/applying-icons

## Contrast levels and contrast ratios

(User contrast levels were added in May 2025.)

| Level | What Material says it provides |
|-------|--------------------------------|
| Standard (default) | a mix of high- and low-contrast elements to express hierarchy |
| Medium | a minimum contrast ratio of 3:1, for people who need more contrast but are uncomfortable with very high contrast |
| High | 7:1 on essential elements; the example applies it to the content of a card and not the card container |

- [MD] Custom components support contrast levels by using the proper role pairs (the example is primary container with on primary container) through tokens.
- [MD] Text contrast targets: 4.5:1 for small text, 3:1 for large text. Large is 14pt bold or 18pt regular and up; the same 3:1 applies to graphics. Material attributes these figures to the W3C.
- [MD] Non-text: elements clustered with others, such as a group of buttons, should reach 3:1 between container and background. Standalone prominent elements such as a FAB are said not to need it.
- [MD] For interactive components, the edges between overlapping surfaces must have enough contrast to be seen as separate.
- [MD] Disabled states do not need to meet the contrast targets.
- [MD] In informative images, essential content follows the same 3:1 and 4.5:1 targets; decorative parts do not have to.

Source: https://m3.material.io/styles/color/system/how-the-system-works , https://m3.material.io/foundations/designing/color-contrast , https://m3.material.io/styles/elevation/applying-elevation , https://m3.material.io/foundations/writing/best-practices

## State layers

A state layer is a semi-transparent overlay between the container and its content. Its color is the content color (normally the "on" role), at a fixed opacity per state.

| State | Opacity | Notes |
|-------|---------|-------|
| Hover | 8% | low-emphasis animated fade; one hovered element at a time |
| Focus | 10% | plus a ring-like keyboard focus indicator; one focused element at a time |
| Pressed | 10% | shown as a ripple; high emphasis; one pressed element at a time |
| Dragged | 16% | low emphasis; components may also gain elevation |

- [API] The token list also contains a disabled state layer opacity of 0.38. Per-component disabled container and content opacities are in the component specs, not on this page.
- [MD] Only one state layer applies at a time, though states can combine visually (selected plus hover, selected plus focus).
- [API] The state layer is 40dp while the interactive target is 48dp.
- [MD] Example mapping: secondary container with on secondary container content takes an on secondary container state layer; a surface container with primary content takes a primary state layer.
- [MD] Disabled components cannot be focused, dragged or pressed and show no state layers. If a FAB's action is unavailable, remove the FAB instead of disabling it.
- [MD] Apply states to the actionable elements inside a bar, not to the whole app bar.

Source: https://m3.material.io/foundations/interaction/states/state-layers , https://m3.material.io/foundations/interaction/states/applying-states , https://m3.material.io/foundations/interaction/states/overview

## Scrim

- [MD] A scrim sits beneath elements such as modals and expanded navigation to focus attention. It uses the scrim color role at 32% opacity.
- [MD] On large screens the scrim behind a floating pane is optional; on desktop a side sheet for tools is shown without one.

Source: https://m3.material.io/styles/elevation/applying-elevation , https://m3.material.io/foundations/layout/scaffold/panes , https://m3.material.io/foundations/desktop/components

## Surface tint and elevation overlays (deprecated)

- [API] Material states that the surface tint color is deprecated and says to use elevation level tokens (0-5) instead. The token still appears in the elevation token list (baseline light value #6750A4).
- [API] Tone-based surface roles replaced the earlier approach of surfaces at +1 to +5 elevation in Feb 2023; the stated reason is flexibility and support for features such as user-controlled contrast.
- [MD] Replacement in practice: express separation with a surface container role chosen for emphasis, and express z-order with the elevation level. Do not compute a primary-tinted overlay from elevation. Levels and shadows: `references/foundations-shape-motion.md`.
- [Conv] The percentage overlay table from early Material 3 (primary at rising opacities per level) no longer appears on the current pages; treat any rule that derives a surface color from elevation as outdated.

Source: https://m3.material.io/styles/elevation/tokens , https://m3.material.io/styles/color/system/overview , https://m3.material.io/styles/elevation/applying-elevation

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Hard-coded hex or tonal-palette values in components | Read color roles from the theme |
| Text in a container role, or primary container on primary | Use the "on" role of the fill underneath |
| Outline on dividers or card borders | Outline variant |
| Outline variant as the only boundary of an empty target | Outline, or another 3:1 color |
| Tinting surfaces by elevation (surface tint overlay) | Surface container roles plus elevation levels |
| Separate hand-made dark palette | Same roles; let the scheme supply dark values |
| Dynamic color with no fallback | Ship a custom or baseline scheme as the fallback |
| Dynamic or content-based color replacing error red | Keep semantic colors static (harmonize if wanted) |
| Different surface roles for the same region on phone and tablet | Keep the mapping per region across breakpoints |
| Fixed accent roles under text that needs contrast | Regular accent roles |
| Disabling a FAB | Remove it while the action is unavailable |
| State layer opacity picked by eye, or a state layer in a color other than the content color | Hover 8%, focus 10%, pressed 10%, dragged 16% of the content color |
