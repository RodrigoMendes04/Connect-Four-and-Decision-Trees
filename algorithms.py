import monteCarlo
import random

def random_move(game):
    possible_moves = [col for col in range(game.COLUMNS) if not game.full_column(col)]
    return random.choice(possible_moves)

def move(game, algorithm):
    if algorithm == 'monteCarlo':
        return monteCarlo.main(game)
    elif algorithm == 'random':
        return random_move(game)
    else:
        raise ValueError("Unknown algorithm: " + str(algorithm))
