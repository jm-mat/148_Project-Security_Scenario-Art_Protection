# fast repeater bot

import requests
import random
import time

BASE = "http://127.0.0.1:5000"

PAGES = ["/" , "/api/artworks", "/api/artwork/1", "/api/artwork/2"]

# per-instance randomness
time.sleep(random.uniform(0.2, 2.0))  # staggered start
SPEED = random.uniform(0.2, 0.6)    # faster than humans
MY_PAGES = random.sample(PAGES, random.randint(2, len(PAGES)))

for i in range(200):
    page = random.choice(MY_PAGES)
    delay = random.uniform(0.05, 0.25) * SPEED  # shorter delay intervals

    r = requests.get(BASE + page)
    print(f"[FAST] {i}: GET {page} => status {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)