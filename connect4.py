import numpy as np
from os import system, name

ROWS = 6
COLUMNS = 7


# ----------------------------------------------------------------------------------
def clear():
    # para windows
    if name == 'nt':
        _ = system('cls')

    # para mac e linux(aqui, os.name eh 'posix')
    else:
        _ = system('clear')

# ----------------------------------------------------------------------------------
def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

# ----------------------------------------------------------------------------------
def valid_location(board, column):
    return board[ROWS - 1][column] == 0

# ----------------------------------------------------------------------------------
def drop_piece(board, column, piece):
    for r in range(ROWS):
        if board[r][column] == 0:
            board[r][column] = piece
            return

# ----------------------------------------------------------------------------------
def is_winning_move(board, piece):
    # verifica se existem quatro peças em linha na horizontal, vertical e diagonais
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

# ----------------------------------------------------------------------------------
def minimax(board, depth, maximizing_player):
    global explored_states
    if is_winning_move(board, 2):  # IA ganhou
        return (None, 100)
    elif is_winning_move(board, 1):  # jogador humano ganhou
        return (None, -100)
    elif len(get_valid_locations(board)) == 0:  # jogo empatado
        return (None, 0)
    elif depth == 0:  # profundidade máxima atingida
        return (None, 0)

    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 2)
            explored_states += 1
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value

    else:  # minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 1)
            explored_states += 1
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value, explored_states

# ----------------------------------------------------------------------------------
def minimax_pruning(board, depth, alpha, beta, maximizing_player):
    global explored_states
    if is_winning_move(board, 2):  # IA ganhou
        return (None, 100)
    elif is_winning_move(board, 1):  # jogador humano ganhou
        return (None, -100)
    elif len(get_valid_locations(board)) == 0:  # jogo empatado
        return (None, 0)
    elif depth == 0:  # profundidade máxima atingida
        return (None, 0)

    valid_locations = get_valid_locations(board)
    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 2)
            explored_states += 1
            new_score = minimax_pruning(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            temp_board = board.copy()
            drop_piece(temp_board, col, 1)
            explored_states += 1
            new_score = minimax_pruning(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


# ----------------------------------------------------------------------------------
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMNS):
        if valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


# ----------------------------------------------------------------------------------
def count_two_piece(board, piece):
    count = 0
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == 0:
                count +=1
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == 0:
               count +=1
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == 0:
                count +=1
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == 0:
                count +=1

    return count

# ----------------------------------------------------------------------------------
def count_three_piece(board, piece):
    count = 0
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == 0:
                count +=1
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == 0:
                count +=1
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == 0:
                count +=1
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == 0:
                count +=1
    return count

# ----------------------------------------------------------------------------------
def count_weight(board, piece):
    count = 0
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == piece:
                count += weights_board[r][c]
    return count

# ----------------------------------------------------------------------------------
def heuristic_calculation(board):
    return (count_weight(board ,1) + count_two_piece(board,1) + 2 * count_three_piece(board,1) ) - ( count_weight(board, 2) + count_two_piece(board,2) + 2 * count_three_piece(board,2))

# ----------------------------------------------------------------------------------
def create_weights_board():
    matriz = [[0] * COLUMNS for _ in range(ROWS)]
    
    for i in range(ROWS):
        for j in range(COLUMNS):
            valor = min(i, j, ROWS - i - 1, COLUMNS - j - 1) + 1
            matriz[i][j] = valor
    
    return matriz

# ----------------------------------------------------------------------------------
def imprimir_matriz(matriz):
    mat90= np.rot90(matriz, k = 1, axes = (0, 1))
    mat180= np.rot90(mat90, k = 1, axes = (0, 1))

    for l in mat180:
        for element in l:
            if element == 0:
                print("_", end=' ')
            else:
                if element == 1: 
                    print("X", end=' ')
                else:
                    print("O", end=' ')
        print()
# ----------------------------------------------------------------------------------
# CSI457 e CSI701
# Programa Principal
# Data: 06/05/2023
# ----------------------------------------------------------------------------------
board = create_board()
weights_board = create_weights_board()
game_over = False
turn = 0
explored_states = 0

clear()
opc = input("Deseja realizar poda? [S/N]")
while opc != "S" and opc != "N": 
    opc = input("Deseja realizar poda? [S/N]")

while not game_over:
    explored_states = 0
    # Movimento do Jogador 1
    if turn == 0:
        col = int(input("Jogador 1, selecione a coluna ({}-0):".format(COLUMNS-1)))
        while col < 0 or col > COLUMNS -1: 
            col = int(input("Jogador 1, selecione a coluna ({}-0):".format(COLUMNS-1)))
        if valid_location(board, col):
            drop_piece(board, col, 1)
            if is_winning_move(board, 1):
                print("Jogador 1 Vence!! Parabéns!!")
                game_over = True

    # Movimento da IA
    else:
        if opc == "N":
            col, minimax_score= minimax(board, 4, True)
        else:
            col, minimax_score= minimax_pruning(board, 4,-1000000000, 1000000000, True)
        if valid_location(board, col):
            drop_piece(board, col, 2)
            if is_winning_move(board, 2):
                print("Jogador 2 Vence!!!")
                game_over = True

    imprimir_matriz(board)
    print(" ")
    print("Heuristica: ", heuristic_calculation(board))
    print("Estados explorados:  ", explored_states)
    print(" ")
    turn += 1
    turn = turn % 2