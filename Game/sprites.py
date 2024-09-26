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

x, y = (0, 0)

clock = pygame.time.Clock()

while not game_over: 
    dt = clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            x -= spriteWidth/2
            y -= spriteHeight/2
    pressed = pygame.key.get_pressed()
    if pressed[K_UP]:
        y -= 0.5 * dt
    if pressed[K_DOWN]:
        y += 0.5 * dt
    if pressed[K_LEFT]: 
        x -= 0.5 * dt
    if pressed[K_RIGHT]: 
        x += 0.5 * dt
    if pressed[K_SPACE]:
        x = 0
        y = 0
    
    if x > (screen.get_width() - spriteWidth):
        x = screen.get_width() - spriteWidth
    if y > (screen.get_height() - spriteHeight):
        y = screen.get_height() - spriteHeight
    if x < 0:
        x = 0
    if y < 0:
        y = 0
        
    screen.fill((0,0,0))
    screen.blit(player, (x, y))    
    pygame.display.update()
    
pygame.quit()