# randomizer.py
import requests
import random
import time

BASE = "http://127.0.0.1:5000"

PAGES = [
    "/", "/api/artworks",
    "/artwork/1", "/artwork/2", "/artwork/3",
    "/api/artwork/1", "/api/artwork/2", "/api/artwork/3",
]

# per-instance randomness
time.sleep(random.uniform(0.3, 4.0))   #staggered start
SPEED = random.uniform(0.4, 1.6)        
MY_PAGES = random.sample(PAGES, random.randint(3, len(PAGES)))

for i in range(120):
    page = random.choice(MY_PAGES)
    delay = random.expovariate(1.0) * SPEED  # bursty randomness

    r = requests.get(BASE + page)
    print(f"[RANDOM] {i}: GET {page} => {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)
