# Self-Hosted Runner Setup — Xstar Sports

For Test matches (5 days) or back-to-back ODIs, GitHub's 6-hour job limit
will cut your stream. A self-hosted runner on a cheap VPS runs indefinitely.

---

## Option A: Hetzner VPS (Recommended — €4/month)

Best price/performance for streaming.

### 1. Get a VPS

Sign up at hetzner.com → Cloud → Create Server
- Location: pick closest to your YouTube audience
- Image: Ubuntu 22.04
- Type: CX21 (2 vCPU, 4GB RAM) — minimum for dual stream
         CX31 (2 vCPU, 8GB RAM) — recommended
- Cost: ~€4–6/month

### 2. SSH into your VPS

```bash
ssh root@YOUR_VPS_IP
```

### 3. Install dependencies

```bash
# System packages
apt-get update && apt-get install -y \
  ffmpeg chromium-browser xvfb \
  fonts-noto-color-emoji fonts-liberation \
  python3 python3-pip curl git

pip3 install requests

# GitHub Actions runner
mkdir -p /opt/actions-runner && cd /opt/actions-runner
curl -o actions-runner.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.315.0/actions-runner-linux-x64-2.315.0.tar.gz
tar xzf actions-runner.tar.gz
```

### 4. Register runner with your repo

Go to: GitHub repo → Settings → Actions → Runners → New self-hosted runner

Copy the token shown, then run:

```bash
cd /opt/actions-runner
./config.sh \
  --url https://github.com/YOUR_USERNAME/YOUR_REPO \
  --token YOUR_RUNNER_TOKEN \
  --name "xstar-vps" \
  --labels "self-hosted,xstar" \
  --unattended
```

### 5. Install as a system service (auto-starts on reboot)

```bash
cd /opt/actions-runner
./svc.sh install
./svc.sh start
./svc.sh status   # should show: active (running)
```

### 6. Update workflow to use self-hosted runner

In `.github/workflows/stream.yml`, change the stream job:

```yaml
stream:
  runs-on: self-hosted    # ← change from ubuntu-latest
  timeout-minutes: 10080  # 7 days (Test match coverage)
```

---

## Option B: Oracle Cloud Free Tier (£0/month)

Oracle gives a permanently free VM:
- 4 ARM CPUs, 24GB RAM (Ampere A1)
- Enough for dual stream + headroom

Steps are identical to Hetzner above.
Go to: cloud.oracle.com → Compute → Instances → Create

Note: ARM runner needs `runs-on: [self-hosted, linux, ARM64]`

---

## Option C: Raspberry Pi 5 (one-time cost)

If you have a Pi 5 at home on a good internet connection:
- 4 cores, 8GB RAM
- Runs 24/7 on ~5W electricity
- Same setup steps as above

---

## Checking your runner is online

Go to: GitHub repo → Settings → Actions → Runners

Your runner should show as **Idle** (green dot) when waiting for jobs.
It shows **Active** while streaming.

---

## Monthly cost comparison

| Option                | Cost        | Runtime limit |
|-----------------------|-------------|---------------|
| GitHub Actions free   | Free        | 6h per job    |
| GitHub Actions paid   | $0.008/min  | 35 days       |
| Hetzner CX21 VPS      | €4/month    | Unlimited     |
| Hetzner CX31 VPS      | €6/month    | Unlimited     |
| Oracle Free Tier      | $0/month    | Unlimited     |
| Raspberry Pi 5        | ~£80 one-off| Unlimited     |

**Recommendation:** Hetzner CX31 at €6/month.
Covers any cricket format indefinitely, handles dual stream comfortably.
