import pygame

def get_user_input():
    keys = pygame.key.get_pressed()
    moving_left = keys[pygame.K_a]
    moving_right = keys[pygame.K_d]
    jump = keys[pygame.K_w]
    attack = pygame.mouse.get_pressed()[0]  # Botão esquerdo do mouse
    return moving_left, moving_right, jump, attack
