import os
import concurrent.futures
from time import sleep, time
import algorithms
import operators
import contextlib
import threading
import sys

with contextlib.redirect_stdout(None):
    import pygame
    import pygame.gfxdraw

COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARE_SIZE = 100
WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (73, 107, 171)
YELLOW = (237, 175, 40)
DARK_YELLOW = (148, 105, 13)
RED = (255, 36, 0)
DARK_RED = (94, 25, 20)

def draw_message(screen, message):
    font = pygame.font.SysFont("monospace", 50)
    label = font.render(message, 1, BLACK)
    screen.blit(label, (40, 10))

def draw_hover_piece(screen, current_player, column, piece_surface):
    color = YELLOW if current_player == "O" else RED
    center_x = (column * SQUARE_SIZE) + (SQUARE_SIZE // 2)
    center_y = SQUARE_SIZE // 2
    
    piece_surface.fill((0, 0, 0, 0))
    pygame.gfxdraw.aacircle(piece_surface, SQUARE_SIZE // 2, SQUARE_SIZE // 2, SQUARE_SIZE // 2 - 5, WHITE)
    pygame.gfxdraw.filled_circle(piece_surface, SQUARE_SIZE // 2, SQUARE_SIZE // 2, SQUARE_SIZE // 2 - 5, color)
    
    screen.blit(piece_surface, (center_x - SQUARE_SIZE // 2, center_y - SQUARE_SIZE // 2))

def draw_board(game, screen):
    def draw(color):
        pygame.gfxdraw.aacircle(screen, c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2 - 5, BLUE)
        pygame.gfxdraw.filled_circle(screen, c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 1) * SQUARE_SIZE + SQUARE_SIZE // 2, SQUARE_SIZE // 2 - 5, color)
    
    screen.fill(BLUE)
    
    for c in range(COLUMN_COUNT):
        for r in reversed(range(ROW_COUNT)):
            draw(WHITE)
            if game.board[r][c] == "O":
                draw(YELLOW)
            elif game.board[r][c] == "X":
                draw(RED)
            elif game.board[r][c] == "o":
                draw(DARK_YELLOW)
            elif game.board[r][c] == "x":
                draw(DARK_RED)
    
    if game.turn == "O":
        draw_message(screen, "Yellow Turn")
    else:
        draw_message(screen, "Red Turn")
    
    if game.game_over(True):
        font = pygame.font.Font(None, 64)
        if game.winner == "X":
            winner_text = font.render("Red wins!", True, RED)
        elif game.winner == "O":
            winner_text = font.render("Yellow wins!", True, YELLOW)
        else:
            winner_text = font.render("It's a tie!", True, BLACK)
        
        text_rect = winner_text.get_rect(center=(WIDTH // 2, SQUARE_SIZE // 2))
        screen.blit(winner_text, text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
    
    pygame.display.update()

def input_column():
    while True:
        column = input("Choose a column: ")
        if column.isdigit():
            column = int(column)
            if 1 <= column <= COLUMN_COUNT:
                return column - 1
        print("Invalid column")

def play_on_terminal(game):
    while True:
        operators.refresh()
        print(game)
        
        # Process pygame events to keep window responsive
        pygame.event.pump()
        
        if game.game_over(True):
            if game.winner == "X":
                print("Red wins!")
            elif game.winner == "O":
                print("Yellow wins!")
            else:
                print("It's a tie!")
            break
        elif game.turn == "O":
            print("Yellow's turn")
            if game.algorithm1 is None:
                column = input_column()
            else:
                # Show thinking indicator
                def show_progress():
                    i = 0
                    chars = ['-', '\\', '|', '/']
                    while not move_done.is_set():
                        print(f"\rThinking {chars[i % 4]}", end='')
                        i += 1
                        sleep(0.2)
                        pygame.event.pump()  # Keep UI responsive
                    print("\rMove complete!     ")
                
                move_done = threading.Event()
                
                def ai_move():
                    nonlocal column
                    column = algorithms.move(game, game.algorithm1)
                    move_done.set()
                
                column = None
                progress_thread = threading.Thread(target=show_progress)
                progress_thread.daemon = True
                ai_thread = threading.Thread(target=ai_move)
                ai_thread.daemon = True
                
                progress_thread.start()
                ai_thread.start()
                
                # Process events while waiting
                while not move_done.is_set():
                    pygame.event.pump()
                    sleep(0.1)
                
                ai_thread.join()
                progress_thread.join()
            
            if not game.move(column):
                print("Invalid move")
        else:
            print("Red's turn")
            if game.algorithm2 is None:
                if game.algorithm1 is None:
                    column = input_column()
                else:
                    # Same approach for algorithm1
                    move_done = threading.Event()
                    
                    def ai_move():
                        nonlocal column
                        column = algorithms.move(game, game.algorithm1)
                        move_done.set()
                    
                    def show_progress():
                        i = 0
                        chars = ['-', '\\', '|', '/']
                        while not move_done.is_set():
                            print(f"\rThinking {chars[i % 4]}", end='')
                            i += 1
                            sleep(0.2)
                            pygame.event.pump()
                        print("\rMove complete!     ")
                    
                    column = None
                    progress_thread = threading.Thread(target=show_progress)
                    progress_thread.daemon = True
                    ai_thread = threading.Thread(target=ai_move)
                    ai_thread.daemon = True
                    
                    progress_thread.start()
                    ai_thread.start()
                    
                    while not move_done.is_set():
                        pygame.event.pump()
                        sleep(0.1)
                    
                    ai_thread.join()
                    progress_thread.join()
            else:
                # For algorithm2
                move_done = threading.Event()
                
                def ai_move():
                    nonlocal column
                    column = algorithms.move(game, game.algorithm2)
                    move_done.set()
                
                def show_progress():
                    i = 0
                    chars = ['-', '\\', '|', '/']
                    while not move_done.is_set():
                        print(f"\rThinking {chars[i % 4]}", end='')
                        i += 1
                        sleep(0.2)
                        pygame.event.pump()
                    print("\rMove complete!     ")
                
                column = None
                progress_thread = threading.Thread(target=show_progress)
                progress_thread.daemon = True
                ai_thread = threading.Thread(target=ai_move)
                ai_thread.daemon = True
                
                progress_thread.start()
                ai_thread.start()
                
                while not move_done.is_set():
                    pygame.event.pump()
                    sleep(0.1)
                
                ai_thread.join()
                progress_thread.join()
            
            if not game.move(column):
                print("Invalid move")
        
        print()

def player_vs_player(game):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Connect 4 - player vs player')
    
    piece_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    
    while True:
        draw_board(game, screen)
        
        # Process all events to keep UI responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                draw_hover_piece(screen, game.turn, event.pos[0] // SQUARE_SIZE, piece_surface)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                column = pos[0] // SQUARE_SIZE
                
                if game.move(column):
                    draw_board(game, screen)
        
        pygame.display.update()

def player_vs_algorithm(game):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Connect 4 - player vs ' + str(game.algorithm1))
    
    piece_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    thinking_font = pygame.font.SysFont("monospace", 30)
    
    while True:
        draw_board(game, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEMOTION and game.turn == "O":  # Only show hover when it's player's turn
                draw_hover_piece(screen, game.turn, event.pos[0] // SQUARE_SIZE, piece_surface)
            
            elif event.type == pygame.MOUSEBUTTONDOWN and game.turn == "O":  # Only accept clicks when it's player's turn
                column = event.pos[0] // SQUARE_SIZE
                
                if game.move(column):
                    draw_board(game, screen)
        
        # Computer's turn with threading
        if not game.game_over() and game.algorithm1 and game.turn == "X":
            # Show thinking message
            thinking_label = thinking_font.render("Thinking...", 1, WHITE)
            thinking_rect = thinking_label.get_rect(center=(WIDTH // 2, 30))
            pygame.draw.rect(screen, BLUE, thinking_rect)
            screen.blit(thinking_label, thinking_rect)
            pygame.display.update()
            
            # Use threading to prevent UI freezing
            move_done = threading.Event()
            
            def ai_move():
                nonlocal column
                column = algorithms.move(game, game.algorithm1)
                move_done.set()
            
            column = None
            ai_thread = threading.Thread(target=ai_move)
            ai_thread.daemon = True
            ai_thread.start()
            
            # Keep processing events while AI is thinking
            while not move_done.is_set():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                # Add animation or progress indicator here if desired
                pygame.display.update()
                sleep(0.05)
            
            # Wait for thread to complete
            ai_thread.join()
            
            # Make the move
            if game.move(column):
                draw_board(game, screen)
        
        pygame.display.update()

def algorithm_vs_algorithm(game):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'Connect 4 - {game.algorithm1} vs {game.algorithm2}')
    
    thinking_font = pygame.font.SysFont("monospace", 30)
    
    while not game.game_over():
        draw_board(game, screen)
        
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Show which algorithm is thinking
        algorithm = game.algorithm1 if game.turn == "O" else game.algorithm2
        thinking_label = thinking_font.render(f"{algorithm} is thinking...", 1, WHITE)
        thinking_rect = thinking_label.get_rect(center=(WIDTH // 2, 30))
        pygame.draw.rect(screen, BLUE, thinking_rect)
        screen.blit(thinking_label, thinking_rect)
        pygame.display.update()
        
        # Use threading for AI move
        move_done = threading.Event()
        
        def ai_move():
            nonlocal column
            column = algorithms.move(game, algorithm)
            move_done.set()
        
        column = None
        ai_thread = threading.Thread(target=ai_move)
        ai_thread.daemon = True
        ai_thread.start()
        
        # Keep processing events while AI thinks
        while not move_done.is_set():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            sleep(0.05)
        
        # Wait for thread
        ai_thread.join()
        
        # Make move
        game.move(column)
        sleep(0.5)  # Brief pause between moves
    
    # Show final state
    draw_board(game, screen)
    pygame.time.delay(3000)  # Show the result for 3 seconds
    pygame.quit()
    sys.exit()
