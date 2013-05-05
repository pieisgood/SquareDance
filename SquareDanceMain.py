import os, sys
import pygame
from pygame.locals import *
from SquareDanceFactory import SquareFactory
from SquareEventManager import *
from SquareDanceController import *
from SquareDanceState import *
from SquareDanceSList import *

if not pygame.font: print 'NO FONTS!'
if not pygame.mixer: print 'NO SOUND!!'

gFactory = SquareFactory("config.txt")

#A class to handle the main loop of the game and initialization of API elements
class SquareDanceMain:

    def __init__(self, width = 640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.map = None
        self.state = SquareDanceState()
        self.evManager = SquareEventManager()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.menuSystem = SquareMenuController(self.evManager, self.state, gFactory.newSquareMenu(self.state, self.screen, self.width, self.height))
        self.styleList = gFactory.newStyleList( self.screen, self.width, self.height)
        self.sController = gFactory.newSquareController(self.evManager, self.styleList, self.screen, gFactory.createMap(self.width,self.height), self.state)
        self.CPUTicker = SquareCPUController(self.evManager, self.state)
        self.KeyBoard = SquareKeyBoardController( self.evManager, self.state)

    def MainLoop(self):
        self.CPUTicker.Run()
                





if __name__ == "__main__":
    Game = SquareDanceMain(1280, 720)
    Game.MainLoop()
                    
