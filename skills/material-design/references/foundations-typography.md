# Typography foundations

Scope: the Material 3 type scale (baseline and emphasized) with published sizes, line heights, tracking and weights, when to use each role, fonts and fallback, units and text scaling, readability and language-height rules; code for typography is in `references/implementation-theming.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- Structure of the type scale
- Type scale values
- Which role for what
- Emphasized styles
- Fonts and fallback
- Units
- Text scaling
- Minimum sizes and line length
- Line height, numerals and alignment
- Text color and links
- Language height
- Customizing the scale
- Editorial treatments and variable axes
- Form-factor notes
- Common mistakes

## Structure of the type scale

- [API] One type scale with five roles (display, headline, title, body, label), each in three sizes (large, medium, small): 15 styles. Since the May 2025 Expressive update each style also has an emphasized counterpart, so the scale holds 30 styles: 15 baseline and 15 emphasized.
- [API] Each of the 30 styles has one token carrying all its properties, for example `md.sys.typescale.display-large` and `md.sys.typescale.emphasized.display-large`; font, size, line height, tracking and weight also have individual tokens.
- [MD] No product needs all the styles; choose the subset that fits. Baseline and emphasized styles are meant to be used together.
- [API] Material lists the type scale as available for Jetpack Compose and for Android Views (MDC-Android), including the Expressive emphasized styles on both.

Source: https://m3.material.io/styles/typography/overview , https://m3.material.io/styles/typography/type-scale-tokens

## Type scale values

Values exactly as published in the type scale token table (default typeface Roboto, small language height). The table prints the unit as "pt"; the unit on Android is sp (see Units). The emphasized styles keep the size, line height and tracking of their baseline style and change only the weight.

| Style | Size | Line height | Tracking | Weight, baseline | Weight, emphasized |
|-------|------|-------------|----------|------------------|--------------------|
| Display large | 57 | 64 | -0.25 | 400 | 500 |
| Display medium | 45 | 52 | 0 | 400 | 500 |
| Display small | 36 | 44 | 0 | 400 | 500 |
| Headline large | 32 | 40 | 0 | 400 | 500 |
| Headline medium | 28 | 36 | 0 | 400 | 500 |
| Headline small | 24 | 32 | 0 | 400 | 500 |
| Title large | 22 | 28 | 0 | 400 | 500 |
| Title medium | 16 | 24 | 0.15 | 500 | 700 |
| Title small | 14 | 20 | 0.1 | 500 | 700 |
| Body large | 16 | 24 | 0.5 | 400 | 500 |
| Body medium | 14 | 20 | 0.25 | 400 | 500 |
| Body small | 12 | 16 | 0.4 | 400 | 500 |
| Label large | 14 | 20 | 0.1 | 500 | 700 |
| Label medium | 12 | 16 | 0.5 | 500 | 700 |
| Label small | 11 | 16 | 0.5 | 500 | 700 |

- [API] For the five emphasized styles listed at weight 700 (title medium and small, all labels), the same token table gives the variable-font `wght` axis value as 600, not 700. The static weight and the variable axis value disagree on the page; both are reported here.
- [API] The scale follows a Major Second ratio (1.125) anchored on 14 as the base size.
- [API] The smallest style in the scale is label small at 11; the smallest body style is body small at 12.

Source: https://m3.material.io/styles/typography/type-scale-tokens

## Which role for what

| Role | Use | Font guidance |
|------|-----|---------------|
| Display | the largest text on screen; short, important text or numerals; works best on large screens | an expressive face (handwritten, script) may be considered; set optical size if the font has it |
| Headline | short, high-emphasis text on smaller screens; primary passages and important regions | expressive faces allowed if line height and letter spacing keep it readable |
| Title | medium-emphasis text that stays relatively short; dividing secondary passages or regions (an app bar title, a category header) | be cautious with expressive, display, handwritten or script faces |
| Body | longer passages | use a face designed for body text; avoid expressive or decorative fonts |
| Label | utilitarian text inside components and very small text such as captions; navigation bar destination text, timecodes | must read quickly at small sizes |

- [API] Buttons use label large.
- [Conv] Material components already map their text to the right style. Pick a role yourself only for custom content, and pick by purpose and hierarchy, not by the number in the table.

Source: https://m3.material.io/styles/typography/applying-type

## Emphasized styles

(Material 3 Expressive.)

- [API] Material components do not use emphasized styles by default. To emphasize, swap the baseline token for the emphasized token of the same style.
- [MD] Recommended for selection, actions, headlines and editorial treatments. Components named as good fits: badges, buttons for primary actions, the extended FAB, selected list items, selected menu items.
- [MD] Two ways in: by weight (apply to text that already uses medium or bold to carry hierarchy) and by context (selected states, unread messages, key interactions). Both can be used at once.
- [MD] When customizing, keep emphasized styles visually consistent with one another (for example all wider than baseline). A different typeface may be used for emphasized styles.

Source: https://m3.material.io/styles/typography/type-scale-tokens

## Fonts and fallback

- [API] Roboto is the default typeface on Android and in the type scale. The scale has two typeface slots: brand (larger styles such as display and headline) and plain (smaller styles such as body and label). Roboto is the default for both.
- [API] Static fonts such as Roboto are currently applied by default to all Material 3 components. Variable fonts such as Roboto Flex are not yet part of the type scale.
- [API] Roboto Flex is a variable font with slant, width, weight, grade and optical size axes plus advanced parametric axes; Roboto Serif and Roboto Mono are also offered. Roboto Mono suits code and aligned numbers.
- [API] Noto Sans is the fallback collection for scripts Roboto does not cover (more than 150 scripts).
- [MD] With a variable brand font, set fallback in this order: Roboto Flex, then Roboto, then the Noto Sans collection, and confirm with engineering that fallback is in place.
- [MD] Replacing Roboto with a brand typeface is encouraged for expression; set the brand and plain typeface tokens instead of restyling individual texts.

Source: https://m3.material.io/styles/typography/fonts , https://m3.material.io/styles/typography/type-scale-tokens

## Units

| | Android | Web |
|--|---------|-----|
| Font size unit | sp | rem |
| Conversion ratio | 1.0 | 0.0625 (sp / 16 = rem) |
| Letter spacing unit | em | rem |
| Letter spacing conversion | tracking / font size in sp | tracking / font size |

- [API] Example given: a tracking of 0.2 on a 16sp font is 0.0125 em.
- [MD] Android guidance: specify font size in sp so people can adjust it, and do not use sp for padding or for heights that assume implicit padding.

Source: https://m3.material.io/styles/typography/type-scale-tokens , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://developer.android.com/about/versions/14/features

## Text scaling

- [MD] UIs should support a text increase of at least 200%.
- [Req] Stated as a must: content, understandability and functionality are not lost when people change their type settings (Material notes possible exceptions for non-Latin scripts).
- [API] How Material components scale: text size and line height multiply by the scale value; padding stays at 1x; spacing between elements in a component stays at 1x. Components without text (progress indicators, checkboxes, radio buttons) are not resized.
- [API] Android 14 and later supports font scaling up to 200% with a non-linear curve: large text grows less than small text so hierarchy is preserved. Test at the maximum font size setting.
- [MD] Fixes for overflow, in the order Material lists them: let containers grow; reflow (stack side-by-side buttons); scroll, preferably vertically and in one direction only; for app bars, navigation bars, navigation rails and fixed tabs, keep the text at 1x and show the enlarged label in a touch-and-hold tooltip.
- [MD] Wrap text when it is critical or when space allows; if it still does not fit, give a way to see the rest. Do not cut text off with no way to read it. An ellipsis is acceptable only when the full text is reachable through a tooltip or link.
- [MD] Use flexible containers; avoid text size limits that do not fit the component's space.
- [MD] When text size is controlled in the app instead of by the OS, offer multipliers such as 1.5x or 2x.

Source: https://m3.material.io/foundations/writing/text-resizing , https://m3.material.io/foundations/writing/text-truncation , https://developer.android.com/about/versions/14/features

## Minimum sizes and line length

- [API] The Material typography pages state no minimum font size for phones or tablets. The only floor they imply is the scale itself (label small 11, body small 12).
- [MD] Android's design guidance for accessibility says not to make body text smaller than 12sp, and notes that this matches the Material type scale default.
- [MD] XR: Material gives a minimum body size of 14dp. Wear OS quality guidance gives 12sp for essential and 10sp for non-essential text; see `references/platforms-wear.md` and `references/platforms-auto-xr.md`.
- [MD] Line length: the typography pages give none. The layout pages do: across all breakpoints, adjust margins and type styles to keep text between 40 and 60 characters per line. See `references/foundations-layout.md`.
- [MD] Be careful with very light weights for body text (thin strokes render poorly on lower-resolution displays; use light weights at display sizes) and with excessive weight at small sizes.

Source: https://m3.material.io/styles/typography/type-scale-tokens , https://developer.android.com/design/ui/mobile/guides/foundations/accessibility , https://m3.material.io/foundations/xr/design/accessibility , https://m3.material.io/foundations/layout/breakpoints/overview , https://m3.material.io/styles/typography/editorial-treatments

## Line height, numerals and alignment

- [MD] Recommended line-height ratios: about 1.2 times the type size for title, headline and display; about 1.5 times for body and label. The default tokens are already tuned for their size.
- [MD] Use tabular (monospaced) figures in tables and wherever values change often, such as clocks, to prevent layout shift.
- [API] Vertical measurement: Android specs measure distances to the text baseline (line height is baseline to baseline); web and iOS specs use the bounding box with equal half-leading above and below.
- [MD] Text beside a Material Symbol: same size and optical weight for both, with the symbol's baseline shifted down by about 11.5% of the text size. See `references/foundations-icons-writing.md`.

Source: https://m3.material.io/styles/typography/applying-type , https://m3.material.io/styles/icons/applying-icons

## Text color and links

- [MD] Contrast targets: 4.5:1 for small text and 3:1 for large text.
- [MD] Default text color is on surface; on surface variant is the alternative for lower emphasis.
- [MD] Links on a surface use primary, or tertiary to be less prominent.
- [Req] Stated as a must: hyperlinked text is also underlined.
- [MD] Do not underline a text button; links belong in hyperlinked body text. See `references/components-controls.md`.

Source: https://m3.material.io/styles/typography/applying-type

## Language height

(Added Aug 2026.) The type scale can adapt line height to the script.

| Category | Relative height | Scripts and languages listed |
|----------|-----------------|------------------------------|
| Small (base) | base | Cyrillic, Greek, Hebrew, Latin-based languages except Vietnamese |
| Medium | about 7% taller | Amharic, Arabic, Armenian, Bangla, Chinese, Gujarati, Hindi, Japanese, Kannada, Khmer, Korean, Lao, Malayalam, Odia, Punjabi, Sinhala, Tamil, Thai, Vietnamese, most others |
| Large | about 30% taller | Burmese, Telugu |
| Extra large | about 100% taller | Nastaliq |

- [MD] Default to medium language height and switch by detected language.
- [API] A Material component sized by vertical padding grows with the language height on its own; one with a fixed height is designed around the small category and may need adjusting for taller scripts.
- [MD] Do not hard-code container heights around Latin line heights: taller scripts then collide or break the layout, which fails both internationalization and readability.
- [API] Text in other languages averages about 1.5 times the length of English, so leave room horizontally as well.

Source: https://m3.material.io/styles/typography/type-scale-tokens , https://m3.material.io/styles/typography/overview , https://m3.material.io/foundations/content-design/global-writing/word-choice

## Customizing the scale

- [MD] To change the look of existing styles: change the brand and plain typeface tokens, then adjust line height and letter spacing. Avoid changing the type size, because it changes how components render and reflow. Repeat for baseline and emphasized.
- [MD] Heavier fonts may need wider letter spacing; fonts with long ascenders and descenders need different line heights.
- [MD] The scale itself may be customized when different sizes are needed (for example for other devices): add or remove styles, or change a size to another value on the Major Second scale. Keep enough contrast between adjacent sizes.
- [API] Customizing the scale or individual styles may stop the product from receiving Material's typography token updates.
- [Conv] The two statements pull in different directions: sizes may be customized at the scale level, but Material discourages changing the size of a style that components depend on. Change a size only with a stated reason, and re-test every component that uses the style.

Source: https://m3.material.io/styles/typography/type-scale-tokens

## Editorial treatments and variable axes

(Material 3 Expressive.)

- [MD] Editorial treatments are standalone, type-led showcase moments with custom sizes: celebrating content, expressing the user's voice, or marking bespoke functionality. They should not be used in labels or merely to convey information.
- [MD] Keep similar editorial moments consistent (tokenize them), match the tone to the task, do not mix clashing styles in one layout, and do not imitate personalization theming.
- [MD] Variable axes: weight, grade (changes apparent weight without reflowing text), width, optical size. Avoid wide widths in tight places such as a top app bar; match optical size to the rendered size and never use a large optical size at small sizes.

Source: https://m3.material.io/styles/typography/editorial-treatments

## Form-factor notes

| Form factor | Note | More |
|-------------|------|------|
| Large screens | display styles work best here; watch line length at large and extra-large breakpoints | `references/platforms-large-screens.md` |
| Watch | Expressive adds numeral and arc text styles for watches; test all font sizes and bold text | `references/platforms-wear.md` |
| XR | minimum 14dp body text; legibility depends on distance and lighting | `references/platforms-auto-xr.md` |

Source: https://m3.material.io/foundations/watches/styles , https://m3.material.io/foundations/watches/layout , https://m3.material.io/foundations/xr/design/accessibility , https://m3.material.io/foundations/layout/breakpoints/large-extra-large

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Font sizes in dp or px | sp for text, so the user's font size applies |
| Hard-coded size and weight on each text | Use a type scale style from the theme |
| Saying the scale has 15 styles | 30: 15 baseline plus 15 emphasized |
| Emphasized style everywhere | Components use baseline by default; emphasize selection, primary actions, unread or key moments |
| Changing a style's size to fit a design | Change typeface, line height and tracking first; sizes affect component layout |
| Fixed-height containers around text | Let containers grow; test at 200% and with taller scripts |
| Scaling padding with the font scale | Padding and spacing stay at 1x |
| Truncating with an ellipsis and no way to read the rest | Wrap, grow, or expose the full text |
| Decorative font for body text | Body uses a face designed for long reading |
| Display styles for long text or on small screens | Display is for short text; use headline on smaller screens |
| Proportional digits in a clock or table | Tabular figures |
| Link shown by color only | Underline it and use primary or tertiary |
| Quoting a Material minimum font size for phones | The Material pages give none; Android's design guidance says body no smaller than 12sp |
