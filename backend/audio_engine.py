"""
audio_engine.py — Xstar Sports Cricket Audio Engine
=====================================================
Generates 100% copyright-free cricket atmosphere audio by:
  - Looping ambient crowd noise continuously
  - Overlaying event sounds on: FOUR, SIX, WICKET, MILESTONE, SUPER OVER
  - Writing raw PCM to a named pipe for FFmpeg to encode

All audio is synthesized mathematically using Python's wave module.
No external audio files needed. Completely copyright-free.

Usage (called by stream.py):
  engine = AudioEngine(data_file, pipe_path, audio_dir)
  engine.start()   # runs in background thread
  engine.stop()
"""

import os, wave, struct, math, time, threading, json, logging
from pathlib import Path

log = logging.getLogger("AudioEngine")

SAMPLE_RATE   = 44100
CHANNELS      = 2
SAMPLE_WIDTH  = 2   # 16-bit
CHUNK_SIZE    = 4096 # samples per write chunk


# ── Audio file generator ──────────────────────────────────────────────────

def _noise(amp, n):
    """Gaussian noise."""
    import random
    return [random.gauss(0, amp) for _ in range(n)]

def _sine(freq, amp, n):
    return [amp * math.sin(2 * math.pi * freq * i / SAMPLE_RATE) for i in range(n)]

def _envelope(sig, attack, decay, sustain_level, release):
    n = len(sig)
    out = list(sig)
    for i in range(n):
        if i < attack:
            gain = i / max(1, attack)
        elif i < attack + decay:
            gain = 1.0 - (1.0 - sustain_level) * (i - attack) / max(1, decay)
        elif i < n - release:
            gain = sustain_level
        else:
            gain = sustain_level * max(0, n - i) / max(1, release)
        out[i] = sig[i] * gain
    return out

def _lowpass(sig, alpha):
    """Simple first-order lowpass. alpha = cutoff_fraction (0-1)."""
    out = [0.0] * len(sig)
    for i in range(1, len(sig)):
        out[i] = out[i-1] + alpha * (sig[i] - out[i-1])
    return out

def _mix(*signals):
    n = min(len(s) for s in signals)
    return [sum(s[i] for s in signals) for i in range(n)]

def _to_bytes(samples_l, samples_r=None):
    if samples_r is None:
        samples_r = samples_l
    out = bytearray()
    for l, r in zip(samples_l, samples_r):
        lc = max(-32767, min(32767, int(l * 32767)))
        rc = max(-32767, min(32767, int(r * 32767)))
        out += struct.pack('<hh', lc, rc)
    return bytes(out)

def _write_wav(path, samples_l, samples_r=None):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(CHANNELS)
        w.setsampwidth(SAMPLE_WIDTH)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(_to_bytes(samples_l, samples_r))


def generate_audio_files(audio_dir: Path):
    """Generate all cricket audio files. Called once at startup if missing."""
    audio_dir.mkdir(parents=True, exist_ok=True)

    # ── Ambient crowd (3s seamless loop) ─────────────────────────────────
    p = audio_dir / "ambient_crowd.wav"
    if not p.exists():
        n = 3 * SAMPLE_RATE
        import random
        random.seed(42)  # deterministic for seamless loop
        base = _noise(0.08, n)
        low  = _lowpass(_noise(0.12, n), 0.003)
        mid  = _lowpass(_noise(0.06, n), 0.015)
        swell = [0.65 + 0.35 * math.sin(2*math.pi*0.15*i/SAMPLE_RATE) for i in range(n)]
        l = [swell[i] * (base[i] + low[i] + mid[i]) for i in range(n)]
        random.seed(43)
        base2 = _noise(0.08, n)
        r = [swell[i] * (base2[i] + low[i] + mid[i]) for i in range(n)]
        _write_wav(p, l, r)
        log.info("Generated ambient_crowd.wav")

    # ── Boundary cheer (2s) ───────────────────────────────────────────────
    p = audio_dir / "boundary_cheer.wav"
    if not p.exists():
        n = 2 * SAMPLE_RATE
        b = _mix(_noise(0.4, n), _lowpass(_noise(0.6, n), 0.008), _lowpass(_noise(0.4, n), 0.02))
        att = int(0.08 * SAMPLE_RATE)
        cheer = _envelope(b, att, int(0.12*SAMPLE_RATE), 0.85, int(0.8*SAMPLE_RATE))
        _write_wav(p, cheer)
        log.info("Generated boundary_cheer.wav")

    # ── Six cheer (2.5s — bigger) ─────────────────────────────────────────
    p = audio_dir / "six_cheer.wav"
    if not p.exists():
        n = int(2.5 * SAMPLE_RATE)
        b = _mix(_noise(0.45, n), _lowpass(_noise(0.7, n), 0.007), _lowpass(_noise(0.5, n), 0.018))
        att = int(0.06 * SAMPLE_RATE)
        six = _envelope(b, att, int(0.15*SAMPLE_RATE), 0.92, int(1.0*SAMPLE_RATE))
        _write_wav(p, six)
        log.info("Generated six_cheer.wav")

    # ── Wicket roar (3s — most dramatic) ─────────────────────────────────
    p = audio_dir / "wicket_roar.wav"
    if not p.exists():
        n = 3 * SAMPLE_RATE
        b = _mix(_noise(0.5, n), _lowpass(_noise(0.8, n), 0.006), _lowpass(_noise(0.55, n), 0.016))
        att = int(0.05 * SAMPLE_RATE)
        roar = _envelope(b, att, int(0.2*SAMPLE_RATE), 0.95, int(1.2*SAMPLE_RATE))
        boom_dur = int(0.35 * SAMPLE_RATE)
        boom = [math.exp(-5*i/boom_dur) * math.sin(2*math.pi*55*i/SAMPLE_RATE) * 0.5
                for i in range(boom_dur)] + [0.0]*(n-boom_dur)
        final = [roar[i] + boom[i] for i in range(n)]
        _write_wav(p, final)
        log.info("Generated wicket_roar.wav")

    # ── Milestone cheer (2s — 50/100) ────────────────────────────────────
    p = audio_dir / "milestone_cheer.wav"
    if not p.exists():
        n = 2 * SAMPLE_RATE
        b = _mix(_noise(0.38, n), _lowpass(_noise(0.55, n), 0.009))
        att = int(0.12 * SAMPLE_RATE)
        mile = _envelope(b, att, int(0.12*SAMPLE_RATE), 0.80, int(0.7*SAMPLE_RATE))
        _write_wav(p, mile)
        log.info("Generated milestone_cheer.wav")

    # ── Super Over jingle (1.5s) ──────────────────────────────────────────
    p = audio_dir / "super_over.wav"
    if not p.exists():
        n = int(1.5 * SAMPLE_RATE)
        notes = [523, 659, 784, 1047]
        jingle = [0.0] * n
        note_dur = n // (len(notes) + 1)
        for idx, freq in enumerate(notes):
            start = idx * note_dur
            for i in range(note_dur):
                if start + i < n:
                    g = math.exp(-3.5 * i / note_dur)
                    jingle[start+i] += (
                        math.sin(2*math.pi*freq*(start+i)/SAMPLE_RATE)*0.35 +
                        math.sin(2*math.pi*freq*2*(start+i)/SAMPLE_RATE)*0.12
                    ) * g
        crowd_u = _lowpass(_noise(0.3, n), 0.01)
        att = int(0.15*SAMPLE_RATE)
        crowd_e = _envelope(crowd_u, att, int(0.2*SAMPLE_RATE), 0.7, int(0.5*SAMPLE_RATE))
        final = [jingle[i] + crowd_e[i] for i in range(n)]
        _write_wav(p, final)
        log.info("Generated super_over.wav")

    log.info(f"Audio files ready in {audio_dir}")


def _load_pcm(wav_path: Path) -> bytes:
    """Load WAV file and return raw stereo 16-bit PCM bytes."""
    with wave.open(str(wav_path), 'rb') as w:
        frames = w.readframes(w.getnframes())
        ch     = w.getnchannels()
        sw     = w.getsampwidth()
        fr     = w.getframerate()

    # Resample/convert if needed
    if fr != SAMPLE_RATE or ch != CHANNELS or sw != SAMPLE_WIDTH:
        # Simple nearest-neighbour resample
        n_frames = len(frames) // (sw * ch)
        samples = []
        for i in range(n_frames):
            idx = i * sw * ch
            if sw == 2:
                s = struct.unpack_from('<h', frames, idx)[0] / 32767.0
            else:
                s = (struct.unpack_from('<H', frames, idx)[0] - 128) / 128.0
            samples.append(s)
        # Convert to stereo 44100
        ratio = SAMPLE_RATE / fr
        new_n = int(n_frames * ratio)
        resampled = []
        for i in range(new_n):
            src = min(n_frames - 1, int(i / ratio))
            resampled.append(samples[src])
        out = bytearray()
        for s in resampled:
            v = max(-32767, min(32767, int(s * 32767)))
            out += struct.pack('<hh', v, v)
        return bytes(out)
    return frames


# ── Audio Engine ──────────────────────────────────────────────────────────

class AudioEngine:
    """
    Runs in a background thread.
    Continuously writes cricket atmosphere audio to a named pipe.
    FFmpeg reads from the pipe as its audio input.
    """

    WICKET_EVENTS   = {"WICKET", "OUT", "CAUGHT", "LBW", "RUN OUT", "STUMPED", "BOWLED"}
    AMBIENT_VOLUME  = 0.55   # base crowd volume
    EVENT_VOLUME    = 0.95   # event sound volume

    def __init__(self, data_file: Path, pipe_path: str, audio_dir: Path):
        self.data_file  = data_file
        self.pipe_path  = pipe_path
        self.audio_dir  = audio_dir
        self._running   = False
        self._thread    = None
        self._pcm_cache = {}
        self._last_comm = []
        self._last_inn  = 0
        self._event_q   = []   # list of (pcm_bytes, position)
        self._lock      = threading.Lock()

    def _load_sounds(self):
        sound_files = {
            "ambient":   "ambient_crowd.wav",
            "boundary":  "boundary_cheer.wav",
            "six":       "six_cheer.wav",
            "wicket":    "wicket_roar.wav",
            "milestone": "milestone_cheer.wav",
            "super_over":"super_over.wav",
        }
        for key, fname in sound_files.items():
            path = self.audio_dir / fname
            if path.exists():
                self._pcm_cache[key] = _load_pcm(path)
                log.info(f"Loaded {fname}: {len(self._pcm_cache[key])//1024}KB PCM")
            else:
                log.warning(f"Audio file missing: {path}")

    def _read_data(self) -> dict:
        try:
            return json.loads(self.data_file.read_text())
        except Exception:
            return {}

    def _detect_events(self, d: dict):
        """Check for new events in commentary and queue appropriate sounds."""
        comm = d.get("live_commentary") or d.get("commentary") or []
        inn  = d.get("innings_num", 1)

        # Super Over detection
        if inn >= 3 and self._last_inn < 3:
            self._queue_event("super_over")
            log.info("Audio: Super Over!")
        self._last_inn = inn

        if not comm or comm == self._last_comm:
            return
        # Find new entries (compare first entry)
        if self._last_comm and comm and comm[0] == self._last_comm[0]:
            return

        self._last_comm = list(comm)

        # Check most recent commentary entry for events
        if comm:
            ev = (comm[0].get("event") or "").upper()
            txt = (comm[0].get("text") or "").lower()

            if any(w in ev for w in self.WICKET_EVENTS) or \
               any(w in txt for w in ["wicket", "out!", "caught", "lbw", "run out", "stumped", "bowled"]):
                self._queue_event("wicket")
                log.info("Audio: Wicket!")
            elif ev == "SIX" or "six" in txt:
                self._queue_event("six")
                log.info("Audio: Six!")
            elif ev == "FOUR" or "four" in txt or "boundary" in txt:
                self._queue_event("boundary")
                log.info("Audio: Four!")

        # Milestone detection from all recent commentary
        for c in comm[:3]:
            txt2 = (c.get("text") or "").lower()
            if "fifty" in txt2 or "half-century" in txt2 or "century" in txt2 or "hundred" in txt2:
                self._queue_event("milestone")
                log.info("Audio: Milestone!")
                break

    def _queue_event(self, sound_key: str):
        if sound_key in self._pcm_cache:
            with self._lock:
                # Don't queue same event twice rapidly
                if not self._event_q or self._event_q[-1][0] != sound_key:
                    self._event_q.append((sound_key, 0))

    def _mix_chunk(self, ambient_pcm: bytes, ambient_pos: int,
                   chunk_samples: int) -> bytes:
        """Mix ambient loop with any active event sounds."""
        n_bytes    = chunk_samples * CHANNELS * SAMPLE_WIDTH
        amb_len    = len(ambient_pcm)

        # Build ambient chunk (looped)
        amb_chunk = bytearray()
        pos = ambient_pos
        while len(amb_chunk) < n_bytes:
            remaining = n_bytes - len(amb_chunk)
            from_amb  = min(remaining, amb_len - (pos % amb_len))
            start     = pos % amb_len
            amb_chunk += ambient_pcm[start:start + from_amb]
            pos       += from_amb

        # Apply ambient volume
        result = bytearray(n_bytes)
        for i in range(0, n_bytes, 2):
            v = struct.unpack_from('<h', amb_chunk, i)[0]
            v = int(v * self.AMBIENT_VOLUME)
            struct.pack_into('<h', result, i, max(-32767, min(32767, v)))

        # Overlay active events
        with self._lock:
            still_active = []
            for sound_key, ev_pos in self._event_q:
                ev_pcm = self._pcm_cache.get(sound_key, b'')
                if ev_pos >= len(ev_pcm):
                    continue
                # Mix event into result
                samples_to_mix = min(n_bytes, len(ev_pcm) - ev_pos)
                for i in range(0, samples_to_mix, 2):
                    r_idx = i
                    e_val = struct.unpack_from('<h', ev_pcm, ev_pos + i)[0]
                    r_val = struct.unpack_from('<h', result, r_idx)[0]
                    mixed = int(r_val + e_val * self.EVENT_VOLUME)
                    struct.pack_into('<h', result, r_idx, max(-32767, min(32767, mixed)))
                new_pos = ev_pos + samples_to_mix
                if new_pos < len(ev_pcm):
                    still_active.append((sound_key, new_pos))
            self._event_q = still_active

        return bytes(result)

    def _run(self):
        """Main audio loop — writes PCM to named pipe."""
        log.info(f"AudioEngine starting → {self.pipe_path}")

        # Create pipe if not exists
        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)

        ambient_pcm = self._pcm_cache.get("ambient", b'\x00' * (SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH))
        chunk_samples  = CHUNK_SIZE
        bytes_per_chunk = chunk_samples * CHANNELS * SAMPLE_WIDTH
        ambient_pos    = 0
        last_check     = 0

        try:
            with open(self.pipe_path, 'wb') as pipe:
                log.info(f"AudioEngine pipe open — streaming audio")
                while self._running:
                    # Check for events every 0.5s
                    now = time.time()
                    if now - last_check >= 0.5:
                        d = self._read_data()
                        self._detect_events(d)
                        last_check = now

                    # Mix and write chunk
                    chunk = self._mix_chunk(ambient_pcm, ambient_pos, chunk_samples)
                    try:
                        pipe.write(chunk)
                        pipe.flush()
                    except BrokenPipeError:
                        log.warning("AudioEngine: pipe broken (FFmpeg restarting?)")
                        time.sleep(0.5)
                        break

                    ambient_pos = (ambient_pos + bytes_per_chunk) % max(1, len(ambient_pcm))

        except Exception as e:
            log.error(f"AudioEngine error: {e}")

        log.info("AudioEngine stopped")

    def start(self):
        generate_audio_files(self.audio_dir)
        self._load_sounds()
        self._running = True
        self._thread  = threading.Thread(target=self._run, daemon=True,
                                         name="AudioEngine")
        self._thread.start()
        # Give pipe time to be created before FFmpeg tries to open it
        time.sleep(0.3)
        log.info("AudioEngine started")

    def stop(self):
        self._running = False
        # Clean up pipe
        try:
            if os.path.exists(self.pipe_path):
                os.unlink(self.pipe_path)
        except Exception:
            pass


if __name__ == "__main__":
    # Generate audio files only
    import sys
    logging.basicConfig(level=logging.INFO)
    audio_dir = Path(__file__).parent.parent / "audio"
    generate_audio_files(audio_dir)
    print("All audio files generated.")
