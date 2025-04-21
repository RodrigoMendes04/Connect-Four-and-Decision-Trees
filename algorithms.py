from monteCarlo import monte_carlo_tree_search, NUM_SIMULATIONS
import random
import pygame
import time

def move(game, algorithm):
    # Process pygame events before starting move calculation
    pygame.event.pump()
    
    if algorithm == "Monte Carlo":
        # Show that the algorithm is thinking
        print("Monte Carlo algorithm is calculating...")
        
        # Start timer for timeout
        start_time = time.time()
        timeout = 5  # 5 seconds timeout
        
        # Process events periodically during calculation
        while time.time() - start_time < 0.5:  # Small delay to show thinking
            pygame.event.pump()
            time.sleep(0.1)
        
        best_move, _, _ = monte_carlo_tree_search(game, NUM_SIMULATIONS)
        return best_move
        
    elif algorithm == "Random":
        possible_moves = game.get_possible_moves()
        
        # Add a small delay for consistency
        pygame.event.pump()
        time.sleep(0.3)
        
        return random.choice(possible_moves)
    else:
        raise ValueError("Unknown algorithm")

def random_move(game):
    possible_moves = game.get_possible_moves()
    return random.choice(possible_moves) if possible_moves else None
