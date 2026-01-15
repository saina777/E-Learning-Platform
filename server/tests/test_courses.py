import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_course(client):
    response = client.post("/courses/", json={
        "title": "Test Course",
        "description": "Test Description"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Course"

def test_get_course(client):
    # Create course first
    create_response = client.post("/courses/", json={
        "title": "Test Course",
        "description": "Test Description"
    })
    course_id = create_response.json()["id"]
    
    # Get course
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Course"

def test_get_nonexistent_course(client):
    response = client.get("/courses/999")
    assert response.status_code == 404

def test_update_course(client):
    # Create course first
    create_response = client.post("/courses/", json={
        "title": "Original Title",
        "description": "Original Description"
    })
    course_id = create_response.json()["id"]
    
    # Update course
    response = client.put(f"/courses/{course_id}", json={
        "title": "Updated Title",
        "description": "Updated Description"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_course(client):
    # Create course first
    create_response = client.post("/courses/", json={
        "title": "To Delete",
        "description": "Will be deleted"
    })
    course_id = create_response.json()["id"]
    
    # Delete course
    response = client.delete(f"/courses/{course_id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_response = client.get(f"/courses/{course_id}")
    assert get_response.status_code == 404