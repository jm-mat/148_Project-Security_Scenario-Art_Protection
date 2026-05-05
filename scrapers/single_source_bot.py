"""
Single-source scraper bot — simulates a basic bot hitting the API repeatedly.
Run this from the Mininet host or locally against the Flask server.

Usage:
    python3 single_source_bot.py --host 10.0.0.1 --port 5000 --rate 5 --count 100
"""
import argparse
import time
import requests

def run(host, port, rate, count):
    base = f"http://{host}:{port}"
    delay = 1.0 / rate
    results = {"200": 0, "429": 0, "403": 0, "other": 0}

    print(f"[Bot] Targeting {base} | {rate} req/s | {count} total requests")

    for i in range(count):
        try:
            r = requests.get(f"{base}/api/artworks", timeout=5)
            key = str(r.status_code) if r.status_code in (200, 429, 403) else "other"
            results[key] += 1
            print(f"  [{i+1:03d}] GET /api/artworks -> {r.status_code}")
        except Exception as e:
            results["other"] += 1
            print(f"  [{i+1:03d}] ERROR: {e}")
        time.sleep(delay)

    print("\n[Bot] Summary:", results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host",  default="127.0.0.1")
    parser.add_argument("--port",  default=5000, type=int)
    parser.add_argument("--rate",  default=5, type=float, help="requests per second")
    parser.add_argument("--count", default=100, type=int)
    args = parser.parse_args()
    run(args.host, args.port, args.rate, args.count)
