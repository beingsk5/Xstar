"""
watchdog_check.py
=================
Called by GitHub Actions watchdog workflow.
1. Checks GitHub API if stream workflow is currently running
2. Checks if any matches are active
3. Writes need_restart= and sport= to GITHUB_OUTPUT
Always exits 0.
"""
import json, os, sys, urllib.request

GITHUB_OUTPUT = os.environ.get("GITHUB_OUTPUT", "")
GH_TOKEN      = os.environ.get("GH_TOKEN", "")
REPO          = os.environ.get("REPO", "")


def write_output(key: str, value: str):
    if GITHUB_OUTPUT:
        with open(GITHUB_OUTPUT, "a") as f:
            f.write(f"{key}={value}\n")
    print(f"OUTPUT: {key}={value}")


def is_stream_running() -> bool:
    if not GH_TOKEN or not REPO:
        print("No GH_TOKEN or REPO — assuming stream not running")
        return False
    url = f"https://api.github.com/repos/{REPO}/actions/runs?status=in_progress&per_page=20"
    req = urllib.request.Request(url, headers={
        "Authorization":        f"Bearer {GH_TOKEN}",
        "Accept":               "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        names = [x.get("name", "") for x in data.get("workflow_runs", [])]
        print(f"In-progress workflows: {names}")
        return any("Live Stream" in n or "Xstar" in n for n in names)
    except Exception as e:
        print(f"GitHub API failed: {e}")
        return False


def check_matches():
    """Returns (has_match: bool, sport: str)"""
    # scheduler.py was already run and output saved to /tmp/sched.json
    try:
        with open("/tmp/sched.json") as f:
            d = json.load(f)
        return bool(d.get("should_stream")), str(d.get("sport") or "cricket")
    except Exception as e:
        print(f"Could not read /tmp/sched.json: {e}")
        return False, "cricket"


# --- Main logic ---
stream_running = is_stream_running()
print(f"Stream currently running: {stream_running}")

if stream_running:
    print("Stream is active — no restart needed")
    write_output("need_restart", "false")
    write_output("sport", "cricket")
    sys.exit(0)

has_match, sport = check_matches()
print(f"Active match found: {has_match} sport={sport}")

if has_match:
    print(f"Stream is DOWN but match is live — restart needed for sport={sport}")
    write_output("need_restart", "true")
    write_output("sport", sport)
else:
    print("No active match — watchdog idle")
    write_output("need_restart", "false")
    write_output("sport", "cricket")

sys.exit(0)
