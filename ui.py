import pygame
from pygame.locals import *
import sys
from board import Board
# from board import Board,MCTSNode, mcts_search
import math 
import numpy as np

'''
layout of file:
1. on_execute
2. on_render 
3. drawing functions (board, token)
4. event handling (handle_events, handle_mouse_motion)
5. game logic (handle_mouse_click, show_turn)
'''

class UI:

    def __init__(self,board):
        #initialize board
        self.board = board
        self.row_count = self.board.row_count
        self.column_count = self.board.column_count

        #initialize pygame features 
        self.running=True
        self.token_size = 100 # best size (less than 50 the window is too small and greater than 100 you can't see all of the  board
        self.show_hover_token = True

        #pygame.time.Clock()
        self._display_surf = None
        self._clock = None 
        self.player_pieces = {1: 'red', 2: 'yellow'}  
        self.colors = {
            0: (255, 255, 255), # white - empty slot
            1: (255, 0, 0),     # red player 1
            2: (255, 255, 0)    # yellow player 2
        }
        #initialize mouse position 
        self.mouse_x = 0 #initialize so you don't get an error later 
        self.mouse_column=0 #same,initialize so you don't get an error later

        # initialize font and text 
        self.font = pygame.font.SysFont(None, 36)
        self.message = "" 
        self.winner_message = ""

        # self.hint_column = None
        # self.hint_button_rect = pygame.Rect(20, 20, 100, 40) 

        #screen: board on left hint button on right 
        screen_width = self.column_count * self.token_size + 1000  # Add extra space for hint button
        screen_height = self.row_count * self.token_size  # Keep the board height the same
        self._display_surf = pygame.display.set_mode((screen_width, screen_height))

            
        # hint_button_width = 100  # Width of the hint button
        # hint_button_height = 50  # Height of the hint button
        # hint_button_x = self.column_count * self.token_size -10  # Positioned in the white space
        # hint_button_y=10

        # self.hint_button_rect = pygame.Rect(hint_button_x, hint_button_y, hint_button_width, hint_button_height)

# # =========== Main Game Functions =========== # # 
    def on_execute(self):
        '''
        Game logic 
        '''
        depth = 3
        alpha = -math.inf
        beta = math.inf
        pygame.init()
        hint_button_space = 0 
        # hint_button_space = 100  # Additional space on the right for the hint button
        width = self.column_count * self.token_size + hint_button_space  # Add space for the hint button
        height = (self.row_count + 1) * self.token_size
        self._display_surf = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Connect 4")

        while self.running:
            self.handle_events()  # Handle user input
            self.on_render()  # Render the game state

            # If it's the computer's turn
            if self.board.current_player != self.board.human:
                pygame.time.delay(200) 
                col, _ = self.board.minimax(self.board.board, depth, alpha, beta, True)

                if self.board.check_valid_location(self.board.board, col):
                    row = self.board.next_open_row(self.board.board, col)
                    self.board.drop_piece(self.board.board, row, col, self.board.current_player)
                    self.on_render()  # Render after the computer's move
                    pygame.display.flip()  # Update display

                    # After the AI's move, check for a win or tie
                    if self.board.check_for_win(self.board.board, self.board.current_player):
                        # Display a win message 
                        self.winner_message = "Computer wins!"
                        self.running = False  # End the game loop
                        pygame.time.delay(500)
                        print("Computer wins!")
                    elif self.board.is_tie(self.board.board):
                        self.winner_message = "It's a tie!"
                        self.running = False  # End the game loop
                    else:
                        self.board.switch_player()  # Switch to the other player

        # Once the game ends, display the winner message
        if self.winner_message:
            self.on_render()  # Render the winner message after the game ends
            pygame.display.flip()  # Ensure the screen updates to show the winner message
            pygame.time.delay(5000)
    
    def on_render(self):
        '''
        show whatever is happening 
        '''
        self._display_surf.fill((255, 255, 255))
        self.draw_board(self._display_surf)
        # self.draw_hint_button(self._display_surf)  # Draw the hint button
        self.display_token()
        self.update_turn_message()
        self.display_turn()
        if self.winner_message:
            self.display_winner()
        pygame.display.flip()

# # =========== Drawing Functions =========== # # 
    def draw_board(self, screen):
        # hint_button_space = 200  # Space for the hint button on the right
        board_width = self.column_count * self.token_size
        board_height = self.row_count * self.token_size

        # Draw the blue board
        pygame.draw.rect(
            screen,
            (0, 0, 255),  # Blue color
            (0,  # Upper left corner X
            self.token_size,  # Upper left corner Y
            board_width,  # Adjusted width for the board
            board_height)  # Height remains unchanged
        )

        # Draw empty slots
        for row in range(self.row_count):
            for col in range(self.column_count):
                piece = int(self.board.board[row][col])  # Get the value from the board grid
                pygame.draw.circle(
                    screen,
                    self.colors[piece],  # Token color based on value
                    (int(col * self.token_size + self.token_size / 2),  # X position
                    int((self.row_count - row - 1) * self.token_size + self.token_size / 2 + self.token_size)),  # Y position
                    int(self.token_size / 2 - 5)  # Radius
                )

    def draw_token(self, column):
        color = (255, 0, 0) if self.board.current_player == 1 else (255, 255, 0)

        # Calculate the x-position where the token will hover above (centered over the column)
        token_x = column * self.token_size + self.token_size // 2  
        
        # Adjust token_y to position the token just above the first row
        token_y = self.token_size // 2  # Position just above the board

        # Draw the hovering token with a slightly larger radius for visibility
        pygame.draw.circle(
            self._display_surf,  # Surface to draw on (the screen)
            color,  # Token color (based on player)
            (token_x, token_y),  # Token position (x and y)
            int(self.token_size / 2 - 5)  # Radius of the token (circle size)
        )
    

    # def draw_hint_button(self, screen):
    #     pygame.draw.rect(screen, (200, 200, 200), self.hint_button_rect)  # Light grey
    #     pygame.draw.rect(screen, (100, 100, 100), self.hint_button_rect, 2)  # Border
    #     text = self.font.render("Hint", True, (0, 0, 0))
    #     text_rect = text.get_rect(center=self.hint_button_rect.center)
    #     screen.blit(text, text_rect)


    # # =========== Functions to handle input =========== # # 
        '''
        functions to handle mouse clicking, moving etc
        '''
    # def handle_mouse_motion(self, pos):
    #     self.mouse_x, _ = pos
    #     self.mouse_column = self.mouse_x // self.token_size

    def handle_mouse_motion(self, pos):
        self.mouse_x, _ = pos
        hint_button_space = 200  # Space reserved for the hint button
        board_width = self.column_count * self.token_size  # Width of the board

        # Check if the mouse is within the board's width
        if self.mouse_x < board_width:
            self.mouse_column = self.mouse_x // self.token_size
            self.show_hover_token = True  # Show the token
        else:
            self.show_hover_token = False  # Hide the token

     # Handle mouse click to drop a token
    def handle_mouse_click(self, pos):
        x, y = pos
        # if self.hint_button_rect.collidepoint(x,y):
        #     self.show_hint()
        #     return 
        self.mouse_column = self.mouse_x // self.token_size



                    
    # # =========== Helper functions =========== # # 
        '''
        show turn, handle events, etc
        '''



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)

            if self.board.current_player == self.board.human:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)

                    if self.board.check_valid_location(self.board.board, self.mouse_column):
                        row = self.board.next_open_row(self.board.board, self.mouse_column)
                        self.board.drop_piece(self.board.board, row, self.mouse_column, self.board.current_player)
                        self.show_hover_token = False  # Hide token preview

                        self.on_render()
                        pygame.display.update()

                        if self.board.check_for_win(self.board.board, self.board.current_player):
                            self.winner_message = "You win!"
                            # self.display_winner()
                            self.running = False
                        elif self.board.is_tie(self.board.board):
                            self.winner_message = "It's a tie!"
                            # self.display_winner()
                            self.running = False
                        else:
                            self.board.switch_player()


    
    
    def display_turn(self):
        text= self.font.render(self.message, True, (0, 0, 0)) 
        self._display_surf.blit(text, (self.token_size // 2, 0))
    
    def display_winner(self):
        text = self.font.render(self.winner_message, True, (255, 0, 0)) 
        text_rect = text.get_rect(center=(self._display_surf.get_width() // 2, text.get_height() // 2 + 10))
        self._display_surf.blit(text, text_rect)

    def update_turn_message(self):
        if self.board.current_player == self.board.human:
            self.message = "Your turn"
        else:
            self.message = "Computer's turn"
    
    def display_token(self):
        ''' 
        function to display the hovering token if it's player's turn 
        '''
        if self.show_hover_token:
            if self.board.current_player == self.board.human:
                self.draw_token(self.mouse_column)
    
    # def show_hint(self):
    #     '''
    #     function to show hint for the player 
    #     '''
    #     if self.board.current_player == self.board.human:
    #         # Use MCTS to find the best move
    #         best_move = mcts_search(self.board, 1000)
            

        


    

# # =========== Run Game =========== # #

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame
    board = Board()  # Create a Board instance
    ui = UI(board)  # Pass the board to the UI
    ui.on_execute()  # Start the game loop
    pygame.quit() 