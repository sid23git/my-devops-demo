import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_status(client):
    response = client.get("/")
    assert response.status_code == 200

def test_home_content(client):
    response = client.get("/")
    assert b"CI/CD Pipeline" in response.data

def test_health_status(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_health_content(client):
    response = client.get("/health")
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "version" in data
