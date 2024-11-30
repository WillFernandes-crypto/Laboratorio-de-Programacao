import random
from typing import List, Tuple, Dict, Set
from utils.text_formatter import format_puzzle_text

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
        text_question = format_puzzle_text(
            "Dado o grafo ponderado abaixo:",
            max_chars_per_line=35
        )
        
        graph_visual = """
        A --4-- B
        |      /|
        2    1  5
        |  /    |
        C --8-- D
        \\     /
         10  2
          \\ /
           E"""
        
        text_instruction = format_puzzle_text(
            "Qual é o caminho mais curto de A até E e qual é a soma total dos pesos deste caminho?",
            max_chars_per_line=35
        )
        
        answer = format_puzzle_text(
            "O caminho mais curto é A -> C -> B -> D -> E com peso total de 10 (2 + 1 + 5 + 2)",
            max_chars_per_line=35
        )
        
        return f"{text_question}\n\n{graph_visual}\n\n{text_instruction}", answer
    
    def minimum_spanning_tree_puzzle(self) -> Tuple[str, str]:
        """Puzzle sobre árvore geradora mínima"""
        text_question = format_puzzle_text(
            "Dado o grafo não-direcionado ponderado abaixo:",
            max_chars_per_line=35
            )
        graph_visual = """
        A ---3--- B
        |\\      /|
        4  2   6  5
        |    X   |
        C ---1-- D
        """

        text_instruction = format_puzzle_text(
            "Encontre a Árvore Geradora Mínima (MST) e a soma total dos seus pesos.",
            max_chars_per_line=35
        )
        
        answer = format_puzzle_text(
            "A MST é formada pelas arestas: C-D (1), A-B (3), B-D (5) com peso total de 9",
            max_chars_per_line=35
        )
        
        return f"{text_question}\n\n{graph_visual}\n\n{text_instruction}", answer
    
    def graph_coloring_puzzle(self) -> Tuple[str, str]:
        """Puzzle sobre coloração de grafos"""
        text_question = format_puzzle_text(
            "Considere o grafo não-direcionado abaixo onde cada vértice deve ser colorido de forma que vértices adjacentes não podem ter a mesma cor:",
            max_chars_per_line=35
        )
        
        graph_visual = """
        A ---- B
        |\\    |
        |  \\  |
        |    \\|
        C ---- D"""
        
        text_instruction = format_puzzle_text(
            "Qual é o número cromático deste grafo (número mínimo de cores necessárias)? Forneça um exemplo de coloração válida.",
            max_chars_per_line=35
        )
        
        answer = format_puzzle_text(
            "O número cromático é 3. Uma coloração válida seria: A: Vermelho, B: Azul, C: Azul, D: Vermelho",
            max_chars_per_line=35
        )
        
        return f"{text_question}\n\n{graph_visual}\n\n{text_instruction}", answer
