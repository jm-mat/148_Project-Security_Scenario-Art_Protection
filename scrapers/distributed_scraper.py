"""
Distributed scraper — simulates multiple IPs hitting the server simultaneously.
Spoofs X-Forwarded-For headers to simulate distributed sources.

Usage:
    python3 distributed_scraper.py --host 10.0.0.1 --port 5000 --bots 5 --rate 3
"""
import argparse
import threading
import time
import requests
import random

FAKE_IPS = [f"10.0.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(20)]

def bot_worker(bot_id, host, port, rate, count, results, lock):
    base  = f"http://{host}:{port}"
    delay = 1.0 / rate
    fake_ip = FAKE_IPS[bot_id % len(FAKE_IPS)]
    headers = {"X-Forwarded-For": fake_ip, "User-Agent": "Mozilla/5.0 (compatible; bot)"}

    for i in range(count):
        try:
            endpoint = random.choice([
                "/api/artworks",
                f"/api/artwork/{random.randint(1,10)}",
                f"/artwork/{random.randint(1,10)}",
            ])
            r = requests.get(f"{base}{endpoint}", headers=headers, timeout=5)
            code = r.status_code
        except Exception:
            code = 0

        with lock:
            results[code] = results.get(code, 0) + 1

        time.sleep(delay)

    print(f"  [Bot-{bot_id}] ({fake_ip}) done.")


def run(host, port, num_bots, rate, count):
    results = {}
    lock    = threading.Lock()
    threads = []

    print(f"[Distributed] {num_bots} bots | {rate} req/s each | {count} requests each")

    for i in range(num_bots):
        t = threading.Thread(target=bot_worker,
                             args=(i, host, port, rate, count, results, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    total = sum(results.values())
    print(f"\n[Distributed] Results ({total} total):")
    for code, cnt in sorted(results.items()):
        print(f"  HTTP {code}: {cnt}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",  default="127.0.0.1")
    parser.add_argument("--port",  default=5000, type=int)
    parser.add_argument("--bots",  default=5, type=int)
    parser.add_argument("--rate",  default=3, type=float)
    parser.add_argument("--count", default=50, type=int)
    args = parser.parse_args()
    run(args.host, args.port, args.bots, args.rate, args.count)
