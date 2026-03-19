"""
audio_engine.py — Xstar Sports Cricket Audio Engine
=====================================================
Generates 100% copyright-free cricket atmosphere audio by synthesizing
realistic stadium ambience using layered harmonic techniques.

FIX: Replaced white/gaussian noise (sounds like radio static) with:
  - Layered crowd murmur using bandpass-filtered brown noise
  - Natural swell patterns with low-frequency oscillation
  - Harmonic overtones for warmth and realism
  - Smooth crossfades on event sounds
  - No clipping or distortion
"""

import os, wave, struct, math, time, threading, json, logging, random
from pathlib import Path

log = logging.getLogger("AudioEngine")

SAMPLE_RATE  = 44100
CHANNELS     = 2
SAMPLE_WIDTH = 2   # 16-bit
CHUNK_SIZE   = 4096


# ── DSP helpers ───────────────────────────────────────────────────────────────

def _sine(freq, amp, n, phase=0.0):
    return [amp * math.sin(2 * math.pi * freq * i / SAMPLE_RATE + phase) for i in range(n)]

def _brown_noise(amp, n, seed=42):
    """Brown noise (1/f²) — much warmer and more natural than white/gaussian noise."""
    rng = random.Random(seed)
    out = [0.0] * n
    v = 0.0
    for i in range(n):
        v += rng.gauss(0, 0.02)
        v = max(-1.0, min(1.0, v))
        out[i] = v * amp
    return out

def _bandpass(sig, low_alpha, high_alpha):
    """Bandpass filter: highpass then lowpass."""
    # Highpass
    hp = [0.0] * len(sig)
    prev_in = 0.0
    prev_out = 0.0
    a = 1.0 - high_alpha
    for i in range(len(sig)):
        hp[i] = a * (prev_out + sig[i] - prev_in)
        prev_in = sig[i]
        prev_out = hp[i]
    # Lowpass
    lp = [0.0] * len(sig)
    for i in range(1, len(sig)):
        lp[i] = lp[i-1] + low_alpha * (hp[i] - lp[i-1])
    return lp

def _lowpass(sig, alpha):
    out = [0.0] * len(sig)
    for i in range(1, len(sig)):
        out[i] = out[i-1] + alpha * (sig[i] - out[i-1])
    return out

def _envelope(sig, attack_s, decay_s, sustain_level, release_s):
    n = len(sig)
    attack  = int(attack_s * SAMPLE_RATE)
    decay   = int(decay_s * SAMPLE_RATE)
    release = int(release_s * SAMPLE_RATE)
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

def _mix(*signals):
    n = min(len(s) for s in signals)
    return [sum(s[i] for s in signals) for i in range(n)]

def _clamp_norm(sig, target_peak=0.82):
    """Normalize and clamp — prevents clipping."""
    peak = max(abs(x) for x in sig) or 1.0
    scale = target_peak / peak
    return [max(-1.0, min(1.0, x * scale)) for x in sig]

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


# ── Audio file generator ──────────────────────────────────────────────────────

def generate_audio_files(audio_dir: Path):
    """
    Generate all cricket atmosphere audio files.
    FIX: Uses brown noise + bandpass filtering for natural crowd sound,
    NOT gaussian/white noise which sounds like radio static.
    """
    audio_dir.mkdir(parents=True, exist_ok=True)

    # ── Ambient crowd (5s seamless loop) ─────────────────────────────────
    # Sounds like a cricket stadium between balls: distant murmur, gentle buzz
    p = audio_dir / "ambient_crowd.wav"
    if not p.exists():
        dur = 5.0
        n = int(dur * SAMPLE_RATE)

        # Layer 1: Low-frequency stadium rumble (brown noise, bandpass 80-300Hz)
        rumble_l = _bandpass(_brown_noise(0.5, n, seed=1), 0.008, 0.04)
        rumble_r = _bandpass(_brown_noise(0.5, n, seed=2), 0.008, 0.04)

        # Layer 2: Mid crowd chatter (brown noise, bandpass 300-2000Hz)
        chat_l = _bandpass(_brown_noise(0.35, n, seed=3), 0.04, 0.25)
        chat_r = _bandpass(_brown_noise(0.35, n, seed=4), 0.04, 0.25)

        # Layer 3: High ambience — distant applause texture (highpass >2kHz, very quiet)
        hf_l = _bandpass(_brown_noise(0.12, n, seed=5), 0.25, 0.7)
        hf_r = _bandpass(_brown_noise(0.12, n, seed=6), 0.25, 0.7)

        # Layer 4: Natural swell — slow oscillation (0.08Hz) for breathing feel
        swell = [0.70 + 0.30 * math.sin(2*math.pi*0.08*i/SAMPLE_RATE) for i in range(n)]

        # Mix layers with swell modulation
        l = [swell[i] * (rumble_l[i]*0.6 + chat_l[i]*0.9 + hf_l[i]*0.5) for i in range(n)]
        r = [swell[i] * (rumble_r[i]*0.6 + chat_r[i]*0.9 + hf_r[i]*0.5) for i in range(n)]

        # Seamless loop: crossfade last 0.3s into first 0.3s
        fade_n = int(0.3 * SAMPLE_RATE)
        for i in range(fade_n):
            t = i / fade_n
            fade_in  = math.sin(math.pi * t / 2)
            fade_out = math.cos(math.pi * t / 2)
            l[i] = l[i] * fade_in + l[n - fade_n + i] * fade_out
            r[i] = r[i] * fade_in + r[n - fade_n + i] * fade_out

        l = _clamp_norm(l, 0.70)
        r = _clamp_norm(r, 0.70)
        _write_wav(p, l, r)
        log.info("Generated ambient_crowd.wav (stadium murmur)")

    # ── Boundary cheer (2.5s) — excited crowd on a four ─────────────────
    p = audio_dir / "boundary_cheer.wav"
    if not p.exists():
        dur = 2.5
        n = int(dur * SAMPLE_RATE)

        # Rising cheer: brown noise boosted through midrange, sharp attack
        base_l = _bandpass(_brown_noise(1.0, n, seed=10), 0.02, 0.35)
        base_r = _bandpass(_brown_noise(1.0, n, seed=11), 0.02, 0.35)

        # Add harmonic shimmer at 1.2kHz (group-cheer overtone)
        shimmer = _sine(1200, 0.08, n)
        shimmer_shaped = _envelope(shimmer, 0.05, 0.2, 0.6, 0.8)

        l = [base_l[i] + shimmer_shaped[i] for i in range(n)]
        r = [base_r[i] + shimmer_shaped[i] * 0.9 for i in range(n)]

        # Cheer envelope: sharp attack (0.05s), sustain, long decay
        l = _envelope(l, 0.05, 0.15, 0.88, 1.2)
        r = _envelope(r, 0.05, 0.15, 0.88, 1.2)

        l = _clamp_norm(l, 0.80)
        r = _clamp_norm(r, 0.80)
        _write_wav(p, l, r)
        log.info("Generated boundary_cheer.wav")

    # ── Six cheer (3s) — bigger, more euphoric than boundary ─────────────
    p = audio_dir / "six_cheer.wav"
    if not p.exists():
        dur = 3.0
        n = int(dur * SAMPLE_RATE)

        base_l = _bandpass(_brown_noise(1.0, n, seed=20), 0.015, 0.4)
        base_r = _bandpass(_brown_noise(1.0, n, seed=21), 0.015, 0.4)

        # Bigger shimmer + bass thump
        shimmer = _sine(900, 0.12, n)
        shimmer = _envelope(shimmer, 0.04, 0.2, 0.7, 1.0)
        bass    = _sine(80, 0.15, n)
        bass    = _envelope(bass, 0.02, 0.1, 0.5, 1.5)

        l = [base_l[i] + shimmer[i] + bass[i] for i in range(n)]
        r = [base_r[i] + shimmer[i]*0.9 + bass[i]*0.95 for i in range(n)]

        l = _envelope(l, 0.04, 0.12, 0.92, 1.4)
        r = _envelope(r, 0.04, 0.12, 0.92, 1.4)

        l = _clamp_norm(l, 0.84)
        r = _clamp_norm(r, 0.84)
        _write_wav(p, l, r)
        log.info("Generated six_cheer.wav")

    # ── Wicket roar (3.5s) — dramatic collective gasp then roar ──────────
    p = audio_dir / "wicket_roar.wav"
    if not p.exists():
        dur = 3.5
        n = int(dur * SAMPLE_RATE)

        base_l = _bandpass(_brown_noise(1.0, n, seed=30), 0.01, 0.45)
        base_r = _bandpass(_brown_noise(1.0, n, seed=31), 0.01, 0.45)

        # Deep bass thump (impact feel — bat hitting stumps)
        boom_dur = int(0.4 * SAMPLE_RATE)
        boom = [math.exp(-6*i/boom_dur) * math.sin(2*math.pi*55*i/SAMPLE_RATE) * 0.45
                for i in range(boom_dur)] + [0.0] * (n - boom_dur)

        # Crowd roar — mid frequencies surge
        mid_roar = _bandpass(_brown_noise(0.8, n, seed=32), 0.03, 0.3)
        mid_roar = _envelope(mid_roar, 0.06, 0.15, 0.95, 1.5)

        l = [base_l[i] + boom[i] + mid_roar[i] for i in range(n)]
        r = [base_r[i] + boom[i]*0.9 + mid_roar[i] for i in range(n)]

        l = _envelope(l, 0.04, 0.10, 0.96, 1.6)
        r = _envelope(r, 0.04, 0.10, 0.96, 1.6)

        l = _clamp_norm(l, 0.88)
        r = _clamp_norm(r, 0.88)
        _write_wav(p, l, r)
        log.info("Generated wicket_roar.wav")

    # ── Milestone cheer (2.5s) — warm sustained applause ─────────────────
    p = audio_dir / "milestone_cheer.wav"
    if not p.exists():
        dur = 2.5
        n = int(dur * SAMPLE_RATE)

        base_l = _bandpass(_brown_noise(0.85, n, seed=40), 0.02, 0.30)
        base_r = _bandpass(_brown_noise(0.85, n, seed=41), 0.02, 0.30)

        # Warm overtone at 700Hz — applause shimmer
        warm = _sine(700, 0.09, n)
        warm = _envelope(warm, 0.08, 0.2, 0.65, 0.9)

        l = [base_l[i] + warm[i] for i in range(n)]
        r = [base_r[i] + warm[i]*0.95 for i in range(n)]

        l = _envelope(l, 0.08, 0.15, 0.82, 1.0)
        r = _envelope(r, 0.08, 0.15, 0.82, 1.0)

        l = _clamp_norm(l, 0.78)
        r = _clamp_norm(r, 0.78)
        _write_wav(p, l, r)
        log.info("Generated milestone_cheer.wav")

    # ── Super Over jingle (2s) — ascending notes + crowd swell ───────────
    p = audio_dir / "super_over.wav"
    if not p.exists():
        dur = 2.0
        n = int(dur * SAMPLE_RATE)

        # Ascending 4-note fanfare (C5-E5-G5-C6) with harmonics
        notes_hz = [523.25, 659.25, 783.99, 1046.50]
        note_dur = n // (len(notes_hz) + 1)
        jingle = [0.0] * n
        for idx, freq in enumerate(notes_hz):
            start = idx * note_dur
            for i in range(min(note_dur, n - start)):
                t = i / note_dur
                env = math.exp(-3.0 * t)
                # Fundamental + second + third harmonic
                jingle[start+i] += env * (
                    math.sin(2*math.pi*freq*(start+i)/SAMPLE_RATE) * 0.35 +
                    math.sin(2*math.pi*freq*2*(start+i)/SAMPLE_RATE) * 0.10 +
                    math.sin(2*math.pi*freq*3*(start+i)/SAMPLE_RATE) * 0.04
                )

        # Crowd swell underneath
        crowd_l = _bandpass(_brown_noise(0.5, n, seed=50), 0.02, 0.3)
        crowd_r = _bandpass(_brown_noise(0.5, n, seed=51), 0.02, 0.3)
        crowd_e = _envelope(crowd_l, 0.15, 0.2, 0.7, 0.6)

        l = [jingle[i] + crowd_e[i] * 0.6 for i in range(n)]
        r = [jingle[i] + _envelope(crowd_r, 0.15, 0.2, 0.7, 0.6)[i] * 0.6 for i in range(n)]

        l = _clamp_norm(l, 0.82)
        r = _clamp_norm(r, 0.82)
        _write_wav(p, l, r)
        log.info("Generated super_over.wav")

    log.info(f"All audio files ready in {audio_dir}")


def _load_pcm(wav_path: Path) -> bytes:
    """Load WAV file and return raw stereo 16-bit PCM bytes."""
    with wave.open(str(wav_path), 'rb') as w:
        frames = w.readframes(w.getnframes())
        ch  = w.getnchannels()
        sw  = w.getsampwidth()
        fr  = w.getframerate()

    if fr != SAMPLE_RATE or ch != CHANNELS or sw != SAMPLE_WIDTH:
        n_frames = len(frames) // (sw * ch)
        samples = []
        for i in range(n_frames):
            idx = i * sw * ch
            if sw == 2:
                s = struct.unpack_from('<h', frames, idx)[0] / 32767.0
            else:
                s = (struct.unpack_from('<H', frames, idx)[0] - 128) / 128.0
            samples.append(s)
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


# ── Audio Engine ──────────────────────────────────────────────────────────────

class AudioEngine:
    """
    Runs in a background thread.
    Continuously writes cricket atmosphere audio to a named pipe.
    FFmpeg reads from the pipe as its audio input.
    """

    WICKET_EVENTS  = {"WICKET", "OUT", "CAUGHT", "LBW", "RUN OUT", "STUMPED", "BOWLED"}
    AMBIENT_VOLUME = 0.55
    EVENT_VOLUME   = 0.92

    def __init__(self, data_file: Path, pipe_path: str, audio_dir: Path):
        self.data_file  = data_file
        self.pipe_path  = pipe_path
        self.audio_dir  = audio_dir
        self._running   = False
        self._thread    = None
        self._pcm_cache = {}
        self._last_comm = []
        self._last_inn  = 0
        self._event_q   = []
        self._lock      = threading.Lock()

    def _load_sounds(self):
        sound_files = {
            "ambient":    "ambient_crowd.wav",
            "boundary":   "boundary_cheer.wav",
            "six":        "six_cheer.wav",
            "wicket":     "wicket_roar.wav",
            "milestone":  "milestone_cheer.wav",
            "super_over": "super_over.wav",
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
        comm = d.get("live_commentary") or d.get("commentary") or []
        inn  = d.get("innings_num", 1)

        if inn >= 3 and self._last_inn < 3:
            self._queue_event("super_over")
            log.info("Audio: Super Over!")
        self._last_inn = inn

        if not comm or comm == self._last_comm:
            return
        if self._last_comm and comm and comm[0] == self._last_comm[0]:
            return

        self._last_comm = list(comm)

        if comm:
            ev  = (comm[0].get("event") or "").upper()
            txt = (comm[0].get("text")  or "").lower()

            if any(w in ev for w in self.WICKET_EVENTS) or \
               any(w in txt for w in ["wicket", "out!", "caught", "lbw", "run out", "stumped", "bowled"]):
                self._queue_event("wicket")
            elif ev == "SIX" or " six" in txt or txt.startswith("six"):
                self._queue_event("six")
            elif ev == "FOUR" or "four" in txt or "boundary" in txt:
                self._queue_event("boundary")

        for c in comm[:3]:
            txt2 = (c.get("text") or "").lower()
            if "fifty" in txt2 or "half-century" in txt2 or "century" in txt2 or "hundred" in txt2:
                self._queue_event("milestone")
                break

    def _queue_event(self, sound_key: str):
        if sound_key in self._pcm_cache:
            with self._lock:
                if not self._event_q or self._event_q[-1][0] != sound_key:
                    self._event_q.append((sound_key, 0))

    def _mix_chunk(self, ambient_pcm: bytes, ambient_pos: int, chunk_samples: int) -> bytes:
        n_bytes = chunk_samples * CHANNELS * SAMPLE_WIDTH
        amb_len = len(ambient_pcm)

        amb_chunk = bytearray()
        pos = ambient_pos
        while len(amb_chunk) < n_bytes:
            remaining = n_bytes - len(amb_chunk)
            from_amb  = min(remaining, amb_len - (pos % amb_len))
            start     = pos % amb_len
            amb_chunk += ambient_pcm[start:start + from_amb]
            pos       += from_amb

        result = bytearray(n_bytes)
        for i in range(0, n_bytes, 2):
            v = struct.unpack_from('<h', amb_chunk, i)[0]
            v = int(v * self.AMBIENT_VOLUME)
            struct.pack_into('<h', result, i, max(-32767, min(32767, v)))

        with self._lock:
            still_active = []
            for sound_key, ev_pos in self._event_q:
                ev_pcm = self._pcm_cache.get(sound_key, b'')
                if ev_pos >= len(ev_pcm):
                    continue
                samples_to_mix = min(n_bytes, len(ev_pcm) - ev_pos)
                for i in range(0, samples_to_mix, 2):
                    e_val = struct.unpack_from('<h', ev_pcm, ev_pos + i)[0]
                    r_val = struct.unpack_from('<h', result, i)[0]
                    mixed = int(r_val + e_val * self.EVENT_VOLUME)
                    struct.pack_into('<h', result, i, max(-32767, min(32767, mixed)))
                new_pos = ev_pos + samples_to_mix
                if new_pos < len(ev_pcm):
                    still_active.append((sound_key, new_pos))
            self._event_q = still_active

        return bytes(result)

    def _run(self):
        log.info(f"AudioEngine starting → {self.pipe_path}")

        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)

        ambient_pcm     = self._pcm_cache.get("ambient", b'\x00' * (SAMPLE_RATE * CHANNELS * SAMPLE_WIDTH))
        chunk_samples   = CHUNK_SIZE
        bytes_per_chunk = chunk_samples * CHANNELS * SAMPLE_WIDTH
        ambient_pos     = 0
        last_check      = 0

        try:
            with open(self.pipe_path, 'wb') as pipe:
                log.info("AudioEngine pipe open — streaming stadium audio")
                while self._running:
                    now = time.time()
                    if now - last_check >= 0.5:
                        d = self._read_data()
                        self._detect_events(d)
                        last_check = now

                    chunk = self._mix_chunk(ambient_pcm, ambient_pos, chunk_samples)
                    try:
                        pipe.write(chunk)
                        pipe.flush()
                    except BrokenPipeError:
                        log.warning("AudioEngine: pipe broken — waiting for FFmpeg restart")
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
        self._thread  = threading.Thread(target=self._run, daemon=True, name="AudioEngine")
        self._thread.start()
        time.sleep(0.3)
        log.info("AudioEngine started")

    def stop(self):
        self._running = False
        try:
            if os.path.exists(self.pipe_path):
                os.unlink(self.pipe_path)
        except Exception:
            pass


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    audio_dir = Path(__file__).parent.parent / "audio"
    generate_audio_files(audio_dir)
    print("All audio files generated.")
