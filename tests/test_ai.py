 """Tests for the /api/ai endpoints (email drafting, follow-ups, insights)."""

from __future__ import annotations


def test_draft_email_without_api_key_returns_friendly_message(client):
 response = client.post(
 "/api/ai/draft-email",
 json={"purpose": "Introduce our new product", "tone": "friendly"},
 )
 assert response.status_code == 200
 body = response.json()
 assert body["ai_enabled"] is False
 assert "AI features are not configured" in body["result"]


def test_followups_requires_valid_related_entity(client):
 lead = client.post("/api/leads", json={"title": "Followup Target"}).json()
 response = client.post(
 "/api/ai/followups",
 json={"related_type": "lead", "related_id": lead["id"]},
 )
 assert response.status_code == 200
 body = response.json()
 assert isinstance(body["suggestions"], list)
 assert body["ai_enabled"] is False


def test_followups_with_unknown_entity_returns_404(client):
 response = client.post(
 "/api/ai/followups", json={"related_type": "lead", "related_id": 999999}
 )
 assert response.status_code == 404


def test_customer_insights_without_api_key(client):
 customer = client.post("/api/customers", json={"name": "Insights Co"}).json()
 response = client.post(f"/api/ai/customer-insights/{customer['id']}")
 assert response.status_code == 200
 body = response.json()
 assert body["ai_enabled"] is False
 assert "AI features are not configured" in body["result"]
