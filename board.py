import numpy as np
import copy 
import random
import math

class Board:
    def __init__(self):
        self.row_count = 6
        self.column_count = 7
        self.board = self.create_board()
        self.players = [1, 2]
        self.human = random.choice(self.players)
        self.comp = 2 if self.human == 1 else 1
        self.current_player = 1
        self.winner = None
        self.tie = False

    def create_board(self):
        return np.zeros((self.row_count, self.column_count), dtype=int)

    def print_board(self, board):
        print(np.flip(board, 0))

    # def check_valid_location(self, board, column):
    #     return board[0, column] == 0
    
    def check_valid_location(self, board, column):
        return board[self.row_count - 1][column] == 0

    def next_open_row(self, board, column):
        for r in range(self.row_count):
            if board[r][column] == 0:
                return r
        return None

    def drop_piece(self, board, row, column, piece):
        board[row][column] = piece

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_for_win(self, board, piece):
        # Horizontal
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if all(board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if all(board[r + i][c] == piece for i in range(4)):
                    return True

        # Positive diagonal
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if all(board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Negative diagonal
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if all(board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_tie(self, board):
        return np.all(board != 0)

    def player_turn(self):
        return self.current_player == self.human

    def get_valid_locations(self, board):
        return [col for col in range(self.column_count) if self.check_valid_location(board, col)]

    def score_position(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, self.column_count // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        for r in range(self.row_count):
            row_array = list(board[r, :])
            for c in range(self.column_count - 3):
                window = row_array[c:c + 4]
                score += self.evaluate_window(window, piece)

        for c in range(self.column_count):
            col_array = list(board[:, c])
            for r in range(self.row_count - 3):
                window = col_array[r:r + 4]
                score += self.evaluate_window(window, piece)

        for r in range(self.row_count - 3):
            for c in range(self.column_count - 3):
                window = [board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(3, self.row_count):
            for c in range(self.column_count - 3):
                window = [board[r - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.check_for_win(board, 1) or self.check_for_win(board, 2) or self.is_tie(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_for_win(board, self.comp):
                    return (None, 1000000)
                elif self.check_for_win(board, self.human):
                    return (None, -1000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, self.comp))

        if maximizingPlayer:
            value = -math.inf
            best_column = random.choice(valid_locations)
            for column in valid_locations:
                row = self.next_open_row(board, column)
                temp_board = np.copy(board)
                self.drop_piece(temp_board, row, column, self.comp)
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_column = column
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_column, value

        else:
            value = math.inf
            best_column = random.choice(valid_locations)
            for column in valid_locations:
                row = self.next_open_row(board, column)
                temp_board = board.copy()
                self.drop_piece(temp_board, row, column, self.human)
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_column = column
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_column, value


#==== Main Game Loop ====#
def play_game():
    depth = 4
    alpha = -math.inf
    beta = math.inf
    game = Board()
    game_over = False

    while not game_over:
        game.print_board(game.board)

        if game.player_turn():
            try:
                col = int(input("Player 1 Make your Selection (0-6): "))
                if col not in range(game.column_count) or not game.check_valid_location(game.board, col):
                    print(game.check_valid_location(game.board, col))
                    print("check_valid_location is giving False") 
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Please enter a number between 0 and 6.")
                continue

            row = game.next_open_row(game.board, col)
            game.drop_piece(game.board, row, col, game.current_player)

            if game.check_for_win(game.board, game.current_player):
                game.print_board(game.board)
                print("Human wins!")
                game_over = True
            elif game.is_tie(game.board):
                game.print_board(game.board)
                print("It's a tie!")
                game_over = True
            else:
                game.switch_player()
        else:
            print("AI is thinking... ._.")
            col, minimax_score = game.minimax(game.board, depth, alpha, beta, True)
            print(f"AI selects column {col}")
            if game.check_valid_location(game.board, col):
                row = game.next_open_row(game.board, col)
                game.drop_piece(game.board, row, col, game.current_player)

                if game.check_for_win(game.board, game.current_player):
                    game.print_board(game.board)
                    print("Computer wins!")
                    game_over = True
                elif game.is_tie(game.board):
                    game.print_board(game.board)
                    print("It's a tie!")
                    game_over = True
                else:
                    game.switch_player()


if __name__ == "__main__":
    play_game()
