import pygame
from pygame.locals import * 

pygame.init()

screen = pygame.display.set_mode((800, 600), 0, 32)

player = pygame.image.load('Game\img\player.png') 
player = pygame.transform.scale(player, (100, 100))
spriteWidth = player.get_width()
spriteHeight = player.get_height()

pygame.display.set_caption('The Emptiness Machine')

screen.fill((0,0,0))

game_over = False

while not game_over: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    screen.blit(player, (screen.get_width() / 2 - spriteWidth / 2,
                           screen.get_height() / 2 - spriteHeight / 2))
    pygame.display.update()
pygame.quit()