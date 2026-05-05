# randomizer bot (Layer 6 tester)
import requests
import random
import time
import os

BASE = "http://127.0.0.1:5001"
FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

PAGES = [
    "/", "/api/artworks",
    "/artwork/1", "/artwork/2", "/artwork/3",
    "/api/artwork/1", "/api/artwork/2", "/api/artwork/3",
]

# per-instance randomness
time.sleep(random.uniform(0.3, 4.0))   # staggered start
SPEED = random.uniform(0.4, 1.6)
MY_PAGES = random.sample(PAGES, random.randint(3, len(PAGES)))

#no User-Agent = suspicious header pattern
HEADERS = {"X-Forwarded-For": FAKE_IP}

for i in range(120):
    # NEW: weighted randomness (bots often favor API endpoints)
    page = random.choices(
        MY_PAGES,
        weights=[1 if "api" not in p else 3 for p in MY_PAGES]
    )[0]

    # keep bursty randomness
    delay = random.expovariate(1.0) * SPEED

    r = requests.get(BASE + page, headers=HEADERS)
    print(f"[RANDOM] {i}: GET {page} => {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)
