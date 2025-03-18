import monteCarlo
import miniMax
import random

def random_move(game):
    possible_moves = []
    for i in range(7):
        if not game.full_column(i):
            possible_moves.append(i)
    random.shuffle(possible_moves)
    return possible_moves.pop()

def move(game, algorithm):
    if algorithm == 'monteCarlo':
        return monteCarlo.main(game)
    elif algorithm == 'miniMax':
        return miniMax.main(game)
    else:  # algorithm == 'random':
        return random_move(game)