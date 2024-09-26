import pygame

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

    def draw(self, screen):  # Modificado para aceitar 'screen' como argumento
        screen.blit(self.image, self.rect)  # Desenha a imagem na tela fornecida
