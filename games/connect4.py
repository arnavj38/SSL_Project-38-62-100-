import pygame 
import sys
import numpy as np
from game import BaseGame

blue = (30, 100, 200)
red = (220, 50, 50)
empty = (2, 27, 70)
yellow = (251, 194, 6)
white = (255, 255, 255)

quit_rect = pygame.Rect(14, 11, 119, 61)

class Connect4(BaseGame):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)

        self.current_player = 1
        self.board = np.zeros((7,7), dtype=int)
        self.rows = 7 
        self.cols = 7 

        self.GRID_X = 334      
        self.GRID_Y = 145      
        self.CELL_SIZE = 50    
        self.CIRCLE_RADIUS = 20

        self.font1 = pygame.font.Font("PressStart2P-Regular.ttf", 26)
        self.font2 = pygame.font.Font("PressStart2P-Regular.ttf", 100)

        self.bg1 = pygame.image.load("games/Connect4_final.png")
        self.bg1 = pygame.transform.scale(self.bg1, (1000,700))

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_draw(self):
        return not np.any(self.board == 0)

    def draw_board(self, screen):
        pygame.draw.rect(screen, blue, (self.GRID_X, self.GRID_Y, 350, 350))

        for row in range(self.rows):
            for col in range(self.cols):
                x = self.GRID_X + col * self.CELL_SIZE
                y = self.GRID_Y + row * self.CELL_SIZE
                cx = x + self.CELL_SIZE // 2
                cy = y + self.CELL_SIZE // 2

                if self.board[row, col] == 0:
                    pygame.draw.circle(screen, empty, (cx, cy), self.CIRCLE_RADIUS)
                elif self.board[row, col] == 1:
                    pygame.draw.circle(screen, yellow, (cx, cy), self.CIRCLE_RADIUS)
                elif self.board[row, col] == 2:
                    pygame.draw.circle(screen, red, (cx, cy), self.CIRCLE_RADIUS)

        if self.current_player == 1:
            name = self.player1
            color = yellow
        else:
            name = self.player2
            color = red

        if not self.game_over:
            text = self.font1.render(f"{name}'s Turn", True, color)
            x = (1000 - text.get_width()) // 2
            screen.blit(text, (x, 505))
        else:
            if self.is_draw():
                win_text = self.font2.render("DRAW!", True, white)
            else:
                winner_name = self.player1 if self.current_player == 1 else self.player2
                win_text = self.font2.render(f"{winner_name} WINS!", True, white)

            sub_text = self.font1.render("Click anywhere to continue", True, white)

            screen.blit(win_text, ((1000 - win_text.get_width()) // 2, 150))
            screen.blit(sub_text, ((1000 - sub_text.get_width()) // 2, 370))

    def get_next_open_row(self, col):
        if col < 0 or col >= self.cols:
            return -1
        for row in range(self.rows-1, -1, -1):
            if self.board[row, col] == 0:
                return row
        return -1

    def check_win(self, piece):
        window = np.lib.stride_tricks.sliding_window_view(self.board, (1,4))
        if np.any(np.all(window == piece, axis=3)):
            return True

        window = np.lib.stride_tricks.sliding_window_view(self.board, (4,1))
        if np.any(np.all(window == piece, axis=2)):
            return True

        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(self.board, (4,4)), axis1=2, axis2=3)
        if np.any(np.all(window == piece, axis=2)):
            return True

        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(np.fliplr(self.board), (4,4)), axis1=2, axis2=3)
        if np.any(np.all(window == piece, axis=2)):
            return True

        return False

    def run(self, screen):
        clock = pygame.time.Clock()

        while self.running:
            screen.blit(self.bg1, (0, 0))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return None, None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if quit_rect.collidepoint(x, y):
                        return None, None

                    if self.game_over:
                        if self.is_draw():
                            return "Draw", "Draw"
                        else:
                            winner = self.player1 if self.current_player == 1 else self.player2
                            loser  = self.player2 if self.current_player == 1 else self.player1
                            return winner, loser

                    col = (x - self.GRID_X) // self.CELL_SIZE
                    row = self.get_next_open_row(col)

                    if row != -1:
                        piece = self.current_player
                        self.board[row, col] = piece

                        if self.check_win(piece):
                            self.game_over = True
                        elif self.is_draw():
                            self.game_over = True
                        else:
                            self.switch_turn()

            self.draw_board(screen)
            pygame.display.flip()
            clock.tick(60)