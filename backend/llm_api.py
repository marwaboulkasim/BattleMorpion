import os
import ast
import requests
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")



def get_llm_move(board, model="llama3", player="x"):
    """
    Gère à la fois Ollama (local) et Azure OpenAI pour générer un coup de morpion.
    Retourne un move [x, y].
    """

    prompt = f"""
    Tu joues au morpion 10x10.
    Le joueur actuel est {player}.
    Objectif : aligner 5 symboles consécutifs (horizontal, vertical, diagonal).
    Voici la grille :
    {board}

    Règles :
    1. Ne joue jamais sur une case déjà occupée.
    2. Si tu peux gagner, fais-le.
    3. Sinon, bloque ton adversaire.
    4. Sinon, joue un coup stratégique.
    5. Réponds STRICTEMENT au format [x, y].
    Exemple : [3, 5]

    """

    if model == "o4-mini":
        try:
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_API_KEY"),
                api_version="2024-12-01-preview",
                azure_endpoint=os.getenv("AZURE_ENDPOINT")
            )

            response = client.chat.completions.create(
                model=os.getenv("AZURE_MODEL", "o4-mini"),
                messages=[
                    {"role": "system", "content": "Tu es un joueur de morpion stratégique."},
                    {"role": "user", "content": prompt}
                ]
            )

            move_text = response.choices[0].message.content.strip()
            print("Réponse brute Azure :", move_text)

            move = ast.literal_eval(move_text)
            if isinstance(move, list) and len(move) == 2:
                return move

        except Exception as e:
            print(" Erreur Azure :", e)
            return [0, 0]


    else:
        try:
            r = requests.post(f"{OLLAMA_URL}/api/generate", json={
                "model": model,
                "prompt": prompt,
                "system": "You are a Tic-Tac-Toe AI that only returns [x, y].",
                "stream": False
            }, timeout=25)

            data = r.json()
            text = data.get("response", "").strip()
            print("Réponse brute Ollama :", text)

            move = ast.literal_eval(text)
            if isinstance(move, list) and len(move) == 2 and all(isinstance(i, int) for i in move):
                return move

        except Exception as e:
            print(" Erreur Ollama :", e)
            return [0, 0]

    return [0, 0]
