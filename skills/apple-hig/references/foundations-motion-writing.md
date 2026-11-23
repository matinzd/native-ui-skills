# Motion, haptics, feedback, writing and privacy

Scope: motion, Reduce Motion, haptics, feedback, UI copy, capitalization, and privacy rules and requirements.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Motion
- Reduce Motion
- Haptics
- Feedback
- Writing: labels and copy
- Capitalization and alert wording
- Privacy: permission requests
- Privacy: tracking, accounts and data protection
- Common mistakes

## Motion

- [HIG] System components already include motion and adapt it to accessibility settings and input method (Liquid
  Glass reacts more strongly to touch than to a trackpad, OS 26+). Prefer them over custom animation.
- [HIG] Add custom motion only with a purpose: status, feedback, instruction. Gratuitous animation distracts and
  can cause physical discomfort.
- [HIG] Make motion optional: never the only carrier of important information. Back it with haptics or audio.
- [HIG] Feedback motion should follow the gesture and expectations: a view revealed by sliding down from the top is
  not dismissed by sliding sideways.
- [HIG] Keep feedback animations brief and precise.
- [HIG] Do not add motion to frequent interactions on custom elements; standard elements already animate subtly.
- [HIG] Let people cancel motion: do not block input until an animation completes, above all for repeated ones.
- [HIG] Consider animated SF Symbols (SF Symbols 5 or later); see `references/foundations-icons-images.md`.
- [HIG] Games: a steady 30 to 60 fps typically looks smooth; choose good defaults per platform and let people
  trade visuals for performance or battery.

| Platform | Motion specifics |
|----------|------------------|
| iOS, iPadOS, macOS, tvOS | No additional considerations on the Motion page. |
| visionOS | Avoid motion at the edges of the field of view; for large moving objects raise translucency or lower contrast; fade out, move, fade in instead of animating a relocation; do not let people rotate the virtual world (use an instant change during a quick fade); give a stationary frame of reference; avoid sustained oscillation, especially around 0.2 Hz. |
| watchOS | WatchKit layout and appearance animations always include easing that cannot be disabled or customized. |

Source: https://developer.apple.com/design/human-interface-guidelines/motion

## Reduce Motion

The Motion page does not mention the setting by name; the rules are on the Accessibility page.

- [HIG] When Reduce Motion is on, reduce automatic and repetitive animation, including zooming, scaling and
  peripheral motion.
- [HIG] Techniques listed: tighten springs to cut bounce; track animations directly with the gesture; do not
  animate z-axis depth changes; replace x, y and z transitions with fades; do not animate into or out of blurs.
- [HIG] Use fast-moving and blinking animation cautiously in all cases (distraction, dizziness, seizure risk).
- [HIG] Avoid auto-dismissing, time-boxed UI; prefer explicit dismissal.
- [HIG] Do not autoplay audio or video without start and stop controls; video playback should respect the Dim
  Flashing Lights setting.

Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Haptics

- [HIG] Use system haptic patterns only for their documented meanings. If none fits, use a generic pattern or a
  custom one; do not repurpose.
- [HIG] Keep a consistent cause-and-effect link between an action and its haptic.
- [HIG] Haptics complement visual and audio feedback; match intensity and sharpness to the accompanying animation.
- [HIG] Do not overuse. In apps prefer short haptics on discrete events; long-running haptics belong mostly to games.
- [HIG] Make haptics optional: allow turning them off, and keep the app fully usable without them.
- [HIG] Haptics can disturb the camera, gyroscope and microphone; avoid them during such use.
- [HIG] Pair audio cues with haptics so people who cannot hear the cue still receive it.
- [HIG] Standard controls (toggles, sliders, pickers) play system haptics by default on supported iPhone models.
- [Conv] Do not add a second haptic on top of a standard control's built-in one.

| Platform | What the page defines |
|----------|-----------------------|
| iOS | Three feedback categories. Notification: success, warning, error (task outcome). Impact: light, medium, heavy, rigid, soft (physical metaphor such as a snap or collision). Selection: values changing. The page names `UIFeedbackGenerator`. |
| macOS | Only with a Magic Trackpad (Force Touch), during drag or force click: alignment, level change, generic. The page names `NSHapticFeedbackPerformer`. |
| watchOS | Named set, each with one meaning: notification, up, down, success, failure, retry, start, stop, click. Digital Crown detents are provided by the system (Series 4 and later). Do not overuse click. |
| iPadOS, tvOS, visionOS | No built-in pattern list on the page; game controllers can play haptics, and Apple Pencil and some trackpads can on certain iPad models. |

- [HIG] Custom haptics combine transient events (taps) and continuous events (sustained vibration), each with
  sharpness and intensity; the page points to Core Haptics.

Source: https://developer.apple.com/design/human-interface-guidelines/playing-haptics
Source: https://developer.apple.com/design/human-interface-guidelines/accessibility

## Feedback

- [HIG] Match the delivery to the significance: passive status near the item it describes; interruption only for
  critical information.
- [HIG] Deliver feedback through several channels (color, text, sound, haptics) so it reaches people who silence
  the device, look away or use VoiceOver.
- [HIG] Alerts are for critical, ideally actionable information; overuse weakens them.
- [HIG] Warn before data loss that is unexpected and irreversible. Do not warn when the loss is the expected result
  of the action (Finder does not confirm every move to the Trash).
- [HIG] Confirm completion only for significant tasks; people assume success and mainly need to hear of failure.
- [HIG] When a command cannot be carried out, say so and say why.
- [HIG] watchOS: do not show an indeterminate progress indicator; tell people a notification will arrive when the
  work completes.

Source: https://developer.apple.com/design/human-interface-guidelines/feedback

## Writing: labels and copy

- [HIG] Define a voice and a term list; vary tone with context (serious for errors, light for achievements).
- [HIG] Be clear and short: check that every word is needed.
- [HIG] Label buttons and links with verbs that say what happens ("Send", not "Let's do it!"). No "Click here";
  use descriptive link text, which also serves screen readers.
- [HIG] Keep language patterns consistent. In multistep flows pick one scheme ("Get Started", then "Continue" or
  "Next", then "Done") and keep it.
- [HIG] Use possessive pronouns sparingly ("Favorites", not "Your Favorites") and consistently. Avoid "we"
  altogether: "Unable to load content", not "We're having trouble loading this content".
- [HIG] Name gestures correctly per device: "tap" on touch devices, not "click".
- [HIG] Be brief on small screens (iPhone, Apple Watch) and on TV, where text is large and several people may read it.
- [HIG] Empty states: say what to do next and offer a button or link; do not put crucial information there.
- [HIG] Error messages: show next to the problem, do not blame, state the fix ("Choose a password with at least
  8 characters", not "That password is too short"). No "oops" or "uh-oh". No bare "Invalid name".
- [HIG] Text fields: label every field and show a hint or example ("name@example.com"). Phrase validation as what
  to do ("Use only letters for your name").
- [HIG] Settings: practical labels; describe what the setting does when on; link directly to a setting instead of
  describing its location.
- [HIG] Write for everyone: plain language, no jargon, no gendered terms; see
  `references/foundations-design-principles.md` (Inclusion).

Source: https://developer.apple.com/design/human-interface-guidelines/writing

## Capitalization and alert wording

- [HIG] The Writing page does not impose one style: choose a capitalization style per element type and apply it
  consistently (title case reads formal, sentence case casual).
- [HIG] Component pages are more specific and take precedence for those components:

| Element | Style stated in the HIG |
|---------|-------------------------|
| Button titles (including alert buttons) | Title-style capitalization, no ending punctuation |
| Menu item labels | Title-style capitalization |
| Alert title that is a complete sentence | Sentence-style capitalization with ending punctuation |
| Alert title that is a fragment | Title-style capitalization, no ending punctuation |
| Alert informative text | Complete sentences, sentence-style capitalization, punctuation |
| Permission purpose string | Sentence case, active voice, ends with a period |

- [HIG] Alert titles: say what happened and why; no "Error" or error codes alone; no more than two lines.
- [HIG] Alert buttons: one or two words describing the result, verbs preferred ("View All", "Reply", "Ignore");
  "OK" only for informational alerts; avoid "Yes" and "No"; always "Cancel" for the cancelling button.
- [Conv] Where a component page is silent, title-style capitalization for short control labels and sentence style
  for explanatory text matches Apple's own apps.

Source: https://developer.apple.com/design/human-interface-guidelines/writing
Source: https://developer.apple.com/design/human-interface-guidelines/alerts
Source: https://developer.apple.com/design/human-interface-guidelines/buttons
Source: https://developer.apple.com/design/human-interface-guidelines/menus

## Privacy: permission requests

- [Req] Access to protected data and resources goes through the system permission alert. The page lists personal
  data (location, health, financial, contacts), user content (messages, calendar, photos, audio, video), protected
  resources (Bluetooth, local network, Wi-Fi, home automation), camera and microphone, ARKit data in a visionOS
  Full Space, and the advertising identifier.
- [Req] The app supplies the purpose string shown in that alert.
- [HIG] Purpose string: one brief, complete, specific sentence saying how and why the data is used; sentence
  case, active voice, ending period. Not vague ("...for a better experience") and not imperative ("Turn on
  microphone access.").
- [HIG] Request only what a feature needs, as specifically as possible.
- [HIG] Ask when the person uses the feature, not before. Ask at launch only when the app cannot function without
  the data (navigation app and location).
- [HIG] iOS, iPadOS, watchOS: the system location button grants one-time location access on tap. Only title
  choice, filled or outlined glyph, colors and corner radius are customizable; a button the system judges
  illegible will not grant access.
- [HIG] A custom pre-alert screen is allowed only when extra explanation is essential. It has exactly one button,
  titled like "Continue" or "Next" (not "Allow"), that opens the system alert.
- [HIG] No other actions on the pre-alert screen (no close or cancel path that skips the alert), unless needed to
  obtain a legal consent. Worded "Don't".
- [HIG] Process data on device where possible; respect Hide My Email and Mail Privacy Protection choices.
- [HIG] visionOS: ARKit data is unavailable in the Shared Space; gaze is not exposed before a tap; the back camera
  returns blank input, so remove or replace camera-dependent features when bringing an iOS app over.

Source: https://developer.apple.com/design/human-interface-guidelines/privacy

## Privacy: tracking, accounts and data protection

- [Req] App Store submission requires privacy details (practices and data collected) for the product page.
- [Req] To track from launch, the system App Tracking Transparency alert must be shown before any tracking data
  is collected.
- [Req] Never precede the tracking alert with a custom screen that could confuse or mislead. The page states that
  these designs cause App Store rejection: offering incentives, a screen that imitates the request, an image of
  the alert, and annotating the screen behind the alert. A consent screen required by local privacy law is
  allowed before or after the alert. The page cites App Review Guideline 5.1.1 (iv).
- [Req] If the app lets people create an account, it must also let them delete it (not just deactivate). If
  deletion cannot happen in the app, the app must provide a direct, easy-to-find link to the web page where it can.
- [Req] An account created with Sign in with Apple needs its tokens revoked on deletion (developer note).
- [HIG] Keep in-app and web deletion flows equivalent; say when deletion completes and notify when done; if
  scheduled deletion is offered, also offer immediate deletion; explain that subscriptions billed through Apple
  continue until cancelled.
- [HIG] Require an account only if core functionality needs it.
- [HIG] Do not rely on passwords alone: prefer passkeys, Sign in with Apple or Password AutoFill over custom
  schemes; add two-factor authentication if passwords remain; use biometrics for apps that stay signed in. Do not
  call an app credential a "passcode".
- [HIG] Store secrets in the keychain. Never store passwords or other secure content in plain-text files.
- [Req] macOS: apps submitted to the Mac App Store require sandboxing.
- [HIG] macOS: sign with a Developer ID when distributing outside the store; do not assume who is signed in
  (fast user switching).

Source: https://developer.apple.com/design/human-interface-guidelines/privacy
Source: https://developer.apple.com/design/human-interface-guidelines/managing-accounts

## Common mistakes

- Animation that must finish before the next tap registers -> make it interruptible.
- Ignoring Reduce Motion, or replacing motion with nothing -> cross-fade and remove bounce, zoom and parallax.
- Status conveyed only by an animation or only by a haptic -> add text or a symbol.
- Success haptic on every tap, or an error pattern reused for emphasis -> documented meanings, sparingly.
- Confirmation alert for every delete -> warn only for unexpected, irreversible loss; otherwise offer undo.
- Buttons titled "OK", "Yes" or "No" on a decision alert -> specific verbs plus "Cancel".
- "Oops! Something went wrong" -> say what happened and how to fix it, next to the field.
- "We couldn't..." or "Click here" -> neutral phrasing; descriptive link text; "tap" on touch devices.
- Sentence-case button titles mixed with title-case ones -> title-style for button and menu titles throughout.
- Permission prompts fired at first launch -> ask in context when the feature is used.
- Pre-permission screen with "Allow" and "Not now" buttons -> one "Continue" button that opens the system alert.
- Incentive or look-alike screen before the tracking alert -> remove; it leads to App Review rejection.
- Account creation without in-app deletion -> add deletion or a direct link to it.
