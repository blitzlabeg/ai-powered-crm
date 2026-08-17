"""Tests for the Companies JSON API â€” covers full CRUD lifecycle."""

from __future__ import annotations


def test_create_company(client):
    response = client.post(
        "/api/companies",
        json={"name": "Acme Corp", "industry": "Manufacturing", "city": "Springfield"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Acme Corp"
    assert body["industry"] == "Manufacturing"
    assert "id" in body


def test_list_companies(client):
    client.post("/api/companies", json={"name": "Beta LLC"})
    client.post("/api/companies", json={"name": "Gamma Inc"})

    response = client.get("/api/companies")
    assert response.status_code == 200
    names = [c["name"] for c in response.json()]
    assert "Beta LLC" in names
    assert "Gamma Inc" in names


def test_get_company_by_id(client):
    created = client.post("/api/companies", json={"name": "Delta Co"}).json()
    response = client.get(f"/api/companies/{created['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Delta Co"


def test_get_missing_company_returns_404(client):
    response = client.get("/api/companies/99999")
    assert response.status_code == 404


def test_update_company(client):
    created = client.post("/api/companies", json={"name": "Epsilon"}).json()
    response = client.put(
        f"/api/companies/{created['id']}", json={"industry": "Software"}
    )
    assert response.status_code == 200
    assert response.json()["industry"] == "Software"
    assert response.json()["name"] == "Epsilon"  # untouched fields remain


def test_delete_company(client):
    created = client.post("/api/companies", json={"name": "Zeta"}).json()
    response = client.delete(f"/api/companies/{created['id']}")
    assert response.status_code == 204

    follow_up = client.get(f"/api/companies/{created['id']}")
    assert follow_up.status_code == 404


def test_company_html_pages_render(client):
    created = client.post("/api/companies", json={"name": "HTML Co"}).json()

    list_page = client.get("/companies")
    assert list_page.status_code == 200
    assert "HTML Co" in list_page.text

    detail_page = client.get(f"/companies/{created['id']}")
    assert detail_page.status_code == 200
    assert "HTML Co" in detail_page.text

    new_page = client.get("/companies/new")
    assert new_page.status_code == 200
