import requests
import re
from openai import AzureOpenAI
from backend import URL

def fallback_move(board):
    empty = [(x, y) for y, row in enumerate(board) for x, c in enumerate(row) if c == ""]
    if not empty:
        return [0, 0]
    return empty[0]

def get_llm_move(board, model:str, player:str, client:AzureOpenAI = None):
    prompt = f"""
        You play 10x10 tic-tac-toe. You are {player}.
        Goal: 5 in a row.
        Rules:
        - Only play on empty cells.
        - If you can win, do it.
        - If opponent can win next, block.
        - Otherwise play a good move.
        Return ONLY: [x, y] with 0-9 indices.
        If you output anything else than [x, y], your answer is invalid.
        Board:
        {board}
        """
    if isinstance(client, AzureOpenAI):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Tic-Tac-Toe AI that only returns [x, y] moves."},
                {"role": "user", "content": prompt}
            ]
        )

        text = response.choices[0].message.content.strip()
        print(text)
        print("Réponse brute du modèle :", text)

    else:
        r = requests.post(f"{URL}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "system": "You are a Tic-Tac-Toe AI that only returns [x, y] moves.",
            "stream": False,
            "options": {"num_predict": 16,"temperature": 0.2}
        })

        data = r.json()
        text = data.get("response", "").strip()
        print("Réponse brute du modèle :", text)
    
    if not isinstance(text, str):
        print("Réponse non textuelle, fallback.")
        return fallback_move(board)

    try:
        match = re.search(r"\[\s*(\d+)\s*,\s*(\d+)\s*\]", text)
        if not match:
            print("Aucun pattern [x, y] détecté, fallback.")
            return fallback_move(board)
        x, y = int(match.group(1)), int(match.group(2))
        move = [x, y]
        if not (0 <= x < len(board[0]) and 0 <= y < len(board)):
            print(f"Coup hors grille {move}, fallback.")
            return fallback_move(board)
        if board[y][x] != "":
            print(f"Coup sur case occupée {move}, fallback.")
            return fallback_move(board)
        
        return move

    except Exception as e:
        print("Erreur lors du parsing :", e)
        return fallback_move(board)
