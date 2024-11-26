import pygame
import os
from utils.settings import *
from utils.timer import Timer
from os.path import join
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, semi_collision_sprites, frames, data):
        # Setup geral
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        self.data = data
        
        # Imagem
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]

        # Rects
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-76, -36)
        self.old_rect = self.hitbox_rect.copy()

        # Movimentação
        self.direction = pygame.math.Vector2()
        self.speed = 200
        self.gravity = 1300
        self.jump = False
        self.jump_height = 800
        self.attacking = False

        # Colisões
        self.collision_sprites = collision_sprites
        self.semi_collision_sprites = semi_collision_sprites
        self.on_surface = {'floor': False, 'left': False, 'right': False}
        self.plataform = None

        # Timer
        self.timers = {
			'wall jump': Timer(400),
			'wall slide block': Timer(250),
			'platform skip': Timer(100),
			'attack block': Timer(500),
			'hit': Timer(400)
		}

        self.interacting = False

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()  # Pega o estado dos botões do mouse
        input_vector = pygame.math.Vector2(0, 0)
        
        if not self.timers['wall jump'].active:
            if keys[pygame.K_d]:
                input_vector.x += 1
                self.facing_right = True
            if keys[pygame.K_a]:
                input_vector.x -= 1
                self.facing_right = False
            self.direction.x = input_vector.normalize().x if input_vector.length() > 0 else 0
            if keys[pygame.K_s]:
                self.timers['platform skip'].activate()
            
            # Verifica se o botão esquerdo do mouse está pressionado
            if mouse_buttons[0]:  # 0 = botão esquerdo
                self.attack()
        
        if keys[pygame.K_w]:
            self.jump = True

        # Adiciona verificação da tecla E para interação
        if keys[pygame.K_e]:
            self.interacting = True
        else:
            self.interacting = False

    def attack(self):
        if not self.attacking and not self.timers['attack block'].active:
            self.attacking = True
            self.frame_index = 0
            self.timers['attack block'].activate()

    def move(self, delta_time):
        # Movimentação horizontal
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        # Movimentação vertical
        if not self.on_surface['floor'] and any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
            self.direction.y = 0
            self.hitbox_rect.y += self.gravity / 10 * delta_time
        else:
            self.direction.y += self.gravity * delta_time
            self.hitbox_rect.y += self.direction.y * delta_time

        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.timers['wall slide block'].activate()
                self.hitbox_rect.bottom -= 1
            elif any((self.on_surface['left'], self.on_surface['right'])) and not self.timers['wall slide block'].active:
                self.timers['wall jump'].activate()
                self.direction.y = -self.jump_height
                self.direction.x = 1 if self.on_surface['left'] else -1
            self.jump = False

        self.collision('vertical')
        self.semi_collision()
        self.rect.center = self.hitbox_rect.center

    def platform_move(self, delta_time):
        if self.plataform:
            self.hitbox_rect.topleft += self.plataform.direction * self.plataform.speed * delta_time

    def check_contact(self):
        floor_rect = pygame.Rect(self.hitbox_rect.bottomleft, (self.hitbox_rect.width, 2))
        right_rect = pygame.Rect(self.hitbox_rect.topright + pygame.math.Vector2(0, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        left_rect = pygame.Rect(self.hitbox_rect.topleft + pygame.math.Vector2(-2, self.hitbox_rect.height / 4), (2, self.hitbox_rect.height / 2))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        semi_collide_rect = [sprite.rect for sprite in self.semi_collision_sprites]

        # Colisões
        self.on_surface['floor'] = True if floor_rect.collidelist(collide_rects) >= 0 or floor_rect.collidelist(semi_collide_rect) >= 0 and self.direction.y >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(collide_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(collide_rects) >= 0 else False

        self.plataform = None
        sprites = self.collision_sprites.sprites() + self.semi_collision_sprites.sprites()
        for sprite in [sprite for sprite in sprites if hasattr(sprite, 'moving')]:
            if sprite.rect.colliderect(floor_rect):
                self.plataform = sprite

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if axis == 'horizontal':
                    # left
                    if self.hitbox_rect.left <= sprite.rect.right and int(self.old_rect.left) >= int(sprite.old_rect.right):
                        self.hitbox_rect.left = sprite.rect.right
                    # right
                    if self.hitbox_rect.right >= sprite.rect.left and int(self.old_rect.right) <= int(sprite.old_rect.left):
                        self.hitbox_rect.right = sprite.rect.left
                elif axis == 'vertical': # vertical
                    # top
                    if self.hitbox_rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.hitbox_rect.top = sprite.rect.bottom
                        if hasattr(sprite, 'moving'):
                            self.rect.top += 6
                    # bottom
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.hitbox_rect.bottom = sprite.rect.top
                    self.direction.y = 0

    def semi_collision(self):
        if not self.timers['platform skip'].active:
            for sprite in self.semi_collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if self.hitbox_rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = sprite.rect.top
                        if self.direction.y > 0:
                            self.direction.y = 0

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def animate(self, delta_time):
        self.frame_index += ANIMATION_SPEED * delta_time
        
        # Verifica se a animação de ataque terminou
        if self.state in ['attack', 'air_attack']:
            if self.frame_index >= len(self.frames[self.state]):
                self.attacking = False  # Reseta o estado de ataque
                self.frame_index = 0
                self.state = 'idle'
                return
        
        # Atualiza o frame atual
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)

    def get_state(self):
            if self.on_surface['floor']:
                if self.attacking:
                    self.state = 'attack'
                else:
                    self.state = 'idle' if self.direction.x == 0 else 'walk'
            else:
                if self.attacking:
                    self.state = 'air_attack'
                else:
                    if any((self.on_surface['left'], self.on_surface['right'])):
                        self.state = 'fall'
                    else:
                        self.state = 'jump' if self.direction.y < 0 else 'fall'

    def get_damage(self):
        if not self.timers['hit'].active:
            self.data.health -= 1
            self.timers['hit'].activate()

    def flicker(self):
        if self.timers['hit'].active and sin(pygame.time.get_ticks() * 100) >= 0:
            white_mask = pygame.mask.from_surface(self.image)
            white_surf = white_mask.to_surface()
            white_surf.set_colorkey('black')
            self.image = white_surf

    def update(self, delta_time):
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()

        self.platform_move(delta_time)  # Mover o player com a plataforma antes de mover o player
        self.input()
        self.move(delta_time)
        self.check_contact()

        self.get_state()
        self.animate(delta_time)
