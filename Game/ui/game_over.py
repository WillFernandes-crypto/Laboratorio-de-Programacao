import pygame
import os
from utils.settings import *
from ui.menu import Botao  # Reaproveitando a classe Botao

class GameOver:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        
        # Carrega e configura os elementos visuais
        self.carregar_imagens()
        self.criar_botoes()
        self.criar_titulo()
        
    def criar_titulo(self):
        self.fonte = pygame.font.Font(os.path.join('assets', 'fonts', 'pixellari.ttf'), 80)
        self.titulo = self.fonte.render("Game Over", True, (255, 0, 0))
        self.titulo_rect = self.titulo.get_rect(center=(SCREEN_WIDTH // 2, 100))
        
    def carregar_imagens(self):
        # Carrega botões
        retry_img = pygame.image.load(os.path.join('assets', 'buttons', 'new_game.png')).convert_alpha()
        exit_img = pygame.image.load(os.path.join('assets', 'buttons', 'exit.png')).convert_alpha()
        
        # Redimensiona botões
        novo_tamanho = (int(retry_img.get_width() * 0.6), int(retry_img.get_height() * 0.6))
        self.retry_img = pygame.transform.scale(retry_img, novo_tamanho)
        self.exit_img = pygame.transform.scale(exit_img, novo_tamanho)
        
    def criar_botoes(self):
        self.retry_button = Botao(SCREEN_WIDTH // 2 - self.retry_img.get_width() // 2, 300, self.retry_img)
        self.exit_button = Botao(SCREEN_WIDTH // 2 - self.exit_img.get_width() // 2, 450, self.exit_img)
        
    def reposicionar_elementos(self):
        largura_tela = self.display_surface.get_width()
        altura_tela = self.display_surface.get_height()
        
        # Posiciona o título
        self.titulo_rect = self.titulo.get_rect(center=(largura_tela // 2, altura_tela * 0.2))
        
        # Posiciona os botões
        self.retry_button.rect.centerx = largura_tela // 2
        self.retry_button.rect.centery = altura_tela * 0.5
        
        self.exit_button.rect.centerx = largura_tela // 2
        self.exit_button.rect.centery = altura_tela * 0.7
        
    def run(self):
        while True:
            self.clock.tick(60)
            self.display_surface.fill((0, 0, 0))  # Fundo preto
            
            # Desenha elementos
            self.display_surface.blit(self.titulo, self.titulo_rect)
            
            # Verifica interações com botões
            if self.retry_button.desenhar(self.display_surface):
                return True  # Reiniciar jogo
                
            if self.exit_button.desenhar(self.display_surface):
                return False  # Sair do jogo
            
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                elif evento.type == pygame.VIDEORESIZE:
                    self.display_surface = pygame.display.set_mode((evento.w, evento.h), pygame.RESIZABLE)
                    self.reposicionar_elementos()
            
            pygame.display.update()
