# simulated human-like scraper (parallel-safe)
import requests
import random
import time
import os

BASE = "http://10.0.0.1:5001" #server running locally

FAKE_IP = os.getenv("FAKE_IP", "10.0.0.1")

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

# Simulated browsing paths
SESSIONS = [
    ["/", "/api/artworks", "/artwork/1"],
    ["/", "/artwork/5", "/api/artwork/5"],
    ["/", "/artwork/3", "/api/artwork/2"]
]

time.sleep(random.uniform(0.5, 5.0)) # Staggered startup so bots don't all hit at once
SPEED = random.uniform(0.7, 1.4) # Per-instance speed variation

print(f"[BOT {FAKE_IP}] Starting simulated user")

for session_id, session in enumerate(SESSIONS):
    print(f"[BOT {FAKE_IP}] Starting session {session_id}")

    for page in session:
        try:
            r = requests.get(BASE + page, headers=HEADERS, timeout=3)
            print(f"[BOT {FAKE_IP}] {page} => {r.status_code}")
        except Exception as e:
            print(f"[BOT {FAKE_IP}] ERROR on {page}: {e}")

        time.sleep(random.uniform(1.2, 3.1) * SPEED)

    # Simulate user switching tabs or going idle
    idle = random.uniform(5, 15)
    print(f"[BOT {FAKE_IP}] Idle for {idle:.1f}s")
    time.sleep(idle)
