import pygame
from utils.settings import *
from utils.sprites import *
import math
from random import choice
from utils.text_formatter import format_puzzle_text

class State(pygame.sprite.Sprite):
    def __init__(self, pos, groups, is_initial=False, is_final=False):
        super().__init__(groups)
        # Visual
        self.radius = 30
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)
        
        # Estado
        self.is_initial = is_initial
        self.is_final = is_final
        self.transitions = {}  # {simbolo: estado_destino}
        self.selected = False
        
        self.draw_state()
    
    def draw_state(self):
        # Desenha círculo principal
        pygame.draw.circle(self.image, 'white', (self.radius, self.radius), self.radius, 2)
        
        # Se for estado final, desenha círculo interno
        if self.is_final:
            pygame.draw.circle(self.image, 'white', (self.radius, self.radius), self.radius - 5, 2)
            
        # Se for estado inicial, desenha seta
        if self.is_initial:
            start_pos = (0, self.radius)
            end_pos = (self.radius - 10, self.radius)
            pygame.draw.line(self.image, 'white', start_pos, end_pos, 2)
            # Desenha ponta da seta
            pygame.draw.polygon(self.image, 'white', [
                (end_pos[0], end_pos[1]),
                (end_pos[0] - 10, end_pos[1] - 5),
                (end_pos[0] - 10, end_pos[1] + 5)
            ])

class Transition:
    def __init__(self, from_state, to_state, symbol):
        self.from_state = from_state
        self.to_state = to_state
        self.symbol = symbol

class AutomataPuzzle:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.states = pygame.sprite.Group()
        self.transitions = []
        self.font = pygame.font.Font(None, 36)
        
        # Estados do puzzle
        self.completed = False
        self.escape_pressed = False
        self.transition_start = None
        self.current_symbol = None
        
        # Mensagens de feedback
        self.message = ""
        self.message_timer = 0
        
        # Seleciona aleatoriamente um dos três puzzles
        self.puzzle_type = choice(['ab', 'aab', 'aba'])
        
        # Criar estados iniciais
        self.create_initial_states()
        
        self.success_message = ""
    
    def create_initial_states(self):
        # Configuração comum para todos os puzzles
        if self.puzzle_type == 'ab':
            # Estado inicial (q0)
            self.q0 = State(
                pos=(200, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_initial=True
            )
            
            # Estado intermediário (q1)
            self.q1 = State(
                pos=(400, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states]
            )
            
            # Estado final (q2)
            self.q2 = State(
                pos=(600, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_final=True
            )
            
        elif self.puzzle_type == 'aab':
            # Estado inicial (q0)
            self.q0 = State(
                pos=(200, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_initial=True
            )
            
            # Estado após primeiro 'a' (q1)
            self.q1 = State(
                pos=(400, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states]
            )
            
            # Estado após segundo 'a' (q2)
            self.q2 = State(
                pos=(600, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states]
            )
            
            # Estado final após 'b' (q3)
            self.q3 = State(
                pos=(800, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_final=True
            )
            
        elif self.puzzle_type == 'aba':
            # Estado inicial (q0)
            self.q0 = State(
                pos=(200, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_initial=True
            )
            
            # Estado após 'a' (q1)
            self.q1 = State(
                pos=(400, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states]
            )
            
            # Estado após 'b' (q2)
            self.q2 = State(
                pos=(600, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states]
            )
            
            # Estado final após segundo 'a' (q3)
            self.q3 = State(
                pos=(800, SCREEN_HEIGHT//2),
                groups=[self.all_sprites, self.states],
                is_final=True
            )
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.escape_pressed = True
            elif event.key == pygame.K_RETURN and not self.completed:
                self.check_solution()
            elif self.transition_start and not self.completed and event.key in [pygame.K_a, pygame.K_b]:
                self.current_symbol = pygame.key.name(event.key)
                self.show_message(f"Símbolo '{self.current_symbol}' selecionado. Agora selecione o estado de destino")
                
        if not self.completed:  # Só permite modificações se não estiver completo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo
                    mouse_pos = pygame.mouse.get_pos()
                    for state in self.states:
                        if state.rect.collidepoint(mouse_pos):
                            if not self.transition_start:
                                self.transition_start = state
                                self.show_message("Selecione o símbolo (a/b)")
                            elif self.current_symbol:
                                if self.create_transition(self.transition_start, state, self.current_symbol):
                                    self.show_message(f"Transição '{self.current_symbol}' criada!")
                                self.transition_start = None
                                self.current_symbol = None
                            break
                            
                elif event.button == 3:  # Botão direito
                    self.transition_start = None
                    self.current_symbol = None
                    self.show_message("Seleção cancelada")
    
    def create_transition(self, from_state, to_state, symbol):
        # Verifica se já existe uma transição entre estes estados
        existing_transition = None
        for t in self.transitions:
            if t.from_state == from_state and t.to_state == to_state:
                existing_transition = t
                break
        
        # Se já existe transição entre estes estados
        if existing_transition:
            # Verifica se o símbolo já existe
            if symbol in existing_transition.symbol:
                self.show_message(f"Símbolo '{symbol}' já existe nesta transição!")
                return False
            # Adiciona o novo símbolo à transição existente
            existing_transition.symbol += f",{symbol}"
            from_state.transitions[symbol] = to_state
            return True
        else:
            # Cria nova transição
            self.transitions.append(Transition(from_state, to_state, symbol))
            from_state.transitions[symbol] = to_state
            return True
        
    def show_message(self, text):
        self.message = text
        self.message_timer = 60  # Frames que a mensagem ficará visível
    
    def check_solution(self):
        """Verifica se o autômato aceita a linguagem correta"""
        try:
            if self.verify_solution():
                self.completed = True
                self.success_message = "Autômato construído com sucesso! Pressione ESC para sair"
                self.show_message(self.success_message)
            else:
                self.show_message("Solução incorreta. Tente novamente!")
        except AttributeError:
            self.show_message("Construa o autômato completo!")
    
    def draw_instructions(self):
        instructions = []
        
        if self.puzzle_type == 'ab':
            instructions = [
                "Construa um autômato que aceite a palavra 'ab'",
                "Clique esquerdo: selecionar estado",
                "Teclas a/b: definir símbolo da transição",
                "Clique direito: cancelar seleção",
                "ENTER: verificar solução",
                "ESC: sair do puzzle"
            ]
        elif self.puzzle_type == 'aab':
            instructions = [
                "Construa um autômato que aceite a palavra 'aab'",
                "Clique esquerdo: selecionar estado",
                "Teclas a/b: definir símbolo da transição",
                "Clique direito: cancelar seleção",
                "ENTER: verificar solução",
                "ESC: sair do puzzle"
            ]
        elif self.puzzle_type == 'aba':
            instructions = [
                "Construa um autômato que aceite a palavra 'aba'",
                "Clique esquerdo: selecionar estado",
                "Teclas a/b: definir símbolo da transição",
                "Clique direito: cancelar seleção",
                "ENTER: verificar solução",
                "ESC: sair do puzzle"
            ]
        
        for i, text in enumerate(instructions):
            text_surf = self.font.render(text, True, 'white')
            text_rect = text_surf.get_rect(topleft=(50, 50 + i * 40))
            self.display_surface.blit(text_surf, text_rect)
            
        if self.message and self.message_timer > 0:
            text_surf = self.font.render(self.message, True, 'yellow')
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
            self.display_surface.blit(text_surf, text_rect)
            self.message_timer -= 1
    
    def draw_transitions(self):
        for transition in self.transitions:
            start_pos = transition.from_state.rect.center
            end_pos = transition.to_state.rect.center
            
            # Verifica se é uma transição para o mesmo estado
            if transition.from_state == transition.to_state:
                # Ajustes para o arco ficar acima do estado
                radius = 30
                center_y = start_pos[1] - radius  # Move o centro do arco para cima
                
                # Define o retângulo para o arco
                rect = pygame.Rect(
                    start_pos[0] - radius,
                    center_y - radius,  # Posiciona o retângulo acima do estado
                    radius * 2,
                    radius * 2
                )
                
                # Desenha o semicírculo
                pygame.draw.arc(self.display_surface, 'white', rect, 
                              0, math.pi, 2)
                
                # Calcula o ponto para a seta (no lado esquerdo do arco)
                arrow_pos = (start_pos[0] - radius, center_y)
                
                # Desenha a ponta da seta
                arrow_size = 10
                arrow_p1 = (arrow_pos[0] - arrow_size, arrow_pos[1] - arrow_size)
                arrow_p2 = (arrow_pos[0] - arrow_size, arrow_pos[1] + arrow_size)
                
                pygame.draw.polygon(self.display_surface, 'white', 
                                  [arrow_pos, arrow_p1, arrow_p2])
                
                # Desenha o(s) símbolo(s)
                text_surf = self.font.render(transition.symbol, True, 'yellow')
                text_rect = text_surf.get_rect(center=(start_pos[0], center_y - radius))
                self.display_surface.blit(text_surf, text_rect)
            else:
                # Transição normal entre estados diferentes
                mid_x = (start_pos[0] + end_pos[0]) // 2
                mid_y = (start_pos[1] + end_pos[1]) // 2
                mid_pos = (mid_x, mid_y)
                
                # Desenha a linha
                pygame.draw.line(self.display_surface, 'white', start_pos, end_pos, 2)
                
                # Desenha a ponta da seta
                angle = math.atan2(end_pos[1] - start_pos[1], end_pos[0] - start_pos[0])
                arrow_size = 20
                arrow_angle = math.pi / 6
                
                arrow_p1 = (end_pos[0] - arrow_size * math.cos(angle - arrow_angle),
                           end_pos[1] - arrow_size * math.sin(angle - arrow_angle))
                arrow_p2 = (end_pos[0] - arrow_size * math.cos(angle + arrow_angle),
                           end_pos[1] - arrow_size * math.sin(angle + arrow_angle))
                
                pygame.draw.polygon(self.display_surface, 'white', 
                                  [end_pos, arrow_p1, arrow_p2])
                
                # Desenha o símbolo da transição
                text_surf = self.font.render(transition.symbol, True, 'yellow')
                text_rect = text_surf.get_rect(center=mid_pos)
                self.display_surface.blit(text_surf, text_rect)
    
    def run(self, delta_time):
        if self.escape_pressed:
            return
            
        self.display_surface.fill('black')
        
        # Só permite desenhar linha temporária se não estiver completo
        if not self.completed and self.transition_start and self.current_symbol:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.display_surface, 'yellow', 
                           self.transition_start.rect.center, mouse_pos, 2)
        
        self.draw_transitions()
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)
        
        # Mostra instruções apenas se não estiver completo
        if not self.completed:
            self.draw_instructions()
        
        # Se estiver completo, mostra apenas a mensagem de sucesso
        if self.completed:
            # Desenha um texto centralizado maior
            text_surf = self.font.render(self.success_message, True, 'yellow')
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100))
            self.display_surface.blit(text_surf, text_rect)
    
    def verify_solution(self):
        """Verifica se o autômato aceita a linguagem correta"""
        try:
            if self.puzzle_type == 'ab':
                # Verifica se aceita 'ab'
                return (
                    'a' in self.q0.transitions and self.q0.transitions['a'] == self.q1 and
                    'b' in self.q1.transitions and self.q1.transitions['b'] == self.q2 and
                    self.q2.is_final
                )
            
            elif self.puzzle_type == 'aab':
                # Verifica se aceita 'aab'
                return (
                    'a' in self.q0.transitions and self.q0.transitions['a'] == self.q1 and
                    'a' in self.q1.transitions and self.q1.transitions['a'] == self.q2 and
                    'b' in self.q2.transitions and self.q2.transitions['b'] == self.q3 and
                    self.q3.is_final
                )
            
            elif self.puzzle_type == 'aba':
                # Verifica se aceita 'aba'
                return (
                    'a' in self.q0.transitions and self.q0.transitions['a'] == self.q1 and
                    'b' in self.q1.transitions and self.q1.transitions['b'] == self.q2 and
                    'a' in self.q2.transitions and self.q2.transitions['a'] == self.q3 and
                    self.q3.is_final
                )
            
            return False
            
        except AttributeError:
            return False
    
    def get_puzzle_text(self):
        """Retorna o texto do puzzle baseado no tipo selecionado"""
        puzzle_texts = {
            'ab': format_puzzle_text(
                "Construa um autômato finito que aceite a linguagem L = {ab}",
                max_chars_per_line=35
            ),
            'aab': format_puzzle_text(
                "Construa um autômato finito que aceite a linguagem L = {aab}",
                max_chars_per_line=35
            ),
            'aba': format_puzzle_text(
                "Construa um autômato finito que aceite a linguagem L = {aba}",
                max_chars_per_line=35
            )
        }
        return puzzle_texts[self.puzzle_type]
