import math
import random
from time import time
import pickle
import pygame

# Reduzido de 10000 para 1000 para melhor desempenho
NUM_SIMULATIONS = 50000
C = math.sqrt(1.41)  # Constante de exploração
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
    
    # Processar eventos pygame no início
    pygame.event.pump()
    
    # Adicionar timestamp para timeout
    start_time = time()
    max_time = 5  # 5 segundos máximo
    
    for i in range(num_simulations):
        # Verificar timeout ou processar eventos a cada 100 iterações
        if i % 100 == 0:
            # Processar eventos pygame para manter UI responsiva
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
            
            # Verificar se excedemos o limite de tempo
            if time() - start_time > max_time:
                break
                
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
    
    # Encontrar melhor movimento
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
    max_iterations = 100
    iteration = 0
    opponent = "X" if player == "O" else "O"

    while not game.game_over() and iteration < max_iterations:
        possible_moves = game.get_possible_moves()
        if not possible_moves:
            break

        # 1. Tenta ganhar imediatamente
        for move in possible_moves:
            temp_game = game.make_copy()
            temp_game.make_move(move)
            if temp_game.winner == player:
                game.make_move(move)
                break
        else:
            # 2. Tenta bloquear vitória do adversário
            for move in possible_moves:
                temp_game = game.make_copy()
                temp_game.make_move(move)
                if temp_game.winner == opponent:
                    game.make_move(move)
                    break
            else:
                # 3. Caso contrário, joga aleatoriamente
                move = random.choice(possible_moves)
                game.make_move(move)
        iteration += 1

    if game.winner == player:
        return 1
    elif game.winner == "Draw":
        return 0
    else:
        return 0

def train(game, iterations, save_file="training_data.pkl"):
    data = load_training_data(save_file) or {}
    print("Loaded training data.")
    
    for i in range(iterations):
        print(f"Training iteration {i+1}/{iterations}")
        
        # Processar eventos pygame durante o treino
        if i % 10 == 0:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
        
        monte_carlo_tree_search(game, NUM_SIMULATIONS // 10)  # Simulações reduzidas para treino
    
    save_training_data(data, save_file)
    print("Training data saved.")

def save_training_data(data, filename="training_data.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_training_data(filename="training_data.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
