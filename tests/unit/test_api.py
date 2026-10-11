import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_login_failure(client):
    response = client.post("/api/v1/auth/login", json={"email": "wrong", "password": "wrong"})
    assert response.status_code == 401

def test_login_success(client):
    response = client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json
