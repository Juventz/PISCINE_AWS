from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

# Connexion au moteur sans base de données (pour interroger toutes les bases)
SQLALCHEMY_ROOT_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/"
engine_root = create_engine(SQLALCHEMY_ROOT_URL)

# Connexion à la base de données réelle
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base de données si elle n'existe pas
with engine_root.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE};"))
    # Supprimer mes databases existantes
    # conn.execute(text("DROP DATABASE IF EXISTS My_Database;"))
    # print("Database 'My_Database' dropped.")
    # conn.execute(text("DROP DATABASE IF EXISTS My_Database_test;"))
    # print("Database 'My_Database_test' dropped.")

# Afficher toutes les bases de données existantes
with engine_root.connect() as conn:
    result = conn.execute(text("SHOW DATABASES;"))
    print("Existing databases:")
    for row in result:
        print(row[0])

# Créer les tables de la base de données
Base.metadata.create_all(bind=engine)
