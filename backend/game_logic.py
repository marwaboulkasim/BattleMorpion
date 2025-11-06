def create_empty_board(size=10):
    """Crée une grille vide size x size"""
    return [["" for _ in range(size)] for _ in range(size)]

def make_move(board, move, player):
    """Place le joueur sur la grille si la case est vide"""
    x, y = move
    if board[x][y] == "":
        board[x][y] = player
    return board

def check_winner(board, align=5):
    """
    Vérifie si un joueur a aligné 'align' symboles
    Retourne le joueur gagnant ou None
    """
    size = len(board)
    
    # Vérifier lignes
    for row in board:
        for start in range(size - align + 1):
            segment = row[start:start+align]
            if segment[0] != "" and all(cell == segment[0] for cell in segment):
                return segment[0]
    
    # Vérifier colonnes
    for col in range(size):
        for start in range(size - align + 1):
            segment = [board[row][col] for row in range(start, start+align)]
            if segment[0] != "" and all(cell == segment[0] for cell in segment):
                return segment[0]
    
    # Vérifier diagonales principales (\)
    for x in range(size - align + 1):
        for y in range(size - align + 1):
            segment = [board[x+i][y+i] for i in range(align)]
            if segment[0] != "" and all(cell == segment[0] for cell in segment):
                return segment[0]
    
    # Vérifier diagonales secondaires (/)
    for x in range(size - align + 1):
        for y in range(align-1, size):
            segment = [board[x+i][y-i] for i in range(align)]
            if segment[0] != "" and all(cell == segment[0] for cell in segment):
                return segment[0]
    
    return None
