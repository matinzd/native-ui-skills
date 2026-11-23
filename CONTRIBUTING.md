# Contributing and content conventions

This repository ships one Agent Skill, `skills/apple-hig/`. Everything an agent loads lives in that directory;
research notes, evals and repo tooling live outside it and are not installed.

## Ground rules

1. **Apple's documentation is the source of truth.** Verify a claim against the HIG or the developer documentation
   before adding it. Both serve machine-readable JSON:
   - HIG page: `https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json`
   - API page: `https://developer.apple.com/tutorials/data/documentation/<framework>/<symbol>.json`
     (`metadata.platforms` carries `introducedAt` / `deprecatedAt`).
2. **Paraphrase and link; never copy Apple's prose.** Short factual values (a point size, a contrast ratio) are fine.
   Do not copy content from other skills or repositories either.
3. **Never invent** APIs, numbers or guidelines. If something could not be verified, either leave it out or tag it
   `[Unverified]`.
4. **Label the strength of every rule** with one of the tags below.

## Rule tags

| Tag | Meaning |
|-----|---------|
| `[Req]` | Something Apple states as mandatory ("must" wording, or an obligation the HIG says is enforced). Rare. |
| `[HIG]` | Recommendation stated in the HIG. Most guidance is this. |
| `[API]` | Documentation or platform fact: availability, deprecation, fixed system behaviour, "not supported on this platform". |
| `[Conv]` | Convention, interpretation, or this skill's own working rule that Apple does not state. |
| `[Unverified]` | Could not be confirmed against Apple's documentation. Use sparingly. |

## Reference file format (`skills/apple-hig/references/*.md`)

- File name: `<group>-<topic>.md`, group is one of `foundations`, `components`, `patterns`, `platforms`,
  `accessibility`, `implementation`, `review`. Flat directory, no subfolders.
- Line 1: `# Title`. Then a one-line scope statement, then
  `Verified: YYYY-MM-DD against the sources linked in each section (SDK cycle: OS NN).`
- Files over 100 lines start with a `## Contents` list. Target 120-250 lines; hard cap 300 lines and 30 KB. Split rather than grow.
- One `##` section per topic. Each section ends with `Source: <human HIG or documentation URL>` (one or more).
  Human HIG URLs look like `https://developer.apple.com/design/human-interface-guidelines/<slug>`.
- Write rules as short imperative bullets, each starting with a tag (table rows need no tag): `- [HIG] Prefer a tab bar for top-level ...`.
- Put platform differences in a compact table when more than two platforms differ.
- Mark era-dependent guidance explicitly, for example `(OS 26+, Liquid Glass)`; give API availability as
  `iOS 17+` and never guess it.
- End with a `## Common mistakes` section (mistake -> fix) when the topic has them.
- Cross-reference other skill files by skill-root path in backticks, for example `references/platforms-ios.md`.
  Every reference file must also be linked directly from `SKILL.md`.
- Plain Markdown, ASCII punctuation, no HTML, no images, no emoji.

## Swift examples

- State minimum OS versions in a comment at the top. Use only APIs whose spelling and availability were checked
  in the documentation JSON. There is no requirement that CI compiles them, so keep them conservative and say so
  when something could not be compiled.

## Before you commit

```bash
python3 tools/validate_skill.py
```
