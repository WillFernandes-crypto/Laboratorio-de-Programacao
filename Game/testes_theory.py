import pygame
import sys
from puzzles.theory_puzzle import TheoryPuzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de Teoria")

def render_text(screen, text, font, start_y, max_width=700):
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
        screen.blit(text_surface, (50, y))
        y += 30
    
    return y

def main():
    theory = TheoryPuzzle()
    question, options, correct = theory.get_random_puzzle()
    font = pygame.font.Font(None, 32)
    selected_option = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    selected_option = int(event.unicode) - 1
                    if selected_option == correct:
                        print("Correto!")
                    else:
                        print("Incorreto!")
                if event.key == pygame.K_SPACE:
                    question, options, correct = theory.get_random_puzzle()
                    selected_option = None
        
        screen.fill((0, 0, 0))
        
        # Renderiza a questão
        y = render_text(screen, question, font, 50)
        y += 20  # Espaço extra entre a questão e as opções
        
        # Renderiza as opções
        for i, option in enumerate(options):
            color = (0, 255, 0) if selected_option == i else (255, 255, 255)
            # Formata cada opção e adiciona o número
            formatted_option = f"{i+1}. {option}"
            y = render_text(screen, formatted_option, font, y, max_width=650)
            y += 10  # Espaço extra entre opções
        
        pygame.display.flip()

if __name__ == "__main__":
    main()