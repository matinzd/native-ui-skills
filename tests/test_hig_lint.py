#!/usr/bin/env python3
"""Self-test for skills/apple-hig/scripts/hig_lint.py. Standard library only.

Checks that the linter finds the problems planted in the eval fixtures, and that the skill's own example
files, which are meant to model good practice, come out clean.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = ROOT / "skills" / "apple-hig" / "scripts" / "hig_lint.py"
FIXTURES = ROOT / "tests" / "evals" / "files"
EXAMPLES = ROOT / "skills" / "apple-hig" / "examples"

EXPECTED = {
    "OrdersView.swift": {"deprecated-navigationview", "tap-gesture-as-button", "fixed-font-size", "icon-only-button",
                         "small-fixed-frame", "deprecated-navigationbar-modifiers", "deprecated-alert-actionsheet"},
    "RootTabs.swift": {"tap-gesture-as-button", "fixed-font-size", "deprecated-foregroundcolor", "hard-coded-color"},
    "ProfileHeader.swift": {"fixed-font-size", "deprecated-foregroundcolor"},
    "PlayerControls.swift": {"tap-gesture-as-button", "small-fixed-frame", "pinned-dynamic-type", "endless-animation",
                             "hard-coded-color"},
    "LibraryView.swift": {"device-idiom-layout", "fixed-font-size"},
}


def run(*args):
    proc = subprocess.run([sys.executable, str(LINT), *map(str, args), "--format", "json"],
                          capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def main():
    failures = []
    for name, expected in EXPECTED.items():
        found = {lead["rule"] for lead in run(FIXTURES / name)["leads"]}
        missing = expected - found
        if missing:
            failures.append(f"{name}: expected leads not reported: {sorted(missing)}")

    if EXAMPLES.exists():
        for lead in run(EXAMPLES)["leads"]:
            # Deprecated API is allowed in the examples inside marked availability fallbacks; the repository
            # validator (tools/validate_skill.py) checks that those are marked.
            if lead["rule"].startswith("deprecated-"):
                continue
            failures.append(f"example flagged: {lead['file']}:{lead['line']} {lead['rule']}: {lead['code']}")

    # Crafted lines: each must produce exactly the listed rules (an empty set means "must stay clean").
    cases = [
        ('Image(systemName: "x").font(.system(size: iconSize))', set()),
        ('Text("t").font(.system(size: 14))', {"fixed-font-size"}),
        ('label.font = .systemFont(ofSize: 9)', {"fixed-font-size"}),
        ('Text("t").onTapGesture { one() }', {"tap-gesture-as-button"}),
        ('Text("u")\n    .onTapGesture(count: 2) { two() }', set()),
        ('Color.blue.ignoresSafeArea()', set()),
        ('ScrollView { }.ignoresSafeArea()', {"ignores-safe-area"}),
        ('Text("a").frame(width: 42, height: 42)', {"small-fixed-frame"}),
        ('Text("a").frame(width: 44, height: 44)', set()),
        ('/* Text("x").foregroundColor(.red) */', set()),
        ('// Text("x").foregroundColor(.red)', set()),
        ('Text("b").alert(isPresented: $s, error: err) { _ in } message: { _ in }', set()),
        ('Text("c").onChange(of: x) { newValue in go() }', {"deprecated-onchange-perform"}),
        ('Text("d").onChange(of: x) { old, new in go() }', set()),
        ('Text("e").foregroundStyle(Color(.sRGB, red: 1, green: 0, blue: 0))', {"hard-coded-color"}),
        ('Text("f").foregroundStyle(.secondary)', set()),
        ('Button(action: add) { Image(systemName: "plus") }', {"icon-only-button"}),
        ('Button(action: add) { Image(systemName: "plus") }\n    .accessibilityLabel("Add")', set()),
        ('Text("g").foregroundColor(.red) // hig-lint:ignore', set()),
    ]
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        for i, (code, expected) in enumerate(cases):
            f = Path(tmp) / f"Case{i}.swift"
            f.write_text(code + "\n", encoding="utf-8")
            found = {lead["rule"] for lead in run(f)["leads"]}
            if found != expected:
                failures.append(f"crafted case {code!r}: expected {sorted(expected)}, got {sorted(found)}")
        # A project that happens to live under a directory named like a build folder must still be scanned.
        nested = Path(tmp) / "build" / "App"
        nested.mkdir(parents=True)
        (nested / "V.swift").write_text('Text("t").font(.system(size: 14))\n', encoding="utf-8")
        if not run(Path(tmp) / "build")["leads"]:
            failures.append("files under a scan root named 'build' were skipped")
    proc = subprocess.run([sys.executable, str(LINT), "/nonexistent-path"], capture_output=True, text=True, check=False)
    if proc.returncode != 2:
        failures.append("a missing path should exit 2")

    proc = subprocess.run([sys.executable, str(LINT), "--help"], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        failures.append("--help did not exit 0")
    proc = subprocess.run([sys.executable, str(LINT), str(FIXTURES), "--fail-on", "high"],
                          capture_output=True, text=True, check=False)
    if proc.returncode != 1:
        failures.append("--fail-on high should exit 1 on the fixtures")

    for f in failures:
        print(f"FAIL: {f}")
    print(f"hig_lint self-test: {'failed' if failures else 'passed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
