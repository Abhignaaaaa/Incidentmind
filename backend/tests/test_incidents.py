from fastapi.testclient import TestClient
from app.main import app
from app.database.connection import Base, engine, get_db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_incident():
    response = client.post(
        "/api/incidents",
        json={
            "title": "Test Incident",
            "service": "Test Service",
            "severity": "HIGH",
            "description": "Test description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Incident"
    assert "id" in data
