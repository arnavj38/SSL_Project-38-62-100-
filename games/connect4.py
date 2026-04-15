import pygame 
import sys

import numpy as np
from game import BaseGame


blue = (30, 100, 200)
red = (220, 50, 50)
green = (50, 200, 100)
empty = (20, 20, 20)



class Connect4(BaseGame):
    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        self.board = np.zeros((7,7), dtype=int)
        self.rows = 7 
        self.cols = 7 
        self.cell_size = 100
        self.font = pygame.font.SysFont("monospace", 48)

    def draw_board(self,screen):
        pygame.draw.rect(screen,green,(0,0,100*self.rows,100*self.cols))
        for row in range(self.rows):
            for column in range(self.cols):
                center_x = column*self.cell_size + self.cell_size//2
                center_y = row*self.cell_size + self.cell_size//2
                if self.board[row, column] == 0:
                    pygame.draw.circle(screen,empty,(center_x,center_y),40)
                elif self.board[row, column] == 1:
                    pygame.draw.circle(screen,blue,(center_x,center_y),40)
                elif self.board[row, column] == 2:
                    pygame.draw.circle(screen,red,(center_x,center_y),40)
    def get_next_open_row(self,col):
        for row in range(6,-1,-1):
            if self.board[row, col] == 0:
                return row
        return -1

    def check_win(self,piece):
    
        window = np.lib.stride_tricks.sliding_window_view(self.board, (1,4))
        if (np.any(np.all(window == piece, axis=3))):
            return True
        
        window = np.lib.stride_tricks.sliding_window_view(self.board, (4, 1))
        if (np.any(np.all(window == piece, axis=2))):
            return True
        
        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(self.board, (4, 4)), axis1=2, axis2=3)
        if (np.any(np.all(window == piece, axis=2))):
            return True
        
        window = np.diagonal(np.lib.stride_tricks.sliding_window_view(np.fliplr(self.board), (4, 4)), axis1=2, axis2=3)
        if (np.any(np.all(window == piece, axis=2))):
            return True
        
        return False

    def run(self, screen):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        winner = self.current_player
                        loser = self.player2 if self.current_player == self.player1 else self.player1
                        return winner, loser
                    mouse_x, mouse_y = event.pos
                    column = mouse_x//self.cell_size
                    row = self.get_next_open_row(column)
                # if not np.any(board == 0):
                    if self.current_player == self.player1:
                        piece = 1
                    else:
                        piece = 2
                    if row != -1 and not self.game_over:
                        self.board[row, column] = piece
                        if self.check_win(piece):
                            print(f"Player {self.current_player} Wins!!")
                            self.game_over = True
                        else:
                            self.switch_turn()
            self.draw_board(screen)
            if self.game_over:
                text = self.font.render(f"Player {self.current_player} Wins!!!", True, (255,255,255))
                text_width = text.get_width()
                x = (700 - text_width)//2
                screen.blit(text, (x,20))
            pygame.display.flip()
            clock.tick(60)
            


