import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/signup?email=removeme@mergington.edu")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_for_activity_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    # Sign up once
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]


def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "Participant removed" in response.json()["message"]
