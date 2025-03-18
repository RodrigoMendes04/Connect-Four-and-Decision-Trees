import math
import random
from time import time
from operators import successors

TIME = 3  # Increase the time to 3 seconds
C = math.sqrt(2)
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
        possible_moves, _ = successors(self.game)
        return len(self.children) == len(possible_moves)

    def expand(self):
        possible_moves, _ = successors(self.game)
        for move in possible_moves:
            self.children.append(Node(move, self))

    def select_child(self):
        total_visits = math.log(self.visits)
        best_score = -float("inf")
        best_children = []
        unvisited_children = []

        for child in self.children:
            if child.visits == 0:
                unvisited_children.append(child)
            else:
                exploration_term = math.sqrt(math.log(total_visits + 1) / child.visits)
                score = child.wins / child.visits + C * exploration_term
                if score == best_score:
                    best_children.append(child)
                elif score > best_score:
                    best_score = score
                    best_children = [child]
        if unvisited_children:
            return random.choice(unvisited_children)
        return random.choice(best_children)

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent is not None:
            self.parent.backpropagate(result)

def monte_carlo_tree_search(game, t):
    root = Node(game)
    ti = time()
    tf = time()
    nodes_expanded = []

    while tf - ti < t:
        node = root
        while not node.is_leaf():
            node = node.select_child()
        if not node.is_fully_expanded():
            node.expand()
            new_node = random.choice(node.children)
        else:
            new_node = node.select_child()
        result = simulate(new_node.game)
        new_node.backpropagate(result)
        nodes_expanded.append(root.visits)
        tf = time()

    best_score = float("-inf")
    best_move = None
    for child in root.children:
        if child.visits > 0:  # Ensure the child has been visited at least once
            score = child.wins / child.visits
            if PRINT_ALL:
                print("Column: " + str(child.game.last_move) + " Win rate: " + str(round(score * 100, 2)) + "%")
            if score > best_score:
                best_score = score
                best_move = child.game.last_move

    return best_move, best_score, len(nodes_expanded)

def simulate(game):
    while not game.game_over():
        possible_moves, _ = successors(game)
        game = random.choice(possible_moves)
    if game.winner == "X":
        return 1
    elif game.winner == "O":
        return -1
    return 0

def main(game):
    ti = time()
    best_move, best_score, nodes_expanded = monte_carlo_tree_search(game, TIME)
    tf = time()
    if PRINT_BEST:
        print("Monte Carlo Simulation Tree Search: \n")
        print("Best column: " + str(best_move))
        print("Win rate: " + str(round(best_score * 100, 2)) + "%")
        print("Time: " + str(tf - ti) + "s")
        print("Nodes generated: " + str(nodes_expanded) + "\n")
    return best_move