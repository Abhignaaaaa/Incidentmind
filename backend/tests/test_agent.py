from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_agent_chat():
    response = client.post(
        "/api/agent/chat",
        json={"message": "Hello agent"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
