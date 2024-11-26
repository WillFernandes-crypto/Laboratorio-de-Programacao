from .automata_puzzle import AutomataPuzzle
from .theory_puzzle import TheoryPuzzle
from .graphs_puzzle import GraphsPuzzle
from .aed_puzzle import create_random_aed_puzzle
import random

class PuzzleManager:
    def __init__(self):
        self.puzzle_types = {
            'automata': AutomataPuzzle,
            'theory': TheoryPuzzle,
            'graphs': GraphsPuzzle,
            'aed': create_random_aed_puzzle
        }
        self.current_puzzle = None
        self.current_type = None
    
    def create_puzzle(self, puzzle_type=None):
        """
        Cria um novo puzzle do tipo especificado ou aleatório
        
        Args:
            puzzle_type (str, optional): 'automata', 'theory', 'graphs' ou 'aed'
        """
        if puzzle_type is None:
            puzzle_type = random.choice(list(self.puzzle_types.keys()))
            
        if puzzle_type not in self.puzzle_types:
            raise ValueError(f"Tipo de puzzle inválido: {puzzle_type}")
            
        self.current_type = puzzle_type
        self.current_puzzle = self.puzzle_types[puzzle_type]()
        return self.current_puzzle
    
    def get_current_puzzle(self):
        """Retorna o puzzle atual"""
        return self.current_puzzle
    
    def get_puzzle_type(self):
        """Retorna o tipo do puzzle atual"""
        return self.current_type
    
    def check_completion(self):
        """Verifica se o puzzle atual foi completado"""
        if self.current_puzzle is None:
            return False
            
        if hasattr(self.current_puzzle, 'completed'):
            return self.current_puzzle.completed
        return False
    
    def handle_event(self, event):
        """
        Encaminha eventos para o puzzle atual
        
        Args:
            event: Evento do Pygame
        """
        if self.current_puzzle and hasattr(self.current_puzzle, 'handle_event'):
            self.current_puzzle.handle_event(event)
    
    def update(self, delta_time):
        """
        Atualiza o puzzle atual
        
        Args:
            delta_time: Tempo desde o último frame
        """
        if self.current_puzzle and hasattr(self.current_puzzle, 'run'):
            self.current_puzzle.run(delta_time)
