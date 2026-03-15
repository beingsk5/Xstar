"""
Xstar Sports Fetcher v6
=========================
Changes vs v5:
  - Removed dead YouTubeTitleUpdater class (replaced by BroadcastManager in stream.py)
  - Removed YOUTUBE_API_KEY / YOUTUBE_BROADCAST_ID usage
  - All other logic unchanged and working
"""

import json, time, logging, importlib, sys, argparse, threading
from queue import Queue, Empty, Full
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
from priority import assign_streams

POLL_FAST_SEC    = 5
POLL_MEDIUM_SEC  = 12
POLL_SLOW_SEC    = 50
DISC_SEC         = 35
COMM_MAX         = 6
PRE_MATCH_WINDOW = 600

ROOT         = Path(__file__).parent.parent
FRONTEND_DIR = ROOT / "frontend"
HEALTH_FILE  = ROOT / "health.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("XstarFetcher")

SPORT_PROVIDERS = {"cricket": "providers.cricket"}

def load_provider(sport: str):
    return importlib.import_module(SPORT_PROVIDERS[sport])


# ── Thread-safe JSON writer ───────────────────────────────────────────────────
class SafeWriter:
    def __init__(self, maxsize: int = 100):
        self._q = Queue(maxsize=maxsize)
        self._t = threading.Thread(target=self._run, daemon=True, name="SafeWriter")
        self._t.start()

    def write(self, path: Path, data: dict):
        try:
            self._q.put_nowait((path, data))
        except Full:
            self._atomic_write(path, data)

    def _run(self):
        while True:
            try:
                path, data = self._q.get(timeout=1)
                self._atomic_write(path, data)
            except Empty:
                continue
            except Exception as e:
                log.warning(f"SafeWriter: {e}")

    def _atomic_write(self, path: Path, data: dict):
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            tmp.replace(path)
        except Exception as e:
            log.warning(f"Write failed {path}: {e}")


WRITER = SafeWriter()


def read_json(path: Path) -> dict:
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return {}


# ── Per-match polling thread ──────────────────────────────────────────────────
class MatchPoller(threading.Thread):
    def __init__(self, sport: str, match_meta: dict,
                 stream_type: str, out_file: Path):
        super().__init__(daemon=True, name=f"Poller-{stream_type}")
        self.sport        = sport
        self.match_meta   = match_meta
        self.match_id     = str(match_meta.get("matchId", ""))
        self.stream_type  = stream_type
        self.out_file     = out_file
        self.provider     = load_provider(sport)
        self.running      = True
        self._last_slow   = 0
        self._last_medium = 0
        self._comm_page   = 1
        self._last_api_ok = time.time()
        self._prev_dls    = ""

    def L(self):
        return f"[{self.stream_type.upper()}]"

    def run(self):
        log.info(f"{self.L()} Polling: {self.match_meta.get('title')} id={self.match_id}")

        while self.running:
            now = time.time()

            # ── Medium: summary + commentary ─────────────────────────
            if now - self._last_medium >= POLL_MEDIUM_SEC:
                try:
                    summary = self.provider.fetch_summary(self.match_id)
                    stream  = self.provider.build_stream_data(self.match_meta, summary)
                    stream["stream_type"] = self.stream_type

                    # Innings page — never go backwards
                    try:
                        live_innings = int(summary.get("innings_num") or 1)
                    except (TypeError, ValueError):
                        live_innings = 1
                    live_innings   = max(1, min(live_innings, 4))
                    new_page       = min(2, max(self._comm_page, live_innings))
                    if new_page != self._comm_page:
                        log.info(f"{self.L()} Commentary innings {self._comm_page}→{new_page}")
                        self._comm_page = new_page

                    commentary = self.provider.fetch_commentary_page(
                        self.match_id, self._comm_page
                    )
                    stream["live_commentary"] = commentary[:COMM_MAX]
                    stream["innings_page"]    = self._comm_page

                    # DLS announcement flag
                    dls_tgt = summary.get("dls_target", "")
                    if dls_tgt and dls_tgt != self._prev_dls:
                        stream["dls_announcement"] = True
                        log.info(f"{self.L()} DLS target revised: {dls_tgt}")
                        self._prev_dls = dls_tgt
                    else:
                        stream["dls_announcement"] = False

                    # Merge
                    existing = read_json(self.out_file)
                    merged   = {**existing, **stream}
                    for k in ("live_batsmen", "current_bowler", "live_score",
                              "live_overs", "live_crr", "live_rrr",
                              "live_target", "live_dls_target",
                              "last_ball", "is_free_hit",
                              "partnership_runs", "partnership_balls"):
                        if not stream.get(k) and existing.get(k):
                            merged[k] = existing[k]

                    WRITER.write(self.out_file, merged)
                    self._last_api_ok = now

                    log.info(
                        f"{self.L()} {stream.get('score','?')} "
                        f"({stream.get('overs','?')}ov) "
                        f"phase={stream.get('over_phase','')} "
                        f"[{stream.get('interruption') or stream.get('state','')}]"
                    )

                    # Match complete
                    state = (stream.get("state") or "").lower()
                    if "complete" in state or "result" in state:
                        merged["stream_complete"] = True
                        WRITER.write(self.out_file, merged)
                        log.info(f"{self.L()} Match complete")

                except Exception as e:
                    log.warning(f"{self.L()} medium: {e}", exc_info=True)
                self._last_medium = now

            # ── Fast: ball-by-ball ────────────────────────────────────
            try:
                live = self.provider.fetch_live(self.match_id)
                if live:
                    existing = read_json(self.out_file)
                    existing.update(live)
                    existing["last_updated"] = datetime.now(timezone.utc).isoformat()
                    WRITER.write(self.out_file, existing)
                    self._last_api_ok = now
            except Exception as e:
                log.warning(f"{self.L()} fast: {e}")

            # ── Slow: scorecard ───────────────────────────────────────
            if now - self._last_slow >= POLL_SLOW_SEC:
                try:
                    scorecard = self.provider.fetch_scorecard(self.match_id)
                    existing  = read_json(self.out_file)
                    existing["scorecard"] = scorecard
                    WRITER.write(self.out_file, existing)
                except Exception as e:
                    log.warning(f"{self.L()} slow: {e}")
                self._last_slow = now

            # Stale warning
            if time.time() - self._last_api_ok > 120:
                log.warning(
                    f"{self.L()} No API response for "
                    f"{time.time()-self._last_api_ok:.0f}s"
                )

            time.sleep(POLL_FAST_SEC)

        log.info(f"{self.L()} Poller stopped")


# ── Orchestrator ──────────────────────────────────────────────────────────────
def _is_imminent(meta: dict) -> bool:
    ts = meta.get("matchStartTs", 0)
    if not ts:
        return False
    try:
        diff_s = (int(ts) - int(time.time() * 1000)) / 1000
        return 0 <= diff_s <= PRE_MATCH_WINDOW
    except Exception:
        return False


def run(sports: list):
    log.info(f"Xstar Fetcher v6 — sports: {sports}")
    pollers:  dict[str, MatchPoller] = {}
    last_disc = 0

    while True:
        now = time.time()

        if now - last_disc >= DISC_SEC:
            all_matches = []
            for sport in sports:
                try:
                    prov    = load_provider(sport)
                    matches = prov.discover_matches()
                    for m in matches:
                        state = m.get("state", "")
                        if state in ("In Progress", "Preview", "Innings Break"):
                            all_matches.append(m)
                        elif state not in ("Complete", "Result") and _is_imminent(m):
                            m["state"] = "Preview"
                            all_matches.append(m)
                    log.info(
                        f"[{sport}] "
                        f"{len([x for x in all_matches if x.get('sport')==sport])} active"
                    )
                except Exception as e:
                    log.warning(f"Discovery [{sport}]: {e}")

            assignment = assign_streams(all_matches)

            # Health file
            health = {
                "status":        "running",
                "ts":            datetime.now(timezone.utc).isoformat(),
                "active_sports": sports,
                "main_match":    (assignment.get("main")   or {}).get("title", "none"),
                "shorts_match":  (assignment.get("shorts") or {}).get("title", "none"),
                "total_matches": len(all_matches),
            }
            for st in ("main", "shorts"):
                f = FRONTEND_DIR / f"stream_data_{st}.json"
                d = read_json(f)
                lu = d.get("last_updated", "")
                try:
                    age = int(
                        (time.time() - datetime.fromisoformat(lu).timestamp())
                    ) if lu else -1
                except Exception:
                    age = -1
                health[f"{st}_data_age_s"] = age
            WRITER.write(HEALTH_FILE, health)

            for stream_type in ("main", "shorts"):
                meta     = assignment.get(stream_type)
                out_file = FRONTEND_DIR / f"stream_data_{stream_type}.json"

                if meta is None:
                    WRITER.write(out_file, {
                        "stream_type":      stream_type,
                        "state":            "waiting",
                        "status":           "No active match — standby",
                        "title":            "Xstar Sports",
                        "team1": "", "team2": "",
                        "live_commentary":  [],
                        "scorecard":        {},
                        "interruption":     "",
                        "dls_announcement": False,
                    })
                    if stream_type in pollers:
                        pollers[stream_type].running = False
                        del pollers[stream_type]
                    continue

                new_id = str(meta.get("matchId", ""))
                ep     = pollers.get(stream_type)

                if ep is None or ep.match_id != new_id:
                    if ep:
                        ep.running = False
                    p = MatchPoller(
                        meta.get("sport", "cricket"), meta,
                        stream_type, out_file
                    )
                    p.start()
                    pollers[stream_type] = p
                    log.info(f"[{stream_type.upper()}] → {meta.get('title')}")

            last_disc = now

        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sports", nargs="+", default=["cricket"])
    args = parser.parse_args()
    run(args.sports)
