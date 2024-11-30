import pygame
import sys
from puzzles.aed_puzzle import create_random_aed_puzzle

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste - Puzzle de AED")

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
    puzzle = create_random_aed_puzzle()
    font = pygame.font.Font(None, 32)
    user_input = ""
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if puzzle.check_solution(user_input):
                        print("Correto!")
                    else:
                        print("Incorreto!")
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_SPACE:
                    puzzle = create_random_aed_puzzle()
                    user_input = ""
                else:
                    user_input += event.unicode
        
        screen.fill((0, 0, 0))
        
        # Renderiza o texto do puzzle
        y = render_text(screen, puzzle.get_puzzle_text(), font, 50)
        
        # Renderiza a entrada do usuário com espaçamento adequado
        input_text = f"Sua resposta: {user_input}"
        y = render_text(screen, input_text, font, y + 40)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()