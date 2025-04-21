import numpy as np
import copy 
import random
import math

class Board:
    def __init__(self):
        self.row_count=6
        self.column_count=7
        self.board = self.create_board()
        self.players = [1, 2]
        self.human=random.choice(self.players)
        self.comp= 2 if self.human==1 else 1
        self.current_player = 1  # Player 1 starts
        self.winner = None
        self.tie = False
    
    def create_board(self):
        return np.zeros((self.row_count, self.column_count), dtype=int)

    def reset_board(self):
        pass

    def print_board(self):
        print(np.flip(self.board, 0))

    def check_valid_location(self,board, column):
        # return board[0][column] == 0  # check top row
        return board[0, column] == 0

    def next_open_row(self,board, column):
        for r in range(self.row_count):
            if board[r][column] == 0:
                return r
        return None # if no open row is found 

    def drop_piece(self, row, column, piece):
        self.board[row][column] = piece

    def switch_player(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def check_for_win(self,board, piece):
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if all(board[r][c+i] == piece for i in range(4)):
                    return True

        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if all(board[r+i][c] == piece for i in range(4)):
                    return True

        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if all(board[r+i][c+i] == piece for i in range(4)):
                    return True

        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if all(board[r-i][c+i] == piece for i in range(4)):
                    return True

        return False

    def is_tie(self,board):
        return np.all(board != 0)
    
    def copy_board(self):
        return copy.deepcopy(self.board)
    
    def player_turn(self):
        #checks if it's the user's turn 
        return self.current_player == self.human
            
    def get_valid_locations(self, board):
        valid_locations = []
        for column in range(self.column_count):
            if self.check_valid_location(board, column):
                valid_locations.append(column)
        return valid_locations


    def score_position(self, board, piece):
        score = 0
        center_column = [int(i) for i in list(board[:, self.column_count // 2])]
        center_count = center_column.count(piece)
        score += center_count * 3
        return score


    #will move minimax func to ai.py but now it is here
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.check_for_win(board, 1) or self.check_for_win(board, 2) or self.is_tie(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_for_win(board, 2):  # AI wins
                    return (None, 1000000)
                elif self.check_for_win(board, 1):  # Human wins
                    return (None, -1000000)
                else:
                    return (None, 0)  # Tie
            else:
                return (None, self.score_position(board, 2))  # Heuristic score

        if maximizingPlayer:
            value = -math.inf
            best_column = random.choice(valid_locations)
            for column in valid_locations:
                row = self.next_open_row(board, column)
                temp_board = copy.deepcopy(board)  # deepcopy to avoid modifying the original
                self.drop_piece(temp_board, row, column, 2)  # 2 = AI
                new_score = self.minimax(temp_board, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_column = column
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff
            return best_column, value

        else:
            value = math.inf
            best_column = random.choice(valid_locations)
            for column in valid_locations:
                row = self.next_open_row(board, column)
                temp_board = copy.deepcopy(board)
                self.drop_piece(temp_board, row, column, 1)  # 1 = Human
                new_score = self.minimax(temp_board, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_column = column
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff
            return best_column, value


#====try running the game====#
def play_game():
    depth=0
    alpha=-math.inf
    beta=math.inf
    game= Board()
    game_over=False

    while not game_over:
        game.print_board()
        #if person's turn
        if game.player_turn():
            col = int(input("Player 1 Make your Selection (0-6):"))
            row = game.next_open_row(game.board,col)
            game.drop_piece(row, col, game.current_player)

            if game.check_for_win(game.board,game.current_player):
                print("Human wins!")
                game_over = True
            elif game.is_tie(game.board):
                print("It's a tie!")
                game_over = True
            else:
                game.switch_player()

        else:
            print("AI is thinking... ._.")
            col, minimax_score = game.minimax(game.board,depth, alpha, beta, True)
            print(col)
       
            if game.check_valid_location(game.board,col):
                row = game.next_open_row(game.board,col)
                game.drop_piece(row, col, game.current_player)

        #         if game.check_for_win(game.board,game.current_player):
        #             print("Computer wins!")
        #             game_over = True

        #         elif game.is_tie(game.board):
        #             print("It's a tie!")
        #             game_over = True
        #         else:
        #             game.switch_player()
        # game.print_board()

#======end of connect4 game=====#

if __name__ == "__main__":
    play_game()

# game= Board()
# game.create_board()
# col=3
# game.check_valid_location(game.board, col)
# row= game.next_open_row(game.board, col)
# print(row)
# game.drop_piece(row, col, game.current_player)
# row= game.next_open_row(game.board, col)
# print(row)