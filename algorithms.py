import monteCarlo

def move(game, algorithm):
    if algorithm == "Monte Carlo":
        best_move, _, _ = monteCarlo.monte_carlo_tree_search(game, monteCarlo.TIME)
        return best_move
    elif algorithm == "Random":
        possible_moves = game.get_possible_moves()
        return random.choice(possible_moves)
    else:
        raise ValueError("Unknown algorithm")

def random_move(game):
    import random
    possible_moves = game.get_possible_moves()
    return random.choice(possible_moves) if possible_moves else None