# character.py

import pygame

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
            self.rect.bottom = ground_level - 30  # Mantém o buggy 30 pixels acima do solo
            self.vel_y = 0  # Reseta a velocidade vertical

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
    
    def update(self):
        animation_cooldown = 100
        # Atualiza a imagem e lida com a animação
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
            # Reinicia o índice de animação ao final
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                
        # Atualiza a imagem atual
        self.image = self.animation_list[self.action][self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Desenha a imagem na tela fornecida
