import numpy as np
import math 
import random   

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
    
    
    
def negamax(self, board, depth, alpha, beta):
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
    
    value = -math.inf
    best_column = random.choice(valid_locations)

    for column in valid_locations:
        row = self.next_open_row(board, column)
        temp_board = np.copy(board)
        self.drop_piece(temp_board, row, column, self.comp)

        new_score = -self.negamax(temp_board, depth - 1, -beta, -alpha)[1]

        if new_score > value:
            value = new_score
            best_column = column

        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return best_column, value

class MCTS:
    def __init__(self, board, time_limit=3):
        self.board = board
        self.time_limit = time_limit