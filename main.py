"""
    main function
"""
#imports
from threading import Thread
import Assets, pygame, sys, json

pygame.init()#init

with open("saves.json", 'r') as file:#get save file
    saves = json.load(file)#convert to json

#init vars
SIZE = saves["size"]
BOARDSIZE = saves["boardSize"]
FPS = saves["fps"]

#init pygame window
WIN = pygame.display.set_mode((SIZE, SIZE+50))# sets window
pygame.display.set_caption("Minesweeper")#sets caption
pygame.display.set_icon(pygame.image.load("Assets/textures/bomb.png"))#sets icon
board = Assets.Board(BOARDSIZE, (SIZE, SIZE+50))#sets board
clock = pygame.time.Clock()#sets clock

#draws the display
def drawDisplay():
    WIN.fill((255, 255, 255))#fills the window with white
    board.draw(WIN)#draws the board

    pygame.display.update()#updates the display

#main function
def main():
    #game loop
    while True:
        displayThread = Thread(target=drawDisplay)#init thread
        displayThread.start()#start thread

        #get events
        for event in pygame.event.get():
            #exit
            if event.type == pygame.QUIT:
                sys.exit()
            #mouse movements
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if pygame.mouse.get_pressed()[0]:
                    board.lClick(pygame.mouse.get_pos())
                #right click
                elif pygame.mouse.get_pressed()[2]:
                    board.rClick(pygame.mouse.get_pos())
            #reset keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()

        clock.tick(FPS)#fps

        displayThread.join()#joins the thread

#if the file is not being imported start automatically
if __name__ == '__main__':
    main()