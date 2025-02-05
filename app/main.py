from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import UserDB
from app.database import SessionLocal
from app.schemas import User, UserCreate

app = FastAPI()


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

    db_user = UserDB(**user.model_dump())
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
    for key, value in user.model_dump().items():
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