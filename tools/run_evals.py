#!/usr/bin/env python3
"""Run a skill's evals in Claude Code, with and without the skill.

    python3 tools/run_evals.py tasks --skill apple-hig                  # all task scenarios, both configurations
    python3 tools/run_evals.py tasks --skill apple-hig --ids 6 16 18    # selected scenarios
    python3 tools/run_evals.py triggers --skill material-design --limit 12
    python3 tools/run_evals.py tasks --skill apple-hig --jobs 4 --out eval-workspace/apple-hig/iteration-1

Requires the `claude` CLI on PATH and a signed-in account. Each run starts a fresh, non-interactive session in an
empty temporary project; the "with_skill" project has the skill copied to .claude/skills/, the "without_skill"
project has nothing. With --all-skills, every skill in this repository is installed in the "with_skill" project,
which is how to check that sibling skills do not steal each other's queries. Outputs (final answer, tool calls, files read, token usage) are written as JSON under --out.
`skill_files_read` lists files opened with the Read tool; `skill_files_touched` lists files named in shell or
search commands (a grep that matched a file may have loaded only a few lines). This script collects outputs only. Grade them against the assertions in tests/evals/evals.json separately.
Standard library only. Runs cost real tokens: roughly 18 scenarios x 2 configurations for a full task run.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
# Set from --skill in main().
SKILL = SKILLS_DIR / "apple-hig"
EVALS = ROOT / "tests" / "evals" / "apple-hig"
INSTALL_ALL = False


def run_claude(prompt: str, with_skill: bool, files: list[str], timeout: int) -> dict:
    with tempfile.TemporaryDirectory(prefix="hig-eval-") as tmp:
        project = Path(tmp)
        if with_skill:
            for src in (sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir()) if INSTALL_ALL else [SKILL]):
                dest = project / ".claude" / "skills" / src.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
        for rel in files:
            target = project / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / rel, target)
        cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--max-turns", "25",
               "--permission-mode", "acceptEdits"]
        try:
            proc = subprocess.run(cmd, cwd=project, capture_output=True, text=True, timeout=timeout,
                                  stdin=subprocess.DEVNULL, check=False)
        except subprocess.TimeoutExpired:
            return {"error": f"timed out after {timeout}s"}
        result = {"answer": "", "tool_calls": [], "skill_invoked": False, "other_skills_invoked": [],
                  "skill_files_read": [],
                  "skill_files_touched": [], "edited": {}}
        for line in proc.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "assistant":
                for block in event["message"].get("content", []):
                    if block.get("type") == "tool_use":
                        name, inp = block["name"], block.get("input", {})
                        result["tool_calls"].append({"name": name, "input": json.dumps(inp)[:300]})
                        if name == "Skill":
                            called = str(inp.get("skill", "")).split(":")[-1]
                            if called == SKILL.name:
                                result["skill_invoked"] = True
                            elif called:
                                result["other_skills_invoked"].append(called)
                        path = str(inp.get("file_path", ""))
                        if name == "Read" and f"skills/{SKILL.name}/" in path:
                            if path.endswith("SKILL.md"):
                                result["skill_invoked"] = True
                            else:
                                result["skill_files_read"].append(path.split(f"skills/{SKILL.name}/")[1])
                        elif name in ("Bash", "Grep", "Glob"):
                            # Agents also reach skill files through the shell or search tools.
                            for hit in re.findall(r"(?:references|examples|scripts)/[\w.-]+\.\w+", json.dumps(inp)):
                                if (SKILL / hit).exists() and hit not in result["skill_files_touched"]:
                                    result["skill_files_touched"].append(hit)
            elif event.get("type") == "result":
                result["answer"] = event.get("result", "")
                result["turns"] = event.get("num_turns")
                result["cost_usd"] = event.get("total_cost_usd")
                result["duration_ms"] = event.get("duration_ms")
                usage = event.get("usage", {})
                result["tokens"] = {k: usage.get(k) for k in
                                    ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")}
        for rel in files:
            after = (project / rel).read_text(encoding="utf-8")
            if after != (ROOT / rel).read_text(encoding="utf-8"):
                result["edited"][rel] = after
        if not result["answer"] and proc.returncode != 0:
            result["error"] = (proc.stderr or proc.stdout)[-500:]
        return result


def cmd_tasks(args) -> int:
    data = json.loads((EVALS / "evals.json").read_text())
    evals = [e for e in data["evals"] if not args.ids or e["id"] in args.ids]
    jobs = [(e, cfg) for e in evals for cfg in ("with_skill", "without_skill") if cfg in args.configs]

    def one(job):
        ev, cfg = job
        res = run_claude(ev["prompt"], cfg == "with_skill", ev.get("files", []), args.timeout)
        out = args.out / f"eval-{ev['id']:02d}-{ev['name']}" / cfg
        out.mkdir(parents=True, exist_ok=True)
        (out / "output.json").write_text(json.dumps(res, indent=2))
        (out / "answer.md").write_text(res.get("answer", "") or res.get("error", ""))
        return ev["id"], cfg, res

    with cf.ThreadPoolExecutor(args.jobs) as pool:
        for eid, cfg, res in pool.map(one, jobs):
            print(f"eval {eid:>2} {cfg:<13} skill_invoked={res.get('skill_invoked')} "
                  f"refs={len(res.get('skill_files_read', []))} cost=${res.get('cost_usd')} {res.get('error', '')}")
    return 0


def cmd_triggers(args) -> int:
    queries = json.loads((EVALS / "trigger-queries.json").read_text())
    if args.split:
        queries = [q for q in queries if q.get("split") == args.split]
    if args.limit:
        pos = [q for q in queries if q["should_trigger"]][: args.limit // 2]
        neg = [q for q in queries if not q["should_trigger"]][: args.limit - len(pos)]
        queries = pos + neg

    def one(q):
        prompt = q["query"] + "\n\n(Answer briefly. Do not create or edit files.)"
        return q, run_claude(prompt, True, [], args.timeout)

    rows, correct = [], 0
    with cf.ThreadPoolExecutor(args.jobs) as pool:
        for q, res in pool.map(one, queries):
            ok = bool(res.get("skill_invoked")) == q["should_trigger"] and "error" not in res
            correct += ok
            rows.append({"query": q["query"], "should_trigger": q["should_trigger"],
                         "triggered": res.get("skill_invoked"), "other_skills": res.get("other_skills_invoked"),
                         "correct": ok, "error": res.get("error")})
            print(f"{'ok  ' if ok else 'MISS'} expect={q['should_trigger']!s:<5} got={res.get('skill_invoked')!s:<5} "
                  f"other={','.join(res.get('other_skills_invoked') or []) or '-':<16} {q['query'][:70]}")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "triggers.json").write_text(json.dumps({"correct": correct, "total": len(rows), "rows": rows}, indent=2))
    print(f"{correct}/{len(rows)} correct")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("tasks", "triggers"):
        p = sub.add_parser(name)
        p.add_argument("--skill", required=True, help="skill directory name under skills/")
        p.add_argument("--all-skills", action="store_true", help="install every skill of this repository, not only --skill")
        p.add_argument("--out", type=Path)
        p.add_argument("--jobs", type=int, default=3)
        p.add_argument("--timeout", type=int, default=600)
    sub.choices["tasks"].add_argument("--ids", type=int, nargs="*")
    sub.choices["tasks"].add_argument("--configs", nargs="*", default=["with_skill", "without_skill"])
    sub.choices["triggers"].add_argument("--limit", type=int, default=0)
    sub.choices["triggers"].add_argument("--split", choices=("train", "validation"), help="run only this split")
    args = ap.parse_args()
    global SKILL, EVALS, INSTALL_ALL
    SKILL, EVALS, INSTALL_ALL = SKILLS_DIR / args.skill, ROOT / "tests" / "evals" / args.skill, args.all_skills
    if not (SKILL / "SKILL.md").exists():
        print(f"error: no skill named {args.skill!r} under skills/", file=sys.stderr)
        return 2
    args.out = args.out or ROOT / "eval-workspace" / args.skill / "run"
    if shutil.which("claude") is None:
        print("error: the `claude` CLI is not on PATH", file=sys.stderr)
        return 2
    return cmd_tasks(args) if args.command == "tasks" else cmd_triggers(args)


if __name__ == "__main__":
    sys.exit(main())
