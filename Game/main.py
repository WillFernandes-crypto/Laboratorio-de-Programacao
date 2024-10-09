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
    global screen, screen_width, screen_height
    clock = pygame.time.Clock()

    ground_level = screen_height - 50
    player = Character(200, ground_level, 'Player', 100, 10, 3, 10)
    buggy = Character(550, ground_level - 30, 'Buggy', 30, 3, 3, 0)

    mob_list = [buggy]

    player_health_bar = HealthBar(10, 30, player.max_hp, red, bar_length=200)
    score = 0

    def player_attack():
        nonlocal score
        for mob in mob_list:
            if player.rect.colliderect(mob.rect):
                mob.hp = max(mob.hp - player.damage, 0)  # Evitar HP abaixo de 0
                if mob.hp == 0:
                    mob_list.remove(mob)
                    score += 10

    def check_game_over():
        if player.hp <= 0:
            player.die()

    game_over = False
    mob_damage_timer = 0  # Controle de dano por segundo dos mobs
    while not game_over:
        dt = clock.tick(60)
        mob_damage_timer += dt

        draw_bg(screen, scenery)

        keys = pygame.key.get_pressed()
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]

        if keys[pygame.K_w]:
            player.jump_action()

        if keys[pygame.K_j]:
            player_attack()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            player_attack()

        player.update()
        player.move(move_left, move_right)
        player.apply_gravity(ground_level)
        player.draw(screen)

        draw_text(f'{player.name} HP: {player.hp}', font, red, screen, 10, 5)
        player_health_bar.draw(screen, player.hp)

        for mob in mob_list:
            mob.apply_gravity(ground_level)
            mob.update()
            mob.draw(screen)

            mob_health_bar = HealthBar(mob.rect.centerx - 25, mob.rect.top - 15, mob.max_hp, green, bar_length=50)
            mob_health_bar.draw(screen, mob.hp)

            # Controla o tempo para o mob causar dano
            if mob.name == 'Buggy' and player.rect.colliderect(mob.rect) and mob_damage_timer >= 2000:  # 2 segundos
                player.hp = max(player.hp - 1, 0)  # Evitar HP abaixo de 0
                mob_damage_timer = 0  # Reseta o timer de dano

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

