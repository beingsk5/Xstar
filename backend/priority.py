"""
Match Priority Engine
======================
Decides which matches are MAIN stream vs SHORTS stream.
Returns top-2 ranked matches from all sports combined.

Priority scoring factors:
  - Match format weight (Test > ODI > T20 > T10)
  - Series importance (World Cup > Champions Trophy > Bilateral)
  - Teams involved (top-ranked nations score higher)
  - Match state (In Progress > Preview > Innings Break)
  - Audience appeal (rivalry matches get bonus)

Output:
  {
    "main":   { ...match_meta, "stream": "main"   },
    "shorts": { ...match_meta, "stream": "shorts" },
  }
  Either can be None if <2 matches exist.
"""

import re

# ── Format weights ─────────────────────────────────────────────────────────────
FORMAT_WEIGHT = {
    "TEST": 100, "ODI": 85, "T20I": 80, "T20": 75,
    "T10": 60, "THE HUNDRED": 65, "IPL": 90, "PSL": 82,
    "BBL": 78, "CPL": 70, "SA20": 70, "ILT20": 68,
}

# ── Series keyword importance ──────────────────────────────────────────────────
SERIES_KEYWORDS = {
    "world cup":         50,
    "champions trophy":  45,
    "wct20":             45,
    "wc":                40,
    "final":             40,
    "semi final":        35,
    "semifinal":         35,
    "tri series":        20,
    "asia cup":          30,
    "ipl":               35,
    "psl":               30,
    "ashes":             40,
    "border-gavaskar":   38,
}

# ── Top-tier teams (higher = more audience) ────────────────────────────────────
TEAM_WEIGHT = {
    "india": 30, "ind": 30,
    "australia": 22, "aus": 22,
    "england": 20, "eng": 20,
    "pakistan": 20, "pak": 20,
    "south africa": 16, "sa": 16,
    "new zealand": 14, "nz": 14,
    "west indies": 13, "wi": 13,
    "sri lanka": 12, "sl": 12,
    "bangladesh": 11, "ban": 11,
    "afghanistan": 10, "afg": 10,
}

# ── Rivalry bonus pairs ────────────────────────────────────────────────────────
RIVALRIES = [
    ({"india", "pakistan"},       25),
    ({"india", "australia"},      18),
    ({"australia", "england"},    20),  # Ashes
    ({"india", "england"},        15),
    ({"pakistan", "afghanistan"}, 10),
]

STATE_WEIGHT = {
    "in progress":    30,
    "innings break":  20,
    "preview":        10,
    "complete":        0,
}


def score_match(match: dict) -> float:
    total = 0.0

    # Format
    fmt = (match.get("matchFormat") or match.get("match_format") or "").upper()
    total += FORMAT_WEIGHT.get(fmt, 50)

    # Series name keywords
    series = (match.get("seriesName") or match.get("series") or "").lower()
    for kw, w in SERIES_KEYWORDS.items():
        if kw in series:
            total += w
            break

    # Teams
    t1 = (match.get("team1") or "").lower()
    t2 = (match.get("team2") or "").lower()
    for key, w in TEAM_WEIGHT.items():
        if key in t1: total += w
        if key in t2: total += w

    # Rivalry bonus
    teams_set = set()
    for t in [t1, t2]:
        for key in TEAM_WEIGHT:
            if key in t:
                teams_set.add(key)
    for rivals, bonus in RIVALRIES:
        if rivals.issubset(teams_set):
            total += bonus

    # State
    state = (match.get("state") or "").lower()
    for key, w in STATE_WEIGHT.items():
        if key in state:
            total += w
            break

    return total


def rank_matches(matches: list[dict]) -> list[dict]:
    """Sort matches by priority score, highest first."""
    scored = [(score_match(m), m) for m in matches]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [m for _, m in scored]


def assign_streams(matches: list[dict]) -> dict:
    """
    Given a list of matches (from all sports),
    return {"main": match|None, "shorts": match|None}
    """
    ranked = rank_matches(matches)
    result = {
        "main":   None,
        "shorts": None,
        "all_ranked": ranked,
    }
    if len(ranked) >= 1:
        result["main"]   = {**ranked[0], "stream_type": "main"}
    if len(ranked) >= 2:
        result["shorts"] = {**ranked[1], "stream_type": "shorts"}
    return result
