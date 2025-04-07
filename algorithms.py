from monteCarlo import monte_carlo_tree_search, NUM_SIMULATIONS
import random

def move(game, algorithm):
    if algorithm == "Monte Carlo":
        best_move, _, _ = monte_carlo_tree_search(game, NUM_SIMULATIONS)
        return best_move
    elif algorithm == "Random":
        possible_moves = game.get_possible_moves()
        return random.choice(possible_moves)
    else:
        raise ValueError("Unknown algorithm")

def random_move(game):
    possible_moves = game.get_possible_moves()
    return random.choice(possible_moves) if possible_moves else None
