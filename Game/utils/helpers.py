import pygame

# Definindo cores
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Função para desenhar o texto na tela
def draw_text(text, font, color, screen, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Função para desenhar o fundo
def draw_bg(screen, scenery):
    scaled_scenery = pygame.transform.scale(scenery, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_scenery, (0, 0))

# Função para carregar o fundo (cenário)
def load_background():
    return pygame.image.load(f'./img/scenery.png').convert_alpha()

