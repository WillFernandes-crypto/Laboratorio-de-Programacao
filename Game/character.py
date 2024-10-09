# character.py
import pygame
import random
from utils import red, green

class Character:
    def __init__(self, x, y, name, max_hp, mana, potions, damage):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.mana = mana
        self.potions = potions
        self.alive = True
        self.damage = damage
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle, 1: attack, 2: dano, 3: morto
        self.update_time = pygame.time.get_ticks()
        
        # Ajuste do caminho com base no tipo de personagem
        if self.name == 'Player':
            base_path = './img/player'
        else:
            base_path = f'./img/mobs/{self.name}'

        # Carregar animações de idle
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'{base_path}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar animações de attack
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'{base_path}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False

        if self.name == 'Buggy':
            self.vel_y = 0

    def apply_gravity(self, ground_level):
        gravity = 0.5
        if self.name == 'Player':
            self.vel_y += gravity
            self.rect.y += self.vel_y
            if self.rect.bottom >= ground_level:
                self.rect.bottom = ground_level
                self.vel_y = 0
                self.jump = False
        else:
            self.rect.bottom = ground_level - 30

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def move(self, move_left, move_right):
        if move_left and self.rect.x > 0:
            self.rect.x -= 5
        if move_right and self.rect.x < 800 - self.rect.width:
            self.rect.x += 5

    def jump_action(self):
        if not self.jump:
            self.vel_y = -10
            self.jump = True

    def die(self):
        self.action = 3  # 3 representa a ação de "morto"
        self.frame_index = 0
        self.animation_list[3] = []
        for i in range(4):  # Supondo que haja 4 frames na animação de morte
            img = pygame.image.load(f'./img/player/died/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            self.animation_list[3].append(img)

    def update(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Se estiver morto, não faz mais nada
                self.frame_index = len(self.animation_list[self.action]) - 1  # Mantém o último frame de morte
            else:
                self.idle()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class HealthBar:
    def __init__(self, x, y, max_hp, color, bar_length=50):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.bar_length = bar_length
        self.height = 5
        self.color = color

    def draw(self, surface, current_hp):
        ratio = current_hp / self.max_hp
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.bar_length * ratio, self.height))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.bar_length, self.height), 2)
