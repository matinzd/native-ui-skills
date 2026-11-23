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
