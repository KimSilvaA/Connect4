import numpy as np
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

    def negamax(self, board, depth, alpha, beta, color):
        comp = 1 if self.human == 2 else 2  #need to define comp only for negamax so it's defined here and not under __init__ 

        valid_locations = self.get_valid_locations(board)
        is_terminal = self.check_for_win(board, comp) or self.check_for_win(board, self.human) or self.is_tie(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_for_win(board, comp):
                    return (None, color * 1000000)
                elif self.check_for_win(board, self.human):
                    return (None, color * -1000000)
                else:
                    return (None, 0)
            else:
                return (None, color * self.score_position(board, comp))

        value = -math.inf
        best_column = random.choice(valid_locations)

        for column in valid_locations:
            row = self.next_open_row(board, column)
            temp_board = np.copy(board)
            piece = comp if color == 1 else self.human
            self.drop_piece(temp_board, row, column, piece)

            new_score = -self.negamax(temp_board, depth - 1, -beta, -alpha, -color)[1]

            if new_score > value:
                value = new_score
                best_column = column

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return best_column, value

class MCTSNode:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent #the previous state that led to the current state
        self.children = [] #all possible future game states from current state
        self.wins = 0 #counts winning result of a simulation 
        self.visits = 0 #counts number of times a node has been visited
        self.unexplored_moves = self.board.get_valid_locations(self.board.board) 
        
    def print_board(self):
        self.board.print_board(self.board.board) #defined again in MCTSNode or else using it is confsing and wordy 


    def is_fully_expanded(self):
        return len(self.unexplored_moves)==0 #see if all valid locations are explored, no unexplored moves means everything has been explored. 
    
    def expand(self):
        '''
        explore a new move, add it to children and returns new child node 
        '''
        col = self.unexplored_moves.pop()  # Get a column to explore, remove from unexplored moves since you'll explore it 
        #copy the current board's state 
        new_board_array = np.copy(self.board.board) #this is the numpy board 
        # create new board with the copied array state
        new_board = Board() 
        new_board.board = new_board_array  
        new_board.current_player = self.board.current_player  # define this so the new board knows whose turn it is 
        
        # drop piece in new board 
        row = new_board.next_open_row(new_board.board, col)  # Find the open row for the move
        new_board.drop_piece(new_board.board, row, col, new_board.current_player)  # Drop the piece
        new_board.switch_player()
        self.children.append(MCTSNode(new_board, self))  # Add the new board as a child node
        return self.children[-1]  # Return the new child node
    

    def simulate(self):
        '''
        run a simulation from the current node to the end of the game
        returns result of simulation 
        '''

        new_board_array = np.copy(self.board.board)
        new_board = Board()
        new_board.board = new_board_array
        new_board.current_player = self.board.current_player  # Set the current player for the new board
        starting_player = new_board.current_player  # Store the starting player to get the results later 
        #go down the tree until the end 
        is_terminal=new_board.check_for_win(new_board.board, new_board.current_player) or new_board.is_tie(new_board.board)
        while not is_terminal:
            valid_locations= new_board.get_valid_locations(new_board.board)
            best_column = random.choice(valid_locations) 
            row = new_board.next_open_row(new_board.board, best_column)
            new_board.drop_piece(new_board.board, row, best_column, new_board.current_player)
            new_board.switch_player()
            is_terminal=new_board.check_for_win(new_board.board, new_board.current_player) or new_board.is_tie(new_board.board)
        #results 
        if new_board.check_for_win(new_board.board, new_board.current_player) and new_board.current_player == starting_player:
            result=1 #player who started in the simulation wins
        elif new_board.is_tie(new_board.board):
            result=0 #tie no one wins
        else:
            result=-1 #player who started loses 
        return result 
     
    
    def backpropagation(self,node,result):
        '''
        backpropagation step of MCTS, update the node's win and visit counts
        '''
        node=self 
        while node is not None:
            node.visits+=1
            node.wins+=result
            result=-result #reverse the result because in each turn the player changes 
            node=node.parent #go from child to parent node 
    
    def best_child(self):
        '''
        returns child node with highest wins per visit ratio 
        '''
        best_child=None
        best_ratio=-math.inf
        for child in self.children:
            if child.visits>0:
                ratio=child.wins/child.visits
                if ratio>best_ratio:
                    best_ratio=ratio
                    best_child=child
        return best_child  
    
    def select(self):
        '''
        Selects a child node to explore.
        Uses a combination of win/visit ratio and exploration bonus.
        '''
        best_child = None
        best_ratio = -math.inf
        for child in self.children:
            if child.visits > 0:
                ratio = child.wins / child.visits 
            else:
                return child  # Prefer unvisited nodes immediately
            if ratio > best_ratio:
                best_ratio = ratio
                best_child = child
        return best_child


def mcts_search(board, max_iterations=100):
    """
    Runs the Monte Carlo Tree Search (MCTS) to determine the best column for the AI to play.
    The result is the column that the AI should play.
    """
    root = MCTSNode(board)

    for _ in range(max_iterations):
        node = root
        while node.is_fully_expanded() and node.children:
            node = max(
                node.children,
                key=lambda child: child.wins / child.visits + math.sqrt(2 * math.log(node.visits) / child.visits)
            )

        # expansion: expand the node if explored
        if not node.is_fully_expanded():
            node = node.expand()
        #simulate game
        result = node.simulate()
        # update node
        node.backpropagation(node, result)
    # Choose based on num of visits
    best_child = max(root.children, key=lambda child: child.visits)
    #finds column that changed from last time 
    for col in range(board.column_count):
        if not (board.board[:, col] == best_child.board.board[:, col]).all():
            return col

#==== Test MCTS ====#
# test_board=Board()
# test_node=MCTSNode(test_board)
# a=test_node.simulate()
# print(a)
# col=mcts_search(test_board, max_iterations=1000)
# print(col)







#==== Main Game Loop ====#
# uncomment me for a text-based game! 
        
# def play_game():
#     depth = 4
#     alpha = -math.inf
#     beta = math.inf
#     game = Board()
#     game_over = False

#     while not game_over:
#         game.print_board(game.board)

#         if game.player_turn():
#             try:
#                 col = int(input("Player 1 Make your Selection (0-6): "))
#                 if col not in range(game.column_count) or not game.check_valid_location(game.board, col):
#                     print(game.check_valid_location(game.board, col))
#                     print("check_valid_location is giving False") 
#                     print("Invalid move. Try again.")
#                     continue
#             except ValueError:
#                 print("Please enter a number between 0 and 6.")
#                 continue

#             row = game.next_open_row(game.board, col)
#             game.drop_piece(game.board, row, col, game.current_player)

#             if game.check_for_win(game.board, game.current_player):
#                 game.print_board(game.board)
#                 print("Human wins!")
#                 game_over = True
#             elif game.is_tie(game.board):
#                 game.print_board(game.board)
#                 print("It's a tie!")
#                 game_over = True
#             else:
#                 game.switch_player()
#         else:
#             print("AI is thinking... ._.")
#             col, _ = game.minimax(game.board, depth, alpha, beta, True)
#             print(f"AI selects column {col}")
#             if game.check_valid_location(game.board, col):
#                 row = game.next_open_row(game.board, col)
#                 game.drop_piece(game.board, row, col, game.current_player)

#                 if game.check_for_win(game.board, game.current_player):
#                     game.print_board(game.board)
#                     print("Computer wins!")
#                     game_over = True
#                 elif game.is_tie(game.board):
#                     game.print_board(game.board)
#                     print("It's a tie!")
#                     game_over = True
#                 else:
#                     game.switch_player()


# if __name__ == "__main__":
#     play_game()
