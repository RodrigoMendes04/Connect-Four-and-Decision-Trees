import math
import random
from time import time
import pickle

NUM_SIMULATIONS = 10000  # Número fixo de iterações para MCTS
C = math.sqrt(2)  # Constante de exploração

PRINT_ALL = False
PRINT_BEST = True

class Node:
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_leaf(self):
        return self.game.game_over() or len(self.children) == 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.get_possible_moves())

    def expand(self):
        possible_moves = self.game.get_possible_moves()
        for move in possible_moves:
            new_game = self.game.make_copy()
            new_game.make_move(move)
            self.children.append(Node(new_game, self))

    def select_child(self):
        best_score = -float("inf")
        best_children = []

        for child in self.children:
            if child.visits == 0:
                return child
            # Fórmula UCB1
            exploration = math.sqrt(math.log(self.visits) / child.visits)
            score = (child.wins / child.visits) + C * exploration
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        return random.choice(best_children)

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None:
            self.parent.backpropagate(result)

def monte_carlo_tree_search(game, num_simulations):
    root = Node(game)

    for _ in range(num_simulations):
        node = root

        # Seleção
        while not node.is_leaf():
            node = node.select_child()

        # Expansão
        if not node.is_fully_expanded() and not node.game.game_over():
            node.expand()
            if node.children:
                node = random.choice(node.children)

        # Simulação
        result = simulate(node.game.make_copy(), node.game.current_player)

        # Retropropagação
        node.backpropagate(result)

    # Escolher melhor movimento
    best_score = -float("inf")
    best_move = None
    for child in root.children:
        if child.visits > 0:
            score = child.wins / child.visits
            if score > best_score:
                best_score = score
                best_move = child.game.last_move
    return best_move, best_score, root.visits

def simulate(game, player):
    while not game.game_over():
        possible_moves = game.get_possible_moves()
        if not possible_moves:
            break
        move = random.choice(possible_moves)
        game.make_move(move)

    if game.winner == player:
        return 1
    elif game.winner == "Draw":
        return 0
    else:
        return -1

def save_training_data(data, filename="training_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_training_data(filename="training_data.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def train(game, iterations, save_file="training_data.pkl"):
    data = load_training_data(save_file) or {}
    print("Loaded training data.")
    for i in range(iterations):
        print(f"Training iteration {i+1}/{iterations}")
        monte_carlo_tree_search(game, NUM_SIMULATIONS)
    save_training_data(data, save_file)
    print("Training data saved.")

def move(game, algorithm):
    if algorithm == "Monte Carlo":
        best_move, _, _ = monte_carlo_tree_search(game, NUM_SIMULATIONS)
        return best_move
    elif algorithm == "Random":
        possible_moves = game.get_possible_moves()
        return random.choice(possible_moves)
