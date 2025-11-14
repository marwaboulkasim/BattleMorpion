from backend.llm_api import get_llm_move
import random
from backend.config import client_AI, MODELS, URL, logger

def init_board():
    return [["" for _ in range(10)] for _ in range(10)]

def print_board(board):
    for row in board:
        print(" ".join(cell if cell else "." for cell in row))
    print("\n")

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

def fallback_move(board):
    empty = [
        (x, y)
        for y, row in enumerate(board)
        for x, c in enumerate(row)
        if c == ""
    ]
    if not empty:
        logger.info("Plus aucun coup possible, fin de la partie. Pas de gagnants")
        return None
    return random.choice(empty)

# Met à jour la grille avec le coup
def make_move(board, move, player):
    x, y = move

    if not (0 <= x < len(board[0]) and 0 <= y < len(board)):
        logger.warning(f"Coup hors grille: {move}")
        x, y = fallback_move(board)
        logger.info("Fallback en [%s, %s]", x, y)
    
    if board[y][x] != "":
        logger.warning(f"Case déjà occupée en {move}")
        x, y = fallback_move(board)
        logger.info("Fallback en [%s, %s]", x, y)

    board[y][x] = player 
    if player == "x":
        logger.info("%s (X) joue : [%s, %s]", MODELS[0], x, y)
    else:
        logger.info("%s (O) joue : [%s, %s]", MODELS[1], x, y)
    return board

def battle():
    board = init_board()
    players = [("x", lambda board: get_llm_move(board=board, model=MODELS[0], url=URL, player="x")), 
               ("o", lambda board: get_llm_move(board=board, client=client_AI, model=MODELS[1], player="o"))]
    turn = 0

    logger.info("Début du duel : %s vs %s \n", MODELS[0], MODELS[1])
    while True:
        # Sélection du joueur courant
        player_symbol, llm_func = players[turn % 2]
        move = llm_func(board)
        board = make_move(board, move, player_symbol)

        print_board(board)

        # Vérification de la victoire
        if check_winner(board, player_symbol):
            logger.info(" Le joueur %s a gagné!", player_symbol)
            break

        # Vérification si la grille est pleine -> match nul
        if all(cell != "" for row in board for cell in row):
            logger.info("Match nul!")
            break

        # Passage au joueur suivant
        turn += 1

    logger.info("------------------------------\n Fin du match !")


if __name__ == "__main__":
    battle()
