import random
from typing import List, Tuple, Dict
from utils.text_formatter import format_puzzle_text

class TheoryPuzzle:
    def __init__(self):
        self.puzzles = [
            self.turing_machine_puzzle,
            self.complexity_puzzle,
            self.computability_puzzle
        ]
        
    def get_random_puzzle(self) -> Tuple[str, List[str], int]:
        """Retorna um puzzle aleatório sobre teoria da computação"""
        puzzle_func = random.choice(self.puzzles)
        return puzzle_func()
    
    def turing_machine_puzzle(self) -> Tuple[str, List[str], int]:
        """Puzzle sobre Máquina de Turing"""
        question = format_puzzle_text(
            "Considere uma Máquina de Turing M que aceita a linguagem L = {w#w | w ∈ {0,1}*}. Qual das seguintes afirmações é verdadeira sobre esta máquina?",
            max_chars_per_line=35
        )
        
        options = [
            format_puzzle_text("A máquina precisa apenas de uma fita para reconhecer esta linguagem", max_chars_per_line=35),
            format_puzzle_text("A máquina precisa necessariamente de duas fitas para reconhecer esta linguagem", max_chars_per_line=35),
            format_puzzle_text("A máquina precisa de memória infinita para reconhecer qualquer entrada", max_chars_per_line=35),
            format_puzzle_text("Esta linguagem não pode ser reconhecida por uma Máquina de Turing", max_chars_per_line=35)
        ]
        
        correct_answer = 0
        return question, options, correct_answer
    
    def complexity_puzzle(self) -> Tuple[str, List[str], int]:
        """Puzzle sobre Complexidade Computacional"""
        question = format_puzzle_text(
            "Dado um problema P que é NP-Completo, qual das seguintes afirmações é verdadeira?",
            max_chars_per_line=35
        )
        
        options = [
            format_puzzle_text("Se P ≠ NP, então P não pode ser resolvido em tempo polinomial", max_chars_per_line=35),
            format_puzzle_text("P pode ser reduzido ao problema do caminho hamiltoniano em tempo polinomial", max_chars_per_line=35),
            format_puzzle_text("Se encontrarmos um algoritmo polinomial para P, então P = NP", max_chars_per_line=35),
            format_puzzle_text("P não pode ser resolvido por nenhum algoritmo", max_chars_per_line=35)
        ]
        
        correct_answer = 2
        return question, options, correct_answer
    
    def computability_puzzle(self) -> Tuple[str, List[str], int]:
        """Puzzle sobre Computabilidade"""
        question = """
        Sobre o Problema da Parada (Halting Problem), qual afirmação é correta?
        """
        
        options = [
            format_puzzle_text("É possível criar um programa que determine se qualquer outro programa irá parar", max_chars_per_line=35),
            format_puzzle_text("O problema é decidível para programas que usam apenas loops 'for'", max_chars_per_line=35),
            format_puzzle_text("O problema é indecidível, mas semi-decidível", max_chars_per_line=35),
            format_puzzle_text("O problema é decidível para programas que não usam recursão", max_chars_per_line=35)
        ]
        
        correct_answer = 2  # índice da resposta correta (0-based)
        return question, options, correct_answer

    def format_as_html(self, question: str, options: List[str]) -> str:
        """Formata o puzzle como HTML com cards clicáveis"""
        html = f"""
        <div class="puzzle-container">
            <div class="question">
                {question}
            </div>
            <div class="options">
        """
        
        for i, option in enumerate(options):
            html += f"""
                <button class="option-card" onclick="checkAnswer({i})">
                    {option}
                </button>
            """
            
        html += """
            </div>
        </div>
        <style>
            .puzzle-container {
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            
            .question {
                font-size: 18px;
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f5f5f5;
                border-radius: 8px;
            }
            
            .options {
                display: grid;
                gap: 15px;
            }
            
            .option-card {
                padding: 15px;
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: left;
                font-size: 16px;
            }
            
            .option-card:hover {
                background-color: #f0f0f0;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
        </style>
        <script>
            function checkAnswer(selectedIndex) {
                // Esta função será implementada no frontend para verificar a resposta
                console.log('Selected answer:', selectedIndex);
            }
        </script>
        """
        return html
