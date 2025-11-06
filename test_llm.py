from backend.llm_api import get_llm_move

# On crée une grille vide 10x10
board = [["" for _ in range(10)] for _ in range(10)]

# On simule quelques coups pour tester le LLM
board[4][4] = "x"
board[5][4] = "o"
board[4][5] = "x"

player = "o"
model = "llama3"

# On demande au LLM de jouer
move = get_llm_move(board, model=model, player=player)

print("Grille actuelle :")
for row in board:
    print(row)
print(f"Coup généré pour le joueur {player} : {move}")
