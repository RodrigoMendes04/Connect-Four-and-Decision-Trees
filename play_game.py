import os
import concurrent.futures
from time import sleep, time
import algorithms
import operators
import contextlib

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
        exit()
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
            if game.algorithm2 is None:
                column = input_column()
            else:
                column = algorithms.move(game, game.algorithm1)
                sleep(0.5)
            if not game.move(column):
                print("Invalid move")
        else:
            print("Red's turn")
            if game.algorithm2 is None:
                if game.algorithm1 is None:
                    column = input_column()
                else:
                    column = algorithms.move(game, game.algorithm1)
                    sleep(0.5)
            else:
                column = algorithms.move(game, game.algorithm2)
                sleep(0.5)
            if not game.move(column):
                print("Invalid move")
            print()

def player_vs_player(game):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Connect 4 - player vs player')

    while True:
        draw_board(game, screen)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEMOTION:
            draw_hover_piece(screen, game.turn, pygame.mouse.get_pos()[0] // SQUARE_SIZE, pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // SQUARE_SIZE
            if game.move(column):
                draw_board(game, screen)
        pygame.display.update()

def player_vs_algorithm(game):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Connect 4 - player vs ' + str(game.algorithm1))

    while True:
        draw_board(game, screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEMOTION:
                draw_hover_piece(screen, game.turn, event.pos[0] // SQUARE_SIZE, pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                column = event.pos[0] // SQUARE_SIZE
                if game.move(column):
                    draw_board(game, screen)
                    if not game.game_over() and game.algorithm1:
                        # Movimento do computador (sem threads)
                        column = algorithms.move(game, game.algorithm1)
                        pygame.time.delay(500)  # Delay de 500ms para evitar travamentos
                        if game.move(column):
                            draw_board(game, screen)
        pygame.display.update()

def algorithm_vs_algorithm(game):
    while True:
        operators.refresh()
        print(game)
        if game.game_over(True):
            if game.winner == "X":
                print("Red wins!")
            elif game.winner == "O":
                print("Yellow wins!")
            else:
                print("It's a tie!")
            break
        elif game.turn == "O":
            column = algorithms.move(game, game.algorithm1)
            sleep(0.5)
            if not game.move(column):
                print("Invalid move")
        else:
            column = algorithms.move(game, game.algorithm2)
            sleep(0.5)
            if not game.move(column):
                print("Invalid move")
            print()

def main(algorithm1, algorithm2, gui):
    game = operators.create_game()
    game.algorithm1 = algorithm1
    game.algorithm2 = algorithm2

    if not gui:
        if algorithm1 and algorithm2:
            algorithm_vs_algorithm(game)
        else:
            play_on_terminal(game)
    else:
        if algorithm1 is None:
            player_vs_player(game)
        if algorithm2 is None:
            player_vs_algorithm(game)
        else:
            algorithm_vs_algorithm(game)
