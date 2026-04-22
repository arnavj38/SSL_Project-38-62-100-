import sys
import pygame
import random
from datetime import date

from games.othello import Othello
from games.tictactoe import TicTacToe

bg_color = (5,5,30)
white = (255,255,255)
light_blue = (200,200,255)
cyan = (0,220,255)
button_panel = (20,20,60)
button_hover = (40,40,100)

def record_result(winner, loser, game_name):
    with open("history.csv", "a") as f:
        f.write(f"{winner}, {loser}, {date.today().isoformat()}, {game_name}\n")

def main():
    player1 = sys.argv[1]
    player2 = sys.argv[2]

    pygame.init()
    title_font = pygame.font.SysFont("Arial", 48)
    button_font = pygame.font.SysFont("Arial", 32)

    screen = pygame.display.set_mode((1000,700))
    pygame.display.set_caption("Mini Game Hub")

    clock = pygame.time.Clock()

    title = title_font.render("Mini Game Hub", True, cyan)
    connect4_button = button_font.render("Connect-4", True, white)
    tictactoe_button = button_font.render("Tic-Tac-Toe", True, white)
    othello_button = button_font.render("Othello", True, white)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(bg_color)

        
        for _ in range(150):
            pygame.draw.circle(screen, light_blue, (random.randint(0,1000), random.randint(0,700)), 1)

        screen.blit(title, ((1000 - title.get_width())//2, 80))

        
        def draw_button(text_surf, y):
            x = (1000 - text_surf.get_width())//2
            rect = pygame.Rect(x-10, y, text_surf.get_width()+20, 52)
            pygame.draw.rect(
                screen,
                button_hover if rect.collidepoint(mouse_pos) else button_panel,
                rect
            )
            screen.blit(text_surf, (x, y+10))
            return rect

        connect4_rect = draw_button(connect4_button, 210)
        tictactoe_rect = draw_button(tictactoe_button, 310)
        othello_rect = draw_button(othello_button, 410)

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if tictactoe_rect.collidepoint(x, y):
                    game = TicTacToe(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "TicTacToe")

                if othello_rect.collidepoint(x, y):
                    game = Othello(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Othello")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()