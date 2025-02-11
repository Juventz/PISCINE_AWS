import pytest
from app.models import Base
from fastapi.testclient import TestClient
from app.database import SessionLocal, engine
from app.main import app


@pytest.fixture(scope="function")
def db_session():
    """Crée une session temporaire de base de données pour chaque test."""
    # Base.metadata.create_all(bind=engine) // mute car move in database.py
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    """Fournit un client FastAPI pour tester l'API."""
    return TestClient(app)
