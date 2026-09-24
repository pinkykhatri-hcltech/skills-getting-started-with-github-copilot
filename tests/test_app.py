from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)


def test_duplicate_signup_returns_400():
    activity_name = "Chess Club"
    original_participants = app_module.activities[activity_name]["participants"][:]
    email = "existing@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email]

    try:
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    finally:
        app_module.activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    activity_name = "Soccer Team"
    original_participants = app_module.activities[activity_name]["participants"][:]
    email = "student@mergington.edu"
    app_module.activities[activity_name]["participants"] = [email, "other@mergington.edu"]

    try:
        response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

        assert response.status_code == 200
        assert email not in app_module.activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
