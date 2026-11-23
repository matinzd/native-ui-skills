#!/usr/bin/env python3
"""Scan Swift source for mechanically detectable Apple HIG and accessibility leads.

    python3 scripts/hig_lint.py <file-or-directory> [...]
    python3 scripts/hig_lint.py Sources --format json
    python3 scripts/hig_lint.py App --fail-on medium     # exit 1 when a Medium or High lead is found
    python3 scripts/hig_lint.py --list-rules

This is a regex-based helper, not a compiler or a HIG verdict. Every hit is a LEAD: read the surrounding code
before reporting it, and drop it when the context makes it fine (for example a deprecated API inside an
availability fallback, or a fixed size on a decorative shape). Absence of hits does not mean the interface
follows the HIG; most guidance cannot be checked this way.

Known blind spots (it will not report these): icon-only buttons whose label closure is on a different line
from `Button`; fixed sizes passed through variables; frames that set only a width or only a height; contrast;
anything that depends on layout at run time; UIKit and AppKit beyond a few font and color calls.

Exit status: 0 normally; 1 with --fail-on when a lead meets the threshold; 2 when a path does not exist or no
Swift files were found.

Suppress a line with a trailing comment:  // hig-lint:ignore   or   // hig-lint:ignore rule-id
Standard library only. Python 3.8+. Reads files, writes nothing, needs no network.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HIG = "https://developer.apple.com/design/human-interface-guidelines/"
DOC = "https://developer.apple.com/documentation/"
SKIP_DIRS = {".build", "build", "DerivedData", "Pods", "Carthage", ".git", "node_modules", ".swiftpm", "vendor"}
LEVELS = {"low": 1, "medium": 2, "high": 3}

VIOLATION = "Confirmed guideline or API violation"
A11Y = "Accessibility issue"
PLATFORM = "Platform convention mismatch"
IMPROVE = "Recommended improvement"


def rule(rid, pattern, klass, severity, message, source, unless=None, unless_file=None, unless_line=None):
    return {
        "id": rid, "re": re.compile(pattern), "class": klass, "severity": severity, "message": message,
        "source": source, "unless": re.compile(unless) if unless else None,
        "unless_line": re.compile(unless_line) if unless_line else None,
        "unless_file": re.compile(unless_file) if unless_file else None,
    }


DEPRECATED_NOTE = " Deprecated API is acceptable inside a fallback for systems older than the replacement."

RULES = [
    # Deprecated or removed API. The replacement's own minimum OS is listed in references/implementation-availability.md.
    rule("deprecated-navigationview", r"\bNavigationView\b", VIOLATION, "Low",
         "NavigationView is deprecated. Use NavigationStack or NavigationSplitView (iOS 16+, macOS 13+)." + DEPRECATED_NOTE,
         DOC + "swiftui/navigationview"),
    rule("deprecated-navigationbar-modifiers", r"\.navigationBar(Title|Items|Hidden)\(", VIOLATION, "Low",
         "navigationBarTitle / navigationBarItems / navigationBarHidden are deprecated. Use navigationTitle, toolbar "
         "with ToolbarItem, and toolbar visibility modifiers." + DEPRECATED_NOTE,
         DOC + "swiftui/view/navigationtitle(_:)"),
    rule("deprecated-foregroundcolor", r"\.foregroundColor\(", VIOLATION, "Low",
         "foregroundColor is deprecated. Use foregroundStyle (iOS 15+)." + DEPRECATED_NOTE,
         DOC + "swiftui/view/foregroundstyle(_:)"),
    rule("deprecated-accentcolor", r"\.accentColor\(", VIOLATION, "Low",
         "The accentColor modifier is deprecated. Use tint (iOS 15+) or the asset catalog accent color." + DEPRECATED_NOTE,
         DOC + "swiftui/view/tint(_:)"),
    rule("deprecated-cornerradius", r"\.cornerRadius\(", VIOLATION, "Low",
         "cornerRadius is deprecated. Use clipShape with a rounded rectangle shape." + DEPRECATED_NOTE,
         DOC + "swiftui/view/clipshape(_:style:)"),
    rule("deprecated-tabitem", r"\.tabItem\b", VIOLATION, "Low",
         "tabItem is deprecated. Use Tab inside TabView (iOS 18+, macOS 15+)." + DEPRECATED_NOTE,
         DOC + "swiftui/tab"),
    rule("deprecated-alert-actionsheet", r"\bActionSheet\(|\bAlert\(title:|\.actionSheet\(|\.alert\(isPresented:\s*[^,)]*\)\s*\{",
         VIOLATION, "Low",
         "Alert / ActionSheet values are deprecated. Use alert(_:isPresented:actions:message:) and confirmationDialog "
         "(iOS 15+)." + DEPRECATED_NOTE,
         DOC + "swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:)"),
    rule("deprecated-edgesignoringsafearea", r"\.edgesIgnoringSafeArea\(", VIOLATION, "Low",
         "edgesIgnoringSafeArea is deprecated. Use ignoresSafeArea (iOS 14+), and only on backgrounds.",
         DOC + "swiftui/view/ignoressafearea(_:edges:)"),
    rule("deprecated-onchange-perform", r"\.onChange\(of:[^)]*,\s*perform:|\.onChange\(of:[^)]*\)\s*\{\s*\w+\s+in\b",
         VIOLATION, "Low",
         "onChange(of:perform:) is deprecated as of iOS 17. Use the zero- or two-parameter closure form." + DEPRECATED_NOTE,
         DOC + "swiftui/view/onchange(of:initial:_:)"),
    rule("deprecated-uiscreen-main", r"\bUIScreen\.main\b", VIOLATION, "Medium",
         "UIScreen.main is deprecated as of iOS 26 and is wrong in multi-window apps. Lay out from the container: size "
         "classes, container-relative frames, or the view's window scene.",
         DOC + "uikit/uiscreen/main"),

    # Typography and Dynamic Type.
    rule("fixed-font-size", r"\.system\(\s*size:\s*(?:\d|[^,)]*[?:]\s*\d)|\b(?:systemFont|boldSystemFont|italicSystemFont)\(ofSize:\s*\d|"
                            r"\b(?:UIFont|NSFont)\(name:[^)]*size:\s*\d",
         A11Y, "Medium",
         "Fixed font size does not follow the person's text size setting on platforms with Dynamic Type. Use a text "
         "style (.body, .headline ...) or scale a custom size with a text style.",
         HIG + "typography"),
    rule("custom-font-not-scaled", r"\.custom\([^)]*\bfixedSize:", A11Y, "Medium",
         "Font.custom(_:fixedSize:) never scales. Use Font.custom(_:size:relativeTo:) unless the text must not scale.",
         DOC + "swiftui/font/custom(_:size:relativeto:)"),
    rule("pinned-dynamic-type", r"\.dynamicTypeSize\(\s*\.[A-Za-z0-9]+\s*\)", A11Y, "High",
         "dynamicTypeSize with a single value pins the text size and ignores the person's setting. Fix the layout "
         "instead; restrict the range only for chrome that cannot grow.",
         HIG + "accessibility"),
    rule("shrink-to-fit-text", r"\.minimumScaleFactor\(", A11Y, "Low",
         "Shrinking text to fit works against larger text sizes. Prefer wrapping or an alternative layout at "
         "accessibility sizes.",
         HIG + "typography"),

    # Color and appearance.
    rule("hard-coded-color", r"\bColor\.(white|black)\b|\bColor\(\s*(?:\.\w+\s*,\s*)?(red|white|hue):|\bColor\(\s*hex:|"
                             r"\bUIColor\(\s*(red|white|hue):|"
                             r"\bUIColor\.(white|black)\b|\bNSColor\.(white|black)\b|#colorLiteral\(|"
                             r"\.(background|foregroundStyle)\(\s*\.(white|black)\s*[,)]",
         IMPROVE, "Medium",
         "Hard-coded color does not adapt to Dark Mode, Increase Contrast, or the platform's appearance. Use a "
         "semantic style or an asset catalog color with light and dark variants. Check contrast in both appearances.",
         HIG + "dark-mode"),
    rule("forced-color-scheme", r"\.preferredColorScheme\(\s*\.(light|dark)\s*\)", IMPROVE, "Low",
         "Forcing one appearance overrides the person's system setting. Follow the system appearance unless the "
         "content demands otherwise.",
         HIG + "dark-mode"),

    # Controls and interaction.
    rule("tap-gesture-as-button", r"\.onTapGesture\b", A11Y, "Medium",
         "onTapGesture gives no button trait, focus, keyboard, hover, or pressed state. If this is an action, use "
         "Button (with a custom style if needed).",
         DOC + "swiftui/button", unless=r"count:\s*[2-9]"),
    rule("icon-only-button", r"\bButton\b[^\n]*\{\s*Image\(systemName:", A11Y, "Medium",
         "Icon-only button: make sure it has a text label for VoiceOver and Voice Control, for example "
         "Label(\"Add\", systemImage: \"plus\") or an accessibilityLabel.",
         HIG + "accessibility", unless=r"accessibilityLabel|Label\("),
    rule("small-fixed-frame", r"\.frame\(\s*width:\s*(?:[0-3]?\d|4[0-3])(?:\.\d+)?\s*,\s*height:\s*(?:[0-3]?\d|4[0-3])(?:\.\d+)?\s*[,)]",
         A11Y, "Low",
         "Fixed frame smaller than 44x44 pt. If this element is tappable, enlarge its hit region to the platform's "
         "default control size (44 pt on iPhone and iPad; see the Accessibility page for other platforms).",
         HIG + "accessibility"),

    # Layout and adaptivity.
    rule("device-idiom-layout", r"\buserInterfaceIdiom\b", PLATFORM, "Medium",
         "Branching on device idiom breaks in resizable windows, multitasking, and on new devices. Adapt to size "
         "classes or let an adaptive container decide.",
         HIG + "layout"),
    rule("ignores-safe-area", r"\.ignoresSafeArea\(\s*\)", IMPROVE, "Low",
         "ignoresSafeArea() on all edges: apply it only to backgrounds so content and controls stay clear of system "
         "areas.",
         HIG + "layout", unless_line=r"Color[.(]|Gradient|Image\(|\.background|Rectangle\("),
    rule("geometry-reader", r"\bGeometryReader\b", IMPROVE, "Low",
         "GeometryReader is often used to hand-compute layout that stacks, grids, ViewThatFits, or "
         "containerRelativeFrame handle adaptively. Confirm it is needed.",
         DOC + "swiftui/geometryreader"),

    # Motion.
    rule("endless-animation", r"\.repeatForever\(", A11Y, "Medium",
         "Repeating animation with no Reduce Motion handling in this file. Check accessibilityReduceMotion and offer "
         "a still or fading alternative.",
         HIG + "motion", unless_file=r"accessibilityReduceMotion|isReduceMotionEnabled"),
]

IGNORE = re.compile(r"//\s*hig-lint:ignore(?:\s+([\w-]+))?")


def swift_files(paths, missing):
    for raw in paths:
        p = Path(raw)
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*.swift")):
                if not SKIP_DIRS.intersection(f.relative_to(p).parts):
                    yield f
        else:
            missing.append(raw)
            print(f"hig_lint: no such file or directory: {raw}", file=sys.stderr)


def code_part(line):
    """Drop a trailing // comment so commented-out code and prose are not flagged (string contents are kept)."""
    out, in_string, i = [], False, 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and in_string:
            out.append(line[i:i + 2])
            i += 2
            continue
        if ch == '"':
            in_string = not in_string
        elif ch == "/" and not in_string and line[i:i + 2] == "//":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def scan(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"hig_lint: cannot read {path}: {exc}", file=sys.stderr)
        return []
    # Blank out /* ... */ comments but keep line numbers.
    text_nc = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    lines = text_nc.splitlines()
    findings = []
    for n, line in enumerate(lines, 1):
        code = code_part(line)
        if not code.strip():
            continue
        ignore = IGNORE.search(line)
        if ignore and not ignore.group(1):
            continue
        # The statement: this line plus directly following lines that continue it with a leading-dot modifier.
        end = n
        while end < len(lines) and end - n < 3 and lines[end].lstrip().startswith("."):
            end += 1
        context = "\n".join(lines[n - 1:end])
        for r in RULES:
            if not r["re"].search(code):
                continue
            if ignore and ignore.group(1) == r["id"]:
                continue
            if r["unless"] and r["unless"].search(context):
                continue
            if r["unless_line"] and r["unless_line"].search(code):
                continue
            if r["unless_file"] and r["unless_file"].search(text):
                continue
            findings.append({
                "file": str(path), "line": n, "rule": r["id"], "class": r["class"], "severity": r["severity"],
                "message": r["message"], "source": r["source"], "code": line.strip()[:160],
            })
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", help="Swift files or directories to scan")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--fail-on", choices=tuple(LEVELS), help="exit 1 if a lead at or above this severity is found")
    ap.add_argument("--max", type=int, default=200, help="maximum leads to print (default 200)")
    ap.add_argument("--list-rules", action="store_true", help="print the rules and exit")
    args = ap.parse_args()

    if args.list_rules:
        for r in RULES:
            print(f"{r['id']:<34} {r['severity']:<6} {r['class']}\n    {r['message']}\n    {r['source']}")
        return 0
    if not args.paths:
        ap.print_usage(sys.stderr)
        return 2

    missing = []
    files = list(swift_files(args.paths, missing))
    if missing or not files:
        if not missing:
            print("hig_lint: no Swift files found", file=sys.stderr)
        return 2
    findings = [f for path in files for f in scan(path)]
    findings.sort(key=lambda f: (-LEVELS[f["severity"].lower()], f["file"], f["line"]))
    shown = findings[:args.max]

    if args.format == "json":
        json.dump({"files_scanned": len(files), "total": len(findings), "leads": shown}, sys.stdout, indent=2)
        print()
    else:
        for f in shown:
            print(f"{f['file']}:{f['line']}: [{f['severity']}] {f['rule']} ({f['class']})")
            print(f"    {f['code']}")
            print(f"    {f['message']}")
            print(f"    Source: {f['source']}")
        hidden = len(findings) - len(shown)
        print(f"{len(files)} file(s) scanned, {len(findings)} lead(s)" + (f", {hidden} not shown" if hidden else "")
              + ". Leads need confirmation by reading the code.")

    if args.fail_on and any(LEVELS[f["severity"].lower()] >= LEVELS[args.fail_on] for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
