import logging
import os
from aws_s3 import upload_to_s3

# Dossier pour stocker les logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Fichier de log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configuration du logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Fonction pour enregistrer un log
def log_operation(message):
    logging.info(message)
    upload_to_s3(LOG_FILE)

# Exemple d'utilisation
if __name__ == "__main__":
    log_operation("Test de logging : un utilisateur s'est connecté.")
