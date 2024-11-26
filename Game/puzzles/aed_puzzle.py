import random
from abc import ABC, abstractmethod

class AEDPuzzle(ABC):
    def __init__(self):
        self.completed = False
        
    @abstractmethod
    def check_solution(self, answer):
        pass
    
    @abstractmethod
    def get_puzzle_text(self):
        pass

class SortingPuzzle(AEDPuzzle):
    def __init__(self):
        super().__init__()
        self.sequences = [
            ([5, 2, 8, 1, 9], [1, 2, 5, 8, 9]),
            ([3, 7, 4, 1, 6], [1, 3, 4, 6, 7]),
            ([10, 5, 3, 8, 2], [2, 3, 5, 8, 10])
        ]
        self.selected_sequence = random.choice(self.sequences)
        
    def check_solution(self, answer):
        # Resposta deve ser uma string com os números em ordem
        try:
            user_sequence = [int(x) for x in answer.split()]
            self.completed = user_sequence == self.selected_sequence[1]
            return self.completed
        except:
            return False
            
    def get_puzzle_text(self):
        return f"Ordene a seguinte sequência em ordem crescente: {' '.join(map(str, self.selected_sequence[0]))}"

class BinarySearchTreePuzzle(AEDPuzzle):
    def __init__(self):
        super().__init__()
        self.trees = [
            ([5, 3, 7, 2, 4], "5,3,7,2,4"),  # Representação em pré-ordem
            ([8, 4, 12, 2, 6], "8,4,12,2,6"),
            ([10, 5, 15, 3, 7], "10,5,15,3,7")
        ]
        self.selected_tree = random.choice(self.trees)
        
    def check_solution(self, answer):
        # Resposta deve ser a sequência em pré-ordem
        try:
            self.completed = answer.strip() == self.selected_tree[1]
            return self.completed
        except:
            return False
            
    def get_puzzle_text(self):
        return f"Insira os seguintes valores em uma árvore binária de busca e forneça a travessia em pré-ordem (separados por vírgula): {' '.join(map(str, self.selected_tree[0]))}"

class GraphTraversalPuzzle(AEDPuzzle):
    def __init__(self):
        super().__init__()
        self.graphs = [
            {
                'vertices': ['A', 'B', 'C', 'D'],
                'edges': [('A','B'), ('B','C'), ('C','D'), ('D','A')],
                'bfs_from_a': "A,B,D,C"
            },
            {
                'vertices': ['A', 'B', 'C', 'D'],
                'edges': [('A','B'), ('A','C'), ('B','D'), ('C','D')],
                'bfs_from_a': "A,B,C,D"
            }
        ]
        self.selected_graph = random.choice(self.graphs)
        
    def check_solution(self, answer):
        # Resposta deve ser a sequência BFS começando do vértice A
        try:
            self.completed = answer.strip() == self.selected_graph['bfs_from_a']
            return self.completed
        except:
            return False
            
    def get_puzzle_text(self):
        edges_text = ', '.join([f"{e[0]}-{e[1]}" for e in self.selected_graph['edges']])
        return f"Para o grafo com arestas: {edges_text}, forneça a ordem de visitação usando BFS começando do vértice A (separados por vírgula)"

def create_random_aed_puzzle():
    puzzle_types = [SortingPuzzle, BinarySearchTreePuzzle, GraphTraversalPuzzle]
    selected_puzzle = random.choice(puzzle_types)
    return selected_puzzle()
