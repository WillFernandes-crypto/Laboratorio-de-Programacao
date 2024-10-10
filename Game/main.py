# main.py
import pygame
import sys
from character import Character, HealthBar
from utils import load_background, draw_bg, draw_text, red, green

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('The Emptiness Machine')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Times New Roman', 26)
scenery = load_background()

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        draw_text('THE EMPTINESS MACHINE', font, WHITE, screen, screen_width // 2 - 200, screen_height // 2 - 100)
        draw_text('Press [ENTER] to Start', font, WHITE, screen, screen_width // 2 - 150, screen_height // 2)
        draw_text('Press [ESC] to Quit', font, WHITE, screen, screen_width // 2 - 130, screen_height // 2 + 100)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game():
    attack_range = 70  # Aumentando a distância de ataque do jogador
    dead_mobs = []  # Lista para armazenar mobs mortos e suas animações

    global screen, screen_width, screen_height
    clock = pygame.time.Clock()

    ground_level = screen_height - 50
    player = Character(200, ground_level, 'Player', 100, 10, 3, 10)
    buggy = Character(550, ground_level - 30, 'Buggy', 30, 3, 3, 0)

    mob_list = [buggy]

    player_health_bar = HealthBar(10, 30, player.max_hp, red, bar_length=200)
    score = 0

    def check_game_over():
        if player.hp <= 0 and not player.is_dead:
            player.die()  # Chama o método de morte
            player.is_dead = True  # Marca o player como morto


    game_over = False
    mob_damage_timer = 0  # Controle de dano por segundo dos mobs
    attack_timer = 0  # Timer para ataques do player
    attack_interval = 1000  # Intervalo de ataque em milissegundos (1 segundo)

    while not game_over:
        dt = clock.tick(60)
        mob_damage_timer += dt
        attack_timer += dt  # Atualiza o timer de ataque

        draw_bg(screen, scenery)

        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]

        if keys[pygame.K_w]:
            player.jump_action()

        if keys[pygame.K_j] and attack_timer >= attack_interval:
            player.attack()  # Chama o método de ataque
            attack_timer = 0  # Reseta o timer de ataque

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and attack_timer >= attack_interval:
            player.attack()
            attack_timer = 0

        # Verifica se o jogador ainda está vivo
        if not player.is_dead:
            player.update()
            player.move(move_left, move_right)
            player.apply_gravity(ground_level)
            player.draw(screen)

            draw_text(f'{player.name} HP: {player.hp}', font, red, screen, 10, 5)
            player_health_bar.draw(screen, player.hp)

        else:
            # Se o jogador está morto, atualiza a animação de morte
            player.rect.y = ground_level - player.rect.height  # Ajuste a posição do player morto
            player.update()
            player.draw(screen)  # Desenha o personagem na animação de morte


        # Atualização e desenho dos mobs
        for mob in mob_list:
            mob.apply_gravity(ground_level)
            mob.update()
            mob.draw(screen)

            mob_health_bar = HealthBar(mob.rect.centerx - 25, mob.rect.top - 15, mob.max_hp, green, bar_length=50)
            if not mob.is_dead:
                mob_health_bar.draw(screen, mob.hp)

            # Lógica de dano e morte dos mobs permanece inalterada
            if mob.name == 'Buggy' and player.hitbox.colliderect(mob.hitbox) and mob_damage_timer >= mob.damage_interval and mob.hp > 0:
                player.hp = max(player.hp - mob.damage_value, 0)
                mob_damage_timer = 0

            if player.action == 1 and abs(player.hitbox.centerx - mob.hitbox.centerx) <= attack_range:
                mob.hp = max(mob.hp - player.damage, 0)

            if mob.hp <= 0 and not mob.is_dead:
                mob.action = 3
                mob.is_dead = True
                score += 10
                mob.frame_index = 0
                mob.update_time = pygame.time.get_ticks()

            # Atualiza a animação dos mobs mortos
            for dead_mob in dead_mobs[:]:
                dead_mob.draw(screen)
                if pygame.time.get_ticks() - dead_mob.update_time > 1000:
                    dead_mobs.remove(dead_mob)

        pygame.draw.rect(screen, red, player.hitbox, 2)

        draw_text(f'Score: {score}', font, WHITE, screen, screen_width - 200, 20)

        check_game_over()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                ground_level = screen_height - 50

        pygame.display.update()

main_menu()
game()
pygame.quit()