import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_auth_registration_and_login():
    import uuid
    unique_email = f"citizen_{uuid.uuid4().hex[:8]}@example.com"
    
    # 1. Register new user
    reg_payload = {
        "email": unique_email,
        "password": "Password123!",
        "full_name": "Ramesh Kumar"
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 200
    data = reg_res.json()
    assert "access_token" in data
    assert data["user"]["email"] == unique_email
    assert data["user"]["full_name"] == "Ramesh Kumar"
    
    token = data["access_token"]
    
    # 2. Get current user profile with token
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["email"] == unique_email
    
    # 3. Test duplicate email registration
    dup_res = client.post("/api/auth/register", json=reg_payload)
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"].lower()
    
    # 4. Login with correct credentials
    login_payload = {
        "email": unique_email,
        "password": "Password123!"
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()
    
    # 5. Login with invalid password
    bad_login = {
        "email": unique_email,
        "password": "WrongPassword"
    }
    bad_res = client.post("/api/auth/login", json=bad_login)
    assert bad_res.status_code == 401

