 """Tests for the Leads API, including graceful AI fallback behavior."""

from __future__ import annotations


def test_create_and_list_leads(client):
 response = client.post(
 "/api/leads",
 json={"title": "New Website Inquiry", "status": "new", "source": "website"},
 )
 assert response.status_code == 201
 lead = response.json()
 assert lead["title"] == "New Website Inquiry"
 assert lead["status"] == "new"

 listed = client.get("/api/leads").json()
 assert any(item["id"] == lead["id"] for item in listed)


def test_filter_leads_by_status(client):
 client.post("/api/leads", json={"title": "Lead A", "status": "new"})
 client.post("/api/leads", json={"title": "Lead B", "status": "qualified"})

 response = client.get("/api/leads", params={"status": "qualified"})
 assert response.status_code == 200
 titles = [item["title"] for item in response.json()]
 assert "Lead B" in titles
 assert "Lead A" not in titles


def test_update_lead_status(client):
 created = client.post("/api/leads", json={"title": "Follow up lead"}).json()
 response = client.put(f"/api/leads/{created['id']}", json={"status": "converted"})
 assert response.status_code == 200
 assert response.json()["status"] == "converted"


def test_lead_summarize_without_api_key_shows_friendly_message(client):
 """AI is disabled in tests (no OPENAI_API_KEY) ” summarizing should not
 crash; it should store a friendly explanatory message instead."""
 created = client.post("/api/leads", json={"title": "AI Test Lead"}).json()

 response = client.post(f"/leads/{created['id']}/summarize", follow_redirects=True)
 assert response.status_code == 200

 lead = client.get(f"/api/leads/{created['id']}").json()
 assert lead["ai_summary"] is not None
 assert "AI features are not configured" in lead["ai_summary"]


def test_delete_lead(client):
 created = client.post("/api/leads", json={"title": "To be deleted"}).json()
 response = client.delete(f"/api/leads/{created['id']}")
 assert response.status_code == 204
 assert client.get(f"/api/leads/{created['id']}").status_code == 404
