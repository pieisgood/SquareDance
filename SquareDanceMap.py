import os, sys
import pygame
from pygame.locals import *
from SquareDanceBlock import *
from SquareDanceBar import *

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

#A class that represents the playing field
class SquareDanceMap:

    def __init__(self, width, height):
        self.field = [[None for x in xrange(12)] for y in xrange(16)]
        #consider using an N-1xM-1 sized square map
        #this will ensure the ability to draw the squares in their
        #proper location when the time comes in the view/controller
        self.squares = [[None for x in xrange(12)] for y in xrange(16)]
        self.blocksToDrop = []
        self.positions = SquareDancePositionMap(width, height)
        self.pDelta = self.positions.get_pdelta()*14
        self.aGroup = None
	self.nextGroupQueue = [None]*4
	self.bar = SquareDanceBar(self.positions, 10000)
	self.combo = 0
	self.highlights = [[None for x in xrange(12)] for y in xrange(16)]
	self.sequential = [[None for x in xrange(12)] for y in xrange(16)]
	self.width = width
	self.height = height
		
	for x in xrange(4):
		self.nextGroupQueue[x] = Group()
		
	self.aGroup = Group()

    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
		
    def get_active_group(self):
	return self.aGroup

    def get_bar(self):
        return self.bar
		
    def get_field(self):
	return self.field

    def get_position_map(self):
        return self.positions

    def get_combo(self):
        #combo code goes here
        comboR = str(self.combo)
        #print comboR
        #self.combo = 0
        return comboR

    def get_sequential(self):
        return self.sequential

    def game_check(self):
        for x in range(16):
            for y in range(2):
                if self.field[x][y] != None:
                    return False
        return True
        
        

    def delete_sequential(self):
        location = self.bar.get_position()
        location = location.get_x()
        empty = True
        deleted_something = 0

        for x in range(15):
            column_one = self.positions.get_coords(x,0)
            column_two = self.positions.get_coords(x+1,0)
            column_one = column_one.get_x()
            column_two = column_two.get_x()
            
            if  location > column_one and column_two > location:
                for y in range(12):
                    self.sequential[x][y] = self.squares[x][y]
                    if self.sequential[x][y] == True:
                        empty = False

        if empty == True :
            
            for x in range(16):
                for y in range(12):
                    if self.sequential[x][y]:
                        self.sequential[x][y] = None
                        self.squares[x][y] = None
                        self.field[x][y] = None
                        self.highlights[x][y] = None
                        deleted_something += 1
            if deleted_something > 0 :
                return True
        else:
            return False

	
    def insert_group(self, in_group):
    	for x in [0,1,2,3]:
            tempB = in_group.get_block(x)
            location = tempB.get_place()
            self.insert_block(tempB, location[0], location[1] )
    	return True

    def delete_block(self, row, column):
        self.field[row][column] = None

    def insert_block(self, newBlock, row, column):
        self.field[row][column] = newBlock
        tposition = self.positions.get_coords(row,column)
        newBlock.set_currPosition(tposition.get_x(), tposition.get_y())
        return True

    def square_highlights_check(self):
        for x in range(15):
            for y in range(11):
                if self.squares[x][y] and self.squares[x+1][y] \
                   and self.squares[x][y+1] and self.squares[x+1][y+1] :
                    if self.field[x][y] != None and self.field[x+1][y] != None and self.field[x][y+1] != None and self.field[x+1][y+1] != None:
                        if self.field[x][y].get_color() == self.field[x][y+1].get_color() == self.field[x+1][y].get_color() == self.field[x+1][y+1].get_color(): 
                            self.highlights[x][y] = self.field[x][y]

        return True

    def get_highlights(self):
        return self.highlights
        
    def new_map(newMap):
        i = 0
        j = 0

        while i < 10:
            j = 0
            while j < 16:
                newMap.field[i][j] = self.field[i][j]
                j += 1
            i += 1

        return newMap

    def smooth_drop(self, msDelta):
        for block in self.blocksToDrop:
            next_place = block.get_place()
            next_position = self.positions.get_coords(next_place[0],next_place[1])
            if (next_position.get_y() - block.get_currPosition().get_y()) < 0 :
                block.set_currPosition(next_position.get_x(),next_position.get_y())
                self.blocksToDrop.remove(block)
                continue
            curr_position = block.get_currPosition()
            updated_y = curr_position.get_y() + (self.pDelta / 1000)*msDelta
            block.set_currPosition(next_position.get_x(), updated_y)

        return True

    def set_active_group(self, group):
        self.aGroup = group
        return True

    def rotate_group(self, direction):
        if direction == pygame.K_d:
            self.aGroup.rotateRight()
        elif direction == pygame.K_a:
            self.aGroup.rotateLeft()

        return True

    def delete_squares(self):
        for x in range(16):
            for y in range(12):
                #print self.squares[x][y]
                if self.squares[x][y] == True:
                    self.field[x][y] = None
                    self.squares[x][y] = None
                    
        self.highlights = [[None for x in xrange(12)] for y in xrange(16)]
        self.combo = 0
        
        return True
        
        

    def find_squares(self):
        for x in range(15):
            for y in range(11):
                if self.field[x][y] != None and self.field[x+1][y] != None and self.field[x][y+1] != None and self.field[x+1][y+1] != None:
                    if self.field[x][y].get_color() == self.field[x+1][y].get_color() == self.field[x+1][y+1].get_color() == self.field[x][y+1].get_color():
                        if self.squares[x][y] == True and self.squares[x+1][y] == True and self.squares[x][y+1] == True and self.squares[x+1][y+1] == True:
                            continue
                        else:
                            self.squares[x][y] = True
                            self.squares[x+1][y] = True
                            self.squares[x][y+1] = True
                            self.squares[x+1][y+1] = True
                            self.combo += 1
                        
        return True

    def drop_blocks(self):

        for x in xrange(16):
            for y in reversed(xrange(12)):
                if self.field[x][y] != None \
                   and y != 11:
                    if self.field[x][y+1] == None:
                        self.blocksToDrop.append(self.field[x][y])
                        tempB = self.field[x][y]
                        tempB.set_place(x, y+1)
                        posfi = self.positions.get_coords(x,y+1)
                        tempB.set_position(posfi.get_x(), posfi.get_y())
                        self.field[x][y+1] = tempB
                        self.field[x][y] = None
            
		
    def try_move(self, direction):
        #code for moving down group goes here
	if self.aGroup:
	    if direction == DOWN:
		tempB = 0
		location = 0
		for x in xrange(0,4,1):
                    #print x
		    tempB = self.aGroup.get_block(x)
		    location = tempB.get_place()
		    #print location[0]
		    #print location[1]
		    if location[1] == 11:
			self.insert_group(self.aGroup)
			self.aGroup = Group()
			return False
		    if self.field[location[0]][location[1]+1] != None:
			self.insert_group(self.aGroup)
			self.aGroup = Group()
			return False
		self.aGroup.move_direction(direction)
	    elif direction == LEFT:
		tempB = 0
		location = 0
    		for x in [0,1,2,3]:
		    tempB = self.aGroup.get_block(x)
		    location = tempB.get_place()
		    if location[0] == 0:
			return False
		    if self.field[location[0]-1][location[1]] != None:
			return False
		self.aGroup.move_direction(direction)
	    elif direction == RIGHT:
    		tempB = 0
		location = 0
		for x in [0,1,2,3]:
		    tempB = self.aGroup.get_block(x)
		    location = tempB.get_place()
		    if location[0] == 15:
                        return False
		    if self.field[location[0]+1][location[1]] != None:
			return False
                self.aGroup.move_direction(direction)
	return True
		
#holds positions for each place in the play field, allows for easier rendering of blocks
class SquareDancePositionMap:

    def __init__(self, width, height):
        self.pMap = [[Position() for x in xrange(12)] for x in xrange(16)]
        self.build_positions(width, height)
        self.position_delta = 0.04*height

    def build_positions(self, width, height):
        for x in xrange(16):
            for y in xrange(12):
                self.pMap[x][y] = Position( 0.5*width - (height*0.05*8) + 0.05*height*x, 0.2*height + 0.05*height*y)
            
        return True

    def get_coords(self, i, j):
        return self.pMap[i][j]

    def get_pdelta(self):
        return self.position_delta

    

        
