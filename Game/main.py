import pygame
import sys
from character import Character
from utils import load_background, draw_bg, draw_text  # Removido set_screen

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

# Carregar a fonte
font = pygame.font.Font(None, 50)

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
    global screen  # Declara screen como global
    player = Character(200, 260, 'Player', 30, 10, 3)
    buggy = Character(550, 270, 'Buggy', 10, 0, 0)

    mob_list = [buggy]
    clock = pygame.time.Clock()
    ground_level = screen_height - 50  # Define o nível do solo

    score = 0  # Inicializa a pontuação do jogador

    # Função para o ataque do jogador
    def player_attack():
        nonlocal score
        for mob in mob_list:
            if player.rect.colliderect(mob.rect):  # Se o jogador colidir com o mob
                mob.hp -= 5  # Dano ao mob
                if mob.hp <= 0:
                    mob_list.remove(mob)  # Remove o mob quando ele é derrotado
                    score += 10  # Aumenta a pontuação ao derrotar um mob

    # Loop principal do jogo
    game_over = False
    while not game_over:
        dt = clock.tick(100)

        # Desenha o background
        draw_bg(screen, scenery)  # Adicione a variável screen aqui

        # Checa as teclas pressionadas
        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_a]  # Tecla 'A'
        move_right = keys[pygame.K_d]  # Tecla 'D'
        
        if keys[pygame.K_w]:  # Tecla 'W'
            player.jump_action()

        # Verifica ataques (tecla J)
        if keys[pygame.K_j]:
            player_attack()

        # Verifica cliques do mouse para ataque
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Botão esquerdo do mouse
            player_attack()

        # Movimenta o player
        player.move(move_left, move_right)

        # Aplica gravidade ao player e desenha
        player.apply_gravity(ground_level)
        player.draw(screen)  # Passe a variável screen aqui

        # Desenha os mobs
        for mob in mob_list:
            mob.apply_gravity(ground_level)
            mob.draw(screen)  # Passe a variável screen aqui

        # Exibe a pontuação no canto superior direito
        draw_text(f'Score: {score}', font, WHITE, screen, screen_width - 200, 20)  # Passe a variável screen aqui
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                # Atualiza a largura e altura da tela quando redimensionada
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                ground_level = event.h - 50  # Atualiza o nível do solo com o redimensionamento da tela

        # Atualiza a tela
        pygame.display.update()

# Inicia o jogo com o menu principal
main_menu()
game()

pygame.quit()
