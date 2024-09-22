import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Define as dimensões da janela
largura, altura = 800, 600
screen = pygame.display.set_mode((largura, altura))

# Define a cor de fundo (RGB)
cor_fundo = (0, 128, 255)

# Define o título da janela
pygame.display.set_caption('Janela Simples')

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Preenche o fundo da janela com a cor definida
    screen.fill(cor_fundo)

    # Atualiza a tela
    pygame.display.update()
