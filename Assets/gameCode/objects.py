import pygame, random

pygame.init()

numberImgs = []

for i in range(9):
    numberImgs.append(pygame.image.load(f"Assets/textures/number{i}.png"))

hiddenImg = pygame.image.load("Assets/textures/hidden.png")

bombImg = pygame.image.load("Assets/textures/bomb.png")

class TooManyBombs(Exception):
    pass

def getNumBombs(x: int, y: int, board: list) -> int:
        bombs = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= len(board[0]) or localY < 0
                outX = localX >= len(board) or localX < 0
                if not(center) and not(outX) and not(outY) and board[localX][localY].isBomb:
                    bombs+=1    
        return bombs

class Number:
    isHidden = True
    isFlaged = False
    isBomb = False
    num = None
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def draw(self, WIN: pygame.surface) -> None:
        if not self.isHidden:
            WIN.blit(numberImgs[self.num], self.rect)
        else:
            WIN.blit(hiddenImg, self.rect)

class Bomb:
    isHidden = True
    isFlaged = False
    isBomb = True
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect

    def draw(self, WIN: pygame.surface) -> None:
        if not self.isHidden:
            WIN.blit(bombImg, self.rect)
        else:
            WIN.blit(hiddenImg, self.rect)

class Board:
    def __init__(self, board_res: tuple, res: tuple, numBombs: int) -> None:
        global numberImgs, bombImg, hiddenImg
        if numBombs > (board_res[0]*board_res[1]):
            raise TooManyBombs("There can't be more bombs than pieces")
        
        for i in range(9):
            numberImgs[i] = pygame.transform.scale(numberImgs[i], (res[1]/board_res[1], res[1]/board_res[1]))
        bombImg = pygame.transform.scale(bombImg, (res[1]/board_res[1], res[1]/board_res[1]))
        hiddenImg = pygame.transform.scale(hiddenImg, (res[1]/board_res[1], res[1]/board_res[1]))

        self.numBombs = numBombs
        self.WIDTH = res[0]
        self.HEIGHT = res[1]
        self.board = []
        bombs = [[False for i in range(board_res[1])] for i in range(board_res[0])]
        
        for i in range(numBombs):
            while True:
                x = random.randint(0, board_res[0]-1)
                y = random.randint(0, board_res[1]-1)
                if not bombs[x][y]:
                    bombs[x][y] = True
                    break

        for x in range(board_res[0]):
            self.board.append([])
            for y in range(board_res[1]):
                if bombs[x][y]:
                    xPos = res[1]/board_res[1] * x
                    yPos = res[1]/board_res[1] * y
                    self.board[x].append(Bomb(pygame.Rect(xPos, yPos, res[1]/board_res[1], res[1]/board_res[1])))
                else:
                    xPos = res[1]/board_res[1] * x
                    yPos = res[1]/board_res[1] * y
                    self.board[x].append(Number(pygame.Rect(xPos, yPos, res[1]/board_res[1], res[1]/board_res[1])))

        for x in range(board_res[0]):
            for y in range(board_res[1]):
                if not self.board[x][y].isBomb:
                    self.board[x][y].num = getNumBombs(x, y, self.board)
    def draw(self, WIN: pygame.surface) -> None:
        for x in self.board:
            for y in x:
                y.draw(WIN)
    
    def keyPress(self, mousePos: tuple) -> None:
        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                if self.board[x][y].rect.collidepoint(mousePos):
                    self.board[x][y].isHidden = False
                    break