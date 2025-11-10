from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.game_logic import make_move
from backend.llm_api import get_llm_move, get_llm_move_azure
from backend.schemas import PlayRequest

app = FastAPI(title="Battle Morpion API")

# CORS pour ton frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur Battle Morpion API"}

@app.post("/play")
def play_move(request: PlayRequest):
    print("Request reçu :", request)

    if request.player.lower() == "x":
        move = get_llm_move(request.board, model="llama3", player="x")
    else:
        move = get_llm_move_azure(request.board, player="o")

    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}
