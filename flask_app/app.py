import os
import time
import json
import logging
from collections import defaultdict
from functools import wraps
from flask import Flask, request, jsonify, render_template, abort

app = Flask(__name__)

# ── Logging ──────────────────────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/requests.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

# ── In-memory stores ──────────────────────────────────────────────────────────
request_counts = defaultdict(list)   # ip -> [timestamps]
blocked_ips    = set()

# ── Config ────────────────────────────────────────────────────────────────────
RATE_LIMIT_WINDOW = 10   # seconds
RATE_LIMIT_MAX    = 20   # requests per window before rate-limit
BLOCK_THRESHOLD   = 50   # requests per window before hard block

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

# ── Helpers ───────────────────────────────────────────────────────────────────
def log_request(ip, path, status, flagged=False):
    logging.info(json.dumps({
        "ip": ip, "path": path, "status": status,
        "flagged": flagged, "ts": time.time()
    }))


def check_rate_limit(ip):
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    timestamps = [t for t in request_counts[ip] if t > window_start]
    timestamps.append(now)
    request_counts[ip] = timestamps
    count = len(timestamps)

    if ip in blocked_ips or count > BLOCK_THRESHOLD:
        blocked_ips.add(ip)
        return "blocked", count
    if count > RATE_LIMIT_MAX:
        return "limited", count
    return "ok", count


def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ip = request.remote_addr
        status, count = check_rate_limit(ip)

        if status == "blocked":
            log_request(ip, request.path, 403, flagged=True)
            return jsonify({"error": "Forbidden — IP blocked due to excessive requests."}), 403

        if status == "limited":
            log_request(ip, request.path, 429, flagged=True)
            return jsonify({
                "error": "Too Many Requests",
                "retry_after": RATE_LIMIT_WINDOW,
                "requests_in_window": count
            }), 429

        log_request(ip, request.path, 200)
        return f(*args, **kwargs)
    return decorated


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
@rate_limit
def index():
    return render_template("index.html", artworks=ARTWORKS)


@app.route("/artwork/<int:artwork_id>")
@rate_limit
def artwork_detail(artwork_id):
    artwork = ARTWORK_INDEX.get(artwork_id)
    if not artwork:
        abort(404)
    return render_template("artwork.html", artwork=artwork)


# ── API endpoints (primary scraping targets) ──────────────────────────────────
@app.route("/api/artworks")
@rate_limit
def api_artworks():
    return jsonify(ARTWORKS)


@app.route("/api/artwork/<int:artwork_id>")
@rate_limit
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
    stats = {}
    for ip, timestamps in request_counts.items():
        recent = [t for t in timestamps if t > window_start]
        stats[ip] = {
            "requests_in_window": len(recent),
            "total_requests": len(timestamps),
            "blocked": ip in blocked_ips,
        }
    return jsonify({
        "window_seconds": RATE_LIMIT_WINDOW,
        "rate_limit_max": RATE_LIMIT_MAX,
        "block_threshold": BLOCK_THRESHOLD,
        "blocked_ips": list(blocked_ips),
        "ip_stats": stats,
    })


@app.route("/admin/reset", methods=["POST"])
def admin_reset():
    request_counts.clear()
    blocked_ips.clear()
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
