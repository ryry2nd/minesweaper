"""
    singleplayer game
"""
#imports
from threading import Thread
from Assets.gameCode.backend.vars import *
from Assets.gameCode.backend.objects import Board
import pygame, sys

#init vars
board = Board(BOARDSIZE, (SIZE, SIZE+50))#sets board
clock = pygame.time.Clock()#sets clock

#draws the display
def drawDisplay():
    WIN.fill((255, 255, 255))#fills the window with white
    board.draw(WIN)#draws the board
    pygame.display.update()#updates the display

#main function
def startSingleplayer():
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
            #keys
            elif event.type == pygame.KEYDOWN:
                #reset board
                if event.key == pygame.K_r:
                    board.reset()
                #escape
                elif event.key == pygame.K_ESCAPE:
                    return

        clock.tick(FPS)#fps

        displayThread.join()#joins the thread