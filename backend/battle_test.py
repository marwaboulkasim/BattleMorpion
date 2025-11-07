from llm_api import get_llm_move, get_llm_move_azure

# Initialisation de la grille 10x10 vide
def init_board():
    return [["" for _ in range(10)] for _ in range(10)]

# Affiche la grille dans le terminal
def print_board(board):
    for row in board:
        print(" ".join(cell if cell else "." for cell in row))
    print("\n")

# Vérifie si un joueur a gagné (alignement de 5)
def check_winner(board, player):
    N = 10
    for i in range(N):
        for j in range(N):
            # horizontal
            if j <= N - 5 and all(board[i][j+k] == player for k in range(5)):
                return True
            # vertical
            if i <= N - 5 and all(board[i+k][j] == player for k in range(5)):
                return True
            # diagonale droite
            if i <= N - 5 and j <= N - 5 and all(board[i+k][j+k] == player for k in range(5)):
                return True
            # diagonale gauche
            if i <= N - 5 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                return True
    return False

# Met à jour la grille avec le coup
def make_move(board, move, player):
    x, y = move
    if board[x][y] == "":
        board[x][y] = player
    return board

def battle():
    board = init_board()
    players = [("x", get_llm_move), ("o", get_llm_move_azure)]
    turn = 0

    print(" Début du duel : Llama3 (Ollama) vs o4-mini (Azure)\n")
    while True:
        player_symbol, llm_func = players[turn % 2]
        move = llm_func(board, player=player_symbol)
        board = make_move(board, move, player_symbol)

        print(f"{'Llama3 (X)' if player_symbol == 'x' else 'Azure o4-mini (O)'} joue : {move}")
        print_board(board)

        if check_winner(board, player_symbol):
            print(f" Le joueur {player_symbol} a gagné !")
            break

        # Si la grille est pleine
        if all(cell != "" for row in board for cell in row):
            print(" Match nul !")
            break

        turn += 1

    print("------------------------------\n Fin du match !")

if __name__ == "__main__":
    battle()
