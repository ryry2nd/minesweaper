"""
    main
"""
#imports
from Assets import *
import pygame, sys

pygame.init()#init

#init pygame window
pygame.display.set_caption("Minesweeper")#sets caption
pygame.display.set_icon(pygame.image.load("Assets/textures/bomb.png"))#sets icon
clock = pygame.time.Clock()#sets clock

#main function
def main():
    while True:#game loop
        #loop through the events
        for event in pygame.event.get():
            #quit
            if event.type == pygame.QUIT:
                sys.exit()
            #keys
            elif event.type == pygame.KEYDOWN:# runs when a key is pressed
                #escape
                if event.key == pygame.K_ESCAPE:# if escape is pressed, escape
                    sys.exit()

        WIN.fill((0, 0, 0))# fills the screen

        #if the box is clicked, start a single player game
        if clickWindow(WIN, (100, 100), "Single", "Player"):
            startSingleplayer()
            
        #if the box is clocked go to the find a game code
        elif clickWindow(WIN, (300, 100), "Join a", "Server"):
            IP = getServer()#asks for the ip
            if IP:
                pass
                #client(IP)# finds the ip

        #if the box is clicked make a server
        elif clickWindow(WIN, (500, 100), "Be a", "Server"):
            pass

        pygame.display.update()#update the display
        clock.tick(FPS)#fps

#if it is not being imported automatically run main
if __name__ == '__main__':
    main()