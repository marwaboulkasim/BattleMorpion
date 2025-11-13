# Étape 1 : image de base
FROM python:3.10-slim

# Étape 2 : copie des fichiers
WORKDIR /app
COPY . /app

# Étape 3 : installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4 : exposition du port
EXPOSE 8000

# Étape 5 : commande de démarrage
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
