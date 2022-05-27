from Assets.gameCode.vars import *
import pygame, random, time

pygame.init()
pygame.font.init()

class TooManyBombs(Exception):
    pass

def putTheNumberOn(WIN: pygame.Surface, img: pygame.image, rect: pygame.Rect, size: int) -> None:
    scaledImg = pygame.transform.scale(img, (size, size))
    WIN.blit(scaledImg, rect)

class Number:
    isHidden = True
    isFlagged = False
    isBomb = False
    num = None
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.Surface) -> None:
        if not(self.isHidden) and self.isFlagged:
            putTheNumberOn(WIN, notABombImg, self.rect, self.squareSize)
        elif self.isFlagged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, numberImgs[self.num], self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Bomb:
    isHidden = True
    isFlagged = False
    isBomb = True
    win = True
    isExploded = False
    def __init__(self, rect: pygame.Rect, squareSize: int) -> None:
        self.rect = rect
        self.squareSize = squareSize

    def draw(self, WIN: pygame.Surface) -> None:
        if self.isExploded:
            putTheNumberOn(WIN, explodedBombImg, self.rect, self.squareSize)
        elif self.isFlagged:
            putTheNumberOn(WIN, flagImg, self.rect, self.squareSize)
        elif not self.isHidden:
            putTheNumberOn(WIN, bombImg, self.rect, self.squareSize)
        else:
            putTheNumberOn(WIN, hiddenImg, self.rect, self.squareSize)

class Board:
    def __init__(self, board_res: int, res: tuple) -> None:
        global numberImgs, bombImg, hiddenImg, flagImg, explodedBombImg, notABombImg
        if (board_res**2)//10 > board_res ** 2:
            raise TooManyBombs("There can't be more bombs than pieces")

        self.startTime = time.time()
        self.timeSoFar = 0
        self.headerHgt = 50
        self.isEnded = False
        self.numBombs = (board_res**2)//10
        self.res = self.WIDTH, self.HEIGHT = res
        self.boardWidth = res[0]
        self.boardHeight = res[1] - self.headerHgt
        self.board_res = board_res
        self.squareSize = self.boardHeight/self.board_res
        self.resetRect = pygame.Rect(self.WIDTH//2, 0, self.headerHgt, self.headerHgt)
        self.board = [[Number(pygame.Rect(x*self.squareSize, y*self.squareSize + self.headerHgt, self.squareSize, self.squareSize), self.squareSize)
            for y in range(board_res)] for x in range(board_res)]
        
        for i in range(self.numBombs):
            while True:
                x = random.randint(0, board_res-1)
                y = random.randint(0, board_res-1)
                xPos = x*self.squareSize
                yPos = y*self.squareSize + self.headerHgt
                if not self.board[x][y].isBomb:
                    self.board[x][y] = Bomb(pygame.Rect(xPos, yPos, self.squareSize, self.squareSize), self.squareSize)
                    break

        for x in range(board_res):
            for y in range(board_res):
                square = self.board[x][y]
                if not square.isBomb:
                    square.num = self.getNumBombs(x, y)

    def showAll(self) -> None:
        for x in range(self.board_res):
            for y in range(self.board_res):
                self.board[x][y].isHidden = False
    
    def flagsLeft(self) -> int:
        numFlags = 0
        for i in self.board:
            for ii in i:
                if ii.isFlagged:
                    numFlags += 1
        
        return self.numBombs - numFlags

    def draw(self, WIN: pygame.Surface) -> None:
        if not self.isEnded:
            self.timeSoFar = time.time() - self.startTime
            
        second = self.timeSoFar % 60
        minute = int(self.timeSoFar - second) // 60

        WIN.blit(defaultFont.render("Time Playing:", True, (0, 0, 0)), (0, 0))
        WIN.blit(defaultFont.render(f"{minute:0>2}:{second:0>5.2f}", True, (0, 0, 0)), (0, 25))
        WIN.blit(defaultFont.render("Flags:", True, (0, 0, 0)), (self.WIDTH-100, 0))
        WIN.blit(defaultFont.render(str(self.flagsLeft()), True, (0, 0, 0)), (self.WIDTH-100, 25))
        putTheNumberOn(WIN, resetImg, self.resetRect, self.headerHgt)
        for x in self.board:
            for y in x:
                y.draw(WIN)

    def lClick(self, mousePos: tuple) -> None:
        if self.resetRect.collidepoint(mousePos):
            self.reset()
            return

        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and not(square.isFlagged) and not(self.isEnded):
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
        for x in range(self.board_res):
            for y in range(self.board_res):
                square = self.board[x][y]
                if square.rect.collidepoint(mousePos) and square.isHidden and not(self.isEnded) and (self.flagsLeft() or square.isFlagged):
                    square.isFlagged = not square.isFlagged
                    self.checkWin()
                    return

    def getNumBombs(self, x: int, y: int) -> int:
        bombs = 0
        for x2 in range(-1,2):
            for y2 in range(-1,2):
                localX = x+x2
                localY = y+y2
                center = x2 == 0 and y2 == 0
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
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
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
                if not(center) and not(outX) and not(outY) and self.board[localX][localY].isFlagged:
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
                outY = localY >= self.board_res or localY < 0
                outX = localX >= self.board_res or localX < 0
                if not(center) and not(outX) and not(outY):
                    square = self.board[localX][localY]
                    if square.isHidden and not square.isFlagged:
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
        self.__init__(self.board_res, self.res)

    def checkAllNums(self) -> bool:
        for i in self.board:
            for ii in i:
                if (ii.isHidden and not ii.isBomb):
                    return False
        return True

    def checkWin(self) -> None:
        if not self.isEnded:
            if self.checkAllNums():
                for i in self.board:
                    for ii in i:
                        if ii.isBomb:
                            ii.isFlagged = True
                self.endGame()

    def endGame(self) -> None:
        self.showAll()
        self.isEnded = True