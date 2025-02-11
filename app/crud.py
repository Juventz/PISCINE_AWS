from sqlalchemy.orm import Session
from app.models import UserDB
from app.schemas import UserCreate


def create_user(db: Session, user: UserCreate):

    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
