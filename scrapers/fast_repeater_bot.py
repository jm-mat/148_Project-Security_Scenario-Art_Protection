# fast repeater bot (Layer 1 tester)

import requests
import random
import time
import os

BASE = "http://10.0.0.1:5001"   # Flask server running on host 'srv' in Mininet
FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

PAGES = ["/", "/api/artworks", "/api/artwork/1", "/api/artwork/2"]

# per-instance randomness
time.sleep(random.uniform(0.2, 2.0))  # staggered start
SPEED = random.uniform(0.2, 0.6)      # faster than humans
MY_PAGES = random.sample(PAGES, random.randint(2, len(PAGES)))

# start with a normal delay, then accelerate
delay = random.uniform(0.15, 0.35) * SPEED

for i in range(200):
    page = random.choice(MY_PAGES)

    r = requests.get(BASE + page, headers={"X-Forwarded-For": FAKE_IP})
    print(f"[FAST] {i}: GET {page} => {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)

    # accelerate slightly each iteration
    delay = max(0.02, delay * 0.92)
