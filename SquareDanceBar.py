import os, sys
import pygame
from pygame.locals import *
from SquareDanceBlock import *

class SquareDanceBar:

    def __init__(self, pMap, timeInterval):
        #counts the number of square combos in the current cycle of
        #square counting
        self.comboCount = "0"
        self.position = Position(0,0)
        #used to tell which column the bar is over
        self.location = 0
        self.pMap = pMap
        self.timeInterval = timeInterval
        self.location_one = pMap.get_coords(0,0)
        self.location_two = pMap.get_coords(15,0)
        self.position.set_position(self.location_one.get_x(), self.location_one.get_y())
        self.position_interval = self.location_two.get_x() - self.location_one.get_x()
        print self.position_interval
        self.delta = self.position_interval / self.timeInterval
        print self.delta
        print self.location_one.get_x()
        print self.position.get_x()

    def update_position(self, x):
        #print x
        self.position.set_position(x,self.position.get_y())
        return True

    def update_location(self, column):
        self.location = column
        return True

    def update_comboCount(self, sCombo):
        self.comboCount = sCombo

    def new_position(self, ms):
        x = ms * self.delta + self.location_one.get_x()
        #nx = x + self.position.get_x()
        nx = x 
        #print nx
        self.update_position(x)
        return True

    def get_position(self):
        #print self.position.get_x()
        return self.position
        
        

    
