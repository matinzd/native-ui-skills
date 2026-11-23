# Shared research brief

> The brief given to the six research agents on 2026-11-23, kept for transparency about method.

Project: build `apple-hig`, an Agent Skill (agentskills.io spec) that helps AI coding agents design, implement,
review and adapt native Apple-platform UIs per Apple's Human Interface Guidelines. You are one of six parallel
research workstreams. Today is 2026-11-23. Your output feeds the lead engineer who will write the skill.

## Network facts

- `curl` works for developer.apple.com. HIG pages are JS-rendered, so fetch the JSON instead:
  - HIG page: https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json
  - API docs: https://developer.apple.com/tutorials/data/documentation/swiftui/<symbol>.json (lowercase path)
- Some hosts were unreachable from the build environment (agentskills.io, cursor.com, developers.openai.com); the
  specification was read from its source repository instead.
- Keep downloads and scratch files out of the repository.

## Rules
- Never invent Apple APIs, numbers, or HIG statements. Every substantive claim needs a source URL.
- Tag each claim: [V] = you fetched the source in this session and it says this; [M] = from memory/secondary source, not verified.
- Distinguish: hard requirement (App Review / API contract / HIG "must"), HIG recommendation, community convention.
- Record API availability (introduced OS version, deprecations) from metadata, not memory.
- Note what the *current* HIG says (it changes; e.g. Liquid Glass era redesign) and flag anything that looks stale in common lore.
- Paraphrase; do not copy Apple's prose at length (short quotes for exact numbers/wording are fine).
- Write ONLY your own deliverable file (path given in your task). Do not touch other files or run git.
- Keep the deliverable dense and structured (tables/bullets), at most ~450 lines. Final reply to the lead: a <=25-line summary
  with the most decision-relevant findings, anything you could not verify, and contradictions with common lore.
