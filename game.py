import sys
import pygame
import subprocess   # ✅ ADDED
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


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


def record_result(winner,loser,game_name):
    if winner is None:
        return
    with open("history.csv", "a") as f:
        f.write(f"{winner},{loser},{date.today().isoformat()},{game_name}\n")


# ─────────────────────────────────────────────
# ✅ ADDED: SORT MENU
# ─────────────────────────────────────────────

import subprocess
import pygame

def show_sort_menu(screen):
    import pygame
    import subprocess

    clock = pygame.time.Clock()

    # Background
    sort_bg = pygame.image.load("sortmetric_bg.png")
    sort_bg = pygame.transform.scale(sort_bg, (1000, 700))

    # Buttons
    wins_img = pygame.image.load("wins_button_transparent.png")
    losses_img = pygame.image.load("losses_button_transparent.png")
    ratio_img = pygame.image.load("wlratio_button_transparent.png")

    wins_img = pygame.transform.scale(wins_img, (300, 80))
    losses_img = pygame.transform.scale(losses_img, (300, 80))
    ratio_img = pygame.transform.scale(ratio_img, (300, 80))

    wins_rect = wins_img.get_rect(center=(500, 300))
    losses_rect = losses_img.get_rect(center=(500, 400))
    ratio_rect = ratio_img.get_rect(center=(500, 500))

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

        screen.blit(sort_bg, (0, 0))

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


def generate_graphs(sort_by):
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm

    fm.fontManager.addfont("PressStart2P-Regular.ttf")
    pixel_prop = fm.FontProperties(fname="PressStart2P-Regular.ttf")

    players, wins, losses, game_counts = [], [], [], {}

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

            game = game.strip()
            game_counts[game] = game_counts.get(game, 0) + 1

    if sort_by == "wins":
        values, title, bar_color = wins, "Wins Leaderboard", "#69FF47"
    elif sort_by == "losses":
        values, title, bar_color = losses, "Losses Leaderboard", "#FF4C4C"
    else:
        values = [round(wins[i] / losses[i], 2) if losses[i] else wins[i] for i in range(len(players))]
        title, bar_color = "W/L Ratio Leaderboard", "#47C8FF"

    YELLOW = "#FFE94E"
    WHITE  = "#FFFFFF"

    # ── BAR GRAPH ───────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    ax.bar(range(len(players)), values, color=bar_color, edgecolor=YELLOW, linewidth=1.2)

    ax.set_xticks(range(len(players)))
    ax.set_xticklabels(players, rotation=25, fontsize=24, color=YELLOW, fontproperties=pixel_prop)

    ax.tick_params(axis='y', labelsize=22, colors=YELLOW)
    for lbl in ax.get_yticklabels():
        lbl.set_fontproperties(pixel_prop)

    ax.set_title(title, fontsize=60, color=YELLOW, pad=20, fontproperties=pixel_prop)  # bigger title

    ax.spines[:].set_color(YELLOW)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color=YELLOW)

    for i, v in enumerate(values):
        ax.text(i, v + 0.05, str(v), ha='center', fontsize=22, color=YELLOW, fontproperties=pixel_prop)

    plt.savefig("bar_graph.png", dpi=200, transparent=True, bbox_inches='tight')
    plt.close()

    # ── PIE GRAPH ───────────────────────────────────────────────
    wedge_colors = ["#E8365D", "#3A86FF", "#8338EC", "#FB5607", "#06D6A0", "#FF006E"]

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))

    wedges, texts, autotexts = ax.pie(
        list(game_counts.values()),
        labels=list(game_counts.keys()),
        autopct='%1.1f%%',
        startangle=140,
        colors=wedge_colors[:len(game_counts)],
        wedgeprops={'edgecolor': YELLOW, 'linewidth': 1.8},
        textprops={'color': WHITE}
    )

    for t in texts:
        t.set_fontproperties(pixel_prop)
        t.set_fontsize(21)

    for at in autotexts:
        at.set_fontproperties(pixel_prop)
        at.set_fontsize(19)

    ax.set_title("Games Played Distribution", fontsize=60, color=YELLOW, pad=20, fontproperties=pixel_prop)  # bigger title

    plt.tight_layout()
    plt.savefig("pie_graph.png", dpi=200, transparent=True)
    plt.close()


def show_graphs(screen):
    import pygame

    clock = pygame.time.Clock()

    bg = pygame.transform.scale(pygame.image.load("genbg_resized.jpeg"), (1000, 700))
    pie_img = pygame.transform.smoothscale(pygame.image.load("pie_graph.png"), (360, 330))
    bar_img = pygame.transform.smoothscale(pygame.image.load("bar_graph.png"), (520, 280))

    pie_rect = pie_img.get_rect(center=(500, 195))
    bar_rect = bar_img.get_rect(center=(500, 480))

    pie_bg = pygame.Surface((pie_rect.width + 20, pie_rect.height + 20), pygame.SRCALPHA)
    pie_bg.fill((0, 0, 0, 180))
    pie_bg_rect = pie_bg.get_rect(center=pie_rect.center)

    bar_bg = pygame.Surface((bar_rect.width + 20, bar_rect.height + 20), pygame.SRCALPHA)
    bar_bg.fill((0, 0, 0, 180))
    bar_bg_rect = bar_bg.get_rect(center=bar_rect.center)

    font = pygame.font.Font("PressStart2P-Regular.ttf", 11)
    FOOTER_COLOR = (176, 176, 255)

    running = True
    while running:
        screen.blit(bg, (0, 0))

        screen.blit(pie_bg, pie_bg_rect)
        screen.blit(pie_img, pie_rect)

        screen.blit(bar_bg, bar_bg_rect)
        screen.blit(bar_img, bar_rect)

        for i, text in enumerate(["Leaderboard printed on terminal", "CLICK ANYWHERE TO RETURN"]):
            surf = font.render(text, True, FOOTER_COLOR)
            screen.blit(surf, surf.get_rect(center=(500, 630 + i * 40)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.update()
        clock.tick(60)

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
    tictactoe_hover_rect = tictactoe_hover_img.get_rect(center=tictactoe_rect.center)
    othello_hover_img = pygame.transform.smoothscale(othello_img, hover_size)
    othello_hover_rect = othello_hover_img.get_rect(center=othello_rect.center)
    
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
                    show_sort_menu(screen)   # ✅ ADDED

                if tictactoe_rect.collidepoint(mouse_x, mouse_y):
                    print("Tic-Tac-Toe selected.")
                    game = TicTacToe(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "TicTacToe")
                    show_sort_menu(screen)   # ✅ ADDED

                if othello_rect.collidepoint(mouse_x, mouse_y):
                    print("Othello selected.")
                    game = Othello(player1, player2)
                    winner, loser = game.run(screen)
                    record_result(winner, loser, "Othello")
                    show_sort_menu(screen)   # ✅ ADDED


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
    from games.othello import Othello
    from games.tictactoe import TicTacToe

    main()