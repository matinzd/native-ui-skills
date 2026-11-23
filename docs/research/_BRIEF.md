# Shared research brief (read first)

Project: build `apple-hig`, an Agent Skill (agentskills.io spec) that helps AI coding agents design, implement,
review and adapt native Apple-platform UIs per Apple's Human Interface Guidelines. You are one of six parallel
research workstreams. Today is 2026-11-23. Your output feeds the lead engineer who will write the skill.

## Network facts (verified by the lead)
- `curl` works for developer.apple.com. HIG pages are JS-rendered, so fetch the JSON instead:
  - HIG page:  https://developer.apple.com/tutorials/data/design/human-interface-guidelines/<slug>.json
    (index/TOC: .../human-interface-guidelines.json ; e.g. layout.json, typography.json, tab-bars.json)
  - API docs:  https://developer.apple.com/tutorials/data/documentation/swiftui/<symbol>.json (lowercase path,
    e.g. swiftui/navigationsplitview.json, uikit/uifontmetrics.json)
  Parse with python3 (`-I` flag) / jq to extract text; the JSON is DocC render JSON (primaryContentSections, abstract,
  topicSections, metadata.platforms with introducedAt / deprecated).
- raw.githubusercontent.com works (file contents of public repos). github.com HTML and api.github.com are blocked by proxy.
- agentskills.io, cursor.com, developers.openai.com are blocked for curl. The spec source is at
  https://raw.githubusercontent.com/agentskills/agentskills/main/ (try docs/specification.mdx and neighbours).
  code.claude.com/docs works. Your WebSearch/WebFetch tools (if you have them) may reach hosts curl cannot - try them.
- Put any downloads/scratch in /tmp/claude-0/-home-user-apple-hig-skill/4b8f6fc4-b934-5d7d-9f48-9d6e78d71918/scratchpad/<your-name>/ , never in the repo.

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
