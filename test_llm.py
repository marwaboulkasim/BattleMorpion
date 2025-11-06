from backend.llm_api import get_llm_move
from dotenv import load_dotenv
import os

# Charger les variables d'environnement (.env)
load_dotenv()

# Récupérer le modèle depuis le .env ou par défaut "llama3"
model = os.getenv("MODEL_NAME", "llama3")

# Création d'une grille vide 10x10
board = [["" for _ in range(10)] for _ in range(10)]

# Simulation de quelques coups
board[4][4] = "x"
board[5][4] = "o"
board[4][5] = "x"

player = "o"

# Test du modèle
print(f" Test du modèle : {model}")
move = get_llm_move(board, model=model, player=player)

print("\n Grille actuelle :")
for row in board:
    print(row)

print(f"\n Coup généré pour le joueur '{player}' : {move}")
