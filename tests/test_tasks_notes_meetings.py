"""Tests for Tasks, Notes, and Meetings."""

from __future__ import annotations


def test_create_and_complete_task(client):
    created = client.post("/api/tasks", json={"title": "Call the client"}).json()
    assert created["status"] == "open"

    response = client.post(f"/tasks/{created['id']}/complete", follow_redirects=True)
    assert response.status_code == 200

    task = client.get(f"/api/tasks/{created['id']}").json()
    assert task["status"] == "completed"


def test_task_can_link_to_a_related_entity(client):
    lead = client.post("/api/leads", json={"title": "Linked Lead"}).json()
    task = client.post(
        "/api/tasks",
        json={"title": "Follow up with lead", "related_type": "lead", "related_id": lead["id"]},
    ).json()
    assert task["related_type"] == "lead"
    assert task["related_id"] == lead["id"]


def test_create_note_and_list(client):
    company = client.post("/api/companies", json={"name": "Note Target"}).json()
    note = client.post(
        "/api/notes",
        json={
            "body": "Had a great first call.",
            "author": "Jamie",
            "related_type": "company",
            "related_id": company["id"],
        },
    ).json()
    assert note["body"] == "Had a great first call."

    notes = client.get(
        "/api/notes", params={"related_type": "company", "related_id": company["id"]}
    ).json()
    assert any(n["id"] == note["id"] for n in notes)


def test_create_meeting_and_summarize_without_api_key(client):
    meeting = client.post(
        "/api/meetings",
        json={
            "title": "Kickoff Call",
            "starts_at": "2026-08-01T10:00:00",
            "notes": "Discussed timeline and budget.",
        },
    ).json()
    assert meeting["title"] == "Kickoff Call"

    response = client.post(f"/meetings/{meeting['id']}/summarize", follow_redirects=True)
    assert response.status_code == 200

    updated = client.get(f"/api/meetings/{meeting['id']}").json()
    assert updated["ai_summary"] is not None
