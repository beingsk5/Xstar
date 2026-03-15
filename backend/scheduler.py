"""
Scheduler v5 — Match Detection for GitHub Actions
===================================================
Fixes vs v4:
  - sys.path.insert ensures providers.cricket always importable regardless of CWD
  - Pre-match awareness: matches starting within 10 min trigger should_stream=true
  - Always exits 0 — workflow reads should_stream from JSON
  - Outputs clean JSON to stdout for workflow parsing
"""

import sys, json, logging, importlib, time
from pathlib import Path

# FIX: ensure providers.cricket is always importable regardless of CWD
_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
                    handlers=[logging.StreamHandler(sys.stderr)])
log = logging.getLogger("Scheduler")

MONITORED_SPORTS = [
    "cricket",
    # "football",
]

SPORT_PROVIDERS = {
    "cricket":  "providers.cricket",
    # "football": "providers.football",
}

STREAMABLE_STATES = {"In Progress", "Innings Break", "Preview"}
PRE_MATCH_WINDOW  = 600  # 10 minutes


def _is_imminent(match: dict) -> bool:
    """True if matchStartTs is within PRE_MATCH_WINDOW seconds from now."""
    ts = match.get("matchStartTs", 0)
    if not ts:
        return False
    try:
        start_ms = int(ts)
        now_ms   = int(time.time() * 1000)
        diff_s   = (start_ms - now_ms) / 1000
        return 0 <= diff_s <= PRE_MATCH_WINDOW
    except Exception:
        return False


def check_all() -> dict:
    found = []

    for sport in MONITORED_SPORTS:
        try:
            provider = importlib.import_module(SPORT_PROVIDERS[sport])
            matches  = provider.discover_matches()
            for m in matches:
                state = m.get("state", "")
                if state in STREAMABLE_STATES:
                    found.append(m)
                    log.info(f"[{sport}] Active: {m.get('title')} [{state}]")
                elif _is_imminent(m):
                    m["state"] = "Preview"
                    found.append(m)
                    log.info(f"[{sport}] Imminent: {m.get('title')} (starting <10min)")
        except Exception as e:
            log.warning(f"Error checking {sport}: {e}")

    if not found:
        return {
            "should_stream": False,
            "sport":         None,
            "matches":       [],
            "reason":        "No active or imminent matches",
        }

    primary_sport = found[0].get("sport", "cricket")
    return {
        "should_stream": True,
        "sport":         primary_sport,
        "matches":       found,
        "reason":        f"Found {len(found)} streamable match(es)",
    }


if __name__ == "__main__":
    result = check_all()
    # Print JSON to stdout — workflow parses this
    print(json.dumps(result, indent=2))
    # Also write to file
    try:
        Path("/tmp/schedule.json").write_text(json.dumps(result, indent=2))
    except Exception:
        pass
    sys.exit(0)  # Always 0 — workflow reads should_stream from JSON
