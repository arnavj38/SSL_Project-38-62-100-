import sys
import pygame
import random
from datetime import date

# IMPORT YOUR GAMES
from games.othello import Othello   # ✅ ADD THIS

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

    # SAME SCREEN WILL BE REUSED
    screen = pygame.display.set_mode((1000,700))   # ✅ match othello
    pygame.display.set_caption("Mini Game Hub")

    clock = pygame.time.Clock()

    title = title_font.render("Mini Game Hub", True, cyan)
    connect4_button = button_font.render("Connect-4", True, white)
    tictactoe_button = button_font.render("Tic-Tac-Toe", True, white)
    othello_button = button_font.render("Othello", True, white)

    connect4_rect = None
    tictactoe_rect = None
    othello_rect = None
    
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # ── CONNECT 4 ──
                if connect4_rect.collidepoint(mouse_x, mouse_y):
                    game = Connect4(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Connect-4")

                # ── TIC TAC TOE (not implemented yet) ──
                if tictactoe_rect.collidepoint(mouse_x, mouse_y):
                    print("Tic-Tac-Toe selected.")

                # ── OTHELLO ──
                if othello_rect.collidepoint(mouse_x, mouse_y):
                    print("Othello selected.")
                    game = Othello(player1, player2)
                    winner, loser = game.run(screen)   # ✅ SAME SCREEN
                    record_result(winner, loser, "Othello")

        mouse_pos = pygame.mouse.get_pos()

        # ── BACKGROUND ──
        screen.fill(bg_color)

        # stars
        stars = [(random.randint(0,1000), random.randint(0,700)) for _ in range(150)]
        for star in stars:
            pygame.draw.circle(screen, light_blue, star, 1)
        
        # ── TITLE ──
        title_width = title.get_width()
        x = (1000 - title_width)//2
        screen.blit(title, (x,80))
        
        # ── CONNECT4 BUTTON ──
        connect4_width = connect4_button.get_width()
        x = (1000 - connect4_width)//2
        connect4_rect = pygame.Rect(x-10,210,connect4_width+20,52)

        pygame.draw.rect(
            screen,
            button_hover if connect4_rect.collidepoint(mouse_pos) else button_panel,
            connect4_rect
        )
        screen.blit(connect4_button, (x,220))
        
        # ── TIC TAC TOE BUTTON ──
        tictactoe_width = tictactoe_button.get_width()
        x = (1000 - tictactoe_width)//2
        tictactoe_rect = pygame.Rect(x-10,310,tictactoe_width+20,52)

        pygame.draw.rect(
            screen,
            button_hover if tictactoe_rect.collidepoint(mouse_pos) else button_panel,
            tictactoe_rect
        )
        screen.blit(tictactoe_button, (x,320))
        
        # ── OTHELLO BUTTON ──
        othello_width = othello_button.get_width()
        x = (1000 - othello_width)//2
        othello_rect = pygame.Rect(x-10,410,othello_width+20,52)

        pygame.draw.rect(
            screen,
            button_hover if othello_rect.collidepoint(mouse_pos) else button_panel,
            othello_rect
        )
        screen.blit(othello_button, (x,420))
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()


