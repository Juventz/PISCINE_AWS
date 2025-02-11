from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.schemas import UserCreate
from app import crud

# Initialiser le client de test FastAPI
client = TestClient(app)


def create_test_user():
    """Crée un utilisateur de test dans la base de données."""

    user_data = {
        "email": "testuser@example.com",
        "name": "Test User",
        "age": 42
    }
    user = UserCreate(**user_data)
    return user


def test_create_user():
    user = create_test_user()

    # Envoyer une requête POST à l'API
    response = client.post("/users/", json=user.dict())

    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["email"] == user.email
    assert response_data["name"] == user.name
    assert response_data["age"] == user.age


# def test_get_user():
#     user = create_test_user()

#     response = client.post("/users/", json=user.dict())
#     # Récupérer l'utilisateur créé
#     created_user = response.json()

#     # Envoyer une requête GET à l'API pour récupérer l'utilisateur
#     response = client.get(f"/users/{created_user['id']}")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["id"] == created_user["id"]
#     assert response_data["email"] == created_user["email"]
#     assert response_data["name"] == created_user["name"]
#     assert response_data["age"] == created_user["age"]


# def test_update_user():
#     user = create_test_user()

#     response = client.post("/users/", json=user.dict())
#     created_user = response.json()

#     updated_data = {
#         "email": "updateuser@example.com",
#         "name": "Update User",
#         "age": 24
#     }
#     response = client.put(f"/users/{created_user['id']}", json=updated_data)

#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["email"] == updated_data["email"]
#     assert response_data["name"] == updated_data["name"]
#     assert response_data["age"] == updated_data["age"]


# def test_delete_user():
#     user = create_test_user()

#     response = client.post("/users/", json=user.dict())
#     created_user = response.json()

#     response = client.delete(f"/users/{created_user['id']}")
#     assert response.status_code == 200
#     response_data = response.json()
#     assert response_data["id"] == created_user["id"]

#     # Vérifier que l'utilisateur a été supprimé de la base de données
#     response = client.get(f"/users/{created_user['id']}")
#     assert response.status_code == 404
