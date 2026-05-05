# casual human downloader

import requests
import random
import time

BASE = "http://127.0.0.1:5000"

PAGES = ["/", "/api/artworks", "/artwork/1", "/artwork/2", "/artwork/3", "/api/artwork/1", "/api/artwork/5"]

for i in range(20):
    page = random.choice(PAGES)
    delay = random.uniform(1.3, 3.2)    # slow and typical human intervals

    r = requests.get(BASE + page)
    print(f"{i}: GET {page} => status {r.status_code} (delay {delay:.2f}s)")

    time.sleep(delay)