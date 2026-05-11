import os
import time
import json
import logging
import importlib
from functools import wraps
from flask import Flask, request, jsonify, render_template, abort
from collections import defaultdict, deque

app = Flask(__name__)

TOPOLOGY = os.getenv("TOPOLOGY", "topology1_mappings")  # change topology_mapping based on the topology being ran
topo = importlib.import_module(f"flask_app.topologies.{TOPOLOGY}")

try:
    topo = importlib.import_module(f"flask_app.topologies.{TOPOLOGY}")
    print(f"[TOPOLOGY] Loaded mapping module: {TOPOLOGY}")
except Exception as e:
    print(f"[TOPOLOGY IMPORT ERROR] Could not load {TOPOLOGY}: {e}")
    raise


SCRAPER_NAMES = topo.SCRAPER_NAMES
BOT_CLUSTERS = topo.BOT_CLUSTERS

# Dashboard visualization
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("dashboard.html")
# cluster helper
def get_cluster(ip):
    for cluster, members in BOT_CLUSTERS.items():
        if ip in members:
            return cluster
    return ip

# ── Logging ──────────────────────────────────────────────────────────────────
# Absolute path to the folder containing app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute path to logs directory
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Timestamped log file
timestamp = time.strftime("%Y%m%d_%H%M%S")

# Clean topology name
topology_name = TOPOLOGY.replace("_mappings", "")

log_filename = os.path.join(
    LOG_DIR,
    f"{topology_name}_requests_{timestamp}.log"
)

logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

# debug route
@app.route("/debug/ip")
def debug_ip():
    return {
        "remote_addr": request.remote_addr,
        "x_forwarded_for": request.headers.get("X-Forwarded-For"),
        "detected_ip": get_client_ip()
    }

# ── In-memory stores ──────────────────────────────────────────────────────────
request_counts = defaultdict(list)       # ip -> [timestamps]
api_request_counts = defaultdict(list)   # ip -> [timestamps]
global_api_requests = []                 # all API timestamps
blocked_ips = set()

anomaly_scores = defaultdict(int)        # ip -> score
anomaly_reasons = defaultdict(list)      # ip -> list of reasons
artwork_ids_seen = defaultdict(set)      # ip -> artwork ids scraped
honeypot_hits = defaultdict(int)

# ── Config ────────────────────────────────────────────────────────────────────
RATE_LIMIT_WINDOW = 10
RATE_LIMIT_MAX = 20
BLOCK_THRESHOLD = 50

API_RATE_LIMIT_MAX = 15          # stricter limit for /api routes
GLOBAL_API_LIMIT_MAX = 80        # catches distributed scraping burst
ANOMALY_BLOCK_SCORE = 6

# Only enable this for your simulation if you want X-Forwarded-For spoofing
TRUST_X_FORWARDED_FOR = os.getenv("TRUST_X_FORWARDED_FOR", "false").lower() == "true"

# ── Mock artwork data ─────────────────────────────────────────────────────────
ARTWORKS = [
    {"id": 1, "title": "Midnight Forest",     "artist": "Elena Vasquez",   "year": 2021, "style": "Digital Painting",  "price": "$1,200"},
    {"id": 2, "title": "Urban Decay No. 7",   "artist": "Marcus Chen",     "year": 2022, "style": "Photography",       "price": "$850"},
    {"id": 3, "title": "Solstice",            "artist": "Amara Osei",      "year": 2020, "style": "Watercolor",        "price": "$2,400"},
    {"id": 4, "title": "Fractured Light",     "artist": "Lena Hoffmann",   "year": 2023, "style": "Generative Art",    "price": "$500"},
    {"id": 5, "title": "The Weight of Words", "artist": "Juno Park",       "year": 2019, "style": "Mixed Media",       "price": "$3,100"},
    {"id": 6, "title": "Coastal Memory",      "artist": "Elena Vasquez",   "year": 2022, "style": "Oil Painting",      "price": "$1,800"},
    {"id": 7, "title": "Signal and Noise",    "artist": "Raj Anand",       "year": 2023, "style": "Generative Art",    "price": "$750"},
    {"id": 8, "title": "Still Life 404",      "artist": "Marcus Chen",     "year": 2021, "style": "Photography",       "price": "$620"},
    {"id": 9, "title": "Erosion",             "artist": "Amara Osei",      "year": 2023, "style": "Sculpture (3D)",    "price": "$4,500"},
    {"id": 10,"title": "Bloom Protocol",      "artist": "Lena Hoffmann",   "year": 2022, "style": "Digital Painting",  "price": "$980"},
]

ARTWORK_INDEX = {a["id"]: a for a in ARTWORKS}

# ── Defense helpers ───────────────────────────────────────────────────────────
def get_client_ip():
    """
    Returns the client IP.
    If TRUST_X_FORWARDED_FOR=true, use the header sent by bots.
    """
    if TRUST_X_FORWARDED_FOR:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

    # fallback: real remote address
    return request.remote_addr or "unknown"



def log_request(ip, path, status, flagged=False, reason=None):
    logging.info(json.dumps({
        "ip": ip,
        "path": path,
        "method": request.method,
        "status": status,
        "flagged": flagged,
        "reason": reason,
        "user_agent": request.headers.get("User-Agent", ""),
        "ts": time.time()
    }))


def prune_timestamps(timestamps, window):
    now = time.time()
    cutoff = now - window
    return [t for t in timestamps if t > cutoff]


def add_anomaly(ip, points, reason):
    anomaly_scores[ip] += points
    anomaly_reasons[ip].append({
        "reason": reason,
        "points": points,
        "ts": time.time()
    })


def check_rate_limit(ip, is_api=False):
    now = time.time()

    request_counts[ip] = prune_timestamps(request_counts[ip], RATE_LIMIT_WINDOW)
    request_counts[ip].append(now)

    count = len(request_counts[ip])

    if ip in blocked_ips or count > BLOCK_THRESHOLD:
        blocked_ips.add(ip)
        return "blocked", count, "hard block threshold exceeded"

    if count > RATE_LIMIT_MAX:
        return "limited", count, "per-ip request rate exceeded"

    if is_api:
        api_request_counts[ip] = prune_timestamps(api_request_counts[ip], RATE_LIMIT_WINDOW)
        api_request_counts[ip].append(now)

        api_count = len(api_request_counts[ip])
        if api_count > API_RATE_LIMIT_MAX:
            add_anomaly(ip, 2, "high API request rate")
            return "limited", api_count, "per-ip API rate exceeded"

        global global_api_requests
        global_api_requests = prune_timestamps(global_api_requests, RATE_LIMIT_WINDOW)
        global_api_requests.append(now)

        if len(global_api_requests) > GLOBAL_API_LIMIT_MAX:
            add_anomaly(ip, 2, "global API traffic surge")
            return "limited", len(global_api_requests), "global API surge detected"

    return "ok", count, None


def check_anomaly(ip, path):
    ua = request.headers.get("User-Agent", "").lower()

    suspicious_agents = [
        "python-requests",
        "curl",
        "wget",
        "bot",
        "scrapy",
        "spider"
    ]

    if any(agent in ua for agent in suspicious_agents):
        add_anomaly(ip, 2, "suspicious user-agent")

    if path.startswith("/api/artwork/"):
        try:
            artwork_id = int(path.rstrip("/").split("/")[-1])
            artwork_ids_seen[ip].add(artwork_id)

            if len(artwork_ids_seen[ip]) >= 6:
                add_anomaly(ip, 2, "many unique artwork detail pages scraped")
        except ValueError:
            pass

    if path in ["/api/export-all", "/hidden/scraper-trap"]:
        honeypot_hits[ip] += 1
        add_anomaly(ip, 6, "honeypot endpoint accessed")

    if anomaly_scores[ip] >= ANOMALY_BLOCK_SCORE:
        blocked_ips.add(ip)
        return "blocked", anomaly_scores[ip], "anomaly score threshold exceeded"

    return "ok", anomaly_scores[ip], None


def protect(is_api=False):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = get_client_ip()
            path = request.path

            rate_status, count, rate_reason = check_rate_limit(ip, is_api=is_api)
            if rate_status == "blocked":
                log_request(ip, path, 403, flagged=True, reason=rate_reason)
                return jsonify({
                    "error": "Forbidden — IP blocked.",
                    "reason": rate_reason,
                    "requests_in_window": count
                }), 403

            if rate_status == "limited":
                log_request(ip, path, 429, flagged=True, reason=rate_reason)
                return jsonify({
                    "error": "Too Many Requests",
                    "reason": rate_reason,
                    "retry_after": RATE_LIMIT_WINDOW,
                    "requests_in_window": count
                }), 429

            anomaly_status, score, anomaly_reason = check_anomaly(ip, path)
            if anomaly_status == "blocked":
                log_request(ip, path, 403, flagged=True, reason=anomaly_reason)
                return jsonify({
                    "error": "Forbidden — automated scraping behavior detected.",
                    "reason": anomaly_reason,
                    "anomaly_score": score
                }), 403

            response = f(*args, **kwargs)
            log_request(ip, path, 200)
            return response

        return decorated
    return decorator


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
@protect()
def index():
    return render_template("index.html", artworks=ARTWORKS)


@app.route("/artwork/<int:artwork_id>")
@protect()
def artwork_detail(artwork_id):
    artwork = ARTWORK_INDEX.get(artwork_id)
    if not artwork:
        abort(404)
    return render_template("artwork.html", artwork=artwork)


# ── API endpoints (primary scraping targets) ──────────────────────────────────
@app.route("/api/artworks")
@protect(is_api=True)
def api_artworks():
    return jsonify(ARTWORKS)


@app.route("/api/artwork/<int:artwork_id>")
@protect(is_api=True)
def api_artwork(artwork_id):
    artwork = ARTWORK_INDEX.get(artwork_id)
    if not artwork:
        return jsonify({"error": "Not found"}), 404
    return jsonify(artwork)


# ── Admin: view live stats (no rate limit on this endpoint) ───────────────────
@app.route("/admin/stats")
def admin_stats():
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW

    # --- Per-IP stats ---
    stats = {}
    for ip, timestamps in request_counts.items():The defense module is organized into several coordinated layers that work together to identify and mitigate scraper activity:

The Per‑IP Rate Limiting layer tracks requests per IP over a 10‑second window, applying soft limits above 20 requests and hard blocks above 50 to stop high‑frequency scraping from a single source.

The API‑Specific Rate Limiting layer enforces stricter thresholds for /api/* endpoints, allowing a maximum of 15 API requests per window to protect structured data commonly targeted by scrapers.

The Global API Rate Monitoring layer tracks total API traffic across all clients, triggering alerts when combined activity exceeds 80 requests per 10 seconds, enabling detection of distributed scraping attacks that stay below per‑IP limits.

The Anomaly‑Based Detection layer assigns each IP an anomaly score based on suspicious behaviors such as bot‑like User‑Agents, high API usage, or scraping many unique artwork IDs; reaching a score of 6 results in an automatic block.

The Honeypot Endpoint layer introduces fake URLs (e.g., /api/export-all, /hidden/scraper-trap) that legitimate users never access; any request to these endpoints immediately flags the client and adds a high anomaly score.

The Header & Behavior Analysis layer inspects User‑Agent strings and navigation patterns to distinguish normal users from bots, detecting missing headers, sequential scraping, and other non‑human behaviors.

Together, these layered defenses provide a robust, multi‑angle protection system capable of identifying predictable, randomized, and evasive scraper strategies.
        recent = [t for t in timestamps if t > window_start]
        recent_api = [t for t in api_request_counts[ip] if t > window_start]

        stats[ip] = {
            "ip": ip,
            "scraper_name": SCRAPER_NAMES.get(ip, "Unknown"),
            "requests_in_window": len(recent),
            "api_requests_in_window": len(recent_api),
            "total_requests": len(timestamps),
            "blocked": ip in blocked_ips,
            "anomaly_score": anomaly_scores[ip],
            "honeypot_hits": honeypot_hits[ip],
            "unique_artworks_scraped": len(artwork_ids_seen[ip]),
            "recent_reasons": anomaly_reasons[ip][-5:]
        }

    # --- Cluster-level stats ---
    cluster_stats = {}

    #Initialize cluster entries
    for cluster, members in BOT_CLUSTERS.items():
        cluster_stats[cluster] = {
            "members": members,
            "requests_in_window": 0,
            "api_requests_in_window": 0,
            "total_requests": 0,
            "blocked": False,
            "anomaly_score": 0,
            "honeypot_hits": 0,
            "unique_artworks_scraped": 0,
            "recent_reasons": []
        }

    # Populate cluster stats from IP stats
    for cluster, members in BOT_CLUSTERS.items():
        for ip in members:
            if ip in stats:
                s = stats[ip]
                cluster_stats[cluster]["requests_in_window"] += s["requests_in_window"]
                cluster_stats[cluster]["api_requests_in_window"] += s["api_requests_in_window"]
                cluster_stats[cluster]["total_requests"] += s["total_requests"]
                cluster_stats[cluster]["anomaly_score"] += s["anomaly_score"]
                cluster_stats[cluster]["honeypot_hits"] += s["honeypot_hits"]
                cluster_stats[cluster]["unique_artworks_scraped"] += s["unique_artworks_scraped"]
                cluster_stats[cluster]["recent_reasons"] += s["recent_reasons"]

                if s["blocked"]:
                    cluster_stats[cluster]["blocked"] = True

    # If a cluster is blocked, block all its members
    for cluster, cstats in cluster_stats.items():
        if cstats["blocked"]:
            for ip in cstats["members"]:
                blocked_ips.add(ip)

    return jsonify({
        "window_seconds": RATE_LIMIT_WINDOW,
        "rate_limit_max": RATE_LIMIT_MAX,
        "api_rate_limit_max": API_RATE_LIMIT_MAX,
        "global_api_limit_max": GLOBAL_API_LIMIT_MAX,
        "block_threshold": BLOCK_THRESHOLD,
        "anomaly_block_score": ANOMALY_BLOCK_SCORE,
        "global_api_requests_in_window": len([t for t in global_api_requests if t > window_start]),
        "blocked_ips": list(blocked_ips),
        "ip_stats": stats,
        "cluster_stats": cluster_stats
    })


@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    request_counts.clear()
    api_request_counts.clear()
    global_api_requests.clear()
    blocked_ips.clear()
    anomaly_scores.clear()
    anomaly_reasons.clear()
    artwork_ids_seen.clear()
    honeypot_hits.clear()
    return jsonify({"status": "reset"})

# ── Honeypot endpoints ────────────────────────────────────────────────────────
@app.route("/api/export-all")
@protect(is_api=True)
def api_export_all_honeypot():
    """
    Fake bulk-export endpoint.
    Normal users should never visit this. Bots looking for easy scrape targets may.
    """
    ip = get_client_ip()
    blocked_ips.add(ip)
    log_request(ip, request.path, 403, flagged=True, reason="honeypot bulk export endpoint")
    return jsonify({
        "error": "Forbidden — honeypot endpoint accessed."
    }), 403


@app.route("/hidden/scraper-trap")
@protect()
def hidden_scraper_trap():
    ip = get_client_ip()
    blocked_ips.add(ip)
    log_request(ip, request.path, 403, flagged=True, reason="hidden honeypot endpoint")
    return jsonify({
        "error": "Forbidden — honeypot endpoint accessed."
    }), 403


@app.route("/robots.txt")
def robots_txt():
    return (
        "User-agent: *\n"
        "Disallow: /api/\n"
        "Disallow: /api/export-all\n"
        "Disallow: /hidden/scraper-trap\n",
        200,
        {"Content-Type": "text/plain"}
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
