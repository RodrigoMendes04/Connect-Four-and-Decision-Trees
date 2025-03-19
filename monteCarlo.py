import math
import random
from time import time
from game import Game

TIME = 3  # Tempo máximo para o MCTS pensar (em segundos)
C = math.sqrt(2)  # Constante de exploração

class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state  # Estado atual do jogo
        self.parent = parent  # Nó pai
        self.move = move  # Movimento que levou a este estado
        self.children = []  # Lista de nós filhos
        self.wins = 0  # Número de vitórias nas simulações
        self.visits = 0  # Número de visitas nas simulações
        self.untried_moves = self.get_legal_moves()  # Movimentos ainda não explorados

    def get_legal_moves(self):
        # Retorna uma lista de colunas válidas para jogar
        return [col for col in range(self.game_state.COLUMNS) if not self.game_state.full_column(col)]

    def select_child(self):
        # Seleciona o filho com o maior UCB1 (Upper Confidence Bound)
        best_score = -float("inf")
        best_child = None

        for child in self.children:
            if child.visits == 0:
                return child  # Retorna um filho não visitado
            exploitation = child.wins / child.visits
            exploration = math.sqrt(2 * math.log(self.visits) / child.visits)
            score = exploitation + C * exploration

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def expand(self):
        # Expande um movimento não tentado
        move = self.untried_moves.pop()
        new_game_state = self.game_state.__copy__()
        new_game_state.move(move)
        child_node = Node(new_game_state, self, move)
        self.children.append(child_node)
        return child_node

    def update(self, result):
        # Atualiza as estatísticas do nó com o resultado da simulação
        self.visits += 1
        self.wins += result

def simulate(game_state):
    # Simula um jogo aleatório até o fim
    while not game_state.game_over():
        legal_moves = [col for col in range(game_state.COLUMNS) if not game_state.full_column(col)]
        move = random.choice(legal_moves)
        game_state.move(move)
    # Retorna 1 se o jogador atual venceu, -1 se perdeu, 0 se empate
    if game_state.winner == "X":
        return 1
    elif game_state.winner == "O":
        return -1
    return 0

def monte_carlo_tree_search(game, time_limit):
    root = Node(game)

    start_time = time()
    while time() - start_time < time_limit:
        node = root

        # Seleção: Escolha do melhor nó filho
        while not node.untried_moves and node.children:
            node = node.select_child()

        # Expansão: Expande um nó não explorado
        if node.untried_moves:
            node = node.expand()

        # Simulação: Simula um jogo aleatório a partir do nó expandido
        result = simulate(node.game_state.__copy__())

        # Retropropagação: Atualiza as estatísticas dos nós pais
        while node is not None:
            node.update(result)
            node = node.parent

    # Escolhe o movimento mais visitado
    best_move = max(root.children, key=lambda c: c.visits).move
    return best_move

def main(game):
    best_move = monte_carlo_tree_search(game, TIME)
    print(f"Monte Carlo escolheu a coluna: {best_move}")
    return best_move
