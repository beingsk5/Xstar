"""
write_placeholder.py
====================
Writes clean placeholder stream_data JSON files before the stream starts.
Called by GitHub Actions before starting the fetcher.
"""
import json, os, sys

PLACEHOLDER = {
    "state":            "waiting",
    "status":           "Connecting to live data...",
    "team1":            "",
    "team2":            "",
    "title":            "Xstar Sports",
    "sport":            "cricket",
    "score":            "",
    "overs":            "",
    "run_rate":         "",
    "venue":            "",
    "live_commentary":  [],
    "scorecard":        {},
    "current_bowler":   {},
    "live_batsmen":     [],
    "is_free_hit":      False,
    "stream_complete":  False,
    "interruption":     "",
    "dls_announcement": False,
    "innings_page":     1,
    "over_phase":       "",
    "dls_target":       "",
    "resumption":       "",
    "match_start_ts":   0,
    "last_updated":     "",
}

root = os.path.join(os.path.dirname(__file__), "..", "frontend")
for fname in ["stream_data_main.json", "stream_data_shorts.json"]:
    path = os.path.join(root, fname)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(PLACEHOLDER, f, indent=2)
    print(f"Written: {path}")

sys.exit(0)
