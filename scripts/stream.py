"""
Xstar Sports Stream — Final
=============================
Architecture:
  - StreamSession creates ONE liveStream at startup → permanent RTMP URL
  - FFmpeg always streams to this fixed RTMP URL (never restarts)
  - liveBroadcasts are created/ended per match without touching FFmpeg
  - Slot promotion: old broadcast ends → new broadcast created → bound to same stream
  - Manual key fallback if YOUTUBE_TOKEN_JSON not set
"""

import argparse, subprocess, sys, os, time, signal, logging
import threading, json, urllib.request
from pathlib import Path

log = logging.getLogger("XstarStream")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

ROOT     = Path(__file__).parent.parent
FRONTEND = ROOT / "frontend"
BACKEND  = ROOT / "backend"

CHROMIUM_RESTART_SEC = 7200
COMPLETE_WAIT_SEC    = 600
FFMPEG_RETRY_DELAY   = 8


def notify(msg: str):
    def _send():
        webhook = os.environ.get("DISCORD_WEBHOOK", "")
        if not webhook:
            return
        try:
            payload = json.dumps({"content": f"Xstar Sports — {msg}"}).encode()
            req = urllib.request.Request(
                webhook, data=payload,
                headers={"Content-Type": "application/json"}, method="POST"
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            log.warning(f"Webhook: {e}")
    threading.Thread(target=_send, daemon=True).start()


def read_data(data_file: Path) -> dict:
    try:
        return json.loads(data_file.read_text())
    except Exception:
        return {}


def current_match_id(data_file: Path) -> str:
    try:
        return str(json.loads(data_file.read_text()).get("match_id", ""))
    except Exception:
        return ""


def is_complete(data_file: Path) -> bool:
    try:
        d     = json.loads(data_file.read_text())
        state = (d.get("state") or "").lower()
        return (
            d.get("stream_complete") is True
            or "complete" in state
            or "result" in state
        )
    except Exception:
        return False


def ffmpeg_cmd(display: int, width: int, height: int,
               fps: int, rtmp_url: str) -> list:
    return [
        "ffmpeg", "-y",
        "-f", "x11grab", "-r", str(fps),
        "-s", f"{width}x{height}",
        "-i", f":{display}.0+0,0",
        "-f", "lavfi",
        "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-vcodec", "libx264", "-preset", "veryfast",
        "-tune", "zerolatency",
        "-maxrate", "4500k", "-bufsize", "9000k",
        "-pix_fmt", "yuv420p",
        "-g", str(fps * 2), "-keyint_min", str(fps),
        "-sc_threshold", "0",
        "-acodec", "aac", "-ab", "128k", "-ar", "44100",
        "-f", "flv", rtmp_url,
    ]


def start_xvfb(display_num: int, width: int, height: int) -> subprocess.Popen:
    p = subprocess.Popen(
        ["Xvfb", f":{display_num}",
         "-screen", "0", f"{width}x{height}x24",
         "-ac", "-nolisten", "tcp"],
        stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL
    )
    time.sleep(2)
    log.info(f"Xvfb :{display_num} started ({width}x{height})")
    return p


def launch_chromium(display_num: int, html_file: Path,
                    width: int, height: int) -> subprocess.Popen:
    env = os.environ.copy()
    env["DISPLAY"] = f":{display_num}"
    p = subprocess.Popen([
        "chromium-browser",
        "--no-sandbox", "--disable-setuid-sandbox",
        "--disable-gpu-sandbox", "--disable-dev-shm-usage",
        f"--window-size={width},{height}", "--window-position=0,0",
        "--kiosk", "--force-device-scale-factor=1",
        "--disable-extensions", "--disable-infobars",
        "--disable-translate",
        "--disable-features=TranslateUI,Translate,AutofillServerCommunication",
        "--no-first-run", "--disable-default-apps",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows",
        "--disable-ipc-flooding-protection",
        "--allow-file-access-from-files", "--allow-file-access",
        f"--app=file://{html_file.resolve()}",
    ], env=env, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    time.sleep(6)
    log.info(f"Chromium :{display_num} PID={p.pid}")
    return p


def kill_proc(p, name: str = ""):
    if p is None:
        return
    try:
        p.terminate()
        p.wait(timeout=6)
    except subprocess.TimeoutExpired:
        try: p.kill()
        except Exception: pass
    except Exception:
        pass


def run_stream(label: str, display_num: int, width: int, height: int,
               fps: int, html_file: Path, rtmp_url: str,
               stop_event: threading.Event, data_file: Path,
               session=None):
    """
    session: StreamSession instance or None.
    RTMP URL is fixed for lifetime of this function — FFmpeg never restarts for URL changes.
    Broadcasts are created/ended via session without touching FFmpeg.
    """
    log.info(f"[{label}] Starting {width}x{height} @{fps}fps")
    notify(f"[{label}] Stream starting")

    xvfb           = start_xvfb(display_num, width, height)
    chrome         = launch_chromium(display_num, html_file, width, height)
    chrome_started = time.time()

    env_ff = os.environ.copy()
    env_ff["DISPLAY"] = f":{display_num}"

    cmd    = ffmpeg_cmd(display_num, width, height, fps, rtmp_url)
    ffmpeg = subprocess.Popen(
        cmd, env=env_ff,
        stderr=subprocess.PIPE, stdout=subprocess.DEVNULL
    )
    log.info(f"[{label}] FFmpeg PID={ffmpeg.pid}")

    # Create initial broadcast and go live ~10s after FFmpeg starts
    if session and session.available:
        d = read_data(data_file)
        session.create_broadcast(d)

        def _initial_go_live():
            time.sleep(10)
            if session.go_live():
                notify(f"[{label}] LIVE: {session.broadcast_url}")
                log.info(f"[{label}] YouTube: {session.broadcast_url}")
            else:
                log.warning(f"[{label}] go_live failed — enableAutoStart should handle it")
        threading.Thread(target=_initial_go_live, daemon=True,
                         name=f"GoLive-{label}").start()

    active_match_id = current_match_id(data_file)
    complete_time   = None
    crash_count     = 0

    while not stop_event.is_set():

        # ── Match complete → result screen → stop ─────────────────────
        if is_complete(data_file):
            if complete_time is None:
                log.info(f"[{label}] Match complete — stopping in {COMPLETE_WAIT_SEC}s")
                notify(f"[{label}] Match ended — closing in {COMPLETE_WAIT_SEC//60}min")
                complete_time = time.time()
            elif time.time() - complete_time >= COMPLETE_WAIT_SEC:
                log.info(f"[{label}] Closing after result screen")
                break

        # ── Slot promotion: match_id changed in JSON ──────────────────
        # Fetcher swapped to a new match.
        # session.promote() ends old broadcast, creates + goes live on new one.
        # FFmpeg keeps streaming to same RTMP URL — no interruption.
        new_mid = current_match_id(data_file)
        if (new_mid and new_mid != active_match_id
                and complete_time is None
                and session and session.available):
            log.info(f"[{label}] Slot promotion: {active_match_id} → {new_mid}")
            active_match_id = new_mid
            d = read_data(data_file)

            def _promote(match_data=d, s=session):
                ok = s.promote(match_data)
                if ok:
                    notify(f"[{label}] New match LIVE: {s.broadcast_url}")
                    log.info(f"[{label}] Promoted: {s.broadcast_url}")
                else:
                    log.warning(f"[{label}] Slot promotion broadcast failed")
            threading.Thread(target=_promote, daemon=True,
                             name=f"Promote-{label}").start()

        # ── Chromium watchdog ─────────────────────────────────────────
        if time.time() - chrome_started >= CHROMIUM_RESTART_SEC:
            log.info(f"[{label}] Chromium 2h restart")
            kill_proc(chrome)
            chrome         = launch_chromium(display_num, html_file, width, height)
            chrome_started = time.time()

        # ── FFmpeg crash recovery ─────────────────────────────────────
        if ffmpeg.poll() is not None:
            crash_count += 1
            log.warning(f"[{label}] FFmpeg crash #{crash_count} rc={ffmpeg.returncode}")
            notify(f"[{label}] FFmpeg crash #{crash_count} — restarting")
            time.sleep(FFMPEG_RETRY_DELAY)
            ffmpeg = subprocess.Popen(
                cmd, env=env_ff,
                stderr=subprocess.PIPE, stdout=subprocess.DEVNULL
            )
            log.info(f"[{label}] FFmpeg restarted PID={ffmpeg.pid}")

        time.sleep(4)

    # ── Clean shutdown ────────────────────────────────────────────────
    log.info(f"[{label}] Shutting down (crashes={crash_count})")
    notify(f"[{label}] Stream ended — {crash_count} crash(es)")
    if session and session.available:
        session.end_broadcast()
    kill_proc(ffmpeg, "FFmpeg")
    kill_proc(chrome, "Chromium")
    kill_proc(xvfb,   "Xvfb")


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Xstar Sports Stream")
    parser.add_argument("--main-fps",   type=int, default=24)
    parser.add_argument("--shorts-fps", type=int, default=20)
    args = parser.parse_args()

    token_json    = os.environ.get("YOUTUBE_TOKEN_JSON", "")
    manual_main   = os.environ.get("XSTAR_MAIN_KEY", "")
    manual_shorts = os.environ.get("XSTAR_SHORTS_KEY", "")

    sys.path.insert(0, str(BACKEND))

    main_rtmp    = ""
    shorts_rtmp  = ""
    main_session = None
    shorts_session = None

    if token_json:
        log.info("Mode: auto-broadcast (YOUTUBE_TOKEN_JSON)")
        from youtube_broadcast import StreamSession

        # Create sessions — each creates ONE liveStream = ONE permanent RTMP URL
        main_session = StreamSession(is_shorts=False)
        if main_session.available:
            main_rtmp = main_session.rtmp_url
            log.info(f"Main session ready, RTMP: ...{main_rtmp[-20:]}")
        else:
            log.warning("Main session unavailable — falling back to manual key")
            main_rtmp = manual_main

        # Shorts: only if YOUTUBE_SHORTS_KEY is set
        if manual_shorts:
            shorts_session = StreamSession(is_shorts=True)
            if shorts_session.available:
                shorts_rtmp = shorts_session.rtmp_url
                log.info(f"Shorts session ready")
            else:
                log.warning("Shorts session unavailable — falling back to manual key")
                shorts_rtmp = manual_shorts

    else:
        log.info("Mode: manual RTMP key")
        main_rtmp   = manual_main
        shorts_rtmp = manual_shorts
        base = "rtmps://a.rtmp.youtube.com/live2"
        if main_rtmp and "/" not in main_rtmp:
            main_rtmp = f"{base}/{main_rtmp}"
        if shorts_rtmp and "/" not in shorts_rtmp:
            shorts_rtmp = f"{base}/{shorts_rtmp}"

    if not main_rtmp:
        log.error(
            "No RTMP URL available.\n"
            "  Option A (recommended): Set YOUTUBE_TOKEN_JSON secret\n"
            "  Option B (manual key):  Set YOUTUBE_MAIN_KEY secret"
        )
        sys.exit(1)

    # ── Launch threads ────────────────────────────────────────────────
    stop    = threading.Event()
    threads = []

    t1 = threading.Thread(
        target=run_stream,
        args=("MAIN", 99, 1920, 1080, args.main_fps,
              FRONTEND / "main.html", main_rtmp, stop,
              FRONTEND / "stream_data_main.json",
              main_session),
        daemon=True, name="MAIN"
    )
    threads.append(t1)

    if shorts_rtmp:
        t2 = threading.Thread(
            target=run_stream,
            args=("SHORTS", 100, 1080, 1920, args.shorts_fps,
                  FRONTEND / "shorts.html", shorts_rtmp, stop,
                  FRONTEND / "stream_data_shorts.json",
                  shorts_session),
            daemon=True, name="SHORTS"
        )
        threads.append(t2)
        log.info("Dual stream: MAIN@24fps + SHORTS@20fps")
    else:
        log.info("Single stream: MAIN@24fps only")

    def shutdown(sig, frame):
        log.info("Shutdown signal received")
        stop.set()

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for t in threads:
        t.start()
    log.info(f"{len(threads)} stream thread(s) active")
    for t in threads:
        t.join()

    log.info("All streams stopped.")
    sys.exit(0)
