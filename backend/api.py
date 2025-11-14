from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import client_AI, MODELS, URL, logger
from backend.llm_api import get_llm_move
from backend.game_logic import make_move
from backend.schemas import PlayRequest

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

@app.get("/config")
def get_config():
    return {"MODELS": MODELS}

@app.post("/play")
def play_move(request: PlayRequest):
    logger.info("Request reçu : %s", request)
    if request.player.lower() == "x":
        move = get_llm_move(board=request.board, url=URL, model=MODELS[0], player="x")
    else:
        move = get_llm_move(board=request.board, client=client_AI, model=MODELS[1], player="o")

    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}
