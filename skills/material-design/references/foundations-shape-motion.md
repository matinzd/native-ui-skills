# Shape, elevation and motion foundations

Scope: the Material 3 corner radius scale, the shape library and shape morph, elevation levels and when to show shadow versus tone, the spring-based motion schemes, the status of legacy easing and duration tokens, transition patterns, and reduced motion; code is in `references/implementation-theming.md`.
Verified: 2026-11-23 against the sources linked in each section (Material 3 Expressive).

## Contents

- What changed with Material 3 Expressive
- Corner radius scale
- Which components use which corner
- Customizing shape
- Shape library and shape morph
- Elevation levels
- Shadow versus tone
- Motion schemes and springs
- Spring tokens
- Legacy easing and duration (no longer maintained)
- Transition patterns
- Transition quality rules
- Reduced motion
- Form-factor notes
- Common mistakes

## What changed with Material 3 Expressive

| Area | Earlier | Now |
|------|---------|-----|
| Shape scale | Material 2: three levels based on component size | ten corner styles named by roundedness; 20dp, 32dp and 48dp steps added May 2025 |
| Fully rounded | defined as 50% of the component size | its own "full" value |
| Shape library | none | 35 shapes with built-in morphing (May 2025), in the Figma kit and Jetpack Compose |
| Elevation | Material 2: shadows at every level | six levels; tone by default, shadow only where needed; surface tint deprecated |
| Component motion | easing curves plus duration tokens | motion physics: springs chosen by a motion scheme (May 2025) |
| Transitions | easing and duration | still easing and duration; Material says they will move to the physics system eventually |

Source: https://m3.material.io/styles/shape/overview-principles , https://m3.material.io/styles/shape/corner-radius-scale , https://m3.material.io/styles/elevation/overview , https://m3.material.io/styles/motion/overview/how-it-works , https://m3.material.io/styles/motion/transitions/transition-patterns

## Corner radius scale

| Style | Corner value |
|-------|--------------|
| None | 0dp |
| Extra small | 4dp |
| Small | 8dp |
| Medium | 12dp |
| Large | 16dp |
| Large increased (Material 3 Expressive) | 20dp |
| Extra large | 28dp |
| Extra large increased (Material 3 Expressive) | 32dp |
| Extra extra large (Material 3 Expressive) | 48dp |
| Full | fully rounded |

- [API] The scale defines every rectangular component shape. Shape corner tokens set all four corners; corner-value tokens set individual corners.
- [API] Asymmetric variants in the token list: extra small top, large top, large start, large end, extra large top. They use the same ten steps.
- [API] Asymmetric "inner corners" are used where items sit close together, such as menus and split buttons; those component tokens map to individual corner tokens.
- [MD] Products should generally use these shape styles consistently; customization is acceptable, and encouraged, for hero moments and custom components.

Source: https://m3.material.io/styles/shape/corner-radius-scale

## Which components use which corner

The shape pages name only a few mappings; the rest come from each component's specs page.

| Component | Default corner | Stated on |
|-----------|----------------|-----------|
| Buttons | full | corner radius scale page (corner values vary by button size on the specs page) |
| Cards | medium, 12dp | corner radius scale page; cards specs |
| Small FAB | medium | corner radius scale page |
| Chips | 8dp (avatar inside an input chip 12dp) | chips specs |
| Basic dialog | 28dp | dialogs specs |
| Full-screen dialog | 0dp | dialogs specs |
| Menus, split buttons | asymmetric inner corners | corner radius scale page |
| XR spatial panel | 32dp at launch | XR layout page |

- [Conv] For any component not listed, read its shape from the theme or the component's specs page instead of guessing; see the `components-*` files. Do not hard-code a radius on a Material component.

Source: https://m3.material.io/styles/shape/corner-radius-scale , https://m3.material.io/components/cards/specs , https://m3.material.io/components/chips/specs , https://m3.material.io/components/dialogs/specs , https://m3.material.io/foundations/xr/design/layout

## Customizing shape

- [MD] Style-level change: resize a style (for example medium) and every component mapped to it follows, unless it has an override.
- [MD] Component-level change: remap one component to another style on the scale, for example buttons from full to small or medium.
- [MD] The corner family can change from rounded to cut. Cut corners clip more content than a rounded corner of the same size, so add padding in information-dense components.
- [MD] Be careful applying large or full corners to information-dense components such as cards.
- [MD] Nested rounded shapes: avoid the same radius on both. Use optical roundness: outer radius minus padding equals inner radius (the worked example is 48dp - 14dp = 34dp).
- [MD] Mixing square and fully rounded shapes to create tension is allowed and described as more expressive, for states or to draw attention.

Source: https://m3.material.io/styles/shape/corner-radius-scale , https://m3.material.io/styles/shape/overview-principles

## Shape library and shape morph

(Material 3 Expressive.)

- [MD] Use the 35-shape library for mostly visual elements: image crops, avatar masks, decorative and other non-interactive elements. Avoid unconventional shapes on text-heavy containers.
- [MD] Use abstract shapes sparingly and with a reason; do not trade clarity for visual effect.
- [MD] Shape is not semantic: avoid giving one shape a fixed function or meaning. (The example: a wavy loading indicator does not make the wave a symbol for progress.)
- [MD] Morph shapes to communicate interaction states (a selected button), actions in progress (typing, loading) and changes in the environment. Morphing should respond to user interaction.
- [API] All library shapes can morph into each other. Material components that use shape morph: the standard button group and the loading indicator.
- [API] Shape morph uses the expressive motion scheme by default and can be switched to the standard scheme.
- [API] Availability as listed: shape library in Jetpack Compose and in Android Views (MDC-Android); shape morph on Android through the Compose shapes API; not available on web.

Source: https://m3.material.io/styles/shape/overview-principles , https://m3.material.io/styles/shape/shape-morph , https://m3.material.io/styles/shape/corner-radius-scale

## Elevation levels

| Level | dp | Components resting at this level |
|-------|----|----------------------------------|
| 0 | 0dp | app bar (not scrolled); filled, tonal and outlined buttons; button groups; filled and outlined cards; carousel; chips; full-screen dialog; FAB and extended FAB inside a navigation rail; FAB menu list items; icon buttons; list; navigation rail; segmented button; docked side sheet; slider; split button; tabs |
| 1 | 1dp | banner; modal bottom sheet; elevated button; elevated card; elevated chips; modal navigation drawer; modal side sheet |
| 2 | 3dp | app bar (scrolled); menu; navigation bar; rich tooltip; toolbar |
| 3 | 6dp | date pickers; modal dialogs; extended FAB; FAB; FAB menu close button; search; time pickers |
| 4 | 8dp | not assigned as a resting level |
| 5 | 12dp | not assigned as a resting level |

- [API] Resting elevation is level 0 to 3. Levels 4 and 5 are reserved for user-interacted states such as hover and dragged.
- [MD] Keep each Material component at the resting elevation it ships with, and work with few levels overall.
- [MD] When interaction or a system event changes elevation, similar elements should change in the same way. Hover or focus usually raises a component one level (a FAB goes from 3 to 4; all Material buttons rise one level on hover).
- [API] Elevation tokens carry only the z-distance. They have no shadow or color of their own; each platform decides how a level is drawn.

Source: https://m3.material.io/styles/elevation/tokens , https://m3.material.io/styles/elevation/applying-elevation , https://m3.material.io/styles/elevation/overview

## Shadow versus tone

- [MD] By default, Material 3 surfaces show separation through tonal difference: overlapping areas get different surface or surface container roles. Roles: `references/foundations-color.md`.
- [MD] Add a visible shadow only when it is needed: to protect an element against a patterned or busy background (cards, chips, buttons over imagery), or to encourage interaction (an element lifting on focus, selection or swipe).
- [MD] A scrim is the third way to separate layers; use it beneath modals and expanded navigation. It uses the scrim role at 32% opacity.
- [MD] For interactive components, the edge between surfaces must have enough contrast to be seen as separate.
- [MD] Smaller, sharper shadows read as close; larger, softer shadows read as farther away. Fewer levels give each one more power.
- [API] Surface tint color is deprecated; Material says to use the elevation level tokens (0-5). Surface container roles are not tied to elevation.
- [API] On Android, enter and exit motion avoids scale and z-axis movement because those imply an elevation change that does not fit the reduced elevation model.

Source: https://m3.material.io/styles/elevation/applying-elevation , https://m3.material.io/styles/elevation/overview , https://m3.material.io/styles/elevation/tokens , https://m3.material.io/styles/motion/transitions/transition-patterns

## Motion schemes and springs

(Material 3 Expressive, May 2025.) The motion physics system replaces easing and duration for component motion.

| Scheme | Character | Use |
|--------|-----------|-----|
| Expressive | overshoots the final value and bounces into place | Material's opinionated default: most situations, especially hero moments and key interactions |
| Standard | minimal bounce; eases into the final value | utilitarian products |
| Custom | defined by the product | when neither preset fits; still themed |

- [MD] Most motion in a product should use one scheme. A product may swap the scheme for specific elements to emphasize key moments.
- [API] A spring is defined by stiffness, damping and initial velocity. Springs handle gestures, interruption and retargeting, which fixed-duration animation does not.
- [API] The scheme is chosen at product (theme) level and is not part of the token name, so switching scheme does not change which token an element uses.
- [API] Availability as listed: Jetpack Compose available, and 21 Material components use the physics system by default; Android Views (MDC-Android) has the spring tokens but they are not applied to components; Flutter unavailable; web is "compatible" through converted curves.
- [MD] Three levels of use: take a default scheme (stated as sufficient for all motion needs); define a custom scheme for the whole product; or swap the scheme for one element, screen or component.

Source: https://m3.material.io/styles/motion/overview/how-it-works , https://m3.material.io/styles/motion/overview/specs

## Spring tokens

Six tokens per scheme: two kinds times three speeds, named like `md.sys.motion.spring.fast.spatial`.

| Kind | Animates | Overshoot |
|------|----------|-----------|
| Spatial | position (x, y), rotation, size, rounded corners | yes: overshoots and settles |
| Effects | color and opacity | no: there should be no overshoot |

| Speed | Spatial example | Effects example |
|-------|-----------------|-----------------|
| Default (most motion) | elements that partly cover the screen: bottom sheet, expanded navigation rail | opacity of content inside a navigation rail |
| Fast (smaller elements) | switches, buttons | color change of a switch handle |
| Slow (larger elements) | full-screen animations | full-screen content refresh |

Values shown in the token table for the standard scheme on Android (damping / stiffness):

| Token | Spatial | Effects |
|-------|---------|---------|
| Fast | 0.9 / 1400 | 1 / 3800 |
| Default | 0.9 / 700 | 1 / 1600 |
| Slow | 0.9 / 300 | 1 / 800 |

- [API] Exact token values differ by device class (wearable, phone, tablet) so that "fast" feels fast on each; do not copy numbers between form factors.
- [Unverified] The damping and stiffness values of the expressive scheme were not readable in the rendered token table (it displayed the standard scheme only). Take them from the library source, not from memory.
- [MD] Custom components should use the spring tokens too: spatial for anything that moves or resizes, effects for color and opacity.
- [API] Web conversion table (cubic-bezier, duration), for comparison only: expressive spatial fast 0.42, 1.67, 0.21, 0.90 at 350ms; default 0.38, 1.21, 0.22, 1.00 at 500ms; slow 0.39, 1.29, 0.35, 0.98 at 650ms. Standard spatial 0.27, 1.06, 0.18, 1.00 at 350, 500 and 750ms. Effects, both schemes: fast 0.31, 0.94, 0.34, 1.00 at 150ms; default 0.34, 0.80, 0.34, 1.00 at 200ms; slow 0.34, 0.88, 0.34, 1.00 at 300ms. Material says to use real springs when possible and curves only for animations without gestures or interruption.

Source: https://m3.material.io/styles/motion/overview/how-it-works , https://m3.material.io/styles/motion/overview/specs

## Legacy easing and duration (no longer maintained)

- [API] Status in Material's words, paraphrased: components and motion now use the physics system; products should migrate; easing and duration is still used for transitions and by teams not yet on Expressive, but is no longer maintained. The specs page calls these tokens a fallback and says the easing, duration and path tokens "can be ignored" for the physics system.
- [Conv] So: springs for component and custom-element motion; easing and duration only for screen transitions that have not moved yet, or on a library version without the motion scheme.

| Easing | Default duration | Transition type | Android curve |
|--------|------------------|-----------------|---------------|
| Emphasized | 500ms | begins and ends on screen; also exits that can be retrieved | two-segment path interpolator |
| Emphasized decelerate | 400ms | enters the screen | 0.05, 0.7, 0.1, 1 |
| Emphasized accelerate | 200ms | exits the screen permanently | 0.3, 0, 0.8, 0.15 |
| Standard | 300ms | begins and ends on screen | 0.2, 0, 0, 1 |
| Standard decelerate | 250ms | enters the screen | 0, 0, 0, 1 |
| Standard accelerate | 200ms | exits the screen | 0.3, 0, 1, 1 |

| Duration tokens | Values | Use |
|-----------------|--------|-----|
| short1-4 | 50, 100, 150, 200ms | small utility transitions |
| medium1-4 | 250, 300, 350, 400ms | transitions crossing a medium area |
| long1-4 | 450, 500, 550, 600ms | large expressive transitions, often with emphasized easing |
| extra-long1-4 | 700, 800, 900, 1000ms | rare; ambient transitions without user input |

- [MD] The emphasized set is recommended for most transitions; the standard set is for small, quick utility transitions and as a fallback where emphasized is unsupported (Material names iOS and web).
- [MD] Duration scales with the area covered. Exits, dismissals and collapses are shorter than entrances. Avoid durations so short that they jar, or so long that people wait.

Source: https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration , https://m3.material.io/styles/motion/easing-and-duration/tokens-specs , https://m3.material.io/styles/motion/overview/specs

## Transition patterns

| Pattern | Use for | Motion | Commonly with |
|---------|---------|--------|---------------|
| Container transform | an element expanding to show more detail | a persistent container (or hero element) links start and end | cards, lists, image galleries, search boxes, sheets, FABs, chips |
| Forward and backward | consecutive levels of hierarchy, such as inbox to thread | horizontal slide; Android's default also fades so screens travel less | lists, cards, buttons, links |
| Lateral | peer content at one level, such as tabs | grouped horizontal slide with no fade or parallax; hints at swiping | tabs, carousels, image galleries |
| Top level | switching top-level destinations | exiting screen fades out quickly, then the entering screen fades in; no shared elements | navigation bar, rail, drawer |
| Enter and exit | introducing or removing a component | Android components expand and collapse along x or y, away from the nearest edge | dialogs, menus, snackbars, FABs, tooltips; sheets, bars and drawers from beyond the screen |
| Skeleton loaders | loading to loaded | subtle pulse from top left to bottom right; content fades in quickly on top | any loading surface |

- [MD] Forward and backward navigation should use the platform default transition (Material says this for both Android and iOS).
- [MD] Do not use a lateral transition between top-level destinations: it implies swiping, which conflicts with carousels and swipeable list items. Do not use lateral or enter-and-exit transitions for hierarchical navigation either.
- [MD] Reserve container transform for hero moments and shallow hierarchies. Do not use it in apps with deep hierarchies, and do not use a plain forward and backward transition for a hero moment such as opening a photo memory.
- [MD] Bottom sheets and the keyboard enter from the bottom; a navigation drawer enters from the leading side; where a component enters tells people where it lives.

Source: https://m3.material.io/styles/motion/transitions/transition-patterns , https://m3.material.io/styles/motion/transitions/applying-transitions

## Transition quality rules

- [MD] Common transitions keep a simple style. Do not put overt effects such as bouncy springs on them: they are frequent and cover large areas.
- [MD] Give a transition one unified direction; group elements along a primary axis and keep only important elements (a hero image) persistent.
- [MD] Fade old content fully out before fading new content in. If a cross-fade is unavoidable, keep it short and hide it in the fastest part of the transition.
- [MD] Do not fade a bottom sheet as it enters or exits, and do not slowly fade components over other content. A dialog's fade should be short.
- [MD] Keep layouts stable with skeleton loaders; content should not pop in or shift position during a transition.
- [MD] Avoid jump cuts by default; a jump cut may be right where pure efficiency matters, such as opening a menu in a productivity app.
- [MD] Keep one spatial model: do not switch a carousel between horizontal and vertical layouts across a transition.

Source: https://m3.material.io/styles/motion/transitions/applying-transitions

## Reduced motion

- [MD] When the platform's reduced animation setting is on, transitions should use subtle fades instead of strong sliding or scaling, and decorative effects such as parallax and shape morphing should be disabled.
- [MD] Carousel, as a component example: with reduced motion on, remove the parallax effect and stop items expanding as they come into view; all items become the same size.
- [MD] On dense products such as desktop, menus may open instantly to reduce motion.
- [Conv] Material words this as "should". Treat ignoring the setting as an accessibility issue in review, because people set it for motion sensitivity. How to read the setting in code: `references/accessibility-implementation.md`.

Source: https://m3.material.io/styles/motion/transitions/applying-transitions , https://m3.material.io/components/carousel/accessibility , https://m3.material.io/components/menus/guidelines

## Form-factor notes

| Form factor | Note | More |
|-------------|------|------|
| Desktop | transitions can be faster for small elements and short distances; slow down or simplify when large elements move far | `references/platforms-large-screens.md` |
| Watch | spring token values differ for wearables; Wear OS has its own shape and motion guidance | `references/platforms-wear.md` |
| XR | real depth (spatial elevation) replaces shadow-based elevation; panels launch with 32dp corners | `references/platforms-auto-xr.md` |

Source: https://m3.material.io/foundations/desktop/overview , https://m3.material.io/foundations/watches/styles , https://m3.material.io/foundations/xr/design/layout

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Arbitrary radii such as 6dp or 10dp on components | Use a step from the scale: 0, 4, 8, 12, 16, 20, 28, 32, 48dp, full |
| "Full" written as 50% | Use the full corner style |
| Same radius on a container and the element nested in it | Inner radius = outer radius minus padding |
| Unusual shapes on text-heavy containers | Keep library shapes for imagery, avatars and decoration |
| Shadows on every surface | Tone first; shadow for busy backgrounds or lifted interaction |
| Tinting a surface by elevation | Surface tint is deprecated; use container roles and elevation levels |
| Resting elevation at level 4 or 5, or changed component defaults | Rest at 0-3; keep defaults |
| Easing and duration tokens on component animation | Motion scheme springs: spatial for movement, effects for color and opacity |
| Overshoot on a color or opacity animation | Effects springs do not overshoot |
| Bouncy spring on a screen transition | Transitions stay simple; platform default for forward and back |
| Sliding sideways between navigation bar destinations | Top-level fade through |
| Ignoring the reduced animation setting | Fades instead of slides and scales; no parallax or shape morph |
