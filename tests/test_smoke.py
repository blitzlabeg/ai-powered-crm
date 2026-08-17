 """Smoke tests: app starts, health check works, dashboard renders."""

from __future__ import annotations


def test_health_check(client):
 response = client.get("/health")
 assert response.status_code == 200
 body = response.json()
 assert body["status"] == "ok"
 assert body["app"] == "ai-powered-crm"
 assert body["ai_enabled"] is False # no API key configured in tests


def test_dashboard_page_loads(client):
 response = client.get("/")
 assert response.status_code == 200
 assert "Dashboard" in response.text or "Welcome back" in response.text


def test_unknown_route_returns_404(client):
 response = client.get("/companies/9999")
 assert response.status_code == 404
