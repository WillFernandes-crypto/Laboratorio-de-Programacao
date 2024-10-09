# main.py
import pygame
import sys
from character import Character, HealthBar  # Adiciona HealthBar
from utils import load_background, draw_bg, draw_text, draw_panel, red, green

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Define o título da janela
pygame.display.set_caption('The Emptiness Machine')

# Define cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carregar a fonte após a inicialização do Pygame
font = pygame.font.SysFont('Times New Roman', 26)

# Carregar o background
scenery = load_background()

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text('THE EMPTINESS MACHINE', font, WHITE, screen, screen_width // 2 - 200, screen_height // 2 - 100)
        draw_text('Press [ENTER] to Start', font, WHITE, screen, screen_width // 2 - 150, screen_height // 2)
        draw_text('Press [ESC] to Quit', font, WHITE, screen, screen_width // 2 - 130, screen_height // 2 + 100)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tecla Enter
                    menu_running = False  # Sai do menu e inicia o jogo
                if event.key == pygame.K_ESCAPE:  # Tecla Esc
                    pygame.quit()
                    sys.exit()  # Fecha o jogo

def game():
    global screen
    clock = pygame.time.Clock()

    ground_level = screen_height - 50
    player = Character(200, ground_level, 'Player', 100, 10, 3)
    buggy = Character(550, ground_level - 30, 'Buggy', 30, 10, 3)

    buggy_list = [buggy]

    # Barra de vida do player (vermelha) - Aumentada
    player_health_bar = HealthBar(10, 30, player.max_hp, red, bar_length=200)

    score = 0

    def player_attack():
        nonlocal score
        for buggy in buggy_list:
            if player.rect.colliderect(buggy.rect):
                buggy.hp -= 5
                if buggy.hp <= 0:
                    buggy_list.remove(buggy)
                    score += 10

    game_over = False
    while not game_over:
        dt = clock.tick(60)

        # Desenha o background
        draw_bg(screen, scenery)

        # Checa as teclas pressionadas
        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        
        if keys[pygame.K_w]:
            player.jump_action()

        if keys[pygame.K_j]:
            player_attack()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            player_attack()

        player.update()
        player.move(move_left, move_right)
        player.apply_gravity(ground_level)
        player.draw(screen)

        # Atualiza o HP do player para testar
        #player.hp = 90

        # Desenha o texto e a barra de vida do player
        draw_text(f'{player.name} HP: {player.hp}', font, red, screen, 10, 5)
        player_health_bar.draw(screen, player.hp)

        # Desenha os buggys e suas barras de vida
        for buggy in buggy_list:
            buggy.apply_gravity(ground_level)
            buggy.update()
            buggy.draw(screen)

            # Barra de vida do buggy menor
            buggy_health_bar = HealthBar(buggy.rect.centerx - 25, buggy.rect.top - 15, buggy.max_hp, green, bar_length=50)
            buggy_health_bar.draw(screen, buggy.hp)

        # Exibe a pontuação
        draw_text(f'Score: {score}', font, WHITE, screen, screen_width - 200, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ground_level = event.h - 50

        pygame.display.update()

# Inicia o jogo com o menu principal
main_menu()
game()

pygame.quit()
