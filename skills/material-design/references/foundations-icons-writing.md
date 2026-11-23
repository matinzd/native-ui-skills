# Icons and writing foundations

Scope: Material Symbols (styles, axes, sizes, state, targets, localization) and Material content design (capitalization, labels, punctuation, pronouns, tone, errors, alt text, notifications, writing for translation); icon and string APIs are in `references/implementation-theming.md`, TalkBack labelling in `references/accessibility-guidelines.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- Material Symbols: styles
- The four axes
- Sizes and optical size
- Filled versus outlined for state
- Icon touch targets and labels
- Icons with text
- Drawing custom icons
- Localizing and mirroring icons
- Capitalization
- Button, label and navigation wording
- Punctuation and formatting
- Pronouns and tone
- Error messages
- Alt text and content descriptions
- Notifications
- Writing for translation
- Common mistakes

## Material Symbols: styles

- [API] Material Symbols are the default icon set: a variable icon font in three styles, outlined, rounded and sharp. The older Material Icons remain available but lack the variable-font axes.
- [MD] Outlined: a light, clean style that works in dense UIs. Rounded: pairs with heavier type, curved logos and circular elements. Sharp: straight corners, legible at small sizes, for brands that rounded shapes do not reflect.
- [MD] Keep one visual style across an icon set; do not mix styles.
- [MD] Some symbols should stay filled for recognition even in an outlined set; the examples are full-body human icons and proprietary icons.
- [API] Symbols are obtained from fonts.google.com/icons, where they can be recolored and resized.

Source: https://m3.material.io/styles/icons/overview , https://m3.material.io/styles/icons/applying-icons , https://m3.material.io/styles/icons/designing-icons

## The four axes

| Axis | Range | Use |
|------|-------|-----|
| Weight | 100 (thin) to 700 (bold); 400 is regular, a 2dp stroke | match or contrast the weight of the typography |
| Fill | 0 (unfilled) to 1 (filled) | convey a state change, such as unselected to selected |
| Grade | finer than weight; default 0 for a dark icon on a light background, -25 for a light icon on a dark background | compensate for visual bleed; match the text font's grade; a positive grade adds emphasis for an active state |
| Optical size | 20dp to 48dp | keep stroke weight correct as the symbol is scaled |

- [MD] Do not use the lightest weight on standard 24dp icons; the minimum weight at that size should be 200. Be careful with excessive weight at 24dp too.
- [MD] Apply weight consistently; do not mix weights.
- [API] Weight can change the overall size of a symbol; grade has a smaller effect on size.

Source: https://m3.material.io/styles/icons/applying-icons

## Sizes and optical size

| Size | Intended use |
|------|--------------|
| 20dp | desktop, dense layouts, small-scale visuals |
| 24dp | the standard size |
| 40dp, 48dp | alongside display or headline type, on larger screens, and to highlight primary actions |

- [MD] Set the optical size to the rendered size so strokes do not become too heavy when a symbol is scaled up from 24dp.
- [MD] Simple symbols (a rating star) can be used alone at any size while they stay identifiable. Below 20dp, complex icons and icons for key actions should have a text label.

Source: https://m3.material.io/styles/icons/designing-icons , https://m3.material.io/styles/icons/applying-icons

## Filled versus outlined for state

- [MD] Use the fill axis for state: unfilled for unselected, filled for selected, as in a navigation bar.
- [MD] Navigation components: filled icon for the active destination, outlined for inactive; where a symbol has no filled version, increase its weight instead. Detail: `references/components-navigation.md`.
- [MD] A positive grade can mark an active icon without changing its size.
- [Conv] Fill alone is a visual cue. Selected state also needs to reach assistive technology; see `references/accessibility-guidelines.md`.

Source: https://m3.material.io/styles/icons/applying-icons , https://m3.material.io/components/navigation-bar/guidelines

## Icon touch targets and labels

- [MD] A 24dp symbol should have a 48dp target by default.
- [MD] When mouse and keyboard are the primary inputs, a 20dp symbol may use a 40dp target for denser layouts.
- [API] The state layer on an icon is 40dp while the interactive target is 48dp.
- [Req] Material words this as a must: navigation items have labels, for clarity and accessibility.
- [MD] Be cautious about icons shown without labels; meaning must be unambiguous. Labels may be omitted only where reduced visual impact is necessary. Add label text when a symbol is abstract.
- [MD] Every icon-only control needs an accessibility label that states its purpose, not its appearance. See Alt text and content descriptions below.

Source: https://m3.material.io/styles/icons/applying-icons , https://m3.material.io/foundations/interaction/states/state-layers

## Icons with text

- [MD] Use the same size for the symbol and the text next to it, and the same optical weight.
- [MD] Shift the symbol's baseline down by approximately 11.5% of the text size; do not share the text baseline.
- [MD] Match grade between text and symbols when the text font has a grade axis.

Source: https://m3.material.io/styles/icons/applying-icons

## Drawing custom icons

- [MD] Draw on a 24x24dp grid; keep content in the 20x20dp live area with 2dp padding. Content may extend into the padding for visual weight but never beyond the trim area.
- [API] Keyline shapes: square 18dp; circle 20dp diameter; vertical rectangle 20dp high by 16dp wide; horizontal rectangle 16dp high by 20dp wide.
- [MD] Stroke 2dp (regular weight 400) with squared terminals; corner radius 2dp by default, with square interior corners in the outlined style and 0dp corners in the sharp style. Complex shapes may drop to a 1.5dp stroke.
- [MD] Keep icons simple, bold and front-facing: not overly literal, not delicate, not tilted, rotated or dimensional. Place them on-pixel.

Source: https://m3.material.io/styles/icons/designing-icons

## Localizing and mirroring icons

- [MD] Test iconography across age groups, cultures and languages. Adapt symbols to the market (cart, bag or basket for checkout). Colors and symbols carry different meanings across cultures; red is not a warning color everywhere.
- [MD] In right-to-left layouts mirror directional icons such as back, forward and send. Do not mirror clocks, circular refresh, clockwise progress arrows or media controls. Full rules: `references/foundations-layout.md`.

Source: https://m3.material.io/styles/icons/applying-icons , https://m3.material.io/foundations/layout/bidirectionality-rtl

## Capitalization

The style guide is for English-language UX writing and generally follows AP style.

- [MD] Use sentence case for all product text: titles, headings, labels, menu items, navigation components, app bars and buttons. Only the first word and proper nouns (product and brand names included) are capitalized.
- [MD] Do not use title case.
- [MD] Do not use all caps ("caps blocks"); Material calls them not accessible.

Source: https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices , https://m3.material.io/foundations/content-design/style-guide/grammar-and-punctuation

## Button, label and navigation wording

The content design section has no chapter on button wording; these rules come from the component pages.

- [MD] Button label: describes the action that happens on tap; very brief, ideally 1-3 words; sentence case; always fully visible on one line, never truncated or wrapped.
- [MD] Dialog confirmation: name what happens next (Send, Create); avoid vague words such as Done, OK or Close.
- [MD] Omit the ellipsis on buttons and menu items that open a dialog or start a process.
- [MD] An ampersand may replace "and" in headlines, column and table headers, navigation labels and buttons; spell out "and" in sentences when there is room.
- [MD] Navigation bar labels: every item has a label of 1-2 words; the navigation rail page says one word. Do not truncate, wrap or shrink them. Detail: `references/components-navigation.md`.
- [MD] Text field label: always visible, short, one line, never truncated. Detail: `references/components-controls.md`.
- [MD] Use specific titles and headings that describe the topic; people scan.

Source: https://m3.material.io/components/buttons/guidelines , https://m3.material.io/components/dialogs/guidelines , https://m3.material.io/foundations/content-design/style-guide/grammar-and-punctuation , https://m3.material.io/components/text-fields/guidelines , https://m3.material.io/components/navigation-bar/guidelines , https://m3.material.io/components/navigation-rail/guidelines

## Punctuation and formatting

- [MD] No period on a single sentence in labels, tooltip text, bulleted lists, dialog body text or hyperlinked text. Use periods for multiple sentences, and for long or complex ones where it suits.
- [MD] Use contractions; "do not" may be kept for emphasis where caution is needed.
- [MD] Use the serial comma, except before an ampersand. Commas go inside quotation marks.
- [MD] Numbers: commas from 1,000 up to 1 million, but not in addresses, radio frequencies or years. "M" may abbreviate million when conveying volume.
- [MD] No colon after a heading that introduces a list; use a colon for lists inside body text.
- [MD] Exclamation points sparingly: greetings and real accomplishments, not empty states or routine tasks.
- [MD] Ellipses only for an action in progress or incomplete text; no space before one.
- [MD] Parentheses to define terms or acronyms, not for side notes.
- [MD] Avoid em dashes. Use an en dash without spaces for ranges. Never put spaces around hyphens.
- [MD] Emphasize with bold weight; italics only for a single word or phrase such as a title.
- [MD] Spell words out; use abbreviations sparingly; avoid "e.g." and "etc." in favor of "for example" and "and more".

Source: https://m3.material.io/foundations/content-design/style-guide/grammar-and-punctuation , https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices

## Pronouns and tone

- [MD] Address the user as "you" and "your".
- [MD] Do not mix first and second person ("my" with "your") on one screen; pick "you" or drop the pronoun.
- [MD] Be cautious with "I", "we" and "our" speaking for the company. Exception: legal acknowledgments such as "I agree to the terms of service".
- [MD] Explain consequences in neutral, direct language: say what will happen if the person acts and how to undo it. Avoid warnings that sound alarming, intimidating or condescending.
- [MD] Do not misrepresent consequences or steer the person's decision.
- [MD] Plain, everyday language over jargon; avoid idioms and colloquialisms.

Source: https://m3.material.io/foundations/content-design/style-guide/word-choice , https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices , https://m3.material.io/foundations/content-design/global-writing/word-choice

## Error messages

The content design section has no dedicated error-message page; these statements are spread across it and the component pages.

- [MD] Avoid polite filler such as "Please", "Sorry" and "Thank you", especially in error messages. "Please" is acceptable when asking for something inconvenient.
- [MD] An error message explains briefly and clearly what caused the error and how to fix it.
- [MD] Text field: replace the supporting text with the error text; do not add a second line that shifts the layout. If several errors are possible, describe how to avoid the most likely one.
- [MD] Showing an error icon on a text field in the error state is strongly recommended as a second visual indicator, so the error is not carried by color alone.
- [MD] In forms and full-screen dialogs, show field errors inline where they occur, and show all errors at once so everything can be fixed before retrying.
- [MD] Do not use emoji to accentuate bad news.

Source: https://m3.material.io/foundations/content-design/global-writing/word-choice , https://m3.material.io/components/text-fields/guidelines , https://m3.material.io/components/dialogs/guidelines , https://m3.material.io/foundations/content-design/notifications

## Alt text and content descriptions

- [MD] Write alt text for images that carry information. Test: if removing the image loses no information, it is decorative and needs neither alt text nor a caption; mark it so screen readers skip it.
- [MD] Describe the meaning in context, not every detail. The same image can need different alt text in different places.
- [MD] Do not start with "image of" or "picture of"; the screen reader already announces an image. Do not leave a file name as alt text.
- [MD] Length: the alt text page recommends 140 characters and says not to exceed it; the accessibility writing page describes alt text as a short label of up to 125 characters. The two Material pages disagree. [Conv] Aim for 125 or fewer; treat 140 as the ceiling.
- [MD] Do not repeat the caption; keep word choices consistent with nearby text (not "antique" in one and "vintage" in the other).
- [MD] Text embedded in an image is not read; put essential embedded text in the alt text.
- [MD] Name the image type only when it helps: chart, infographic, map, graph, screenshot, headshot, diagram.
- [MD] Charts: summarize the purpose and key takeaway instead of listing data points. Formula: summary of the data type plus the reason for showing the chart. Link to the data if available. For analysis charts with many takeaways, describe the structure and point to the data instead of picking a conclusion; consider an interactive chart.
- [MD] Motion: an informative animation or GIF gets alt text that summarizes the action (think of a title for it). Long-form video uses video description, not alt text.
- [MD] Labels for controls: describe purpose ("Search"), not appearance ("magnifying glass"); do not include the control type ("button", "menu"), which the role adds. See `references/accessibility-guidelines.md`.

Source: https://m3.material.io/foundations/content-design/alt-text , https://m3.material.io/foundations/writing/best-practices , https://m3.material.io/foundations/designing/elements

## Notifications

- [MD] Make notifications about the user: precise, timely, actionable and relevant; easy to opt out of in context; never unsolicited ads; not triggered during onboarding.
- [MD] Lead with the most important information; state the next action clearly.
- [MD] Suggested character counts: title under 29, collapsed body under 40, expanded body under 80 (start with the collapsed text and add to it), 1-2 buttons of 1-2 words each.
- [MD] Do not repeat the app name; the system already shows it.
- [MD] Avoid dynamic text in the title (it cannot expand and breaks limits when translated); put it in the body.
- [MD] Name the day of the week instead of "today" or "tomorrow"; Material cites about 20% of people not seeing a notification on the day it is sent. Exception: notifications that auto-dismiss at a set time.
- [MD] Emoji sparingly, never replacing words. No jokes.
- [Conv] System behaviour, channels and permission are in `references/platforms-system.md`.

Source: https://m3.material.io/foundations/content-design/notifications

## Writing for translation

- [MD] Short, simple sentences. Other languages average about 1.5 times the length of English.
- [MD] Use global examples; explain local references (places, names, currencies, temperatures, date formats, providers) in the message description for translators.
- [MD] Avoid abbreviations (common time abbreviations are fine). Repeat the noun instead of an ambiguous "it"; do not start a sentence with "this" or "that" unless the noun follows.
- [MD] Do not use both meanings of an ambiguous word ("filter", "change", "home") in one string; give translators context.

Source: https://m3.material.io/foundations/content-design/global-writing/overview , https://m3.material.io/foundations/content-design/global-writing/word-choice

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Title Case or ALL CAPS button labels | Sentence case for all product text |
| "OK" or "Done" on a confirming action | A specific verb for what happens next |
| Ellipsis on a button or menu item that opens a dialog | Omit it |
| Period after a single-sentence label or dialog body | Omit it |
| "Sorry, please try again" errors | Say what went wrong and how to fix it, without filler |
| Error text added under supporting text | Replace the supporting text; add an error icon |
| Mixed outlined, rounded and sharp icons, or mixed weights | One style and one weight |
| 24dp icon rendered at weight 100 | Weight 200 or more at 24dp |
| Scaling a 24dp icon up without changing optical size | Set optical size to the rendered size (20-48dp) |
| Icon-only navigation items | Navigation items have labels |
| 24dp icon with a 24dp target | 48dp target (40dp for a 20dp icon when pointer-first) |
| Alt text starting "Image of", or duplicating the caption | Describe the meaning; keep it short |
| Label that names the control type ("Submit button") | "Submit"; the role supplies the type |
| "Today" or the app name in a notification | Day of the week; no app name |
