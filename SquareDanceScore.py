import os, sys
import pygame
from pygame.locals import *
import math

class SquareDanceScore:

    def __init__(self):
        self.currentScore = 0
        self.currentScoreStr = str(self.currentScore)
        self.comboVal = 0


    def get_score(self):
        return self.currentScore

    def get_scoreStr(self):
        return self.currentScoreStr

    def update_score(self, updateValue):
        self.currentScore += updateValue
        self.currentScoreStr = str(self.currentScore)
        return True

    def calculate_newScore(self, comboCount, blockCount):
        self.currentScore += 10*blockCount*comboCount
        self.currentScoreStr = str(self.currentScore)
        return True
