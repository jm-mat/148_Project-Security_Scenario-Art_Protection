# enumerator bot (Layer 4 tester)
import requests
import random
import time
import os

BASE = "http://127.0.0.1:5001"
FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

# per-instance randomness
time.sleep(random.uniform(0.2, 2.0))  # staggered start
SPEED = random.uniform(0.2, 0.6)      # faster than humans

start = random.randint(1, 5)
end = start + random.randint(10, 40)

# loop through the range repeatedly to accumulate anomaly score
while True:
    for art_id in range(start, end):
        page = f"/api/artwork/{art_id}"
        delay = random.uniform(0.3, 0.7) * SPEED

        r = requests.get(BASE + page, headers={"X-Forwarded-For": FAKE_IP})
        print(f"[ENUM] GET {page} => {r.status_code} (delay {delay:.2f}s)")

        time.sleep(delay)
