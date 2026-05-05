import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app

@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        client.post("/admin/reset")
        yield client
        client.post("/admin/reset")


def get(client, path, ip="1.1.1.1", ua="Mozilla/5.0"):
    return client.get(
        path,
        environ_base={"REMOTE_ADDR": ip},
        headers={"User-Agent": ua}
    )


def test_normal_user_can_browse_homepage(client):
    r = get(client, "/")
    assert r.status_code == 200


def test_single_source_rate_limit_returns_429(client):
    ip = "10.0.0.2"

    last = None
    for _ in range(25):
        last = get(client, "/api/artworks", ip=ip)

    assert last.status_code == 429


def test_hard_block_after_excessive_requests(client):
    ip = "10.0.0.3"

    last = None
    for _ in range(60):
        last = get(client, "/", ip=ip)

    assert last.status_code == 403


def test_honeypot_blocks_client(client):
    ip = "10.0.0.4"

    r = get(client, "/api/export-all", ip=ip)
    assert r.status_code == 403

    r2 = get(client, "/", ip=ip)
    assert r2.status_code == 403


def test_suspicious_user_agent_gets_blocked_after_repeated_api_scraping(client):
    ip = "10.0.0.5"

    last = None
    for artwork_id in range(1, 8):
        last = get(
            client,
            f"/api/artwork/{artwork_id}",
            ip=ip,
            ua="python-requests/2.31"
        )

    assert last.status_code in [403, 429]


def test_admin_stats_reports_defense_metrics(client):
    ip = "10.0.0.6"

    get(client, "/api/artworks", ip=ip, ua="python-requests/2.31")
    stats = client.get("/admin/stats").get_json()

    assert ip in stats["ip_stats"]
    assert "anomaly_score" in stats["ip_stats"][ip]
    assert "api_requests_in_window" in stats["ip_stats"][ip]