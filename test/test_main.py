import pytest
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.models import UserDB, Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import SQLALCHEMY_DATABASE_URL

# Connexion à AWS RDS pour les tests
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    # Redéfinir la fonction get_db pour utiliser notre session de test
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def db_session():
    # Créer la base de données et les tables avant chaque test
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS My_Database_test;"))
        print(f"Base de données active : {result.fetchone()[0]}")
        conn.execute(text(f"USE My_Database_test;"))
    
    # Créer les tables si elles n'existent pas déjà
    Base.metadata.create_all(bind=engine)

    # Initialiser la session de base de données
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()  # Annuler les changements pour que les tests soient indépendants
        session.close()

        # Nettoyer après le test : supprimer les données des tables
        with engine.connect() as conn:
            conn.execute(text(f"USE My_Database_test;"))
            conn.execute(text(f"TRUNCATE TABLE users;"))  # Effacer les données de la table 'users'
        
        # Supprimer la base de données après les tests
        with engine.connect() as conn:
            conn.execute(text(f"DROP DATABASE IF EXISTS My_Database_test;"))

def test_create_user(client, db_session):
    user_data = {
        "email": "testuser@example.com",
        "name": "Test User",
        "age": 25
        }

    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert response.json()["name"] == user_data["name"]
    assert response.json()["age"] == user_data["age"]

# def test_get_user(client, db_session):
#     user_data = {
#         "email": "testuser@example.com",
#         "name": "Test User",
#         "age": 25
#         }

#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     response = client.get(f"/users/{user.id}")
#     assert response.status_code == 200
#     assert response.json()["email"] == user_data["email"]
#     assert response.json()["name"] == user_data["name"]
#     assert response.json()["age"] == user_data["age"]


# def test_update_user(db_session):
#     user_data = {
#         "email": "testuser@example.com",
#         "name": "Test User",
#         "age": 25
#         }

#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     update_data = {"email": "testuser2@example.com",
#                    "name": "Update Test User",
#                    "age": 26
#                    }
#     response = client.put(f"/users/{user.id}", json=update_data)

#     assert response.status_code == 200
#     assert response.json()["email"] == update_data["email"]
#     assert response.json()["name"] == update_data["name"]
#     assert response.json()["age"] == update_data["age"]


# def test_delete_user(db_session):
#     user_data = {
#         "email": "testuser@example.com",
#         "name": "Test User",
#         "age": 25
#     }

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
