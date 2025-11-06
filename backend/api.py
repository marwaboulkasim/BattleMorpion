from fastapi import FastAPI
from backend.game_logic import make_move
from backend.llm_api import get_llm_move
from backend.schemas import PlayRequest

app = FastAPI(title="Battle Morpion API")

@app.get("/")
def root():
    return {"message": "Bienvenue sur Battle Morpion API"}

@app.post("/play")
def play_move(request: PlayRequest):
    print("Request reçu :", request)
    move = get_llm_move(request.board, request.model, request.player)
    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}
