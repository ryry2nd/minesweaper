from threading import Thread
from Assets.gameCode.backend.objects import Board
from Assets.gameCode.backend.vars import *
from Assets.gameCode.gui.clickWindow import clickWindow
import socket, sys, pickle, pygame

playerConn = []

def getEvents(conn: socket.socket, board: Board):
    conn.settimeout(0.01)
    try:
        event = pickle.loads(conn.recv(512))
        if event[0] == 0:
            board.lClick(event[1])
        elif event[0] == 1:
            board.rClick(event[1])
        elif event[0] == 2:
            board.reset()
    except TimeoutError:
        pass

def look4Players(s: socket.socket):
    global playerConn
    while True:
        try:
            conn, addr = s.accept()
        except OSError:
            break
        
        playerConn.append(conn)
        conn.sendall(pickle.dumps((BOARDSIZE, (SIZE, SIZE+50))))

def sendBoard(board) -> list:
    retBoard = []
    for x in range(len(board)):
        retBoard.append([])
        for y in range(len(board[0])):
            piece = board[x][y]
            if piece.isHidden:
                retBoard[x].append((piece.rect, piece.squareSize, piece.isHidden, piece.isFlagged, None, piece.isExploded, False))
            else:
                retBoard[x].append((piece.rect, piece.squareSize, piece.isHidden, piece.isFlagged, piece.num, piece.isExploded, piece.isBomb))
    return retBoard

def startServer():
    global playerConn
    playerConn.clear()
    board = Board(BOARDSIZE, (SIZE, SIZE+50))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((IP, PORT))
    s.listen()

    Thread(target=look4Players, args=(s, )).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                for conn in playerConn:
                    conn.close()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    s.close()
                    for conn in playerConn:
                        conn.close()
                    return
        
        WIN.fill((0, 0, 0))
        WIN.blit(ipFont.render(f"The IP is {IP}", True, (255, 255, 255)), (0, 0))
        WIN.blit(ipFont.render(f"{len(playerConn)} players joined", True, (255, 255, 255)), (0, 100))
        if playerConn and clickWindow(WIN, (0, 200), "Start"):
            break
        pygame.display.update()
    
    s.close()
    for conn in playerConn:
        try:
            conn.send(pickle.dumps(False))
        except ConnectionResetError:
            playerConn.remove(conn)
    
    while True:
        for conn in playerConn:
            try:
                conn.sendall(pickle.dumps((sendBoard(board.board), board.isEnded, board.timeSoFar)))
            except ConnectionResetError:
                playerConn.remove(conn)

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
                    break
        
        for conn in playerConn:
            getEvents(conn, board)

        WIN.fill((255, 255, 255))
        board.draw(WIN)
        pygame.display.update()

        clock.tick(FPS)
    
    for conn in playerConn:
        conn.close()