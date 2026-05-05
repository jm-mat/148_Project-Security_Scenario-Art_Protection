# experienced human downloader

import requests
import random
import time

BASE = "http://127.0.0.1:5000"

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))  # staggered start to simulate humans starting at different times
SPEED = random.uniform(0.7, 1.4)
DELAY_CHANCE = random.uniform(0.05, 0.25) 

for art_id in range(1,10):
    r = requests.get(f"{BASE}/api/artwork/{art_id}")
    print(f"Successfully downloaded {art_id}: {r.status_code}")
    
    delay = random.uniform(0.8, 2.5) * SPEED    # typical human intervals but faster than casual
    time.sleep(delay)
   
    # simulate occasional longer breaks
    if random.random() < DELAY_CHANCE:
        long_delay = random.uniform(5,9)
        print(f"Taking a longer break: {long_delay:.1f}s")
        time.sleep(long_delay)
