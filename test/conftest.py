import sys
import os

# # Ajouter le répertoire app au chemin
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

# Ajouter le répertoire app au chemin
sys.path.insert(0, '/home/jaristil/My_Project/PISCINE_AWS/app')

from app.models import Base

print("Import successful!")