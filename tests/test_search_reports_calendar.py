"""Tests for global search, reports, and the calendar page."""

from __future__ import annotations


def test_search_finds_matching_company(client):
    client.post("/api/companies", json={"name": "Searchable Widgets Inc"})
    response = client.get("/search", params={"q": "Searchable"})
    assert response.status_code == 200
    assert "Searchable Widgets Inc" in response.text


def test_search_with_no_query_shows_prompt(client):
    response = client.get("/search")
    assert response.status_code == 200


def test_reports_page_renders_with_data(client):
    client.post("/api/deals", json={"title": "Report Deal", "value": 2500, "stage": "closed_won"})
    client.post("/api/leads", json={"title": "Report Lead", "source": "referral"})

    response = client.get("/reports")
    assert response.status_code == 200
    assert "Reports" in response.text


def test_calendar_page_renders(client):
    response = client.get("/calendar")
    assert response.status_code == 200
    assert "Calendar" in response.text


def test_calendar_navigation_params(client):
    response = client.get("/calendar", params={"year": 2027, "month": 1})
    assert response.status_code == 200
    assert "2027" in response.text
