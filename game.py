import sys
import pygame
import random

from datetime import date
bg_color = (5,5,30)
white = (255,255,255)
light_blue = (200,200,255)
cyan = (0,220,255)
button_panel = (20,20,60)
button_hover = (40,40,100)

class BaseGame:
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.board = None
        self.running = True
        self.game_over = False
    def switch_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
    def check_win(self):
        pass
    def reset(self):
        pass 


def record_result(winner, loser, game_name):
    with open("history.csv", "a") as f:
        f.write(f"{winner}, {loser}, {date.today().isoformat()}, {game_name}\n")





def main():
    player1 = sys.argv[1]
    player2 = sys.argv[2]
    print(f"Welcome! {player1} and {player2}.")
    pygame.init()
    title_font = pygame.font.SysFont("Arial", 48)
    button_font = pygame.font.SysFont("Arial", 32)
    screen = pygame.display.set_mode((1000,700))
    pygame.display.set_caption("Mini Game Hub")
    clock = pygame.time.Clock()

    bg = pygame.image.load("mainmenu_final_1000x700.png")
#    connect4_img = pygame.image.load("connect4_button.png")

    connect4_rect  = pygame.Rect(349, 234, 302, 87)
    othello_rect   = pygame.Rect(349, 336, 398, 79)
    tictactoe_rect = pygame.Rect(352, 434, 388, 81)
    quit_rect = pygame.Rect(17,18,118,67)
    
    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if quit_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                if connect4_rect.collidepoint(mouse_x, mouse_y):
                    print("Connect4 selected.")
                    game = Connect4(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Connect-4")
                if tictactoe_rect.collidepoint(mouse_x, mouse_y):
                    print("Tic-Tac-Toe selected.")
#                    game = tictactoe(player1, player2)
#                    winner, loser = game.run(screen)
#                    record_result(winner, loser, "Connect-4")
                if othello_rect.collidepoint(mouse_x, mouse_y):
                    print("Othello selected.")
#                    game = othello(player1, player2)
#                    winner, loser = game.run(screen)
#                    record_result(winner, loser, "Connect-4")

        mouse_pos = pygame.mouse.get_pos()
        screen.blit(bg,(0,0))

        """
        if connect4_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, (x-10,210,connect4_width+20,52))
        else:
            pygame.draw.rect(screen, button_panel, (x-10,210,connect4_width+20,52))
        screen.blit(connect4_button, (x,220))
        
        tictactoe_width = tictactoe_button.get_width()
        x = (900 - tictactoe_width)//2
        tictactoe_rect = pygame.Rect(x-10,310,tictactoe_width+20,52)
        if tictactoe_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, (x-10,310,tictactoe_width+20,52))
        else:
            pygame.draw.rect(screen, button_panel, (x-10,310,tictactoe_width+20,52))
        screen.blit(tictactoe_button, (x,320))
        
        othello_width = othello_button.get_width()
        x = (900 - othello_width)//2
        othello_rect = pygame.Rect(x-10,410,othello_width+20,52)
        if othello_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover, (x-10,410,othello_width+20,52))
        else:
            pygame.draw.rect(screen, button_panel, (x-10,410,othello_width+20,52))
        screen.blit(othello_button, (x,420))
        """
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    from games.connect4 import Connect4
    main()





