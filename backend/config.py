from backend.openai_client import OpenAIClient
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import os

load_dotenv()
MODELS=tuple(os.getenv("MODELS", "").replace(",", " ").split())
URL=os.getenv("OLLAMA_TCP")+"/api/generate"
client_AI = OpenAIClient()

# Dossier pour les logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Fichier log principal
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Format d'affichage
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configuration basique
logging.basicConfig(
    level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler(),  # console
        RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
    ]
)

# Création du logger de ton app
logger = logging.getLogger("battle_morpion")
