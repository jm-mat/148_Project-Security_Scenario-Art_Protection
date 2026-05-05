# experienced human downloader (safe, human-like)
import requests
import random
import time
import os

BASE = "http://10.0.0.1:5001"   # Flask server running on host 'srv' in Mininet

FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

# Realistic browser headers
HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ]),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": BASE + "/",
    "X-Forwarded-For": FAKE_IP
}

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))   # staggered start
SPEED = random.uniform(0.7, 1.4)       # slightly faster than casual humans
DELAY_CHANCE = random.uniform(0.05, 0.25)

for art_id in range(1, 10):
    r = requests.get(f"{BASE}/api/artwork/{art_id}", headers=HEADERS)
    print(f"[EXPERIENCED] Downloaded {art_id}: {r.status_code}")

    delay = random.uniform(0.8, 2.5) * SPEED
    time.sleep(delay)

    # occasional longer breaks
    if random.random() < DELAY_CHANCE:
        long_delay = random.uniform(5, 9)
        print(f"[EXPERIENCED] Taking a longer break: {long_delay:.1f}s")
        time.sleep(long_delay)
