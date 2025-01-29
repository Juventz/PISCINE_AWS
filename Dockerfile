# Choisir l'image de base Python
FROM python:3.11

# Créer un répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du répertoire courant dans le répertoire de travail
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Exécuter le serveur web
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]