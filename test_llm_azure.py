from backend.llm_api import get_llm_move_azure

board = [["" for _ in range(10)] for _ in range(10)]
board[4][4] = "x"
board[5][4] = "o"
board[4][5] = "x"

move = get_llm_move_azure(board, player="o")

print("\nGrille actuelle :")
for row in board:
    print(row)

print(f"\nCoup généré par Azure o4-mini : {move}")
