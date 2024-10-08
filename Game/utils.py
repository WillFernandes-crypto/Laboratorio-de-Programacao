# utils.py

import pygame

def draw_text(text, font, color, screen, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bg(screen, scenery):
    scaled_scenery = pygame.transform.scale(scenery, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_scenery, (0, 0))

def load_background():
    return pygame.image.load(f'./img/scenery.png').convert_alpha()

