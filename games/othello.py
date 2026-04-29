import pygame
import numpy as np
import sys
from game import BaseGame

pygame.init()

# ── WINDOW ──
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# ── GRID ──
GRID_SIZE = 328
GRID_N = 8
CELL = GRID_SIZE // GRID_N
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = 144

# ── COLORS ──
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)
GOLD = (218, 165, 32)
RED = (255, 0, 0)

# QUIT button
QUIT_RECT = pygame.Rect(30, 20, 120, 60)

BG_IMAGE = pygame.image.load("games/bg_images/othello.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("consolas", 22, bold=True)

DIRS = [(-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1), (1,0),  (1,1)]


class Othello(BaseGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        self.board = np.zeros((GRID_N, GRID_N), dtype=int)
        self.game_over = False
        self.winner_name = None

        self.init_board()

    def init_board(self):
        mid = GRID_N // 2
        self.board[mid-1, mid-1] = 2
        self.board[mid,   mid]   = 2
        self.board[mid-1, mid]   = 1
        self.board[mid,   mid-1] = 1

    def inside(self, r, c):
        return 0 <= r < GRID_N and 0 <= c < GRID_N

    def valid_moves(self, player):
        empty = np.argwhere(self.board == 0)
        moves = []

        for r, c in empty:
            if self.can_flip(r, c, player):
                moves.append((r, c))

        return moves

    def can_flip(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            found_opponent = False

            while self.inside(nr, nc) and self.board[nr, nc] == opponent:
                nr += dr
                nc += dc
                found_opponent = True

            if found_opponent and self.inside(nr, nc) and self.board[nr, nc] == player:
                return True

        return False

    def flip_discs(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            path = []
            nr, nc = r + dr, c + dc

            while self.inside(nr, nc) and self.board[nr, nc] == opponent:
                path.append((nr, nc))
                nr += dr
                nc += dc

            if self.inside(nr, nc) and self.board[nr, nc] == player:
                for pr, pc in path:
                    self.board[pr, pc] = player

    def place(self, r, c):
        if (r, c) not in self.valid_moves(self.current_player):
            return

        self.board[r, c] = self.current_player
        self.flip_discs(r, c, self.current_player)

        self.switch_turn()

        if not self.valid_moves(self.current_player):
            self.switch_turn()

            if not self.valid_moves(self.current_player):
                self.game_over = True
                self.winner_name = self.check_win()

    def check_win(self):
        if not self.game_over:
            return None

        counts = np.bincount(self.board.flatten(), minlength=3)
        p1, p2 = counts[1], counts[2]

        if p1 > p2:
            return self.player1
        elif p2 > p1:
            return self.player2
        else:
            return "Draw"

    def run(self, screen):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            draw_board(self)
            draw_status(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if QUIT_RECT.collidepoint(mx, my):
                        return "QUIT", "QUIT"

                    cell = pixel_to_cell(mx, my)
                    if cell and not self.game_over:
                        self.place(*cell)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.player1, self.player2)

                    if event.key == pygame.K_ESCAPE:
                        return "QUIT", "QUIT"

            pygame.display.update()


def draw_board(game):
    WIN.blit(BG_IMAGE, (0, 0))

    for r in range(GRID_N):
        for c in range(GRID_N):
            if game.board[r, c] != 0:
                color = BLACK if game.board[r, c] == 1 else WHITE
                cx = GRID_X + c*CELL + CELL//2
                cy = GRID_Y + r*CELL + CELL//2
                pygame.draw.circle(WIN, color, (cx, cy), CELL//2 - 5)

    for r, c in game.valid_moves(game.current_player):
        cx = GRID_X + c*CELL + CELL//2
        cy = GRID_Y + r*CELL + CELL//2
        pygame.draw.circle(WIN, GRAY, (cx, cy), 5)


def draw_status(game):
    counts = np.bincount(game.board.flatten(), minlength=3)
    black_count, white_count = counts[1], counts[2]

    # positions above grid
    TOP_Y = GRID_Y - 60
    LEFT_X = GRID_X + 40
    RIGHT_X = GRID_X + GRID_SIZE - 40

    label_font = pygame.font.SysFont("consolas", 16, bold=True)
    score_font = pygame.font.SysFont("verdana", 40, bold=True)

    # BLACK (left)
    black_label = label_font.render(f"{game.player1} (BLACK)", True, GOLD)
    black_score = score_font.render(str(black_count).zfill(2), True, GOLD)

    WIN.blit(black_label, black_label.get_rect(center=(LEFT_X, TOP_Y)))
    WIN.blit(black_score, black_score.get_rect(center=(LEFT_X, TOP_Y + 30)))

    # WHITE (right)
    white_label = label_font.render(f"{game.player2} (WHITE)", True, GOLD)
    white_score = score_font.render(str(white_count).zfill(2), True, GOLD)

    WIN.blit(white_label, white_label.get_rect(center=(RIGHT_X, TOP_Y)))
    WIN.blit(white_score, white_score.get_rect(center=(RIGHT_X, TOP_Y + 30)))

    # GAME OVER TEXT
    if game.game_over:
        if game.winner_name == "Draw":
            msg = "DRAW!"
        else:
            msg = f"{game.winner_name} WINS!"

        over_surf = FONT.render(msg + " (R / ESC)", True, (255, 0, 0))
        WIN.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, 20))


def pixel_to_cell(x, y):
    if GRID_X <= x <= GRID_X + GRID_SIZE and GRID_Y <= y <= GRID_Y + GRID_SIZE:
        c = (x - GRID_X) // CELL
        r = (y - GRID_Y) // CELL
        return int(r), int(c)
    return None