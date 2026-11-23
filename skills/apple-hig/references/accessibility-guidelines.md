# Accessibility guidelines (design side)

Scope: what the HIG asks of a design for vision, hearing, mobility, speech and cognitive accessibility, with the exact numbers it gives; API usage lives in `references/accessibility-implementation.md`.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- How to read the numbers
- Vision: text size
- Vision: contrast and color
- Vision: VoiceOver
- Mobility: control size and spacing
- Mobility: gestures and assistive input
- Hearing
- Speech and keyboard
- Cognitive: simplicity, time limits, media
- Cognitive: motion
- Assistive Access (iOS, iPadOS)
- Platform notes
- Accessibility review checklist
- Common mistakes

## How to read the numbers

- [HIG] Treat every size and contrast figure below as a recommendation. The HIG phrases them as "strive to meet", "ideally", "as a general rule" and "about"; none is stated as an App Review requirement. Report a miss as a warning with the HIG figure, not as a hard failure.
- [HIG] Aim for an interface that is intuitive (familiar, consistent interactions), perceivable (no single sense carries the information) and adaptable (follows system accessibility settings or offers its own).
- [HIG] Audit with Accessibility Inspector during design, and declare what the app supports with Accessibility Nutrition Labels on the App Store.
- [HIG] Respect systemwide settings (accessibility accommodations included) instead of duplicating them as in-app settings.
- [HIG] Prefer system components: they carry accessibility support, interaction states and appearance adaptation by default.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/settings , https://developer.apple.com/design/human-interface-guidelines/buttons

## Vision: text size

- [HIG] Let people enlarge text (and meaningful icons). The stated ideal is at least 200 percent enlargement, or 140 percent in watchOS apps, through Dynamic Type or through custom UI.
- [HIG] Use the built-in text styles with system fonts to get Dynamic Type and the larger accessibility sizes where the platform has them.
- [HIG] Dynamic Type exists on iOS, iPadOS, tvOS, visionOS and watchOS. macOS does not support it.
- [HIG] Follow the per-platform default and minimum sizes for custom type as well as system type:

| Platform | Default size | Minimum size |
|----------|--------------|--------------|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- [HIG] Go larger than these sizes when a custom font has a thin weight. In general avoid Ultralight, Thin and Light; prefer Regular, Medium, Semibold or Bold.
- [HIG] Make custom fonts behave like system fonts: scale with Dynamic Type and respond to Bold Text. Test text with Bold Text turned on.
- [HIG] Verify the layout at every text size, including Larger Accessibility Text Sizes on iPhone and iPad.
- [HIG] Keep truncation minimal: show about as much useful text at the largest accessibility size as at the largest standard size, let labels wrap to as many lines as needed, and do not truncate in scrollable regions unless the full text can be opened elsewhere.
- [HIG] At large sizes, stack text above secondary items (glyphs, timestamps) and reduce the number of text columns.
- [HIG] Scale meaningful interface icons with text; SF Symbols do this automatically.
- [HIG] Keep the relative hierarchy of text elements when sizes change, and prioritise the content people care about: not every element must grow (the HIG example is tab titles staying the same size).
- [HIG] Do not rasterize text (stated for widgets): real text scales and can be spoken by VoiceOver.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/typography , https://developer.apple.com/design/human-interface-guidelines/text-views , https://developer.apple.com/design/human-interface-guidelines/widgets

## Vision: contrast and color

The Accessibility page names two measurement standards, WCAG and APCA, and says to use standard contrast calculators. It then lists the values Accessibility Inspector uses, taken from WCAG Level AA, as guidance. That is the only way the HIG invokes WCAG: as the origin of the tool's thresholds, not as a conformance requirement.

| Text size | Text weight | Minimum contrast ratio |
|-----------|-------------|------------------------|
| Up to 17 pt | All | 4.5:1 |
| 18 pt | All | 3:1 |
| All | Bold | 3:1 |

- [HIG] Strive to meet these minimums for foreground text and icons against their background.
- [Conv] Read the "18 pt" row as 18 pt and larger; the page does not say so explicitly and gives no figure between 17 and 18 pt. Use 4.5:1 when in doubt.
- [HIG] Dark Mode page figure: keep contrast no lower than 4.5:1 in every appearance, and for custom foreground and background colors strive for 7:1, especially for small text.
- [HIG] If the default palette misses the minimum, at least supply a higher-contrast scheme that applies when Increase Contrast is on.
- [HIG] Check contrast in both light and dark appearances. In Dark Mode, also test with Increase Contrast and Reduce Transparency on, separately and together; dark text on dark backgrounds is the named failure.
- [HIG] Prefer system-defined colors: they already have light, dark and increased-contrast variants that adapt automatically.
- [HIG] For each custom color supply light and dark variants plus an increased-contrast option for each, with clearly greater visual differentiation. Provide both light and dark values even for a single-appearance app (OS 26+, Liquid Glass adaptivity).
- [HIG] Never rely on color alone to distinguish objects, show interactivity or state, or carry essential information. Add shapes, icons or text. Red-green and blue-orange are the pairings the HIG names as hard for color-blind people.
- [HIG] For toggles and custom switches, make on and off differ by more than hue (fill, shape, checkmark), and keep a custom switch color distinguishable from the off state.
- [HIG] Consider letting people customise color schemes such as chart colors or game characters.
- [HIG] Liquid Glass and materials (OS 26+): their appearance changes when people reduce transparency or increase contrast, so never pick a material for the color it seems to produce. Use the regular glass variant where text legibility is at risk, use system vibrant colors on materials, avoid the quaternary vibrancy level on thin and ultra-thin materials, and keep the resting state of content under controls legible.
- [Unverified] Smart Invert and Differentiate Without Color are not mentioned in the current HIG pages read for this file; any rule about them (for example excluding photos from inversion) must come from the API documentation, not the HIG.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/dark-mode , https://developer.apple.com/design/human-interface-guidelines/color , https://developer.apple.com/design/human-interface-guidelines/materials , https://developer.apple.com/design/human-interface-guidelines/toggles

## Vision: VoiceOver

Descriptions:

- [HIG] Give every key interface element an alternative label. System controls have generic default labels; replace them with ones that describe the app's function. Label all custom elements, custom icons and custom symbols.
- [HIG] Keep labels current as content and state change.
- [HIG] Describe meaningful images, and describe only what the image itself conveys; surrounding captions are read separately.
- [HIG] Exclude purely decorative images from VoiceOver (the HIG points to `accessibilityHidden(_:)`, `accessibilityElement` and `isAccessibilityElement`).
- [HIG] Give each chart or infographic a concise description of what it conveys, and make any chart interaction available to VoiceOver. Audio Graphs can supplement labels; Swift Charts supplies a default implementation.
- [HIG] For gauges, write short labels for the current value and both ends of the range.

Navigation:

- [HIG] Give each screen a unique, succinct title; it is the first thing an assistive technology announces. Use accurate section headings.
- [HIG] VoiceOver reads in the reading order of the active language and locale (top-to-bottom, left-to-right in US English). Where relationships are only visual (proximity, alignment), declare grouping, order and links so that, for example, each image is read with its own caption.
- [HIG] Announce visible content or layout changes so people's mental map stays correct (`AccessibilityNotification`).
- [HIG] Support the VoiceOver rotor where content has headings, links or similar types.
- [HIG] Make all feedback reach more than one sense (color, text, sound, haptics) so it still arrives when someone uses VoiceOver, has the device silenced or is looking away.
- [HIG] Keep a grabber on resizable sheets: it lets VoiceOver users resize the sheet.
- [HIG] Offer non-drag ways to do drag-and-drop tasks (menu commands, for example); on iOS and iPadOS, accessibility APIs can expose drag sources and drop points.

Source: https://developer.apple.com/design/human-interface-guidelines/voiceover , https://developer.apple.com/design/human-interface-guidelines/charts , https://developer.apple.com/design/human-interface-guidelines/feedback , https://developer.apple.com/design/human-interface-guidelines/gauges , https://developer.apple.com/design/human-interface-guidelines/sheets , https://developer.apple.com/design/human-interface-guidelines/drag-and-drop

## Mobility: control size and spacing

Accessibility page table ("strive to meet"):

| Platform | Default control size | Minimum control size |
|----------|----------------------|----------------------|
| iOS, iPadOS | 44x44 pt | 28x28 pt |
| macOS | 28x28 pt | 20x20 pt |
| tvOS | 66x66 pt | 56x56 pt |
| visionOS | 60x60 pt | 28x28 pt |
| watchOS | 44x44 pt | 28x28 pt |

- [HIG] Buttons page figure: as a general rule a button needs a hit region of at least 44x44 pt, or 60x60 pt in visionOS.
- [Conv] The two pages do not agree on their face: Buttons calls 44 pt (60 pt visionOS) the least a hit region should be, while the Accessibility table lists a smaller "minimum control size" (28 pt on iOS, iPadOS, visionOS, watchOS). The HIG does not reconcile them. A workable reading is that the table describes the control and the Buttons figure the hit region, but that is an interpretation, not Apple's wording.
- [Conv] Safe default for agents: give every interactive element a hit region of at least the table's default size (44 pt iOS, iPadOS, watchOS; 60 pt visionOS; 66 pt tvOS; 28 pt macOS). Flag anything under the default as a warning, and anything under the table minimum as a defect. The visible shape may be smaller than the hit region.
- [HIG] Spacing matters as much as size: about 12 pt of padding around elements that have a bezel, about 24 pt around the visible edges of elements without one.
- [HIG] visionOS: keep at least 16 pt of margin around each interactive item or place centers at least 60 pt apart; add 4 pt of padding around buttons that are 60 pt or larger; avoid rows or stacks of small and mini buttons.
- [HIG] macOS with a touch display (HIG change dated 2026-10-28): enlarge tap targets rather than the controls, keep layout and density unchanged, and never make touch the only route to a feature. Standard controls get a suitable tap target automatically.
- [HIG] macOS image buttons: leave about 10 pixels between the image and the button edge so imprecise clicks still register.
- [HIG] Always give a custom button a press state.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/buttons , https://developer.apple.com/design/human-interface-guidelines/eyes , https://developer.apple.com/design/human-interface-guidelines/gestures

## Mobility: gestures and assistive input

- [HIG] Use the simplest possible gesture for frequent actions; avoid custom multifinger and multihand gestures.
- [HIG] Make core functionality reachable by more than one kind of physical interaction. Every gesture needs an onscreen alternative: a swipe-to-dismiss view also gets a button.
- [HIG] Do not assume anyone can perform a particular gesture; people may be using voice, a keyboard or Switch Control.
- [HIG] Use shortcut gestures to supplement standard navigation and actions, never to replace them, and do not conflict with system gestures.
- [HIG] Voice Control: label interface elements appropriately so they can be addressed by speaking.
- [HIG] Integrate with Siri and Shortcuts so frequent tasks can be done by voice alone.
- [HIG] Test with VoiceOver, AssistiveTouch, Full Keyboard Access, Pointer Control and Switch Control, and confirm elements are labeled for them. The HIG gives no AssistiveTouch-specific design rules beyond this.
- [HIG] Switch Control drives the device from separate hardware, game controllers or sounds; the app must be navigable with it. In interactive charts, give keyboard and Switch Control users a logical path (for example along one axis, or through subsets of a large data set) instead of every data point in file order.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/gestures , https://developer.apple.com/design/human-interface-guidelines/charts

## Hearing

- [HIG] Never deliver dialogue or crucial information through audio alone.
- [HIG] Offer the text form that fits the media, and let people customise how that text looks:

| Form | What it carries | Good for |
|------|-----------------|----------|
| Captions | Text equivalent of audible information, synchronised with the media | Video clips, game cutscenes, audio-only content |
| Subtitles | Onscreen dialogue in the viewer's preferred language | TV shows, movies |
| Audio descriptions | Spoken narration of visual-only information, placed in natural pauses | Video |
| Transcripts | Full text of audible and visual information | Podcasts, audiobooks, long-form media |

- [HIG] Pair audio cues (success chime, error sound, game feedback) with matching haptics for people who cannot hear them or have sound off. On iOS and iPadOS, Music Haptics and Audio Graphs are additional options.
- [HIG] Add visual cues to audio cues, especially in games and spatial apps where the event may be off screen; when sound guides people to an action, also show where to interact.
- [HIG] Keep haptics optional: people can turn them off, so the app must remain usable without them. Use system haptic patterns only for their documented meanings.
- [HIG] In SharePlay sessions keep volume and subtitle settings per participant.
- [HIG] The system video player's transport controls expose subtitles and audio language in tvOS and visionOS, and the RealityKit video player supports closed captions; prefer system players so these come for free.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/playing-haptics , https://developer.apple.com/design/human-interface-guidelines/playing-audio , https://developer.apple.com/design/human-interface-guidelines/playing-video , https://developer.apple.com/design/human-interface-guidelines/shareplay

## Speech and keyboard

The HIG's Speech section covers people with speech disabilities and people who prefer text-based interaction; its two rules are keyboard-only operation and Switch Control (see above).

- [HIG] Make the app fully usable from the keyboard alone and check it with Full Keyboard Access, which is available in iOS, iPadOS, macOS and visionOS.
- [HIG] Do not override system-defined keyboard shortcuts, including the accessibility shortcuts.
- [HIG] iPadOS and macOS: provide your own focus support for content elements (list items, text fields, search fields) and leave buttons, sliders, toggles and similar controls to Full Keyboard Access rather than adding custom keyboard navigation for them.
- [HIG] tvOS: every onscreen element must be able to take focus, because the remote reaches things only through focus.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/keyboards , https://developer.apple.com/design/human-interface-guidelines/focus-and-selection

## Cognitive: simplicity, time limits, media

- [HIG] Keep interactions easy to remember and consistent. Prefer system gestures and behaviors people already know over custom ones they must learn.
- [HIG] Minimise time-boxed interface elements. Views and controls that dismiss themselves on a timer fail people who need longer to read or whose assistive technology takes longer to traverse the screen; dismiss with an explicit action instead. The HIG states no specific time-out duration.
- [HIG] Do not autoplay audio or video without discoverable, easy controls to start and stop it. Consider a global setting to opt out of all autoplay (the HIG points to `isVideoAutoplayEnabled` and the animated-images setting).
- [HIG] Apps that play video should respond to the Dim Flashing Lights setting.
- [HIG] Games: consider difficulty accommodations (easier completion criteria, adjustable reaction time, control assistance) and let players adjust type size, control mapping, motion intensity and sound balance.
- [HIG] Describe a chart's purpose in its title and labels before the detail; the HIG names VoiceOver users and people with some cognitive disabilities as relying on this.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/designing-for-games , https://developer.apple.com/design/human-interface-guidelines/charts

## Cognitive: motion

- [HIG] Be cautious with fast-moving and blinking animation; in excess it distracts, can cause dizziness and in some cases epileptic episodes.
- [HIG] When Reduce Motion is on, reduce automatic and repetitive animation, including zooming, scaling and peripheral motion. Further practices the HIG lists:
  - tighten springs to cut bounce;
  - make animation track the person's gesture directly;
  - do not animate depth changes between z-axis layers;
  - replace x, y and z transitions with fades;
  - do not animate into or out of blurs.
- [HIG] Make motion optional: never use it as the only carrier of important information; back it with haptics or audio, and with a non-animated cue for VoiceOver users and people who turn animations off.
- [HIG] Let people cancel motion; do not make them wait for an animation, especially a repeated one.
- [HIG] Avoid adding custom motion to interactions that happen frequently.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/motion , https://developer.apple.com/design/human-interface-guidelines/charts

## Assistive Access (iOS, iPadOS)

- [HIG] Assistive Access presents a streamlined version of an app for people with cognitive disabilities, with a system-set layout and control presentation. When it is on:
  - cut the app to its core function and consider removing noncritical flows and elements;
  - split multistep flows so each screen holds one interaction;
  - ask for confirmation twice before any action that is hard to undo, such as deleting a file.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Platform notes

The Accessibility and VoiceOver pages state no additional considerations for iOS, iPadOS, macOS, tvOS or watchOS; the rows below collect what those and neighbouring pages say per platform.

| Platform | Notes |
|----------|-------|
| iOS, iPadOS | [HIG] Dynamic Type with larger accessibility sizes; Assistive Access; Music Haptics and Audio Graphs; Full Keyboard Access covers controls and drag and drop. |
| macOS | [HIG] No Dynamic Type; 13 pt default and 10 pt minimum text; 28 pt default and 20 pt minimum controls; Full Keyboard Access and VoiceOver can perform drag and drop; touch is secondary input, enlarge tap targets only. |
| tvOS | [HIG] 29 pt default and 23 pt minimum text; 66 pt default and 56 pt minimum controls; everything must be focusable; Dynamic Type is available. |
| watchOS | [HIG] Text enlargement ideal is 140 percent; 16 pt default and 12 pt minimum text; 44 pt default and 28 pt minimum controls; Dark Mode is not supported. |
| visionOS | [HIG] See the list below. Dark Mode is not supported. |

visionOS:

- [HIG] System accessibility features include VoiceOver, Switch Control, Dwell Control, Guided Access, head and hand Pointer Control, and Zoom.
- [Req] With VoiceOver on, apps that define custom gestures do not receive hand input by default; a person must enable Direct Gesture mode to pass hand input through. Do not make a custom gesture the only way to do something.
- [HIG] Do not anchor content to the wearer's head: it feels confining and blocks assistive technologies such as Pointer Control.
- [HIG] Keep interface elements inside the field of view, prefer horizontal over vertical layouts, and do not demand attention in different places in quick succession.
- [HIG] Reduce the speed and intensity of animated objects, above all in peripheral vision; keep camera and video motion gentle; avoid making the world seem to move without the person's control; avoid sustained oscillation, in particular around 0.2 Hz.
- [HIG] Minimise large and repetitive gestures; do not require specific body movements, positions or both hands without a lower-effort alternative.
- [HIG] Never convey important information by sound alone, here as on every platform.
- [HIG] For text with no background behind it, prefer bold weight to shadows for legibility; test text legibility at different scales.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility , https://developer.apple.com/design/human-interface-guidelines/voiceover , https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos , https://developer.apple.com/design/human-interface-guidelines/motion , https://developer.apple.com/design/human-interface-guidelines/gestures , https://developer.apple.com/design/human-interface-guidelines/typography , https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Accessibility review checklist

Run each item against the design or code; the bracket names the section that holds the rule and its numbers.

1. [HIG] Text uses text styles or otherwise scales; nothing is fixed at one point size where Dynamic Type exists. (Vision: text size)
2. [HIG] No text is below the platform minimum size; body content is at or near the default size. (Vision: text size)
3. [HIG] At the largest accessibility text size nothing clips, overlaps or truncates essential text; rows restack. (Vision: text size)
4. [HIG] No Ultralight, Thin or Light weights for small text; custom fonts honor Bold Text. (Vision: text size)
5. [HIG] Text and icon contrast meets 4.5:1 (3:1 for 18 pt or bold) in light and in dark. (Vision: contrast and color)
6. [HIG] Custom colors have light, dark and increased-contrast variants; no hard-coded non-adaptive colors. (Vision: contrast and color)
7. [HIG] State, status, validity and interactivity are never signalled by color alone. (Vision: contrast and color)
8. [HIG] Text over materials or glass stays legible with Reduce Transparency and Increase Contrast on. (Vision: contrast and color)
9. [HIG] Every control, custom element and icon-only button has a descriptive label that tracks its state. (Vision: VoiceOver)
10. [HIG] Meaningful images and charts are described; decorative images are hidden from VoiceOver. (Vision: VoiceOver)
11. [HIG] Each screen has a unique title and real headings; reading order and grouping match the visual logic. (Vision: VoiceOver)
12. [HIG] Content and layout changes are announced. (Vision: VoiceOver)
13. [Conv] Every hit region is at least the platform default size, and never under the table minimum. (Mobility: control size and spacing)
14. [HIG] Adjacent controls have about 12 pt (bezeled) or 24 pt (unbezeled) of padding; visionOS centers are 60 pt apart. (Mobility: control size and spacing)
15. [HIG] Every swipe, long press, drag or custom gesture has a visible control or menu alternative. (Mobility: gestures and assistive input)
16. [HIG] The screen works with Full Keyboard Access and Switch Control; no system shortcut is overridden. (Speech and keyboard)
17. [HIG] No essential information arrives by sound alone; audio cues have haptic or visual partners. (Hearing)
18. [HIG] Video and audio content offers captions, subtitles, audio descriptions or transcripts as appropriate. (Hearing)
19. [HIG] The app remains fully usable with haptics off. (Hearing)
20. [HIG] Nothing essential auto-dismisses on a timer. (Cognitive: simplicity, time limits, media)
21. [HIG] Media does not autoplay without visible start and stop controls; video honors Dim Flashing Lights. (Cognitive: simplicity, time limits, media)
22. [HIG] With Reduce Motion on, zooms, scaling, parallax, bounce and blur transitions are reduced or replaced by fades. (Cognitive: motion)
23. [HIG] No information is conveyed only by animation; no excessive flashing or blinking. (Cognitive: motion)
24. [HIG] visionOS only: nothing is head-anchored, nothing needs a specific posture or two hands, custom gestures have alternatives under VoiceOver. (Platform notes)

## Common mistakes

- Calling 44x44 pt a universal Apple requirement -> it is the iOS, iPadOS and watchOS default and a Buttons-page general rule; use the per-platform table and report misses as HIG recommendations.
- Treating 28 pt as an acceptable everyday target on iOS because the table lists it -> it is the floor; design to the default.
- Quoting WCAG AA as something Apple requires -> the HIG only says Accessibility Inspector uses those values as guidance and also names APCA.
- Checking contrast in light appearance only -> check dark too, and with Increase Contrast and Reduce Transparency.
- Red and green dots as the only status indicator -> add a shape, icon or text.
- Shrinking the visible button to fit a dense layout and shrinking its hit region with it -> keep the hit region at the default size and keep the padding.
- Fixed point sizes or single-line labels that truncate at large text sizes -> text styles, wrapping, stacked layouts.
- Labelling a decorative image, or leaving an icon-only button with its symbol name as the label -> hide decoration; write a functional label.
- Swipe-only delete, long-press-only menus, drag-only reordering -> add a visible button or menu command.
- Toasts and banners carrying essential information that vanish after a few seconds -> keep them until dismissed.
- Ignoring Reduce Motion, or removing all feedback instead of substituting fades -> reduce motion but keep the state change perceivable.
- Sound-only or haptic-only feedback -> pair it with a visual cue.
- Building custom keyboard navigation for buttons on iPadOS -> leave controls to Full Keyboard Access; handle focus for content elements.
- Adding an in-app copy of a system accessibility setting -> follow the system setting.
- Assuming macOS scales text with Dynamic Type -> it does not; choose sizes from the macOS defaults.
