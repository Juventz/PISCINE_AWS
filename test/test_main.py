from app.models import Base
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME") + "_test"


# Moteur sans base sélectionnée pour gérer la création/suppression
SQLALCHEMY_ROOT_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/"
engine_root = create_engine(SQLALCHEMY_ROOT_URL)

# Moteur pour la base de test
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine_test = create_engine(SQLALCHEMY_DATABASE_URL)

# Crée une session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="module")
def db():
# Créer la base de test si elle n'existe pas
    with engine_root.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE};"))

    # Créer les tables dans la base de test
    Base.metadata.create_all(bind=engine_test)

    # Créer une session pour interagir avec la base de test
    db_session = SessionLocal()

    yield db_session  # Exécute les tests avec cette session

    # Nettoyage après tests
    db_session.close()
    Base.metadata.drop_all(bind=engine_test)

    # Supprimer la base de test après les tests
    with engine_root.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(f"DROP DATABASE IF EXISTS {DATABASE};"))


# Test simple de connexion
def test_example(db):
    result = db.execute(text("SELECT 1")).fetchone()
    assert result is not None


# Test de performance avec EXPLAIN
def test_performance(db):
    result = db.execute(text("EXPLAIN SELECT * FROM users")).fetchall()
    assert len(result) > 0  # Vérifie que MySQL retourne un plan d'exécution
