import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.models import UserDB, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import SQLALCHEMY_DATABASE_URL
# import uuid

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = SessionLocal()  # Utilise SQLite en mémoire
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# TestClient de FastAPI pour envoyer des requêtes HTTP à l'API
client = TestClient(app)

# session de test pour chaque test
@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()


# # Fonction pour générer un email unique
# def generate_unique_email():
#     return f"testuser_{uuid.uuid4().hex}@example.com"


def test_create_user(db_session):
    # user_data = {"email": generate_unique_email(), "name": "Test User", "age": 25}
    user_data = {"email": "testuser1@example.com", "name": "Test User", "age": 25}


    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["name"] == user_data["name"]
    assert response.json()["age"] == user_data["age"]


# def test_get_user(db_session):
#     user_data = {"email": generate_unique_email(), "name": "Test User", "age": 25}

#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     print(f"User ID: {user.id}")  # Ajoutez ceci pour vérifier que l'ID est bien récupéré

#     response = client.get(f"/users/{user.id}")
#     assert response.status_code == 200
#     assert response.json()["email"] == user_data["email"]
#     assert response.json()["name"] == user_data["name"]
#     assert response.json()["age"] == user_data["age"]


# def test_update_user(db_session):
#     user_data = {"email": generate_unique_email(), "name": "Test User", "age": 25}

#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     update_data = {"email": "testuser2@example.com", "name": "Update Test User", "age": 26}
#     response = client.put(f"/users/{user.id}", json=update_data)

#     assert response.status_code == 200
#     assert response.json()["email"] == update_data["email"]
#     assert response.json()["name"] == update_data["name"]
#     assert response.json()["age"] == update_data["age"]


# def test_delete_user(db_session):
#     user_data = {"email": generate_unique_email(), "name": "Test User", "age": 25}

#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     print(f"User ID: {user.id}")

#     response = client.delete(f"/users/{user.id}")

#     assert response.status_code == 200
#     assert response.json()["email"] == user_data["email"]
#     assert response.json()["name"] == user_data["name"]
#     assert response.json()["age"] == user_data["age"]

#     db_user = db_session.query(UserDB).filter(UserDB.id == user.id).first()
#     print(db_user)
#     assert db_user is None
