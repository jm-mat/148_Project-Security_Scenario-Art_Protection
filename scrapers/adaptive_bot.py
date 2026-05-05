# adaptive bot
import requests
import time
import random
import os

BASE = "http://10.0.0.1:5001"   # Flask server running on host 'srv' in Mininet

FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

# per-instance randomness
time.sleep(random.uniform(0.5, 3.0))   # staggered start
SPEED = random.uniform(0.6, 1.4)       # human-like speed variation

HEADERS = {
    "User-Agent": random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)"
    ]),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": BASE + "/",
    "X-Forwarded-For": FAKE_IP
}

HTML_PAGES = ["/", "/artwork/1", "/artwork/2", "/artwork/3"]
# expanded to hit more unique IDs without honeypots
API_PAGES = [f"/api/artwork/{i}" for i in range(1, 11)]

def human_delay():
    time.sleep(random.uniform(0.3, 1.4) * SPEED)

def idle_break():
    if random.random() < 0.1:
        pause = random.uniform(2, 5)
        print(f"[ADAPT] Idle break for {pause:.2f}s")
        time.sleep(pause)

# natural drift toward API usage over time
session_counter = 0

while True:
    session_counter += 1

    # after some time, UA becomes slightly more suspicious (helps Layer 6)
    if session_counter == 90:
        HEADERS["User-Agent"] = "python-requests/2.31"
        print(f"[ADAPT] UA shifted to more suspicious: {HEADERS['User-Agent']}")

    # occasional human-like mistake
    if random.random() < 0.02:
        page = "/artwork/999"   # guaranteed 404
    else:
        # early in the session: mostly HTML
        # later in the session: gradually more API
        api_bias = min(0.2 + session_counter * 0.0015, 0.9)

        if random.random() < api_bias:
            page = random.choice(API_PAGES)
        else:
            page = random.choice(HTML_PAGES)

    # subtle repeated pattern every around 40 requests
    if session_counter % 40 == 0:
        page = "/api/artwork/1"

    print(f"[ADAPT] GET {page} (UA={HEADERS['User-Agent']})")

    try:
        r = requests.get(BASE + page, headers=HEADERS, timeout=3)
        print(f"[ADAPT] Status: {r.status_code}")
    except Exception as e:
        print(f"[ADAPT] Request error: {e}")

    # tiny micro-burst every around 25 requests
    if session_counter % 25 == 0:
        print("[ADAPT] Micro-burst triggered")
        for _ in range(3):
            try:
                burst_page = random.choice(API_PAGES)
                r2 = requests.get(BASE + burst_page, headers=HEADERS, timeout=3)
                print(f"[ADAPT] Burst Status: {r2.status_code}")
            except Exception:
                pass
            time.sleep(random.uniform(0.05, 0.15))

    human_delay()
    idle_break()
