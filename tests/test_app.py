from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_200_and_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "tester@example.com"

    # ensure email not present initially
    assert test_email not in activities[activity]["participants"]

    # signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # signing up again should return 400
    resp = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    assert resp.status_code == 400

    # unregister
    resp = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email not in activities[activity]["participants"]

    # unregistering again should return 400
    resp = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    assert resp.status_code == 400
