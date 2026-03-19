"""
parse_schedule.py
=================
Called by GitHub Actions after scheduler.py runs.
Reads /tmp/sched.json and writes go= and sport= to GITHUB_OUTPUT.
Always exits 0.
"""
import json, os, sys

GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "")

def write_output(key: str, value: str):
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")

try:
    with open("/tmp/sched.json") as f:
        d = json.load(f)
    go    = str(d.get("should_stream", False)).lower()
    sport = str(d.get("sport") or "cricket")
except Exception as e:
    print(f"Parse error: {e}", file=sys.stderr)
    go    = "false"
    sport = "cricket"

write_output("go",    go)
write_output("sport", sport)
sys.exit(0)
