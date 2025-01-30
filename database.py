from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Connexion à la base de données
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creation de la table User
Base.metadata.create_all(bind=engine)
 