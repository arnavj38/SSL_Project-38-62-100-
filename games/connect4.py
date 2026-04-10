import pygame 
import sys

import numpy as np

rows = 7
cols = 7
cell_size = 100
blue = (30, 100, 200)
red = (220, 50, 50)
green = (50, 200, 100)
empty = (20, 20, 20)

pygame.init()
screen = pygame.display.set_mode((100*rows,100*cols))
pygame.display.set_caption('######  Connect-4  ######')
clock = pygame.time.Clock()

board = np.zeros((7,7), dtype=int)

def draw_board(screen,board):
    pygame.draw.rect(screen,green,(0,0,100*rows,100*cols))
    for row in range(rows):
        for column in range(cols):
            center_x = column*cell_size + cell_size//2
            center_y = row*cell_size + cell_size//2
            if board[row, column] == 0:
                pygame.draw.circle(screen,empty,(center_x,center_y),40)
            elif board[row, column] == 1:
                pygame.draw.circle(screen,blue,(center_x,center_y),40)
            elif board[row, column] == 2:
                pygame.draw.circle(screen,red,(center_x,center_y),40)

def get_next_open_row(board,col):
    for row in range(6,-1,-1):
        if board[row, col] == 0:
            return row
    return -1

def check_win(board,player):
    for row in range(rows):
        for i in range(4):
            if np.all(board[row, i:i+4] == player):
                return True
    for column in range(cols):
        for i in range(4):
            if np.all(board[i:i+4, column] == player):
                return True
    for row in range(rows-3):
        for column in range(cols-3):
            window = np.array([board[row+i,column+i] for i in range(4)])
            if np.all(window == player):
                return True
    for row in range(6,2,-1):
        for column in range(cols-3):
            window = np.array([board[row-i,column+i] for i in range(4)])
            if np.all(window == player):
                return True
    return False



game_over = False
current_player = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            column = mouse_x//cell_size
            row = get_next_open_row(board,column)
            center_x = column*cell_size + cell_size//2
            center_y = row*cell_size + cell_size//2
            if row != -1 and not game_over:
                board[row, column] = current_player
                if check_win(board,current_player):
                    print(f"Player {current_player} Wins!!")
                    game_over = True
                else:
                    if current_player == 1:
                        current_player = 2
                    else:
                        current_player = 1
                print(column)
    draw_board(screen,board)
    pygame.display.flip()
    clock.tick(60)
