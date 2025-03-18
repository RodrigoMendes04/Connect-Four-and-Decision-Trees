import numpy as np
import copy

class Game:
    ROWS = 6
    COLUMNS = 7
    CELL_SIZE = 3

    def __init__(self, board=None, turn="O", score=0, played_moves=0,
                 winnings_coords=None, last_move=None):
        self.board = board if board is not None else np.full((self.ROWS, self.COLUMNS), "-")
        self.winner = None
        self.turn = turn
        self.score = score
        self.played_moves = played_moves
        self.winnings_coords = winnings_coords
        self.last_move = last_move
        self.game_over_flag = False

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
        return Game(copy.deepcopy(self.board), self.turn, self.score, self.played_moves,
                    self.winnings_coords, self.last_move)

    def __str__(self):
        board_string = ""
        count = 1
        for i in range(6):
            row = ""
            for j in range(7):
                if i != 6:
                    row += self.board[i][j]
                else:
                    row += str(count)
                    count += 1
            board_string += row + "\n"
        return board_string

    def print_board(self):
        print("\n")
        print("-" * (self.COLUMNS * 2 + 1))
        for row in self.board:
            print("|", " | ".join(row), "|")
        print("-" * (self.COLUMNS * 2 + 1))

    def run_game(self, mode):
        while not self.game_over():
            self.print_board()
            print(f"Turno do jogador: {self.turn}")
            try:
                col = int(input(f"Escolha uma coluna (0-6): "))
                if not self.move(col):
                    print("Movimento inválido. Tente novamente.")
            except ValueError:
                print("Por favor, insira um número entre 0 e 6.")

        self.print_board()
        if self.winner == "Draw":
            print("Empate!")
        else:
            print(f"Jogador {self.winner} venceu!")


if __name__ == "__main__":
    game = Game()
    game.run_game("human_vs_human")
