import requests
import re
from openai import AzureOpenAI
from backend.config import logger

def get_llm_move(board, model:str, player:str, client:AzureOpenAI = None, url = None):
    board_str = "\n".join(" ".join(cell or "." for cell in row) for row in board)
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
        {board_str}
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
        logger.info("Réponse brute du modèle : %s", text)

    else:
        r = requests.post(url, json={
            "model": model,
            "prompt": prompt,
            "system": "You are a Tic-Tac-Toe AI that only returns [x, y] moves.",
            "stream": False,
        })

        data = r.json()
        text = data.get("response", "").strip()
        logger.info("Réponse brute du modèle : %s", text)
    
    if not isinstance(text, str):
        logger.error("Réponse non textuelle, error.")

    try:
        match = re.search(r"\[\s*(\d+)\s*,\s*(\d+)\s*\]", text)
        if not match:
            logger.error("Aucun pattern [x, y] détecté.")
        x, y = int(match.group(1)), int(match.group(2))
        move = [x, y]
        return move

    except Exception as e:
        logger.error("Erreur lors du parsing : %s", e)
        return None
