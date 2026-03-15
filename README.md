# Xstar Sports — Automated YouTube Cricket Stream

Fully automated live cricket streaming. Detects matches, creates YouTube broadcasts,
streams to Main + Shorts simultaneously, and ends cleanly when matches finish.
Zero manual steps after first-time setup.

---

## First-Time Setup (15 minutes, done once, never again)

### Step 1 — Fork this repo

Fork to your GitHub account.

### Step 2 — Enable YouTube Data API

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project called `xyz`
3. **APIs & Services → Enable APIs → YouTube Data API v3 → Enable**
4. **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
5. Application type: **Desktop app** → Create
6. Download the JSON file → save it as `backend/client_secrets.json`

### Step 3 — Run auth once on your PC

```bash
cd backend
python youtube_broadcast.py --auth
```

A browser opens → sign in with your YouTube channel account → done.

The terminal prints your `token.json` contents. Copy the entire JSON output.

### Step 4 — Add GitHub Secrets

Go to: **Your repo → Settings → Secrets and variables → Actions → New secret**

| Secret Name | Value | Required |
|-------------|-------|----------|
| `YOUTUBE_TOKEN_JSON` | Paste the JSON from Step 3 | ✅ Required |
| `YOUTUBE_SHORTS_KEY` | YouTube stream key for shorts channel | Optional |
| `DISCORD_WEBHOOK` | Discord webhook URL for crash alerts | Optional |

> **YOUTUBE_SHORTS_KEY** — only needed if you want a separate Shorts stream.
> Get it from: YouTube Studio → Go Live → Stream → Stream Key (copy just the key, not the full URL)

### Step 5 — Enable GitHub Actions

**Your repo → Actions tab → Enable workflows**

**Done.** From now on, everything runs automatically forever.

---

## How It Works

```
Every 15 minutes:
  GitHub Actions cron → scheduler.py checks Cricbuzz for live/imminent matches
        │
  Match found?
        │ YES
        ↓
  fetcher.py starts — polls Cricbuzz every 5-50s
  writes stream_data_main.json + stream_data_shorts.json
        │
        ↓
  youtube_broadcast.py — creates YouTube broadcast for each stream
  Title + description set once with SEO keywords and hashtags
        │
        ↓
  Xvfb + Chromium renders the HTML overlay
  FFmpeg captures and streams to YouTube
        │
  YouTube goes LIVE automatically
        │
  Match ends → result screen 10 min → broadcast ends → job exits

Every 25 minutes:
  Watchdog checks if stream is running but match is live
  If stream died → auto-triggers restart
```

---

## What Happens With Multiple Matches

| Situation | Result |
|-----------|--------|
| 1 match live | Streams to MAIN only |
| 2 matches live | #1 ranked → MAIN, #2 ranked → SHORTS |
| 3+ matches live | #1 → MAIN, #2 → SHORTS, rest wait in queue |
| MAIN match ends | #2 moves to MAIN, #3 moves to SHORTS automatically |
| New higher-priority match starts | Replaces lower-priority in slot |

Match priority is based on: format weight + series importance + team popularity + rivalry bonus.
Example: India vs Pakistan World Cup Final always beats any other match for the MAIN slot.

---

## Priority Ranking

| Factor | Examples | Points |
|--------|---------|--------|
| Format | Test=100, IPL=90, ODI=85, T20I=80, T20=75 | Up to 100 |
| Series | World Cup+50, Champions Trophy+45, Final+40 | Up to 50 |
| Teams | India+30, Australia+22, England/Pakistan+20 | Up to 60 |
| Rivalry | IND-PAK+25, Ashes+20, BGT+18 | Up to 25 |
| State | In Progress+30, Innings Break+20 | Up to 30 |

---

## YouTube Broadcast Details

### What gets set automatically at stream start:

**Main stream title example:**
```
India vs Pakistan | Final | 🏏 ODI | ICC Champions Trophy
```

**Shorts stream title example:**
```
India vs Pakistan | Final | 🏏 ODI | #Shorts
```

**Description (auto-generated per match):**
```
🔴 LIVE NOW — India vs Pakistan
🏏 ODI | Final

📍 Dubai International Cricket Stadium
🏆 ICC Champions Trophy 2025
🪙 Toss: India won the toss and elected to bat

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📺 Xstar Sports — Live Cricket
🔔 Subscribe and turn on notifications
━━━━━━━━━━━━━━━━━━━━━━━━━━━

#ChampionsTrophy #CricketLive #INDvPAK #India #ODI #Pakistan #XstarSports
```

Title and description are **set once at broadcast creation and never changed.**

### Stream settings:
| | Main (1920×1080) | Shorts (1080×1920) |
|--|-----------------|-------------------|
| Resolution | 1080p | 1080p |
| Frame rate | 30fps | variable |
| Latency | Low (~5-10s) | Ultra-low |
| DVR (rewind) | Enabled | Disabled |
| Category | Sports (17) | Sports (17) |
| FPS for encoding | 24fps | 20fps |

---

## Overlay Features

### Main Stream (1920×1080)
- Live match info: series, match type, format, venue
- Both team scores with batting team highlighted
- Target banner during chase
- CRR / RRR / Overs / Last Over stats
- Over phase: POWERPLAY / MIDDLE / DEATH
- Win probability bar (tied state handled)
- Partnership live display
- Rotating scorecard: Batting → Bowling → Partnerships → Fall of Wickets (15s each)
- Innings selector: switch between 1st and 2nd innings
- Permanent 6-ball commentary (always visible, never rotates away)
- 1ST / 2ND INNINGS pill indicator
- Live batsmen + current bowler cards
- This-over balls track (colour coded)
- Scrolling ticker

### Shorts Stream (1080×1920)
- Large hero score with team flags
- Target banner during chase
- CRR / RRR / Overs / Last Over mini stats
- Win probability bar
- Top scorer + best bowler strip
- Two batsmen side-by-side
- Bowler + this-over balls
- 6-ball commentary with innings pill
- Ticker

### Event Animations
WICKET · CAUGHT · LBW · RUN OUT · STUMPED · FOUR · SIX · NO BALL · FREE HIT · DRS REVIEW · 50 · 100 · END OF OVER · DLS TARGET REVISED

### Special Screens
- Skeleton loader on cold start
- Countdown screen before match starts
- Innings Break screen
- Rain / Bad Light / Lunch / Tea / Drinks / Injury / Abandoned / DLS / Suspended interruption screens (each with resumption time if available)
- Match Result screen (shown 10 min after match ends)
- Data Delayed badge (if API data goes stale)

---

## API Usage

### Cricbuzz (match data)
Unofficial API, no published quota. ~1,400 calls/hr per stream. Rate limiting handled with exponential backoff.

### YouTube Data API v3 (broadcast management)
Default quota: 10,000 units/day

| Scenario | Units used | % of daily limit |
|----------|-----------|-----------------|
| 1 match, 2 streams | 520 | 5.2% |
| Normal day, 2 matches | 1,040 | 10.4% |
| Tournament day, 8 matches | 4,160 | 41.6% |
| Busiest possible, 15 matches | 7,800 | 78% |

Title and description are set **once per broadcast** — no ongoing API calls for updates.

If you ever need more quota: [console.cloud.google.com → YouTube API → Quotas → Request increase](https://console.cloud.google.com) (free, approved in minutes, typically 50,000 units/day granted).

---

## Secrets Reference

| Secret | Purpose | Where to get it |
|--------|---------|----------------|
| `YOUTUBE_TOKEN_JSON` | OAuth2 token for auto-broadcast | Run `python backend/youtube_broadcast.py --auth` |
| `YOUTUBE_SHORTS_KEY` | Shorts stream key (optional) | YouTube Studio → Go Live → Stream Key |
| `DISCORD_WEBHOOK` | Crash/restart alerts (optional) | Discord → Server Settings → Integrations → Webhooks |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Stream not starting | Check YOUTUBE_TOKEN_JSON secret is set correctly |
| "No auth code received" | Make sure port 8080 is free when running `--auth` |
| Only main stream | Set YOUTUBE_SHORTS_KEY secret |
| Black screen | Chromium install failed — check Actions logs |
| Data not updating | Check fetcher.log in Actions artifacts |
| Stream cuts off mid-match | Switch to self-hosted runner (see SELF_HOSTED_RUNNER.md) |
| No Discord alerts | Set DISCORD_WEBHOOK secret |
| YouTube broadcast not appearing | Token may be expired — re-run `--auth` and update secret |

---

## Long Matches (Test cricket, full-day ODIs)

GitHub's free tier caps jobs at 6 hours. A Test match runs 5 days.

See **SELF_HOSTED_RUNNER.md** for the complete guide to setting up a cheap VPS (~€6/month on Hetzner) that runs indefinitely.

The watchdog workflow (`restart.yml`) automatically restarts the stream every time the runner hits its limit — but with a self-hosted runner you never hit any limit.

---

## Adding a New Sport

1. Create `backend/providers/football.py` with these functions:
```python
def discover_matches() -> list[dict]: ...
def fetch_summary(match_id: str) -> dict: ...
def fetch_live(match_id: str) -> dict: ...
def fetch_scorecard(match_id: str) -> dict: ...
def fetch_commentary_page(match_id: str, page: int) -> list[dict]: ...
def build_stream_data(meta: dict, summary: dict) -> dict: ...
```

2. Register in `backend/fetcher.py`:
```python
SPORT_PROVIDERS = {
    "cricket":  "providers.cricket",
    "football": "providers.football",
}
```

3. Register in `backend/scheduler.py`:
```python
MONITORED_SPORTS = ["cricket", "football"]
```

---

## Repository Structure

```
xstar-sports/
├── .github/workflows/
│   ├── stream.yml          Main stream (cron every 15 min)
│   └── restart.yml         Watchdog (cron every 25 min, auto-restart)
│
├── backend/
│   ├── fetcher.py          Dual-stream data orchestrator
│   ├── scheduler.py        Match detection (pre-match aware, always exits 0)
│   ├── priority.py         Match ranking engine
│   ├── parse_schedule.py   Parses scheduler output → GitHub Actions outputs
│   ├── write_placeholder.py Writes initial data files before fetcher starts
│   ├── verify_data.py      Confirms live data is flowing (diagnostic only)
│   ├── watchdog_check.py   GitHub API check — is stream running?
│   ├── youtube_broadcast.py YouTube API: create, go-live, end broadcasts
│   └── providers/
│       └── cricket.py      Cricbuzz API (all endpoints, all edge cases handled)
│
├── frontend/
│   ├── main.html           Main overlay 1920×1080
│   ├── shorts.html         Shorts overlay 1080×1920
│   ├── stream_data_main.json   Live data bridge (main)
│   ├── stream_data_shorts.json Live data bridge (shorts)
│   └── fonts/
│       └── download-fonts.sh   Downloads fonts at stream start (fallback to system fonts)
│
├── scripts/
│   └── stream.py           Dual FFmpeg engine + YouTube broadcast lifecycle
│
├── SELF_HOSTED_RUNNER.md   VPS setup for Test matches / long streams
└── README.md               This file
```
