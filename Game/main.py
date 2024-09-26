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
        self.vel_y = 0  # Velocidade vertical para gravidade
        self.vel_x = 0  # Velocidade horizontal
        self.jump = False  # Flag para verificar se o personagem está no ar

    def apply_gravity(self, ground_level):
        gravity = 0.5  # A força da gravidade
        self.vel_y += gravity  # Aumenta a velocidade vertical com a gravidade
        self.rect.y += self.vel_y  # Atualiza a posição do personagem no eixo Y
        
        # Verifica se o personagem atingiu o solo
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level  # Mantém o personagem no solo
            self.vel_y = 0  # Reseta a velocidade vertical ao atingir o solo
            self.jump = False  # Permite que o personagem pule novamente

    def move(self, move_left, move_right):
        move_speed = 5  # Velocidade de movimento
        if move_left:
            self.rect.x -= move_speed
        if move_right:
            self.rect.x += move_speed

    def jump_action(self):
        if not self.jump:  # Só permite pular se não estiver no ar
            self.vel_y = -10  # Velocidade do pulo
            self.jump = True

    def draw(self):
        screen.blit(self.image, self.rect)

player = Character(200, 260, 'Player', 30, 10, 3)
buggy = Character(550, 270, 'Buggy', 10, 0, 0)

mob_list = [buggy]

clock = pygame.time.Clock()

game_over = False
ground_level = screen_height - 50  # Define o nível do solo

# Loop principal do jogo
while not game_over:
    dt = clock.tick(100)

    # Desenha o background
    draw_bg()

    # Checa as teclas pressionadas
    keys = pygame.key.get_pressed()
    move_left = keys[pygame.K_a]  # Tecla 'A'
    move_right = keys[pygame.K_d]  # Tecla 'D'
    
    if keys[pygame.K_w]:  # Tecla 'W'
        player.jump_action()

    # Movimenta o player
    player.move(move_left, move_right)

    # Aplica gravidade ao player e desenha
    player.apply_gravity(ground_level)
    player.draw()

    for mob in mob_list:
        mob.apply_gravity(ground_level)
        mob.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.VIDEORESIZE:
            # Atualiza a largura e altura da tela quando redimensionada
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            ground_level = event.h - 50  # Atualiza o nível do solo com o redimensionamento da tela

    # Atualiza a tela
    pygame.display.update()

pygame.quit()
