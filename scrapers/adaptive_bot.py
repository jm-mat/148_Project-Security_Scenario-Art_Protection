# adaptive bot scraper

import requests
import random
import time

BASE = "http://127.0.0.1:5000"

PAGES = ["/", "/api/artworks", "/api/artwork/1","/api/artwork/2"]

# per-instance randomness
time.sleep(random.uniform(0.5, 3.5))  # staggered start to simulate humans starting at different times
SPEED = random.uniform(0.5, 1.2)
MY_PAGES = random.sample(PAGES, random.randint(2, len(PAGES)))

rate_adjust = 1.0 

for i in range(150):
    page = random.choice(MY_PAGES)
    delay = random.uniform(0.2, 1.0) * SPEED * rate_adjust

    r = requests.get(BASE + page)
    print(f"[ADAPT] {i}: GET {page} => status {r.status_code} (delay {delay:.2f}s)")

    # adaptative behavior
    # slow down if "Too Many Request" response is received
    # gradually return to original speed if not
    if r.status_code == 429:
        rate_adjust = min(rate_adjust * 1.5, 5.0)
    else:
        rate_adjust = max(rate_adjust * 0.9, 1.0)
    time.sleep(delay)