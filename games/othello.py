import pygame
import numpy as np
import sys
import os
from game import BaseGame

pygame.init()


WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")


GRID_SIZE = 578
GRID_N = 8
CELL = GRID_SIZE // GRID_N
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = 72


GREEN = (0, 120, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (180, 180, 180)

BG_IMAGE = pygame.image.load("games/bg_images/othello.png")
BG_IMAGE = pygame.transform.scale(BG_IMAGE, (WIDTH,HEIGHT))


FONT = pygame.font.SysFont("consolas", 22, bold=True)


DIRS = [(-1,-1), (-1,0), (-1,1),
        (0,-1),         (0,1),
        (1,-1), (1,0),  (1,1)]


'''
class BoardGame:
    def __init__(self, p1, p2, size):
        self.player1 = p1
        self.player2 = p2
        
        self.board = np.zeros((GRID_N, GRID_N), dtype=int)

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1
'''

# ── Othello Class ──
class Othello(BaseGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        self.board = np.zeros((GRID_N,GRID_N), dtype=int)
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
                    cell = pixel_to_cell(*event.pos)
                    if cell and not self.game_over:
                        self.place(*cell)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.player1, self.player2)

            if self.game_over:
                p1, p2 = self.score()
                if p1 > p2:
                    return self.player1, self.player2
                elif p2 > p1:
                    return self.player2, self.player1
                else:
                    return "Draw", "Draw"

            pygame.display.update()


def draw_board(game):
    WIN.blit(BG_IMAGE, (0, 0))

    
    for i in range(GRID_N + 1):
        pygame.draw.line(WIN, BLACK,
            (GRID_X, GRID_Y + i*CELL),
            (GRID_X + GRID_SIZE, GRID_Y + i*CELL), 2)

        pygame.draw.line(WIN, BLACK,
            (GRID_X + i*CELL, GRID_Y),
            (GRID_X + i*CELL, GRID_Y + GRID_SIZE), 2)

    
    for r in range(GRID_N):
        for c in range(GRID_N):
            if game.board[r][c] != 0:
                color = BLACK if game.board[r][c] == 1 else WHITE
                cx = GRID_X + c*CELL + CELL//2
                cy = GRID_Y + r*CELL + CELL//2
                pygame.draw.circle(WIN, color, (cx, cy), CELL//2 - 5)

   
    for r, c in game.valid_moves(game.current_player):
        cx = GRID_X + c*CELL + CELL//2
        cy = GRID_Y + r*CELL + CELL//2
        pygame.draw.circle(WIN, GRAY, (cx, cy), 5)

def draw_status(game):
   
    p1_count, p2_count = game.score()
    
  
    P1_POS = (105, 430) 
    P2_POS = (884, 430)
    
 
    score_font = pygame.font.SysFont("verdana", 50, bold=True)
    GOLD = (218, 165, 32) # Matches the UI borders
    
    # 4. Render and Center
    p1_surf = score_font.render(str(p1_count).zfill(2), True, GOLD)
    p2_surf = score_font.render(str(p2_count).zfill(2), True, GOLD)
    
    p1_rect = p1_surf.get_rect(center=P1_POS)
    p2_rect = p2_surf.get_rect(center=P2_POS)
    
    
    WIN.blit(p1_surf, p1_rect)
    WIN.blit(p2_surf, p2_rect)
    
    
    if game.game_over:
        msg = "GAME OVER!" if p1_count != p2_count else "DRAW!"
        over_surf = FONT.render(msg, True, (255, 0, 0))
        WIN.blit(over_surf, (WIDTH//2 - over_surf.get_width()//2, 10))
    
def pixel_to_cell(x, y):
    if GRID_X <= x <= GRID_X + GRID_SIZE and GRID_Y <= y <= GRID_Y + GRID_SIZE:
        c = (x - GRID_X) // CELL
        r = (y - GRID_Y) // CELL
        return int(r), int(c)
    return None


