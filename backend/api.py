from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import make_move, get_llm_move, PlayRequest, client_AI, MODELS


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
        move = get_llm_move(board=request.board, model=MODELS[0], player="x")
    else:
        move = get_llm_move(board=request.board, client=client_AI, model=MODELS[1], player="o")

    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}
