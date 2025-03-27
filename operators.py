# operators.py
import copy

def create_game():
    # Instead of importing Game, we'll return a basic board structure
    return {
        'board': [["-"] * 7 for _ in range(6)],
        'turn': "O",
        'winner': None,
        'played_moves': 0
    }

def refresh():
    print("\n" * 100)

def successors(game_state):
    possible_successors = []
    cols = []
    for i in range(7):
        # Create a deep copy of the game state
        successor = copy.deepcopy(game_state)
        if not is_column_full(successor['board'], i):
            # Make the move
            make_move(successor, i)
            possible_successors.append(successor)
            cols.append(i)
    return possible_successors, cols

def is_column_full(board, column):
    return board[0][column] != "-"

def make_move(game_state, column):
    for row in reversed(range(6)):
        if game_state['board'][row][column] == "-":
            game_state['board'][row][column] = game_state['turn']
            game_state['played_moves'] += 1
            game_state['turn'] = "X" if game_state['turn'] == "O" else "O"
            return True
    return False