# character.py

import pygame
from utils import red, green

class Character:
    def __init__(self, x, y, name, max_hp, mana, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.mana = mana
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0 
        self.action = 0 #0: idle, 1: attack, 2: dano, 3: morto
        self.update_time = pygame.time.get_ticks()
        
        # Carrega as imagens da animação idle
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'./img/{self.name}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        
        self.animation_list.append(temp_list)

        # Carrega as imagens da animação de ataque
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'./img/{self.name}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Velocidade vertical inicial
        self.vel_y = 0  # Velocidade vertical para gravidade (inicialmente 0 para o buggy)
        self.vel_x = 0  # Velocidade horizontal
        self.jump = False  # Flag para verificar se o personagem está no ar

        # Se for o buggy, mantenha a velocidade vertical como 0
        if self.name == 'Buggy':
            self.vel_y = 0

    def apply_gravity(self, ground_level):
        gravity = 0.5  # A força da gravidade

        # Verifica se o personagem é o Player
        if self.name == 'Player':
            self.vel_y += gravity  # Aumenta a velocidade vertical com a gravidade
            self.rect.y += self.vel_y  # Atualiza a posição do player no eixo Y
            
            # Verifica se o player atingiu o solo
            if self.rect.bottom >= ground_level:
                self.rect.bottom = ground_level  # Mantém o player no solo
                self.vel_y = 0  # Reseta a velocidade vertical ao atingir o solo
                self.jump = False  # Permite que o player pule novamente
        else:  # Para o buggy
            # O buggy não deve ter gravidade; mantenha-o fixo acima do solo
            self.rect.bottom = ground_level - 30  # Mantém o buggy um pouco acima do solo

    def jump_action(self):
        if self.jump == False:  # Permite pular apenas se não estiver no ar
            self.vel_y = -10  # Dano do pulo
            self.jump = True  # Marca que o player está no ar

    def update(self):
        self.image = self.animation_list[self.action][self.frame_index]

        # Atualiza o tempo da animação
        if pygame.time.get_ticks() - self.update_time > 100:  # 100 ms por frame
            self.frame_index += 1  # Avança para o próximo frame
            self.update_time = pygame.time.get_ticks()  # Atualiza o tempo da animação

        if self.frame_index >= len(self.animation_list[self.action]):  # Reseta a animação se chegar ao fim
            self.frame_index = 0

    def move(self, move_left, move_right):
        if move_left and self.rect.x > 0:
            self.rect.x -= 5
        if move_right and self.rect.x < 800 - self.rect.width:
            self.rect.x += 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class HealthBar:
    def __init__(self, x, y, max_hp, color, bar_length=50):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.bar_length = bar_length  # Permite personalizar o tamanho da barra
        self.height = 5  # Altura da barra de vida
        self.color = color  # Cor da barra de vida

    def draw(self, surface, current_hp):
        ratio = current_hp / self.max_hp  # Proporção de HP restante
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.bar_length * ratio, self.height))  # Desenha a barra de vida
        # Adiciona bordas
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.bar_length, self.height), 2)  # Borda branca

