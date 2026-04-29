import sys
import pygame
import subprocess
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# basic UI colors
bg_color = (5,5,30)
white = (255,255,255)
light_blue = (200,200,255)
cyan = (0,220,255)
button_panel = (20,20,60)
button_hover = (40,40,100)

# graph colors
green_bar = (105,255,71)
red_bar = (255,76,76)
blue_bar = (71,200,255)
yellow = (255,233,78)
white_graph = (255,255,255)

# pie chart colors
pie_colors = [
    (232,54,93),
    (58,134,255),
    (131,56,236),
    (251,86,7),
    (6,214,160),
    (255,0,110)
]

class BaseGame:
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.current_player = 1
        self.board = None
        self.running = True
        self.game_over = False

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_win(self):
        pass

    def reset(self):
        pass


# save match result
def record_result(winner,loser,game_name):
    if winner is None:
        return
    with open("history.csv", "a") as f:
        f.write(f"{winner},{loser},{date.today().isoformat()},{game_name}\n")


# show sorting menu
def show_sort_menu(screen):
    clock = pygame.time.Clock()

    # load background
    sort_bg = pygame.image.load("games/bg_images/sortmetric_bg.png")
    sort_bg = pygame.transform.scale(sort_bg, (1000, 700))

    # load buttons
    wins_img = pygame.image.load("games/button_images/wins_button_transparent.png")
    losses_img = pygame.image.load("games/button_images/losses_button_transparent.png")
    ratio_img = pygame.image.load("games/button_images/wlratio_button_transparent.png")

    wins_img = pygame.transform.scale(wins_img, (300, 80))
    losses_img = pygame.transform.scale(losses_img, (300, 80))
    ratio_img = pygame.transform.scale(ratio_img, (300, 80))

    # button positions
    wins_rect = wins_img.get_rect(center=(500, 300))
    losses_rect = losses_img.get_rect(center=(500, 400))
    ratio_rect = ratio_img.get_rect(center=(500, 500))

    # hover effect size
    hover_size = (330, 90)

    wins_hover = pygame.transform.smoothscale(wins_img, hover_size)
    losses_hover = pygame.transform.smoothscale(losses_img, hover_size)
    ratio_hover = pygame.transform.smoothscale(ratio_img, hover_size)

    wins_hover_rect = wins_hover.get_rect(center=wins_rect.center)
    losses_hover_rect = losses_hover.get_rect(center=losses_rect.center)
    ratio_hover_rect = ratio_hover.get_rect(center=ratio_rect.center)

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:

                if wins_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh", "wins"])
                    generate_graphs("wins")
                    show_graphs(screen)
                    return

                if losses_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh", "losses"])
                    generate_graphs("losses")
                    show_graphs(screen)
                    return

                if ratio_rect.collidepoint(mouse_pos):
                    subprocess.run(["bash", "leaderboard.sh", "ratio"])
                    generate_graphs("ratio")
                    show_graphs(screen)
                    return

        # draw background
        screen.blit(sort_bg, (0, 0))

        # draw buttons with hover
        if wins_rect.collidepoint(mouse_pos):
            screen.blit(wins_hover, wins_hover_rect)
        else:
            screen.blit(wins_img, wins_rect)

        if losses_rect.collidepoint(mouse_pos):
            screen.blit(losses_hover, losses_hover_rect)
        else:
            screen.blit(losses_img, losses_rect)

        if ratio_rect.collidepoint(mouse_pos):
            screen.blit(ratio_hover, ratio_hover_rect)
        else:
            screen.blit(ratio_img, ratio_rect)

        pygame.display.flip()
        clock.tick(60)


# generate graphs using matplotlib
def generate_graphs(sort_by):
    import matplotlib.font_manager as fm

    fm.fontManager.addfont("PressStart2P-Regular.ttf")
    pixel_prop = fm.FontProperties(fname="PressStart2P-Regular.ttf")

    players, wins, losses, game_counts = [], [], [], {}

    # read history file
    with open("history.csv", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 4:
                continue

            winner, loser, _, game = parts

            if winner in ["", "None", "Draw"] or loser in ["", "None", "Draw"]:
                continue

            if winner not in players:
                players.append(winner)
                wins.append(0)
                losses.append(0)
            wins[players.index(winner)] += 1

            if loser not in players:
                players.append(loser)
                wins.append(0)
                losses.append(0)
            losses[players.index(loser)] += 1

            game_counts[game] = game_counts.get(game, 0) + 1

    # choose graph type
    if sort_by == "wins":
        values = wins
        title = "Wins Leaderboard"
        bar_color = green_bar

    elif sort_by == "losses":
        values = losses
        title = "Losses Leaderboard"
        bar_color = red_bar

    else:
        values = [round(wins[i] / losses[i], 2) if losses[i] else wins[i] for i in range(len(players))]
        title = "W/L Ratio Leaderboard"
        bar_color = blue_bar

    # bar graph
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    ax.bar(range(len(players)), values, color=bar_color, edgecolor=yellow)

    ax.set_xticks(range(len(players)))
    ax.set_xticklabels(players, rotation=25, fontproperties=pixel_prop, color=yellow)

    ax.tick_params(axis='y', colors=yellow)

    ax.set_title(title, color=yellow, fontproperties=pixel_prop)

    for i, v in enumerate(values):
        ax.text(i, v + 0.05, str(v), ha='center', color=yellow, fontproperties=pixel_prop)

    plt.savefig("bar_graph.png", transparent=True)
    plt.close()

    # pie graph
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0)

    wedges, texts, autotexts = ax.pie(
        list(game_counts.values()),
        labels=list(game_counts.keys()),
        autopct='%1.1f%%',
        colors=pie_colors[:len(game_counts)]
    )

    for t in texts:
        t.set_fontproperties(pixel_prop)

    for at in autotexts:
        at.set_fontproperties(pixel_prop)

    ax.set_title("Games Played Distribution", color=yellow, fontproperties=pixel_prop)

    plt.savefig("pie_graph.png", transparent=True)
    plt.close()


# show graphs on screen
def show_graphs(screen):
    clock = pygame.time.Clock()

    bg = pygame.transform.scale(pygame.image.load("games/bg_images/genbg_resized.jpeg"), (1000, 700))
    pie_img = pygame.transform.smoothscale(pygame.image.load("pie_graph.png"), (360, 330))
    bar_img = pygame.transform.smoothscale(pygame.image.load("bar_graph.png"), (520, 280))

    pie_rect = pie_img.get_rect(center=(500, 195))
    bar_rect = bar_img.get_rect(center=(500, 480))

    font = pygame.font.Font("PressStart2P-Regular.ttf", 11)

    running = True
    while running:
        screen.blit(bg, (0, 0))
        screen.blit(pie_img, pie_rect)
        screen.blit(bar_img, bar_rect)

        # footer text
        text1 = font.render("Leaderboard printed on terminal", True, light_blue)
        text2 = font.render("CLICK ANYWHERE TO RETURN", True, light_blue)

        screen.blit(text1, text1.get_rect(center=(500, 630)))
        screen.blit(text2, text2.get_rect(center=(500, 670)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()
        clock.tick(60)


# main menu
def main():
    player1 = sys.argv[1]
    player2 = sys.argv[2]

    pygame.init()
    screen = pygame.display.set_mode((1000,700))
    pygame.display.set_caption("Mini Game Hub")
    clock = pygame.time.Clock()

    # load images
    bg = pygame.image.load("games/bg_images/game_hub.png")
    connect4_img = pygame.transform.scale(pygame.image.load("games/button_images/connect4_button_cropped.png"), (302,87))
    tictactoe_img = pygame.transform.scale(pygame.image.load("games/button_images/tictactoe_button_transparent.png"), (302,87))
    othello_img = pygame.transform.scale(pygame.image.load("games/button_images/othello_button_transparent.png"), (302,87))

    quit_rect = pygame.Rect(17,18,118,67)

    # button positions
    connect4_rect = connect4_img.get_rect(center=(500, 280))
    tictactoe_rect = tictactoe_img.get_rect(center=(500, 480))
    othello_rect = othello_img.get_rect(center=(500, 380))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

                if connect4_rect.collidepoint(pygame.mouse.get_pos()):
                    game = Connect4(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Connect-4")
                    show_sort_menu(screen)

                if tictactoe_rect.collidepoint(pygame.mouse.get_pos()):
                    game = TicTacToe(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "TicTacToe")
                    show_sort_menu(screen)

                if othello_rect.collidepoint(pygame.mouse.get_pos()):
                    game = Othello(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Othello")
                    show_sort_menu(screen)

        screen.blit(bg,(0,0))
        screen.blit(connect4_img, connect4_rect)
        screen.blit(tictactoe_img, tictactoe_rect)
        screen.blit(othello_img, othello_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    from games.connect4 import Connect4
    from games.othello import Othello
    from games.tictactoe import TicTacToe

    main()