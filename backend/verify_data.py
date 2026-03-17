"""
verify_data.py
==============
Called by GitHub Actions to verify stream_data_main.json has live data.
Always exits 0 — just prints diagnostic info.
"""
import json, os, sys

path = os.path.join(os.path.dirname(__file__), "..", "frontend", "stream_data_main.json")
try:
    with open(path) as f:
        d = json.load(f)
    print(f"Match : {d.get('title', 'not set')}")
    print(f"Score : {d.get('score', 'not set')}")
    print(f"State : {d.get('state', 'not set')}")
    print(f"Venue : {d.get('venue', 'not set')}")
    print(f"Series: {d.get('series', 'not set')}")
except Exception as e:
    print(f"Could not read data file: {e}")

sys.exit(0)
