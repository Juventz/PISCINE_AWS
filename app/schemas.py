from pydantic import BaseModel, EmailStr, conint


# Modèle d'utilisateur pour la création
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(ge=18)


# Modèle d'utilisateur avec l'ID
class User(UserCreate):
    id: int
