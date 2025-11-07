import requests
import ast
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

def get_llm_move(board, model="llama3", player="x"):
    prompt = f"""
    Tu es un joueur de morpion (Tic-Tac-Toe) sur une grille 10x10.
    Deux joueurs, X et O, jouent à tour de rôle.
    L'objectif est d'aligner 5 symboles consécutifs (horizontal, vertical ou diagonal).
    Le joueur actuel est {player}. Voici la grille actuelle :
    {board}

    Règles :
    1. Ne joue jamais sur une case déjà occupée.
    2. Si tu peux aligner 5 symboles, fais-le.
    3. Si l'adversaire peut aligner 5 symboles au prochain tour, bloque-le.
    4. Sinon, joue un coup stratégique pour te rapprocher de 5 alignés.
    5. Répond STRICTEMENT avec un format : [x, y] (indices de 0 à 9).

    Exemple de réponse correcte : [4, 7]
    Ne réponds pas avec du texte ou autre chose.
    """

    r = requests.post(f"{OLLAMA_URL}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "system": "You are a Tic-Tac-Toe AI that only returns [x, y] moves.",
        "stream": False
    })

    data = r.json()
    text = data.get("response", "").strip()
    print("Réponse brute du modèle :", text)

    try:
        move = ast.literal_eval(text)
        if isinstance(move, list) and len(move) == 2 and all(isinstance(i, int) for i in move):
            return move
    except Exception as e:
        print("Erreur lors du parsing :", e)

    return [0, 0]

def get_llm_move_azure(board, player="o"):
    client = AzureOpenAI(
    api_key=os.getenv("AZURE_API_KEY"),
    api_version="2024-12-01-preview",  # ← change cette ligne
    azure_endpoint=os.getenv("AZURE_ENDPOINT")
)


    prompt = f"""
    Tu es un joueur de morpion sur une grille 10x10.
    Le joueur actuel est {player}.
    Voici la grille :
    {board}
    
    Règles :
    - Ne joue jamais sur une case déjà occupée.
    - Si tu peux gagner, fais-le.
    - Sinon, bloque ton adversaire.
    - Réponds UNIQUEMENT avec un format [x, y] (indices 0 à 9).
    """

    response = client.chat.completions.create(
        model=os.getenv("AZURE_MODEL"),
        messages=[
            {"role": "system", "content": "Tu es un joueur de morpion stratégique."},
            {"role": "user", "content": prompt}
        ]
    )

    move_text = response.choices[0].message.content.strip()
    print("Réponse brute Azure :", move_text)

    try:
        move = ast.literal_eval(move_text)
        if isinstance(move, list) and len(move) == 2:
            return move
    except Exception:
        pass

    return [0, 0]