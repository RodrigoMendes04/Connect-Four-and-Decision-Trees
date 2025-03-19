from play_game import main
from sys import argv

def exit_program():
    print("Invalid argument!\n")
    print("Usage: python3 main.py --> player vs player")
    print("Usage: python3 main.py [algorithm] --> player vs algorithm (algorithms: monteCarlo, miniMax)")
    print("Usage: python3 main.py [algorithm] [algorithm]--> algorithm vs algorithm (algorithms: monteCarlo, miniMax)\n")
    print("IMPORTANT: Don't repeat the same algorithm!\n")
    print("Usable arguments: (--terminal/-t) to play on terminal. Default is on GUI.")
    exit()

def start_program(algorithm1=None, algorithm2=None, GUI=True):
    print("Welcome to Connect 4!")
    print("The first to get 4 in a row wins!\n")
    if algorithm1 is None:
        print("Now playing: Player vs Player\n")
        main(algorithm1, algorithm2, GUI)
    elif algorithm2 is None:
        print("Now playing: Player vs " + str(algorithm1) + "\n")
        main(algorithm1, algorithm2, GUI)
    else:
        print("Now playing: " + str(algorithm1) + " vs " + str(algorithm2) + "\n")
        main(algorithm1, algorithm2, GUI)

def show_menu():
    print("Choose a game mode:")
    print("1. Human vs Human")
    print("2. Human vs Computer")
    print("3. Computer vs Computer")
    choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        start_program()
    elif choice == '2':
        algorithm = input("Choose algorithm:\n1. monteCarlo\n2. miniMax\n3. random\nEnter your choice (1/2/3): ")
        if algorithm == '1':
            start_program(algorithm1='monteCarlo')
        elif algorithm == '2':
            start_program(algorithm1='miniMax')
        elif algorithm == '3':
            start_program(algorithm1='random')
        else:
            print("Invalid algorithm")
            exit_program()
    elif choice == '3':
        algorithm1 = input("Choose algorithm for player 1:\n1. Monte Carlo\n2. MiniMax\n3. Random\nEnter your choice (1/2/3): ")
        algorithm2 = input("Choose algorithm for player 2:\n1. Monte Carlo\n2. MiniMax\n3. Random\nEnter your choice (1/2/3): ")
        if algorithm1 == '1':
            algorithm1 = 'monteCarlo'
        elif algorithm1 == '2':
            algorithm1 = 'miniMax'
        elif algorithm1 == '3':
            algorithm1 = 'random'
        else:
            print("Invalid algorithm")
            exit_program()
        if algorithm2 == '1':
            algorithm2 = 'monteCarlo'
        elif algorithm2 == '2':
            algorithm2 = 'miniMax'
        elif algorithm2 == '3':
            algorithm2 = 'random'
        else:
            print("Invalid algorithm")
            exit_program()
        start_program(algorithm1=algorithm1, algorithm2=algorithm2)
    else:
        print("Invalid choice")
        exit_program()

if __name__ == '__main__':
    show_menu()
