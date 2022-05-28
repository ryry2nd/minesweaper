"""
gets the server
"""
#imports
import pygame, sys
from Assets.gameCode.gui.inputIp import *
from Assets.gameCode.backend.vars import *

#inits
pygame.init()
pygame.font.init()

#fonts
SERVER_TEXT = defaultFont.render(
    str("Chose the IP of the player you want to join"), 1, (255, 255, 255))

#defines main function
def getServer():
    inputL = InputIp()#inits the ip class

    #define vars
    clock = pygame.time.Clock()

    #game loop
    while True:
        clock.tick(FPS)#fps

        for event in pygame.event.get():#loops through the events
            if event.type == pygame.QUIT:#if it is quit, quit
                sys.exit()
            elif event.type == pygame.KEYDOWN:# runs when a key is pressed
                if event.key == pygame.K_ESCAPE:# if escape is pressed, escape
                    return False
                elif event.key == pygame.K_RETURN:# if return is pressed return the letters
                    return IP
                else:#otherwise add the key
                    inputL.addkey(event.key)

        WIN.fill((0, 0, 0))#fill the screen

        #adds the text
        WIN.blit(SERVER_TEXT, (0, SIZE/2 - 100))
        inputL.placeText(WIN, (0, SIZE/2 - 200))

        pygame.display.update()#updates the display