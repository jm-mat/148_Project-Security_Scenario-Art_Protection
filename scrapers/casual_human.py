# casual human downloader (safe, human-like)
import requests
import random
import time
import os

BASE = "http://10.0.0.1:5001"   # Flask server running on host 'srv' in Mininet

FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

# Realistic browser headers (prevents Layer 6 flags)
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

PAGES = [
    "/", "/api/artworks",
    "/artwork/1", "/artwork/2", "/artwork/3",
    "/api/artwork/1", "/api/artwork/5"
]

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))  # staggered start
SPEED = random.uniform(0.7, 1.4)
MY_PAGES = random.sample(PAGES, random.randint(3, len(PAGES)))

for i in range(20):
    page = random.choice(MY_PAGES)
    delay = random.uniform(1.3, 3.2) * SPEED  # slow, human-like

    r = requests.get(BASE + page, headers=HEADERS)
    print(f"[CASUAL] {i}: GET {page} => status {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)
