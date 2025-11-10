from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.game_logic import make_move
# from backend.llm_api import get_llm_move
from backend.schemas import PlayRequest


from .game_logic import make_move
from .llm_api import get_llm_move

app = FastAPI(title="Battle Morpion API")

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
        move = get_llm_move(request.board, model="llama3", player="x")  # Ollama
    else:
        move = get_llm_move(request.board, model="o4-mini", player="o")  # Azure

    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}
