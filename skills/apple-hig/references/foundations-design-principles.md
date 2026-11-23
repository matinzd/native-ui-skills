# Design principles, branding and inclusion

Scope: the eight HIG design principles and how to use them to settle trade-offs, plus branding and inclusion rules.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- The eight principles
- Applying the principles to trade-offs
- Branding
- Inclusion
- Common mistakes

## The eight principles

The Design principles page was reintroduced on 2026-06-08. It replaces older lore: "Clarity, Deference, Depth" is not
in the current HIG and should not be quoted as Apple's principles. The page says there is no single right way to apply
the principles; they are tools for weighing competing priorities. Every item below is a recommendation.

| Principle | Tagline | What the page asks for |
|-----------|---------|------------------------|
| Purpose | Make something meaningful | Keep asking what the product is for; put effort into the most important features; study existing solutions and do not just re-create them. |
| Agency | Let people do things their own way | Get people straight to the task or content; do not lock them into flows or modes; make guided flows easy to skip or escape; make recovery from mistakes cheap. |
| Responsibility | Act in people's best interest | State intentions up front; give a clear rationale when asking permission; say what is collected and how it is used; collect only what the product needs; anticipate misuse. |
| Familiarity | Build on what people know | Reuse real-world and software concepts; once an element has a behaviour or appearance, keep it everywhere; show availability and change; use system patterns for alerts and choices. |
| Flexibility | Adapt to diverse contexts and needs | Treat accessibility as a priority from the start; keep content and controls in predictable positions across platforms and configurations; support many inputs (voice, touch, keyboard and more); give every supported platform equal care. |
| Simplicity | Be clear and direct | Include just what is necessary (the page says simplicity is not minimalism); use exactly the words needed; prefer recognizable controls and a consistent structure. |
| Craft | Care about every detail | Be deliberate about visuals, animation, wording and audio; prototype early and discard what fails; test in real settings; keep the UI current with platform capabilities after shipping. |
| Delight | Make it human | Decide which emotion fits the product; look for small defining moments (even a button press or an error message); do not confuse delight with decoration. |

- [HIG] Craft includes maintenance: keep the interface current with the latest platform capabilities and design
  patterns after shipping.
- [Conv] Use the eight names as the rationale vocabulary when explaining a decision, and read the Craft sub-rule
  above as the reason to adopt current-era components (OS 26+, Liquid Glass) instead of preserving a pre-26 look.

Source: https://developer.apple.com/design/human-interface-guidelines/design-principles

## Applying the principles to trade-offs

The page gives no priority order. The pairings below are this skill's reading of how the page's own sub-rules resolve
common conflicts; each bullet cites the sub-rule it leans on.

- [HIG] Onboarding or tutorial vs. getting to content: Agency wins. A guided flow is acceptable only when necessary
  and must be easy to skip or escape.
- [HIG] Brand expression vs. standard components: Familiarity wins on behaviour, placement and sizing; brand may change
  appearance (see Branding below).
- [HIG] Animation or ornament vs. task speed: Delight does not override Purpose. Remove a flourish that slows the
  core task.
- [HIG] Feature count vs. focus: Purpose and Simplicity ask for fewer, better features, but Simplicity is explicitly
  not minimalism. Keep important things close by; do not hide needed controls to look clean.
- [HIG] Data-hungry feature vs. trust: Responsibility wins. Collect only what the feature needs and explain why at the
  moment of asking (details in `references/foundations-motion-writing.md`, Privacy section).
- [HIG] Destructive or irreversible action: Agency asks for forgiveness built in (undo, return to previous state)
  so recovery does not cost time or work.
- [HIG] One layout vs. per-platform tuning: Flexibility asks for both a preserved context (predictable positions,
  natural transition animations) and platform-specific intent. Keep structure recognizable, adapt presentation.
- [HIG] Custom gesture or input: Flexibility asks for alternative inputs; never make one input method the only path.
- [Conv] When two principles still conflict, prefer the option that keeps system-standard behaviour; the rest of the
  HIG repeatedly resolves ties that way, but the principles page itself does not say so.

Source: https://developer.apple.com/design/human-interface-guidelines/design-principles

## Branding

Page last changed 2026-09-09 (refined brand-color guidance). No platform-specific differences are listed.

- [HIG] Use the brand's voice and tone in all written text.
- [HIG] Apply the app accent (brand) color sparingly. Minimize it on controls; reserve it for primary actions and
  status indicators such as an unread badge or the selected tab's icon.
- [HIG] (OS 26+, Liquid Glass) To express brand through color, move the color into the content layer, where it
  scrolls under glass controls and is picked up by them, instead of tinting the controls.
- [HIG] Make sure a custom brand font stays legible at all sizes and supports Bold Text and Dynamic Type. A good split
  is custom font for headlines and subheadings, system font for body and captions.
- [HIG] Express brand with familiar components. If a component's appearance is customized, keep its sizing,
  placement and behaviour familiar for the platform.
- [HIG] Branding defers to content. Do not spend screen space on an element that only shows a brand asset.
- [HIG] Keep standard patterns even in a heavily styled UI: expected locations, standard symbols for common actions,
  established navigation and modality conventions.
- [HIG] Do not show the logo throughout the app unless it is essential for context.
- [HIG] Do not use the launch screen for branding. Put branding on a welcome or onboarding screen instead.
- [Req] Apple trademarks must not appear in the app name or images (the page uses "must not" and links Apple's
  trademark guidelines).

Source: https://developer.apple.com/design/human-interface-guidelines/branding

## Inclusion

All items are recommendations; the page lists no platform differences. Accessibility specifics live in the
accessibility references, not here.

- [HIG] Address people as "you/your"; avoid "the user" or "the player". Reserve "we/our" for the app or company (the
  Writing page goes further and advises avoiding "we" altogether).
- [HIG] Use plain language. Define any technical term before using it. Replace colloquialisms and idioms; the page
  names "peanut gallery" and "grandfathered in" as exclusionary examples.
- [HIG] Be careful with humor: it is subjective, tires with repetition and translates badly.
- [HIG] Avoid unnecessary gender references in copy ("Subscribers can post recipes..." instead of "his or her").
- [HIG] Prefer nongendered person imagery and let people customize avatars and characters.
- [HIG] Ask for gender only when needed (for example health or legal reasons); then offer inclusive options such as
  nonbinary, self-identify and decline to state, and consider asking for pronouns.
- [HIG] Show a range of people, bodies, ages, abilities and relatable settings; avoid stereotyped roles.
- [HIG] Do not build flows on culture- or capability-specific assumptions. The page's example is security questions:
  prefer "What's your favorite activity?" over "What was the make of your first car?".
- [HIG] Include people with disabilities in imagery, use people-first language, and never use a disability as a
  negative metaphor.
- [HIG] Prepare for localization: internationalize first, and check color meanings per locale (white and red are
  the page's examples of colors whose meaning varies by culture).

Source: https://developer.apple.com/design/human-interface-guidelines/inclusion

## Common mistakes

- Quoting "Clarity, Deference, Depth" as the HIG principles -> use the eight current principles.
- Citing a principle as if it were a requirement -> principles are [HIG] rationale; only cite [Req] for items the
  HIG states as mandatory.
- Mandatory multi-screen onboarding with no skip -> make it skippable or remove it (Agency).
- Tinting every control with the brand color -> keep controls neutral, color one primary action, move brand color
  into content (Branding, OS 26+).
- Logo in every toolbar or a branded launch screen -> remove; launch screens are not a branding surface.
- Stripping labels and controls for a "minimal" look -> Simplicity is not minimalism; keep what people need close by.
- Adding animation because it is delightful -> keep it only if it serves the task (Delight vs. Purpose).
- Gendered copy or binary-only gender pickers -> neutral wording; inclusive options only when the data is needed.
