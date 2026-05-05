# casual human downloader

import requests
import random
import time

BASE = "http://127.0.0.1:5000"

PAGES = ["/", "/api/artworks", "/artwork/1", "/artwork/2", "/artwork/3", "/api/artwork/1", "/api/artwork/5"]

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))  # staggered start to simulate humans starting at different times
SPEED = random.uniform(0.7, 1.4)
MY_PAGES = random.sample(PAGES, random.randint(3, len(PAGES)))

for i in range(20):
    page = random.choice(MY_PAGES)
    delay = random.uniform(1.3, 3.2) * SPEED    # slow and typical human intervals

    r = requests.get(BASE + page)
    print(f"[CASUAL] {i}: GET {page} => status {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)
