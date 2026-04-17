import pygame
import sys
import os
import numpy as np

pygame.init()

# ── Window (matches background image exactly) ──
WIDTH, HEIGHT = 589, 413
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("10x10 Tic Tac Toe")

# background image
IMG_PATH   = os.path.join("games/bg_images/tictactoe.png")

BG = pygame.image.load(IMG_PATH).convert()

# ── Grid constants (measured from image pixels) ──
GRID_X    = 171   # left edge of grid
GRID_Y    = 119   # top  edge of grid
GRID_SIZE = 250   # 250 x 250 px perfect square
GRID_N    = 10    # 10 x 10 cells
CELL      = 25    # 25 px per cell exactly
PAD       = 4     # padding inside each cell before drawing mark

# ── Colours (just 3) ──
WHITE  = (255, 255, 255)   # UI text
CYAN   = (0,   220, 255)   # X colour
PINK   = (255,  60, 220)   # O colour

# ── Font ──
FONT = pygame.font.SysFont("consolas", 16, bold=True)


# ── Cell helpers ──
def cell_origin(row, col):
    return (GRID_X + col * CELL, GRID_Y + row * CELL)

def pixel_to_cell(px, py):
    if GRID_X <= px < GRID_X + GRID_SIZE and GRID_Y <= py < GRID_Y + GRID_SIZE:
        return (py - GRID_Y) // CELL, (px - GRID_X) // CELL
    return None


# ── Draw X ──
def draw_x(row, col):
    cx, cy = cell_origin(row, col)
    x1, y1 = cx + PAD,        cy + PAD
    x2, y2 = cx + CELL - PAD, cy + CELL - PAD
    pygame.draw.line(WIN, CYAN, (x1, y1), (x2, y2), 2)
    pygame.draw.line(WIN, CYAN, (x2, y1), (x1, y2), 2)

# ── Draw O ──
def draw_o(row, col):
    cx, cy = cell_origin(row, col)
    center = (cx + CELL // 2, cy + CELL // 2)
    pygame.draw.circle(WIN, PINK, center, CELL // 2 - PAD, 2)


# ── Base class ──
class BoardGame:
    def __init__(self, player1, player2, size):
        self.player1        = player1
        self.player2        = player2
        self.current_player = 1
        self.board          = np.zeros((size, size), dtype=int)

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1


# ── TicTacToe (5-in-a-row) ──
class TicTacToe(BoardGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, GRID_N)
        self.game_over = False
        self.winner    = None

    def place(self, row, col):
        if self.board[row][col] != 0 or self.game_over:
            return
        self.board[row][col] = self.current_player
        if self.check_win(self.current_player):
            self.game_over = True
            self.winner    = self.current_player
        elif np.all(self.board != 0):
            self.game_over = True          # draw
        else:
            self.switch_turn()

    def check_win(self, player):
        b, n = self.board, GRID_N
        for r in range(n):                 # horizontal
            for c in range(n - 4):
                if np.all(b[r, c:c+5] == player): return True
        for r in range(n - 4):            # vertical
            for c in range(n):
                if np.all(b[r:r+5, c] == player): return True
        for r in range(n - 4):            # diagonal ↘
            for c in range(n - 4):
                if all(b[r+i][c+i] == player for i in range(5)): return True
        for r in range(n - 4):            # diagonal ↙
            for c in range(4, n):
                if all(b[r+i][c-i] == player for i in range(5)): return True
        return False

    def reset(self):
        self.board          = np.zeros((GRID_N, GRID_N), dtype=int)
        self.game_over      = False
        self.winner         = None
        self.current_player = 1


# ── Draw all marks ──
def draw_marks(game):
    for r in range(GRID_N):
        for c in range(GRID_N):
            if game.board[r][c] == 1:
                draw_x(r, c)
            elif game.board[r][c] == 2:
                draw_o(r, c)


# ── Draw top status bar ──
def draw_status(game):
    # one clean horizontal line of text centred at top of window
    if game.game_over:
        if game.winner:
            name = game.player1 if game.winner == 1 else game.player2
            col  = CYAN        if game.winner == 1 else PINK
            msg  = f"{name} wins!   Press R to restart"
        else:
            msg = "Draw!   Press R to restart"
            col = WHITE
    else:
        name = game.player1 if game.current_player == 1 else game.player2
        col  = CYAN        if game.current_player == 1 else PINK
        msg  = f"Current turn:  {name}"

    surf = FONT.render(msg, True, col)
    x    = (WIDTH - surf.get_width()) // 2   # horizontally centred
    WIN.blit(surf, (x, 10))                  # y=10: sits cleanly above the grid


# ── Main loop ──
def run_game(player1="Player 1", player2="Player 2"):
    game  = TicTacToe(player1, player2)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        WIN.blit(BG, (0, 0))
        draw_marks(game)
        draw_status(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = pixel_to_cell(*pygame.mouse.get_pos())
                if cell:
                    game.place(*cell)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game.reset()

        pygame.display.update()


if __name__ == "__main__":
    run_game()
