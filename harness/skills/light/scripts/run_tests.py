#!/usr/bin/env python3
"""Run a subgoal's test[] and write subgoals/<id>/test-<n>.json. Usage: RUN=<dir> run_tests.py <id> [attempt]"""
import json, os, subprocess, sys

run = os.environ.get("RUN")
if not run or len(sys.argv) < 2:
    sys.exit("usage: RUN=<dir> run_tests.py <id> [attempt]")
sid, n = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "1"
spec = json.load(open(f"{run}/02-goal-spec.json"))
goal = next(x for x in spec["subgoals"] if x["id"] == sid)
checks = []
for t in goal["test"]:
    p = subprocess.run(["bash", "-c", t], capture_output=True, text=True)
    checks.append({"cmd": t[:160], "exit": p.returncode, "out": (p.stdout + p.stderr)[-600:]})
verified = all(c["exit"] == 0 for c in checks)
os.makedirs(f"{run}/subgoals/{sid}", exist_ok=True)
with open(f"{run}/subgoals/{sid}/test-{n}.json", "w") as f:
    json.dump({"verified": verified, "checks": checks}, f, ensure_ascii=False, indent=1)
print(sid, "verified" if verified else "FAILED", [c["exit"] for c in checks])
for c in checks:
    if c["exit"]:
        print("---", c["cmd"][:100], "\n", c["out"][-300:])
sys.exit(0 if verified else 3)
