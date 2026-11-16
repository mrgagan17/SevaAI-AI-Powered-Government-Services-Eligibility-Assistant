import uuid
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SevaAI API"
    assert "disclaimer" in data

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "indexed_chunks" in data

def test_profile_api():
    # 1. Unauthenticated request must return 401 Unauthorized
    unauth_res = client.get("/api/profile")
    assert unauth_res.status_code == 401

    # 2. Register a unique test user to obtain auth token
    test_email = f"citizen_profile_{uuid.uuid4().hex[:8]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "email": test_email,
        "password": "Password123!",
        "full_name": "Test Citizen"
    })
    assert reg_res.status_code == 200
    token = reg_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. GET authenticated profile
    response = client.get("/api/profile", headers=headers)
    assert response.status_code == 200
    profile = response.json()
    assert "id" in profile
    assert profile["name"] == "Test Citizen"

    # 4. POST update profile
    update_payload = {
        "name": "Test Citizen",
        "age": 28,
        "education": "Postgraduate",
        "category": "OBC",
        "annual_income": 200000.0
    }
    post_res = client.post("/api/profile", json=update_payload, headers=headers)
    assert post_res.status_code == 200
    updated = post_res.json()
    assert updated["name"] == "Test Citizen"
    assert updated["age"] == 28
