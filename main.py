from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Modèle d'utilisateur
class User(BaseModel):
    id: int
    name: str
    email: str
    age: int


# Liste d'utilisateurs temporaires
users: List[User] = []


# Route pour ajouter un utilisateur
@app.post("/users/", response_model=User)
def create_user(user: User):
    # Verification email unique
    if any(u.email == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    users.append(user)
    return user


# Route pour obtenir un utilisateur par son ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


# Route pour mettre a jour un utilisateur par son ID
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, uptade_user: User):
    for i, u in enumerate(users):
        if u.id == user_id:
            users[i] = update_user
            return update_user
    raise HTTPException(status_code=404, detail="User not found")


# Route pour supprimer un utilisateur par son ID
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            delete_user = users.pop(i)
            return {"message": "User deleted successfully",
                    "deleted_user": delete_user}
    raise HTTPException(status_code=404, detail="User not found")