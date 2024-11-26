import random
from typing import List, Tuple, Dict, Set

class GraphsPuzzle:
    def __init__(self):
        self.puzzles = [
            self.shortest_path_puzzle,
            self.minimum_spanning_tree_puzzle,
            self.graph_coloring_puzzle
        ]
        
    def get_random_puzzle(self) -> Tuple[str, str]:
        """Retorna um puzzle aleatório sobre grafos"""
        puzzle_func = random.choice(self.puzzles)
        return puzzle_func()
    
    def shortest_path_puzzle(self) -> Tuple[str, str]:
        """Puzzle sobre caminho mais curto em um grafo ponderado"""
        graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'A': 4, 'C': 1, 'D': 5},
            'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
            'D': {'B': 5, 'C': 8, 'E': 2},
            'E': {'C': 10, 'D': 2}
        }
        
        question = """
        Dado o grafo ponderado abaixo:
        A --4-- B
        |      /|
        2    1  5
        |  /    |
        C --8-- D
        \\     /
         10  2
          \\ /
           E
        
        Qual é o caminho mais curto de A até E e qual é a soma total dos pesos deste caminho?
        """
        
        answer = "O caminho mais curto é A -> C -> B -> D -> E com peso total de 10 (2 + 1 + 5 + 2)"
        return question, answer
    
    def minimum_spanning_tree_puzzle(self) -> Tuple[str, str]:
        """Puzzle sobre árvore geradora mínima"""
        question = """
        Dado o grafo não-direcionado ponderado abaixo:
        A ---3--- B
        |\\      /|
        4  2   6  5
        |    X   |
        C ---1-- D
        
        Encontre a Árvore Geradora Mínima (MST) e a soma total dos seus pesos.
        """
        
        answer = "A MST é formada pelas arestas: C-D (1), A-B (3), B-D (5) com peso total de 9"
        return question, answer
    
    def graph_coloring_puzzle(self) -> Tuple[str, str]:
        """Puzzle sobre coloração de grafos"""
        question = """
        Considere o grafo não-direcionado abaixo onde cada vértice deve ser colorido
        de forma que vértices adjacentes não podem ter a mesma cor:
        
        A ---- B
        |\\    |
        |  \\  |
        |    \\|
        C ---- D
        
        Qual é o número cromático deste grafo (número mínimo de cores necessárias)?
        Forneça um exemplo de coloração válida.
        """
        
        answer = """O número cromático é 3.
        Uma coloração válida seria:
        A: Vermelho
        B: Azul
        C: Azul
        D: Vermelho"""
        return question, answer
