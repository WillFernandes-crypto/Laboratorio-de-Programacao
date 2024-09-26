import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Define o título da janela
pygame.display.set_caption('The Emptiness Machine')

# Carregar o background
scenery = pygame.image.load(r'Game/img/scenery.png').convert_alpha()

def draw_bg():
    # Redimensiona o fundo para o tamanho da tela atual
    scaled_scenery = pygame.transform.scale(scenery, (screen.get_width(), screen.get_height()))
    screen.blit(scaled_scenery, (0, 0))

class Character:
    def __init__(self, x, y, name, max_hp, mana, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.mana = mana
        self.potions = potions
        self.alive = True
        img_player = self.image = pygame.image.load(f'Game/img/{self.name}.png')
        self.image = pygame.transform.scale(img_player, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)

player = Character(200, 260, 'Player', 30, 10, 3)
buggy = Character(550, 270, 'Buggy', 10, 0, 0)

mob_list = []
mob_list.append(buggy)
mob_list.append(buggy)

clock = pygame.time.Clock()

game_over = False
# Loop principal do jogo
while not game_over:
    dt = clock.tick(100)

    # Desenha o background
    draw_bg()

    # Desenha os personagens
    player.draw()
    for mobs in mob_list:
        buggy.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.VIDEORESIZE:
            # Atualiza a largura e altura da tela quando redimensionada
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Atualiza a tela
    pygame.display.update()

pygame.quit()
