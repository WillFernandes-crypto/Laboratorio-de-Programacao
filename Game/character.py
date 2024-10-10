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
        self.action = 0  # 0: idle, 1: attack, 2: dano, 3: morto, 4: andar, 5: pular
        self.update_time = pygame.time.get_ticks()
        self.is_attacking = False  # Atributo para controlar se está atacando

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

        # Carregar animações de ataque
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'{base_path}/attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar animações de dano
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'{base_path}/damage/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar animações de morte
        temp_list = []
        for i in range(7): 
            img = pygame.image.load(f'{base_path}/dead/{i}.png')  # Corrigido para 'dead'
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        # Carregar animações de movimento (walk)
        temp_list = []
        for i in range(11):  # Supondo que haja 6 frames na animação de walk
            img = pygame.image.load(f'{base_path}/walk/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)  # Adicionando a animação de walk à lista (índice 4)

        # Carregar animações de pulo
        temp_list = []
        for i in range(14):  # Supondo que existam 14 frames de pulo (0.png até 13.png)
            img = pygame.image.load(f'{base_path}/jump/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 1.5, img.get_height() * 1.5))
            temp_list.append(img)
        self.animation_list.append(temp_list)  # Adiciona animação de pulo à lista (índice 5)

        self.facing_left = False  # Direção inicial do personagem
        self.damage_interval = 2000  # Intervalo de 2 segundos para causar dano
        self.damage_value = 10 if name == 'Buggy' else damage  # Dano inicial para o buggy é 10
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
        self.vel_x = 0
        self.jump = False
        self.is_dead = False

        # Criar hitbox menor e centralizada
        if self.name == 'Buggy':
            self.hitbox = pygame.Rect(self.rect.centerx - 8, self.rect.centery - 35, 20, 40)  # Hitbox do buggy
        elif self.name == 'Player':
            self.hitbox = pygame.Rect(self.rect.centerx - 45, self.rect.centery - 10, 40, 85)  # Hitbox do player
        else:
            self.hitbox = self.rect  # Outros personagens usam a hitbox normal

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

    def damage(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def die(self):
        self.action = 3  # Muda a ação para morte
        self.frame_index = 0  # Reinicia o índice do frame de morte
        self.update_time = pygame.time.get_ticks()

    def move(self, move_left, move_right):
        if move_left and self.rect.x > 0:
            self.rect.x -= 5
            self.facing_left = True
            if not self.jump:  # Altera para andar apenas se não estiver pulando
                self.action = 4  # Ação de movimento (walk) para a esquerda
        elif move_right and self.rect.x < 800 - self.rect.width:
            self.rect.x += 5
            self.facing_left = False
            if not self.jump:  # Altera para andar apenas se não estiver pulando
                self.action = 4  # Ação de movimento (walk) para a direita
        else:
            if self.action == 4:
                self.idle()  # Se o jogador parar de se mover, volta para o idle

    def jump_action(self):
        if not self.jump:
            self.vel_y = -10
            self.jump = True
            self.action = 5  # Altera a ação para pular
            self.frame_index = 0  # Reinicia o índice do frame de pulo
            self.update_time = pygame.time.get_ticks()  # Atualiza o tempo para animação


    def attack(self):
        self.action = 1  # Muda a ação para ataque
        self.frame_index = 0  # Reseta o índice do frame da animação de ataque
        self.update_time = pygame.time.get_ticks()

    def update(self):
        # Atualiza a posição da hitbox para seguir o personagem
        if self.name == 'Player':
            self.hitbox.x = self.rect.centerx - (self.hitbox.width // 2) - 5
            self.hitbox.y = self.rect.centery - (self.hitbox.height // 2) - 10
        else:
            self.hitbox.x = self.rect.centerx - (self.hitbox.width // 2)
            self.hitbox.y = self.rect.centery - (self.hitbox.height // 2)
 
        # Verifica se a ação atual é pulo e atualiza o frame
        if self.action == 5:  # Pulo
            if pygame.time.get_ticks() - self.update_time > 100:  # Tempo de troca de frame
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0  # Reseta para o início da animação de pulo
                # Não altera para idle, pois o personagem ainda está no ar

        # Espelhamento do sprite se estiver virado para a esquerda
        if self.facing_left:
            self.image = pygame.transform.flip(self.animation_list[self.action][self.frame_index], True, False)
        else:
            self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > 100:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:  # Se a ação for morte
                self.frame_index = len(self.animation_list[self.action]) - 1  # Mantém o último frame de morte
            else:
                self.idle()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
class HealthBar:
    def __init__(self, x, y, max_hp, color, bar_length=100, bar_height=10):
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.bar_length = bar_length
        self.bar_height = bar_height
        self.color = color

    def draw(self, surface, current_hp):
        ratio = current_hp / self.max_hp
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.bar_length * ratio, self.bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.bar_length, self.bar_height), 2)