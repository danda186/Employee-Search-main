import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_basic_ok():
    r = client.get("/api/v1/employees/search", params={"org_id": 1, "q": "john"})
    assert r.status_code == 200
    body = r.json()
    assert "data" in body and "meta" in body
    assert all(set(item.keys()).issubset(set(body["meta"]["visible_columns"])) for item in body["data"])
    # Only org_id=1 results
    assert all("Globex" not in (d.get("email","") or "") for d in body["data"])

def test_org_isolation():
    # org 2 should not see org 1's emails/domains
    r = client.get("/api/v1/employees/search", params={"org_id": 2})
    assert r.status_code == 200
    data = r.json()["data"]
    # Should only return columns configured for org 2
    assert r.json()["meta"]["visible_columns"] == ["name", "position", "location"]
    # Ensure no extra keys leak
    assert all(set(d.keys()) == set(["name","position","location"]) for d in data)
