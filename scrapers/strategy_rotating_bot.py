# strategy rotating bot (multi-phase defense tester)
import requests
import time
import random
import os

BASE = "http://10.0.0.1:5001"   # Flask server running on host 'srv' in Mininet

FAKE_IP = os.getenv("FAKE_IP", "127.0.0.1")

# per-instance randomness
time.sleep(random.uniform(0.5, 3.0))   # staggered start
SPEED = random.uniform(0.7, 1.4)       # speed variation per instance

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Forwarded-For": FAKE_IP
}

def slow_browsing():
    print("[ROTATE] Phase: slow_browsing")
    pages = ["/", "/artwork/1", "/artwork/2", "/artwork/3"]
    for p in pages:
        r = requests.get(BASE + p, headers=HEADERS)
        print(f"[slow] GET {p} => {r.status_code}")
        time.sleep(random.uniform(0.8, 1.5) * SPEED)

def fast_burst():
    print("[ROTATE] Phase: fast_burst")
    for _ in range(20):
        r = requests.get(BASE + "/api/artwork/1", headers=HEADERS)
        print(f"[burst] GET /api/artwork/1 => {r.status_code}")
        time.sleep(0.05 * SPEED)

def enumerator():
    print("[ROTATE] Phase: enumerator")
    for i in range(1, 11):
        p = f"/api/artwork/{i}"
        r = requests.get(BASE + p, headers=HEADERS)
        print(f"[enum] GET {p} => {r.status_code}")
        time.sleep(0.2 * SPEED)

def api_mode():
    print("[ROTATE] Phase: api_mode")
    for _ in range(30):
        r = requests.get(BASE + "/api/artworks", headers=HEADERS)
        print(f"[api] GET /api/artworks => {r.status_code}")
        time.sleep(0.1 * SPEED)

def random_mode():
    print("[ROTATE] Phase: random_mode")
    endpoints = [
        "/", "/artwork/1", "/artwork/2",
        "/api/artwork/1", "/api/artwork/2", "/api/artworks"
    ]
    for _ in range(20):
        p = random.choice(endpoints)
        r = requests.get(BASE + p, headers=HEADERS)
        print(f"[rand] GET {p} => {r.status_code}")
        time.sleep(random.uniform(0.2, 1.0) * SPEED)

def honeypot_probe():
    print("[ROTATE] Phase: honeypot_probe (intentional trap hit)")
    r1 = requests.get(BASE + "/api/export-all", headers=HEADERS)
    print(f"[trap] GET /api/export-all => {r1.status_code}")
    time.sleep(1 * SPEED)
    r2 = requests.get(BASE + "/hidden/scraper-trap", headers=HEADERS)
    print(f"[trap] GET /hidden/scraper-trap => {r2.status_code}")

PHASES = [
    slow_browsing,
    fast_burst,
    enumerator,
    api_mode,
    random_mode,
    honeypot_probe
]

while True:
    phase = random.choice(PHASES)
    print(f"\n[ROTATE] Selected phase: {phase.__name__}")
    phase()
    time.sleep(1 * SPEED)
