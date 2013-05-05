import os, sys
import pygame
from pygame.locals import *
import math
import random

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
#A class built to handle the Real valued position of a block or element
class Position:

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def set_position(self,x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def distance(self, x,y):
        return math.sqrt((self.x - x)*(self.x - x) + (self.y - y)*(self.y - y))
    
    
#A class meant to represent each block and the color of the block
class Block:

    def __init__(self, color):
        self.color = color
        self.position = Position(0,0)
        self.currPosition = Position(0,0)
        self.place = [0, 0]

    def set_position(self, x,y):
        self.position.set_position(x,y)

    def get_position(self):
        return self.position

    def set_color(self, newColor):
        self.color = newColor

    def get_currPosition(self):
        return self.currPosition

    def set_currPosition(self, x, y):
        self.currPosition.set_position(x,y)
        return True

    def get_color(self):
        return self.color

    def set_place(self, i, j):
        self.place = [i, j]
        return True

    def get_place(self):
        return self.place

        

class Group:

    def __init__(self):
        #self.newBlock = Block(None)
        self.quad = [Block(None),Block(None),Block(None),Block(None)]
        self.rand = 0
        for i in xrange(4):
            self.rand = random.random()
            if self.rand > 0.5:
                self.quad[i].set_color('one')
            else:
                self.quad[i].set_color('two')

        self.quad[0].set_place(10, 0)
        self.quad[1].set_place(10, 1)
        self.quad[2].set_place(11, 0)
        self.quad[3].set_place(11, 1)

    def rotateRight(self):
        location = self.quad[0].get_place()
        self.quad[0].set_place(location[0]+1, location[1])
        location = self.quad[1].get_place()
        self.quad[1].set_place(location[0], location[1]-1)
        location = self.quad[2].get_place()
        self.quad[2].set_place(location[0], location[1]+1)
        location = self.quad[3].get_place()
        self.quad[3].set_place(location[0]-1, location[1])
        location = 0
        
        placeholder = self.quad[0]
        self.quad[0] = self.quad[1]
        self.quad[1] = self.quad[3]
        self.quad[3] = self.quad[2]
        self.quad[2] = placeholder

         
        return True

    def rotateLeft(self):
        location = self.quad[0].get_place()
        self.quad[0].set_place(location[0], location[1]+1)
        location = self.quad[1].get_place()
        self.quad[1].set_place(location[0]+1, location[1])
        location = self.quad[2].get_place()
        self.quad[2].set_place(location[0]-1, location[1])
        location = self.quad[3].get_place()
        self.quad[3].set_place(location[0], location[1]-1)
        location = 0
        
        placeholder = self.quad[0]
        self.quad[0] = self.quad[2]
        self.quad[2] = self.quad[3]
        self.quad[3] = self.quad[1]
        self.quad[1] = placeholder

        
        return True

        

    def get_block(self, i):
        return self.quad[i]
		
    def move_direction(self, direction):
		
	if direction == DOWN:
	    for x in self.quad:
		x.set_place(x.get_place()[0], x.get_place()[1]+1)
	elif direction == LEFT:
            for x in self.quad:
		x.set_place(x.get_place()[0] - 1, x.get_place()[1])
	elif direction == RIGHT:
            for x in self.quad:
		x.set_place(x.get_place()[0] + 1, x.get_place()[1])
            

    
                    
        
