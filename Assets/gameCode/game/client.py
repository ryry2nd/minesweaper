from threading import Thread
from Assets.gameCode.backend.vars import *
from Assets.gameCode.backend.objects import Board, Piece
from Assets.gameCode.gui.errors import *
import pygame, socket, pickle, sys

loading = True

def recvBoard(board) -> list:
    retBoard = []
    for x in range(len(board)):
        retBoard.append([])
        for y in range(len(board[0])):
            retBoard[x].append(Piece.convertData(board[x][y]))
    return retBoard

def updateLoading(server: socket.socket):
    global loading
    try:
        loading = pickle.loads(server.recv(4))
    except EOFError:
        loading = None
    except ConnectionAbortedError:
        loading = None

def startClient(joinIp: str):
    server = socket.socket()
    try:
        server.connect((joinIp, PORT))
    except socket.gaierror:
        ipNotFound(WIN)
        return
    except ConnectionRefusedError:
        ipNotFound(WIN)
        return

    br, bs = pickle.loads(server.recv(1024))
    board = Board(br, bs, False)

    Thread(target=updateLoading, args=(server, )).start()

    while loading:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    server.close()
                    return

        WIN.fill((0, 0, 0))
        WIN.blit(ipFont.render("Joining game", True, (255, 255, 255)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    
    if loading == None:
        return
    
    while True:
        try:
            tempB, board.isEnded, board.timeSoFar = pickle.loads(server.recv(16384))
            board.board = recvBoard(tempB)
        except EOFError:
            break
        #get events
        for event in pygame.event.get():
            #exit
            if event.type == pygame.QUIT:
                sys.exit()
            #mouse movements
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #left click
                if pygame.mouse.get_pressed()[0]:
                    server.sendall(pickle.dumps((0, pygame.mouse.get_pos())))
                #right click
                elif pygame.mouse.get_pressed()[2]:
                    server.sendall(pickle.dumps((1, pygame.mouse.get_pos())))
            #keys
            elif event.type == pygame.KEYDOWN:
                #reset board
                if event.key == pygame.K_r:
                    server.sendall(pickle.dumps((2)))
                #escape
                elif event.key == pygame.K_ESCAPE:
                    return

        WIN.fill((255, 255, 255))
        board.draw(WIN)
        pygame.display.update()
        clock.tick(FPS)