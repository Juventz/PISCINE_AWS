from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Récupérer les informations de connexion
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_NAME")

# Construire l'URL de connexion sans spécifier la base
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/"

def test_connection():
    try:
        # Connexion sans base spécifique
        engine = create_engine(SQLALCHEMY_DATABASE_URL)

        # Vérifier la connexion
        with engine.connect() as connection:
            print("✅ Connexion à AWS RDS réussie !")

            # Vérifier si la base de données existe
            result = connection.execute(text("SHOW DATABASES;"))
            databases = [row[0] for row in result]

            if DATABASE not in databases:
                print(f"⚠️ La base '{DATABASE}' n'existe pas. Création en cours...")
                connection.execute(text(f"CREATE DATABASE {DATABASE};"))
                print(f"✅ Base '{DATABASE}' créée avec succès.")

            else:
                print(f"✅ La base '{DATABASE}' existe déjà.")

    except SQLAlchemyError as e:
        print(f"❌ Erreur de connexion : {e}")

    except Exception as e:
        print(f"❌ Erreur inconnue : {e}")

if __name__ == "__main__":
    test_connection()
