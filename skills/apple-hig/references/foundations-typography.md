# Typography

Scope: system fonts, text styles, default and minimum sizes, Dynamic Type tables, weights, leading, tracking,
custom fonts and per-platform differences.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Default and minimum sizes
- System fonts
- Text styles, weights and leading
- Dynamic Type behaviour
- iOS and iPadOS size tables
- macOS, tvOS and watchOS style tables
- Custom fonts
- Tracking
- Platform notes
- Common mistakes

## Default and minimum sizes

Applies to system and custom fonts. The same table appears on the Accessibility page.

| Platform | Default size | Minimum size |
|----------|--------------|--------------|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- [HIG] Follow the default and minimum per platform. With a thin custom font, go larger than these values.
- [HIG] Ideally let people enlarge text by at least 200 percent (140 percent in watchOS), through Dynamic Type or
  custom UI.
- [HIG] Avoid light weights. With system fonts prefer Regular, Medium, Semibold or Bold; avoid Ultralight, Thin and
  Light, especially at small sizes.
- [HIG] Test legibility in each context (the page singles out game text per platform); fix with larger size, more
  contrast, or a font designed for legibility such as the system fonts.

Source: https://developer.apple.com/design/human-interface-guidelines/typography
Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## System fonts

- [HIG] San Francisco (SF) is the sans serif family: SF Pro, SF Compact, SF Arabic, SF Armenian, SF Georgian,
  SF Hebrew and SF Mono. Rounded variants exist for all of these except SF Mono.
- [HIG] New York (NY) is the serif family, designed to pair with SF.
- [HIG] Both are variable fonts with dynamic optical sizes on all platforms, so there is no need to pick discrete
  Text or Display optical sizes in code.
- [HIG] Weights range from Ultralight to Black; SF also has widths including Condensed and Expanded. SF Symbols use
  the same weights, so symbols match adjacent text.
- [HIG] Do not embed the system fonts in an app or game (stated as "don't" in a developer note); request them
  through the system font-design API. The page names `Font.Design.default` and `Font.Design.serif`.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Text styles, weights and leading

- [HIG] A text style is a combination of weight, point size and leading defined for each text size. Use the
  built-in styles to express hierarchy; with system fonts they bring Dynamic Type and larger accessibility sizes
  where the platform has them.
- [HIG] Build hierarchy with weight, size and color, and keep the relative hierarchy intact when text size changes.
- [HIG] Minimize the number of typefaces, even in a heavily customized UI.
- [HIG] Emphasized variants come from symbolic traits (bold); the emphasized weight can be Medium, Semibold, Bold
  or Heavy depending on the style (see tables).
- [HIG] Leading: use loose leading for wide columns and long passages; tight leading only where height is
  constrained (a list row). Never use tight leading for three or more lines.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Dynamic Type behaviour

Dynamic Type exists in iOS, iPadOS, tvOS, visionOS and watchOS. macOS does not support it.

- [HIG] Make the layout work at every size, including the Larger Accessibility Text Sizes; verify text and glyphs
  stay legible.
- [HIG] Scale meaningful interface icons with text. SF Symbols do this automatically.
- [HIG] Keep truncation minimal: show as much useful text at the largest accessibility size as at the largest
  standard size; do not truncate inside scrollable regions unless the full text opens elsewhere; let labels use as
  many lines as needed.
- [HIG] At large sizes switch to a stacked layout (text above secondary items such as glyphs and timestamps) and
  reduce the number of text columns.
- [HIG] Keep hierarchy stable: primary elements stay toward the top at every size.
- [HIG] Not everything has to grow. Prioritize the content people care about; the page's examples of text that need
  not scale are tab titles and transient hit-damage values in a game.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## iOS and iPadOS size tables

Point size / leading. Weight is Regular for every style except Headline (Semibold). Emphasized weight: Bold for
Large Title, Title 1 and Title 2; Semibold for all others.

| Style | xSmall | Small | Medium | Large (default) | xLarge | xxLarge | xxxLarge |
|-------|--------|-------|--------|-----------------|--------|---------|----------|
| Large Title | 31/38 | 32/39 | 33/40 | 34/41 | 36/43 | 38/46 | 40/48 |
| Title 1 | 25/31 | 26/32 | 27/33 | 28/34 | 30/37 | 32/39 | 34/41 |
| Title 2 | 19/24 | 20/25 | 21/26 | 22/28 | 24/30 | 26/32 | 28/34 |
| Title 3 | 17/22 | 18/23 | 19/24 | 20/25 | 22/28 | 24/30 | 26/32 |
| Headline | 14/19 | 15/20 | 16/21 | 17/22 | 19/24 | 21/26 | 23/29 |
| Body | 14/19 | 15/20 | 16/21 | 17/22 | 19/24 | 21/26 | 23/29 |
| Callout | 13/18 | 14/19 | 15/20 | 16/21 | 18/23 | 20/25 | 22/28 |
| Subhead | 12/16 | 13/18 | 14/19 | 15/20 | 17/22 | 19/24 | 21/28 |
| Footnote | 12/16 | 12/16 | 12/16 | 13/18 | 15/20 | 17/22 | 19/24 |
| Caption 1 | 11/13 | 11/13 | 11/13 | 12/16 | 14/19 | 16/21 | 18/23 |
| Caption 2 | 11/13 | 11/13 | 11/13 | 11/13 | 13/18 | 15/20 | 17/22 |

Larger accessibility sizes:

| Style | AX1 | AX2 | AX3 | AX4 | AX5 |
|-------|-----|-----|-----|-----|-----|
| Large Title | 44/52 | 48/57 | 52/61 | 56/66 | 60/70 |
| Title 1 | 38/46 | 43/51 | 48/57 | 53/62 | 58/68 |
| Title 2 | 34/41 | 39/47 | 44/52 | 50/59 | 56/66 |
| Title 3 | 31/38 | 37/44 | 43/51 | 49/58 | 55/65 |
| Headline | 28/34 | 33/40 | 40/48 | 47/56 | 53/62 |
| Body | 28/34 | 33/40 | 40/48 | 47/56 | 53/62 |
| Callout | 26/32 | 32/39 | 38/46 | 44/52 | 51/60 |
| Subhead | 25/31 | 30/37 | 36/43 | 42/50 | 49/58 |
| Footnote | 23/29 | 27/33 | 33/40 | 38/46 | 44/52 |
| Caption 1 | 22/28 | 26/32 | 32/39 | 37/44 | 43/51 |
| Caption 2 | 20/25 | 24/30 | 29/35 | 34/41 | 40/48 |

- [HIG] Body runs from 14 pt (xSmall) to 53 pt (AX5): design rows and containers for almost a fourfold range.
- [HIG] No style drops below 11 pt at any size, matching the platform minimum.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## macOS, tvOS and watchOS style tables

macOS built-in text styles (fixed; size / line height):

| Style | Size | Weight | Emphasized |
|-------|------|--------|------------|
| Large Title | 26/32 | Regular | Bold |
| Title 1 | 22/26 | Regular | Bold |
| Title 2 | 17/22 | Regular | Bold |
| Title 3 | 15/20 | Regular | Semibold |
| Headline | 13/16 | Bold | Heavy |
| Body | 13/16 | Regular | Semibold |
| Callout | 12/15 | Regular | Semibold |
| Subheadline | 11/14 | Regular | Semibold |
| Footnote | 10/13 | Regular | Semibold |
| Caption 1 | 10/13 | Regular | Medium |
| Caption 2 | 10/13 | Medium | Semibold |

tvOS built-in text styles (size / leading; weight Medium and emphasized Bold unless noted):

| Style | Size | Note |
|-------|------|------|
| Title 1 | 76/96 | |
| Title 2 | 57/66 | |
| Title 3 | 48/56 | |
| Headline | 38/46 | |
| Subtitle 1 | 38/46 | Regular, emphasized Medium |
| Callout | 31/38 | |
| Body | 29/36 | |
| Caption 1 | 25/32 | |
| Caption 2 | 23/30 | |

watchOS point sizes (leading is size + 2.5 pt in the page's standard-size tables). Weight Regular except Headline
(Semibold); emphasized Semibold except Large Title (Bold). Defaults: Small on 38mm; Large on 40mm, 41mm and 42mm;
xLarge on 44mm, 45mm and 49mm.

| Style | xSmall | Small | Large | xLarge | xxLarge | xxxLarge | AX1 | AX2 | AX3 |
|-------|--------|-------|-------|--------|---------|----------|-----|-----|-----|
| Large Title | 30 | 32 | 36 | 40 | 41 | 42 | 44 | 45 | 46 |
| Title 1 | 28 | 30 | 34 | 38 | 39 | 40 | 42 | 43 | 44 |
| Title 2 | 24 | 26 | 28 | 30 | 31 | 32 | 34 | 35 | 36 |
| Title 3 | 17 | 18 | 19 | 20 | 21 | 22 | 24 | 25 | 26 |
| Headline | 14 | 15 | 16 | 17 | 18 | 19 | 21 | 22 | 23 |
| Body | 14 | 15 | 16 | 17 | 18 | 19 | 21 | 22 | 23 |
| Caption 1 | 13 | 14 | 15 | 16 | 17 | 18 | 18 | 19 | 20 |
| Caption 2 | 12 | 13 | 14 | 15 | 16 | 17 | 17 | 18 | 19 |
| Footnote 1 | 11 | 12 | 13 | 14 | 15 | 16 | 16 | 17 | 18 |
| Footnote 2 | 10 | 11 | 12 | 13 | 14 | 15 | 15 | 16 | 17 |

- [HIG] Style names differ by platform: macOS says Subheadline where iOS says Subhead; tvOS has Subtitle 1 and
  no Large Title, Subhead or Footnote; watchOS has Footnote 1 and 2 and no Callout or Subhead; watchOS has no
  Medium size and stops at AX3.
- [HIG] Page inconsistencies to flag: the watchOS xSmall Footnote 1 and Footnote 2 (11 and 10 pt) are below the
  stated 12 pt watchOS minimum; the page says tvOS supports Dynamic Type but publishes a single tvOS table; the
  page publishes no visionOS size table.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Custom fonts

- [HIG] A custom font must be legible at the viewing distances and conditions of the platform; apply the minimum
  sizes above.
- [HIG] System fonts get Dynamic Type and Bold Text behaviour automatically. A custom font has to implement the
  same behaviours (the page says "make sure").
- [HIG] In a Unity-based game, use Apple's Unity plug-ins for Dynamic Type or provide another way to adjust text size.
- [HIG] Branding guidance: custom font for headlines and subheadings, system font for body and captions works well.

Source: https://developer.apple.com/design/human-interface-guidelines/typography
Source: https://developer.apple.com/design/human-interface-guidelines/branding

## Tracking

- [HIG] At runtime the system font adjusts tracking automatically at every point size. Do not set tracking in code
  to imitate the tables.
- [HIG] The page's tracking tables (SF Pro, SF Pro Rounded, New York, SF Compact, SF Compact Rounded; 6 pt upward)
  exist only for producing accurate mockups in design tools. Example values for SF Pro: 12 pt = 0, 17 pt = -26
  (-0.43 pt), 34 pt = +12 (+0.40 pt), in 1/1000 em. Look up other sizes on the page.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Platform notes

| Platform | System font | Dynamic Type | Notes |
|----------|-------------|--------------|-------|
| iOS, iPadOS | SF Pro; NY available | Yes, xSmall to xxxLarge plus AX1 to AX5 | Test with Larger Accessibility Text Sizes on. |
| macOS | SF Pro; NY only for Mac Catalyst apps | No | Use the fixed built-in styles; use AppKit dynamic system font variants (control content, label, menu, menu bar, message, palette, title, tool tips, user, user fixed pitch) to match standard controls. |
| tvOS | SF Pro; NY available | Yes (per the page) | Sizes are large for distance viewing; Medium is the base weight. |
| visionOS | SF Pro; with NY, specify type styles yourself | Yes | Bolder Body and Title styles; adds Extra Large Title 1 and Extra Large Title 2 for wide editorial layouts. |
| watchOS | SF Compact; SF Compact Rounded in complications; NY available | Yes, xSmall to xxxLarge plus AX1 to AX3 | Default size depends on case size. |

- [HIG] visionOS: prefer 2D text; text is white by default for contrast on glass, so test any other color; for text
  with no background prefer bold over shadows; billboard text attached to a point in space so it faces the viewer;
  test legibility when people scale the window.

Source: https://developer.apple.com/design/human-interface-guidelines/typography

## Common mistakes

- Fixed point sizes for UI text on iOS -> built-in text styles so Dynamic Type applies.
- Applying iOS sizes on macOS (17 pt body) or expecting Dynamic Type on macOS -> macOS body is 13 pt, fixed styles.
- Text below the platform minimum (for example 9 or 10 pt captions on iOS) -> 11 pt minimum on iOS and iPadOS.
- Ultralight, Thin or Light weights for small text -> Regular or heavier.
- Single-line labels that truncate at accessibility sizes -> unlimited lines and a stacked layout.
- Scaling every string equally, including tab titles -> prioritize content text.
- Fixed-size icons beside scaling text -> scale icons with text (SF Symbols do).
- Custom font without Dynamic Type or Bold Text support -> implement both, or use the system font.
- Bundling SF font files -> request the system font through the API.
- Hand-set tracking or tight leading on paragraphs -> let the system track; no tight leading for 3+ lines.
- Assuming style names and sizes are identical across platforms -> check the per-platform table.
