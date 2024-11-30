import pygame
import sys
from puzzles.graphs_puzzle import GraphsPuzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de Grafos")

def render_text(screen, text, font, start_y, max_width=500):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_surface = font.render(test_line, True, (255, 255, 255))
        
        if test_surface.get_width() > max_width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    y = start_y
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        x = (800 - text_surface.get_width()) // 2
        screen.blit(text_surface, (x, y))
        y += 30
    
    return y

def main():
    graphs = GraphsPuzzle()
    font = pygame.font.Font(None, 32)
    user_input = ""
    question, answer = graphs.get_random_puzzle()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Resposta correta:", answer)
                    print("Sua resposta:", user_input)
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE:
                    question, answer = graphs.get_random_puzzle()
                    user_input = ""
                else:
                    user_input += event.unicode
        
        screen.fill((0, 0, 0))
        
        # Renderiza a questão e o grafo visual
        parts = question.split('\n\n')
        y = 50
        for part in parts:
            if '---' in part or '\\' in part:  # É um grafo visual
                # Renderiza o grafo linha por linha sem formatação
                for line in part.split('\n'):
                    text_surface = font.render(line, True, (255, 255, 255))
                    screen.blit(text_surface, (50, y))
                    y += 30
            else:
                # Renderiza o texto normal com formatação
                y = render_text(screen, part, font, y)
            y += 20
        
        # Renderiza a entrada do usuário
        input_text = f"Sua resposta: {user_input}"
        y = render_text(screen, input_text, font, y + 30)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()