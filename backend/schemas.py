from pydantic import BaseModel
from typing import List

class PlayRequest(BaseModel):
    player: str = "x"
    model: str = "llama3"
    board: List[List[str]] = [["" for _ in range(10)] for _ in range(10)]
