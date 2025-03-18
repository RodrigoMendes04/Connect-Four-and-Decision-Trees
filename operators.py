from game import Game

DEFAULT_GAME = Game([["-"] * 7 for _ in range(6)])

PRINT_BOARD = False

def create_game():
    return DEFAULT_GAME.__copy__()

def refresh():
    print("\n" * 100)

def successors(game):
    possible_successors = []
    cols = []
    for i in range(7):
        successor = game.__copy__()
        if successor.move(i):
            possible_successors.append(successor)
            cols.append(i)
            if PRINT_BOARD:
                print(successor)
    return possible_successors, cols