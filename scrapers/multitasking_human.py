# multitasking human downloader
import requests
import random
import time

BASE = "http://127.0.0.1:5000"

SESSIONS = [
    ["/", "/api/artworks","/artwork/1"],
    ["/", "/artwork/5","/api/artwork/5"],
    ["/", "/artwork/3","/api/artwork/2"]
] 

# per-instance randomness
time.sleep(random.uniform(0.5, 5.0))  # staggered start to simulate humans starting at different times
SPEED = random.uniform(0.7, 1.4)

for session_id, session in enumerate(SESSIONS):
    print(f"Starting session {session_id}")

    for page in session:
        r = requests.get(BASE + page)
        print(f" {page} => {r.status_code}")
    
        time.sleep(random.uniform(1.2, 3.1) * SPEED) 

    # simulate user switching to other apps or tabs
    idle = random.uniform(5,15)
    print(f"Switching: Idle for {idle:.1f}s")
    time.sleep(idle)