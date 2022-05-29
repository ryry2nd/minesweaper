from Assets.gameCode.backend.vars import *
import pygame

def ipNotFound(WIN: pygame.Surface):
    WIN.fill((0, 0, 0))
    WIN.blit(ipFont.render("Ip not found", True, (255, 255, 255)), (0, 0))
    pygame.display.update()
    pygame.time.delay(3000)