"""
    imports the variable Board so instead of 
    importing Assets.gameCode...
    you import Assets
"""
#imports
from Assets.gameCode.backend.objects import Board
from Assets.gameCode.game.singleplayer import startSingleplayer
from Assets.gameCode.backend.vars import *
from Assets.gameCode.gui.clickWindow import clickWindow
from Assets.gameCode.gui.getServer import getServer
from Assets.gameCode.game.client import startClient
from Assets.gameCode.game.server import startServer