import pygame
import numpy as np
import sys
from game import BaseGame

pygame.init()

# window size and setup
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# grid settings
GRID_SIZE = 328
GRID_N = 8  # 8x8 board
CELL = GRID_SIZE // GRID_N  # size of each cell
GRID_X = (WIDTH - GRID_SIZE) // 2  # center horizontally
GRID_Y = 144  # vertical position

# colors used
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)
GOLD = (218, 165, 32)
RED = (255, 0, 0)

# quit button area
QUIT_RECT = pygame.Rect(30, 20, 120, 60)

# background image
BG_IMAGE = pygame.image.load("games/bg_images/othello.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH, HEIGHT))

# font for text
FONT = pygame.font.SysFont("consolas", 22, bold=True)

# all 8 directions to check flipping
DIRS = [(-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1), (1,0),  (1,1)]


class Othello(BaseGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        # board: 0 empty, 1 black, 2 white
        self.board = np.zeros((GRID_N, GRID_N), dtype=int)
        self.game_over = False
        self.winner_name = None

        # initialize starting pieces
        self.init_board()

    # set the starting 4 discs in center
    def init_board(self):
        mid = GRID_N // 2
        self.board[mid-1, mid-1] = 2
        self.board[mid,   mid]   = 2
        self.board[mid-1, mid]   = 1
        self.board[mid,   mid-1] = 1

    # check if a position is inside board
    def inside(self, r, c):
        return 0 <= r < GRID_N and 0 <= c < GRID_N

    # get all valid moves for a player
    def valid_moves(self, player):
        empty = np.argwhere(self.board == 0)
        moves = []

        # check every empty cell
        for r, c in empty:
            if self.can_flip(r, c, player):
                moves.append((r, c))

        return moves

    # check if placing at (r,c) flips any discs
    def can_flip(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            found_opponent = False

            # move in direction while seeing opponent discs
            while self.inside(nr, nc) and self.board[nr, nc] == opponent:
                nr += dr
                nc += dc
                found_opponent = True

            # valid if opponent discs end with player's disc
            if found_opponent and self.inside(nr, nc) and self.board[nr, nc] == player:
                return True

        return False

    # flip opponent discs after placing move
    def flip_discs(self, r, c, player):
        opponent = 2 if player == 1 else 1

        for dr, dc in DIRS:
            path = []
            nr, nc = r + dr, c + dc

            # store opponent discs in this direction
            while self.inside(nr, nc) and self.board[nr, nc] == opponent:
                path.append((nr, nc))
                nr += dr
                nc += dc

            # if path ends with player's disc, flip them
            if self.inside(nr, nc) and self.board[nr, nc] == player:
                for pr, pc in path:
                    self.board[pr, pc] = player

    # place a move
    def place(self, r, c):
        # ignore invalid move
        if (r, c) not in self.valid_moves(self.current_player):
            return

        self.board[r, c] = self.current_player
        self.flip_discs(r, c, self.current_player)

        # switch turn
        self.switch_turn()

        # if next player has no moves, switch back
        if not self.valid_moves(self.current_player):
            self.switch_turn()

            # if both players have no moves, game ends
            if not self.valid_moves(self.current_player):
                self.game_over = True
                self.winner_name = self.check_win()

    # decide winner based on disc count
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

    # main game loop
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

                    # quit button
                    if QUIT_RECT.collidepoint(mx, my):
                        return "None", "None"

                    # place move if valid
                    cell = pixel_to_cell(mx, my)
                    if cell and not self.game_over:
                        self.place(*cell)

                if event.type == pygame.KEYDOWN:
                    # reset game
                    if event.key == pygame.K_r:
                        self.__init__(self.player1, self.player2)

                    # exit game
                    if event.key == pygame.K_ESCAPE:
                        return "None", "None"

            pygame.display.update()


# draw board and pieces
def draw_board(game):
    WIN.blit(BG_IMAGE, (0, 0))

    for r in range(GRID_N):
        for c in range(GRID_N):
            if game.board[r, c] != 0:
                color = BLACK if game.board[r, c] == 1 else WHITE
                cx = GRID_X + c*CELL + CELL//2
                cy = GRID_Y + r*CELL + CELL//2
                pygame.draw.circle(WIN, color, (cx, cy), CELL//2 - 5)

    # show possible moves
    for r, c in game.valid_moves(game.current_player):
        cx = GRID_X + c*CELL + CELL//2
        cy = GRID_Y + r*CELL + CELL//2
        pygame.draw.circle(WIN, GRAY, (cx, cy), 5)


# draw score and status
def draw_status(game):
    counts = np.bincount(game.board.flatten(), minlength=3)
    black_count, white_count = counts[1], counts[2]

    TOP_Y = GRID_Y - 60
    LEFT_X = GRID_X + 40
    RIGHT_X = GRID_X + GRID_SIZE - 40

    label_font = pygame.font.SysFont("consolas", 16, bold=True)
    score_font = pygame.font.SysFont("verdana", 40, bold=True)

    # player1 (black)
    black_label = label_font.render(f"{game.player1} (BLACK)", True, GOLD)
    black_score = score_font.render(str(black_count).zfill(2), True, GOLD)

    WIN.blit(black_label, black_label.get_rect(center=(LEFT_X, TOP_Y)))
    WIN.blit(black_score, black_score.get_rect(center=(LEFT_X, TOP_Y + 30)))

    # player2 (white)
    white_label = label_font.render(f"{game.player2} (WHITE)", True, GOLD)
    white_score = score_font.render(str(white_count).zfill(2), True, GOLD)

    WIN.blit(white_label, white_label.get_rect(center=(RIGHT_X, TOP_Y)))
    WIN.blit(white_score, white_score.get_rect(center=(RIGHT_X, TOP_Y + 30)))

    # game over message
    if game.game_over:
        if game.winner_name == "Draw":
            msg = "DRAW!"
        else:
            msg = f"{game.winner_name} WINS!"

        over_surf = FONT.render(msg + " (R / ESC)", True, (255, 0, 0))
        WIN.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, 20))


# convert mouse position to grid cell
def pixel_to_cell(x, y):
    if GRID_X <= x <= GRID_X + GRID_SIZE and GRID_Y <= y <= GRID_Y + GRID_SIZE:
        c = (x - GRID_X) // CELL
        r = (y - GRID_Y) // CELL
        return int(r), int(c)
    return None