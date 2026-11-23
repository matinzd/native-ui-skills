#!/usr/bin/env python3
"""Validate the apple-hig Agent Skill and the repository around it.

Standard library only. Exit status 0 when there are no errors, 1 otherwise.

    python3 tools/validate_skill.py            # offline checks
    python3 tools/validate_skill.py --online   # also check that cited Apple URLs still exist
    python3 tools/validate_skill.py --strict   # treat warnings as errors

Checks (E = error, W = warning):
  frontmatter   spec fields only, name/description/metadata constraints, name == directory      E
  budget        SKILL.md under 500 lines / ~5000 tokens; reference files under 300 lines        E/W
  links         every relative link and backticked skill path resolves inside the skill         E
  orphans       every file in references/, examples/, scripts/ is linked from SKILL.md          E
  provenance    each reference has a title, a "Verified: YYYY-MM-DD" line and Apple source URLs  E/W
  swift         code fences closed, brackets balanced, deprecated and made-up API deny-lists     E
  packaging     plugin.json / marketplace.json agree with the skill                             E
  evals         tests/evals JSON files match the expected schema and point at real files         E
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "apple-hig"
SKILL = ROOT / "skills" / SKILL_NAME
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
REFERENCE_GROUPS = ("foundations", "components", "patterns", "platforms", "accessibility", "implementation", "review")
RULE_TAGS = ("[Req]", "[HIG]", "[API]", "[Conv]", "[Unverified]")
STALE_AFTER_DAYS = 270

# Deprecated or discouraged spellings. They may appear in Swift code only when the same line, or one of the
# three lines before it, carries a marker showing the code is a "before" / "avoid" / fallback sample.
DEPRECATED = {
    r"\bNavigationView\b": "NavigationView (use NavigationStack or NavigationSplitView)",
    r"\.foregroundColor\(": "foregroundColor (use foregroundStyle)",
    r"\.cornerRadius\(": "cornerRadius (use clipShape)",
    r"\.tabItem\b": "tabItem (use Tab)",
    r"\bActionSheet\(": "ActionSheet (use confirmationDialog)",
    r"\bAlert\(title:": "Alert value (use alert(_:isPresented:actions:message:))",
    r"\.navigationBarHidden\(": "navigationBarHidden (use toolbar(.hidden, for:))",
    r"\.navigationBarTitle\(": "navigationBarTitle (use navigationTitle)",
    r"\.navigationBarItems\(": "navigationBarItems (use toolbar)",
    r"\.edgesIgnoringSafeArea\(": "edgesIgnoringSafeArea (use ignoresSafeArea)",
    r"\.accentColor\(": "accentColor modifier (use tint)",
    r"\bUIScreen\.main\b": "UIScreen.main (use the view's geometry or trait collection)",
}
MARKER = re.compile(r"avoid|deprecated|before|fallback|don't|do not|legacy|wrong|mistake|instead of|replace", re.I)

# Names that do not exist in SwiftUI. Evals use them as traps; shipped skill files must never present them.
FAKE_APIS = (
    "liquidGlassStyle", "hapticFeedback(", "navigationBarGlass", "minimumTapTarget", "tapTargetSize",
    "roundedCorners(", "adaptiveTabBar",
)
CLAUDE_ONLY = ("$ARGUMENTS", "${CLAUDE_", "!`")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: Path | str, msg: str) -> None:
        self.errors.append(f"{rel(where)}: {msg}")

    def warn(self, where: Path | str, msg: str) -> None:
        self.warnings.append(f"{rel(where)}: {msg}")


def rel(p: Path | str) -> str:
    try:
        return str(Path(p).relative_to(ROOT))
    except ValueError:
        return str(p)


def parse_frontmatter(text: str) -> tuple[dict | None, str, str]:
    """Parse the small YAML subset the spec needs: scalars and one nested string map."""
    if not text.startswith("---\n"):
        return None, text, "SKILL.md must start with '---' on line 1"
    end = text.find("\n---", 4)
    if end == -1:
        return None, text, "frontmatter has no closing '---'"
    raw, body = text[4:end], text[end + 4:].lstrip("\n")
    data: dict = {}
    current: str | None = None
    for n, line in enumerate(raw.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^( *)([A-Za-z0-9_-]+):(?: (.*))?$", line)
        if not m:
            return None, body, f"line {n}: cannot parse {line!r}"
        indent, key, value = len(m.group(1)), m.group(2), (m.group(3) or "").strip()
        if value[:1] in "\"'" and value[-1:] == value[:1] and len(value) > 1:
            value = value[1:-1]
        elif value[:1] in "[{|>":
            return None, body, f"line {n}: flow or block YAML is not supported here; use plain scalars"
        if indent == 0:
            if key in data:
                return None, body, f"duplicate key {key!r}"
            if value == "":
                data[key], current = {}, key
            else:
                data[key], current = value, None
        elif current is not None:
            data[current][key] = value
        else:
            return None, body, f"line {n}: unexpected indentation"
    return data, body, ""


def check_frontmatter(rep: Report, skill_md: Path) -> tuple[dict, str]:
    text = skill_md.read_text(encoding="utf-8")
    data, body, err = parse_frontmatter(text)
    if data is None:
        rep.error(skill_md, err)
        return {}, body
    extra = set(data) - SPEC_FIELDS
    if extra:
        rep.error(skill_md, f"frontmatter keys outside the Agent Skills spec: {sorted(extra)}")
    name = data.get("name", "")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        rep.error(skill_md, f"invalid name {name!r}")
    if name != skill_md.parent.name:
        rep.error(skill_md, f"name {name!r} must equal the directory name {skill_md.parent.name!r}")
    if "anthropic" in str(name) or "claude" in str(name):
        rep.error(skill_md, "name must not contain 'anthropic' or 'claude'")
    desc = data.get("description", "")
    if not isinstance(desc, str) or not desc:
        rep.error(skill_md, "description is required")
    else:
        if len(desc) > 1024:
            rep.error(skill_md, f"description is {len(desc)} characters (limit 1024)")
        if "<" in desc or ">" in desc:
            rep.error(skill_md, "description must not contain '<' or '>'")
        if "use when" not in desc.lower():
            rep.warn(skill_md, "description has no 'Use when' clause")
    comp = data.get("compatibility")
    if comp is not None and (not isinstance(comp, str) or not 1 <= len(comp) <= 500):
        rep.error(skill_md, "compatibility must be a string of 1-500 characters")
    meta = data.get("metadata")
    if meta is not None and (not isinstance(meta, dict) or not all(isinstance(v, str) for v in meta.values())):
        rep.error(skill_md, "metadata must be a flat map of strings")
    lines = body.count("\n") + 1
    tokens = len(body) // 4
    if lines > 500:
        rep.error(skill_md, f"body is {lines} lines (limit 500)")
    if tokens > 5000:
        rep.error(skill_md, f"body is about {tokens} tokens (limit 5000)")
    elif tokens > 4000:
        rep.warn(skill_md, f"body is about {tokens} tokens (warning threshold 4000)")
    for marker in CLAUDE_ONLY:
        if marker in body:
            rep.error(skill_md, f"agent-specific syntax {marker!r} is not portable")
    return data, body


LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICKED = re.compile(r"`((?:references|examples|scripts|assets)/[A-Za-z0-9_./-]+)`")


def local_targets(text: str) -> list[str]:
    out = []
    for target in LINK.findall(text):
        if re.match(r"[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        out.append(target.split("#")[0])
    out.extend(TICKED.findall(text))
    return [t for t in out if t]


def check_links(rep: Report, md: Path) -> set[Path]:
    """Return the set of skill files this document points at."""
    found: set[Path] = set()
    for target in local_targets(md.read_text(encoding="utf-8")):
        if target.startswith("/") or "\\" in target or ".." in Path(target).parts:
            rep.error(md, f"link {target!r} must be a forward-slash path inside the skill")
            continue
        candidates = [SKILL / target, md.parent / target]
        hit = next((c for c in candidates if c.exists()), None)
        if hit is None:
            rep.error(md, f"broken link {target!r}")
        else:
            found.add(hit.resolve())
    return found


def strip_swift(code: str) -> str:
    code = re.sub(r"//[^\n]*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)
    code = re.sub(r'"""(?:.|\n)*?"""', '""', code)
    return re.sub(r'"(?:\\.|[^"\\\n])*"', '""', code)


def check_swift(rep: Report, where: Path, code: str, first_line: int, context: list[str]) -> None:
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    balanced = True
    for ch in strip_swift(code):
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                balanced = False
                break
    if not balanced or stack:
        rep.error(where, f"Swift block starting at line {first_line} has unbalanced brackets")
    lines = code.splitlines()
    for i, line in enumerate(lines):
        window = "\n".join((context + lines)[max(0, i + len(context) - 3): i + len(context) + 1])
        for pattern, label in DEPRECATED.items():
            if re.search(pattern, line) and not MARKER.search(window):
                rep.error(where, f"line {first_line + i}: {label} outside an avoid/before/fallback sample")


def check_markdown_code(rep: Report, md: Path) -> None:
    lines = md.read_text(encoding="utf-8").splitlines()
    open_at: int | None = None
    lang = ""
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if open_at is None:
                open_at, lang = n, line.strip()[3:].strip().lower()
            else:
                if lang == "swift":
                    check_swift(rep, md, "\n".join(lines[open_at:n - 1]), open_at + 1, lines[max(0, open_at - 4):open_at - 1])
                open_at = None
    if open_at is not None:
        rep.error(md, f"code fence opened at line {open_at} is never closed")


def check_fake_apis(rep: Report, path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for name in FAKE_APIS:
        for n, line in enumerate(text.splitlines(), 1):
            if name in line and not re.search(r"not exist|no such|made-up|invented|not a real|hallucinat", line, re.I):
                rep.error(path, f"line {n}: {name!r} is not a real API")


def check_reference(rep: Report, md: Path, today: dt.date) -> None:
    text = md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not re.fullmatch(r"(%s)-[a-z0-9-]+\.md" % "|".join(REFERENCE_GROUPS), md.name):
        rep.error(md, "file name must be <group>-<topic>.md with a known group")
    if not lines or not lines[0].startswith("# "):
        rep.error(md, "line 1 must be a '# Title' heading")
    m = re.search(r"^Verified: (\d{4}-\d{2}-\d{2})", "\n".join(lines[:12]), re.M)
    if not m:
        rep.error(md, "missing 'Verified: YYYY-MM-DD' line near the top")
    else:
        age = (today - dt.date.fromisoformat(m.group(1))).days
        if age > STALE_AFTER_DAYS:
            rep.warn(md, f"last verified {age} days ago; re-check against Apple's documentation")
    if "https://developer.apple.com/" not in text:
        rep.error(md, "no developer.apple.com source URL")
    if not any(tag in text for tag in RULE_TAGS):
        rep.warn(md, "no rule tags ([Req]/[HIG]/[API]/[Conv]/[Unverified]) found")
    if len(lines) > 350:
        rep.error(md, f"{len(lines)} lines (hard limit 350); split the file")
    elif len(lines) > 300:
        rep.warn(md, f"{len(lines)} lines (target is 300 or fewer)")
    if len(lines) > 100 and not re.search(r"^## Contents", text, re.M):
        rep.warn(md, "file is over 100 lines but has no '## Contents' section")
    sections = re.split(r"^## ", text, flags=re.M)[1:]
    for sec in sections:
        title = sec.splitlines()[0].strip()
        if title.lower() in {"contents", "common mistakes"} or title.lower().startswith(("see also", "how to use")):
            continue
        if "https://developer.apple.com/" not in sec and "https://docs.swift.org/" not in sec:
            rep.warn(md, f"section '{title}' has no source URL")
    if re.search(r"\b(TODO|TBD|FIXME)\b", text):
        rep.warn(md, "contains TODO/TBD/FIXME")


def check_packaging(rep: Report, front: dict) -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    market_path = ROOT / ".claude-plugin" / "marketplace.json"
    version = (front.get("metadata") or {}).get("version")
    for path in (plugin_path, market_path):
        if not path.exists():
            rep.warn(path, "missing (the repository cannot be added as a Claude Code plugin marketplace)")
            return
    try:
        plugin = json.loads(plugin_path.read_text())
        market = json.loads(market_path.read_text())
    except json.JSONDecodeError as exc:
        rep.error(".claude-plugin", f"invalid JSON: {exc}")
        return
    if plugin.get("name") != SKILL_NAME:
        rep.error(plugin_path, f"name should be {SKILL_NAME!r}")
    if version and plugin.get("version") != version:
        rep.error(plugin_path, f"version {plugin.get('version')!r} differs from SKILL.md metadata.version {version!r}")
    entries = market.get("plugins") or []
    if not any(e.get("name") == plugin.get("name") for e in entries):
        rep.error(market_path, "no plugin entry matches plugin.json's name")
    if not (market.get("owner") or {}).get("name"):
        rep.error(market_path, "owner.name is required")


def check_evals(rep: Report) -> None:
    evals_path = ROOT / "tests" / "evals" / "evals.json"
    trig_path = ROOT / "tests" / "evals" / "trigger-queries.json"
    if evals_path.exists():
        try:
            data = json.loads(evals_path.read_text())
        except json.JSONDecodeError as exc:
            rep.error(evals_path, f"invalid JSON: {exc}")
            data = {}
        if data and data.get("skill_name") != SKILL_NAME:
            rep.error(evals_path, "skill_name must match the skill")
        ids = set()
        for ev in data.get("evals", []):
            eid = ev.get("id")
            if eid in ids:
                rep.error(evals_path, f"duplicate id {eid}")
            ids.add(eid)
            for key in ("prompt", "expected_output"):
                if not ev.get(key):
                    rep.error(evals_path, f"eval {eid}: missing {key}")
            assertions = ev.get("assertions") or ev.get("expectations") or []
            if not 3 <= len(assertions) <= 10:
                rep.error(evals_path, f"eval {eid}: expected 3-10 assertions, found {len(assertions)}")
            for f in ev.get("files", []):
                if not (ROOT / f).exists():
                    rep.error(evals_path, f"eval {eid}: fixture {f} does not exist")
            for r in ev.get("references_expected", []):
                if not (SKILL / r).exists():
                    rep.error(evals_path, f"eval {eid}: expected reference {r} does not exist")
        if not data.get("evals"):
            rep.error(evals_path, "no evals")
    else:
        rep.warn(evals_path, "missing")
    if trig_path.exists():
        try:
            queries = json.loads(trig_path.read_text())
        except json.JSONDecodeError as exc:
            rep.error(trig_path, f"invalid JSON: {exc}")
            return
        seen = set()
        counts = {True: 0, False: 0}
        for q in queries:
            if not isinstance(q.get("query"), str) or not isinstance(q.get("should_trigger"), bool):
                rep.error(trig_path, f"bad entry: {q!r}")
                continue
            if q["query"] in seen:
                rep.error(trig_path, f"duplicate query: {q['query'][:50]!r}")
            seen.add(q["query"])
            counts[q["should_trigger"]] += 1
        if min(counts.values()) < 8:
            rep.error(trig_path, f"need at least 8 positive and 8 negative queries, found {counts}")
    else:
        rep.warn(trig_path, "missing")


def fetch_ok(url: str) -> bool:
    req = urllib.request.Request(url, headers={"User-Agent": "skill-validator"})
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status == 200
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 410):
                return False
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
    return False


def check_online(rep: Report, files: list[Path]) -> None:
    """The human HIG and documentation pages are client-rendered and return 200 even for missing pages, so check
    the JSON that backs them instead."""
    hig = "https://developer.apple.com/design/human-interface-guidelines"
    doc = "https://developer.apple.com/documentation/"
    urls: dict[str, Path] = {}
    for f in files:
        for url in re.findall(r"https://developer\.apple\.com/[^\s)>`\"',]+", f.read_text(encoding="utf-8")):
            urls.setdefault(url.rstrip(".;:").split("#")[0], f)
    checked = 0
    for url, where in sorted(urls.items()):
        if "<" in url or "{" in url:
            continue
        if url.startswith(hig):
            slug = url[len(hig):].strip("/")
            probe = ("https://developer.apple.com/tutorials/data/design/human-interface-guidelines"
                     + (f"/{slug}" if slug else "") + ".json")
        elif url.startswith(doc):
            probe = "https://developer.apple.com/tutorials/data/documentation/" + url[len(doc):].strip("/").lower() + ".json"
        else:
            continue
        checked += 1
        if not fetch_ok(probe):
            rep.error(where, f"Apple page not found: {url}")
    print(f"online: checked {checked} Apple URLs")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--online", action="store_true", help="also verify that cited Apple URLs still exist")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    rep = Report()
    skill_md = SKILL / "SKILL.md"
    if not skill_md.exists():
        print(f"error: {rel(skill_md)} does not exist")
        return 1
    front, _ = check_frontmatter(rep, skill_md)

    refs = sorted((SKILL / "references").glob("*.md"))
    shipped_md = [skill_md, *refs, *sorted((SKILL / "examples").glob("*.md"))]
    linked_from_skill = check_links(rep, skill_md)
    for md in shipped_md[1:]:
        check_links(rep, md)
    for md in shipped_md:
        check_markdown_code(rep, md)

    today = dt.date.today()
    for md in refs:
        check_reference(rep, md, today)

    for sub in ("references", "examples", "scripts", "assets"):
        for f in sorted((SKILL / sub).rglob("*")) if (SKILL / sub).exists() else []:
            if f.is_dir() or "__pycache__" in f.parts:
                continue
            if f.resolve() not in linked_from_skill:
                rep.error(f, "not linked from SKILL.md (agents will not find it)")
            if f.stat().st_size > 1_000_000:
                rep.warn(f, "larger than 1 MB")
            if f.suffix == ".swift":
                check_swift(rep, f, f.read_text(encoding="utf-8"), 1, [])
            if f.suffix in {".md", ".swift"}:
                check_fake_apis(rep, f)
    check_fake_apis(rep, skill_md)
    for stray in ("evals", "tests"):
        if (SKILL / stray).exists():
            rep.warn(SKILL / stray, "eval material should live outside the skill directory")

    check_packaging(rep, front)
    check_evals(rep)
    if args.online:
        check_online(rep, shipped_md)

    for w in rep.warnings:
        print(f"warning: {w}")
    for e in rep.errors:
        print(f"error: {e}")
    total_lines = sum(len(p.read_text(encoding='utf-8').splitlines()) for p in shipped_md)
    print(f"{len(shipped_md)} Markdown files, {total_lines} lines; "
          f"{len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return 1 if rep.errors or (args.strict and rep.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
