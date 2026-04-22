import pygame
import sys
import numpy as np

GRID_X = 290
GRID_Y = 202
GRID_SIZE = 420
GRID_N = 10
CELL = GRID_SIZE // GRID_N
PAD = CELL // 6

WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
PINK = (255, 60, 220)

FONT = pygame.font.SysFont("consolas", 16, bold=True)

def cell_origin(row, col):
    return (GRID_X + col * CELL, GRID_Y + row * CELL)

def pixel_to_cell(px, py):
    if GRID_X <= px < GRID_X + GRID_SIZE and GRID_Y <= py < GRID_Y + GRID_SIZE:
        return (py - GRID_Y) // CELL, (px - GRID_X) // CELL
    return None

def draw_x(screen, row, col):
    cx, cy = cell_origin(row, col)
    pygame.draw.line(screen, CYAN, (cx + PAD, cy + PAD), (cx + CELL - PAD, cy + CELL - PAD), 2)
    pygame.draw.line(screen, CYAN, (cx + CELL - PAD, cy + PAD), (cx + PAD, cy + CELL - PAD), 2)

def draw_o(screen, row, col):
    cx, cy = cell_origin(row, col)
    center = (cx + CELL // 2, cy + CELL // 2)
    radius = (CELL // 2) - PAD
    pygame.draw.circle(screen, PINK, center, radius, 2)

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

class TicTacToe:
    def __init__(self, p1, p2):
        self.player1 = p1
        self.player2 = p2
        self.current_player = 1
        self.board = np.zeros((GRID_N, GRID_N), dtype=int)
        self.game_over = False
        self.winner = None
        self.win_line = None

        self.bg = pygame.image.load("games/bg_images/tictactoe.jpeg")
        self.bg = pygame.transform.scale(self.bg, (1000, 700))

    def place(self, row, col):
        if self.board[row][col] != 0 or self.game_over:
            return

        self.board[row][col] = self.current_player

        win = self.check_win(self.current_player)
        if win:
            self.game_over = True
            self.winner = self.current_player
            self.win_line = win
        elif np.all(self.board != 0):
            self.game_over = True
        else:
            self.current_player = 2 if self.current_player == 1 else 1

    def check_win(self, player):
        b, n = self.board, GRID_N

        for r in range(n):
            for c in range(n - 4):
                if np.all(b[r, c:c+5] == player):
                    return (r, c), (r, c+4)

        for r in range(n - 4):
            for c in range(n):
                if np.all(b[r:r+5, c] == player):
                    return (r, c), (r+4, c)

        for r in range(n - 4):
            for c in range(n - 4):
                if all(b[r+i][c+i] == player for i in range(5)):
                    return (r, c), (r+4, c+4)

        for r in range(n - 4):
            for c in range(4, n):
                if all(b[r+i][c-i] == player for i in range(5)):
                    return (r, c), (r+4, c-4)

        return None

    def draw(self, screen):
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.board[r][c] == 1:
                    draw_x(screen, r, c)
                elif self.board[r][c] == 2:
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
                    cell = pixel_to_cell(*pygame.mouse.get_pos())
                    if cell:
                        self.place(*cell)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    if event.key == pygame.K_ESCAPE:
                        if self.winner == 1:
                            return self.player1, self.player2
                        elif self.winner == 2:
                            return self.player2, self.player1
                        else:
                            return "Draw", "Draw"

            pygame.display.update()