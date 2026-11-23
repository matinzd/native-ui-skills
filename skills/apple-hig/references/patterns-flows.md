# Flow patterns: launch to settings

Scope: HIG pattern guidance for the flows agents build most often: launching, onboarding, loading, modality, entering data, settings, accounts, notification management, searching, full screen, help, ratings, and sharing.
Verified: 2026-11-23 against the sources linked in each section (SDK cycle: OS 27).

## Contents

- Flow order at a glance
- Launching and launch screens
- Onboarding
- Loading
- Modality
- Entering data
- Settings
- Managing accounts
- Managing notifications
- Searching
- Going full screen
- Offering help and tips
- Ratings and reviews
- Collaboration and sharing
- Other pattern pages
- Common mistakes

## Flow order at a glance

| Moment | What the HIG expects |
|---|---|
| App start | [HIG] Launch screen that matches the first screen, then the first screen with restored state. No alert, no branding moment |
| First run | [HIG] Optional, short, interactive onboarding after launch completes; splash screen (if any) at its start |
| Permissions | [HIG] In onboarding only if the app cannot function without them; otherwise when the feature is first used |
| Sign-in | [HIG] As late as possible; only if core functionality needs an account |
| Rating or purchase prompts | [HIG] After people have experienced the app; never at first launch or during onboarding |
| Setup and customization | [HIG] Postponed; good defaults first |

Source: https://developer.apple.com/design/human-interface-guidelines/launching, https://developer.apple.com/design/human-interface-guidelines/onboarding, https://developer.apple.com/design/human-interface-guidelines/managing-accounts, https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews

## Launching and launch screens

- [HIG] Launch as fast as possible; people may not want to wait more than a couple of seconds.
- [Req] iOS, iPadOS and tvOS display a launch screen the moment the app starts. macOS, visionOS and watchOS do not require one.
- [HIG] The launch screen exists only to make launch feel fast. It is not onboarding, a splash screen or artistic expression.
- [HIG] Make it nearly identical to the first screen (a solid color if the app starts with one), matching current orientation and appearance mode.
- [HIG] No text on the launch screen, even if the first screen has text: it is static and cannot be localized.
- [HIG] Do not advertise: no logos or branding unless they are a fixed part of the first screen; nothing resembling a splash or About screen.
- [HIG] Restore previous state on restart, down to details such as scroll position and window state and location.
- [HIG] iOS, iPadOS: launch in the device's current orientation; a landscape-only app must respond correctly whichever way the device is rotated.
- [HIG] tvOS: the launch screen is static; live-viewing apps may start playback after a few seconds of inactivity.
- [HIG] visionOS: consider launching in the Shared Space even for a fully immersive app, with a control to enter the Full Space.

Source: https://developer.apple.com/design/human-interface-guidelines/launching

## Onboarding

- [HIG] Ideal: none needed. If needed: fast, fun, optional, and after launch (never part of it).
- [HIG] Teach through interaction rather than instructional screens.
- [HIG] Consider contextual tips near the relevant interface (TipKit) instead of one up-front flow.
- [HIG] A required flow must be brief and must not expect memorization.
- [HIG] A separate tutorial is optional and skippable; once skipped do not show it again on later launches, but keep it findable (help, account or settings area).
- [HIG] Cover your own experience only; do not teach system or device basics.
- [HIG] A splash screen, if necessary, is shown briefly.
- [HIG] Do not make people wait for large downloads before they can start; bundle enough content.
- [HIG] Keep licensing details out of onboarding; let the App Store show agreements. If unavoidable, integrate them without disrupting the flow.
- [HIG] Postpone nonessential setup; rely on reasonable defaults.
- [HIG] Request access to private data in onboarding only when the app cannot function without it, and use the moment to explain the benefit; otherwise ask at first use of the feature. Permission-prompt rules (system alert, purpose strings, pre-alert screens) are on the Privacy page.

Source: https://developer.apple.com/design/human-interface-guidelines/onboarding, https://developer.apple.com/design/human-interface-guidelines/privacy

## Loading

- [HIG] Show something as soon as possible: placeholder text, graphics or animation that real content replaces. A blank screen reads as a fault.
- [HIG] Let people do other things while content loads in the background.
- [HIG] For unavoidably long loads, show something worthwhile (tips, hints) sized to the expected wait.
- [HIG] Download large assets in the background at nondisruptive times (Background Assets framework).
- [HIG] When loading takes more than a moment or two, show a progress indicator: determinate when duration is known, indeterminate when not (see `references/components-controls.md`).
- [HIG] Games may use a custom loading view that fits their style.
- [HIG] watchOS: avoid loading indicators as much as possible; if content needs a second or two, an indicator is still better than a blank screen.

Source: https://developer.apple.com/design/human-interface-guidelines/loading, https://developer.apple.com/design/human-interface-guidelines/progress-indicators

## Modality

Component choice (alert, sheet, popover, menu) is in `references/components-presentation.md`.

- [HIG] Present modally only for a clear benefit: critical information, confirming or modifying a recent action, a narrowly scoped task, or immersive focus.
- [HIG] Keep modal tasks simple, short and streamlined.
- [HIG] Avoid an "app within the app": if a modal needs subviews, provide a single path and no buttons that could be mistaken for the dismiss button.
- [HIG] Use a full-screen modal style for in-depth content or complex tasks (video, photos, camera, markup, editing).
- [HIG] Always provide an obvious way to dismiss, following platform convention: a button in the top toolbar or a swipe down on iOS, iPadOS and watchOS; a button in the main content view on macOS and tvOS.
- [HIG] If closing could lose user-generated content, confirm first and offer a way to keep it (on iOS, an action sheet with a save option), whether people use a gesture or a button.
- [HIG] Title the modal with its task, or add text that describes it.
- [HIG] Let people dismiss one modal before another appears. An alert may appear over anything, but never show more than one alert at a time.

Source: https://developer.apple.com/design/human-interface-guidelines/modality

## Entering data

- [HIG] Get information from the system (settings, or with permission location and calendar) instead of asking for it.
- [HIG] Be clear about what is needed: a prompt in the field ("username@company.com") or an introductory label; prefill reasonable defaults.
- [HIG] Use a secure text-entry field for sensitive data. tvOS can obscure digits in a digit entry view.
- [HIG] Never prepopulate a password field; ask for the password or use biometric or keychain authentication.
- [HIG] Offer choices (picker, menu, selection control) instead of typing where possible.
- [HIG] Accept drag and drop and paste as input.
- [HIG] Validate dynamically, as soon as values are entered, so errors are fixed immediately; use number formatters for numeric fields.
- [HIG] Make required data obvious: for example enable Next or Continue only after the required fields are filled.
- [HIG] Error messages sit next to the problem, do not blame, and say how to fix it; hints say what to do rather than what not to do (Writing page).
- [HIG] macOS (including iOS and iPadOS apps running on a Mac): consider expansion tooltips for clipped field text.

Source: https://developer.apple.com/design/human-interface-guidelines/entering-data, https://developer.apple.com/design/human-interface-guidelines/writing

## Settings

- [HIG] Choose defaults that give most people the best experience, so nobody has to adjust anything first.
- [HIG] Minimize the number of settings.
- [HIG] Do not ask in settings for things you can detect (connected controller, Dark Mode).
- [HIG] Respect systemwide settings and do not duplicate them in the app (accessibility accommodations, scrolling behaviour, authentication methods). The Dark Mode page likewise advises against an app-specific appearance setting.
- [HIG] General, rarely changed options go in the app's settings area. Task-specific options (show or hide parts of a view, reorder, filter) go in the screen they affect.
- [HIG] Put only the most rarely changed options in the system Settings app; consider a button that opens them directly.
- [HIG] Make settings reachable in expected ways: Command-Comma with a hardware keyboard; Esc in games.

| Platform | Rules |
|---|---|
| macOS | [HIG] Provide a Settings item in the App menu (document-level options in the File menu); no settings button in the window toolbar. Settings window: minimize and maximize dimmed; noncustomizable toolbar that always shows the active pane; window title is the current pane name ("App Name Settings" if there is one pane); reopen on the last viewed pane. |
| watchOS | [Req] Apps cannot add custom settings to the system Settings app. [HIG] Put a few essential options at the bottom of the main view or in a More menu. |
| iOS, iPadOS, tvOS, visionOS | No additional considerations. |

Source: https://developer.apple.com/design/human-interface-guidelines/settings, https://developer.apple.com/design/human-interface-guidelines/dark-mode

## Managing accounts

- [HIG] Require an account only if core functionality needs it; otherwise let people use the app without one.
- [HIG] Delay sign-in as long as possible; let people see value first (browse before buying).
- [HIG] Explain the benefits of an account and how to sign up, in the sign-in view.
- [HIG] If you do not use Sign in with Apple on iOS, iPadOS, macOS or visionOS, prefer passkeys. If passwords remain, add two-factor authentication.
- [HIG] Name the authentication method on the button ("Sign In with Face ID", not "Sign In") and mention only methods available on the current device.
- [HIG] Do not add an in-app opt-in setting for biometric authentication; that is a system-level choice.
- [HIG] Do not use the word "passcode" for account authentication.
- [Req] If the app lets people create an account, it must also let them delete it (not merely deactivate it). If deletion cannot happen in the app, provide a direct, easy-to-find link to the web page where it can; do not bury it in policy pages. Follow regional legal requirements.
- [Req] Account deletion must be supported even when the subscription was not bought through the app. With Sign in with Apple, revoke tokens on deletion (developer note on the page).
- [HIG] Keep in-app and web deletion flows equally simple; consider scheduled deletion alongside immediate deletion; say when deletion will complete and notify when done; explain that subscription billing continues until cancelled.
- [HIG] tvOS: ask for minimal input; prefer sign-in via another device; for a shared account do not ask people to pick a profile each time; with system-level TV provider sign-in, avoid an in-app sign-out option.
- [HIG] watchOS: use iCloud Keychain sync for autofill of names and passwords.

Source: https://developer.apple.com/design/human-interface-guidelines/managing-accounts

## Managing notifications

- [Req] Permission is required before sending any notification; people can change the decision in Settings.
- [Req] Every noncommunication notification needs a system interruption level. Critical notifications require an entitlement.

| Interruption level | Meaning | Overrides scheduled delivery | Breaks through Focus | Overrides Ring/Silent |
|---|---|---|---|---|
| Passive | View at leisure | No | No | No |
| Active (default) | Nice to know on arrival | No | No | No |
| Time Sensitive | Directly affects the person, needs immediate attention | Yes | Yes | No |
| Critical | Urgent health and safety; extremely rare | Yes | Yes | Yes |

- [HIG] Represent urgency honestly; inflated levels lead people to turn notifications off.
- [HIG] Time Sensitive is only for events happening now or within an hour.
- [Req] No marketing or promotional notifications unless people explicitly agreed; get permission through an interface that describes the content and offers a clear opt in or out.
- [Req] Never send marketing with the Time Sensitive level.
- [Req] Provide an in-app settings screen where people can change their notification choices.
- [HIG] Communication notifications (calls, messages) adopt SiriKit intents so the sender determines delivery.
- [HIG] watchOS: iPhone notification settings apply to the watch app by default.

Content and badge rules: `references/components-content.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/managing-notifications

## Searching

- [HIG] If search matters, give it a primary position (bottom toolbar, or a dedicated tab).
- [HIG] Aim for a single place to search all app content; a local filter within a distinct section is still useful.
- [HIG] Always show the current scope (placeholder text, scope control or title).
- [HIG] Offer suggestions: recent searches before typing, predictions while typing.
- [HIG] Consider privacy before showing search history, and provide a way to clear it.
- [HIG] Make content searchable in Spotlight (iOS, iPadOS, macOS); prefer the system open and save views; provide Quick Look generators for custom file types.

Placement per platform: `references/components-navigation.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/searching

## Going full screen

- [Req] Full-screen modes exist on iPhone, iPad and Mac. Not supported in tvOS or watchOS (apps already fill the screen) or visionOS (immersion instead).
- [HIG] Offer full screen for games, media viewing and in-depth tasks that benefit from fewer distractions.
- [HIG] Adjust layout subtly if needed, but do not programmatically resize the window.
- [HIG] Keep essential controls available or easy to reveal (playback controls).
- [HIG] Hide toolbars and navigation controls only while content is the focus, and restore them with a familiar action: tap, swipe down, or moving the pointer to the top.
- [HIG] Except in games, let people reveal the Dock in iPadOS and macOS.
- [HIG] Let people choose when to enter and when to exit; do not exit automatically when an activity ends. Pause and resume where they left off when they switch away.
- [HIG] iOS, iPadOS: keep the default Home indicator behaviour; defer system edge gestures (two swipes to exit) only if accidental exits are a real problem.
- [HIG] macOS: use the system full-screen support (handles the camera housing); entry via the window's Enter Full Screen button, View menu item or Control-Command-F; no custom window-mode menu; games do not change the display mode.

Source: https://developer.apple.com/design/human-interface-guidelines/going-full-screen

## Offering help and tips

- [HIG] Tie help to the exact task in progress and make it easy to dismiss or ignore.
- [HIG] Match terms and images to the platform and input in use: no "click" on iPhone, no "tap" on Mac, no game controller art when the Siri Remote is in use.
- [HIG] Do not explain how standard components work; explain what they do in your app.
- [HIG] Tips: for simple features (more than three actions is too complex for a tip); one or two sentences; action-oriented; never promotional. Popover tips preserve content flow; inline tips keep surrounding information visible.
- [HIG] Use eligibility rules so a tip reaches only people who can benefit, and limit frequency when there are several tips (for example one every 24 hours).
- [HIG] Tooltips (macOS, visionOS, and iPhone or iPad apps on a Mac): describe only the control under the pointer; start with a verb; do not repeat the control's name; at most 60 to 75 characters; sentence case; no ending punctuation.

Source: https://developer.apple.com/design/human-interface-guidelines/offering-help

## Ratings and reviews

- [HIG] Ask only after demonstrated engagement (a completed level or significant task); never at first launch or during onboarding.
- [HIG] Do not interrupt a task or gameplay; pick natural pauses.
- [HIG] Do not pester: leave at least a week or two between requests and wait for further engagement.
- [HIG] Prefer the system-provided prompt (iOS, iPadOS, macOS; `RequestReviewAction`).
- [Req] The system limits the prompt to three displays per app in a 365-day period, and people can turn the prompts off for all apps; a request may therefore show nothing.

Source: https://developer.apple.com/design/human-interface-guidelines/ratings-and-reviews

## Collaboration and sharing

- [HIG] Put the Share button somewhere convenient such as the toolbar; use the system share sheet or sharing popover (SwiftUI `ShareLink`).
- [HIG] Summarize sharing permissions in a short phrase ("Only invited people can edit") and keep custom sharing options few and grouped.
- [HIG] Show the system Collaboration button prominently once collaboration starts, next to the Share button; add custom actions to its popover only if essential.
- [HIG] Activity view rules: `references/components-presentation.md`. Not available in tvOS.

Source: https://developer.apple.com/design/human-interface-guidelines/collaboration-and-sharing

## Other pattern pages

Not summarized here; fetch the page when the task needs it: Charting data, Live-viewing apps, Multitasking, Playing audio, Playing haptics, Playing video, Printing, Workouts. Feedback, undo, drag and drop and file management are in `references/patterns-interaction.md`.

Source: https://developer.apple.com/design/human-interface-guidelines/patterns

## Common mistakes

| Mistake | Fix |
|---|---|
| Launch screen with logo, tagline, version text or a spinner | Static copy of the first screen, no text, no branding |
| Custom animated splash that delays the first screen | Launch straight into content; any splash belongs briefly at the start of onboarding |
| Multi-page carousel that must be swiped through before use | Interactive, skippable, or contextual tips |
| Tutorial shown again every launch after being skipped | Show once; keep it findable in help or settings |
| All permission prompts fired at first launch | Ask at first use of each feature, unless the app cannot function without it |
| Login wall before any content | Defer sign-in until an action needs it |
| Account creation without in-app deletion or a direct deletion link | Add deletion (not just deactivation) |
| Generic "Sign In" button that triggers Face ID; mentioning Face ID on a device without it | Name the method; check device capability |
| Prefilled or plain-text password field | Secure field, empty |
| Form that reports all errors only on submit | Validate as values are entered; message next to the field |
| Blank screen with a centered spinner while everything loads | Placeholders and progressive content; determinate progress when measurable |
| In-app Dark Mode or text-size switch duplicating system settings | Follow the system setting |
| View options (sort, filter) buried in a settings screen | Put task-specific options in the task |
| Modal flow with its own deep navigation and several close-like buttons | Single path, one obvious dismiss control |
| Dismissing an edited modal silently discards work | Confirm and offer save |
| Rating prompt on first launch, in onboarding, or mid-task; custom rating dialog | System prompt after engagement, at a natural break |
| Marketing push sent without opt-in, or marked Time Sensitive | Explicit opt-in; never Time Sensitive; in-app notification settings |
| macOS gear button in the toolbar opening settings | App menu Settings item (Command-Comma) |
| Auto-exiting full screen when playback ends; resizing the window in code | People choose when to exit; adapt layout only |
