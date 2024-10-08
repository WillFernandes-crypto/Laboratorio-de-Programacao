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
        self.update_time = pygame.time.get_ticks()
        
        # Carrega as imagens da animação
        for i in range(9):
            img = pygame.image.load(f'./img/{self.name}/walk/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            self.animation_list.append(img)
        
        self.image = self.animation_list[self.frame_index]
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
    
    def update(self):
        animation_cooldown = 100
        # Atualiza a imagem e lida com a animação
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
            # Reinicia o índice de animação ao final
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                
        # Atualiza a imagem atual
        self.image = self.animation_list[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)  # Desenha a imagem na tela fornecida
