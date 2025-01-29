from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, conint
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Connexion à la base de données
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base de données
Base = declarative_base()


# Modèle de la table User
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)


# Création de la table User
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Modèle d'utilisateur pour la création
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: conint(ge=18)


# Modèle d'utilisateur avec l'ID
class User(UserCreate):
    id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Route pour ajouter un utilisateur
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Verification email unique
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Route pour obtenir un utilisateur par son ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Route pour mettre a jour un utilisateur par son ID
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Verification email unique
    if db_user.email != user.email:
        db_user_email = db.query(UserDB).filter(UserDB.email == user.email).first()
        if db_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # Mise à jours des champs
    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Route pour supprimer un utilisateur par son ID
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user
