# backend/Dockerfile

FROM python:3.11.4

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances dans l'image Docker
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers backend dans l'image
COPY . /app/

# Commande pour lancer FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
