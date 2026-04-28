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


def record_result(winner,loser,game_name):
    with open("history.csv", "a") as f:
        f.write(f"{winner},{loser},{date.today().isoformat()},{game_name}\n")





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

    bg = pygame.image.load("game_hub.png")
    connect4_img = pygame.image.load("connect4_button_cropped.png")
    connect4_img = pygame.transform.scale(connect4_img, (302, 87))
    tictactoe_img = pygame.image.load("tictactoe_button_transparent.png")
    tictactoe_img = pygame.transform.scale(tictactoe_img, (302, 87))
    othello_img = pygame.image.load("othello_button_transparent.png")
    othello_img = pygame.transform.scale(othello_img, (302, 87))



    quit_rect = pygame.Rect(17,18,118,67)

    
    connect4_rect = connect4_img.get_rect(center=(349 + 302//2, 234 + 87//2))
    tictactoe_rect = tictactoe_img.get_rect(center=(349 + 302//2, 434 + 87//2))
    othello_rect = othello_img.get_rect(center=(349 + 302//2, 336 + 87//2))
    
    hover_size = (int(connect4_rect.width * 1.1), int(connect4_rect.height * 1.1))
    connect4_hover_img = pygame.transform.smoothscale(connect4_img, hover_size)
    connect4_hover_rect = connect4_hover_img.get_rect(center=connect4_rect.center)
    tictactoe_hover_img = pygame.transform.smoothscale(tictactoe_img, hover_size)
    tictactoe_hover_rect = connect4_hover_img.get_rect(center=tictactoe_rect.center)
    othello_hover_img = pygame.transform.smoothscale(othello_img, hover_size)
    othello_hover_rect = connect4_hover_img.get_rect(center=othello_rect.center)
    
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
                    winner,loser = game.run(screen)
                    record_result(winner,loser,"Connect-4")
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
        screen.blit(bg,(0,0))
        mouse_pos = pygame.mouse.get_pos()
        if connect4_rect.collidepoint(mouse_pos):
            screen.blit(connect4_hover_img, connect4_hover_rect)
            
        else:
            screen.blit(connect4_img, connect4_rect)
            
        if tictactoe_rect.collidepoint(mouse_pos):
            screen.blit(tictactoe_hover_img, tictactoe_hover_rect)
            
        else:
            screen.blit(tictactoe_img, tictactoe_rect)
            
        if othello_rect.collidepoint(mouse_pos):
            screen.blit(othello_hover_img, othello_hover_rect)
            
        else:
            screen.blit(othello_img, othello_rect)
            
        pygame.display.flip()
        clock.tick(60)



if __name__ == "__main__":
    from games.connect4 import Connect4
    main()





