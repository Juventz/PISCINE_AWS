# import pytest
# from fastapi.testclient import TestClient
# from app.main import app
# from app.models import UserDB, Base
# from app.database import SessionLocal, engine
# from sqlalchemy.orm import Session

# # Initialiser le client de test FastAPI
# client = TestClient(app)

# # Fixture pour gérer la session de test
# @pytest.fixture(scope="function")
# def db_session():
#     session = SessionLocal()
#     Base.metadata.create_all(bind=engine)  # Créer les tables si elles n'existent pas
#     yield session  # Fournir la session au test
#     session.rollback()  # Nettoyer après chaque test
#     session.close()

# # Test de création d'utilisateur
# def test_create_user(db_session):
#     user_data = {
#         "email": "testuser@example.com",
#         "name": "Test User",
#         "age": 25
#     }
    
#     response = client.post("/users/", json=user_data)
    
#     # Debugging: Afficher la réponse pour voir s'il y a une erreur
#     print("Response status:", response.status_code)
#     print("Response body:", response.json())

#     assert response.status_code == 200
#     assert response.json()["email"] == user_data["email"]
#     assert response.json()["name"] == user_data["name"]
#     assert response.json()["age"] == user_data["age"]

# # Test pour récupérer un utilisateur
# def test_get_user(db_session):
#     user_data = {
#         "email": "testuser@example.com",
#         "name": "Test User",
#         "age": 25
#     }

#     # Insérer un utilisateur directement dans la base
#     user = UserDB(**user_data)
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)

#     response = client.get(f"/users/{user.id}")

#     # Debugging: Afficher la réponse
#     print("Response status:", response.status_code)
#     print("Response body:", response.json())

#     assert response.status_code == 200
#     assert response.json()["email"] == user_data["email"]
#     assert response.json()["name"] == user_data["name"]
#     assert response.json()["age"] == user_data["age"]
