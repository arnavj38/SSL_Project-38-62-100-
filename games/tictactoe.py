import pygame
import sys
import numpy as np
from game import BaseGame
from numpy.lib.stride_tricks import sliding_window_view

GRID_X = 287 # x-offset of top left corner of grid
GRID_Y = 147 # y-offset of top left corner of grid
GRID_SIZE = 320 # width and height of grid
GRID_N = 10 # number of cells in row and column
CELL = GRID_SIZE // GRID_N # size of each cell
PAD = CELL // 6 #space to be left in cell

#colours
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
PINK = (255, 60, 220)

FONT = pygame.font.SysFont("consolas", 16, bold=True)

# QUIT button area
QUIT_RECT = pygame.Rect(30, 20, 120, 60)

# defining position of a cell
def cell_origin(row, col):
    return (GRID_X + col * CELL, GRID_Y + row * CELL)

# getting cell index by its position
def pixel_to_cell(px, py):
    if GRID_X <= px < GRID_X + GRID_SIZE and GRID_Y <= py < GRID_Y + GRID_SIZE:
        return (py - GRID_Y) // CELL, (px - GRID_X) // CELL
    return None

# drawing X function
def draw_x(screen, row, col):
    cx, cy = cell_origin(row, col)
    pygame.draw.line(screen, CYAN, (cx + PAD, cy + PAD), (cx + CELL - PAD, cy + CELL - PAD), 2)
    pygame.draw.line(screen, CYAN, (cx + CELL - PAD, cy + PAD), (cx + PAD, cy + CELL - PAD), 2)

# drawing y function
def draw_o(screen, row, col):
    cx, cy = cell_origin(row, col)
    center = (cx + CELL // 2, cy + CELL // 2)
    radius = (CELL // 2) - PAD
    pygame.draw.circle(screen, PINK, center, radius, 2)

# the line which will connect the winning 5
def draw_win_line(screen, game):
    if not game.win_line:
        return

    (r1, c1), (r2, c2) = game.win_line

    x1 = GRID_X + c1 * CELL + CELL // 2
    y1 = GRID_Y + r1 * CELL + CELL // 2
    x2 = GRID_X + c2 * CELL + CELL // 2
    y2 = GRID_Y + r2 * CELL + CELL // 2

    color = CYAN if game.winner == 1 else PINK
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)


class TicTacToe(BaseGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        self.board = np.zeros((GRID_N, GRID_N), dtype=int)
        self.winner = None
        self.win_line = None

        # setting the background for the game
        self.bg = pygame.image.load("games/bg_images/tictactoe.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 700))

    def place(self, row, col):
        if self.board[row, col] != 0 or self.game_over:
            return

        self.board[row, col] = self.current_player 

        win = self.check_win(self.current_player)

        if win:
            self.game_over = True
            self.winner = self.current_player
            self.win_line = win

        elif np.all(self.board != 0):
            self.game_over = True

        else:
            self.switch_turn()   

    def check_win(self, piece):
        b = self.board

        window = sliding_window_view(b, (1, 5))
        mask = np.all(window == piece, axis=3)
        if np.any(mask):
            r, c = np.argwhere(mask)[0]
            return (r, c), (r, c + 4)

        window = sliding_window_view(b, (5, 1))
        mask = np.all(window == piece, axis=2)
        if np.any(mask):
            r, c = np.argwhere(mask)[0]
            return (r, c), (r + 4, c)

        window = sliding_window_view(b, (5, 5))
        diag = np.diagonal(window, axis1=2, axis2=3)
        mask = np.all(diag == piece, axis=2)
        if np.any(mask):
            r, c = np.argwhere(mask)[0]
            return (r, c), (r + 4, c + 4)

        flipped = np.fliplr(b)
        window = sliding_window_view(flipped, (5, 5))
        diag = np.diagonal(window, axis1=2, axis2=3)
        mask = np.all(diag == piece, axis=2)
        if np.any(mask):
            r, c = np.argwhere(mask)[0]
            n = b.shape[1]
            return (r, n - 1 - c), (r + 4, n - 1 - (c + 4))

        return None

    def draw(self, screen):
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.board[r, c] == 1:
                    draw_x(screen, r, c)
                elif self.board[r, c] == 2:
                    draw_o(screen, r, c)

        draw_win_line(screen, self)

        if self.game_over:
            if self.winner:
                name = self.player1 if self.winner == 1 else self.player2
                msg = f"{name} wins! Press R / ESC"
            else:
                msg = "Draw! Press R / ESC"
        else:
            name = self.player1 if self.current_player == 1 else self.player2
            msg = f"Turn: {name}"

        surf = FONT.render(msg, True, WHITE)
        screen.blit(surf, (350, 20))

    def reset(self):
        self.__init__(self.player1, self.player2)

    def run(self, screen):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            screen.blit(self.bg, (0, 0))
            self.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if QUIT_RECT.collidepoint(mx, my):
                        return "QUIT", "QUIT"

                    cell = pixel_to_cell(mx, my)
                    if cell:
                        self.place(*cell)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()

                    if event.key == pygame.K_ESCAPE:
                        return "QUIT", "QUIT"

            pygame.display.update()