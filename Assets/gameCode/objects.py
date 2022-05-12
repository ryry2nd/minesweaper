import pygame, random

pygame.init()

numberImgs = []
for i in range(9):
    numberImgs.append(pygame.image.load(f"Assets/textures/number{i}.png"))
flagImg = pygame.image.load("Assets/textures/flag.png")
hiddenImg = pygame.image.load("Assets/textures/hidden.png")
bombImg = pygame.image.load("Assets/textures/bomb.png")
explodedBombImg = pygame.image.load("Assets/textures/explodedBomb.png")
notABombImg = pygame.image.load("Assets/textures/notABomb.png")

class TooManyBombs(Exception):
    pass

def putTheNumberOn(WIN: pygame.surface, img: pygame.image, rect: pygame.Rect, size: int) -> None:
    scaledImg = pygame.transform.scale(img, (size, size))
    WIN.blit(scaledImg, rect)

class Number:
    isHidden = True
    isFlaged = False
    isBomb = False
    num = None
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.surface) -> None:
        if not(self.isHidden) and self.isFlaged:
            putTheNumberOn(WIN, notABombImg, self.rect, self.squareSize)
        elif self.isFlaged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, numberImgs[self.num], self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Bomb:
    isHidden = True
    isFlaged = False
    isBomb = True
    win = True
    isExploded = False
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.surface) -> None:
        if self.isExploded:
            putTheNumberOn(WIN, explodedBombImg, self.rect, self.squareSize)
        elif self.isFlaged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, bombImg, self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Board:
    def __init__(self, board_res: tuple, res: tuple, numBombs: int) -> None:
        global numberImgs, bombImg, hiddenImg, flagImg, explodedBombImg, notABombImg
        if numBombs > (board_res[0] * board_res[1]):
            raise TooManyBombs("There can't be more bombs than pieces")

        self.isEnded = False
        self.numBombs = numBombs
        self.WIDTH = res[0]
        self.HEIGHT = res[1]
        self.board_res = board_res
        self.squareSize = res[1]/board_res[1]
        self.board = [[Number(pygame.Rect(x*self.squareSize, y*self.squareSize, self.squareSize, self.squareSize), self.squareSize)
            for y in range(board_res[1])] for x in range(board_res[0])]
        
        for i in range(numBombs):
            while True:
                x = random.randint(0, board_res[0]-1)
                y = random.randint(0, board_res[1]-1)
                xPos = x*self.squareSize
                yPos = y*self.squareSize
                if not self.board[x][y].isBomb:
                    self.board[x][y] = Bomb(pygame.Rect(xPos, yPos, self.squareSize, self.squareSize), self.squareSize)
                    break

        for x in range(board_res[0]):
            for y in range(board_res[1]):
                square = self.board[x][y]
                if not square.isBomb:
                    square.num = self.getNumBombs(x, y)

    def showAll(self) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                self.board[x][y].isHidden = False

    def draw(self, WIN: pygame.surface) -> None:
        for x in self.board:
            for y in x:
                y.draw(WIN)
    
    def lClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and not(square.isFlaged) and not(self.isEnded):
                    if square.isBomb:
                        self.endGame()
                        square.isExploded = True
                        return
                    elif square.isHidden:
                        square.isHidden = False
                    elif self.getNumFlags(x, y) >= self.getNumBombs(x, y):
                        self.selectArea(x, y)
                    if square.num == 0:
                        self.selectArea(x, y)
                    self.checkWin()
                    return
    
    def rClick(self, mousePos: tuple) -> None:
        for x in range(self.board_res[0]):
            for y in range(self.board_res[1]):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and square.isHidden and not(self.isEnded):
                    square.isFlaged = not square.isFlaged
                    self.checkWin()
                    return

    def getNumBombs(self, x: int, y: int) -> int:
        bombs = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isBomb:
                    bombs+=1    
        return bombs
    
    def getNumFlags(self, x: int, y: int) -> int:
        flags = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isFlaged:
                    flags += 1    
        return flags

    emptiesToCheck = []

    def selectArea(self, x: int, y: int) -> None:
        self.emptiesToCheck.append([x,y])
        while self.emptiesToCheck:
            x, y = self.emptiesToCheck.pop()
            self.selectSingleArea(x, y)
        self.emptiesToCheck.clear()

    def selectSingleArea(self, x: int, y: int) -> None:
        for x2 in range(-1, 2):
            for y2 in range(-1, 2):
                localX = x + x2
                localY = y + y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res[1] or localY < 0
                outX = localX >= self.board_res[0] or localX < 0
                if not(center) and not(outX) and not(outY):
                    square = self.board[localX][localY]
                    if square.isHidden and not square.isFlaged:
                        if square.isBomb:
                            self.endGame()
                            square.isExploded = True
                            return
                        square.isHidden = False
                        if square.num == 0:
                            xy=[localX,localY]
                            if xy not in self.emptiesToCheck:
                                self.emptiesToCheck.append(xy)

    def reset(self) -> None:
        self.__init__(self.board_res, (self.WIDTH, self.HEIGHT), self.numBombs)
    
    def checkWin(self) -> None:
        for i in self.board:
            for ii in i:
                if ii.isHidden and not ii.isBomb:
                    return
        for i in self.board:
            for ii in i:
                if ii.isBomb:
                    ii.isFlaged = True
        self.endGame()

    def endGame(self) -> None:
        self.showAll()
        self.isEnded = True