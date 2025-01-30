import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, UserDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client


def test_create_user(client, db):
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com", "age": 30})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["age"] == 30


def test_create_user_invalid_age(client):
    response = client.post("/users/", json={"name": "Too Young", "email": "young@example.com", "age": 16})

    assert response.status_code == 422  
    data = response.json()
    assert "age" in data["detail"][0]["loc"]


def test_get_user(client, db):
    user = UserDB(name="Jane Doe", email="jane@example.com", age=25)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["age"] == 25


def test_update_user(client, db):
    user = UserDB(name="Old Name", email="old@example.com", age=40)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.put(f"/users/{user.id}", json={"name": "New Name", "email": "new@example.com", "age": 35})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "new@example.com"
    assert data["age"] == 35


def test_update_user_invalid_age(client, db):
    user = UserDB(name="Valid User", email="valid@example.com", age=30)

    db.add(user)
    db.commit()
    db.refresh(user)

    # Tentative de mise à jour avec un âge interdit (16 ans)
    response = client.put(f"/users/{user.id}", json={"name": "Invalid Age", "email": "invalid@example.com", "age": 16})

    assert response.status_code == 422
    data = response.json()
    assert "age" in data["detail"][0]["loc"]


def test_delete_user(client, db):
    user = UserDB(name="To Be Deleted", email="delete@example.com", age=50)

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "To Be Deleted"
    assert data["email"] == "delete@example.com"
    assert data["age"] == 50

    # Vérifier si l'utilisateur est bien supprimé
    response = client.get(f"/users/{user.id}")
    assert response.status_code == 404
