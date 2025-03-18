import numpy as np
import pygame
import copy

class Game:
    ROWS = 6
    COLUMNS = 7
    CELL_SIZE = 100
    WIDTH = COLUMNS * CELL_SIZE
    HEIGHT = (ROWS + 1) * CELL_SIZE
    RADIUS = CELL_SIZE // 2 - 5

    def __init__(self, board=None, algorithm=None, turn="O", score=0, played_moves=0,
                 winnings_coords=None, last_move=None, algorithm1=None, algorithm2=None):
        self.board = board if board is not None else np.full((self.ROWS, self.COLUMNS), "-")
        self.algorithm = algorithm
        self.winner = None
        self.turn = turn
        self.score = score
        self.played_moves = played_moves
        self.winnings_coords = winnings_coords
        self.last_move = last_move
        self.game_over_flag = False
        self.algorithm1 = algorithm1
        self.algorithm2 = algorithm2
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pygame.font.SysFont("monospace", 50)
        self.running = True

    def clear_board_except_winning_pieces(self):
        if self.winnings_coords:
            for i in range(6):
                for j in range(7):
                    if (i, j) not in self.winnings_coords:
                        if self.board[i][j] == "O":
                            self.board[i][j] = "o"
                        elif self.board[i][j] == "X":
                            self.board[i][j] = "x"
                        else:
                            self.board[i][j] = "-"

    def get_score(self):
        def evaluate_segment(segm):
            if self.winner == "X":
                return 512
            elif self.winner == "O":
                return -512

            elif "O" in segm and "X" not in segm:
                if segm.count("O") == 3:
                    return -50
                elif segm.count("O") == 2:
                    return -10
                elif segm.count("O") == 1:
                    return -1
            elif segm.count("-") == 4:
                return 0
            elif "X" in segm and "O" not in segm:
                if segm.count("X") == 1:
                    return 1
                elif segm.count("X") == 2:
                    return 10
                elif segm.count("X") == 3:
                    return 50
            return 0

        self.score = 0
        for i in range(6):
            for j in range(4):
                if j + 3 < 7:
                    segment = [self.board[i][j + k] for k in range(4)]
                    self.score += evaluate_segment(segment)
        for i in range(4):
            for j in range(7):
                if i + 3 < 6:
                    segment = [self.board[i + k][j] for k in range(4)]
                    self.score += evaluate_segment(segment)
        for i in range(3):
            for j in range(4):
                if i + 3 < 6 and j + 3 < 7:
                    segment = [self.board[i + k][j + k] for k in range(4)]
                    self.score += evaluate_segment(segment)
        for i in range(3):
            for j in range(3, 7):
                if i + 3 < 6 and j - 3 >= 0:
                    segment = [self.board[i + k][j - k] for k in range(4)]
                    self.score += evaluate_segment(segment)

        return self.score

    def full_column(self, column):
        for i in range(6):
            if self.board[i][column] == "-":
                return False
        return True

    def move(self, column):
        if column < 0 or column > 6 or self.full_column(column):
            return False

        for i in range(5, -1, -1):
            if self.board[i][column] == "-":
                self.board[i][column] = self.turn
                self.played_moves += 1

                self.turn = "X" if self.turn == "O" else "O"

                self.last_move = column
                return True

    def game_over(self, clear_board=False):
        if self.game_over_flag:
            return True
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] != "-":
                    self.winner = self.board[i][j]
                    self.winnings_coords = [(i, j), (i, j + 1), (i, j + 2), (i, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i + 1][j] == self.board[i + 2][j] == self.board[i + 3][j] != "-":
                    self.winner = self.board[i][j]
                    self.winnings_coords = [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] != "-":
                    self.winner = self.board[i][j]
                    self.winnings_coords = [(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True
        for i in range(3, 6):
            for j in range(4):
                if self.board[i][j] == self.board[i - 1][j + 1] == self.board[i - 2][j + 2] == self.board[i - 3][j + 3] != "-":
                    self.winner = self.board[i][j]
                    self.winnings_coords = [(i, j), (i - 1, j + 1), (i - 2, j + 2), (i - 3, j + 3)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True
        if self.played_moves == 42:
            self.winner = "Draw"
            self.game_over_flag = True
            return True
        return False

    def __copy__(self):
        return Game(copy.deepcopy(self.board), self.algorithm, self.turn, self.score, self.played_moves,
                    self.winnings_coords, self.last_move, self.algorithm1, self.algorithm2)

    def __str__(self):
        board_string = ""
        count = 1
        for i in range(7):
            row = ""
            for j in range(7):
                if i != 6:
                    row += self.board[i][j]
                else:
                    row += str(count)
                    count += 1
            board_string += row + "\n"
        return board_string

    def draw_board(self):
        self.screen.fill((200, 200, 200))

        if self.shadow_column is not None:
            shadow_row = self.get_shadow_row(self.shadow_column)
            if shadow_row is not None:
                shadow_color = (255, 150, 150) if self.turn == "O" else (255, 255, 180)
                pygame.draw.circle(self.screen, shadow_color,
                                   (self.shadow_column * self.CELL_SIZE + self.CELL_SIZE // 2,
                                    (shadow_row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS)

        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                pygame.draw.circle(self.screen, (50, 50, 50),
                                   (col * self.CELL_SIZE + self.CELL_SIZE // 2, (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS)
                if self.board[row, col] == "O":
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                       (col * self.CELL_SIZE + self.CELL_SIZE // 2, (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                       self.RADIUS)
                elif self.board[row, col] == "X":
                    pygame.draw.circle(self.screen, (255, 255, 0),
                                       (col * self.CELL_SIZE + self.CELL_SIZE // 2, (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                       self.RADIUS)
        pygame.display.update()

    def run_game(self, mode):
        while self.running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEMOTION:
                    self.shadow_column = event.pos[0] // self.CELL_SIZE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // self.CELL_SIZE
                    if self.move(col):
                        if self.game_over():
                            print(f"Jogador {self.turn} venceu!")
                            self.running = False
                        elif self.is_draw():
                            print("Empate!")
                            self.running = False
                        self.switch_player()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run_game("human_vs_human")