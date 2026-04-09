import pygame
import numpy as np
import sys
import os

pygame.init()

# ── Window ──
WIDTH, HEIGHT = 600, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# ── Grid ──
GRID_SIZE = 480
GRID_N = 8
CELL = GRID_SIZE // GRID_N
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = 100

# ── Colors ──
GREEN = (0, 120, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)

BG_PATH = os.path.join("othello.png")
BG_IMAGE = pygame.image.load(BG_PATH)
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH,HEIGHT))


FONT = pygame.font.SysFont("consolas", 22, bold=True)

# ── Directions (8 directions) ──
DIRS = [(-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1), (1,0),  (1,1)]


# ── Base Class ──
class BoardGame:
    def __init__(self, p1, p2, size):
        self.player1 = p1
        self.player2 = p2
        self.current_player = 1
        self.board = np.zeros((size, size), dtype=int)

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1


# ── Othello Class ──
class Othello(BoardGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2, GRID_N)
        self.init_board()
        self.game_over = False

    def init_board(self):
        mid = GRID_N // 2
        self.board[mid-1][mid-1] = 2
        self.board[mid][mid]     = 2
        self.board[mid-1][mid]   = 1
        self.board[mid][mid-1]   = 1

    def inside(self, r, c):
        return 0 <= r < GRID_N and 0 <= c < GRID_N

    def valid_moves(self, player):
        moves = []
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.board[r][c] == 0 and self.can_flip(r, c, player):
                    moves.append((r, c))
        return moves

    def can_flip(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            found_opponent = False

            while self.inside(nr, nc) and self.board[nr][nc] == opponent:
                nr += dr
                nc += dc
                found_opponent = True

            if found_opponent and self.inside(nr, nc) and self.board[nr][nc] == player:
                return True

        return False

    def flip_discs(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            path = []
            nr, nc = r + dr, c + dc

            while self.inside(nr, nc) and self.board[nr][nc] == opponent:
                path.append((nr, nc))
                nr += dr
                nc += dc

            if self.inside(nr, nc) and self.board[nr][nc] == player:
                for pr, pc in path:
                    self.board[pr][pc] = player

    def place(self, r, c):
        if (r, c) not in self.valid_moves(self.current_player):
            return

        self.board[r][c] = self.current_player
        self.flip_discs(r, c, self.current_player)

        self.switch_turn()

        # Skip turn if no moves
        if not self.valid_moves(self.current_player):
            self.switch_turn()

            if not self.valid_moves(self.current_player):
                self.game_over = True

    def score(self):
        p1 = np.sum(self.board == 1)
        p2 = np.sum(self.board == 2)
        return p1, p2


# ── Drawing ──
def draw_board(game):
    WIN.blit(BG_IMAGE, (0, 0))

    # Grid
    for i in range(GRID_N + 1):
        pygame.draw.line(WIN, BLACK,
            (GRID_X, GRID_Y + i*CELL),
            (GRID_X + GRID_SIZE, GRID_Y + i*CELL), 2)

        pygame.draw.line(WIN, BLACK,
            (GRID_X + i*CELL, GRID_Y),
            (GRID_X + i*CELL, GRID_Y + GRID_SIZE), 2)

    # Discs
    for r in range(GRID_N):
        for c in range(GRID_N):
            if game.board[r][c] != 0:
                color = BLACK if game.board[r][c] == 1 else WHITE
                cx = GRID_X + c*CELL + CELL//2
                cy = GRID_Y + r*CELL + CELL//2
                pygame.draw.circle(WIN, color, (cx, cy), CELL//2 - 5)

    # Highlight valid moves
    for r, c in game.valid_moves(game.current_player):
        cx = GRID_X + c*CELL + CELL//2
        cy = GRID_Y + r*CELL + CELL//2
        pygame.draw.circle(WIN, GRAY, (cx, cy), 5)


def draw_status(game):
    p1, p2 = game.score()

    left_text  = f"{game.player1}: {p1}"
    right_text = f"{game.player2}: {p2}"

    left_surf  = FONT.render(left_text, True, (0,255,255))
    right_surf = FONT.render(right_text, True, (0,255,255))

    left_x  = 50
    right_x = WIDTH - right_surf.get_width() - 50
    y = 30

    # --- BLACK DISC (Player 1) ---


    WIN.blit(left_surf, (left_x, y))

    # --- WHITE DISC (Player 2) ---
    wx = right_x + right_surf.get_width() + 25
    wy = y + 12
    WIN.blit(right_surf, (right_x, y))

    # --- UNDERLINE CURRENT PLAYER ---
    if game.current_player == 1:
        # underline left (black)
        pygame.draw.line(WIN, (0,255,255),
            (left_x, y + left_surf.get_height() + 5),
            (left_x + left_surf.get_width(), y + left_surf.get_height() + 5), 3)

    else:
        # underline right (white)
        pygame.draw.line(WIN, (0,255,255),
            (right_x, y + right_surf.get_height() + 5),
            (right_x + right_surf.get_width(), y + right_surf.get_height() + 5), 3)
    


# ── Helpers ──
def pixel_to_cell(px, py):
    if GRID_X <= px < GRID_X + GRID_SIZE and GRID_Y <= py < GRID_Y + GRID_SIZE:
        return (py - GRID_Y)//CELL, (px - GRID_X)//CELL
    return None


# ── Run Game ──
def run_game(player1="Player 1", player2="Player 2"):
    game = Othello(player1, player2)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        draw_board(game)
        draw_status(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                cell = pixel_to_cell(*event.pos)
                if cell and not game.game_over:
                    game.place(*cell)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game = Othello(player1, player2)

        pygame.display.update()
if __name__ == "__main__":
    run_game()
