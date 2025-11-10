from llm_api import get_llm_move
from backend import client_AI, MODELS

def init_board():
    """
    Crée une grille vide 10x10.
    Chaque cellule vide contient "".
    """
    return [["" for _ in range(10)] for _ in range(10)]


# Affichage de la grille

def print_board(board):
    """
    Affiche la grille dans le terminal.
    - "." représente une case vide
    - "x" ou "o" représente les symboles des joueurs
    """
    for row in board:
        print(" ".join(cell if cell else "." for cell in row))
    print("\n")  # Ligne vide pour séparer les tours


# Vérification de victoire

def check_winner(board, player):
    """
    Vérifie si le joueur 'player' a aligné 5 symboles.
    Teste 4 directions :
    - horizontal
    - vertical
    - diagonale droite (\)
    - diagonale gauche (/)
    """
    N = 10  # Taille de la grille
    for i in range(N):
        for j in range(N):
            # Horizontal : de (i,j) à (i,j+4)
            if j <= N - 5 and all(board[i][j+k] == player for k in range(5)):
                return True
            # Vertical : de (i,j) à (i+4,j)
            if i <= N - 5 and all(board[i+k][j] == player for k in range(5)):
                return True
            # Diagonale droite (\) : de (i,j) à (i+4,j+4)
            if i <= N - 5 and j <= N - 5 and all(board[i+k][j+k] == player for k in range(5)):
                return True
            # Diagonale gauche (/) : de (i,j) à (i+4,j-4)
            if i <= N - 5 and j >= 4 and all(board[i+k][j-k] == player for k in range(5)):
                return True
    return False  # Pas de victoire trouvée


#  Jouer un coup

def make_move(board, move, player):
    """
    Place le symbole du joueur sur la grille.
    move : tuple (x, y)
    """
    x, y = move
    if board[x][y] == "":  # Vérifie que la case est vide
        board[x][y] = player
    return board


# Boucle principale du jeu

def battle():
    board = init_board()
    players = [("x", lambda board: get_llm_move(board=board, model=MODELS[0], player="x")), 
               ("o", lambda board: get_llm_move(board=board, client=client_AI, model=MODELS[1], player="o"))]
    turn = 0

    print(f"Début du duel : {MODELS[0]} vs {MODELS[1]}\n")
    while True:
        # Sélection du joueur courant
        player_symbol, llm_func = players[turn % 2]
        move = llm_func(board)
        board = make_move(board, move, player_symbol)

        print(f"{MODELS[0]} (X) joue : {move}" if player_symbol == "x" else f"{MODELS[1]} (O) joue : {move}")
        print_board(board)

        # Vérification de la victoire
        if check_winner(board, player_symbol):
            print(f" Le joueur {player_symbol} a gagné  !")
            break

        # Vérification si la grille est pleine -> match nul
        if all(cell != "" for row in board for cell in row):
            print(" Match nul !")
            break

        # Passage au joueur suivant
        turn += 1

    print("------------------------------\n Fin du match !")




if __name__ == "__main__":
    battle()
