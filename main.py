from game import Game
import pygame
import algorithms
import sys

def exit_program():
    print("Invalid argument!")
    print("Usage: python main.py --> player vs player")
    print("Usage: python main.py [algorithm] --> player vs algorithm")
    print("Usage: python main.py [algorithm1] [algorithm2] --> algorithm vs algorithm")
    print("\nAvailable algorithms: Monte Carlo, Random")
    sys.exit()

def choose_interface():
    print("\nChoose interface:")
    print("1. Terminal")
    print("2. PyGame (graphical)")
    choice = input("Enter your choice (1/2): ")
    return choice == "2"

def choose_algorithm(player_num):
    print(f"\nChoose algorithm for Player {player_num}:")
    print("1. Monte Carlo")
    print("2. Random")
    choice = input("Enter your choice (1/2): ")

    if choice == "1": return "Monte Carlo"
    elif choice == "2": return "Random"
    else:
        print("Invalid choice, defaulting to Random")
        return "Random"

def main():
    print("Welcome to Connect 4!")
    print("The first to get 4 in a row wins!\n")

    # Choose game mode
    print("\nChoose game mode:")
    print("1. Human vs Human")
    print("2. Human vs Computer")
    print("3. Computer vs Computer")
    mode = input("Enter your choice (1/2/3): ")

    # Set up players based on mode
    if mode == "1":
        algorithm1 = None
        algorithm2 = None
    elif mode == "2":
        algorithm1 = None
        algorithm2 = choose_algorithm(2)
    elif mode == "3":
        algorithm1 = choose_algorithm(1)
        algorithm2 = choose_algorithm(2)
    else:
        print("Invalid choice, defaulting to Human vs Human")
        algorithm1 = None
        algorithm2 = None

    # Create and run game
    print("Creating game...")
    game = Game(algorithm1=algorithm1, algorithm2=algorithm2)

    # Train the algorithms only if both players are algorithms
    if algorithm1 == "Monte Carlo" and algorithm2 == "Monte Carlo":
        from monteCarlo import train
        print("Training algorithms...")
        train(game, 500)  # Adjust the number of iterations as needed
        print("Training completed.")
        sys.exit()  # Stop the program after training

    if choose_interface():
        print("Running game with PyGame interface...")
        game.run_game()
    else:
        # Terminal version
        print("\nStarting game in terminal...")
        print("Enter column numbers (1-7) to make moves.")

        while True:
            print(game)

            if game.game_over():
                if game.winner == "Draw":
                    print("Game Over - It's a draw!")
                else:
                    winner = "Yellow" if game.winner == "O" else "Red"
                    if game.algorithm1 and game.winner == "O":
                        winner = game.algorithm1
                    elif game.algorithm2 and game.winner == "X":
                        winner = game.algorithm2
                    print(f"Game Over - {winner} wins!")
                break

            if (game.turn == "O" and not game.algorithm1) or (game.turn == "X" and not game.algorithm2):
                # Human turn
                try:
                    col = int(input(f"{'Yellow' if game.turn == 'O' else 'Red'}'s turn. Enter column (1-7): ")) - 1
                    if not game.move(col):
                        print("Invalid move! Try again.")
                except ValueError:
                    print("Please enter a number between 1 and 7")
            else:
                # Computer turn
                algorithm = game.algorithm1 if game.turn == "O" else game.algorithm2
                print(f"{algorithm} is thinking...")
                col = algorithms.move(game, algorithm)
                game.move(col)

            # Ensure Pygame events are processed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
