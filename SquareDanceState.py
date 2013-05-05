import os, sys
import pygame
from pygame.locals import *

#this is a state system setup

class SquareDanceState:

    def __init__(self):

        self.currentState = "Start"


    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
        return True
