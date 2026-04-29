import pygame
import sys
import numpy as np
from game import BaseGame
from numpy.lib.stride_tricks import sliding_window_view

# grid position and size (based on background image)
GRID_X = 287
GRID_Y = 147
GRID_SIZE = 320
GRID_N = 10  # 10x10 grid
CELL = GRID_SIZE // GRID_N  # size of each cell
PAD = CELL // 6  # small padding inside each cell

# colors used for drawing
WHITE = (255, 255, 255)
CYAN = (0, 220, 255)
PINK = (255, 60, 220)

# font for displaying text
FONT = pygame.font.SysFont("consolas", 16, bold=True)

# quit button area
QUIT_RECT = pygame.Rect(30, 20, 120, 60)


# gives top-left pixel of a given cell
def cell_origin(row, col):
    return (GRID_X + col * CELL, GRID_Y + row * CELL)


# converts mouse click position to grid cell index
def pixel_to_cell(px, py):
    if GRID_X <= px < GRID_X + GRID_SIZE and GRID_Y <= py < GRID_Y + GRID_SIZE:
        return (py - GRID_Y) // CELL, (px - GRID_X) // CELL
    return None


# draw X (player 1)
def draw_x(screen, row, col):
    cx, cy = cell_origin(row, col)
    pygame.draw.line(screen, CYAN, (cx + PAD, cy + PAD), (cx + CELL - PAD, cy + CELL - PAD), 2)
    pygame.draw.line(screen, CYAN, (cx + CELL - PAD, cy + PAD), (cx + PAD, cy + CELL - PAD), 2)


# draw O (player 2)
def draw_o(screen, row, col):
    cx, cy = cell_origin(row, col)
    center = (cx + CELL // 2, cy + CELL // 2)
    radius = (CELL // 2) - PAD
    pygame.draw.circle(screen, PINK, center, radius, 2)


# draws the line connecting winning cells
def draw_win_line(screen, game):
    # if no win, do nothing
    if not game.win_line:
        return

    (r1, c1), (r2, c2) = game.win_line

    # convert cell indices to pixel positions
    x1 = GRID_X + c1 * CELL + CELL // 2
    y1 = GRID_Y + r1 * CELL + CELL // 2
    x2 = GRID_X + c2 * CELL + CELL // 2
    y2 = GRID_Y + r2 * CELL + CELL // 2

    # color depends on which player won
    color = CYAN if game.winner == 1 else PINK
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 5)


class TicTacToe(BaseGame):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        # board initialized with 0 (empty)
        self.board = np.zeros((GRID_N, GRID_N), dtype=int)
        self.winner = None
        self.win_line = None

        # background image
        self.bg = pygame.image.load("games/bg_images/tictactoe.png")
        self.bg = pygame.transform.scale(self.bg, (1000, 700))

    # places a move on the board
    def place(self, row, col):
        # ignore if already filled or game is over
        if self.board[row, col] != 0 or self.game_over:
            return

        self.board[row, col] = self.current_player

        # check if this move causes a win
        win = self.check_win(self.current_player)

        if win:
            self.game_over = True
            self.winner = self.current_player
            self.win_line = win

        # check draw (no empty cells)
        elif np.all(self.board != 0):
            self.game_over = True

        else:
            # switch turn if game continues
            self.switch_turn()

    # checks for 5 in a row in all directions
    def check_win(self, piece):
        b = self.board

        # horizontal check
        window = sliding_window_view(b, (1, 5))
        mask = np.all(window == piece, axis=3)
        if np.any(mask):
            idx = np.argwhere(mask)[0]
            r, c = idx[0], idx[1]
            return (r, c), (r, c + 4)

        # vertical check
        window = sliding_window_view(b, (5, 1))
        mask = np.all(window == piece, axis=2)
        if np.any(mask):
            idx = np.argwhere(mask)[0]
            r, c = idx[0], idx[1]
            return (r, c), (r + 4, c)

        # diagonal (top-left to bottom-right)
        window = sliding_window_view(b, (5, 5))
        diag = np.diagonal(window, axis1=2, axis2=3)
        mask = np.all(diag == piece, axis=2)
        if np.any(mask):
            idx = np.argwhere(mask)[0]
            r, c = idx[0], idx[1]
            return (r, c), (r + 4, c + 4)

        # diagonal (top-right to bottom-left)
        flipped = np.fliplr(b)
        window = sliding_window_view(flipped, (5, 5))
        diag = np.diagonal(window, axis1=2, axis2=3)
        mask = np.all(diag == piece, axis=2)
        if np.any(mask):
            idx = np.argwhere(mask)[0]
            r, c = idx[0], idx[1]
            n = b.shape[1]
            return (r, n - 1 - c), (r + 4, n - 1 - (c + 4))

        return None

    # draws the board and UI
    def draw(self, screen):
        # draw all X and O
        for r in range(GRID_N):
            for c in range(GRID_N):
                if self.board[r, c] == 1:
                    draw_x(screen, r, c)
                elif self.board[r, c] == 2:
                    draw_o(screen, r, c)

        # draw winning line if exists
        draw_win_line(screen, self)

        # display message
        if self.game_over:
            if self.winner:
                name = self.player1 if self.winner == 1 else self.player2
                msg = f"{name} wins! Click to continue"
            else:
                msg = "Draw! Click to continue"
        else:
            name = self.player1 if self.current_player == 1 else self.player2
            msg = f"Turn: {name}"

        surf = FONT.render(msg, True, WHITE)
        screen.blit(surf, (350, 20))

    # resets the game
    def reset(self):
        self.__init__(self.player1, self.player2)

    # main game loop
    def run(self, screen):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            screen.blit(self.bg, (0, 0))
            self.draw(screen)

            for event in pygame.event.get():
                # if window closed
                if event.type == pygame.QUIT:
                    return None, None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    # quit button
                    if QUIT_RECT.collidepoint(mx, my):
                        return None, None

                    # if game over, return result
                    if self.game_over:
                        if self.winner == 1:
                            return self.player1, self.player2
                        elif self.winner == 2:
                            return self.player2, self.player1
                        else:
                            return "Draw", "Draw"

                    # place move if clicked inside grid
                    cell = pixel_to_cell(mx, my)
                    if cell:
                        self.place(*cell)

                # press R to reset game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()

            pygame.display.update()