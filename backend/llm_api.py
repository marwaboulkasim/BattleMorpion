import requests
import ast

ollama_url = "http://127.0.0.1:11434"  # API locale Ollama

def get_llm_move(board, model="llama3", player="x"):
    prompt = f"""
    Le joueur {player} doit jouer. 
    Voici la grille actuelle (10x10) :
    {board}
    Donne UNIQUEMENT les coordonnées du prochain coup sous forme de [x, y].
    """

    r = requests.post(f"{ollama_url}/api/generate", json={
        "model": model,
        "prompt": prompt,
        "system": """You are a Tic-Tac-Toe player on a 10x10 grid.
        Two players, X and O, take turns placing their marks.
        Your goal is to get 5 in a row (horizontal, vertical or diagonal).
        Respond ONLY with a valid coordinate like [x, y].""",
        "stream": False
    })

    data = r.json()
    text = data.get("response", "").strip()
    print("Réponse brute du modèle :", text)  # pour debug

    try:
        move = ast.literal_eval(text)
        if isinstance(move, list) and len(move) == 2 and all(isinstance(i, int) for i in move):
            return move
    except:
        pass

    return [0, 0]  # fallback
