import numpy as np
import random
import pygame
import sys
import math
import csv

#Constants
BLUE_COLOR = (0, 0, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

ROWS = 6
COLUMNS = 7

HUMAN = 0
COMPUTER = 1

EMPTY_CELL = 0
HUMAN_PIECE = 1
COMPUTER_PIECE = 2

WINDOW_SIZE = 4

CSV_FILE_NAME = "data/connect_four_data.csv"
data = []

# Data tracking, storage and reading
#Function for writing into file
def write_data_to_csv(human_wins, human_losses, computer_wins, computer_losses):
    with open("data/connect_four_data.csv", mode='a', newline='') as csvfile:
        data_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow([human_wins, human_losses, computer_wins, computer_losses])

#Function for reading from file
def read_data_from_csv():
    data = []
    with open('data/connect_four_data.csv', mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)

    if len(data) > 1:
        human_wins = int(data[-1][0])
        human_losses = int(data[-1][1])
        computer_wins = int(data[-1][2])
        computer_losses = int(data[-1][3])
    else:
        human_wins, human_losses, computer_wins, computer_losses = 0, 0, 0, 0

    return human_wins, human_losses, computer_wins, computer_losses


#To create the grid for the connect 4 game
def create_game_board():
    game_board = np.zeros((ROWS, COLUMNS))
    return game_board

#To put the pieces in at certain positions
def place_piece(game_board, row, col, piece):
    game_board[row][col] = piece

#Check if the placement is valid or not
def is_valid_placement(game_board, col):
    return game_board[ROWS - 1][col] == EMPTY_CELL


def get_next_available_row(game_board, col):
    for r in range(ROWS):
        if game_board[r][col] == EMPTY_CELL:
            return r

#To show the game board
def display_game_board(game_board):
    print(np.flip(game_board, 0))

# To check if the current move is the winning move
def is_winning_move(game_board, piece):
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):
        for r in range(ROWS):
            if (
                game_board[r][c] == piece
                and game_board[r][c + 1] == piece
                and game_board[r][c + 2] == piece
                and game_board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if (
                game_board[r][c] == piece
                and game_board[r + 1][c] == piece
                and game_board[r + 2][c] == piece
                and game_board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(ROWS - 3):
            if (
                game_board[r][c] == piece
                and game_board[r + 1][c + 1] == piece
                and game_board[r + 2][c + 2] == piece
                and game_board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):
        for r in range(3, ROWS):
            if (
                game_board[r][c] == piece
                and game_board[r - 1][c + 1] == piece
                and game_board[r - 2][c + 2] == piece
                and game_board[r - 3][c + 3] == piece
            ):
                return True


def evaluate_game_window(window, piece):
    score = 0
    opp_piece = HUMAN_PIECE if piece == COMPUTER_PIECE else COMPUTER_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY_CELL) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY_CELL) == 2:
        score += 2
        
    if window.count(opp_piece) == 3 and window.count(EMPTY_CELL) == 1:
        score -= 4

    return score

def position_score(game_board, piece):
    score = 0
    
    # Score center column
    center_array = [int(i) for i in list(game_board[:, COLUMNS // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3
    
    # Score Horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(game_board[r, :])]
        for c in range(COLUMNS - 3):
            window = row_array[c : c + WINDOW_SIZE]
            score += evaluate_game_window(window, piece)
    
    # Score Vertical
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(game_board[:, c])]
        for r in range(ROWS - 3):
            window = col_array[r : r + WINDOW_SIZE]
            score += evaluate_game_window(window, piece)
    
    # Score positive sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [game_board[r + i][c + i] for i in range(WINDOW_SIZE)]
            score += evaluate_game_window(window, piece)
    
    # Score negative sloped diagonal
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [game_board[r + 3 - i][c + i] for i in range(WINDOW_SIZE)]
            score += evaluate_game_window(window, piece)
    
    return score
def is_terminal_node(game_board):
    return (is_winning_move(game_board, HUMAN_PIECE) or is_winning_move(game_board, COMPUTER_PIECE) or len(get_valid_positions(game_board)) == 0)

#The algorithm that makes the AI play the winning moves
def minimax(game_board, depth, alpha, beta, maximizing_player):
    valid_positions = get_valid_positions(game_board)
    is_terminal = is_terminal_node(game_board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if is_winning_move(game_board, COMPUTER_PIECE):
                return (None, 100000000000000)
            elif is_winning_move(game_board, HUMAN_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else:
            return (None, position_score(game_board, COMPUTER_PIECE))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_positions)
        for col in valid_positions:
            row = get_next_available_row(game_board, col)
            b_copy = game_board.copy()
            place_piece(b_copy, row, col, COMPUTER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    
    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_positions)
        for col in valid_positions:
            row = get_next_available_row(game_board, col)
            b_copy = game_board.copy()
            place_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                    value = new_score
                    column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_positions(game_board):
    valid_positions = []
    for col in range(COLUMNS):
        if is_valid_placement(game_board, col):
            valid_positions.append(col)
    return valid_positions

def pick_best_move(game_board, piece):
    valid_positions = get_valid_positions(game_board)
    best_score = -10000
    best_col = random.choice(valid_positions)
    for col in valid_positions:
        row = get_next_available_row(game_board, col)
        temp_board = game_board.copy()
        place_piece(temp_board, row, col, piece)
        score = position_score(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
        return best_col

def draw_game_board(game_board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE_COLOR, (c * CELL_SIZE, r * CELL_SIZE + CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.circle(screen,BLACK_COLOR, (int(c * CELL_SIZE + CELL_SIZE / 2), int(r * CELL_SIZE + CELL_SIZE + CELL_SIZE / 2)),RADIUS)
            
    for c in range(COLUMNS):
        for r in range(ROWS):
            if game_board[r][c] == HUMAN_PIECE:
                pygame.draw.circle(screen, RED_COLOR, (int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)),RADIUS)
            elif game_board[r][c] == COMPUTER_PIECE:
                pygame.draw.circle(screen,YELLOW_COLOR,(int(c * CELL_SIZE + CELL_SIZE / 2), height - int(r * CELL_SIZE + CELL_SIZE / 2)),RADIUS)
    pygame.display.update()

game_board = create_game_board()
display_game_board(game_board)
game_over = False

pygame.init()

CELL_SIZE = 100

width = COLUMNS * CELL_SIZE
height = (ROWS + 1) * CELL_SIZE

size = (width, height)

RADIUS = int(CELL_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_game_board(game_board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(HUMAN, COMPUTER)

human_wins, human_losses, computer_wins, computer_losses = read_data_from_csv()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK_COLOR, (0, 0, width, CELL_SIZE))
            posx = event.pos[0]
            if turn == HUMAN:
                pygame.draw.circle(screen, RED_COLOR, (posx, int(CELL_SIZE / 2)), RADIUS)
    
        pygame.display.update()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK_COLOR, (0, 0, width, CELL_SIZE))
    
            # Ask for Human Input
            if turn == HUMAN:
                posx = event.pos[0]
                col = int(math.floor(posx / CELL_SIZE))
    
                if is_valid_placement(game_board, col):
                    row = get_next_available_row(game_board, col)
                    place_piece(game_board, row, col, HUMAN_PIECE)
    
                    if is_winning_move(game_board, HUMAN_PIECE):
                        label = myfont.render("Human wins!!", 1, RED_COLOR)
                        screen.blit(label, (40, 10))
                        game_over = True
                        human_wins +=1
                        computer_losses += 1
                    
                    turn += 1
                    turn = turn % 2
    
                    display_game_board(game_board)
                    draw_game_board(game_board)

    # Ask for Computer Input
    if turn == COMPUTER and not game_over:
    
        col, minimax_score = minimax(game_board, 5, -math.inf, math.inf, True)
    
        if is_valid_placement(game_board, col):
            row = get_next_available_row(game_board, col)
            place_piece(game_board, row, col, COMPUTER_PIECE)
    
            if is_winning_move(game_board, COMPUTER_PIECE):
                label = myfont.render("Computer wins!!", 1, YELLOW_COLOR)
                screen.blit(label, (40, 10))
                game_over = True
                computer_wins += 1
                human_losses += 1
    
            display_game_board(game_board)
            draw_game_board(game_board)
    
            turn += 1
            turn = turn % 2
    
    if game_over:
        pygame.time.wait(3000)
        
        
write_data_to_csv(human_wins, human_losses, computer_wins, computer_losses)
