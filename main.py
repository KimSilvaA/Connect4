import pygame
from board import Board
from ui import UI

def main():
    pygame.init()  
    board = Board()  
    ui = UI(board)  
    ui.on_execute()  
    pygame.quit()

if __name__ == "__main__":
    main()
