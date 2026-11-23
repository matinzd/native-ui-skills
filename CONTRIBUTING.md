# Contributing and content conventions

This repository ships one Agent Skill per platform under `skills/` (`apple-hig`, `material-design`). Everything
an agent loads lives in a skill's directory; research notes, evals and repo tooling live outside and are not
installed. Skills do not link to each other's files: each must work when installed alone.

## Ground rules

1. **The official documentation is the source of truth.** Verify a claim against it before adding it.
   - Apple: both the HIG and the API reference serve machine-readable JSON:
     `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json` and
     `https://developer.apple.com/tutorials/data/documentation/<framework>/<symbol>.json`
     (`metadata.platforms` carries `introducedAt` / `deprecatedAt`).
   - Material and Android: `https://m3.material.io/` is rendered by JavaScript, so read it in a browser or render
     it headlessly; `https://developer.android.com/` serves plain HTML; the Compose Material 3 public API is the
     signature file `compose/material3/material3/api/current.txt` in the `androidx/androidx` repository.
2. **Paraphrase and link; never copy the vendor's prose.** Short factual values (a point size, a contrast ratio) are fine.
   Do not copy content from other skills or repositories either.
3. **Never invent** APIs, numbers or guidelines. If something could not be verified, either leave it out or tag it
   `[Unverified]`.
4. **Label the strength of every rule** with one of the tags below.

## Rule tags

| Tag | Meaning |
|-----|---------|
| `[Req]` | Something the platform owner states as mandatory ("must" wording, or an obligation the guidance says is enforced). Rare. |
| `[HIG]` | `apple-hig` only: recommendation stated in Apple's Human Interface Guidelines. Most guidance is this. |
| `[MD]` | `material-design` only: recommendation stated in Material Design or Android design guidance. Most guidance is this. |
| `[API]` | Documentation or platform fact: availability, deprecation, fixed system behaviour, "not supported on this platform". |
| `[Conv]` | Convention, interpretation, or this skill's own working rule that the official guidance does not state. |
| `[Unverified]` | Could not be confirmed against the official documentation. Use sparingly. |

## Reference file format (`skills/<skill>/references/*.md`)

- File name: `<group>-<topic>.md`, group is one of `foundations`, `components`, `patterns`, `platforms`,
  `accessibility`, `implementation`, `review`. Flat directory, no subfolders.
- Line 1: `# Title`. Then a one-line scope statement, then
  `Verified: YYYY-MM-DD against the sources linked in each section (SDK cycle: OS NN).`
- Files over 100 lines start with a `## Contents` list. Target 120-250 lines; hard cap 300 lines and 30 KB. Split rather than grow.
- One `##` section per topic. Each section ends with `Source: <official page URL>` (one or more), for example
  `https://developer.apple.com/design/human-interface-guidelines/<slug>` or
  `https://m3.material.io/components/<name>/guidelines`.
- Write rules as short imperative bullets, each starting with a tag (table rows need no tag): `- [HIG] Prefer a tab bar for top-level ...`.
- Put platform differences in a compact table when more than two platforms differ.
- Mark era-dependent guidance explicitly, for example `(OS 26+, Liquid Glass)` or `(Material 3 Expressive)`;
  give API availability as `iOS 17+` or as the library version and stability (`material3 1.4+, experimental`),
  and never guess it.
- End with a `## Common mistakes` section (mistake -> fix) when the topic has them.
- Cross-reference other skill files by skill-root path in backticks, for example `references/platforms-ios.md`.
  Every reference file must also be linked directly from `SKILL.md`.
- Plain Markdown, ASCII punctuation, no HTML, no images, no emoji.

## Code examples

- State minimum OS versions (Swift) or library versions and experimental opt-ins (Kotlin) in a comment at the top. Use only APIs whose spelling and availability were checked
  in the official API reference. There is no requirement that CI compiles them, so keep them conservative and say so
  when something could not be compiled.

## Before you commit

```bash
python3 tools/validate_skill.py
```
