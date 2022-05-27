from threading import Thread
import Assets, pygame, sys, json

pygame.init()

with open("saves.json", 'r') as file:
    saves = json.load(file)

SIZE = saves["size"]
BOARDSIZE = saves["boardSize"]
FPS = saves["fps"]

WIN = pygame.display.set_mode((SIZE, SIZE+50))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(pygame.image.load("Assets/textures/bomb.png"))
board = Assets.Board(BOARDSIZE, (SIZE, SIZE+50))
clock = pygame.time.Clock()

def drawDisplay():
    WIN.fill((255, 255, 255))
    board.draw(WIN)

    pygame.display.update()

def main():
    while True:
        displayThread = Thread(target=drawDisplay)
        displayThread.start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    board.lClick(pygame.mouse.get_pos())
                elif pygame.mouse.get_pressed()[2]:
                    board.rClick(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()

        clock.tick(FPS)

        displayThread.join()

if __name__ == '__main__':
    main()