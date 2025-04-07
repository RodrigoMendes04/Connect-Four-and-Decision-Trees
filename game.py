import numpy as np
import pygame
import copy
import time
import algorithms

class Game:
    ROWS = 6
    COLUMNS = 7
    CELL_SIZE = 100
    WIDTH = COLUMNS * CELL_SIZE
    HEIGHT = (ROWS + 1) * CELL_SIZE
    RADIUS = CELL_SIZE // 2 - 5

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (73, 107, 171)
    YELLOW = (237, 175, 40)
    RED = (255, 36, 0)
    DARK_YELLOW = (148, 105, 13)
    DARK_RED = (94, 25, 20)

    def __init__(self, board=None, turn="O", score=0, played_moves=0,
                 winnings_coords=None, last_move=None, algorithm1=None, algorithm2=None):
        self.board = board if board is not None else np.full((self.ROWS, self.COLUMNS), "-")
        self.winner = None
        self.current_player = turn  # Added current_player attribute
        self.score = score
        self.played_moves = played_moves
        self.winnings_coords = winnings_coords
        self.last_move = last_move
        self.game_over_flag = False
        self.algorithm1 = algorithm1
        self.algorithm2 = algorithm2
        self.shadow_column = None
        self.running = True
        self.width= self.WIDTH

        # PyGame specific attributes (initialized when needed)
        self.screen = None
        self.font = None
        self.pygame_initialized = False

    def initialize_pygame(self):
        """Initialize PyGame components only when needed for GUI"""
        if not self.pygame_initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            self.font = pygame.font.SysFont("monospace", 50)
            self.pygame_initialized = True

    def clear_board_except_winning_pieces(self):
        """Clear the board except for winning pieces"""
        if self.winnings_coords:
            for i in range(self.ROWS):
                for j in range(self.COLUMNS):
                    if (i, j) not in self.winnings_coords:
                        if self.board[i][j] == "O":
                            self.board[i][j] = "-"
                        elif self.board[i][j] == "X":
                            self.board[i][j] = "-"

    def get_score(self):
        """Calculate the current board score"""
        def evaluate_segment(segment):
            if "O" in segment and "X" not in segment:
                count = segment.count("O")
                if count == 3: return -50
                elif count == 2: return -10
                elif count == 1: return -1
            elif "X" in segment and "O" not in segment:
                count = segment.count("X")
                if count == 1: return 1
                elif count == 2: return 10
                elif count == 3: return 50
            return 0

        self.score = 0
        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                segment = [self.board[row][col + i] for i in range(4)]
                self.score += evaluate_segment(segment)
        # Vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                segment = [self.board[row + i][col] for i in range(4)]
                self.score += evaluate_segment(segment)
        # Diagonal /
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                segment = [self.board[row + i][col + i] for i in range(4)]
                self.score += evaluate_segment(segment)
        # Diagonal \
        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                segment = [self.board[row - i][col + i] for i in range(4)]
                self.score += evaluate_segment(segment)

        return self.score

    def full_column(self, column):
        """Check if a column is full"""
        return self.board[0][column] != "-"

    def move(self, column):
        """Make a move in the specified column"""
        if column < 0 or column >= self.COLUMNS or self.full_column(column):
            return False

        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == "-":
                self.board[row][column] = self.current_player
                self.played_moves += 1
                self.last_move = column
                self.current_player = "X" if self.current_player == "O" else "O"
                return True
        return False

    def get_shadow_row(self, column):
        """Get the row where a piece would land in a column"""
        if column < 0 or column >= self.COLUMNS or self.full_column(column):
            return None
        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == "-":
                return row
        return None

    def game_over(self, clear_board=False):
        """Check if the game is over"""
        if self.game_over_flag:
            return True

        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLUMNS - 3):
                if (self.board[row][col] != "-" and
                        self.board[row][col] == self.board[row][col+1] ==
                        self.board[row][col+2] == self.board[row][col+3]):
                    self.winner = self.board[row][col]
                    self.winnings_coords = [(row, col+i) for i in range(4)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True

        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS):
                if (self.board[row][col] != "-" and
                        self.board[row][col] == self.board[row+1][col] ==
                        self.board[row+2][col] == self.board[row+3][col]):
                    self.winner = self.board[row][col]
                    self.winnings_coords = [(row+i, col) for i in range(4)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True

        # Check diagonal /
        for row in range(self.ROWS - 3):
            for col in range(self.COLUMNS - 3):
                if (self.board[row][col] != "-" and
                        self.board[row][col] == self.board[row+1][col+1] ==
                        self.board[row+2][col+2] == self.board[row+3][col+3]):
                    self.winner = self.board[row][col]
                    self.winnings_coords = [(row+i, col+i) for i in range(4)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True

        # Check diagonal \
        for row in range(3, self.ROWS):
            for col in range(self.COLUMNS - 3):
                if (self.board[row][col] != "-" and
                        self.board[row][col] == self.board[row-1][col+1] ==
                        self.board[row-2][col+2] == self.board[row-3][col+3]):
                    self.winner = self.board[row][col]
                    self.winnings_coords = [(row-i, col+i) for i in range(4)]
                    if clear_board:
                        self.clear_board_except_winning_pieces()
                    self.game_over_flag = True
                    return True

        # Check for draw
        if self.played_moves == self.ROWS * self.COLUMNS:
            self.winner = "Draw"
            self.game_over_flag = True
            return True

        return False


    def draw_board(self):
        """Draw the game board"""
        if not self.pygame_initialized:
            return

        self.screen.fill(self.BLUE)

        # Draw slots
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                pygame.draw.circle(self.screen, self.WHITE,
                                   (col * self.CELL_SIZE + self.CELL_SIZE // 2,
                                    (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS)

                # Draw pieces
                if self.board[row][col] == "O":
                    pygame.draw.circle(self.screen, self.YELLOW,
                                       (col * self.CELL_SIZE + self.CELL_SIZE // 2,
                                        (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                       self.RADIUS)
                elif self.board[row][col] == "X":
                    pygame.draw.circle(self.screen, self.RED,
                                       (col * self.CELL_SIZE + self.CELL_SIZE // 2,
                                        (row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                       self.RADIUS)

        # Draw hover piece
        if self.shadow_column is not None:
            shadow_row = self.get_shadow_row(self.shadow_column)
            if shadow_row is not None:
                color = self.YELLOW if self.current_player == "O" else self.RED
                pygame.draw.circle(self.screen, color,
                                   (self.shadow_column * self.CELL_SIZE + self.CELL_SIZE // 2,
                                    (shadow_row + 1) * self.CELL_SIZE + self.CELL_SIZE // 2),
                                   self.RADIUS)

        # Draw turn indicator
        turn_text = "Yellow's Turn" if self.current_player == "O" else "Red's Turn"
        if self.algorithm1 and self.current_player == "O":
            turn_text = f"{self.algorithm1}'s Turn"
        elif self.algorithm2 and self.current_player == "X":
            turn_text = f"{self.algorithm2}'s Turn"

        label = self.font.render(turn_text, 1, self.WHITE)
        self.screen.blit(label, (10, 10))

        pygame.display.update()

    def run_game(self):
        """Main game loop for PyGame interface"""
        self.initialize_pygame()
        clock = pygame.time.Clock()
        ai_turn = False

        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Human player move
                if not self.algorithm1 and self.current_player == "O" or not self.algorithm2 and self.current_player == "X":
                    if event.type == pygame.MOUSEMOTION:
                        self.shadow_column = event.pos[0] // self.CELL_SIZE
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        column = event.pos[0] // self.CELL_SIZE
                        if self.move(column):
                            self.shadow_column = None
                else:
                    # AI's turn
                    ai_turn = True

            # AI move
            if ai_turn and not self.game_over():
                current_algorithm = self.algorithm1 if self.current_player == "O" else self.algorithm2
                if current_algorithm:
                    column = algorithms.move(self, current_algorithm)
                    if column is not None:
                        self.move(column)
                    time.sleep(0.5)  # Small delay for visualization
                ai_turn = False

            # Draw the board
            self.draw_board()

            # Check for game over
            if self.game_over():
                if self.winner == "Draw":
                    result_text = "Game Over - Draw!"
                else:
                    winner_name = "Yellow" if self.winner == "O" else "Red"
                    if self.algorithm1 and self.winner == "O":
                        winner_name = self.algorithm1
                    elif self.algorithm2 and self.winner == "X":
                        winner_name = self.algorithm2
                    result_text = f"{winner_name} wins!"

                # Display result for 3 seconds
                result_label = self.font.render(result_text, 1, self.WHITE)
                self.screen.blit(result_label, (self.WIDTH//2 - result_label.get_width()//2,
                                                self.HEIGHT//2 - result_label.get_height()//2))
                pygame.display.update()
                time.sleep(3)
                self.running = False

            clock.tick(30)

        pygame.quit()

    def get_possible_moves(self):
        """Get all valid moves"""
        return [col for col in range(self.COLUMNS) if not self.full_column(col)]

    def make_copy(self):
        """Create a deep copy of the game state without pygame objects"""
        new_game = Game(
            board=copy.deepcopy(self.board),
            turn=self.current_player,  # Ensure current_player is copied
            score=self.score,
            played_moves=self.played_moves,
            winnings_coords=copy.deepcopy(self.winnings_coords) if self.winnings_coords else None,
            last_move=self.last_move,
            algorithm1=self.algorithm1,
            algorithm2=self.algorithm2
        )
        new_game.game_over_flag = self.game_over_flag
        return new_game

    def make_move(self, column):
        """Make a move (used by AI algorithms)"""
        if column < 0 or column >= self.COLUMNS or self.full_column(column):
            return False

        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == "-":
                self.board[row][column] = self.current_player
                self.played_moves += 1
                self.last_move = column
                self.current_player = "X" if self.current_player == "O" else "O"
                return True
        return False

    def __copy__(self):
        """Copy support"""
        return self.make_copy()

    def __str__(self):
        """String representation for terminal display"""
        board_str = ""
        for row in self.board:
            board_str += " ".join(row) + "\n"
        board_str += "-" * (self.COLUMNS * 2 - 1) + "\n"
        board_str += " ".join(str(i) for i in range(1, self.COLUMNS + 1)) + "\n"
        return board_str
