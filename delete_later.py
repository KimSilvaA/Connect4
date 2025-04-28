import pygame
from pygame.locals import *
import sys
from board import Board 
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


# # =========== Main Game Functions =========== # # 
    def on_execute(self):
            '''
            game logic 
            '''
            depth = 4
            alpha = -math.inf
            beta = math.inf
            pygame.init()
            width = self.column_count * self.token_size
            height = (self.row_count + 1) * self.token_size
            self._display_surf = pygame.display.set_mode((width, height))

            board_arr=self.board.board 
            pygame.display.set_caption("Connect 4")


            while self.running:
                self.handle_events()  # Handle user input
                self.on_render()  # Render the game state
                
                # if computer's turn 
                if self.board.current_player != self.board.human:
                    pygame.time.delay(100) 
                    col, minimax_score = self.board.minimax(self.board.board, depth, alpha,beta, True)
                    
                    if self.board.check_valid_location(self.board.board, col):
                        row = self.board.next_open_row(self.board.board, col)
                        self.board.drop_piece(self.board.board, row, col, self.board.current_player)
                         # After the AI's move, check for a win or tie
                        if self.board.check_for_win(self.board.board, self.board.current_player):
                            #display a win message 
                            self.running = False  # End the game loop
                        elif self.board.is_tie(self.board.board):
                            #display a tie message
                            self.running = False  # End the game loop
                        else:
                            self.board.switch_player() 
                        
                    
                    



    def on_render(self):
        '''
        show whatever is happening 
        '''
        self._display_surf.fill((255, 255, 255))
        self.draw_board(self._display_surf)
        self.display_token()
        self.update_turn_message()
        self.display_turn()
        
        # self.show_turn() 
        pygame.display.flip()

# # =========== Drawing Functions =========== # # 
    def draw_board(self, screen):
        
        # Draw the blue board 
        pygame.draw.rect(
            screen,
            (0, 0, 255),  # Blue color
            (0,  # Upper left corner
            self.token_size,  # Upper right corner
            self.column_count * self.token_size,  # Width (basically makes all the columns)
            self.row_count * self.token_size)  # Height 
        )

        # Draw empty slots 
        for row in range(self.row_count):  
            for col in range(self.column_count):  
                piece = int(self.board.board[row][col])  # Get the value from the board grid, initialized to 0 
                pygame.draw.circle(
                    screen,  
                    self.colors[piece],  # set token color based on token 
                    (int(col * self.token_size + self.token_size / 2),  # X position
                    int((self.row_count - row - 1) * self.token_size + self.token_size / 2 + self.token_size)),  # Y position, defined as such so token goes to bottom
                    int(self.token_size/2 - 5) #radius 
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

    # # =========== Functions to handle input =========== # # 
        '''
        functions to handle mouse clicking, moving etc
        '''
    def handle_mouse_motion(self, pos):
        self.mouse_x, _ = pos
        self.mouse_column = self.mouse_x // self.token_size

     # Handle mouse click to drop a token
    def handle_mouse_click(self, pos):
        _, y = pos
        self.mouse_column = self.mouse_x // self.token_size
                    
    # # =========== Helper functions =========== # # 
        '''
        show turn, handle events, etc
        '''

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # When the mouse is moving, update the hover token position
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)
            
            # Handle click events if it's the user's turn
            if self.board.current_player == self.board.human:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
                    # Check if the clicked column is valid
                    if self.board.check_valid_location(self.board.board, self.mouse_column):
                        row = self.board.next_open_row(self.board.board, self.mouse_column)
                        self.board.drop_piece(self.board.board, row, self.mouse_column, 1)
                        self.show_hover_token=False #stop showing the token
                        self.board.switch_player() 
    
    
    def display_turn(self):
        text= self.font.render(self.message, True, (0, 0, 0)) 
        self._display_surf.blit(text, (self.token_size // 2, 0))

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

# # =========== Run Game =========== # #

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame
    board = Board()  # Create a Board instance
    ui = UI(board)  # Pass the board to the UI
    ui.on_execute()  # Start the game loop
    pygame.quit() 