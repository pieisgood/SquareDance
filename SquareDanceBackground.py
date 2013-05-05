import os, sys
import pygame
from pygame.locals import *
#a class to hold information about the background
class SquareDanceBackground:

    def __init__(self):
        #frame delta holds the time since the last frame
        #this will allow for proper rendering of the background
        #animations
        self.frameDelta = 0
        self.movie = ''


    
