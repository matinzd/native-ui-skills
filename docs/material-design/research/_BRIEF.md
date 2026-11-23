# Shared research brief: material-design skill

> The brief given to the research agents on 2026-11-23, kept for transparency about method.

Project: build `material-design`, a second Agent Skill in this repository (next to `skills/apple-hig/`). It helps AI
coding agents design, implement, review and adapt Android interfaces per Google's Material Design 3 guidelines and
Android's design and quality guidance, in Jetpack Compose first and Views (Material Components for Android) second.
Read `skills/apple-hig/SKILL.md` and `CONTRIBUTING.md` first: the new skill mirrors that structure, tag vocabulary
and honesty standard. Today is 2026-11-23. You are one of several parallel research workstreams.

## Sources, in priority order

1. Material Design 3: https://m3.material.io/ (guidelines, specs, accessibility tabs of each component and foundation)
2. Android Developers design and UI docs: https://developer.android.com/design , /develop/ui/compose , /develop/ui/views ,
   /guide/topics/large-screens , /docs/quality-guidelines , /training/wearables , /design/ui/tv , /develop/xr
3. Compose Material 3 API: https://developer.android.com/reference/kotlin/androidx/compose/material3/package-summary and the
   public API file https://raw.githubusercontent.com/androidx/androidx/androidx-main/compose/material3/material3/api/current.txt
   (and the adaptive libraries under compose/material3/adaptive/...); release notes at
   https://developer.android.com/jetpack/androidx/releases/compose-material3
4. Material Components for Android (Views): https://raw.githubusercontent.com/material-components/material-components-android/master/docs/...

## Network facts (verified by the lead)

- m3.material.io is reachable but rendered by JavaScript: plain curl returns an empty shell. Render pages with the
  pre-installed Chromium via this helper (prints the page's visible text):
  `node /tmp/claude-0/-home-user-apple-hig-skill/4b8f6fc4-b934-5d7d-9f48-9d6e78d71918/scratchpad/m3/render.js <url> <out.txt>`  (takes ~15 s per page; run several in parallel with `&` and `wait`, at most 4 at a time)
  Component pages have sub-pages: /components/<name>/overview , /specs , /guidelines , /accessibility. The site map is at
  https://m3.material.io/ (navigation) - discover exact slugs by rendering the hub pages, do not guess.
- developer.android.com works with curl (large HTML; strip tags with python3 -I, or use the render helper).
- raw.githubusercontent.com works. github.com HTML, api.github.com, android.googlesource.com and dl.google.com are blocked.
- Keep downloads and scratch files in /tmp/claude-0/-home-user-apple-hig-skill/4b8f6fc4-b934-5d7d-9f48-9d6e78d71918/scratchpad/<your-name>/ , never in the repository.

## Rules

- Never invent APIs, numbers, or guideline statements. Every substantive claim needs a source URL.
- Tag each claim: [V] = you fetched the source in this session and it says this; [M] = from memory, not verified.
- Distinguish: requirement (Google Play policy / core app quality requirement the docs call required, API contract,
  fixed platform behaviour), Material or Android recommendation, community convention. Most Material guidance is
  recommendation; note the exact wording strength ("should", "must", "don't").
- Record API status from the source: stable vs experimental (`@ExperimentalMaterial3Api`, `@ExperimentalMaterial3ExpressiveApi`),
  the library version that introduced it where the release notes say so, and deprecations.
- Record what is current: Material 3 Expressive, current Android version and API level, current Compose BOM / material3
  version, as the sources state them today. Flag common lore that is stale (Material 2 habits, bottom navigation naming,
  old 56dp/48dp numbers, elevation overlays, etc.) - but only where you verified what the current guidance says.
- Paraphrase; do not copy Google's prose at length (short quotes for exact numbers and wording are fine). Material
  guidelines are licensed by Google; record the licence statement you find on m3.material.io and developer.android.com.
- Write ONLY your own deliverable file (path given in your task). Do not touch other files or run git.
- Keep the deliverable dense and structured (tables and bullets). Final reply to the lead: a summary of at most 25 lines
  with the most decision-relevant findings, anything you could not verify, and contradictions with common lore.
