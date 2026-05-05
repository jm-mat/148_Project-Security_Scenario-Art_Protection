# enumerator bot
import requests
import random
import time

BASE = "http://127.0.0.1:5000"

# per-instance randomness
time.sleep(random.uniform(0.2, 2.0))  # staggered start
SPEED = random.uniform(0.2, 0.6)    # faster than humans

start = random.randint(1,5)
end = start + random.randint(10, 40)

for art_id in range(start, end):
    page = f"/api/artwork/{art_id}"
    delay = random.uniform(0.3, 0.7) * SPEED
    
    r = requests.get(BASE + page)
    print(f"ENUM GET {page} => {r.status_code} (delay {delay:.2f}s)")
    time.sleep(delay)