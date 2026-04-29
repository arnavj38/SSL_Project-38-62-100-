import pygame 
import sys
import numpy as np
from game import BaseGame

# basic colors used in the game
blue = (30, 100, 200)
red = (220, 50, 50)
empty = (2, 27, 70)
yellow = (251, 194, 6)
white = (255, 255, 255)

# area where quit button is present (top left)
quit_rect = pygame.Rect(14, 11, 119, 61)

class Connect4(BaseGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)

        # player 1 starts first
        self.current_player = 1

        # 7x7 board initialized with 0 (empty)
        self.board = np.zeros((7,7), dtype=int)
        self.rows = 7 
        self.cols = 7 

        # grid positioning and sizes (taken according to background image)
        self.GRID_X = 334      
        self.GRID_Y = 145      
        self.CELL_SIZE = 50    
        self.CIRCLE_RADIUS = 20

        # fonts for displaying text
        self.font1 = pygame.font.Font("PressStart2P-Regular.ttf", 26)
        self.font2 = pygame.font.Font("PressStart2P-Regular.ttf", 100)

        # background image for connect4
        self.bg1 = pygame.image.load("games/bg_images/Connect4_final.png")
        self.bg1 = pygame.transform.scale(self.bg1, (1000,700))

    # switches turn between player 1 and 2
    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    # checks if board is full (no empty spaces left)
    def is_draw(self):
        return not np.any(self.board == 0)

    # draws the grid and pieces on screen
    def draw_board(self, screen):
        # draw blue rectangle as grid background
        pygame.draw.rect(screen, blue, (self.GRID_X, self.GRID_Y, 350, 350))

        # loop through each cell and draw circle based on value
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.GRID_X + col * self.CELL_SIZE
                y = self.GRID_Y + row * self.CELL_SIZE
                cx = x + self.CELL_SIZE // 2
                cy = y + self.CELL_SIZE // 2

                # empty cell
                if self.board[row, col] == 0:
                    pygame.draw.circle(screen, empty, (cx, cy), self.CIRCLE_RADIUS)
                # player 1 piece
                elif self.board[row, col] == 1:
                    pygame.draw.circle(screen, yellow, (cx, cy), self.CIRCLE_RADIUS)
                # player 2 piece
                elif self.board[row, col] == 2:
                    pygame.draw.circle(screen, red, (cx, cy), self.CIRCLE_RADIUS)

        # show whose turn it is
        if self.current_player == 1:
            name = self.player1
            color = yellow
        else:
            name = self.player2
            color = red

        # if game is still going on
        if not self.game_over:
            text = self.font1.render(f"{name}'s Turn", True, color)
            x = (1000 - text.get_width()) // 2
            screen.blit(text, (x, 505))
        else:
            # if game ended, show result
            if self.is_draw():
                win_text = self.font2.render("DRAW!", True, white)
            else:
                winner_name = self.player1 if self.current_player == 1 else self.player2
                win_text = self.font2.render(f"{winner_name} WINS!", True, white)

            sub_text = self.font1.render("Click anywhere to continue", True, white)

            screen.blit(win_text, ((1000 - win_text.get_width()) // 2, 150))
            screen.blit(sub_text, ((1000 - sub_text.get_width()) // 2, 370))

    # finds the lowest empty row in a column (like real connect4 gravity)
    def get_next_open_row(self, col):
        if col < 0 or col >= self.cols:
            return -1

        # start checking from bottom row upwards
        for row in range(self.rows-1, -1, -1):
            if self.board[row, col] == 0:
                return row
        return -1  # column full

    # checks if current player has 4 in a row
    def check_win(self, piece):
        # horizontal check (1x4 window)
        window = np.lib.stride_tricks.sliding_window_view(self.board, (1,4))
        if np.any(np.all(window == piece, axis=3)):
            return True

        # vertical check (4x1 window)
        window = np.lib.stride_tricks.sliding_window_view(self.board, (4,1))
        if np.any(np.all(window == piece, axis=2)):
            return True

        # diagonal (top-left to bottom-right)
        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(self.board, (4,4)), axis1=2, axis2=3)
        if np.any(np.all(window == piece, axis=2)):
            return True

        # diagonal (top-right to bottom-left)
        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(np.fliplr(self.board), (4,4)), axis1=2, axis2=3)
        if np.any(np.all(window == piece, axis=2)):
            return True

        return False

    # main game loop
    def run(self, screen):
        clock = pygame.time.Clock()

        while self.running:
            screen.blit(self.bg1, (0, 0))

            for event in pygame.event.get():

                # if user closes window
                if event.type == pygame.QUIT:
                    return None, None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    # if quit button clicked
                    if quit_rect.collidepoint(x, y):
                        return None, None

                    # if game already over, just return result
                    if self.game_over:
                        if self.is_draw():
                            return "Draw", "Draw"
                        else:
                            winner = self.player1 if self.current_player == 1 else self.player2
                            loser  = self.player2 if self.current_player == 1 else self.player1
                            return winner, loser

                    # calculate which column was clicked
                    col = (x - self.GRID_X) // self.CELL_SIZE
                    row = self.get_next_open_row(col)

                    # if valid position, place piece
                    if row != -1:
                        piece = self.current_player
                        self.board[row, col] = piece

                        # check for win or draw after move
                        if self.check_win(piece):
                            self.game_over = True
                        elif self.is_draw():
                            self.game_over = True
                        else:
                            self.switch_turn()

            # draw everything on screen
            self.draw_board(screen)
            pygame.display.flip()
            clock.tick(60)