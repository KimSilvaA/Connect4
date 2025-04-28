import pygame
from pygame.locals import *
import sys

class Connect4:







    def ask_for_name(self):
        name = input("Enter your name: ")
        return name  

    # =========== Board Constants =========== #
    row_count = 6
    column_count = 7
    token_size = 100

    def __init__(self):
        self.running = True
        self._display_surf = None
        self._clock = None #will put a timer later 

        
        self.player_pieces = {1: 'red', 2: 'yellow'}  
        self.colors = {
            0: (255, 255, 255), # empty slot
            1: (255, 0, 0),     # red
            2: (255, 255, 0)    # yellow
        }

    
    # =========== pygame =========== #
    def draw_board(self, screen):
        #draw blue board 
        pygame.draw.rect(
            screen,
            (0, 0, 255), 
            (0, #upper left 
             self.token_size, #upper right
             self.column_count * self.token_size, 
             self.row_count * self.token_size)
        )
        #draw empty slots
        for row in range(self.row_count):
            for col in range(self.column_count):
                piece = int(self.board[row][col])  # Define 'piece' as an integer
                pygame.draw.circle(
                    screen,  # The surface to draw on (the screen)
                    self.colors[piece],  # Color based on the piece value
                    (int(col * self.token_size + self.token_size / 2),  # X position
                    int(row * self.token_size + self.token_size + self.token_size / 2)),  # Y position
                    int(self.token_size / 2 - 5)  # Radius
                )
      
             
    def on_render(self):
            self._display_surf.fill((255, 255, 255))
            self.draw_board(self._display_surf)
            pygame.display.flip()

    def on_execute(self):
            pygame.init()
            width = self.column_count * self.token_size
            height = (self.row_count + 1) * self.token_size
            self._display_surf = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Connect 4")

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                self.on_render()
            pygame.quit()
        
if __name__ == "__main__":
    game = Connect4()
    game.on_execute()


