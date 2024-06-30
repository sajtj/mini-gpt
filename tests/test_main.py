import pytest
from fastapi.testclient import TestClient
from ..main import app

@pytest.fixture
def client():
    yield TestClient(app)

def test_register(client):
    response = client.post("/api/register/", json={"username": "testuser"})
    assert response.status_code == 200
    assert response.json() == {"username": "testuser"}

def test_login(client):
    response = client.post("/api/login/", json={"username": "testuser"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    return data["access_token"]

@pytest.fixture
def token(client):
    return test_login(client)

def test_llm(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/llm/", json={"prompt": "Test prompt"}, headers=headers)
    assert response.status_code == 200
    assert "prompt" in response.json()
    assert "response" in response.json()
    assert "tokens" in response.json()
    assert "llm_name" in response.json()

def test_usage(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/usage/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

