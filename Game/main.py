# main.py
import pygame
from core.game import Game
from ui.menu import Menu
from utils.settings import *

if __name__ == '__main__':
    pygame.init()
    # Inicializa a tela antes de criar o menu
    display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("The Emptiness Machine")
    
    menu = Menu()
    
    if menu.run():  # Se o jogador clicar em Start
        game = Game()
        game.run()
        
    pygame.quit()
