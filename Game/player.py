import pygame

pygame.init()

screen = pygame.display.set_mode((640, 488), 0, 32)

pygame.display.set_caption('The Emptiness Machine')

screen.fill((0,0,0))

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
pygame.quit()