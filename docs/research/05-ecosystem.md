# 05 — Ecosystem and competitive analysis (Agent 5)

> Historical research notes from 2026-11-23. They record what each workstream found before the skill was written
> and are not maintained. Where they differ from `skills/apple-hig/`, the skill is correct: several facts here
> were corrected during writing and review (see `docs/validation.md`).

Date: 2026-11-23. Method: GitHub repository/code search through `gh api search/*` (worked), shallow `git clone`
of 23 public repos into the scratchpad and reading their files, `raw.githubusercontent.com` for single files,
Apple DocC JSON for spot checks.

Tags: **[V]** = I read the file / API response in this session. **[M]** = memory or secondary source, not verified.
Star counts and push dates are from the GitHub search API on 2026-11-23 [V] and will drift.

Not reachable in this session (so nothing below relies on them): `skills.sh`, `www.apple.com` (legal pages),
`tessl.io`, `api.github.com/repos/*` (only `search/*` worked). Install counts on skills.sh are therefore unknown.

---

## 0. Headline findings

1. **The space is crowded, and our exact scope already exists.** At least six independent repos ship a skill
   literally named `apple-hig`; GitHub code search returns 1,018 `SKILL.md` hits for `"name: apple-hig"` [V].
   The closest competitor, `AyushRajSinghParihar/apple-human-interface-skills`, has the same four verbs we plan
   (design / implement / review / adapt), 166 eval cases, a published benchmark, and drift CI [V].
2. **Most of the field bundles Apple's text.** The two most-starred HIG skills (`dickwu`, `justinwetch`) and
   `raintree` ship Apple's HIG prose verbatim or near-verbatim and say so in their own notices [V]. One repo
   (`ehmo`) commits a compiled `Apple_HIG.pdf` [V]. Only two repos I read deliberately avoid this
   (`Sunwood-ai-labs` links only; `allexp1` paraphrases) [V].
3. **Common lore that current Apple pages contradict** (lead: verify in the HIG workstreams before use):
   - "44 pt is the minimum tap target." The current HIG Accessibility page lists 44x44 pt as the *default*
     control size for iOS/iPadOS and 28x28 pt as the *minimum*; macOS 28/20, tvOS 66/56, visionOS 60/28,
     watchOS 44/28 [V: https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json].
     `ehmo`, `alirezarezvani`, `twostraws`, `s1gmamale1` all state 44 pt as a hard minimum [V].
   - "Clarity, deference, depth are the HIG principles." The HIG now has a `design-principles` page with eight
     headings: Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight
     [V: .../human-interface-guidelines/design-principles.json]. `s1gmamale1` and `raintree` still lead with the old triad [V].
   - `navigation-bars` no longer resolves (HTTP 404 on the JSON) [V]; `AyushRajSinghParihar` says it now points
     to Toolbars [V in that repo, not independently verified against Apple].
   - A `designing-for-iphone-duo` HIG page exists (a folding iPhone with two displays) [V: .../designing-for-iphone-duo.json].
     Skills updated since ~Oct 2026 cover it; older ones do not.
   - Several repos assert iOS 27 / Xcode 27 / Swift 6.4 are current (`twostraws`, `AvdLee`, `allexp1`,
     `heyparsadev`) [V that they say it; **not** verified against Apple by me — treat as [M] until the API workstream confirms].
4. **Apple reportedly ships its own Agent Skills inside Xcode 27** (`swiftui-specialist`, `swiftui-whats-new-27`,
   `uikit-app-modernization`, ...), redistributed without a licence at `superagents-lab/xcode27-skills` [V that the
   repo exists and claims Apple authorship; the Apple origin itself is [M]]. If true, our skill should defer to
   them for SwiftUI code idiom and stay on design/HIG judgement.
5. **Real gaps remain**: nobody combines (a) no bundled Apple prose, (b) requirement-vs-recommendation labels on
   every rule, (c) a finding taxonomy with severity + source URL + evidence type, (d) OS-version/deployment-target
   awareness, (e) a small context footprint, and (f) honest "verified / not verified" reporting. Pieces exist
   in different repos; no single skill has all of them.

---

## 1. Repositories read

### 1.1 Apple HIG skills (primary competitors)

| # | Repo | Stars / last push | Licence | Shape |
|---|---|---|---|---|
| A | https://github.com/dickwu/apple-design-skill | 3,751 / 2026-11-13 | **None** (no LICENSE file; README says Apple text "reproduced") [V] | 1 skill `apple-design`; SKILL.md 436 lines / 4.3k words; 124 `references/hig/*.md`; `scripts/pull-hig.mjs` |
| B | https://github.com/justinwetch/HIGAgentSkills | 844 / 2026-10-17 | MIT + NOTICE excluding Apple material [V] | 1 skill `apple-hig`; SKILL.md 170 lines; 157 refs (~96k words); `routing-index.md`; 20 Python scripts; 2 test files |
| C | https://github.com/ehmo/platform-design-skills | 651 / 2026-03-19 | MIT [V] | 8 skills (ios, ipados, macos, watchos, tvos, visionos, android, web); each SKILL.md 370–1,450 lines |
| D | https://github.com/raintree-technology/apple-hig-skills (aka `hig-doctor`) | n/a in my search / 2026-11-02 | MIT; README says reference text is (c) Apple [V] | 14 skills + audit plugin; SKILL.md 68–133 lines each; ~156 refs; CLI + MCP server + CI |
| E | https://github.com/AyushRajSinghParihar/apple-human-interface-skills | 30 / 2026-11-10 | MIT; Apple docs/media excluded [V] | 1 skill `apple-hig` (99-line root) + 13 family subskills + 158 topic procedures + 158 source guides; 166 eval cases; drift + validate CI |
| F | https://github.com/ebuntario/apple-hig | 5 / 2026-04-21 | MIT [V] | 1 skill `apple-hig`; SKILL.md 222 lines; 68 refs in 6 folders; 3 checklists; VERSION + CHANGELOG |
| G | https://github.com/allexp1/apple-hig | 4 / 2026-10-19 | MIT + detailed NOTICE [V] | 1 skill `apple-hig` v2.0.0; SKILL.md 175 lines but 3.7k words; 10 refs; `.living/` update protocol |
| H | https://github.com/Sunwood-ai-labs/design-with-apple-hig | 4 / 2026-08-01 | MIT [V] | 1 skill; SKILL.md 89 lines; 6 refs (source map, routing, rubric, verification loop); fetch + validate scripts |
| I | https://github.com/s1gmamale1/apple-design-skills | 44 / 2026-05-25 | MIT file (API reports NOASSERTION) [V] | 9 skills (hub + 8 children), 31–73 lines each |
| J | https://github.com/alirezarezvani/claude-skills (`product-team/apple-hig-expert`) | large multi-skill repo / skill dated 2026-06-11 | MIT (frontmatter) [V] | 1 skill, 108 lines; `hig_checker.py` (contrast, tap target, 100-point score) |
| K | https://github.com/ykswang/apple-hig-skill, https://github.com/mr8lu/apple-design-hig | 6 / 8 | **None** [V] | Distilled HIG + crawl/diff/verify tooling; mr8lu adds MCP server + sync workflow |
| L | https://github.com/CarlosZiegler/apple-hig-skills | 12 / 2026-10-27 | MIT [V] | 21 small skills (29–43 lines each) + refs |

Notes per repo (strengths are patterns, not text to reuse):

**A. dickwu/apple-design-skill** [V]
- Activation: long description listing artefact types (screenshots, mockups, Figma exports, PRs) and colloquial
  triggers ("review my design", "is this good UI"). Good coverage of how people actually ask.
- Strengths: five ordered review lenses with a default severity per lens (accessibility = Critical, platform
  conventions = High, ...); fixed report template (Summary / Critical / Improvements / Craft notes / What works /
  Platform notes); a code-audit reference listing what to grep for; a "heritage" file that explains *why* but is
  barred from overriding current pages; each reference carries the Apple URL and Apple's last-change date; a
  lookup table generated from Apple's own one-line page summaries.
- Weaknesses: references are Apple's wording, by its own description; no LICENSE; tvOS/visionOS/watchOS sections
  deliberately dropped; 4.3k-word SKILL.md; persona framing ("you are two people"); no evals, no validation.

**B. justinwetch/HIGAgentSkills** [V]
- Activation: names platforms, frameworks, task types; also claims to trigger for "any digital interface" even
  without Apple context (broad; risk of over-triggering).
- Strengths: four-tier routing index with per-file frontmatter (`topic`, `tier`, `platforms`, `triggers`,
  `related`) and a stdlib-only router script; strict rules to preserve recommendation strength and logical
  conditions (A-and-B vs A-or-B); "identify the conflict, do not invent a reconciliation"; dated source
  snapshots; published token measurements; opt-in "enforce" mode with two independent reviewers and a frozen
  check register that cannot be weakened to raise a score; NOTICE that separates MIT code from Apple material.
- Weaknesses: loads all 16 foundation files on *every* design or review task (~27k tokens by its own README);
  whole corpus ~163k tokens; reference bullets track Apple's sentences closely; instructs the agent to quote
  Apple clauses verbatim; heavy procedure (ledgers, hashes) that few users will run.

**C. ehmo/platform-design-skills** [V]
- Strengths: one skill per platform (clean platform separation); every rule has a correct/incorrect code pair
  and an impact level; rule IDs (`Rule 1.1`); Android and Web kept apart from Apple.
- Weaknesses: SKILL.md files of 1,000+ lines (over the spec's 500-line guidance); zero mentions of
  "Liquid Glass" in any of the eight skills; "must" language for the 44 pt target; includes non-HIG rules
  ("thumb zone") presented under an HIG banner; no per-rule source links; commits `Apple_HIG.pdf` (2.4 MB);
  last content change March 2026; no evals.

**D. raintree-technology/apple-hig-skills** [V]
- Activation: quoted trigger phrases plus realistic user complaints ("my colors look wrong in dark mode");
  cross-references to sibling skills.
- Strengths: 14 skills split by HIG section; a `hig-project-context` skill that writes a project context file the
  others read before asking questions; nightly drift workflow that hashes Apple's DocC JSON and opens a tracking
  issue; audit CLI moved from a 0–100 score to severity buckets with a `--fail-on` CI gate; changelog.
- Weaknesses: all 156 references are stamped "snapshot 2025-02-02" (pre-Liquid Glass; only 3 files mention it);
  the reference I opened (typography) is only Apple's bold headline sentences with no explanation or numbers;
  14 separately triggered skills compete for activation; skill versions frozen at 1.0.0 since Feb 2025 while
  tooling moved on.

**E. AyushRajSinghParihar/apple-human-interface-skills** [V] — closest to our plan
- Activation: third person, lists frameworks and component vocabulary, and names requests that must *not*
  start the skill (v1.1 changelog reports near-miss false starts went from 2/10 to 0/10).
- Strengths: tiny root (5.8 KB) → searchable topic index → one short procedure per topic → source guide;
  `key-numbers.md` with platform scope and "a minimum is a limit, not a comfortable default"; an
  implementation map from guides to API links with the instruction to check availability in SDK docs; explicit
  output contracts for Design / Implement / Review / Adapt; "report checks as passed, failed or not done";
  "missing evidence does not prove a defect"; stress evals for conflicting numbers, unverified APIs, and
  negative (backend) prompts with rubric + critical-error lists; with/without-skill benchmark that admits noise
  ("do not report a difference of one case as an improvement") and admits cost (about 6.7x input tokens);
  `/apple-hig:review` and `/apple-hig:adapt` commands plus a reviewer subagent; review-hash staleness checks.
- Weaknesses: 381 files / 2.7 MB installed; `.topics/` hidden-directory nesting of 158 sub-SKILL.md files is
  non-standard and may confuse hosts that scan for SKILL.md; topic procedures are dense, telegraphic prose
  (slashes, clipped grammar) that is hard for humans to audit; benchmark is single-run on one model/CLI;
  30 stars, single maintainer.

**F. ebuntario/apple-hig** [V]
- Strengths: every reference has `HIG source:` URL and `Last verified:` date; "common mistakes without this
  skill" section; final review checklist; three checklists as assets (accessibility, platform parity,
  pre-submission); uninstall script; SemVer + Keep-a-Changelog.
- Weaknesses: description orders the agent to "always run Phase 0 (ask targeting questions) before generating
  any code" — blocks autonomous agents and annoys users whose project already answers the questions;
  last verified April 2026 (before the June 2026 HIG changes); no evals or scripts.

**G. allexp1/apple-hig** [V]
- Strengths: the best NOTICE in the set (independence, trademark list, "original synthesis and paraphrase",
  values marked "derived" are the authors' own, MIT does not cover Apple's rights); "current to" statement
  with dates; a `.living/` folder (protocol, sources, hash of the original) for incremental updates.
- Weaknesses: mixes HIG with authors' psychology/philosophy interpretation (Fitts, Hick, Rams) — useful but
  easy to mistake for Apple guidance; 3.7k-word SKILL.md; very long description; `license` frontmatter used
  for a sentence rather than an identifier; many dated product facts I could not verify.

**H. Sunwood-ai-labs/design-with-apple-hig** [V] — best on epistemics
- Strengths: seven claim labels (`APPLE-HIG`, `APPLE-SDK`, `APPLE-RESOURCE`, `ACCESSIBILITY`, `OBSERVATION`,
  `AUDIT`, `HEURISTIC`); separates HIG (design guidance) from SDK docs (implementation fact) from App Review
  (distribution policy) from WCAG; "when Apple gives a principle without a number, do not invent one";
  "HIG-aligned" for Apple platforms vs "Apple-inspired" for web/Android, never "HIG-compliant"; states what a
  screenshot, source code, or a build can and cannot establish; finding fields `Finding, Severity, Evidence,
  Source, Impact, Fix, Verify`; any Critical finding means "not ship-ready" regardless of score; refuses to
  bundle a distilled corpus; repo validation script in CI.
- Weaknesses: depends on live fetches for every material claim (fails offline or behind a proxy, slow);
  ships almost no offline knowledge, so answers vary with network; orchestrates other skills by name; no evals;
  4 stars, last push August 2026.

**I. s1gmamale1/apple-design-skills** [V]
- Strengths: confidence labels on reference claims (`[observed]`, `[documented]`, `[inferred]`,
  `[speculative]`); hub-and-children routing; "restraint first" anti-slop framing; utility-vs-marketing surface axis.
- Weaknesses: mostly about making *web* pages look like apple.com; cites the pre-2026 triad as "the" HIG themes;
  hard 44 pt minimum; unsourced numbers (e.g. "springs <= 300ms"); includes "reverse-engineered backend
  architecture"; references a file path from the author's own project.

**J. alirezarezvani apple-hig-expert** [V]
- Strengths: short; ships a deterministic checker; "What + Why + How" finding phrasing; marks findings as
  tool-verified.
- Weaknesses: 100-point score with -10 per violation (false precision); WCAG contrast formula and 44 pt
  presented as HIG pass/fail; only 2–3 checks; copied into many aggregator repos (NVlabs/Skill2Env,
  borghei/Claude-Skills, ...) [V via code search], so stale copies circulate.

**K/L.** `ykswang`, `mr8lu`: no licence, distilled corpora, but useful tooling ideas (crawl → diff → verify,
manifest of Apple pages). `CarlosZiegler`: 21 micro-skills; same activation-competition problem as raintree.

### 1.2 SwiftUI / Apple-platform coding skills

| # | Repo | Stars / last push | Licence | Shape |
|---|---|---|---|---|
| M | https://github.com/twostraws/SwiftUI-Agent-Skill | 6,616 / 2026-10-26 | MIT [V] | 1 skill `swiftui-pro` v2.0.0; SKILL.md 122 lines; 12 refs totalling 501 lines |
| N | https://github.com/AvdLee/SwiftUI-Agent-Skill | 3,943 / 2026-11-06 | MIT [V] | `swiftui-expert-skill` v5.3.0; SKILL.md 158 lines; 33 refs (~10.4k lines); trace scripts + tests; maintainer skill |
| O | https://github.com/Dimillian/Skills | n/a / 2026-03-29 | MIT [V] | 16 skills incl. `swiftui-ui-patterns` (95 lines + 30 refs), `swiftui-liquid-glass`, `swiftui-view-refactor` |
| P | https://github.com/dpearson2699/swift-ios-skills | 1,313 / 2026-07-31 | **PolyForm Perimeter 1.0.0** (not OSI open source) [V] | ~80+ skills incl. `ios-accessibility` (354 lines), `swiftui-liquid-glass` |
| Q | https://github.com/rshankras/claude-code-apple-skills | 906 / 2026-11-09 | MIT [V] | ~150 skills; `ios/ui-review`, `macos/ui-review-tahoe`, `design/*` |
| R | https://github.com/superagents-lab/xcode27-skills | 372 / 2026-06-09 | **None**; README says content is Apple's and no licence is granted [V] | 7 skills "exported from Xcode 27" |
| S | https://github.com/heyparsadev/liquid-glass-skill | 15 / 2026-10-11 | MIT [V] | 1 skill v2.0.0; SKILL.md 165 lines; refs, patterns, 10 example screens, linter + test, 11 activation evals |

- **M. twostraws** [V]: smallest high-quality skill here. Patterns: a numbered review process mapped one-to-one
  to reference files; "report only genuine problems — do not nitpick or invent issues"; "during feature work,
  suggest unrelated modernization separately; do not apply it"; "check the project's deployment target before
  applying version-specific advice"; output format taught with one worked example and a prioritised summary;
  terse references (9–92 lines). Weaknesses: opinionated house rules mixed with requirements (one type per file);
  "Apple's minimum acceptable tap area is 44x44 ... strictly enforced" conflicts with the current table (§0);
  states iOS 27 as default target (time-sensitive); no source links; no evals.
- **N. AvdLee** [V]: patterns: workflows split by task (review / improve / implement); a topic router;
  `latest-apis.md` organised by deployment target ("When targeting iOS 17+ ...") with a soft- vs hard-deprecation
  policy; "only adopt Liquid Glass when explicitly requested"; "present performance optimizations as
  suggestions, not requirements"; a separate maintainer-only skill (`.agents/skills/update-swiftui-apis`) that
  refreshes the API list from Apple docs; plugin manifests for Claude, Codex, Cursor; release workflow.
  Weaknesses: scope creep (Instruments trace recording inside a SwiftUI skill); 10k lines of references;
  HIG treated in one line ("Follow Apple's Human Interface Guidelines").
- **O. Dimillian** [V]: example-driven component references; Codex `agents/openai.yaml` metadata. No update since
  March 2026; no HIG sourcing.
- **P. dpearson2699** [V]: thorough `ios-accessibility` (assistive tech by type, common mistakes, review
  checklist). The PolyForm Perimeter licence forbids competing use — do not derive from it.
- **Q. rshankras** [V]: two maintenance patterns worth copying: `last_verified` / `review_by` dates in
  frontmatter with a weekly workflow that opens one rollup issue per stale category; and an "API tripwire"
  script that checks every taught Apple symbol against a symbol list, created after a non-existent enum case
  shipped. Also `allowed-tools` in frontmatter.
- **R. xcode27-skills** [V repo; Apple origin [M]]: the skill body opens by declaring it supersedes model
  training. Very short SKILL.md (19–22 lines) whose reference list doubles as routing: each line says *when* to
  open the file. No licence — read for awareness only, do not copy.
- **S. heyparsadev** [V]: `compatibility` and `metadata.docs-verified` frontmatter stating which SDK the claims
  were checked against and which are beta; notes Liquid Glass APIs are not available on visionOS; pattern files
  + compilable example screens; a Python linter with a unit test; activation evals with positive and negative
  cases (`n4-coffee-shop-logo`, `n5-web-glassmorphism`) run five times each via `claude plugin eval`.

### 1.3 General design / review / accessibility skills and directories

| Repo | Licence | What to take |
|---|---|---|
| https://github.com/anthropics/skills (199k stars) — `frontend-design`, `skill-creator` | Per-skill `LICENSE.txt`; frontend-design and skill-creator are Apache-2.0 [V] | `frontend-design` is 71 lines with no references: proof that a short opinionated body works. `skill-creator` ships the eval toolchain (`run_eval.py`, `improve_description.py`, `quick_validate.py`, `package_skill.py`, grader/comparator agents, schemas) [V] — use it for our evals rather than inventing a format. |
| https://github.com/vercel-labs/agent-skills — `web-design-guidelines` v1.1.0 | No root LICENSE file found; README has a License section (not read) [V/unknown] | Rules bundled as one reference pinned to an upstream commit with a SHA-256 and a documented update procedure; "do not fetch rules from the network"; terse `file:line` findings; `argument-hint` metadata. |
| https://github.com/pbakaus/impeccable (115k stars) | Apache-2.0 + NOTICE [V] | One skill (~90 lines) exposing verbs (critique, audit, polish ...); generated copies per harness (`.claude`, `.cursor`, `.agents`, ...); deterministic detector engine with a large fixture/oracle test suite. Web-focused. |
| https://github.com/Community-Access/accessibility-agents (456 stars) | MIT [V] | 113 skills; WCAG 2.2 AA; a source-currency check script in CI; an "edit gate" hook. Web/document focused, little native Apple content. |
| https://github.com/VoltAgent/awesome-agent-skills (37k stars) | MIT [V] | Lists `ehmo/platform-design-skills`, `AvdLee/swiftui-expert-skill`, `raintree-technology/hig-doctor`, `MiniMax-AI/ios-application-dev` [V]. A target for listing once we ship. |
| Others seen, not read: `plugin87/ux-ui-agent-skills` (3.2k), `bergside/awesome-design-skills` (3.8k), `Leonxlnx/taste-skill` (120k), `skydashnet/material-design-3-ui-skill` (414), `Prisma-Labs-Dev/apple-skills` (359), `signerlabs/ShipSwift` (3.3k), `truongduy2611/app-store-preflight-skills` (1.4k), `mjmirza/app-store-compliance` (4.7k), `conorluddy/ios-simulator-skill` (1.3k), `mirzaaghazadeh/iphone-duo-skills` (338), `axiaoge2/Apple-Hig-Designer` (235) | from API | Existence and stars only [V]; contents [M]. |

Names from the task that were wrong or changed: `sickn33/antigravity-awesome-skills` now appears as
`sickn33/agentic-awesome-skills` (50k stars) in search [V]; `raintree-technology/apple-hig-skills` clones fine
but brands itself `hig-doctor` [V]; no dedicated "Apple Cursor rules" repo of note surfaced — the
`.cursor-plugin/plugin.json` manifest inside skill repos has replaced it [V in AvdLee, AyushRaj].

---

## 2. Patterns to adopt

Structure and context budget
- **Small root, routed references.** Root SKILL.md at or under ~150 lines (twostraws 122, Sunwood 89, AyushRaj
  99) with a reference list where each line says *when* to open the file (xcode27, twostraws). The spec
  recommends under 500 lines and under ~5,000 tokens for the body [V: agentskills specification.mdx lines 220–224].
- **Load on demand, never "always load 16 files".** Budget per task: one platform file + one to four topic
  files (Sunwood's stated bundle). Publish the measured token cost (justinwetch, AyushRaj).
- **Task-mode sections** with an explicit output contract per mode: design, implement, review, adapt
  (AyushRaj; AvdLee's per-task workflows).
- **One platform file per platform**; never flatten differences (ehmo, justinwetch "Distinguish platforms").
- **A single key-numbers table** with platform, scope, default vs minimum, and source link per row (AyushRaj).

Epistemics
- **Preserve recommendation strength**: keep must / prefer / consider / avoid as written; do not promote advice
  to a rule (justinwetch, Sunwood, AyushRaj all converge on this).
- **Separate source classes**: HIG guidance, SDK/API fact, App Review policy, WCAG, own heuristic (Sunwood).
- **Evidence limits by artefact**: say what a screenshot, static code, or a build can and cannot prove; report
  checks as passed / failed / not done (Sunwood, AyushRaj).
- **Do not invent violations; do not nitpick** (twostraws, AyushRaj).
- **Per-reference provenance header**: Apple URL + last-verified date (+ Apple's own change-log date) (ebuntario, dickwu).

Review output
- **Fixed finding schema**: Finding, Severity, Evidence, Source, Impact, Fix, Verify (Sunwood); ordered lenses
  with default severity (dickwu); one worked example of the output in SKILL.md (twostraws); prioritised summary last.
- **Severity buckets, not a numeric score**; any Critical blocks "ready" (raintree's move away from 0–100; Sunwood).
- **Scope discipline when editing code**: fix what was asked, list unrelated modernisation separately (twostraws, AvdLee).

Version awareness
- **Check the deployment target first**; organise version-specific guidance by "when targeting X+"; gate with
  availability checks; distinguish soft from hard deprecation (twostraws, AvdLee).
- **State what the skill is current to** in frontmatter metadata (`docs-verified`, snapshot date) (heyparsadev, AyushRaj).
- **Adopt new materials conservatively**: do not restyle to Liquid Glass unless asked or the target requires it (AvdLee).

Activation
- Third-person description; real user vocabulary (frameworks, component names, complaints); artefact types;
  **explicit non-triggers**; then test with positive and negative activation evals (AyushRaj, heyparsadev, raintree).

Maintenance
- Evals in the repo: a few stress cases (conflicting numbers, unverified API, negative/backend prompt) with
  rubric + critical-error list (AyushRaj), plus activation cases (heyparsadev); use `anthropics/skills`
  `skill-creator` tooling.
- Validation script in CI: frontmatter, link integrity, line limits, source-URL presence (Sunwood, AyushRaj, ebuntario lint).
- API-symbol tripwire against a verified list (rshankras); drift detection by hashing Apple's DocC JSON (raintree, AyushRaj).
- `review_by` dates and a staleness report (rshankras); CHANGELOG naming the Apple snapshot date per release (AyushRaj).
- NOTICE file separating our licence from Apple's rights (justinwetch, allexp1).

---

## 3. Gaps our skill can fill

| Gap | State of the field | Our move |
|---|---|---|
| No bundled Apple prose **and** useful offline | Corpus-bundlers (A, B, D, K) vs link-only (H, needs network) | Original, short rules + numbers with source links; works offline; optional live re-check |
| Requirement vs recommendation on every rule | Stated as a principle in B, E, H; not marked per rule anywhere | Tag each rule: `REQ-API`, `REQ-REVIEW` (App Review), `HIG-MUST`, `HIG-REC`, `CONVENTION`, `HEURISTIC` |
| Finding taxonomy | Severity exists (A, D, H); stable finding IDs/categories + source link + evidence type together do not | Stable category codes, severity definition, evidence type, source URL, verification status |
| Default-vs-minimum numbers | Only E reproduces the HIG's two-column tables; most others teach 44 pt as a hard floor | Number table with scope; reviewer flags below-minimum as defect, below-default as advisory |
| Platform detection from the project | D has a context file; F asks questions up front; most assume iOS | Detect from project files first (targets, SDK, deployment target, idiom), ask only if undecidable |
| OS-era awareness | Good for SwiftUI APIs (N, M); weak for *design* guidance across pre-26 / 26 / 27 | Era notes per topic keyed to deployment target; fallback guidance when targeting older OS |
| Honesty about verification | H, E say it; nobody ships per-claim verification status in references | `[verified YYYY-MM-DD]` / `[unverified]` per reference; skill tells agent to say "not checked" |
| Evals + validation in a small package | E has both but 381 files; S has activation evals only; most have none | A dozen evals + one validation script; publish results with caveats |
| UIKit / AppKit parity | Mostly SwiftUI-only code examples | API pointers for SwiftUI, UIKit, AppKit per rule where they differ |
| Adaptation between platforms | Only E names "adapt" as a mode | Dedicated adapt workflow (iPhone→iPad→Mac→visionOS; new foldable form factor) |
| Coexistence with Apple's own Xcode skills and SwiftUI skills | Nobody addresses it | State scope boundary: we own design judgement and HIG review; defer code idiom to those |

---

## 4. Pitfalls to avoid

- **Shipping Apple's text** (verbatim or sentence-by-sentence condensation) or Apple files (PDF, images, fonts,
  SF Symbols exports). Present in A, B, C, D, K.
- **Stale snapshots presented as current**: D is stamped Feb 2025; C has no Liquid Glass; F predates June 2026.
- **Folklore as requirement**: hard 44 pt minimum, "thumb zone", clarity/deference/depth as *the* principles,
  WCAG ratios labelled as HIG rules, invented spring durations.
- **Numeric compliance scores** (J's 100-point scale) and the word "compliant" — neither Apple nor a static
  read can certify it; prefer "aligned, with stated coverage".
- **Oversized bodies**: 1,000+ line SKILL.md (C), 3–4k-word SKILL.md (A, G), always-loaded foundations (B).
- **Many sibling skills** (D: 14, L: 21) that compete for activation and split context.
- **Mandatory question phase** before any work (F) — breaks headless/agentic use.
- **Over-broad triggers** ("any digital interface", B) — fires on web/back-end tasks; test with negatives.
- **Persona prompts and absolute language** ("you are...", "ALWAYS/NEVER") where a reason would do.
- **Hallucinated or beta APIs taught as stable** — the reason Q built its symbol tripwire.
- **Scope creep**: profiling, App Store marketing, backend speculation inside a design skill (N, I).
- **Claims of authority**: "authoritative" (B's description), or text saying the skill supersedes training (R).
  We are an independent summary; Apple's pages win.
- **Non-standard layouts** (hidden `.topics/` with nested SKILL.md, E) and `license` used as free text (G).
- **Depending on network at runtime** for correctness (H) — many agent sandboxes block developer.apple.com.
- **Unlicensed or restrictive sources**: A, K, R have no licence; P is PolyForm Perimeter. Do not derive from them.

---

## 5. Licensing and attribution guidance

What is established
- The HIG is Apple's copyrighted work: the HIG DocC JSON carries the notice "Copyright (c) 2026 Apple Inc. All
  rights reserved." and points to Apple's site terms
  [V: https://developer.apple.com/tutorials/data/design/human-interface-guidelines.json, `legalNotices`].
- I could not fetch Apple's website terms or trademark guidelines (host blocked). From memory [M]: the site
  terms allow personal, non-commercial viewing and forbid reproduction/redistribution without permission; the
  trademark guidelines allow referential use of Apple word marks to describe compatibility, forbid Apple logos
  and names that suggest endorsement, and ask for a trademark credit line. **Lead: re-check both pages
  (`apple.com/legal/internet-services/terms/site.html`, `apple.com/legal/intellectual-property/guidelinesfor3rdparties.html`)
  from an unrestricted network before release.** This is not legal advice.
- Third-party skill repos acknowledge the same boundary in their own notices (A, B, D, G) [V].

Safe practice for our repo
- **Do**: write original guidance in our own words and structure; state facts and numbers (sizes, ratios,
  counts) with their scope and a link to the Apple page; use page titles, API symbol names and section names as
  names; quote at most a short phrase where exact wording is the point, in quotation marks with a link.
- **Do not**: copy or lightly reword paragraphs or bullet lists; mirror a page's full heading-and-sentence
  skeleton; ship Apple images, diagrams, design templates, fonts (SF Pro, New York), SF Symbols artwork, or PDFs;
  ship a scraper whose output we commit. A fetch helper that reads Apple's page at run time for the user's own
  verification is a different matter, but keep fetched text out of the repo.
- **Do not copy from other skills**, including MIT ones: several contain Apple's text, so their MIT grant cannot
  cover it. Record ideas as patterns (as in this document) and write everything fresh.
- Keep a `docs/SOURCES.md` (or per-reference header) listing each Apple URL and the date we verified it.

Recommended licence: **MIT** for all original text and code. It is what most of the ecosystem uses (B, C, D, E,
F, G, H, M, N, O, Q, S) [V], is accepted by skill directories, and the spec has an optional `license` frontmatter
field. Apache-2.0 (used by `anthropics/skills` examples and `impeccable`) is a reasonable alternative if an
explicit patent grant and a formal NOTICE mechanism are wanted. Add a `NOTICE` file either way, and set
`license: MIT` in SKILL.md frontmatter.

Proposed NOTICE / README wording (original, adapt freely):

> This is an independent, community-maintained project. It is not affiliated with, authorized, sponsored, or
> endorsed by Apple Inc.
>
> Apple, iPhone, iPad, Mac, Apple Watch, Apple TV, Apple Vision Pro, iOS, iPadOS, macOS, watchOS, tvOS, visionOS,
> SwiftUI, UIKit, AppKit, Xcode, SF Symbols and Liquid Glass are trademarks of Apple Inc., used here only to
> identify the platforms and technologies this guidance is about.
>
> The guidance in this repository is original writing that summarizes and links to Apple's public Human
> Interface Guidelines and developer documentation. It does not reproduce Apple's text or artwork. Apple's
> documentation is the authoritative source and changes over time; where this project and Apple's current pages
> differ, follow Apple. Each reference lists the Apple pages it is based on and the date they were last checked.
>
> The MIT License covers this project's original text and code only. It grants no rights in Apple's trademarks,
> documentation, design resources, fonts, or symbols.

Also: no Apple logo or SF Symbols glyphs in the README or social image; avoid "official", "authoritative",
"compliant", "certified" in the description.

---

## 6. Naming-collision check: `apple-hig`

Findings [V]
- Skills whose frontmatter `name` is exactly `apple-hig`: `justinwetch/HIGAgentSkills` (844 stars),
  `AyushRajSinghParihar/apple-human-interface-skills`, `ebuntario/apple-hig`, `allexp1/apple-hig`,
  `ykswang/apple-hig-skill`, and a catalogue stub in `nexu-io/open-design` (109k-star repo) that points to
  raintree. Code search for `"name: apple-hig" filename:SKILL.md` reports 1,018 hits, mostly vendored copies
  inside app repos and aggregator mirrors.
- Near names: `apple-hig-expert` (alirezarezvani, widely mirrored), `apple-design` (dickwu, s1gmamale1),
  `hig-*` (raintree), `apple-design-hig` (mr8lu), `design-with-apple-hig` (Sunwood), `apple-hig-designer`.
- No single canonical owner of the name; the most-starred HIG skill is named `apple-design`, not `apple-hig`.
  skills.sh install counts could not be checked.

Does it matter?
- **Technically, yes, a little.** The spec requires `name` to equal the parent directory name
  [V: specification.mdx line 65], so two `apple-hig` skills cannot coexist in one skills directory
  (`~/.claude/skills/apple-hig`, `.agents/skills/apple-hig`); installing ours overwrites or is blocked by
  another. Installers that address `owner/repo --skill name` disambiguate at install time but not on disk.
  Plugin-namespaced installs (`plugin:skill`) avoid the clash.
- **For discovery, yes.** Searching "apple-hig skill" returns many results; the name alone will not identify us.
- **Legally, no new issue** beyond the trademark points in §5: the name is descriptive/referential and already
  in broad community use; keep the disclaimer.

Recommendation
- Keeping `apple-hig` is defensible (short, descriptive, matches what users type) **if** the repo name, README
  title and plugin namespace carry the distinguishing identity, and the README documents how to install beside
  another `apple-hig` (plugin namespace or rename the folder and `name` together).
- If the lead prefers to avoid the clash, pick a name nobody uses that still triggers well; candidates I did
  not find in search results: `apple-hig-review`-style names are taken (`art-si`), so consider a distinct
  suffix tied to our differentiator (for example `apple-hig-guide` or `hig-native-ui`) and check it with one
  code search before committing.
- Either way, do not rely on the name for activation: the description does that work.

---

## 7. Could not verify / open items for the lead

- skills.sh, tessl.io and apple.com legal pages were unreachable; install counts and exact legal wording are [M].
- Whether the `xcode27-skills` content is genuinely Apple-authored, and under what terms Xcode ships it.
- iOS 27 / Xcode 27.x / Swift 6.4 / release dates quoted by other skills — confirm from Apple metadata.
- `vercel-labs/agent-skills` licence (no root LICENSE file in the clone; README section not read).
- `dpearson2699`, `Dimillian`, `rshankras`, `impeccable`, `accessibility-agents`: frontmatter, structure and
  licence read; reference contents sampled only lightly.
- Star counts for repos not returned by my searches (raintree, Dimillian) are not recorded.
- The claim that `navigation-bars` now maps to Toolbars: only the 404 is verified.
