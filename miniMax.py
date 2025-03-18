# miniMax.py

import random
from time import time
import operators

PRINT_BEST = True
PRINT_ALL = False
MAX_DEPTH = 3  # Reduzir a profundidade máxima para 3

def minimax(game, depth, player):
    nodes_generated = 0

    if game.game_over() or depth == 0:
        return (game.get_score(), None), nodes_generated + 1

    if player:
        max_scores = [(float('-inf'), None)]
        successors, cols = operators.successors(game)
        for i in range(len(successors)):
            t, nodes = minimax(successors[i], depth - 1, False)
            score, _ = t
            nodes_generated += nodes
            if PRINT_ALL:
                if depth == MAX_DEPTH:
                    print("Col: " + str(cols[i]) + " Score: " + str(score))
            if score > max_scores[0][0]:
                max_scores.clear()
                max_scores.append((score, cols[i]))
            elif score == max_scores[0][0]:
                max_scores.append((score, cols[i]))
        return random.choice(max_scores), nodes_generated
    else:
        min_scores = [(float('inf'), None)]
        successors, cols = operators.successors(game)
        for i in range(len(successors)):
            t, nodes = minimax(successors[i], depth - 1, True)
            nodes_generated += nodes
            score, _ = t
            if PRINT_ALL:
                if depth == MAX_DEPTH:
                    print("Col: " + str(cols[i]) + " Score: " + str(score))
            if score < min_scores[0][0]:
                min_scores.clear()
                min_scores.append((score, cols[i]))
            elif score == min_scores[0][0]:
                min_scores.append((score, cols[i]))
        return random.choice(min_scores), nodes_generated

def main(game):
    ti = time()
    if game.turn == "X":
        t, nodes_generated = minimax(game, MAX_DEPTH, True)
        score, col = t
    else:
        t, nodes_generated = minimax(game, MAX_DEPTH, False)
        score, col = t
    tf = time()
    if PRINT_BEST:
        print("MiniMax algorithm: \n")
        print("Best column: " + str(col))
        print("Best score: " + str(score))
        print("Time: " + str(round(tf - ti, 5)) + "s")
        print("Nodes generated: " + str(nodes_generated) + "\n")
    return col