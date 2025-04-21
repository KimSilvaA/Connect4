import pygame
from pygame.locals import *
import sys
from board import Board 

class UI:
    def __init__(self,board):
        self.token_size = 100
        self.board = board
        self.row_count = self.board.row_count
        self.column_count = self.board.column_count
        self._display_surf = None
        self._clock = None
        #pygame.time.Clock()
        self.running=True 
        self.player_pieces = {1: 'red', 2: 'yellow'}  
        self.colors = {
            0: (255, 255, 255), # empty slot
            1: (255, 0, 0),     # red
            2: (255, 255, 0)    # yellow
        }
        self.mouse_x = 0
        self.mouse_column=0

    # =========== pygame =========== #
    def draw_board(self, screen):
        
        # Draw blue board (background)
        pygame.draw.rect(
            screen,
            (0, 0, 255),  # Blue color
            (0,  # Upper left corner
            self.token_size,  # Upper right corner
            self.column_count * self.token_size,  # Width of the board (column_count * token_size)
            self.row_count * self.token_size)  # Height of the board (row_count * token_size)
        )

        # Draw empty slots (cells)
        for row in range(self.row_count):  # Access row_count from the local variable
            for col in range(self.column_count):  # Access column_count from the local variable
                piece = int(self.board.board[row][col])  # Get the value from the board grid
                pygame.draw.circle(
                    screen,  # The surface to draw on (the screen)
                    self.colors[piece],  # Color based on the piece value (using self.colors)
                    (int(col * self.token_size + self.token_size / 2),  # X position
                    int(row * self.token_size + self.token_size / 2 + self.token_size)),  # Y position
                    int(self.token_size / 2 - 5)  # Radius (circle size)
                )
    #show who's turn it is on screen
    def show_turn(self):
        font = pygame.font.SysFont("monospace", 36)
        player="Your turn" if self.board.current_player == self.board.human else "Computer's turn"

        label = font.render(f"{player}", 0, (0, 0, 0))
        self._display_surf.blit(label, (self.token_size//2,0))


    # handle user input events
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

    def token(self, mouse_x, column):
        # Set color based on the current player (red for player 1, yellow for player 2)
        color = (255, 0, 0) if self.board.current_player == 1 else (255, 255, 0)

        # Calculate the x-position where the token will hover above (centered over the column)
        token_x = column * self.token_size + self.token_size // 2  # center of the column
        token_y = self.token_size // 2  # Just above the board

        # Draw the hovering token on the display surface
        pygame.draw.circle(
            self._display_surf,  # Surface to draw on (the screen)
            color,  # Token color (based on player)
            (token_x, token_y),  # Token position (x and y)
            int(self.token_size / 2 - 5)  # Radius of the token (circle size)
        )
    
    # Handle mouse motion to update the token position
    def handle_mouse_motion(self, pos):
        self.mouse_x, _ = pos
        self.mouse_column = self.mouse_x // self.token_size

    # Handle mouse click to drop a token
    def handle_mouse_click(self, pos):
        _, y = pos
        self.mouse_column = self.mouse_x // self.token_size
        if self.board.check_valid_location(self.mouse_column):
            row = self.board.next_open_row(self.mouse_column)
            self.board.drop_piece(row, self.mouse_column, self.board.current_player)
            if self.board.check_for_win(self.board.current_player):
                print(f"Player {self.board.current_player} wins!")
                self.running = False
            elif self.board.is_tie():
                print("It's a tie!")
                self.running = False
            else:
                # Switch to the other player
                self.board.current_player = 2 if self.board.current_player == 1 else 1
             
    def on_render(self):
            self._display_surf.fill((255, 255, 255))
            self.draw_board(self._display_surf)
    
            if self.board.current_player==self.board.human:
                #draw hovering token
                self.token(self.mouse_x, self.mouse_column)
            
            self.show_turn() 
            pygame.display.flip()
            

    def on_execute(self):
        pygame.init()
        width = self.column_count * self.token_size
        height = (self.row_count + 1) * self.token_size
        self._display_surf = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Connect 4")

        while self.running:
            self.handle_events()  # Handle user input
            self.on_render()  # Render the screen with updates
        pygame.quit()
        

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame
    board = Board()  # Create a Board instance
    ui = UI(board)  # Pass the board to the UI
    ui.on_execute()  # Start the game loop
    pygame.quit() 

