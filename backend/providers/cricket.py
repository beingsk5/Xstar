"""
Cricket Provider v5 — Cricbuzz API
====================================
Fixes vs v4:
  - Duplicate 'target' key removed from build_stream_data
  - innings_num edge case: try/except around int() conversion
  - Schedule awareness: matchStartTimestamp extracted for pre-match timing
  - DLS revised target extracted separately from main target
  - Rain resumption time extracted from status string
  - Over phase more granular: PP1 / PP2 for ODI
"""

import requests, logging, re, time as _time
from typing import Optional

log = logging.getLogger("Cricket")

BASE    = "https://www.cricbuzz.com/api"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer":         "https://www.cricbuzz.com/",
    "Origin":          "https://www.cricbuzz.com",
}

INTERRUPTION_MAP = [
    (["rain", "wet outfield", "wet outfield"],   "rain"),
    (["bad light", "poor light"],                "bad_light"),
    (["lunch"],                                  "lunch"),
    (["tea"],                                    "tea"),
    (["drinks"],                                 "drinks"),
    (["injury", "medical"],                      "injury"),
    (["abandoned", "no result"],                 "abandoned"),
    (["cancelled"],                              "cancelled"),
    (["delayed", "yet to begin"],                "delayed"),
    (["dls", "revised target", "d/l", "d/ls"],  "dls"),
    (["inspection", "pitch inspection"],         "inspection"),
    (["suspend", "stop", "halt", "interrupt"],   "suspended"),
]

def _detect_interruption(status: str) -> str:
    sl = (status or "").lower()
    for keywords, itype in INTERRUPTION_MAP:
        if any(k in sl for k in keywords):
            return itype
    return ""

def _extract_resumption_time(status: str) -> str:
    """Try to parse ETA from status like 'Expected resumption at 14:30 local'"""
    sl = (status or "").lower()
    m = re.search(r'resumption.{0,20}(\d{1,2}[:.]\d{2})', sl)
    if m:
        return m.group(1)
    m2 = re.search(r'(\d{1,2}[:.]\d{2})\s*(local|ist|gmt)', sl)
    if m2:
        return m2.group(1)
    return ""

def _over_phase(overs_str: str, fmt: str) -> str:
    try:
        ov = float(overs_str or 0)
    except (ValueError, TypeError):
        return ""
    fmt_u = (fmt or "").upper()
    if "T20" in fmt_u or "T10" in fmt_u:
        if ov <= 6:   return "POWERPLAY"
        if ov <= 15:  return "MIDDLE"
        return "DEATH"
    if "ODI" in fmt_u:
        if ov <= 10:  return "PP1"
        if ov <= 40:  return "MIDDLE"
        if ov <= 46:  return "PP2"
        return "DEATH"
    return ""  # Test — no phases

def _get(url: str, retries: int = 3) -> Optional[dict]:
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code == 429:
                wait = 2 ** attempt * 5
                log.warning(f"Rate limited — waiting {wait}s")
                _time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.Timeout:
            log.warning(f"Timeout {url} attempt {attempt+1}")
        except requests.exceptions.ConnectionError as e:
            log.warning(f"Connection {url}: {e}")
        except Exception as e:
            log.warning(f"GET {url}: {e}")
            return None
        _time.sleep(1)
    return None

def _sort_keys(d: dict) -> list:
    def key(k):
        m = re.search(r'(\d+)$', str(k))
        return int(m.group(1)) if m else 0
    return [d[k] for k in sorted(d.keys(), key=key)]

def _safe_int(val, default: int = 1) -> int:
    """Safely convert to int, returns default on None/empty/invalid."""
    try:
        return int(val or default)
    except (TypeError, ValueError):
        return default


# ── 1. Match Discovery ────────────────────────────────────────────────────────
def discover_matches() -> list[dict]:
    data = _get(f"{BASE}/home")
    if not data:
        return []
    results = []
    for entry in data.get("matches", []):
        mi = entry.get("match", {}).get("matchInfo", {})
        if not mi:
            continue
        t1  = mi.get("team1", {}).get("teamName", "TBA")
        t2  = mi.get("team2", {}).get("teamName", "TBA")
        # Schedule awareness: capture start timestamp for pre-match detection
        start_ts = mi.get("matchStartTimestamp", mi.get("startTime", 0))
        results.append({
            "sport":            "cricket",
            "matchId":          mi.get("matchId"),
            "seriesId":         mi.get("seriesId"),
            "seriesName":       mi.get("seriesName", ""),
            "matchDesc":        mi.get("matchDesc", ""),
            "matchFormat":      mi.get("matchFormat", ""),
            "state":            mi.get("state", ""),
            "status":           mi.get("status", ""),
            "team1":            t1,
            "team2":            t2,
            "title":            f"{t1} vs {t2}",
            "matchStartTs":     start_ts,
        })
    return results


# ── 2. Live Summary ───────────────────────────────────────────────────────────
def fetch_summary(match_id: str) -> dict:
    data = _get(f"{BASE}/mcenter/comm/{match_id}")
    if not data:
        return {}

    ms    = data.get("miniscore", {})
    bat   = ms.get("batTeam", {})
    hdr   = data.get("matchHeader", {})
    status_str = hdr.get("status", "")

    # Venue — Cricbuzz uses different locations and field names depending on match type
    # Try matchHeader.venue, then matchInfo.venue, then top-level venueInfo
    _venue_raw = (
        hdr.get("venue")
        or data.get("matchInfo", {}).get("venue")
        or data.get("venueInfo")
        or {}
    )
    venue = _venue_raw if isinstance(_venue_raw, dict) else {}
    venue_name = (
        venue.get("name") or venue.get("ground")
        or venue.get("groundName") or venue.get("stadium") or ""
    )
    venue_city = (
        venue.get("city") or venue.get("location")
        or venue.get("country") or ""
    )

    # Win probability — normalise to 0–1
    raw_wp = data.get("winProbability", {})
    win_prob = {}
    for k, v in (raw_wp or {}).items():
        try:
            fv = float(v)
            win_prob[k] = round(fv / 100.0 if fv > 1 else fv, 3)
        except Exception:
            pass

    # Target — standard chase target
    target = str(ms.get("target", ms.get("chaseTarget", "")) or "")

    # DLS revised target (separate field)
    dls_target = str(ms.get("revisedTarget", ms.get("dlsTarget", "")) or "")

    # Required run rate
    rrr = str(ms.get("requiredRunRate", ms.get("reqRunRate", "")) or "")

    # Innings number — FIX: safe int conversion with try/except
    try:
        innings_num = int(ms.get("inningsId", 1) or 1)
    except (TypeError, ValueError):
        innings_num = 1
    innings_num = max(1, min(innings_num, 4))  # clamp 1–4

    overs_val = str(ms.get("overs", "") or "")
    fmt       = hdr.get("matchFormat", "")
    phase     = _over_phase(overs_val, fmt)
    interruption = _detect_interruption(status_str)
    resumption   = _extract_resumption_time(status_str) if interruption == "rain" else ""

    # Commentary from summary
    comm_raw = []
    mc = data.get("matchCommentary", {})
    for key in ("commentaryList", "matchCommentaryList", "items"):
        val = (mc if isinstance(mc, dict) else {}).get(key)
        if isinstance(val, list) and val:
            comm_raw = val
            break

    commentary = []
    for c in comm_raw[:6]:
        commentary.append({
            "over":    c.get("overNumber", c.get("ballNbr", "")),
            "text":    c.get("commText", c.get("commentary", "")),
            "event":   c.get("event", ""),
            "batsman": (c.get("batsmanStriker") or {}).get("batName", ""),
            "bowler":  (c.get("bowlerStriker")  or {}).get("bowlName", ""),
        })

    return {
        "score":         f"{bat.get('teamScore','?')}/{bat.get('teamWkts','?')}",
        "overs":         overs_val,
        "run_rate":      str(ms.get("currentRunRate", "") or ""),
        "req_rate":      rrr,
        "target":        target,
        "dls_target":    dls_target,
        "last_wicket":   str(ms.get("lastWicket", "") or ""),
        "recent_overs":  str(ms.get("recentOvsStats", "") or ""),
        "win_prob":      win_prob,
        "match_status":  status_str,
        "match_state":   hdr.get("matchState", data.get("matchState", "")),
        "toss":          (hdr.get("toss") or {}).get("decision", ""),
        "venue_name":    venue_name,
        "venue_city":    venue_city,
        "venue_country": venue.get("country", venue.get("location", "")),
        "commentary":    commentary,
        "innings_num":   innings_num,
        "over_phase":    phase,
        "interruption":  interruption,
        "resumption":    resumption,
        "match_format":  fmt,
    }


# ── 3. Ball-by-Ball Fast Refresh ─────────────────────────────────────────────
def fetch_live(match_id: str) -> dict:
    data = _get(f"{BASE}/mcenter/over-refresh/{match_id}")
    if not data:
        return {}

    ms  = data.get("miniscore", {})
    bat = ms.get("batTeam", {})

    striker     = ms.get("batsmanStriker") or ms.get("batStrikerDetails") or {}
    non_striker = ms.get("batsmanNonStriker") or ms.get("batNonStrikerDetails") or {}

    def _parse_batter(b: dict, is_striker: bool) -> dict:
        return {
            "batName":    str(b.get("batName",  b.get("name", "")) or ""),
            "runs":       b.get("batRuns",       b.get("runs", 0)),
            "balls":      b.get("batBalls",      b.get("balls", 0)),
            "fours":      b.get("batFours",      b.get("fours", 0)),
            "sixes":      b.get("batSixes",      b.get("sixes", 0)),
            "strikeRate": str(b.get("batStrikeRate", b.get("strikeRate", "0.00")) or "0.00"),
            "isStriker":  is_striker,
        }

    batsmen = []
    if striker:     batsmen.append(_parse_batter(striker, True))
    if non_striker: batsmen.append(_parse_batter(non_striker, False))

    bowler_raw = ms.get("bowlerStriker") or ms.get("bowlStrikerDetails") or {}
    current_bowler = {}
    if bowler_raw:
        current_bowler = {
            "bowlName": str(bowler_raw.get("bowlName", bowler_raw.get("name", "")) or ""),
            "wickets":  bowler_raw.get("bowlWkts",    bowler_raw.get("wickets", 0)),
            "runs":     bowler_raw.get("bowlRuns",    bowler_raw.get("runs", 0)),
            "overs":    str(bowler_raw.get("bowlOvs", bowler_raw.get("overs", "")) or ""),
            "economy":  str(bowler_raw.get("bowlEcon",bowler_raw.get("economy", "")) or ""),
            "maidens":  bowler_raw.get("bowlMaidens", 0),
        }

    is_free_hit  = bool(ms.get("isFreeHit") or ms.get("freeHit"))
    target       = str(ms.get("target", ms.get("chaseTarget", "")) or "")
    dls_target   = str(ms.get("revisedTarget", ms.get("dlsTarget", "")) or "")

    return {
        "live_score":        f"{bat.get('teamScore','?')}/{bat.get('teamWkts','?')}",
        "live_overs":        str(ms.get("overs", "") or ""),
        "live_crr":          str(ms.get("currentRunRate", "") or ""),
        "live_rrr":          str(ms.get("requiredRunRate", ms.get("reqRunRate", "")) or ""),
        "live_target":       target,
        "live_dls_target":   dls_target,
        "live_batsmen":      batsmen,
        "current_bowler":    current_bowler,
        "last_ball":         str(ms.get("recentOvsStats", "") or ""),
        "last_wicket":       str(ms.get("lastWicket", "") or ""),
        "is_free_hit":       is_free_hit,
        "partnership_runs":  (ms.get("partnerShip") or {}).get("runs", ""),
        "partnership_balls": (ms.get("partnerShip") or {}).get("balls", ""),
    }


# ── 4. Full Scorecard ─────────────────────────────────────────────────────────
def fetch_scorecard(match_id: str) -> dict:
    data = _get(f"{BASE}/mcenter/scorecard/{match_id}")
    if not data:
        return {}

    innings = []
    for card in data.get("scoreCard", []):
        bat_team  = card.get("batTeamDetails", {})
        bowl_team = card.get("bowlTeamDetails", {})
        score_det = card.get("scoreDetails", {})
        extras    = card.get("extrasData", {})
        wickets   = card.get("wicketsData", {})
        partners  = card.get("partnershipsData", {})

        batsmen = []
        for b in _sort_keys(bat_team.get("batsmenData") or {}):
            batsmen.append({
                "name":        str(b.get("batName", "") or ""),
                "runs":        b.get("batRuns",  b.get("runs", 0)),
                "balls":       b.get("batBalls", b.get("balls", 0)),
                "fours":       b.get("batFours", b.get("fours", 0)),
                "sixes":       b.get("batSixes", b.get("sixes", 0)),
                "strike_rate": str(b.get("batStrikeRate", b.get("strikeRate", "0.00")) or "0.00"),
                "out_desc":    str(b.get("outDesc", "batting") or "batting"),
                "is_out":      bool(b.get("outDesc", "")),
            })

        bowlers = []
        for b in _sort_keys(bowl_team.get("bowlersData") or {}):
            bowlers.append({
                "name":    str(b.get("bowlName", "") or ""),
                "overs":   str(b.get("bowlOvs",  b.get("overs", "0")) or "0"),
                "runs":    b.get("bowlRuns",  b.get("runs", 0)),
                "wickets": b.get("bowlWkts",  b.get("wickets", 0)),
                "economy": str(b.get("bowlEcon", b.get("economy", "")) or ""),
                "maidens": b.get("bowlMaidens", 0),
            })

        fow = []
        for _, w in (wickets or {}).items():
            fow.append({
                "runs":   w.get("fowRuns",  0),
                "overs":  str(w.get("fowOver", "") or ""),
                "batter": str(w.get("batName", "") or ""),
            })
        fow.sort(key=lambda x: int(x["runs"]) if str(x["runs"]).isdigit() else 0)

        partnerships = []
        for _, p in (partners or {}).items():
            partnerships.append({
                "bat1":  str(p.get("bat1Name", "") or ""),
                "bat2":  str(p.get("bat2Name", "") or ""),
                "runs":  p.get("totalRuns",  p.get("runs", 0)),
                "balls": p.get("totalBalls", p.get("balls", 0)),
            })

        innings.append({
            "team_name":       str(bat_team.get("batTeamName", "") or ""),
            "runs":            score_det.get("runs",    0),
            "wickets":         score_det.get("wickets", 0),
            "overs":           str(score_det.get("overs", "") or ""),
            "run_rate":        str(score_det.get("runRate", "") or ""),
            "declared":        bool(score_det.get("isDeclared")),
            "extras":          extras,
            "batsmen":         batsmen,
            "bowlers":         bowlers,
            "fall_of_wickets": fow,
            "partnerships":    partnerships,
        })

    return {"innings": innings}


# ── 5. Commentary — correct innings page ─────────────────────────────────────
def fetch_commentary_page(match_id: str, page: int) -> list[dict]:
    """
    page 1 = 1st innings, page 2 = 2nd innings.
    Hard cap at 6 entries — overlay only shows 6 balls.
    """
    data = _get(f"{BASE}/mcenter/{match_id}/full-commentary/{page}")
    if not data:
        return []

    raw = []
    for key in ("commentaryList", "fullCommentaryList", "matchCommentaryList", "commentary", "items"):
        val = data.get(key)
        if isinstance(val, list) and val:
            raw = val
            break
        nested = data.get("matchCommentary", {})
        if isinstance(nested, dict):
            val2 = nested.get(key)
            if isinstance(val2, list) and val2:
                raw = val2
                break

    entries = []
    for c in raw:
        text = c.get("commText", c.get("commentary", c.get("text", "")))
        if not text:
            continue
        entries.append({
            "over":    str(c.get("overNumber", c.get("ballNbr", c.get("over", ""))) or ""),
            "text":    str(text),
            "event":   str(c.get("event", "") or ""),
            "batsman": str((c.get("batsmanStriker") or c.get("batsman") or {}).get("batName", "") or ""),
            "bowler":  str((c.get("bowlerStriker")  or c.get("bowler")  or {}).get("bowlName","") or ""),
            "ts":      c.get("timestamp", 0),
        })
        if len(entries) == 6:
            break

    return entries


# ── 6. Build stream_data ──────────────────────────────────────────────────────
def build_stream_data(meta: dict, summary: dict) -> dict:
    """FIX: removed duplicate 'target' key. All fields present exactly once."""
    venue_parts = [summary.get("venue_name", ""), summary.get("venue_city", "")]
    venue = " • ".join(p for p in venue_parts if p)
    return {
        # Identity
        "sport":          "cricket",
        "match_id":       str(meta.get("matchId", "")),
        "series":         str(meta.get("seriesName", "")),
        "match_desc":     str(meta.get("matchDesc", "")),
        "match_format":   str(summary.get("match_format") or meta.get("matchFormat", "")),
        "team1":          str(meta.get("team1", "")),
        "team2":          str(meta.get("team2", "")),
        "title":          str(meta.get("title", "")),
        "state":          str(meta.get("state", "")),
        # Status
        "status":         str(summary.get("match_status", meta.get("status", ""))),
        "interruption":   str(summary.get("interruption", "")),
        "resumption":     str(summary.get("resumption", "")),
        # Score
        "score":          str(summary.get("score", "")),
        "overs":          str(summary.get("overs", "")),
        "run_rate":       str(summary.get("run_rate", "")),
        "req_rate":       str(summary.get("req_rate", "")),
        "target":         str(summary.get("target", "")),    # ← single occurrence
        "dls_target":     str(summary.get("dls_target", "")),
        "last_wicket":    str(summary.get("last_wicket", "")),
        "recent_overs":   str(summary.get("recent_overs", "")),
        # Win probability
        "win_prob":       summary.get("win_prob", {}),
        # Match info
        "toss":           str(summary.get("toss", "")),
        "venue":          venue,
        # Commentary
        "commentary":     summary.get("commentary", []),
        "live_commentary":     [],
        "innings_num":         summary.get("innings_num", 1),
        "innings_page":        summary.get("innings_num", 1),
        "over_phase":          str(summary.get("over_phase", "")),
        # Live fields (populated by fast poll)
        "scorecard":           {},
        "current_bowler":      {},
        "live_batsmen":        [],
        "live_score":          "",
        "live_overs":          "",
        "live_crr":            "",
        "live_rrr":            "",
        "live_target":         "",
        "live_dls_target":     "",
        "last_ball":           "",
        "is_free_hit":         False,
        "partnership_runs":    "",
        "partnership_balls":   "",
        "last_updated":        "",
        "stream_complete":     False,
        # Schedule
        "match_start_ts":      meta.get("matchStartTs", 0),
    }
