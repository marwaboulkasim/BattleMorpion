from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .game_logic import make_move
from .llm_api import get_llm_move
from .schemas import PlayRequest

app = FastAPI(title="Battle Morpion API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def root():
    return {"message": "Bienvenue sur Battle Morpion API"}

@app.post("/api/play")
def play_move(request: PlayRequest):
    print("Request reçu :", request)

    if request.player.lower() == "x":
        move = get_llm_move(request.board, model="llama3", player="x") 
    else:
        move = get_llm_move(request.board, model="o4-mini", player="o")  

    updated_board = make_move(request.board, move, request.player)
    return {"board": updated_board, "move": move}


frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(frontend_path / "index.html")
