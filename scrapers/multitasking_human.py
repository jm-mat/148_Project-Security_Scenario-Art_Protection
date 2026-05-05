# multitasking human downloader
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

SESSIONS = [
    ["/", "/api/artworks", "/artwork/1"],
    ["/", "/artwork/5", "/api/artwork/5"],
    ["/", "/artwork/3", "/api/artwork/2"]
]

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))  # staggered start
SPEED = random.uniform(0.7, 1.4)

for session_id, session in enumerate(SESSIONS):
    print(f"[MULTI] Starting session {session_id}")

    for page in session:
        r = requests.get(BASE + page, headers=HEADERS)
        print(f"[MULTI] {page} => {r.status_code}")

        time.sleep(random.uniform(1.2, 3.1) * SPEED)

    # simulate user switching apps/tabs
    idle = random.uniform(5, 15)
    print(f"[MULTI] Switching: Idle for {idle:.1f}s")
    time.sleep(idle)
