from backend.llm_api import get_llm_move
#LLM répond correctement et renvoie bien un coup [x, y] valide.
board = [["" for _ in range(10)] for _ in range(10)]
move = get_llm_move(board, model="llama3", player="x")
print("Move généré :", move)
