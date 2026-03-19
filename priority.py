"""
youtube_broadcast.py — Xstar Sports Broadcast Manager
FIX: Use 'variable' frameRate and omit resolution → no HTTP 400.
     All streaming via YouTube Data API v3 OAuth2 — NO RTMP KEYS NEEDED.
"""

import os, json, time, logging, re, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta

log = logging.getLogger("YTBroadcast")

API       = "https://www.googleapis.com/youtube/v3"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES    = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]

FORMAT_ICONS = {
    "TEST": "🏏 TEST MATCH", "ODI": "🏏 ODI", "T20I": "🏏 T20I",
    "T20":  "🏏 T20",        "T10": "🏏 T10", "IPL":  "🏏 IPL",
    "PSL":  "🏏 PSL",        "BBL": "🏏 BBL", "CPL":  "🏏 CPL",
    "SA20": "🏏 SA20",       "ILT20": "🏏 ILT20",
    "THE HUNDRED": "🏏 THE HUNDRED",
}

FORMAT_TAGS = {
    "TEST":  ["#TestCricket", "#TestMatch", "#Cricket"],
    "ODI":   ["#ODI", "#CricketLive", "#OneDay"],
    "T20I":  ["#T20I", "#T20Cricket", "#T20International"],
    "T20":   ["#T20", "#T20Cricket", "#T20Live"],
    "IPL":   ["#IPL", "#IPL2026", "#CricketLive"],
    "PSL":   ["#PSL", "#PSL2026", "#CricketLive"],
    "BBL":   ["#BBL", "#BigBashLeague", "#CricketLive"],
    "CPL":   ["#CPL", "#CricketLive"],
    "SA20":  ["#SA20", "#CricketLive"],
}

TEAM_TAGS = {
    "india":        ["#India", "#TeamIndia", "#IND"],
    "pakistan":     ["#Pakistan", "#TeamPakistan", "#PAK"],
    "australia":    ["#Australia", "#TeamAustralia", "#AUS"],
    "england":      ["#England", "#TeamEngland", "#ENG"],
    "south africa": ["#SouthAfrica", "#SA", "#Proteas"],
    "new zealand":  ["#NewZealand", "#NZ", "#BlackCaps"],
    "west indies":  ["#WestIndies", "#WI"],
    "sri lanka":    ["#SriLanka", "#SL"],
    "bangladesh":   ["#Bangladesh"],
    "afghanistan":  ["#Afghanistan", "#AFG"],
    "mumbai":       ["#MumbaiIndians", "#MI"],
    "chennai":      ["#CSK", "#ChennaiSuperKings"],
    "kolkata":      ["#KKR", "#KolkataKnightRiders"],
    "delhi":        ["#DC", "#DelhiCapitals"],
    "rajasthan":    ["#RR", "#RajasthanRoyals"],
    "punjab":       ["#PBKS", "#PunjabKings"],
    "hyderabad":    ["#SRH", "#SunrisersHyderabad"],
    "bangalore":    ["#RCB", "#RoyalChallengersBangalore"],
    "lahore":       ["#LahoreQalandars", "#LQ"],
    "karachi":      ["#KarachiKings", "#KK"],
    "peshawar":     ["#PeshawarZalmi", "#PZ"],
    "quetta":       ["#QuettaGladiators", "#QG"],
}

SERIES_TAGS = {
    "world cup":        ["#WorldCup", "#CWC"],
    "champions trophy": ["#ChampionsTrophy", "#CT25"],
    "t20 world cup":    ["#T20WorldCup", "#WT20"],
    "asia cup":         ["#AsiaCup"],
    "ipl":              ["#IPL2026", "#IPL", "#TATAIPL"],
    "psl":              ["#PSL2026", "#PSL", "#HBLPSL"],
    "ashes":            ["#TheAshes", "#Ashes"],
    "border-gavaskar":  ["#BGT", "#BorderGavaskarTrophy"],
    "bbl":              ["#BigBash", "#BBL"],
    "sa20":             ["#SA20"],
    "cpl":              ["#CPL"],
}

RIVALRY_TAGS = {
    frozenset(["india", "pakistan"]):     ["#IndVsPak", "#INDvPAK", "#IndPak"],
    frozenset(["india", "australia"]):    ["#IndVsAus", "#INDvAUS", "#BGT"],
    frozenset(["australia", "england"]):  ["#TheAshes", "#Ashes", "#AUSvENG"],
    frozenset(["india", "england"]):      ["#IndVsEng", "#INDvENG"],
    frozenset(["pakistan", "australia"]): ["#PakVsAus", "#PAKvAUS"],
}


def _hashtags(d: dict, is_shorts: bool = False) -> str:
    tags = set()
    fmt = (d.get("match_format") or "").upper()
    for key, vals in FORMAT_TAGS.items():
        if key in fmt:
            tags.update(vals)
            break
    else:
        tags.update(["#Cricket", "#CricketLive"])
    t1l = (d.get("team1") or "").lower()
    t2l = (d.get("team2") or "").lower()
    for key, vals in TEAM_TAGS.items():
        if key in t1l: tags.update(vals[:2])
        if key in t2l: tags.update(vals[:2])
    sl = (d.get("series") or "").lower()
    for key, vals in SERIES_TAGS.items():
        if key in sl:
            tags.update(vals)
            break
    team_keys = {k for k in TEAM_TAGS if k in t1l or k in t2l}
    for pair, vals in RIVALRY_TAGS.items():
        if pair.issubset(team_keys):
            tags.update(vals)
            break
    tags.add("#CricketLive")
    tags.add("#XstarSports")
    if is_shorts:
        tags.add("#Shorts")
        tags.add("#CricketShorts")
    return " ".join(sorted(tags)[:15])


def build_seo_title(d: dict, is_shorts: bool = False) -> str:
    t1     = d.get("team1", "")
    t2     = d.get("team2", "")
    desc   = d.get("match_desc", "")
    fmt    = (d.get("match_format") or "").upper()
    series = d.get("series", "")
    icon   = FORMAT_ICONS.get(fmt, "🏏 LIVE")
    series_short = re.sub(r'\b20\d\d\b', '', series).strip().strip(',').strip()
    if not t1:
        return "Xstar Sports Live Cricket"
    if is_shorts:
        title = f"{t1} vs {t2} | {desc} | {icon} | #Shorts"
    else:
        title = f"{t1} vs {t2} | {desc} | {icon} | {series_short}"
    return title[:100]


def build_seo_description(d: dict, is_shorts: bool = False) -> str:
    t1    = d.get("team1", "")
    t2    = d.get("team2", "")
    desc  = d.get("match_desc", "")
    fmt   = (d.get("match_format") or "").upper()
    icon  = FORMAT_ICONS.get(fmt, "🏏 LIVE")
    venue = d.get("venue", "")
    series= d.get("series", "")
    toss  = d.get("toss", "")
    htags = _hashtags(d, is_shorts=is_shorts)
    lines = [f"🔴 LIVE NOW — {t1} vs {t2}", f"{icon} | {desc}", ""]
    if venue:  lines.append(f"📍 {venue}")
    if series: lines.append(f"🏆 {series}")
    if toss:   lines.append(f"🪙 Toss: {toss}")
    lines += ["", "━━━━━━━━━━━━━━━━━━━━━━━━━━━",
              "📺 Xstar Sports — Live Cricket",
              "🔔 Subscribe and turn on notifications",
              "━━━━━━━━━━━━━━━━━━━━━━━━━━━", "", htags]
    return "\n".join(lines)


class _TokenManager:
    def __init__(self):
        self._data = None
        self._token = None
        self._expiry = 0

    def load(self) -> bool:
        raw = os.environ.get("YOUTUBE_TOKEN_JSON", "")
        if not raw:
            local = Path(__file__).parent / "token.json"
            if local.exists():
                raw = local.read_text()
        if not raw:
            log.warning("YOUTUBE_TOKEN_JSON not set")
            return False
        try:
            self._data = json.loads(raw)
            return True
        except Exception as e:
            log.error(f"Token parse error: {e}")
            return False

    def token(self) -> str:
        if self._token and time.time() < self._expiry - 60:
            return self._token
        if not self._data:
            raise RuntimeError("Token not loaded")
        rt = self._data.get("refresh_token", "")
        ci = self._data.get("client_id", "")
        cs = self._data.get("client_secret", "")
        if not all([rt, ci, cs]):
            raise RuntimeError("Token JSON missing fields")
        payload = urllib.parse.urlencode({
            "grant_type": "refresh_token", "refresh_token": rt,
            "client_id": ci, "client_secret": cs,
        }).encode()
        req = urllib.request.Request(
            TOKEN_URL, data=payload, method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = json.loads(r.read())
        self._token  = resp["access_token"]
        self._expiry = time.time() + resp.get("expires_in", 3600)
        log.info("Token refreshed")
        return self._token


class StreamSession:
    """
    YouTube Live streaming via API only. No RTMP keys needed.
    Token from YOUTUBE_TOKEN_JSON secret → run --auth once to generate.
    """

    def __init__(self, is_shorts: bool = False):
        self._tm           = _TokenManager()
        self._loaded       = self._tm.load()
        self._is_shorts    = is_shorts
        self._stream_id    = None
        self._rtmp_url     = ""
        self._broadcast_id = None
        if self._loaded:
            self._create_stream()

    def _req(self, method, url, body=None, params=None):
        token = self._tm.token()
        if params:
            url = url + "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode() if body else None
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type":  "application/json",
            "Accept":        "application/json",
        }
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            raise RuntimeError(f"HTTP Error {e.code}: {err}")

    def _create_stream(self):
        """
        Creates liveStream via YouTube API.
        KEY FIX: frameRate='variable', no resolution field.
        Setting frameRate='30fps' or resolution='1080p' causes HTTP 400
        on standard/unverified channels. 'variable' works universally.
        """
        label = "Shorts" if self._is_shorts else "Main"
        try:
            stream = self._req("POST", f"{API}/liveStreams", body={
                "snippet": {"title": f"Xstar Sports — {label}"},
                "cdn": {
                    "frameRate":     "variable",   # FIX: was '30fps' → HTTP 400
                    "ingestionType": "rtmp",
                    # FIX: resolution field removed — caused HTTP 400 on standard channels
                },
            }, params={"part": "snippet,cdn"})

            self._stream_id = stream["id"]
            ingestion       = stream.get("cdn", {}).get("ingestionInfo", {})
            base            = ingestion.get("ingestionAddress", "").rstrip("/")
            key             = ingestion.get("streamName", "")
            self._rtmp_url  = f"{base}/{key}"
            log.info(f"✅ liveStream created via API: {self._stream_id} ({label})")
            log.info(f"   RTMP URL obtained from API — no manual key needed")
        except Exception as e:
            log.error(f"liveStream creation failed: {e}")
            self._loaded = False

    def create_broadcast(self, match_data: dict) -> bool:
        if not self._loaded or not self._stream_id:
            return False
        title       = build_seo_title(match_data, self._is_shorts)
        description = build_seo_description(match_data, self._is_shorts)
        start_time  = (
            datetime.now(timezone.utc) + timedelta(seconds=30)
        ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        try:
            broadcast = self._req("POST", f"{API}/liveBroadcasts", body={
                "snippet": {
                    "title":              title,
                    "description":        description[:5000],
                    "scheduledStartTime": start_time,
                    "categoryId":         "17",
                },
                "status": {
                    "privacyStatus":           "public",
                    "selfDeclaredMadeForKids": False,
                },
                "contentDetails": {
                    "enableAutoStart":   True,
                    "enableAutoStop":    False,
                    "enableDvr":         not self._is_shorts,
                    "latencyPreference": "ultraLow" if self._is_shorts else "low",
                    "monitorStream":     {"enableMonitorStream": False},
                },
            }, params={"part": "snippet,status,contentDetails"})

            self._broadcast_id = broadcast["id"]
            log.info(f"Broadcast created: {self._broadcast_id} — {title}")

            self._req("POST", f"{API}/liveBroadcasts/bind",
                      params={
                          "id":       self._broadcast_id,
                          "part":     "id,contentDetails",
                          "streamId": self._stream_id,
                      })
            log.info(f"Broadcast bound to stream {self._stream_id}")
            return True
        except Exception as e:
            log.error(f"create_broadcast failed: {e}")
            return False

    def go_live(self, max_wait: int = 120) -> bool:
        if not self._broadcast_id or not self._stream_id or not self._loaded:
            return False
        log.info("Waiting for stream to become active...")
        for _ in range(max_wait // 5):
            try:
                resp   = self._req("GET", f"{API}/liveStreams",
                                   params={"part": "status", "id": self._stream_id})
                items  = resp.get("items", [])
                status = (items[0].get("status", {}).get("streamStatus", "") if items else "")
                log.info(f"Stream status: {status}")
                if status == "active":
                    break
            except Exception as e:
                log.warning(f"Status check: {e}")
            time.sleep(5)
        else:
            log.warning("Stream not active after wait — trying go_live anyway")
        try:
            self._req("POST", f"{API}/liveBroadcasts/transition",
                      params={"broadcastStatus": "live", "id": self._broadcast_id, "part": "id,status"})
            log.info(f"Broadcast {self._broadcast_id} → LIVE ✅")
            return True
        except RuntimeError as e:
            if "redundantTransition" in str(e) or "redundant" in str(e).lower():
                log.info(f"Broadcast already LIVE (auto-started) ✅")
                return True
            log.error(f"go_live failed: {e}")
            return False
        except Exception as e:
            log.error(f"go_live failed: {e}")
            return False

    def end_broadcast(self) -> bool:
        if not self._broadcast_id or not self._loaded:
            return False
        try:
            self._req("POST", f"{API}/liveBroadcasts/transition",
                      params={"broadcastStatus": "complete", "id": self._broadcast_id, "part": "id,status"})
            log.info(f"Broadcast {self._broadcast_id} → COMPLETE")
            self._broadcast_id = None
            return True
        except Exception as e:
            log.error(f"end_broadcast failed: {e}")
            return False

    def promote(self, match_data: dict) -> bool:
        log.info("Slot promotion — ending old broadcast, creating new one")
        self.end_broadcast()
        ok = self.create_broadcast(match_data)
        if ok:
            time.sleep(3)
            return self.go_live(max_wait=60)
        return False

    @property
    def available(self) -> bool:
        return self._loaded and bool(self._stream_id)

    @property
    def rtmp_url(self) -> str:
        return self._rtmp_url

    @property
    def broadcast_url(self) -> str:
        if self._broadcast_id:
            return f"https://www.youtube.com/watch?v={self._broadcast_id}"
        return ""


def run_auth():
    import webbrowser, http.server, threading, sys
    secrets_path = Path(__file__).parent / "client_secrets.json"
    if not secrets_path.exists():
        print("\nERROR: client_secrets.json not found.")
        print("Download from: console.cloud.google.com")
        print("  APIs & Services → Credentials → OAuth 2.0 → Download JSON")
        print(f"  Save as: {secrets_path}")
        sys.exit(1)
    with open(secrets_path) as f:
        raw = json.load(f)
    creds = raw.get("installed") or raw.get("web") or {}
    cid   = creds.get("client_id", "")
    cs    = creds.get("client_secret", "")
    redir = "http://localhost:8080"
    if not cid:
        print("ERROR: client_secrets.json missing client_id"); sys.exit(1)
    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redir, "response_type": "code",
        "scope": " ".join(SCOPES), "access_type": "offline", "prompt": "consent",
    })
    auth_code = [None]
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            p = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if "code" in p: auth_code[0] = p["code"][0]
            self.send_response(200); self.end_headers()
            self.wfile.write(b"<h1>Done! Close this tab.</h1>")
        def log_message(self, *_): pass
    server = http.server.HTTPServer(("localhost", 8080), Handler)
    t = threading.Thread(target=server.handle_request, daemon=True)
    t.start()
    print("\nOpening browser for Google sign-in...")
    webbrowser.open(auth_url)
    t.join(timeout=120)
    if not auth_code[0]:
        print("ERROR: No auth code received"); sys.exit(1)
    payload = urllib.parse.urlencode({
        "code": auth_code[0], "client_id": cid, "client_secret": cs,
        "redirect_uri": redir, "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=payload, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=15) as r:
        tokens = json.loads(r.read())
    token_data = {
        "refresh_token": tokens.get("refresh_token", ""),
        "client_id": cid, "client_secret": cs,
        "token_uri": TOKEN_URL, "scopes": SCOPES,
    }
    token_path = Path(__file__).parent / "token.json"
    token_path.write_text(json.dumps(token_data, indent=2))
    print(f"\n✅ token.json saved")
    print("\nPaste this into GitHub secret  YOUTUBE_TOKEN_JSON :")
    print("-" * 60)
    print(json.dumps(token_data, indent=2))
    print("-" * 60)
    print("\nDone. No RTMP keys needed ever again.")


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    if "--auth" in sys.argv:
        run_auth()
    else:
        print("Usage:  python youtube_broadcast.py --auth")
