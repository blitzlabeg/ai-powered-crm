"""Tests for the sales pipeline (Deal) API and the kanban stage-move endpoint."""

from __future__ import annotations


def test_create_deal_defaults_to_prospecting(client):
    response = client.post("/api/deals", json={"title": "New Deal", "value": 5000})
    assert response.status_code == 201
    body = response.json()
    assert body["stage"] == "prospecting"
    assert body["value"] == 5000


def test_move_deal_stage_via_kanban_endpoint(client):
    created = client.post("/api/deals", json={"title": "Kanban Deal"}).json()

    response = client.post(
        f"/pipeline/{created['id']}/stage", json={"stage": "negotiation"}
    )
    assert response.status_code == 200
    assert response.json()["stage"] == "negotiation"

    updated = client.get(f"/api/deals/{created['id']}").json()
    assert updated["stage"] == "negotiation"


def test_move_deal_stage_rejects_invalid_stage(client):
    created = client.post("/api/deals", json={"title": "Bad Stage Deal"}).json()
    response = client.post(
        f"/pipeline/{created['id']}/stage", json={"stage": "not_a_real_stage"}
    )
    assert response.status_code == 400


def test_pipeline_board_page_renders(client):
    client.post("/api/deals", json={"title": "Board Deal", "value": 1200})
    response = client.get("/pipeline")
    assert response.status_code == 200
    assert "Board Deal" in response.text


def test_deal_recommendation_without_api_key(client):
    created = client.post("/api/deals", json={"title": "Recommend Me"}).json()
    response = client.post(f"/pipeline/{created['id']}/recommend", follow_redirects=True)
    assert response.status_code == 200

    deal = client.get(f"/api/deals/{created['id']}").json()
    assert deal["ai_recommendation"] is not None
