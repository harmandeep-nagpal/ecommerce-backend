from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user(db):
    response = client.post(
        "/users/register",
        json={
            "email": "pytest_user@example.com",
            "password": "TestPassword123",
            "full_name": "Pytest User"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "pytest_user@example.com"
    assert response.json()["full_name"] == "Pytest User"

def test_register_duplicate_email(db):
    user = {
        "email": "duplicate@example.com",
        "password": "TestPassword123",
        "full_name": "Duplicate User"
    }

    first_response = client.post(
        "/users/register",
        json=user
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/users/register",
        json=user
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"

def test_login_user(db):
    user = {
        "email": "login@example.com",
        "password": "TestPassword123",
        "full_name": "Login User"
    }

    register_response = client.post(
        "/users/register",
        json=user
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/users/login",
        json={
            "email": user["email"],
            "password": user["password"]
        }
    )

    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"