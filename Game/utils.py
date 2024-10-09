# utils.py
import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

def draw_text(text, font, color, screen, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bg(screen, scenery):
    scaled_scenery = pygame.transform.scale(scenery, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_scenery, (0, 0))

def load_background():
    return pygame.image.load(f'./img/scenery.png').convert_alpha()

def draw_panel(screen, player, font):
    # Desenha um painel retangular
    panel_img = pygame.Surface((200, 100))  # Exemplo: crie uma superfície para o painel
    panel_img.fill((0, 0, 0))  # Cor de fundo do painel
    screen.blit(panel_img, (0, 0))  # Desenha o painel na tela
    # Mostra os status do jogador
    draw_text(f'{player.name} HP: {player.hp}', font, red, screen, 10, 10)  # Corrigido para incluir a posição correta
    # for count, i in enumerate(buggy_list):
        # mostrar nome saúde dos buggys
        # draw_text(f'{i.name} HP: {i.hp}', font, red, screen)  # Corrigido para incluir a posição correta
